---
name: agentic-flow
description: Set up and run a file-based multi-agent workflow for a NEW project - an Owner who decides, a Director who plans and writes task prompts, and Builders who execute from a queue and prove their work with reports. Covers the task queue, task prompts, decision log, reports with evidence, session handoffs and model routing, all kept as plain files so no agent depends on memory. Use this skill whenever the user starts a new project that agents will build, wants to organize agent work, split work into tasks or prompts for sub-agents or other sessions, create a backlog/queue/orchestration setup, hand work off between sessions, record decisions, or mentions director/builder, orchestrator, sub-agents, "docs for agents", or "a flow for agents" - even if they do not name the method. Also use it to resume work in a project that was bootstrapped with this flow (docs/flow/ exists). Not for one-off coding tasks, and not for reshaping an existing project that already has its own conventions.
---

# Agentic Flow

Agents forget everything between sessions, and parallel agents cannot see each other's heads. This flow fixes both by making **files the only memory and the only channel**: the Owner decides, the Director turns decisions into written, verifiable tasks, Builders execute them and leave evidence. Anything not written down does not exist for the next agent.

It is project-agnostic on purpose. Nothing here assumes a language, engine or tool; project-specific rules live in the project's own `CLAUDE.md` and `docs/flow/context.md`, which this skill helps you create.

## Step 0 - Work out the situation

Paths written `docs/...` in this skill mean the project's **flow root**: `docs/` for a new project, or `docs/agentic/` when the project already had its own `docs/` (the flow then sits beside their documentation and never edits it). `scripts/init_project.py` picks the root and `scripts/lint_docs.py` finds it.

| You see | Do this |
|---|---|
| New project, no flow yet | **Bootstrap**: read `references/bootstrap.md`, then run `scripts/init_project.py` (or the user's `/agentic-flow:init`) |
| `docs/flow/` or `docs/agentic/flow/` exists (made by this flow) | **Resume**: read `CLAUDE.md`, `<flow root>/flow/context.md`, `QUEUE.md`, `DECISIONS.md`, `HANDOFF.md` (in that order), then Step 1 |
| Existing project with its own docs and conventions, no flow | Do not reshape or move their files. Install the flow isolated in `docs/agentic/` (the init command does this) and append, never rewrite, a short section to their `CLAUDE.md`. If the user wants less than that, offer to borrow single pieces (the task prompt template, the report format) |

## Step 1 - Know your role (ask once if unclear)

- **Owner** - the human. Decides, approves, answers questions, does what only a human can (accounts, payments, publishing).
- **Director** - plans. Analyzes ideas against the existing docs and code, records decisions, writes task prompts, keeps the queue coherent, reads reports. Does not implement.
- **Builder** - executes one task at a time from the queue and proves it.

If the user opened this session to talk, plan or create tasks, you are the Director. If they asked you to run tasks from the queue, you are a Builder. If you are alone (no other agents), use **solo mode**: do the Director pass and the Builder pass as separate steps with the Owner's approval between them, and verify your own work in a fresh read-back pass rather than trusting memory. Details: `references/roles.md`.

## Director loop

1. **Listen, then analyze before writing.** Read the code and docs the idea touches. Tell the Owner what already exists, what conflicts with earlier decisions, the risks, options with trade-offs, and your recommendation. In brainstorm, stay in prose; no tasks and no code until the Owner confirms.
2. **Record the decision** in `docs/flow/DECISIONS.md` (see `references/decisions.md`). Undecided things go to `IDEAS.md`, not the queue.
3. **Write the task prompt** from `docs/tasks/_TEMPLATE.md` and add its row to `QUEUE.md` (see `references/task-prompt.md` for the quality checklist and for splitting big problems into diagnose -> fix -> regression sequences).
4. **Keep the queue coherent.** When a decision changes, adjust every `ready` prompt it affects. Never edit an `in-progress` prompt; write a continuation task that supersedes the changed part.
5. **Verify independently.** When a task reaches `verify`, check the evidence yourself (read back, re-run, sample) before marking it `done` or `rework`. A Builder never closes its own task.
6. **Tell the Owner** what you decided on their behalf (so they can correct it) and what only they can do.

## Builder loop

1. Read `docs/flow/context.md` fully (it changes) and the sections of `CLAUDE.md` the prompt points to.
2. Pick the first `ready` task whose `Needs` are `done` and whose `Areas` do not collide with an `in-progress` task. **Reserve it first** (status `in-progress`, your name) before touching anything.
3. Read what the prompt says to reuse. Reuse, do not duplicate.
4. Implement only the prompt's scope. New scope becomes a note in the report; the Director decides.
5. **Measure, do not theorize.** Every cause you claim and every fix you make is backed by a number, log or capture.
6. Meet the Definition of Done (`references/definition-of-done.md`), update the docs the change touches, restore any temporary test state.
7. Write the report (`references/report.md`), set the task to `verify`, move on.
8. Doubt that would change the result: write it in `QUESTIONS.md`, mark the task `blocked`, take the next one. Do not guess.

## Principles

- **Files are memory.** If the next agent needs it, it is written down.
- **Measure, do not theorize.** Confident theories are often wrong; evidence is cheap.
- **Reuse before creating.** Duplicate systems are the most common way parallel agents hurt a project.
- **Small and proven beats big and presumed.** One task fits one session and proves itself.
- **The Owner decides.** The Director makes clear what it decided for them. Decisions are cited, not reopened.
- **Never stop the line for perfection.** Deliver what is proven and report what is missing.
- **Be honest in reports.** What was not verified, and why, is part of the report.

## Reference map

Read a file only when you reach the step it serves.

| File | Read when |
|---|---|
| `references/bootstrap.md` | starting a new project |
| `references/roles.md` | unsure of a role's limits, solo mode, talking to the Owner |
| `references/queue-and-states.md` | touching `QUEUE.md`, reserving tasks, parallel work |
| `references/task-prompt.md` | writing or splitting tasks |
| `references/report.md` | finishing a task |
| `references/definition-of-done.md` | before setting `verify` or `done` |
| `references/decisions.md` | recording or citing a decision |
| `references/handoff.md` | ending a session mid-work, or kicking off a fresh session or sub-agent |
| `references/model-routing.md` | choosing which model runs a task |
| `references/docs-conventions.md` | creating or reorganizing docs |

## Scripts

- `scripts/init_project.py --target <dir> --name "<Project>"` scaffolds `CLAUDE.md` and `docs/` from `assets/templates/`. It never overwrites existing files.
- `scripts/lint_docs.py <project-dir>` checks the queue against the task and report files, relative links, oversized docs and personal absolute paths. Run it before handing off or closing a batch of tasks.

Both need Python 3 (standard library only). They are conveniences, not requirements: if Python is not available, copy `assets/templates/` into the project by hand (replace `{{PROJECT_NAME}}` and `{{DATE}}`, create `docs/tasks/done/` and `docs/systems/`), and apply the lint checks by eye - each queue row has a task file, `verify`/`done` rows have a report, states are from the list in `queue-and-states.md`, links resolve.
