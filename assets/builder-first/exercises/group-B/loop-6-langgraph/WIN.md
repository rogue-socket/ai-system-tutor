# Loop 6 — Win Criteria

You're done when the graph:

- [ ] Has a `router` node that classifies user input as `math` / `lookup` / `chat` and conditional edges that dispatch accordingly.
- [ ] Has a working math branch (parses + computes a simple arithmetic expression).
- [ ] Has a lookup branch with two **parallel** search nodes whose results merge through a reducer. Both nodes verifiably execute (you've seen the prints).
- [ ] Has a chat branch that handles anything not classified as math or lookup.
- [ ] Has a synthesize node that produces `final_answer` from whichever branch ran.
- [ ] You can run `graph.stream(..., stream_mode="updates")` and see the per-node state diffs.
- [ ] `NOTES.md` has the comparison reflection: where does the graph win over Loop 5's chain, where is it overkill?

When all seven are checked, finish `CHEATSHEET.md`. Then `/loop next` for Loop 7a (single-agent architectures, same Group B venv).

## Stretch (optional)

- Visualize: `print(graph.get_graph().draw_ascii())` — paste the ASCII into `NOTES.md`.
- Add a checkpointer (`from langgraph.checkpoint.memory import MemorySaver`) so state survives across `invoke`s, then re-implement multi-turn memory.
- Add a third parallel branch to lookup (a third "search backend") and observe how the merge handles three sources.
- Add an early-exit edge: if `router` decides the question is trivially answerable, skip the branch nodes and go straight to `synthesize`.

## How the tutor will check

When you say you're done:
1. Ask a math query — only `math_node` fires (verify in stream output).
2. Ask a lookup query — both `search_a` and `search_b` fire in parallel; `merge_lookup` consolidates.
3. Ask a chat query — only `chat_node` fires.
4. Show the per-node state diffs from `graph.stream(...)`.
5. Read aloud the "graph wins / graph overkill" paragraph from `NOTES.md`.

Behavior + state visibility > polish.
