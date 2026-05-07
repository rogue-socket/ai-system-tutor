# Loop 7a — Cheatsheet

*Fill in as you build.*

## Commands

- `python baseline.py` — control
- `python reflexion.py` — self-critique loop
- `python planner_executor.py` — plan-then-execute
- `python self_consistency.py` — vote across N samples
- `python -c "from benchmark import TASKS; print(len(TASKS))"` — count tasks

## Patterns

3–5 reusable code snippets. Suggestions:

- The `agent_fn(question) -> {answer, tokens, iterations}` shape — a uniform interface across all architectures.
- The Reflexion loop with `OK`-prefix termination.
- The planner-executor sanity-check + replan pattern.
- The numeric voting helper (regex-extract + `abs(a-b)<0.01` equivalence).
- The `usage_metadata.total_tokens` accumulation pattern.

## Gotchas

3–5 traps. Suggestions:

- `usage_metadata` may be None on some response shapes. Use `(resp.usage_metadata or {}).get(...)`.
- The critic in reflexion can produce false-OKs — the answer is wrong but the critic approves. Tighten the critic prompt with show-your-work.
- The planner can over-decompose trivial problems. Tighten the planner prompt with "minimum number of steps; trivial = 1 step."
- String voting in self-consistency is brittle. Numeric voting fixes math; semantic voting (LLM-as-judge) is needed for free-form text — that's Loop 9.
- Free-tier rate limits (15 RPM, 1500 RPD). All four architectures running can hit ~200+ calls; halve the benchmark if you're approaching the limit.

## Numbers

Suggestions:

- Cost ratio reflexion-vs-baseline (post-fix): ~_N_x.
- Cost ratio self-consistency-vs-baseline (N=5): ~_N_x.
- Tasks where planner-executor's replan kicked in: _N_/10.
- Tasks where numeric voting picked differently from string voting: _N_/10.
- Free-tier RPM hit: yes/no, at iteration ~_N_.
