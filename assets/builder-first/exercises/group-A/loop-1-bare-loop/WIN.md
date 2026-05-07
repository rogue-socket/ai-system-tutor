# Loop 1 — Win Criteria

You're done when `agent.py`:

- [ ] Runs in a loop. Type a message, get a reply, type another. Type `exit` (or `quit`, or Ctrl-C) to stop.
- [ ] Maintains conversation history across turns. Test: ask "what did I just ask you?" on turn 2 and the model answers correctly.
- [ ] Uses a system prompt that gives the model a role. Any role — "helpful assistant", "snarky pirate", "Linux expert". The role should be visible in the answers.
- [ ] Streams the response. Tokens print incrementally, not all at once at the end of the model's response.
- [ ] Prints the running total token count after each turn. Non-stream: `response.usage_metadata.total_token_count`. Stream: read `usage_metadata` from the *final* chunk after the iterator is exhausted (it's populated on the last chunk, not on every chunk).

When all five boxes are checked, write `NOTES.md` and `CHEATSHEET.md`. Then `/loop next` for Loop 2.

## Stretch (optional, no extra credit)

- Add a `/clear` command that resets history mid-conversation.
- Compare token counts at turn 1 vs turn 10. Watch context grow linearly.
- Force a context-window failure on purpose: paste a long document several times. See what the failure mode looks like — does it silently drop early turns, error out, or something else?
- Switch the system prompt mid-conversation (a `/system <new prompt>` command) and observe behavior shift.

## How the tutor will check

When you say you're done, the tutor will ask you to demonstrate each criterion in your running script — not show the code. Behavior > implementation.
