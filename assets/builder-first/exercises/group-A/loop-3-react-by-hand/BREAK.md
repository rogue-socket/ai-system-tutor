# Loop 3 — What's Broken

ReAct (Reason-Act-Observe) is the most common explicit-reasoning agent pattern. The model alternates between Thought, Action, and Observation, building toward a Final Answer. It's the conceptual ancestor of every agent framework you'll meet later.

The starter implements ReAct with text parsing — no native function calls (that was Loop 2's win). This time we go *back* to parsing structured text from the model's output channel, on purpose, because the failure modes here are properties of the *loop pattern*, not the parsing technique.

It works on simple queries. It breaks on complex ones. The kind of break is the lesson.

## Run it

```bash
python react_agent.py
```

Try these tasks **in order** — each one is harder than the last:

1. `what is 12 + 7?` *(single-step, should work)*
2. `what's the capital of France?` *(single-step, should work)*
3. `find the population of the capital of France, then multiply by 2` *(2–3 step)*
4. `what's the population of Paris times the population of Tokyo?` *(2 searches + 1 calc)*
5. `compute the sum of all the populations of Paris, Tokyo, New York, and London` *(4 searches + 3 calcs — watch this one)*

Each task creates a `traces/<timestamp>.jsonl` file. **Read the latest trace after every run:**

```bash
python traces.py
```

The trace is the artifact you debug. `react_agent.py`'s output is just the final answer; the trace is where you see why the answer is wrong (or how it almost broke even when it was right).

## What's broken

1. **No max-iteration cap.** If the model never emits "Final Answer:", `react()` loops until you Ctrl-C or hit a rate limit. Try task 5 — count the iterations.
2. **Brittle Action parsing.** The regex assumes `Action: tool(args)`. The model sometimes writes `Action: search query about Paris` (no parens) or `Action: search('population of Paris, France')` (comma inside quoted args breaks the dumb split). Both produce silent or crashing failures.
3. **Brittle calculator args.** When the search returns "approximately 2.1 million", the model often emits `calculator(2.1 million, 2, *)`. `float("2.1 million")` raises `ValueError`. Or it emits `calculator(2.1, 2, *)` (asterisk unquoted) — different failure.
4. **No malformed-output recovery.** When `parse_action` fails, the loop sends back `"Observation: (no action found, continue)"` and hopes. Sometimes the model recovers; sometimes it loops emitting the same broken text forever.
5. **No premature-termination detection.** If the model emits `Final Answer: I think it's around 4 million` *before* doing the search, the loop accepts it.
6. **The 10-iteration degradation.** Even when parsing works, traces longer than ~10 steps degrade — model repeats actions, hallucinates tools, invents observations. Task 5 is designed to surface this.

## Your task — five stages

### Stage 1 — Run, fail, read traces (45 min)

Run all 5 sample tasks. After each, run `python traces.py` and read the trace. For each task, write under "the break" in `NOTES.md`:
- What the model attempted (one-line bullet of the actions it took)
- What broke (parsing fail / infinite loop / premature termination / degradation / nothing)
- Whether the *final answer* was correct, even if the process was messy

This is the load-bearing skill of Loop 3: **reading a trace to identify the failure mode by name**. You will use this in every loop after this.

### Stage 2 — Add a max-iteration cap

Set `MAX_STEPS = 10`. If the loop hits the cap without a Final Answer, return a graceful failure (string like `"I couldn't reach a final answer in 10 steps."`) and log it as an error event. Re-run task 5. Compare the trace to Stage 1's.

### Stage 3 — Malformed-output recovery

Replace the `"(no action found, continue)"` filler with a *coaching* observation:

> `"Observation: I couldn't parse your action. Use the format: Action: tool_name(arg1, arg2). Available tools: search, calculator."`

Force a malformed output (e.g. by making the system prompt vague mid-run, or by adding a task the model can't easily structure) and watch whether the model recovers on the next turn.

### Stage 4 — Premature termination guard

If the model emits `Final Answer:` before any successful Observation in this trace, reject it. Send back:

> `"Observation: You haven't gathered any information yet. Continue with Thought + Action."`

This heuristic has a false positive: tasks that need no tools (`what is 2+2?`). Decide how you'll handle that — don't pretend the heuristic is perfect. Note your choice in `NOTES.md`.

### Stage 5 — The "what would I want from a framework" reflection

You've now hit at least three failure modes that aren't really *your* problem to solve from scratch — every agent system has them. Write one paragraph in `NOTES.md` (under "the fix") naming what you'd want from a framework that abstracts all of this. Be concrete — name the failure modes you'd want it to handle, the trace format you'd want, the recovery strategies you'd want pre-built.

This sets up Loop 5 directly. The next time you reach for LangChain or LangGraph, you'll know exactly what you're paying it to do.

## When you get stuck

- **The trace files pile up.** Delete `traces/*.jsonl` periodically, or keep them — they're useful when you compare a Stage-1 run to a Stage-3 run.
- **`traces.show()` doesn't surface what you need.** Edit it. The trace format is yours; if you want to see the raw model response, add a `raw` event in `react_agent.py` and a corresponding pretty-print case in `traces.show`.
- **Action parsing is harder than it looks.** The model's freedom of phrasing is the problem. You can either (a) tighten the system prompt with stricter rules and 1–2 examples, or (b) post-process more aggressively. (a) is usually better — show, don't tell.
- **Infinite loops mid-development.** Ctrl-C works; the trace file is still there to read.

## What you specifically should NOT use

- **Native function calling** — that was Loop 2. ReAct is deliberately parsing the model's text output channel. The point is to feel why this is hard at scale.
- **`langchain`, `langgraph`** — Loop 5+. Resist the urge.
- **`client.chats`** — manage history yourself.
