# Loop 2 — What's Broken

The starter is an agent with one tool — a calculator. The model is *told* to emit JSON when it wants to compute something. The Python code parses that JSON with a regex and dispatches.

It works sometimes. It breaks a lot. That's the lesson.

## Run it first

```bash
python agent.py
```

Try a mix of queries:
- `what's 12 + 7?`
- `multiply 9 by 11`
- `compute 12 + 7, then multiply by 3`
- `if I have 7 apples and eat half, how many are left?`
- `divide 10 by 0`
- `square root of 144`

You'll see at least three different failure modes within ten turns.

## The failure modes

1. **Brittle JSON parsing.** The regex grabs the first `{...}` it sees. Sometimes the model wraps the JSON in prose (`"Sure! {"tool": ...}"`) — works. Sometimes the model emits an inline example `{...}` first and the regex grabs that — broken. Sometimes the model gives no JSON at all — silently falls through.
2. **Wrong-typed args.** The model occasionally outputs `"a": "twelve"` instead of `"a": 12`. `calculator(a="twelve", ...)` raises `TypeError`. Loop crashes.
3. **Hallucinated tool names.** The model invents `{"tool": "math", ...}` or `{"tool": "compute", ...}`. Your dispatcher returns `"Tool result: error"` and the model has no idea why.
4. **Multi-step queries.** "Compute 12 + 7, then multiply by 3" — model emits two JSON blobs back-to-back; the regex only matches the first.
5. **No error recovery.** When `calculator` raises (bad args, division by zero, unknown op), the loop crashes. The model never sees the error, can't try again.

## Your task — six stages, do them in order

Each stage teaches something the next one assumes. Don't skip.

### Stage 1 — Measure the baseline (15 min)

Run 20 turns of mixed queries. For each turn record one of: `success`, `silent_fail` (no JSON found), `crash` (bad args / unknown op / division-by-zero), `wrong_answer` (parsed but model hallucinated). Total them.

Write the four numbers in `NOTES.md` under "the break." You'll compare against post-fix numbers in stage 2.

### Stage 2 — Switch to Gemini's native function calling

Replace the regex parsing with the SDK's native tool-call feature. Define `calculator` as a tool the SDK knows about. Read the response's `function_calls` field instead of parsing text.

Re-run the same 20 queries. Total each category again. Write the comparison in `NOTES.md` under "the fix." The numbers should be dramatically different.

### Stage 3 — Add a second tool

Add `get_weather(city: str) -> str` to `tools.py` (return a hardcoded string — it's a mock). Wire it into the registry. Verify the model picks `calculator` for math queries and `get_weather` for weather queries.

### Stage 4 — Hot-swap the tool registry

Add a CLI command in `agent.py`:
- `/tools list` — print the current registry.
- `/tools remove <name>` — remove a tool from the registry mid-conversation.
- `/tools add <name>` — add it back.

Try removing `calculator` after a few math turns and asking another math question. The model should fail gracefully (acknowledge it doesn't have the tool) rather than hallucinating a number. If it hallucinates anyway, that's a finding for `NOTES.md`.

### Stage 5 — Pydantic schemas for tool args

Define each tool's args as a Pydantic `BaseModel`. Wire them into the function declarations (Gemini accepts Pydantic models in some places; if not, use `Model.model_json_schema()` to derive a JSON schema and pass that).

Force a wrong-typed arg manually (edit your `dispatch` to bypass validation, or send the model a query crafted to produce one). When Pydantic raises `ValidationError`, return the error message string to the model as the tool result. Watch the model self-correct on the next turn.

### Stage 6 — Tool error contracts

Force two failures: divide by zero, and an unknown op. Try two error styles:
- **Opaque:** `"Tool result: error"`.
- **Descriptive:** `"Tool result: calculator failed: cannot divide by zero. Try a non-zero divisor."`

Run the same broken query 5 times under each style. Count how often the model recovers on the next turn vs spirals (retries the same broken call, gives up, hallucinates an answer). Numbers go in `NOTES.md` under "the fix."

## When you get stuck

- **Function calling docs:** `https://ai.google.dev/gemini-api/docs/function-calling`. Start with the *automatic function calling* section — it's the simplest entry point. You can pass a Python function with type hints and Gemini auto-derives the schema.
- **Tool result shape:** when responding to a tool call, you wrap the result in a `types.Content` with role `"tool"` (or use the SDK's helper). Ask the tutor if the exact shape is unclear.
- **Pydantic + Gemini:** Generate JSON Schema with `Model.model_json_schema()`. Hand that to a `FunctionDeclaration` if the SDK won't accept the Pydantic model directly.
- **Multi-tool selection:** if the model picks the wrong tool, your tool descriptions are too vague. Tighten them — short, action-verb-led, no redundancy with the tool name.

## What you specifically should NOT use

- **`langchain` / `langgraph`** — Loop 5+. We're feeling the raw mechanics.
- **`client.chats.create(...)`** — same as Loop 1; you manage history yourself.
- **Loop 1 streaming and token-count code** — leave them out. Streaming + tool calls together is a Loop 9 problem; conflating them now adds noise.
