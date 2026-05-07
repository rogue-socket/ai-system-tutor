# Loop 4 — Win Criteria

You're done when the agent:

- [ ] Has `recall` exposed as a tool AND prepends long-term memory into the system prompt. Tell it your name, exit, restart, ask "what's my name?" — it answers without using a tool.
- [ ] Has working-memory tools (`note_set`, `note_get`). The "bump counter" test works within a session and resets across script restarts.
- [ ] Compacts context automatically when over `TOKEN_BUDGET`. You can demonstrate the threshold being crossed and the agent still answering correctly afterward.
- [ ] Supports `/tools list`, `/tools add <name>`, `/tools remove <name>` commands. After `/tools remove calculator`, math queries either fail gracefully or hallucinate — you can describe which (with your observation in `NOTES.md`).
- [ ] Honors hand-edits to `memory.json`. You added an entry with your text editor (no agent involvement) and the agent's behavior changed on the next run.

When all five are checked, finish `NOTES.md` and `CHEATSHEET.md`. Then `/loop next` for Loop 5 (LangChain — switch to Group B's venv first).

## Stretch (optional)

- Add a `forget(key: str)` tool — symmetric with `remember`. Test it.
- Implement a soft eviction policy in working memory: cap it at N entries; oldest gets evicted.
- After compaction, log the summary to a `compaction.log` file. Compare summaries across multiple compactions of the same conversation — are they consistent?
- Use `client.models.count_tokens(...)` for accurate token counts instead of the `len(text) // 4` estimate. Compare — how off was the estimate?

## How the tutor will check

When you say you're done:
1. Run the "tell name → exit → restart → ask name" flow. See it remember.
2. Run the "bump counter" working-memory test. See within-session persistence and across-restart reset.
3. Force compaction by pasting a long block. Show it firing. Show the post-compaction conversation still working.
4. `/tools remove calculator` mid-session. Ask math. Describe what happened.
5. Hand-edit `memory.json`, restart, demonstrate behavior change.

Behavior > implementation.
