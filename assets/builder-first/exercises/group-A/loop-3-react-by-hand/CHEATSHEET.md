# Loop 3 — Cheatsheet

*Fill in as you build. Skim-this-in-60-seconds-six-months-from-now.*

## Commands

- `python react_agent.py` — run the loop
- `python traces.py` — pretty-print the latest trace
- `ls -t traces/ | head -5` — find recent trace files

## Patterns

3–5 reusable code snippets. Suggestions to replace:

- The minimal ReAct prompt (T/A/O alternation, available tools, output format).
- The trace event schema (`task` / `thought` / `action` / `observation` / `final` / `error`).
- The MAX_STEPS pattern with graceful failure return.
- The coaching-observation pattern for malformed output recovery.

## Gotchas

3–5 traps. Suggestions:

- The model will sometimes "predict" the Observation in its own output — your prompt must explicitly forbid this.
- Action parsing breaks on commas inside quoted args. Either tighten the format or parse with shlex / ast.literal_eval.
- Long traces don't just fail — they degrade silently. The model starts repeating actions or hallucinating tools. Read the trace, don't trust the final answer.
- "Final Answer:" before any Observation is almost always wrong. Premature termination is a real failure mode worth defending against.

## Numbers

What you observed. Suggestions:

- Average iterations for task 3: _N_
- Average iterations for task 5: _N_
- Iteration at which degradation first appears (task 5): typically ~_N_
- Tokens per iteration (rough): ~_N_ (so a 15-step trace is ~_M_ tokens of context)
- Recovery rate after coaching observation: _X_/_N_ tries
