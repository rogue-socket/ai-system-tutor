# Loop 4 — What's Broken

This is *the* loop where memory, context, and tools become first-class objects you touch with your hands. By the end, you'll have edited memory.json with your text editor and watched the agent's behavior change next turn — and that mental-model unlock is what most people building agents are missing.

Three modules ship in the starter:
- `memory.py` — short-term (chat history in `agent.py`), working (a dict scratchpad), long-term (a JSON file).
- `context.py` — token estimation + a `compact()` function that's defined but never called.
- `tools.py` — a `REGISTRY` dict of tools, with `remember` already in but `recall` deliberately absent.

The starter agent is *underwired*. It can write to long-term memory but can't read it back. It has no working memory tools. It never compacts context. The tool registry is hardcoded — you can't change tools mid-session. None of this state survives the script exiting.

You'll wire everything across 5 stages.

## Run it first

```bash
python agent.py
```

Try this script:
1. `remember that my name is Yash` — agent calls `remember`, writes to memory.json.
2. Look at `memory.json` (open it in your editor) — verify the entry is there.
3. `what's my name?` — agent has no `recall` tool, no boot-load. It does not know.
4. `exit`. Restart with `python agent.py`. Ask `what's my name?` — still doesn't know.

That's the broken state. Five stages to fix.

## Your task — five stages

### Stage 1 — Wire long-term memory properly

**1a.** Add a `recall(key: str) -> str` tool to `REGISTRY` in `tools.py`. It's already implemented in `memory.py` — you just need to expose it.

**1b.** Modify `system_prompt()` in `agent.py` to prepend a "what we know" block from `memory.load_long_term()` so the model sees stored facts on every turn. Format suggestion:

```
What we already know about the user:
- name: Yash
- favorite_color: blue
```

Test: tell agent "remember my name is Yash", exit, restart, ask "what's my name?". It should answer without using a tool, just reading the system prompt.

**Why both 1a and 1b?** The system prompt approach is for *frequently-needed* facts (cheap, always-on). The `recall` tool is for *occasionally-needed* facts (expensive to put in every prompt, fine to fetch on demand). Both patterns are real; you'll meet them in production agents.

### Stage 2 — Working memory

Add two tools that read/write the in-process `memory.working` dict:

- `note_set(key: str, value: str) -> str`
- `note_get(key: str) -> str`

Add them to `REGISTRY`. Test: ask the agent to track a counter (`every time I say bump, add 1 to a counter and report it`). Verify the counter survives turns *within* a session but does NOT persist across script restart (working ≠ long-term).

Note in `NOTES.md` when you'd reach for working memory vs long-term memory in a real agent.

### Stage 3 — Context compaction

Wire `context.compact()` into `agent.py`'s turn loop. After each turn:

```python
if context.estimate_tokens(history) > context.TOKEN_BUDGET:
    history = context.compact(client, history)
```

Test: have a long conversation (paste a long text once or twice). Print tokens after each turn. Verify compaction fires when the budget is exceeded, and that the agent still answers correctly afterward (i.e. the summary is good enough).

If the agent loses important info post-compaction, that's a finding for `NOTES.md` — improve the summary prompt.

### Stage 4 — Hot-swap the tool registry

Add CLI commands in `agent.py`:

- `/tools list` — print the current registry.
- `/tools remove <name>` — remove a tool from the registry.
- `/tools add <name>` — add it back (you'll need a side dict of all known tools).

Test:
1. Ask a math question — calculator fires.
2. `/tools remove calculator` — registry now has no calculator.
3. Ask another math question — does the agent fail gracefully ("I don't have that tool") or hallucinate the answer? Whichever happens, write it down in `NOTES.md`.

### Stage 5 — Edit memory.json with your text editor

Stop the agent. Open `memory.json` in your text editor. Add an entry by hand:

```json
{
  "user_name": "Yash",
  "user_preference": "concise responses, no emoji"
}
```

Save. Run `python agent.py`. Ask anything.

The agent should respect the preference (concise, no emoji) without you ever telling it directly. This is the big unlock: **agent state is just files. You can edit it. The agent will follow.**

## When you get stuck

- **`automatic_function_calling=AutomaticFunctionCallingConfig(disable=True)`** — disables the SDK's auto-execution. Without this, function calls fire automatically and you can't route through your registry. Required.
- **Function declarations from Python functions** — Gemini auto-derives schemas from type hints + docstrings. Type hints must be present; missing types break schema derivation.
- **Token estimation is rough.** `len(text) // 4` is a crude approximation. For accuracy, use `client.models.count_tokens(...)` — but it's an extra API call per turn. The rough version is fine for Loop 4's purposes.
- **Compaction can lose facts.** If your compacted summary drops a key reference, the next turn fails. The fix is iterating on the summary prompt; don't expect it to be perfect on first try.

## What you specifically should NOT use

- **Vector memory / embeddings** — Loop 8. The long-term memory here is a flat key-value JSON. That's intentional — vectors solve a different problem (similarity search), and conflating them with the simpler key-value pattern muddles the lesson.
- **`langchain.memory.*`** — Loop 5+. We're feeling the raw mechanics.
- **`client.chats`** — manage history yourself.
