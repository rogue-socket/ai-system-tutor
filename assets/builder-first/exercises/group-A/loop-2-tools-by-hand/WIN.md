# Loop 2 — Win Criteria

You're done when `agent.py`:

- [ ] Has measured failure-rate numbers for text-parse vs native-function-call (Stage 1 vs Stage 2). Numbers live in `NOTES.md`.
- [ ] Uses Gemini's native function-calling API. No regex JSON parsing in the dispatch path.
- [ ] Has at least two tools — `calculator` and one mock (`get_weather` or similar). The model picks the right one per query.
- [ ] Supports hot-swapping the tool registry mid-conversation via a `/tools` command. Behavior visibly changes when tools are added or removed.
- [ ] Defines tool args as Pydantic `BaseModel`s (or equivalent typed schemas). Validation errors get returned to the model as tool results, and the model self-corrects on the next turn.
- [ ] Demonstrates the descriptive-vs-opaque error-contract experiment with measured recovery numbers in `NOTES.md`.

When all six are checked, finish `NOTES.md` and `CHEATSHEET.md`. Then `/loop next` for Loop 3.

## Stretch (optional)

- Add `write_file(path: str, content: str)` and let it actually write. Ask the agent to do it twice with the same args. What happens? Write a paragraph in `NOTES.md` about what *idempotency* would mean for this tool — Loop 9 will revisit.
- Add `get_weather` followed by `format_weather` (takes a weather string, returns a formatted version). Watch the model chain them.
- Replace the system prompt's tool description with the auto-derived function declaration (i.e. just the schema, no prose). Does the model still pick the right tool?

## How the tutor will check

When you say you're done:
1. Run a math query and a weather query in your script — see the right tool fire each time.
2. Run `/tools remove calculator`, then ask a math question — see graceful failure (not hallucination).
3. Show the four-bucket failure-rate numbers and the error-contract recovery numbers in `NOTES.md`.
4. Manually call your dispatcher with a wrong-typed arg — see Pydantic's `ValidationError` come back as a tool result string.

Behavior > implementation.
