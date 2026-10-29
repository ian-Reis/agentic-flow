# Definition of Done

A task may move to `verify` only when all of this is true. The Director re-checks a sample before `done`.

- Automated checks pass: the project's unit tests plus the smoke/regression checks for every area touched (the list lives in `docs/flow/context.md`, under "How to test").
- The measurements the prompt asked for are in the report, with numbers.
- Everything visible or behavioral has before/after evidence.
- Bad paths were exercised (cancel midway, error, exit, unexpected end).
- Temporary test state is restored: test configs reverted, flags back to their defaults, scratch files removed.
- Docs updated: `CLAUDE.md` if an invariant or command changed, the system doc for the touched area, any catalog the sequence keeps.
- The report is written in the standard format, including what was *not* verified.
- The queue row says `verify`, and the prompt is not edited afterwards.

`done` is set by someone other than the Builder who did the work (or, in solo mode, by a separate cold read-back pass that says so).

Why so strict: each item is something that has silently failed in real projects - a test config left on, a doc left stale, a "works" without a number. Cheap to check at the end, expensive to find three tasks later.
