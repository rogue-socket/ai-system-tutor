# Loop 6 — Notes

*Fill in as you go. The "graph wins / graph overkill" reflection in the fix section is the load-bearing content.*

## Concept

What this loop teaches in your own words. What a graph adds over a chain (conditional routing, parallel branches, state visibility). When that's worth the extra ceremony.

If your starter graph was a chain in disguise, write a sentence on what made it that way (no conditionals, no parallel writes, single linear path).

## The break

What was missing in the starter:
- Conditional routing — without it, the graph is a chain.
- Parallel branches — without them, two search backends would have to run sequentially, doubling latency.
- State inspection — without `graph.stream(updates)`, you debug a graph the same way you debug a chain (prints).

Note any specific behaviors you observed when you added each piece — e.g. when you flipped from `invoke` to `stream`, what did you see that you couldn't see before?

## The fix

**The graph-wins / graph-overkill reflection (mandatory):**

Two short paragraphs:

1. **Where the graph wins.** Pick a specific feature you implemented (parallel search, conditional routing, state diff streaming). Sketch how you'd express the same thing in Loop 5's chain. Be honest about how awkward it'd be — chained calls? `RunnableParallel`? `RunnableBranch`? How does the resulting code compare to your graph?

2. **Where the graph is overkill.** Take a concrete example *from this loop* where the graph machinery doesn't earn its keep — a node that does nothing branching, a node whose only job is to pass state through. If your graph has any of those, name them. They're the chain-shaped parts of your graph.

End with: **"I'd reach for a graph when ___, and a chain when ___."** Concrete criteria, not vibes.
