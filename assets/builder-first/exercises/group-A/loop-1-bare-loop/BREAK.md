# Loop 1 — What's Broken

Run `python agent.py`. It works — you'll see "Paris" or similar. It also has nothing you'd actually want from an "agent."

## What's missing

1. **It's a one-shot.** No loop. The script answers one question and exits. An agent should keep going until you tell it to stop.
2. **No conversation history.** Even if you wrap it in a loop, the second turn won't remember the first turn. The model has no memory between API calls — *you* have to feed history back in.
3. **No system prompt.** The model has no role or framing. It'll answer anything however it wants.
4. **Blocking output.** The whole response arrives at once after a wait. For a chat experience you want to see tokens stream as they're generated.

## Your task

Edit `agent.py` until it satisfies `WIN.md`. No frameworks — pure Python, just `google.genai` and a `while` loop. Stay under 60 lines.

When the code works, write `NOTES.md` and `CHEATSHEET.md` (templates are in this folder, fill the sections honestly).

## When you get stuck

- **`KeyError: 'GEMINI_API_KEY'`** — `.env` isn't being found. Check that `~/ai-systems/.env` exists and has your real key.
- **`google.genai.errors.ClientError: 403`** — invalid key. Re-copy from AI Studio.
- **`google.genai.errors.ClientError: 429`** — rate limit on the free tier. Wait 60 seconds.
- **Model returns generic answers ignoring your earlier turns** — you're not feeding history back. The `contents` argument needs the full conversation, not just the latest user message.
- **Streaming chunks don't print incrementally** — make sure you're using `client.models.generate_content_stream(...)` and iterating, not the non-stream version. Don't forget `flush=True` on the print, or use `sys.stdout.write` + `sys.stdout.flush`.

## What you don't need yet

- Tools — that's Loop 2.
- A separate memory module — Loop 4.
- Frameworks (LangChain, anything) — Loop 5.
- Pydantic schemas — Loop 2.

Just plain Python, a list, and a while loop.

## What you specifically should NOT use

- **`client.chats.create(...)`** — the Gemini SDK has a chat helper that auto-manages history for you. **Don't use it for this loop.** The whole point is to feel that the model is stateless and *you* maintain the conversation list. Use `client.models.generate_content(...)` (or `generate_content_stream`) and pass a `contents` list of `{role: 'user'|'model', parts: [...]}` entries that you build up by hand. You'll meet `client.chats` (and equivalents in LangChain) later — by then you'll know what they're hiding.
