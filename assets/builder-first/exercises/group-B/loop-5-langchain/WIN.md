# Loop 5 — Win Criteria

You're done when:

- [ ] You can read `langchain_agent.py` line-by-line and name the Loop 4 equivalent of every abstraction (table in `NOTES.md`).
- [ ] The agent has at least two hand-built tools (`calculator` + one mock).
- [ ] Multi-turn memory works — `my name is Yash` → `what's my name?` answers correctly.
- [ ] Long-term memory works — `remember X` survives script restart, accessible via `recall` or system-prompt prepending.
- [ ] At least one tool comes from `mcp_server.py` via `langchain-mcp-adapters`. `mcp_server.py` is running as a subprocess. Adding a tool to the server makes it appear to the agent without you editing `langchain_agent.py`'s tool definitions.
- [ ] `NOTES.md` has the comparison reflection: *"this code is shorter, this code is now opaque, this is what I'd debug next."*

When all six are checked, finish `CHEATSHEET.md`. Then `/loop next` for Loop 6 (LangGraph — same Group B venv).

## Stretch (optional)

- Replace `MessagesPlaceholder("chat_history")` + manual history list with `RunnableWithMessageHistory` and a session ID. Compare boilerplate.
- Add a community MCP server (npx-based, e.g. `@modelcontextprotocol/server-fetch`) and consume it. Now you've consumed a server you genuinely didn't write, in any language.
- Replace the chain composition with LCEL (`prompt | llm | parser`) for a non-agent task (e.g. summarization) to feel the streaming Runnable interface.
- Hook up LangChain's tracing (`LANGCHAIN_TRACING_V2=true` env var + LangSmith account, or local file logger) and compare to Loop 3's `traces.py`.

## How the tutor will check

When you say you're done:
1. Run multi-turn — show memory across turns.
2. Show your Loop-4-to-LangChain mapping table.
3. Trigger the MCP-served tool — random fact appears, you can point at the running `mcp_server.py` process.
4. Add a third tool to `mcp_server.py` while the agent is running. Reload tools. Watch the agent use the new one.
5. Read aloud the "this code is shorter / now opaque / what I'd debug" reflection.

Behavior + comparison fidelity > implementation polish.
