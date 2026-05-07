# Loop 5 — What's Broken

You're now in **Group B**. Switch venvs first:

```bash
cd ~/ai-systems/exercises/group-B
uv sync
source .venv/bin/activate
```

Verify with `python -c "import langchain; print(langchain.__version__)"` — should print `0.3.29`.

The starter is a minimal LangChain agent with one tool (`calculator`) and no memory. It runs. The compare-to-Loop-4 reflection is the load-bearing exercise — you'll find that this code is shorter than Loop 4's, and you'll find that some things you understood deeply in Loop 4 are now hidden behind framework abstractions. That trade-off is the lesson.

> **Don't `pip install -U` mid-loop.** LangChain's API churns. The version pinned in `uv.lock` is what BREAK and WIN are calibrated to. If you upgrade, the loop's instructions may stop matching the SDK.

## Run it first

```bash
python langchain_agent.py
```

Try:
- `what's 12 + 7?` — calculator fires, you get an answer.
- `multiply 9 by 11` — same.
- `what did I just ask you?` — **the agent has no memory**. It either guesses, says it doesn't know, or hallucinates the previous turn.

That's the broken state. Five stages.

## Your task — five stages

### Stage 1 — Map every line back to Loop 4 (no code, 20 min)

Open `langchain_agent.py` side-by-side with Loop 4's `agent.py`. For each LangChain abstraction, write the Loop-4 equivalent:

| LangChain | Loop 4 plain Python |
|---|---|
| `ChatGoogleGenerativeAI` | `genai.Client` + model string |
| `@tool` decorator | function in `tools.py` + entry in `REGISTRY` |
| `ChatPromptTemplate.from_messages([...])` | (your `system_prompt()` builder) |
| `MessagesPlaceholder("agent_scratchpad")` | (?) |
| `create_tool_calling_agent` | (?) |
| `AgentExecutor` | (your `turn()` while-loop) |

Fill in the `(?)` rows. Some will be one-to-one; others won't have a clean Loop 4 equivalent (that's a finding). Write the table in `NOTES.md` under "the concept."

This step is **non-negotiable**. Skipping it produces cargo-cult LangChain users who can write code that runs without understanding what's running. Most LangChain bugs in the wild are this.

### Stage 2 — Add a second tool

Add a `get_weather(city: str) -> str` tool (mock — return hardcoded strings as in Loop 4). Verify the agent picks the right tool per query. Stage 1's mapping should make this trivial.

### Stage 3 — Add chat history (memory)

Wire conversation memory so multi-turn works. Modern LangChain pattern (0.3+):

1. Add `MessagesPlaceholder("chat_history")` to your `ChatPromptTemplate`.
2. Maintain a list of messages externally (in `main()`'s loop) — append the human input and the agent output each turn.
3. Pass `chat_history` into `executor.invoke(...)`.

Test: `my name is Yash` → `what's my name?` should now answer correctly across turns.

Note in `NOTES.md`: how does this compare to Loop 4's `history` list-of-`Content`? What's LangChain doing for you? What's it hiding?

### Stage 4 — Add long-term memory

Re-implement Loop 4's `remember(key, value)` and `recall(key)` as LangChain tools, backed by a `memory.json` file in this loop's directory. Wire them into `tools`. Verify the agent uses `remember` when asked to remember something and `recall` (or system-prompt prepending) when asked what it knows.

Reflect on `NOTES.md`: did this take more or less code than Loop 4? Where's the equivalence?

### Stage 5 — MCP integration

Now the load-bearing lesson of Loop 5. Tools don't have to live in your codebase — they can live behind a protocol.

`mcp_server.py` ships a tiny MCP server with two tools (`get_random_fact`, `echo`). Your job: **consume it from your LangChain agent.**

Use `langchain-mcp-adapters` (already in Group B):

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

# Spawn the server as a subprocess and load its tools.
server_params = StdioServerParameters(command="python", args=["mcp_server.py"])
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        mcp_tools = await load_mcp_tools(session)
        # mcp_tools is a list of LangChain tools — add to your agent's `tools`.
```

The async context is awkward to fit into your sync chat loop. Two options:
- **Quick:** use `asyncio.run(...)` once at startup to load the tools into a list, keep the session open in a background task. Works but messy.
- **Cleaner:** convert `main()` to async (`async def main()`) and use `executor.ainvoke(...)`. LangChain supports it.

Test: ask the agent for a random fact. The MCP server's `get_random_fact` tool should fire. Verify by checking the `mcp_server.py` is running as a subprocess. Add a third tool to `mcp_server.py` (e.g. `get_time() -> str`) — the agent picks it up automatically with no change to `langchain_agent.py` (other than re-loading the tool list).

That's the lesson: **tool authoring and tool consumption are decoupled by the protocol.** Anthropic, GitHub, Cursor, Claude Desktop all consume MCP servers as their tool layer. This is table-stakes for AI Engineer roles in 2026.

## When you get stuck

- **`@tool` decorator hates type annotations the SDK doesn't understand.** Stick to `str`, `int`, `float`, `bool`, `list`, `dict`. Avoid generics like `dict[str, list[int]]` — they may not survive the schema derivation.
- **`AgentExecutor` exits silently on tool errors in some configs.** `verbose=True` (already on) helps. If a tool raises, `verbose` will show the trace.
- **MCP async context manager scoping.** The `async with` blocks need to wrap *every* call you make to the session, not just initialization. Hold the context open if you want a long-lived session.
- **LangChain prompt placeholders are positional inside the template.** `MessagesPlaceholder("agent_scratchpad")` must come *after* `("human", ...)`. Order matters.

## What you specifically should NOT use

- **`langgraph`** — Loop 6.
- **`from langchain.memory import ConversationBufferMemory`** — deprecated in 0.3+. Use `MessagesPlaceholder("chat_history")` + manual history list.
- **`pip install -U` of any LangChain package** — you'll break the lock.
