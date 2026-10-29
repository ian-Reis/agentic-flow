# Model routing

Use the cheapest model that can do the task. Move up a tier when the task requires judgment, not just execution. This is optional: skip it when only one model is available or the Owner picks the model.

| Tier | Task shape | Examples | Claude example |
|---|---|---|---|
| Light | Mechanical, read-only | inspect a tree, read files back, summarize logs, list properties | haiku |
| Standard | Implementation that is fully specified | build a module from a given interface, bootstrap scripts, configuration edits, QA runs and captures | sonnet |
| Heavy | The builder must *decide how* something should behave | tuning, algorithms, tricky refactors, anything with feel or performance trade-offs | opus |
| Frontier | Hard decisions or opaque bugs | new architecture, instability with no clear cause, conflicting requirements | the strongest available |

Rules of thumb:

- If the prompt dictates exactly what to write, a Standard tier or lower is enough.
- If the agent must choose the approach, use Heavy or higher.
- Failed twice with a model: go up one tier and include the failure report in the new prompt, so the stronger model starts from what was learned.
- The Director decides "is it done" itself; do not delegate verification to a lighter tier that cannot judge it.

Record the chosen tier in the task header so the Owner can see and change it.
