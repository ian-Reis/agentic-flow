# Task prompts

A prompt is one task that fits a single Builder session and proves itself. It must be enough on its own: the Builder has no memory of the conversation that produced it. The template to copy is `docs/tasks/_TEMPLATE.md` (source: `assets/templates/docs/tasks/_TEMPLATE.md`).

## Sections and why each exists

| Section | Purpose |
|---|---|
| Header: needs, areas, required checks | Lets Builders schedule safely and know which tests are mandatory |
| Owner decision (dated) | The decided part, in the Owner's words when that helps. "Do not reopen." Stops each Builder from re-litigating |
| Goal | The visible result in 2-5 lines, and why |
| How it is today (read) | Where the code is and what already exists to **reuse**. Prevents duplicate systems |
| Requirements | Numbered, concrete, verifiable. Initial values plus "measure and adjust" where uncertain. Mark Builder choices as "decide and document" |
| Rules that must not break | The project invariants this task touches, and what not to do (do not change timings, do not delete, move to backup) |
| Out of scope | The tempting things to leave alone |
| Validation | Measurements with numbers, before/after evidence, bad paths, restored test state |
| Delivery | Report per `report.md`, docs to update, what the Owner must do |

## Quality checklist (Director, before queuing)

- [ ] One task. If it has more than ~8 large requirements, split it into a sequence.
- [ ] Says where the code is and what to reuse.
- [ ] Separates "Owner decision" from "decide and document".
- [ ] Criteria are **measurable**. "Same frame +/-1", "no overlaps", "p95 under 200 ms" - not "looks good" or "make it nice".
- [ ] Covers the bad paths: cancel midway, error, exit, unexpected end.
- [ ] States what not to do and what must stay unchanged.
- [ ] `Needs` and `Areas` are filled in the queue row.
- [ ] Other prompts and docs affected by this one were adjusted.

Vague prompts ("polish it") produce arbitrary output. When the target is a feeling or a look, name a reference and a boundary: "level of X, without turning into Y", then attach a number or an example the Builder can check.

## Sequences for big problems

A large problem becomes 3-8 tasks in this order:

1. **Diagnose** - build the tool that measures, measure everything, produce a catalog of problems. Fix nothing yet. This keeps fixes honest, because they are aimed at measured causes.
2. **Fix** - one or more tasks that clear the catalog item by item.
3. **Regress** - an automatic check that runs in one command and fails if the problem returns, plus a rule added to `context.md`: "any task touching X runs check X". Each sequence leaves a permanent safety net, so later tasks do not reopen old bugs.

## Writing guidance

- Give context, not only orders. A Builder who knows why makes better calls in the gaps.
- Values you are unsure of are starting points with "measure and adjust", not facts.
- If an improvement must not change behavior, say so explicitly ("does not change durations or rules").
- If the task needs something only the Owner can provide, say so in Delivery and in the queue as `blocked` until it exists.
