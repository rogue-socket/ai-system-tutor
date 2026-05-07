# Loop 1 — Cheatsheet

*Fill in as you build, not after. Skim-this-in-60-seconds-six-months-from-now is the bar.*

## Commands

Shell + Python one-liners you used a lot. Examples to replace with your own:

- `python agent.py` — run the loop
- `python -c "import os; print(os.environ.get('GEMINI_API_KEY', '')[:8])"` — check key is loaded

## Patterns

3–5 reusable code snippets. Examples to replace:

- The minimal Gemini call (model + contents).
- The pattern for accumulating a chat history list of `{role, content}` dicts.
- The streaming iteration pattern.

## Gotchas

3–5 traps you fell into or almost fell into. Examples to replace:

- `find_dotenv` returns `""` if no `.env` is found, not `None` — surprising.
- Streaming chunks may have empty `.text` — guard with a check.
- Token counts in `usage_metadata` only land at end of response in streaming; track via `response.usage_metadata.total_token_count` after the stream completes.

## Numbers

Token counts, latencies, costs you actually observed in this loop. Examples to replace:

- A 5-turn conversation: ~_X_ input tokens, ~_Y_ output tokens.
- Time-to-first-token: ~_Z_ ms; total response time: ~_W_ ms (so streaming UX matters).
- Free-tier limit you hit (or didn't): ~_N_ requests before you stopped for the day.
