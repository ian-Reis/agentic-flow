#!/usr/bin/env python3
"""Scaffold CLAUDE.md and docs/ for the agent-flow method.

Copies assets/templates/ into the target project, replacing {{PROJECT_NAME}}
and {{DATE}}. Existing files are never overwritten, so re-running is safe.
"""
from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "assets" / "templates"
EMPTY_DIRS = ["docs/tasks/done", "docs/systems"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="project root directory")
    parser.add_argument("--name", required=True, help="project name")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not TEMPLATES.is_dir():
        print(f"error: templates not found at {TEMPLATES}", file=sys.stderr)
        return 2
    target.mkdir(parents=True, exist_ok=True)

    subs = {"{{PROJECT_NAME}}": args.name, "{{DATE}}": datetime.date.today().isoformat()}
    created, skipped = [], []

    for src in sorted(TEMPLATES.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(TEMPLATES)
        dest = target / rel
        if dest.exists():
            skipped.append(rel.as_posix())
            continue
        text = src.read_text(encoding="utf-8")
        for key, value in subs.items():
            text = text.replace(key, value)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8", newline="\n")
        created.append(rel.as_posix())

    for d in EMPTY_DIRS:
        folder = target / d
        folder.mkdir(parents=True, exist_ok=True)
        keep = folder / ".gitkeep"
        if not any(folder.iterdir()):
            keep.touch()

    print(f"Project: {args.name}  ->  {target}")
    for rel in created:
        print(f"  created  {rel}")
    for rel in skipped:
        print(f"  skipped  {rel} (already exists)")
    print("Next: fill CLAUDE.md and docs/flow/context.md, then run lint_docs.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
