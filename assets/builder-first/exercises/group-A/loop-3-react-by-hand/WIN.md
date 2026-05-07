# Loop 3 — Win Criteria

You're done when `react_agent.py`:

- [ ] Has a working ReAct loop that produces complete, readable traces in `traces/`. You can run any of the 5 sample tasks and the trace tells the full story.
- [ ] Has a `MAX_STEPS` cap that returns a graceful failure when hit (no infinite loops).
- [ ] Has malformed-output recovery — when action parsing fails, the model gets a coaching observation, not a useless filler.
- [ ] Has a premature-termination guard with explicit handling for tool-free tasks (your choice, named in `NOTES.md`).
- [ ] Has trace-derived failure-mode notes for all 5 sample tasks in `NOTES.md`.
- [ ] Has a "what I'd want from a framework" paragraph in `NOTES.md` (the framework wishlist).

When all six are checked, finish `CHEATSHEET.md`. Then `/loop next` for Loop 4.

## Stretch (optional)

- Add a third tool (e.g. `current_year() -> int`) and ask a query that needs all three. Watch how the model orders them.
- Inject a *failing* tool result on purpose (`"Observation: search returned an error"`) and watch the model recover — does it retry, switch tools, give up?
- Run task 5 ten times. At what iteration count does degradation typically appear in the trace? Compare to the "ReAct degrades after ~10 iterations" claim from the literature.
- Add a `summary(path)` function to `traces.py` that prints the action chain as a tree.

## How the tutor will check

When you say you're done:
1. Run task 3 (population × 2), then walk the tutor through the trace, naming each step.
2. Manually loosen the system prompt to be vague — show malformed-output recovery firing.
3. Show the framework wishlist paragraph.
4. Run task 5 — show MAX_STEPS firing (or the trace running long but cleanly).

Behavior + trace clarity > implementation.
