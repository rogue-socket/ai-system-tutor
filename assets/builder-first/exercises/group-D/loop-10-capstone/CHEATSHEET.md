# Loop 10 — Cheatsheet

*Capstone-specific. Light on commands (your project defines them); heavy on the meta-skills.*

## Commands (project-specific — fill in)

- `<run command>` — start the agent
- `python evals/run_offline.py` — run eval
- `<deploy command>` — deploy

## Patterns

The patterns that matter for capstone are mostly *meta*, not code-level:

- **Tracer-bullet first.** End-to-end working version (badly) before any layer is polished.
- **Eval cases as you build, in batches of 5.** Not all at the end.
- **Lift from prior loops; don't re-derive.** That's why prior loops exist.
- **Pick 3–4 production stages, not all 12.** Match production hardening to the project's actual risk profile.
- **Postmortem in bullets.** Honesty > eloquence.

## Gotchas

3–5 traps. Suggestions:

- Choosing the bigger project option. Smaller capstone ships; bigger doesn't.
- Adding a feature mid-build "just because." If it's not in `SPEC.md`, edit SPEC and acknowledge cost. Don't quietly add.
- Skipping the deploy step because "it works locally." Deployment surfaces real bugs (env vars, image size, cold starts).
- Skipping the postmortem because the project is "obviously" successful or "obviously" not. The postmortem is non-negotiable regardless.
- Writing 20 eval cases all at the end. Pre-write 10 from `SPEC.md`'s in-scope list before any code.

## Numbers (for your project)

- Lines of code shipped: _N_.
- Lines lifted from prior loops: _N_.
- Eval pass rate: _N_/20.
- Avg latency per request: _N_ ms.
- Cost per 1K requests: $_X_.
- Time spent: _N_ hours (vs estimated 20–40).
- Items cut from initial scope: _N_.
