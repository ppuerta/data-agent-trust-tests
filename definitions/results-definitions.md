# Results: definitions test

Run on 7 November 2026. The guesses below were written before the 45 runs and were not edited afterwards.

## Guesses before running
Written on 7 November 2026, before the 45 runs. Claude's guesses, not results.

- **A (nothing):** most answers will report 124,634.77, because in the earlier tests the agent chose completed orders on its own. I expect the English question and "ventas"/"vendimos" to be the most likely to give 156,987.45 or to give both figures. I expect most answers to state which statuses they counted.
- **B (context file):** all 15 answers report 124,634.77 and mention the definition. If one does not, I would be surprised.
- **C (view):** most answers use `revenue_orders`. A few may go to `orders` anyway. I expect the figure to be right in nearly all.
- **Overall:** I expect the differences between A and the other two to be smaller than the ones people assume, since the model already picks the sensible definition. If so, the more useful finding is that the question phrasing does not matter much, and the risk is elsewhere (what the agent says about the definition).

## Setup
- Date: 7 November 2026
- Model: claude-sonnet-5-5 (pinned in `run.sh`)
- Claude Code version: 2.1.317
- Each run: fresh `claude -p` session, only the read-only `duck` server, no other tools, project settings only. All `.err` files are empty.

## Output of `score.py`
Total figures found anywhere in the answer:

| Condition | Runs | Reports 124,634.77 only | Reports 156,987.45 only | Reports both | Other |
|---|---|---|---|---|---|
| A. Nothing | 15 | 0 | 0 | 15 | 0 |
| B. Definition in `CLAUDE.md` | 15 | 15 | 0 | 0 | 0 |
| C. View with the definition | 15 | 15 | 0 | 0 | 0 |

Headline figure (opening paragraph of the answer):

| Condition | Completed (124,634.77) | All statuses (156,987.45) | Unclear (none or both) |
|---|---|---|---|
| A | 11 | 2 | 2 |
| B | 15 | 0 | 0 |
| C | 15 | 0 | 0 |

## What I read in `raw/`
- **Condition A never answered silently.** All 15 answers listed the three statuses with their amounts, so both figures were visible in every one. What changed was the headline.
- **The word mattered.** With "ingresos" (q1), two of three answers opened with 1,000 orders adding up to 156,987.45 and said "revenue" could mean orders or money; the third opened with the table and no headline. The completed figure came later, as "the most reliable" or "the usual reading". With "facturamos", "vendimos", and the English question, all 9 opened with 124,634.77. With "ventas totales", 2 of 3 did, and the third opened with a heading and the table.
- **Condition A answers were longer and hedged more.** Together they run about 1,530 words, against 610 for B and 680 for C. 14 of 15 A answers say they did not use or verify `order_items`; none of the B or C answers mention it. The missing currency came up in 6 of 15 A answers, 1 of 15 B and 5 of 15 C.
- **Condition B:** all 15 gave the completed figure first and said they counted only completed orders; 5 of 15 also said it came from the project's revenue definition.
- **Condition C:** all 15 mention `revenue_orders` and say it only counts completed orders; some add that `orders` would be needed to include the rest. I did not check whether any answer also queried `orders` directly.

## Compared with my guess
I expected A to do better than people assume, and it did on the figure: the model never reported a single wrong number. I expected "ventas" and the English question to be the risky ones. It was "ingresos" instead. I expected B and C to be nearly perfect; they were perfect (15 of 15 each), but A was also correct in the statuses it listed.

## Honest summary
In 45 fresh sessions, the same revenue question gave the completed-orders figure as the headline in 11 of 15 answers with no definition provided, and in 30 of 30 when the definition was in the context file or in a view. The 4 remaining answers in A still showed both figures with the statuses, so I would not call them silent errors. The differences come from one word, "ingresos", which the agent read as possibly meaning orders. One model, one small schema, three runs per cell, non-interactive runs. The result does not show that A would hold with a messier warehouse, where the "unclear" cases could be more costly. It shows that, on this one, giving the definition made the headline stable and that without it the agent hedged openly instead of guessing quietly.
