# Handoffs and kickoff prompts

Two situations need a written bridge: a session ending mid-work, and a fresh session or sub-agent starting cold.

## 1. Ending a session mid-work: `HANDOFF.md`

Write `docs/flow/HANDOFF.md` (overwrite it; it describes *now*, not history) containing:

- **Where I stopped** - the task ID and the exact step.
- **State of the world** - uncommitted changes, running processes, temporary test config that is still applied and must be reverted, branches.
- **What is left** - an ordered list.
- **Cautions** - things that surprised you, traps, things that look done but are not.
- **Waiting on** - questions or Owner actions.

The next session reads it right after `context.md`, acts on it, then clears it. A stale handoff is worse than none, so when the work is picked up, empty the file.

## 2. Kicking off a fresh session or sub-agent: self-contained prompt

A cold agent has no memory, so the kickoff prompt must carry everything the files do not. Pattern that works:

```
# Task: <name>

You are a <role> continuing a project in progress, in a new session with no memory
of earlier conversations. Everything you need is in the repository and this file.
Answer in <Owner's language>. Code, file names and commit messages in <language>.

## Read, in this order, and only this
1. <path> - why
2. <path> - why
Do not re-read the whole repository; search and read only what you change.

## Owner decisions (override the docs on conflict)
- ...

## How to work
- Stages <S1, S2, ...>. At the end of each: run checks, update docs, commit, summarize
  in <language>, then STOP. Continue only when the Owner says "continue".
- Before coding each stage, write ~10 lines on what you will do and the trade-offs.
  Ask only if something is truly ambiguous and high-impact (security, data, public contract).

## Project conventions
...

## Environment notes (lessons already learned)
...

## Stages
### S1 ...
### S2 ...

## Definition of done per stage
- ...
- Summary: what was done, how to verify, what the Owner must do, risks and debts.
```

Why each part: the ordered, limited reading list saves context; "Owner decisions override" stops the agent from following a stale doc; stage stops with "continue" keep the Owner in control of a long run; the environment notes carry hard-won lessons so they are not relearned.

Use this form when the task is bigger than one queue prompt or the agent will run without the queue. For ordinary queue tasks, the task prompt plus `context.md` is already the kickoff.
