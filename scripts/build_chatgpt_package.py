#!/usr/bin/env python3
"""Build the ZIP that OpenAI's plugin submission portal takes, from chatgpt/.

The review needs a demo video URL, which only exists once someone records the flow, so it is passed in here
rather than committed. Run with --draft to build without it for the portal's automated checks.
"""
import argparse
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "chatgpt"


def build(output: Path, demo_url: str | None, draft: bool) -> Path:
    plugin = json.loads((SOURCE / "plugin.json").read_text(encoding="utf-8"))
    review = plugin["extensions"]["com.openai"]["review"]
    if demo_url:
        review["demo_recording_url"] = demo_url
    if not review.get("demo_recording_url") and not draft:
        sys.exit("A demo video URL is required for review: pass --demo-url, or --draft to build without it.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("plugin.json", json.dumps(plugin, indent=2, ensure_ascii=False) + "\n")
        for path in sorted(SOURCE.rglob("*")):
            if path.is_file() and path.name != "plugin.json":
                archive.write(path, path.relative_to(SOURCE).as_posix())
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo-url", help="Reviewer-accessible URL of the demo recording")
    parser.add_argument("--draft", action="store_true", help="Build without a demo URL")
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "agentdeck-chatgpt.zip")
    args = parser.parse_args()
    print(build(args.output, args.demo_url, args.draft))


if __name__ == "__main__":
    main()
