#!/usr/bin/env python3
"""Lint an agentic-flow project: queue vs task/report files, links, sizes, paths.

Usage: lint_docs.py <project-dir> [--max-kb 15] [--docs-dir <flow root>]

The flow root is found automatically: docs/agentic (isolated install, used when the
project already had its own docs/) or docs. When it is isolated, only files inside it
are checked, so the project's own documentation never produces findings.
Exit code 1 if any ERROR is found; warnings do not fail the run.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

STATES = {"draft", "ready", "in-progress", "verify", "blocked", "rework", "done", "superseded"}
OPEN_STATES = {"draft", "ready", "in-progress", "verify", "blocked", "rework"}
NEEDS_REPORT = {"verify", "done"}
CANDIDATE_ROOTS = ["docs/agentic", "docs"]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
PERSONAL_PATH_RE = re.compile(r"[A-Za-z]:\\Users\\[^\\\s`]+|/Users/[\w.-]+|/home/[\w.-]+")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def find_flow_root(project: Path, override: str | None) -> str:
    if override:
        return override.strip("/\\").replace("\\", "/")
    for cand in CANDIDATE_ROOTS:
        if (project / cand / "flow" / "QUEUE.md").is_file():
            return cand
    return "docs"


def parse_queue(path: Path, rep: Report, flow: str) -> list[dict[str, str]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or not re.fullmatch(r"\d{3,}", cells[0]):
            continue
        if len(cells) < 6:
            rep.error(f"{flow}/flow/QUEUE.md: row {cells[0]} has {len(cells)} cells, expected 6")
            continue
        rows.append(dict(zip(["id", "title", "needs", "areas", "status", "builder"], cells)))
    return rows


def check_queue(project: Path, flow: str, rep: Report) -> None:
    base = project / flow
    queue = base / "flow" / "QUEUE.md"
    if not queue.is_file():
        rep.error(f"{flow}/flow/QUEUE.md is missing")
        return
    rows = parse_queue(queue, rep, flow)
    ids = [r["id"] for r in rows]
    for dup in {i for i in ids if ids.count(i) > 1}:
        rep.error(f"QUEUE.md: duplicate ID {dup}")
    by_id = {r["id"]: r for r in rows}

    tasks_dir = base / "tasks"
    reports_dir = base / "reports"
    open_files = {p.name: p for p in tasks_dir.glob("*.md") if not p.name.startswith("_")}
    done_files = {p.name: p for p in (tasks_dir / "done").glob("*.md")} if (tasks_dir / "done").is_dir() else {}
    report_files = [p.name for p in reports_dir.glob("*.md") if not p.name.startswith("_")]

    for r in rows:
        tid, status = r["id"], r["status"]
        if status not in STATES:
            rep.error(f"task {tid}: invalid status '{status}' (valid: {', '.join(sorted(STATES))})")
        if status == "in-progress" and r["builder"] in ("", "-", "—"):
            rep.error(f"task {tid}: in-progress without a Builder name")
        if status in {"ready", "draft"} and r["builder"] not in ("", "-", "—"):
            rep.warn(f"task {tid}: {status} but Builder is set to '{r['builder']}'")

        prefix = f"{tid}-"
        in_open = [n for n in open_files if n.startswith(prefix)]
        in_done = [n for n in done_files if n.startswith(prefix)]
        if not in_open and not in_done:
            rep.error(f"task {tid}: no prompt file {flow}/tasks/{tid}-*.md")
        elif status == "done" and in_open:
            rep.warn(f"task {tid}: done but prompt still in {flow}/tasks/ (move it to {flow}/tasks/done/)")
        elif status in OPEN_STATES and in_done:
            rep.warn(f"task {tid}: {status} but prompt is in {flow}/tasks/done/")

        if status in NEEDS_REPORT and not any(f"-{tid}-" in n for n in report_files):
            rep.error(f"task {tid}: {status} but no report {flow}/reports/*-{tid}-*.md")

        needs = [n.strip() for n in re.split(r"[,\s]+", r["needs"]) if n.strip() and n.strip() not in ("-", "—")]
        for n in needs:
            if n not in by_id:
                rep.error(f"task {tid}: Needs unknown task {n}")
            elif status in {"in-progress", "verify", "done"} and by_id[n]["status"] != "done":
                rep.warn(f"task {tid}: {status} while prerequisite {n} is {by_id[n]['status']}")

    queued = set(ids)
    for name in open_files:
        m = re.match(r"(\d{3,})-", name)
        if not m:
            rep.warn(f"{flow}/tasks/{name}: file name should start with an ID like 012-")
        elif m.group(1) not in queued:
            rep.error(f"{flow}/tasks/{name}: not listed in QUEUE.md")


def iter_docs(project: Path, flow: str):
    """Files to check. In an isolated install only the flow root is ours."""
    if flow == "docs":
        claude = project / "CLAUDE.md"
        if claude.is_file():
            yield claude
    base = project / flow
    if base.is_dir():
        yield from sorted(base.rglob("*.md"))


def check_files(project: Path, flow: str, max_kb: int, rep: Report) -> None:
    for path in iter_docs(project, flow):
        rel = path.relative_to(project).as_posix()
        size = path.stat().st_size
        if size > max_kb * 1024:
            rep.warn(f"{rel}: {size // 1024} KB exceeds {max_kb} KB budget - split by topic")
        in_fence = False
        for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if PERSONAL_PATH_RE.search(line):
                rep.warn(f"{rel}:{n}: personal/absolute machine path")
            for target in LINK_RE.findall(line):
                if re.match(r"[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                file_part = target.split("#", 1)[0]
                if not file_part:
                    continue
                if not (path.parent / file_part).resolve().exists():
                    rep.error(f"{rel}:{n}: broken link '{target}'")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project", help="project root directory")
    parser.add_argument("--max-kb", type=int, default=15)
    parser.add_argument("--docs-dir", default=None, help="flow root relative to the project (default: auto-detect)")
    args = parser.parse_args()
    project = Path(args.project).resolve()
    if not project.is_dir():
        print(f"error: {project} is not a directory", file=sys.stderr)
        return 2

    flow = find_flow_root(project, args.docs_dir)
    print(f"Flow root: {flow}")
    rep = Report()
    check_queue(project, flow, rep)
    check_files(project, flow, args.max_kb, rep)

    for w in rep.warnings:
        print(f"WARN   {w}")
    for e in rep.errors:
        print(f"ERROR  {e}")
    print(f"\n{len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
