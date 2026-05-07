# Loop 2 — Cheatsheet

*Fill in as you build. Skim-this-in-60-seconds-six-months-from-now is the bar.*

## Commands

Shell + Python one-liners you used a lot.

## Patterns

3–5 reusable code snippets. Suggestions to replace with your own:

- The minimal native function-call shape (declare a tool, read `function_calls`, send back a tool result).
- The Pydantic `BaseModel` → JSON Schema → `FunctionDeclaration` chain.
- The descriptive-error string template (what to include: tool name, what failed, why, what to try next).
- The hot-swap registry: dict + add/remove + re-pass to `GenerateContentConfig`.

## Gotchas

3–5 traps you fell into. Suggestions to replace:

- Regex parsing of model output is unreliable in ways that aren't obvious at small N — measure across 20 turns, not 5.
- Gemini's `function_calls` field is empty (not None) when the model emits text. Check both.
- Pydantic `ValidationError.errors()` is more useful as a tool result than `str(error)` — it's structured.
- "Unknown tool" should *return a result the model can read*, not crash. The model will try to recover if you let it.

## Numbers

Token counts, latencies, costs, *failure rates* you observed. Suggestions:

- Text-parse Stage 1: success _X_ / silent _Y_ / crash _Z_ / wrong _W_ across 20 turns.
- Native function-call Stage 2: success _X_ / silent _Y_ / crash _Z_ / wrong _W_ across same 20 turns.
- Recovery rate, opaque error: _N_/5 turns.
- Recovery rate, descriptive error: _M_/5 turns.
- Latency delta text-parse vs native (ms): negligible / meaningful / large?
