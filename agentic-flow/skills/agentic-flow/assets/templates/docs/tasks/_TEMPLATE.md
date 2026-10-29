# Task NNN - Short title

You are the engineer responsible for this task of the project {{PROJECT_NAME}}.
**Before anything else, read `{{DOCS}}/flow/context.md` in full**, plus: <sections of CLAUDE.md / system docs>.

- **Needs:** NNN, NNN (if any is not `done`, stop and report)
- **Areas touched:** <areas> -> **mandatory checks:** <unit + smoke for those areas>
- **Model tier:** light | standard | heavy | frontier (optional)

## Owner decision (YYYY-MM-DD)
What was decided, in the Owner's words when that helps. Cite `D###`. Do not reopen.

## Goal
The visible result in 2-5 lines, and why it matters.

## How it is today (read)
Where the code is. What already exists and must be REUSED, not duplicated.

## Requirements
1. Concrete and verifiable. Initial values plus "measure and adjust" where uncertain.
2. What the Builder decides: "decide and document".

## Rules that must not break
Project invariants this task touches. What not to do (do not change timings, do not delete - move to backup, do not touch X).

## Out of scope
The tempting things to leave alone.

## Validation
- Measurements with numbers and how they were obtained.
- Before/after evidence for anything visible or behavioral.
- Bad paths: cancel midway, error, exit, unexpected end.
- Mandatory checks passing; test state restored.

## Delivery
Report in `{{DOCS}}/reports/YYYY-MM-DD-NNN-<slug>.md` (template in that folder), docs updated, list of what the Owner must do.
