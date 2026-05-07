# Loop 4 — Cheatsheet

*Fill in as you build.*

## Commands

- `python agent.py` — run
- `cat memory.json | python -m json.tool` — pretty-print long-term memory
- `/tools list`, `/tools remove <name>`, `/tools add <name>` — registry mutation

## Patterns

3–5 reusable code snippets. Suggestions:

- The `system_prompt()` builder that prepends long-term memory facts.
- The pattern for `note_set`/`note_get` operating on a module-level dict.
- The compaction trigger: `if estimate_tokens(history) > BUDGET: history = compact(...)`.
- The `automatic_function_calling=AutomaticFunctionCallingConfig(disable=True)` config — required for manual routing through your own registry.
- The `/tools` command-handler shape (parse the command, mutate REGISTRY, optionally rebuild any cached tool config).

## Gotchas

3–5 traps. Suggestions:

- The starter has `remember` but not `recall` — easy to miss. Function calling wrappers don't tell you when a tool you'd expect doesn't exist; the model just doesn't reach for it.
- Token estimation is rough (~4 chars/token). Real number can be ±25%. Use `count_tokens` for anything precision-critical.
- After compaction, the model's reference to "as discussed earlier" may break if your summary dropped that thread. Iterate the summary prompt.
- Hot-swapping the registry mid-turn (in the middle of a function-call response) confuses the model. Mutate between turns, not during.
- Working memory dies when the script exits. If a learner expected it to persist, that's a working-vs-long-term confusion — name it.

## Numbers

What you observed. Suggestions:

- Token count at turn 5 of a normal chat: ~_N_
- Turn at which compaction first fires: ~_N_
- Tokens saved by compaction: ~_X_ → ~_Y_
- After `/tools remove calculator`, the model: hallucinated _X_/5 times / failed gracefully _Y_/5 times.
- Time for a single turn including tool calls (rough): ~_N_ ms
