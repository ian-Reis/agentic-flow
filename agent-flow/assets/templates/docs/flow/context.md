# Common context - read before any task

Every Builder reads this in full at the start of every task: it changes. Permanent rules go in the sections below; temporary priorities go only in "Current priorities" so they can be rewritten without touching the rules.

## Required reading
1. `CLAUDE.md` - architecture, commands, invariants.
2. <system doc relevant to most tasks, if any>

## Source of truth
<Where to edit. What is a mirror or generated output and must never be edited by hand.>

## Rules that break everything if ignored
- <invariant, security rule, data rule>

## How to test
| Check | Command | Mandatory when a task touches |
|---|---|---|
| Unit tests | `<command>` | anything |
| Smoke / end to end | `<command>` | <areas> |

Temporary test configuration must be reverted before a task is finished.

## Standards
<Code style, comments, naming, UI/visual standard, language of code and docs.>

## Queue and coordination
- The queue is `docs/flow/QUEUE.md`. Reserve a task (`in-progress` + your name) before touching anything.
- Do not edit another Builder's prompt, or any prompt that is not yours.
- Doubt that would change the result: write it in `QUESTIONS.md`, mark `blocked`, take the next task.
- You never set `done`; set `verify` and the Director verifies independently.

## Report
Format and evidence rules: see the `agent-flow` skill, `references/report.md`. Template: `docs/reports/_TEMPLATE.md`.

## Current priorities
<What comes before everything else right now, and for how long. Rewrite freely.>
