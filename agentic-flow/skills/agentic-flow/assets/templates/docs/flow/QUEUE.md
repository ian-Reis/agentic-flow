# Queue

Single index of work. States: `draft` -> `ready` -> `in-progress` -> `verify` -> `done`; side exits `blocked`, `rework`, `superseded`.
Builder sets `in-progress` (before touching anything) and `verify`. Only the Director sets `ready`, `rework`, `done`, `superseded`.
Keep cells short; detail goes in the task file (`{{DOCS}}/tasks/<ID>-<slug>.md`) or the report (`{{DOCS}}/reports/`).

| ID | Title | Needs | Areas | Status | Builder |
|----|-------|-------|-------|--------|---------|
