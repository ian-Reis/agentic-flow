# agentic-flow

A Claude Code plugin that sets up a file-based multi-agent workflow in a new project.

One agent plans and writes tasks. Other agents execute them from a queue and prove their work with reports. Everything is stored as plain files in the repository, so no agent depends on conversation memory.

## What it does

- Adds the command `/agentic-flow:init`, which creates the workflow structure in the current project.
- Adds the skill `agentic-flow`, which Claude loads on its own when you plan tasks, write prompts for sub-agents, hand work off between sessions, or record decisions.

## The workflow

| Role | Does | Does not |
|---|---|---|
| Owner (you) | Decides, approves, does what only a human can | Write task prompts or code |
| Director | Analyzes ideas, records decisions, writes task prompts, keeps the queue, verifies finished work | Implement |
| Builder | Takes the next ready task, implements it, measures, writes a report | Invent scope, close its own task |

A task moves through the queue in `QUEUE.md`:

```
draft -> ready -> in-progress -> verify -> done
```

Side exits are `blocked`, `rework` and `superseded`. A Builder reserves a task before touching anything, sets `verify` when finished, and never sets `done`. The Director verifies the evidence independently and closes it.

## Install

```
claude plugin marketplace add ian-Reis/agentic-flow
claude plugin install agentic-flow@agentic-flow
```

To try it for one session without installing, clone the repository and run:

```
claude --plugin-dir ./agentic-flow
```

## Use

Open Claude Code in a new project and run:

```
/agentic-flow:init [project name]
```

The command:

1. Reads the repository (build files, tests, README) to infer commands and conventions.
2. Asks you one short round of questions about what it could not infer.
3. Creates `CLAUDE.md` and the flow files.
4. Fills them in from what it learned and records your answers as decisions.
5. Adds task `001`, establishing a test baseline, as a `draft` for you to approve.
6. Runs a lint over the result and reports what it did.

It never overwrites an existing file. If the project already has a `docs/` folder with content, the flow is installed in `docs/agentic/` and your existing docs are not touched. An existing `CLAUDE.md` only gets an appended section.

## What it creates

```
CLAUDE.md                  entry point for every agent: commands, invariants, index
docs/
  README.md                index and documentation conventions
  flow/
    context.md             rules every Builder reads before each task
    QUEUE.md               the task queue with status and ownership
    DECISIONS.md           log of decisions, cited by tasks instead of reopened
    QUESTIONS.md           Builder doubts waiting for an answer
    IDEAS.md               undecided ideas, kept out of the queue
    HANDOFF.md             where a session stopped, for the next one
  tasks/                   one prompt per task; done/ holds finished ones
  reports/                 one dated report per finished task
  systems/                 one document per system, as needed
```

## Included in the skill

The method is documented in `agentic-flow/skills/agentic-flow/references/`:

- roles and solo mode
- queue and states
- task prompt template and quality checklist
- report format and evidence rules
- definition of done
- decision log format
- session handoff and kickoff prompts
- model routing by task complexity
- documentation conventions

Two helper scripts live in `scripts/`: `init_project.py` scaffolds the files and `lint_docs.py` checks the queue against task and report files, broken links, oversized documents and personal paths.

## Requirements

Claude Code. Python 3 (standard library only) is needed for the helper scripts, but they are optional: without Python, `/agentic-flow:init` copies the templates by hand.

## License

MIT. See [LICENSE](LICENSE).
