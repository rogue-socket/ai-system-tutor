# Loop 6 — Cheatsheet

*Fill in as you build.*

## Commands

- `python graph_agent.py` — run
- `python -c "from graph_agent import graph; print(graph.get_graph().draw_ascii())"` — visualize

## Patterns

3–5 reusable code snippets. Suggestions:

- The minimal graph build: `StateGraph(State).add_node(...).add_edge(...).compile()`.
- `add_conditional_edges(source, fn, mapping)` — the routing primitive.
- The reducer pattern: `Annotated[list[T], operator.add]` for parallel writes.
- Parallel fan-out: two `add_edge`s from the same source; converge with a third node both edge into.
- `graph.stream(input, stream_mode="updates")` — per-node state diffs as they happen.

## Gotchas

3–5 traps. Suggestions:

- Without a reducer, parallel writes raise `InvalidUpdateError`.
- TypedDict without `total=False` requires you to populate every field at invoke time.
- The conditional-edges `path_map` (third arg) maps return-values-of-fn → node-names. Easy to put node-names in the wrong place.
- If two parallel branches finish at different times, downstream nodes wait for both before firing — that's a *barrier*, not a *first-completer-wins*. Different from `asyncio.wait`.
- LangGraph's "subgraphs" exist for nested control flow but you don't need them in Loop 6.

## Numbers

Suggestions:

- Total nodes in your graph: _N_
- Edges: _M_ (linear: _X_, conditional: _Y_, parallel: _Z_)
- Latency for math route vs lookup route vs chat route: ~_a_ ms / _b_ ms / _c_ ms
- Did parallel search actually save time vs sequential? Measure with `time.perf_counter()` around the lookup branch.
