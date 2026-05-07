# Loop 7a — What's Broken

Same Group B venv. Three single-agent architectures, each with one architectural defect. Plus a baseline (single LLM call, no architecture) for comparison.

The shared `benchmark.py` has 10 word problems with known answers. **Don't rewrite it** — Loop 7b uses it as-is, Loop 9 extends it. The eval discipline you build here carries forward.

## Run all four baselines first

```bash
python baseline.py            # control: single LLM call
python reflexion.py           # broken: no quality-based termination
python planner_executor.py    # broken: no replanning when steps fail
python self_consistency.py    # broken: string-match voting
```

Each prints a summary: accuracy, avg latency, total tokens, total iterations, and a per-task breakdown. **Save the four numbers from each architecture in `NOTES.md` under "the break."** You'll compare against post-fix numbers.

What you'll likely see (numbers will vary):
- **Baseline**: ~80–100% accuracy on this benchmark, ~1 iter/task. The simple problems don't need architecture.
- **Reflexion**: same accuracy as baseline OR worse, but ~10x cost (5 iters × 2 calls each = 10 calls/task minimum).
- **Planner-executor**: variable accuracy — better on multi-step problems, worse on trivial ones (planner over-decomposes "8 - 3").
- **Self-consistency**: comparable accuracy, ~5x cost. May be worse than baseline if string-match voting picks a minority "4.0" over a majority "4" in the same task.

This is the moral of Loop 7a in advance: **architecture isn't free, and on simple tasks it can hurt.** Each fix below makes the architecture earn its keep.

## Your task — five stages

### Stage 1 — Run, measure, record (30 min)

Run all four. Record accuracy / avg latency / tokens / iterations in `NOTES.md` as a table. For each architecture, write one sentence on which task class it helps vs hurts compared to baseline.

This is the load-bearing exercise of Loop 7a. **No architecture insight is durable without numbers behind it.**

### Stage 2 — Fix Reflexion's convergence

In `reflexion.py`, terminate the loop when `last_critique` starts with `"OK"`. Re-run. The accuracy shouldn't change much, but the avg iterations / tokens should drop sharply on tasks that converge in 1 try.

In `NOTES.md`: by how much did tokens drop? Did any task get worse because the critic prematurely approved a wrong answer (false-OK)?

### Stage 3 — Add replanning to planner-executor

In `planner_executor.py`, after each step's executor result, add a sanity check: ask a small LLM call *"is the result reasonable for this step?"*. If no, re-plan from this point.

```python
SANITY_PROMPT = "Step: {step}\nResult: {result}\nIs this result reasonable for the step? Reply YES or NO + one-line reason."
```

If `NO`: regenerate the plan starting from where it failed, with the failure as additional context. Cap re-plans at 2 to avoid runaway.

Re-run the benchmark. Does accuracy go up? Tokens? Trade-off worth it?

### Stage 4 — Smarter self-consistency voting

In `self_consistency.py`, replace the string-match voting with **numeric voting**: parse a number from each sample (regex, like `benchmark.check_answer` does), and vote on the most common number (using `abs(a - b) < 0.01` for equality).

Re-run. What happened?

Bonus: if N samples are evenly split between two numbers, what should you do? (Pick the one with the *highest individual confidence*? Re-sample? Default to a tie-breaker?) Try one approach and note the result.

### Stage 5 — Comparison table + reflection

Run all four (with your fixes) one final time. Build the comparison table in `NOTES.md`:

| Architecture | Accuracy | Avg latency | Total tokens | Cost ratio vs baseline | When worth it? |
|---|---|---|---|---|---|

Then write the **architecture decision rubric** in `NOTES.md` (the most important content):

> "I'd reach for **reflexion** when ___."
> "I'd reach for **planner-executor** when ___."
> "I'd reach for **self-consistency** when ___."
> "I'd stay with a **single agent** when ___."

Concrete criteria. Not vibes.

## When you get stuck

- **Tokens is 0 in some results.** `usage_metadata` may be `None` for streamed responses; for `invoke` it should be populated. If you see 0s consistently, log `resp.response_metadata` to see what fields exist on this SDK version.
- **Reflexion's critic says "OK" on wrong answers.** That's the *false-OK* failure mode. Tighten the critic prompt: include the problem context, demand the critic show its work briefly. Note in `NOTES.md`.
- **Planner generates 8 steps for "what is 2 + 2".** Over-decomposition is a planner-exec failure mode. Tighten the planner prompt to "minimum number of steps needed; trivial problems are 1 step."
- **Self-consistency voting ties.** Common with N=5 on a confused problem. Pick a tie-breaker explicitly; don't let `Counter.most_common(1)` silently pick the first.
- **Free tier rate limit (429).** Each architecture hits the API many times per task. If you hit 429, wait a minute or break the benchmark into halves (`tasks=benchmark.TASKS[:5]`).

## What you specifically should NOT use

- **Loop 7b's multi-agent architectures** — wait for that loop. The single-agent improvements come first because multi-agent is often *one of these* with a coordinator on top.
- **`pip install -U`** — same warning.
- **A new benchmark.** Reuse `benchmark.py`. The shared eval is the point.
