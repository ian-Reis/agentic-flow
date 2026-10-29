---
name: init
description: Initialize the agentic-flow structure (Owner / Director / Builders, task queue, decision log, reports, handoff) in the current project. Run it once at the start of a new project. Safe on projects that already have docs/ - the flow then goes into docs/agentic/ and nothing existing is touched.
argument-hint: "[project name]"
disable-model-invocation: true
---

# /agentic-flow:init

Initialize the agentic-flow structure in the current working directory. You act as the **Director** for this session. The method itself (roles, queue, prompts, reports) is described in the sibling skill at `${CLAUDE_PLUGIN_ROOT}/skills/agentic-flow/SKILL.md`; read `${CLAUDE_PLUGIN_ROOT}/skills/agentic-flow/references/bootstrap.md` now, because this command is its automated form.

Project name: `$ARGUMENTS` (if empty, use the name of the current directory).

**Flow root.** Everything the flow creates lives under one directory, called `<flow>` below:
- `docs` for a new project (nothing in `docs/` yet, ignoring `.gitkeep`);
- `docs/agentic` when `docs/` already holds files. The project's own documentation is never moved, renamed, edited or linted; the flow sits beside it.

The scaffold script decides this itself and prints `FLOW_ROOT=<dir>` on its last line. Use that value for every path below.

## 1. Check the starting point

Look at the project root before changing anything.

- **`docs/flow/` or `docs/agentic/flow/` already exists** -> the flow is already set up. Do not scaffold again. Tell the Owner, run the lint (step 6), and offer to resume: read `CLAUDE.md`, `<flow>/flow/context.md`, `QUEUE.md`, `DECISIONS.md`, `HANDOFF.md` and report the state of the queue. Stop here.
- **Anything else** (empty directory, code only, or a project with its own `docs/` and/or `CLAUDE.md`) -> continue. No confirmation is needed for existing docs: the install is non-destructive and isolated. You will say what you did in the final message.

## 2. Learn the project from the repository first

Inspect: build and manifest files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `*.csproj`...), existing `README`, test folders, CI config, and any existing `CLAUDE.md` or `docs/`. Infer the language, the commands to build, run and test, and the probable source of truth.

Then ask the Owner **one short round** of questions (AskUserQuestion, up to 4 questions), only for what you could not infer and that matters:

1. What the project is and what the first milestone's "done" looks like.
2. The source of truth: where edits happen, and what is generated or mirrored and must never be hand-edited.
3. Hard rules: security, data, things never to touch.
4. Will several agents run in parallel (affects how strictly `Areas` are used)? Should model routing be used?

Never guess an answer. Anything still unknown is written as a single line `TODO (owner): <question>` so it stays visible.

## 3. Scaffold

Run the bundled script from the project root (try `python`, then `python3`, then `py`):

```
python "${CLAUDE_PLUGIN_ROOT}/skills/agentic-flow/scripts/init_project.py" --target "." --name "<Project name>"
```

It creates `CLAUDE.md` and the flow tree (`README.md`, `flow/`, `tasks/`, `reports/`, `systems/`) under `<flow>`, and skips any file that already exists. Read its output: every `skipped` line is a file of the project that you must not overwrite.

If no Python is available (on Windows `python3` is sometimes only a Microsoft Store stub that prints "Python was not found"), do it by hand: decide `<flow>` by the rule above, then copy every file under `${CLAUDE_PLUGIN_ROOT}/skills/agentic-flow/assets/templates/` into the project - `CLAUDE.md` to the root, and each `docs/...` template to `<flow>/...` - replacing `{{PROJECT_NAME}}` with the project name, `{{DATE}}` with today's date and `{{DOCS}}` with `<flow>`; skip files that exist; create `<flow>/tasks/done/` and `<flow>/systems/` with an empty `.gitkeep` in each.

### If the project already had its own files

- **Existing `CLAUDE.md`** (the script skipped it): append, never rewrite. Add at the end a `## Agentic flow` section with the "Working method" paragraph and, in its index table if it has one, a row for the flow, taking the text from `assets/templates/CLAUDE.md` with `{{DOCS}}` replaced by `<flow>`. Leave every existing line as it is.
- **Isolated install and the project has a docs index** (`docs/README.md`, `docs/index.md`): append one line linking to `agentic/README.md`. Do not touch anything else in it.
- Mention both edits to the Owner, with the exact lines added.

## 4. Fill the files that carry the project

Edit, using what you learned in step 2 (replace the `<...>` placeholders; do not leave template prose that is untrue). If `CLAUDE.md` was the project's own, put the commands, source of truth and invariants into `<flow>/flow/context.md` instead and only link to it from the appended section.

- `CLAUDE.md` (when created by the scaffold): what this is, the commands table, source of truth, invariants, and the index.
- `<flow>/flow/context.md`: required reading, source of truth, rules that break everything, how to test (with *when each check is mandatory*), standards, and **current priorities**.
- Record in `<flow>/flow/DECISIONS.md` each decision the Owner gave you during the questions (`D001`, `D002`...), dated today. A choice you made yourself is marked `(director, pending Owner confirmation)`.

Keep each file as short as the project allows: every agent reads them every time.

## 5. Seed the first task: the safety net

Create `<flow>/tasks/001-test-baseline.md` from `<flow>/tasks/_TEMPLATE.md` and add its row to `<flow>/flow/QUEUE.md` with status `draft` (the Owner approves it, then you set `ready`):

```
| 001 | Establish test baseline | - | tests | draft | - |
```

- If the project already has code: the task is to add unit tests for what exists and a single-command smoke/end-to-end check, and to record the commands in `context.md` (and `CLAUDE.md` when you own it).
- If there is no code yet: the task is to decide and document how the project will be tested, and to create the first passing check.

Without a way to prove work, later tasks rest on assumption, so this comes before features.

## 6. Lint and hand over

Run `python "${CLAUDE_PLUGIN_ROOT}/skills/agentic-flow/scripts/lint_docs.py" "."` (same interpreter fallback; if none exists, check by eye that every queue row has a task file and links resolve). It finds `<flow>` on its own and, for an isolated install, checks only the flow's files. Fix every error.

Finish with a short message to the Owner (no more than ~15 lines):

- the flow root you used, and why (`docs/agentic/` means their existing docs were left untouched);
- what was created, what you filled in, and any line you appended to their `CLAUDE.md` or docs index;
- the decisions you recorded, and the ones you made on their behalf that they should confirm;
- the open `TODO (owner)` lines;
- what they must do: approve task `001` (say "approve 001"), and anything only a human can do;
- the phrase to open Builder sessions in other windows (with the real path):

> Read `<flow>/flow/context.md` and follow the Builder loop of the `agentic-flow` skill. You are a Builder. Take the next `ready` task from `<flow>/flow/QUEUE.md`.

Do not start implementing any task in this session. Initializing is the Director's job; building starts only after the Owner approves.
