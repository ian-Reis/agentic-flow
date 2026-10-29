# Queue and states

`docs/flow/QUEUE.md` is the single index of work. Without it, order and prerequisites get lost across prompt files, and two Builders pick the same task.

## Row format

```
| ID  | Title                   | Needs | Areas             | Status      | Builder |
|-----|-------------------------|-------|-------------------|-------------|---------|
| 012 | Countdown before start  | 008   | arena, ui, camera | ready       | -       |
```

- **ID**: three digits, assigned in creation order, never reused. The task file is `docs/tasks/<ID>-<slug>.md`.
- **Needs**: IDs that must be `done` first, comma-separated, or `-`.
- **Areas**: the systems or directories the task touches. Builders use this to avoid collisions.
- **Builder**: who holds it while `in-progress`; `-` otherwise.
- Keep cells short. Detail belongs in the task file or report; long text inside table cells makes the queue unreadable.

## States

| State | Meaning | Who sets it |
|---|---|---|
| `draft` | Written but not approved by the Owner | Director |
| `ready` | Approved and executable now | Director |
| `in-progress` | Reserved by a Builder | Builder (before touching anything) |
| `verify` | Builder finished; report written; awaiting independent check | Builder |
| `blocked` | Waiting on a question, a missing prerequisite or an Owner action | Builder or Director |
| `rework` | Verification failed; reason is in the report or a note | Director |
| `done` | Independently verified | Director (never the Builder who built it) |
| `superseded` | Replaced by a later task; name it in the title or the task file | Director |

Typical path: `draft -> ready -> in-progress -> verify -> done`, with `blocked` and `rework` as side exits.

## Reserving a task

Set `in-progress` and your name in `Builder` **before** reading deeper or editing anything. In a shared file tree this is the lock: two Builders never take the same task. If you cannot update the file, you cannot safely start.

## Parallel work

- **One area at a time.** Two Builders must not work on the same system or in the same environment (same running editor, same database, same working tree) at once. Use `Areas` to pick tasks that do not cross, or give each Builder its own copy (branch, worktree, clone).
- **Prompts are frozen once reserved.** The Director never edits an `in-progress` prompt. If the idea changed, write a **continuation task** ("task 082 changes the decision from 076") and mark the old part superseded. The next Builder applies it.
- A `ready` prompt may be edited freely by the Director.
- The Director does not change the environment a Builder is using; reading is fine.

## Blocking

A doubt that would change the result is not a license to guess. The Builder:
1. writes the question in `docs/flow/QUESTIONS.md` with the task ID and the options it sees;
2. sets the task to `blocked`;
3. takes the next eligible task.

The Director answers (or asks the Owner), then returns the task to `ready`.

## Moving finished tasks

When a task becomes `done`, move its prompt to `docs/tasks/done/`. The active folder then shows only open work, and nothing is lost. The report in `docs/reports/` is the permanent record.
