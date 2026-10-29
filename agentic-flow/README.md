# agentic-flow

A file-based multi-agent workflow for any new project. An **Owner** decides, a **Director** plans and writes task prompts, and **Builders** execute them from a queue and prove their work with reports. Everything is plain files (queue, decisions, reports, handoff), so no agent depends on memory.

## Commands and skills

| Name | What it does |
|---|---|
| `/agentic-flow:init [project name]` | Scaffolds `CLAUDE.md` and `docs/` in the current project, fills them from the repository and a short Owner interview, and seeds the first task (the test baseline). Safe to re-run; never overwrites files. If the project already has a `docs/` folder, the flow is installed in `docs/agentic/` and the existing docs are not touched (an existing `CLAUDE.md` only gets an appended section). |
| `agentic-flow` (skill) | The method itself. Claude loads it on its own when you plan tasks, write prompts for sub-agents, hand off sessions or record decisions. |

## Install

Test for one session, without installing:

```
claude --plugin-dir <path-to>/agentic-flow
```

Install permanently from the local marketplace (the folder that contains `.claude-plugin/marketplace.json`):

```
claude plugin marketplace add <path-to>/skill-flow-agentic
claude plugin install agentic-flow@agentic-flow-local
```

Then, inside a new project, run `/agentic-flow:init`.

## Requirements

Python 3 (standard library only) for the bundled scaffold and lint scripts. They are optional: `/agentic-flow:init` falls back to copying the templates by hand when Python is missing.
