# Loop 5 — Cheatsheet

*Fill in as you build.*

## Commands

- `python langchain_agent.py` — run the agent
- `python mcp_server.py` — run the MCP server standalone (for verifying it works alone)
- `python -c "import langchain; print(langchain.__version__)"` — check pinned version

## Patterns

3–5 reusable code snippets. Suggestions:

- The minimal LangChain agent shape: `llm + tools + prompt → create_tool_calling_agent → AgentExecutor`.
- `ChatPromptTemplate.from_messages([...])` with the three placeholder slots (`system`, `human/{input}`, `MessagesPlaceholder`s).
- The chat_history pattern: maintain a list outside, pass on each `invoke`, append after each turn.
- The MCP consumption pattern: `stdio_client → ClientSession → load_mcp_tools`. Note the async context.
- The `@tool` decorator with type hints — what types LangChain auto-derives schemas for.

## Gotchas

3–5 traps. Suggestions:

- LangChain version churns — pin and don't upgrade.
- `@tool` chokes on complex generics in type hints. Stick to simple types.
- `AgentExecutor` with `verbose=True` is essential — without it, tool errors disappear.
- `MessagesPlaceholder` order in the prompt matters — `agent_scratchpad` must come *after* `human`.
- MCP async session must wrap every call. If you just `asyncio.run` once, the session is closed by the time you try to invoke a tool.
- `from langchain.memory import ConversationBufferMemory` is deprecated in 0.3+. Use `MessagesPlaceholder("chat_history")` + manual list.

## Numbers

What you observed. Suggestions:

- Lines of code: Loop 4 agent.py = _N_ ; Loop 5 langchain_agent.py with same features = _M_.
- Latency overhead: LangChain `verbose=True` logging adds ~_X_ ms per turn.
- MCP subprocess startup: ~_Y_ ms once (then cheap per call).
- Token overhead from LangChain's prompt scaffolding: ~_Z_ extra tokens per turn vs Loop 4.
