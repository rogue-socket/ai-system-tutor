# Loop 7a — Win Criteria

You're done when:

- [ ] You ran `baseline.py`, `reflexion.py`, `planner_executor.py`, `self_consistency.py` — pre-fix and post-fix — and recorded the numbers (accuracy, avg latency, tokens, iterations) for all eight runs in `NOTES.md`.
- [ ] **Reflexion** terminates on `"OK"` from the critic. Token count drops meaningfully vs the broken version.
- [ ] **Planner-executor** detects a bad intermediate result and replans (capped at 2 replans). Accuracy goes up on at least one previously-failing task.
- [ ] **Self-consistency** uses numeric voting (regex-extract + `abs(a-b)<0.01` equivalence) instead of exact string match. You can name a task where this changed the outcome.
- [ ] The 4-row comparison table is in `NOTES.md` with cost-ratio-vs-baseline.
- [ ] The architecture decision rubric (when each is worth it) is written in `NOTES.md` with concrete criteria, not vibes.

When all six are checked, finish `CHEATSHEET.md`. Then `/loop next` for Loop 7b — multi-agent architectures, same Group B venv, same `benchmark.py`.

## Stretch (optional)

- Run the benchmark with `gemini-2.5-flash-lite` (cheaper) and `gemini-2.0-flash-thinking-exp` (more expensive but reasoning-tuned). Compare per-architecture. Does reflexion still help on a reasoning model?
- Add a "hard" task set to `benchmark.TASKS` — multi-step problems where baseline drops to ~50%. Re-run all architectures. The architecture wins should now be visible.
- Add a `compare.py` that runs all four and prints a single combined table.
- Build a "best-of-N + critic" hybrid: sample N answers, run each through the critic, return the highest-rated.

## How the tutor will check

When you say you're done:
1. Run `baseline.py` — see the control numbers.
2. Run `reflexion.py` (post-fix) — show the iteration count dropping for converged tasks.
3. Run `planner_executor.py` (post-fix) — point at a task where the replanner kicked in (you should be able to log when it fires).
4. Run `self_consistency.py` (post-fix) — point at a task where numeric voting picked differently from string voting.
5. Read aloud the architecture decision rubric.

Behavior + numbers > implementation polish.
