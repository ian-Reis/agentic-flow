# Docs conventions

These keep the documentation small enough to read and trustworthy enough to act on. Each one exists because its absence has caused a specific failure: bloated context, contradicting copies, dead docs mistaken for live ones.

1. **One topic per document.** When a document starts covering two topics, split it.
2. **One source of truth.** A rule lives in one place; others link to it and never copy it. Copies drift.
3. **Size budget: about 15 KB per document** (`lint_docs.py` warns above it). Huge documents are expensive in every session and invite contradiction. Split by topic and link.
4. **Living versus historical.**
   - *Living* documents (system docs, `context.md`, `CLAUDE.md`) are updated whenever reality changes.
   - *Historical* documents (reports, done tasks) are not edited after writing; a new result is a new report.
   - What stopped being true is deleted or marked superseded, never left mixed in with the live material.
5. **Names:** lowercase, hyphen-separated, saying the topic (`camera-system.md`, not `DOC3.md`). Reports start with the date `YYYY-MM-DD-`. Flow files in `docs/flow/` keep their uppercase names (`QUEUE.md`).
6. **Everything has a home** (below) and an entry in `docs/README.md`.
7. **Moving or renaming a doc means updating every link** to it - `CLAUDE.md`, prompts, other docs, code comments.
8. **No personal data or machine paths** (`C:\Users\name\...`, `/home/name/...`). They rot and leak. Use paths relative to the repo.
9. **Media and binaries stay out of `docs/`.** Put screenshots, videos, archives and generated artifacts in `assets/` (or similar) and link from the doc. Text documentation that is mixed with heavy files gets slow to search and easy to mistake for source.
10. **Language:** this flow's files are written in English. A project may choose another language for its own system docs; say so in `CLAUDE.md`.

## Layout

```
CLAUDE.md                  small entry point: what this is, commands, invariants,
                           source of truth, and an index "task touches X -> read Y"
docs/
  README.md                index + these conventions
  flow/                    context.md, QUEUE.md, DECISIONS.md, QUESTIONS.md, IDEAS.md, HANDOFF.md
  tasks/                   open task prompts; done/ holds finished ones; _TEMPLATE.md
  reports/                 dated reports; _TEMPLATE.md
  systems/                 one living doc per system, created when a system needs one
```

## `CLAUDE.md` as the front door

Keep it short and current. Required sections: **what this is**, **commands** (build, test, run), **invariants** ("what breaks everything if ignored"), **source of truth** (where to edit; what is generated and must never be hand-edited), and **index** mapping a kind of task to the doc to read. Detail belongs in `docs/systems/`; only rules that always apply stay in `CLAUDE.md`.
