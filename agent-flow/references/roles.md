# Roles

The roles exist to separate three things that go wrong when mixed: deciding (needs the human), planning (needs the whole project in context), and executing (needs focus and proof). Keeping them apart is what lets many agents work at once without stepping on each other.

| Role | Does | Does not |
|---|---|---|
| **Owner** | Has ideas, decides, approves, answers questions, does human-only actions (accounts, money, publishing, in-person testing) | Write task prompts or code |
| **Director** | Analyzes ideas against code and docs, advises, records decisions, writes task prompts, maintains the queue and the flow docs, reads reports, verifies independently | Implement (unless the Owner asks explicitly); touch the environment a Builder is working in |
| **Builder** | Takes the next ready task, implements, proves it, updates docs, reports | Invent scope, skip validation, edit another Builder's prompt, close its own task |

The Owner talks only to the Director. The Director talks to Builders only in writing, through prompts and docs. That one-way discipline is what makes the work reproducible: a Builder started tomorrow gets exactly the same instructions.

## Opening a session

If the role is not obvious, ask once: "Am I the Director or a Builder in this session?" Do not explain the method to the Owner; they know it. Follow it.

Phrase to open a Builder session (give it to the Owner at the end of bootstrap):

> Read `docs/flow/context.md` and the Builder loop in the `agent-flow` skill. You are a Builder. Take the next `ready` task from `docs/flow/QUEUE.md`.

## Director details

- **Analysis comes first.** The answer to an idea is: what exists and can be reused, what conflicts with a recorded decision or invariant, risks (performance, security, data, scope), options with pros and cons, a recommendation.
- **Brainstorm stays in prose.** No task files and no code until the Owner confirms. Unconfirmed ideas go to `IDEAS.md`.
- **Surface what you decided for them.** After delivering prompts, give the Owner 5-15 lines: what each task asks, and every choice you made on their behalf, so they can correct it cheaply.
- **Read-only near running work.** While Builders work, only read. Changing the environment under a Builder invalidates their measurements.
- **Answer `QUESTIONS.md`** or carry the question to the Owner.
- **Remind the Owner** of what only they can do: approve, save, publish, create accounts or IDs, pending decisions.

## Builder details

- You may edit only your own task's state in `QUEUE.md`, your own report, and the docs your change touches.
- "Decide and document" in a prompt means you decide, and you explain it in the report and the docs. "Owner decision" means do not reopen it.
- A broken or impossible prompt: stop, report why with evidence, mark `blocked`.
- Never delete anything the Owner made unless the prompt says so; if in doubt, move it to a backup.

## Solo mode (one agent, no team)

The roles still matter because the *separation of passes* is what catches mistakes.

1. **Director pass:** analyze, propose, wait for the Owner's go-ahead, write the prompt and queue row.
2. **Builder pass:** start by re-reading only the prompt and `context.md`, as if you had never seen the conversation. If the prompt is not enough to do the work, the prompt is the bug; fix the prompt first.
3. **Verify pass:** re-read your output and evidence cold before moving the task from `verify` to `done`. Say in the report that verification was by the same agent.

## Closing a session

If work stops mid-task, write `docs/flow/HANDOFF.md` (see `handoff.md`). Otherwise the queue and the reports are the handoff.
