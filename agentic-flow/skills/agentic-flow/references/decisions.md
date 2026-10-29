# Decisions

`docs/flow/DECISIONS.md` is the log of what the Owner (or the Director, on the Owner's behalf) decided. Without it, every Builder rediscusses the same choice and prompts drift apart.

## Entry format

```
### D014 - Short title            (2026-03-02, active)
Decision: what was decided, in one or two sentences, in the Owner's words when it helps.
Why: the reason or the evidence behind it.
Affects: tasks 012, 015; docs/systems/camera.md
Supersedes: D009            (omit if none)
```

- **ID** `D###`, sequential, never reused.
- **Status** is `active`, `superseded by D###`, or `revoked`. Change the status in place when a decision is replaced and link both ways; do not delete the old entry. History is how a newcomer understands why things are as they are.
- **Who decided** matters. Mark Director-made choices with `(director, pending Owner confirmation)` until the Owner has seen them.

## Using decisions

- Task prompts **cite** a decision (`Owner decision D014`) instead of reopening it.
- When a measurement contradicts a decision, do not quietly override it. Add a new decision that supersedes the old one, with the measurement as the "Why", and state which numbers now prevail. Then adjust the `ready` prompts it affects.
- Decisions that are really architecture (a structural choice with trade-offs and consequences) deserve a few more lines: add `Context` and `Consequences` fields. If a project accumulates many, move those to `docs/decisions/` as one file per decision, keeping `DECISIONS.md` as the index.

## Ideas versus decisions

Anything not decided goes to `docs/flow/IDEAS.md`. An idea becomes a decision when the Owner confirms it, and only then a task. This keeps the queue limited to work that is approved.
