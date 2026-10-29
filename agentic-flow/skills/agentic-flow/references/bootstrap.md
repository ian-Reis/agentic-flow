# Bootstrapping a new project

Done once, by the Director, in the first session. The aim is to leave a state in which a Builder started cold can do useful, verifiable work.

## 1. Gather only what you cannot infer

Look at the directory first (language, build files, tests, existing README). Ask the Owner, in one short message, only what is still unknown and matters:

- What the project is and what "done" looks like for the first milestone.
- How it is built, run and tested (or that none exists yet).
- The **source of truth**: where edits are made, and what is generated or mirrored and must never be edited by hand.
- Hard rules: security, data, things never to touch.
- Whether other agents will run in parallel (affects the `Areas` discipline) and whether the Owner wants model routing.

If the answers are obvious from the repository, do not ask.

## 2. Scaffold

```
python <skill-dir>/scripts/init_project.py --target <project-dir> --name "<Project name>"
```

It creates `CLAUDE.md` and the flow tree from `assets/templates/` and fills in the name, date and paths. It skips files that already exist, so it is safe to re-run. If the project already has files in `docs/`, the flow tree goes into `docs/agentic/` instead (`--docs-dir` overrides the choice); the last line it prints, `FLOW_ROOT=<dir>`, is the path every later step uses. An existing `CLAUDE.md` is skipped, so append the flow section to it by hand and leave the rest as it is.

## 3. Fill the three files that carry the project

- `CLAUDE.md`: what this is, commands, invariants, source of truth, index.
- `docs/flow/context.md`: reading list, source of truth, rules that break everything, how to test (with *when each check is mandatory*), standards, queue rules, report format, current priorities. Keep permanent rules separate from temporary priorities so the priorities can be rewritten without touching the rules.
- `docs/README.md`: adjust the index if the layout differs.

Keep each as short as the project allows. They are read by every agent every time.

## 4. The first sequence is the safety net

Before features, queue a first sequence of tasks that builds testing: unit tests for what exists plus an end-to-end smoke that runs in one command. Without a way to prove work, every later task rests on assumption and the flow cannot scale. If the project has nothing to test yet, the first task is to decide how it will be tested.

## 5. Hand over

- Run `python <skill-dir>/scripts/lint_docs.py <project-dir>` and fix what it reports.
- Tell the Owner what you created, what decisions you recorded on their behalf, and what only they can do.
- Give them the phrase to open Builder sessions (see `roles.md`).
