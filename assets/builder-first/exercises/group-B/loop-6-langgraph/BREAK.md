# Loop 6 — What's Broken

Same Group B venv as Loop 5 — no `uv sync` needed if you came straight from Loop 5.

The starter is a 2-node LangGraph: `receive → llm → END`. It runs. It works. It does *nothing* a chain couldn't do — the graph machinery is there but earns nothing. **That's the lesson.** Your job is to make it earn its keep.

If a graph isn't doing anything a chain can't, it's a chain wearing a costume. After Loop 5 you should be suspicious of frameworks that don't pay rent. LangGraph specifically pays rent in two places: **conditional routing** (decide where to send state at runtime) and **parallel branches** (run nodes concurrently, merge results). Both are awkward to express in a chain.

## Run it first

```bash
python graph_agent.py
```

Try anything — `12 + 7?`, `weather in Paris?`, `tell me a joke`. The graph does the same thing every time: wrap input, call LLM, return.

## Your task — five stages

### Stage 1 — Add a router node + conditional edges

Add a `router(state)` node that classifies the user's input as one of:
- `"math"` — looks like an arithmetic question
- `"lookup"` — looks like a fact-lookup question
- `"chat"` — anything else

Use a small LLM call inside the router (single classification prompt, expects one word back). Set `state["route"]` to the result.

Then add three placeholder branch nodes (`math_node`, `lookup_node`, `chat_node`) — each just sets `final_answer` to a dummy string for now. Wire them with a `conditional_edges`:

```python
g.add_conditional_edges(
    "router",
    lambda state: state["route"],
    {"math": "math_node", "lookup": "lookup_node", "chat": "chat_node"},
)
```

Test: ask different kinds of questions, watch the dummy answer change based on route. **This is the moment the graph stops being a chain.**

### Stage 2 — Implement the math branch

`math_node` parses an arithmetic expression from `state["user_input"]` and computes it. Keep parsing simple — a regex like `(\d+)\s*([+\-*/])\s*(\d+)` is fine; this loop isn't about robust parsing (Loop 2 was). Write to `math_result`. The synthesize node (Stage 5) will format it.

### Stage 3 — Parallel sub-branch in lookup

Inside the lookup branch, add **two parallel search nodes** that both write to `search_results` (the `Annotated[list, operator.add]` reducer in `state.py` makes this safe):

- `search_a(state)` — return a hardcoded fact-list result (mock).
- `search_b(state)` — return a different hardcoded fact-list result (mock).

Wire them in parallel from `lookup_node`. Both run, both append to `search_results`. Then a `merge_lookup(state)` node deduplicates / formats the merged list.

In LangGraph, parallelism is implicit — if you `add_edge("lookup_node", "search_a")` and `add_edge("lookup_node", "search_b")`, both fire. To converge: have both edge into a `merge_lookup` node.

Test: when the route is "lookup", verify both search functions actually executed (add a print in each) and the merge produced something sensible. **This is the second thing a chain can't do cleanly.**

### Stage 4 — Implement the chat branch + synthesize node

`chat_node` calls the LLM with the user's input and writes to `chat_response`.

`synthesize_node` reads whichever branch ran (look at `state["route"]`) and assembles `final_answer`. Wire all three branches to `synthesize_node`, and `synthesize_node` to `END`.

### Stage 5 — State inspection + comparison reflection

Add a small instrumentation pass: at every node, print the state diff (what the node changed). LangGraph supports this natively via `graph.stream(...)` instead of `graph.invoke(...)`:

```python
for event in graph.stream({"user_input": user}, stream_mode="updates"):
    for node, update in event.items():
        print(f"  [{node}] {update}")
```

Run a few queries. **This is the load-bearing skill of Loop 6 — graphs earn their keep through visibility into the run.**

Then write the comparison reflection in `NOTES.md`:
- Pick a feature from the graph (conditional routing, parallel search, state inspection).
- Sketch how you'd express it in Loop 5's plain LangChain chain.
- Be honest: where does the graph win, where is it overkill?

## When you get stuck

- **`StateGraph` constructor takes the schema** — `StateGraph(AgentState)`. Not `StateGraph(state_schema=AgentState)` in 0.4.x.
- **TypedDict with `total=False`** lets you start without all keys populated. Without it, missing keys at invoke time will error.
- **Reducer required for parallel writes.** If two nodes both update the same field with no reducer, LangGraph raises `InvalidUpdateError`. Use `Annotated[T, reducer]` in the state.
- **`add_conditional_edges`** is the routing primitive. The function you pass returns the *value* the routing dict maps from — strings work fine.
- **`graph.stream(..., stream_mode="updates")`** yields per-node state updates. Use this for visibility.
- **Visualize the graph** with `print(graph.get_graph().draw_ascii())` — sanity-checks your wiring.

## What you specifically should NOT use

- **A `MessageGraph` shortcut** — LangGraph has prebuilt patterns (`create_react_agent`, etc.). Don't use them; the point is to *build the graph by hand*.
- **`pip install -U`** — same warning as Loop 5.
- **Adding tools via `bind_tools` on the LLM** — that's the Loop 5 pattern. Loop 6 is about graph control flow, not tool calling.
