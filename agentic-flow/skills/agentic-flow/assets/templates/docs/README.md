# Documentation - {{PROJECT_NAME}}

Index of everything in `{{DOCS}}/`. Agent rules and the code map are in the root `CLAUDE.md`.

## Where to start
| You want to... | Read |
|---|---|
| work as Director or Builder | [flow/context.md](flow/context.md) |
| see what is queued and its status | [flow/QUEUE.md](flow/QUEUE.md) |
| know what was decided and why | [flow/DECISIONS.md](flow/DECISIONS.md) |
| pick up from an interrupted session | [flow/HANDOFF.md](flow/HANDOFF.md) |

## Folders
| Folder | Purpose | Kind |
|---|---|---|
| `flow/` | coordination files: context, queue, decisions, questions, ideas, handoff | living |
| `tasks/` | open task prompts, one per file; `done/` holds finished ones | queue |
| `reports/` | one dated report per finished task | historical |
| `systems/` | one document per system | living |

## Conventions
1. One topic per document.
2. One source of truth; other documents link, never copy.
3. About 15 KB per document at most; split by topic.
4. Living documents are updated when reality changes; reports are never edited after writing. What stopped being true is deleted or marked superseded.
5. Names are lowercase and hyphenated, saying the topic; reports start with `YYYY-MM-DD-<ID>-`.
6. Every new document goes in the folder of its kind and gets a line here.
7. Renaming or moving a document means updating every link to it.
8. No personal data or machine-specific absolute paths.
9. Screenshots, videos and archives live outside `{{DOCS}}/` (e.g. `assets/`) and are linked.
