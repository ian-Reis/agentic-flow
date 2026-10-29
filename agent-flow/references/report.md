# Reports

Every task ends with a report in `docs/reports/YYYY-MM-DD-<ID>-<slug>.md` (start from `docs/reports/_TEMPLATE.md`). The ID in the name is how `lint_docs.py` and the Director find it. A task without evidence is not delivered.

Reports are **historical**: after they are written they are not edited. A new result is a new report. This keeps the record trustworthy.

## Structure

1. **What changed** - files and systems, as a short list.
2. **Measurements and validation** - numbers, command output, test results, before/after captures. Say how each number was obtained so the Director can re-run it.
3. **Not verified, and why** - what you could not check (no access, no time, outside scope). Silence here reads as "verified", so be explicit.
4. **Decisions taken** - every "decide and document" choice with its reason, plus any new scope you suggest. The Director decides on the scope.
5. **Deviations** - where you departed from the prompt and why.
6. **Open problems** - anything still wrong or risky.
7. **What the Owner must do** - save, publish, approve, create accounts or IDs, decisions pending.

## Evidence rules

- A claim about behavior needs a measurement, not an argument. If you found a cause, show the measurement that proves it before the fix and the one that shows it gone after.
- Prefer evidence the Director can reproduce: a command, a test name, a query, a capture with its steps.
- Record the exact state under test (version, config, data) so the result means something later.
- Report failures as plainly as successes. A failing check with its output is more useful than a vague "mostly works".

## After writing

Set the task to `verify` in `QUEUE.md`. The Director verifies independently and sets `done` or `rework`.
