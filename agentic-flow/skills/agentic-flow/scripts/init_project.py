#!/usr/bin/env python3
"""Scaffold CLAUDE.md and the flow docs for the agentic-flow method.

Copies assets/templates/ into the target project, replacing {{PROJECT_NAME}},
{{DATE}} and {{DOCS}}. Existing files are never overwritten, so re-running is safe.

Where the flow lives (--docs-dir):
  auto (default)  "docs" for a new project; "docs/agentic" when docs/ already
                  holds files, so the project's own docs are left untouched.
  <path>          use exactly this directory (relative to --target).
The last line printed is FLOW_ROOT=<dir> for callers to parse.
"""
from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "assets" / "templates"
ISOLATED_DIR = "docs/agentic"
EMPTY_DIRS = ["tasks/done", "systems"]


def has_content(folder: Path) -> bool:
    """True if the folder holds anything besides placeholder files."""
    if not folder.is_dir():
        return False
    return any(p.name != ".gitkeep" for p in folder.rglob("*") if p.is_file())


def choose_docs_dir(target: Path, requested: str) -> str:
    if requested != "auto":
        return requested.strip("/\\").replace("\\", "/")
    return ISOLATED_DIR if has_content(target / "docs") else "docs"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", required=True, help="project root directory")
    parser.add_argument("--name", required=True, help="project name")
    parser.add_argument("--docs-dir", default="auto", help="flow root relative to target (default: auto)")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not TEMPLATES.is_dir():
        print(f"error: templates not found at {TEMPLATES}", file=sys.stderr)
        return 2
    target.mkdir(parents=True, exist_ok=True)

    docs_dir = choose_docs_dir(target, args.docs_dir)
    subs = {
        "{{PROJECT_NAME}}": args.name,
        "{{DATE}}": datetime.date.today().isoformat(),
        "{{DOCS}}": docs_dir,
    }
    created, skipped = [], []

    for src in sorted(TEMPLATES.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(TEMPLATES).as_posix()
        if rel == "docs" or rel.startswith("docs/"):
            rel = docs_dir + rel[len("docs"):]
        dest = target / rel
        if dest.exists():
            skipped.append(rel)
            continue
        text = src.read_text(encoding="utf-8")
        for key, value in subs.items():
            text = text.replace(key, value)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8", newline="\n")
        created.append(rel)

    for d in EMPTY_DIRS:
        folder = target / docs_dir / d
        folder.mkdir(parents=True, exist_ok=True)
        if not any(folder.iterdir()):
            (folder / ".gitkeep").touch()

    print(f"Project: {args.name}  ->  {target}")
    print(f"Flow root: {docs_dir}" + ("  (isolated: existing docs/ left untouched)" if docs_dir == ISOLATED_DIR else ""))
    for rel in created:
        print(f"  created  {rel}")
    for rel in skipped:
        print(f"  skipped  {rel} (already exists)")
    print("Next: fill CLAUDE.md and the flow context.md, then run lint_docs.py.")
    print(f"FLOW_ROOT={docs_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
