# Third test: does the same question get the same revenue figure?

The first two tests were about what an agent may read. This one is about what it reports. "Revenue" has no single definition in the data: summing `orders.amount` over all statuses gives 156,987.45; counting only completed orders gives 124,634.77. The test asks the same question five ways and checks which figure comes back, and whether the agent says which definition it used.

| Condition | What the agent gets |
|---|---|
| **A. Nothing** | The database, read-only. No instructions. |
| **B. Definition in the context file** | Same database plus a `CLAUDE.md` with one sentence defining revenue as completed orders. |
| **C. Definition in the database** | A view `revenue_orders` (completed orders only) with a comment on it. The raw `orders` table is still there. |

Five phrasings (`questions.txt`): ingresos, facturamos, ventas totales, vendimos, and one in English. Each runs 3 times per condition, each in a fresh non-interactive session: 5 x 3 x 3 = 45 runs, about 12 minutes.

## Run it

Requirements: `uv`, Claude Code. From this folder:

```bash
uv run --python 3.12 --with duckdb==1.5.6 python build.py   # also creates demo_view.duckdb
./definitions/run.sh 3
python3 definitions/score.py
```

`run.sh` uses `claude -p` with only the `duck` MCP server (`--strict-mcp-config`), no other tools, project settings only, and the model pinned to `claude-sonnet-5-5`. Set `MODEL` or `CLAUDE_BIN` to change them. If it stops, run it again: finished runs are skipped.

`score.py` only looks for the two figures and a few keywords. Read the files in `raw/` too, in particular what each answer says about the definition.

## Limits

One model, one small invented schema, three runs per cell. Non-interactive runs are not the same as a person working in a session. The question is always about the same month. The condition C view is named in a way that makes it easy to find; a real warehouse has dozens of tables.
