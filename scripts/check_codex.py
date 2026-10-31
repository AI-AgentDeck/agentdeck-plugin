#!/usr/bin/env python3
"""Check native Codex installation, skills and authenticated MCP discovery without model calls."""

import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


ROOT = Path(__file__).resolve().parents[1]


class Fixture(BaseHTTPRequestHandler):
    requests_seen = []
    version = None

    def log_message(self, *args):
        pass

    def do_GET(self):
        self.send_response(405)
        self.end_headers()

    def do_POST(self):
        if self.headers.get("Authorization") != "Bearer adk_synthetic_smoke" or \
                self.headers.get("X-Agentdeck-Plugin-Version") != self.version:
            self.send_response(401)
            self.end_headers()
            return
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        method = data.get("method")
        self.requests_seen.append(method)
        if "id" not in data:
            self.send_response(202)
            self.end_headers()
            return
        if method == "initialize":
            result = {"protocolVersion": data["params"]["protocolVersion"], "capabilities": {"tools": {}},
                      "serverInfo": {"name": "agentdeck-fixture", "version": "1"}}
        elif method == "tools/list":
            result = {"tools": [{"name": "whoami", "description": "Synthetic identity",
                                 "inputSchema": {"type": "object", "properties": {}}}]}
        elif method == "resources/list":
            result = {"resources": []}
        elif method == "resources/templates/list":
            result = {"resourceTemplates": []}
        else:
            result = {}
        body = json.dumps({"jsonrpc": "2.0", "id": data["id"], "result": result}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def inspect_runtime(environment, cwd, overrides=()):
    process = subprocess.Popen(["codex", *overrides, "app-server"], env=environment, cwd=cwd,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, text=True)
    responses = queue.Queue()

    def read():
        for line in process.stdout:
            try:
                responses.put(json.loads(line))
            except ValueError:
                pass

    reader = threading.Thread(target=read, daemon=True)
    reader.start()

    def rpc(identifier, method, params):
        process.stdin.write(json.dumps({"jsonrpc": "2.0", "id": identifier,
                                        "method": method, "params": params}) + "\n")
        process.stdin.flush()
        while True:
            response = responses.get(timeout=30)
            if response.get("id") == identifier:
                if "error" in response:
                    raise ValueError("Codex rejected " + method)
                return response["result"]

    try:
        rpc(1, "initialize", {"clientInfo": {"name": "agentdeck-smoke", "version": "1"},
                              "capabilities": {"experimentalApi": True}})
        skills = rpc(2, "skills/list", {"cwds": [str(cwd)], "forceReload": True})
        names = {skill["name"] for row in skills["data"] for skill in row["skills"]
                 if skill.get("pluginId") == "agentdeck@agentdeck"}
        expected = {"agentdeck:" + name for name in ["create-agent", "update-agent", "test-agent", "go-live"]}
        if names != expected or any(row["errors"] for row in skills["data"]):
            raise ValueError("Codex did not discover all four valid AgentDeck skills")
        servers = rpc(3, "mcpServerStatus/list", {})["data"]
        server = next((item for item in servers if item["name"] == "agentdeck"), None)
        if not server or server.get("toolsError") or "whoami" not in server["tools"]:
            raise ValueError("Codex could not discover authenticated AgentDeck tools")
        if server["httpOrigin"] != environment["AGENTDECK_MCP_URL"].removesuffix("/mcp"):
            raise ValueError("Codex used an unexpected MCP endpoint")
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        reader.join(timeout=5)
        process.stdin.close()
        process.stdout.close()


def check():
    Fixture.requests_seen = []
    Fixture.version = json.loads((ROOT / "plugins/agentdeck/.codex-plugin/plugin.json").read_text())["version"]
    server = ThreadingHTTPServer(("127.0.0.1", 0), Fixture)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        with tempfile.TemporaryDirectory(prefix="agentdeck-codex-smoke-") as temporary:
            base = Path(temporary)
            source = base / "marketplace"
            shutil.copytree(ROOT / ".agents", source / ".agents")
            plugin = source / "plugins/agentdeck"
            shutil.copytree(ROOT / "plugins/agentdeck", plugin,
                            ignore=shutil.ignore_patterns("evals", "evals-live", "__pycache__"))
            mcp_path = plugin / ".codex.mcp.json"
            mcp = json.loads(mcp_path.read_text())
            endpoint = "http://127.0.0.1:" + str(server.server_port) + "/mcp"
            mcp["mcpServers"]["agentdeck"]["url"] = endpoint
            # The package signs in through a browser; this headless check uses the token path scripts use.
            mcp["mcpServers"]["agentdeck"]["bearer_token_env_var"] = "AGENTDECK_TOKEN"
            mcp_path.write_text(json.dumps(mcp))
            home = base / "codex-home"
            home.mkdir()
            environment = {**os.environ, "CODEX_HOME": str(home),
                           "AGENTDECK_TOKEN": "adk_synthetic_smoke", "AGENTDECK_MCP_URL": endpoint}
            for args in [["plugin", "marketplace", "add", str(source), "--json"],
                         ["plugin", "add", "agentdeck@agentdeck", "--json"]]:
                result = subprocess.run(["codex", *args], env=environment, cwd=base,
                                        capture_output=True, text=True, timeout=30)
                if result.returncode:
                    raise ValueError("Codex could not install the isolated marketplace/plugin")
            inspect_runtime(environment, base)
            # A session override must replace the packaged origin when an environment is selected.
            mcp["mcpServers"]["agentdeck"]["url"] = "http://127.0.0.1:1/mcp"
            installed = home / "plugins/cache/agentdeck/agentdeck" / Fixture.version / ".codex.mcp.json"
            installed.write_text(json.dumps(mcp))
            override = 'mcp_servers.agentdeck={url=' + json.dumps(endpoint) + \
                       ',bearer_token_env_var="AGENTDECK_TOKEN",http_headers={"X-Agentdeck-Plugin-Version"=' + \
                       json.dumps(Fixture.version) + '}}'
            inspect_runtime(environment, base, ["-c", override])
            if "initialize" not in Fixture.requests_seen or "tools/list" not in Fixture.requests_seen:
                raise ValueError("Authenticated fixture discovery did not run")
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)
    print("Codex install, four skills, authenticated MCP discovery and environment override passed (no model calls).")


if __name__ == "__main__":
    check()
