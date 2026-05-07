# Loop 5 — Notes

*Fill in as you go. The Stage 1 mapping table is the most important content — do not skip it.*

## Concept

What this loop teaches in your own words. What LangChain *is* (a layer of conventions and abstractions over what you built in Loops 1–4), what it gives you, what it hides. Why MCP exists.

**Mapping table (Stage 1):**

| LangChain | Loop 4 plain Python equivalent |
|---|---|
| `ChatGoogleGenerativeAI` | `genai.Client` + model string |
| `@tool` decorator | function in `tools.py` + entry in `REGISTRY` |
| `ChatPromptTemplate` | (your `system_prompt()` builder) |
| `MessagesPlaceholder("agent_scratchpad")` | |
| `MessagesPlaceholder("chat_history")` | (`history: list[Content]` in agent.py) |
| `create_tool_calling_agent` | |
| `AgentExecutor` | (`turn()` while-loop with function-call dispatch) |
| `executor.invoke({...})` | one call to `turn(user)` |
| `langchain-mcp-adapters` `load_mcp_tools` | (no equivalent — Loop 4 has no protocol layer) |

## The break

What was missing in the starter and what each missing piece would cost. Specifically:
- Without `chat_history`, multi-turn fails. How does that compare to Loop 4 where you maintained `history` yourself?
- Without long-term memory wiring, `remember`/`recall` aren't available. Did re-implementing them in LangChain take more or less code than Loop 4?
- Without MCP, every tool has to live in your codebase. Why is that limiting at scale?

## The fix

**The comparison reflection (mandatory):**

Three short paragraphs:
1. **This code is shorter.** Where specifically? (Boilerplate cut, abstractions reused, conventions assumed.)
2. **This code is now opaque.** Where specifically? Name two things you understood deeply in Loop 4 that you no longer see in the LangChain version. (Examples: how the function-call routing works, how the tool schemas are derived, what happens when a tool raises.)
3. **This is what I'd debug next.** If the agent does something wrong in this LangChain version, what's your debugging plan? Where does `verbose=True` help? Where does it not?

**MCP reflection:**

One paragraph on what MCP changes about agent architecture. *"Tools authored elsewhere, consumed via protocol"* — what does that enable? Distributed teams, capability marketplaces, tool reuse across agents in different languages. Where might this still bite you (latency, security, version skew)?
