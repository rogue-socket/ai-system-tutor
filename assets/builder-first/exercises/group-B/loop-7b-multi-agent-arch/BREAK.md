# Loop 7b — What's Broken

Same Group B venv. Three multi-agent architectures: hierarchical (manager + workers), orchestrator (step-by-step dispatcher + workers), peer (two agents propose & critique). Same benchmark as Loop 7a — `benchmark.py` is identical, do not modify.

The "broken" thing here isn't a bug — all three architectures run. **The break is architectural.** Most multi-agent systems in 2026 are one agent with bad prompts wearing a costume. By the end of this loop you should be able to tell the difference, and you should distrust your own multi-agent designs by default.

`MULTIAGENT_TRAP.md` is non-negotiable reading. Read it after Stage 2 — not before. Run the architectures first; the checklist lands harder when you've felt the cost.

## Run all three first

```bash
python hierarchical.py
python orchestrator.py
python peer.py
```

Each prints a summary just like Loop 7a's runs. Save the four numbers (accuracy / latency / tokens / iterations) for each, in `NOTES.md` under "the break."

You should have Loop 7a's numbers from your earlier work — keep them open.

## Your task — five stages

### Stage 1 — Run all three, record numbers (30 min)

The numbers go in `NOTES.md` next to your Loop 7a numbers. You're building one big comparison table.

Likely outcome (varies): **all three multi-agent architectures cost 3-5x what baseline did and produce comparable or worse accuracy on the Loop 7a/7b benchmark.** That's not a bug; that's the lesson. The benchmark is simple word problems, and architecture overhead doesn't pay for itself when the task is simple.

If you see a multi-agent architecture WIN on accuracy, note exactly which task it nailed that baseline missed. There usually is at least one — that's where the architecture earned its keep on this specific input.

### Stage 2 — Read `MULTIAGENT_TRAP.md` carefully

Don't skim. The five failure modes are diagnostic — apply them.

### Stage 3 — Apply the checklist to each of your architectures

For each of the three, write in `NOTES.md` (under "the fix"):
- Which of the 5 failure modes does it exhibit? Concrete examples from your benchmark runs.
- Which of the 3 "multi-agent IS justified" cases does it fall into? (Probably none, since all three use the same Gemini Flash model.)

If your hierarchical solution exhibits 4 of 5 failure modes and zero of the 3 justifications — that's the answer. Write it down.

### Stage 4 — Re-implement one as well-prompted single-agent

Pick the multi-agent architecture that performed *best* on the benchmark. Re-implement it as a **single LLM call with carefully-tuned prompts** — the prompts can encode "first decompose, then solve, then sanity-check" all in one pass. No coordination, no separate workers.

Save as `well_prompted.py` (your file). Run on the same benchmark. Compare to its multi-agent cousin.

In `NOTES.md`:
- Which won — multi-agent or well-prompted single?
- By how much (accuracy, tokens, latency)?
- Did the multi-agent version add anything the well-prompted single didn't?

If "no" — that's the most important finding in builder-first. Sit with it.

### Stage 5 — The one-sentence test

Write in `NOTES.md` your final answer to:

> "I'd use multi-agent for ___ specifically because ___, and I've ruled out single-agent-with-better-prompts because ___."

The answer should be concrete enough that you could defend it against an engineer who'd say "it's just one agent with role-play." If your blanks are vague, the multi-agent answer is wrong for whatever case you're imagining.

## When you get stuck

- **Hierarchical's manager outputs free-form text instead of `worker: task` lines.** Tighten the manager prompt with one example. Or post-process loosely. (Loop 7b's manager parsing is intentionally rigid; the lesson is that parsing structured manager output is a tax.)
- **Orchestrator goes in circles** (compute, compute, compute…). The orchestrator's blind-spot is cost — it doesn't naturally finalize. Tighten the orchestrator prompt with "if you have an answer, FINALIZE NOW." Or cap iterations harder.
- **Peer's critique is always AGREE.** That's a false-AGREE — same failure as Reflexion's false-OK. The lesson generalizes.
- **Free-tier rate limit (15 RPM).** Multi-agent runs many calls. Halve the benchmark if needed.

## What you specifically should NOT use

- **AutoGen, CrewAI, multi-agent frameworks** — those are out of scope for builder-first. The point of writing these by hand is to see what the frameworks abstract — and what they hide. (The frameworks are great for production multi-agent systems *after* you've internalized when those are appropriate.)
- **`pip install -U`** — same warning.
- **A new benchmark.** Use the existing one.
