#!/usr/bin/env python3
"""Persist portable bundles and stable creation keys without storing environment credentials."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import uuid
from datetime import datetime, timezone


MAX_BYTES = 512 * 1024
ROOT_KEYS = {"schema", "display-name", "agent", "rate-limit", "knowledge-base"}
ENVIRONMENT_PATHS = (
    ("agent", "tenant-id"), ("agent", "legacy-id"), ("agent", "owner-email"),
    ("agent", "api-key"), ("agent", "tenant-status"),
    ("agent", "widget", "domain-languages"),
    ("knowledge-base", "request-cookies"), ("knowledge-base", "own-domains"),
    ("knowledge-base", "domain-languages"), ("knowledge-base", "reset-on-startup"),
)


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def reject_nonfinite(_):
    raise ValueError("non-finite JSON number")


def read_bundle(path):
    raw = sys.stdin.buffer.read(MAX_BYTES + 1) if path == "-" else Path(path).read_bytes()
    if len(raw) > MAX_BYTES:
        raise ValueError("bundle exceeds the backend's 512 KiB limit")
    value = json.loads(raw, object_pairs_hook=unique_keys,
                       parse_constant=reject_nonfinite)
    if not isinstance(value, dict) or not {"schema", "display-name", "agent"} <= value.keys():
        raise ValueError("input must be the bundle object, not an MCP response envelope")
    if value.keys() - ROOT_KEYS:
        raise ValueError("unexpected top-level fields: export only the bundle object")
    if not isinstance(value["schema"], str) or not value["schema"].startswith("agentdeck/agent-bundle@"):
        raise ValueError("not an AgentDeck bundle")
    for path_parts in ENVIRONMENT_PATHS:
        node = value
        for part in path_parts[:-1]:
            node = node.get(part, {}) if isinstance(node, dict) else {}
        if isinstance(node, dict) and path_parts[-1] in node:
            raise ValueError("environment-owned field: " + ".".join(path_parts))
    canonical = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    if len(canonical) > MAX_BYTES:
        raise ValueError("formatted bundle exceeds the backend's 512 KiB limit")
    return canonical


def private_directory(path):
    if path.is_symlink():
        raise ValueError("output directories cannot be symlinks")
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not path.resolve().is_relative_to(Path.cwd().resolve()):
        raise ValueError("output path escapes the workspace")


def atomic_write(path, data):
    if path.is_symlink():
        raise ValueError("output file cannot be a symlink")
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            os.chmod(temporary, 0o600)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
            handle.close()
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)


def persist(command, source, slug, environment=None, replace=False, tenant_id=None):
    if len(slug) > 80 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("slug must contain lowercase words separated by hyphens, at most 80 characters")
    data = read_bundle(source)
    digest = hashlib.sha256(data).hexdigest()
    output = Path("agentdeck") / (slug + ".json")
    private_directory(output.parent)
    if output.is_symlink():
        raise ValueError("bundle destination cannot be a symlink")
    exists = output.exists()
    identical = exists and output.read_bytes() == data
    if exists and not identical and not replace:
        raise ValueError("local bundle differs; use update-agent or explicitly replace the intended local artifact")
    result = {"bundlePath": str(output), "sha256": digest}
    if command == "prepare":
        if tenant_id is not None:
            tenant_id = str(uuid.UUID(tenant_id))
        directory = Path(".agentdeck-work") / slug
        private_directory(directory.parent)
        private_directory(directory)
        state_path = directory / "create.json"
        if state_path.is_symlink():
            raise ValueError("creation state cannot be a symlink")
        try:
            fd = os.open(state_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            state = json.loads(state_path.read_text())
            if (state.get("createBundleHash") != digest or state.get("environment") != environment
                    or state.get("tenantId") != tenant_id):
                raise ValueError("an earlier create used another bundle or environment or workspace; resolve it before creating again")
        else:
            state = {"environment": environment, "tenantId": tenant_id, "idempotencyKey": str(uuid.uuid4()),
                     "createBundleHash": digest, "createdAt": datetime.now(timezone.utc).isoformat()}
            with os.fdopen(fd, "w") as handle:
                json.dump(state, handle, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
        result.update({"statePath": str(state_path), "idempotencyKey": state["idempotencyKey"]})
    if not identical:
        atomic_write(output, data)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "save"])
    parser.add_argument("--input", required=True, help="bundle JSON file, or - for stdin")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--environment", choices=["dev", "prod", "local"])
    parser.add_argument("--tenant-id", help="workspace UUID from whoami for a TENANT token; omit for ADMIN")
    parser.add_argument("--replace", action="store_true", help="replace a deliberately updated local bundle")
    args = parser.parse_args()
    if args.command == "prepare" and (args.environment is None or args.replace):
        parser.error("prepare requires --environment and cannot replace a different bundle")
    try:
        print(json.dumps(persist(args.command, args.input, args.slug, args.environment, args.replace, args.tenant_id)))
    except (OSError, ValueError, KeyError) as error:
        print("Bundle not saved: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
