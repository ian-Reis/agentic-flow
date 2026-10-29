# CLAUDE.md - {{PROJECT_NAME}}

Front door for every agent. Keep it short and current. Detail lives in `docs/systems/`; only rules that always apply stay here.

## What this is
<One paragraph: what the project is, who it is for, and what "done" means for the first milestone.>

## Commands
| Do | Command |
|---|---|
| Build | `<command>` |
| Run | `<command>` |
| Test (unit) | `<command>` |
| Test (smoke / end to end) | `<command>` |

## Source of truth
<Where edits are made. What is generated, mirrored or copied and must NEVER be edited by hand.>

## Invariants (what breaks everything if ignored)
- <rule>

## Working method
This project uses the `agent-flow` method. Read `docs/flow/context.md` before any task; the queue is `docs/flow/QUEUE.md`; decisions are in `docs/flow/DECISIONS.md`.

## Index: the task touches X -> read Y
| Task touches | Read |
|---|---|
| <area> | `docs/systems/<area>.md` |
