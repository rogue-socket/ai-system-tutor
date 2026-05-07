# Loop 10 — Win Criteria

You're done — and the curriculum is done — when:

- [ ] Working agent. The tutor can hit a deployed HTTPS URL (or run a documented local command) and exercise the agent.
- [ ] `SPEC.md` from Step 2 exists and matches what you actually built (within reason — drift is OK if acknowledged).
- [ ] `README.md` (using the template) exists and includes: what it does, quickstart, deployed URL, architecture sketch, eval results, cost per request.
- [ ] `evals/cases.json` has at least 20 cases. Pass-rate is documented in the README.
- [ ] At least 3 production stages from Loop 9 are wired in (caching, retries, cost tracking, evals, injection guards, observability — pick what matters for *your* project, not all of them).
- [ ] `POSTMORTEM.md` (using the template) exists. Five sections, honestly answered. **Non-negotiable.**

When all six are checked, you're done with builder-first. Take a break. Come back in a week and re-read your postmortem.

## What "deployed" means

For agents that fit a request/response shape (Options A, B, C, D, E partially): a working HTTPS URL on Cloud Run / Fly / Render that the tutor can curl.

For batch agents (Option E batch flavor): a documented `make run` (or equivalent) command that processes a sample input and produces output, runnable on a fresh clone.

## What the tutor will check

When you say you're done:
1. The deployed URL works (or the local command runs cleanly on a fresh clone).
2. `python evals/run_offline.py` (or your equivalent) runs and reports pass-rate.
3. The README is skimmable in 2 minutes — someone could clone and run.
4. The postmortem is honest. "I built exactly what I planned and everything went smoothly" is suspicious; real projects have drift, cuts, surprises. Name them.
5. Cost numbers exist. "I don't know what this costs" doesn't pass.

## Stretch (after v1 ships)

- **Open-source it.** Push to GitHub with a real README. Apply MIT or similar.
- **Showcase a single hard case.** Pick the one eval case that broke v1, write a deep dive in the README about how you'd fix it.
- **Cost optimization round.** Profile cost per request, find the most expensive call, cut it. Document the saving.
- **Run a live load test against the deployed instance.** What happens at 10x your expected RPS?
- **Hand it to a real user.** Watch them break it in ways you didn't expect. *That* gets added to your eval set.

## After Loop 10

Builder-first is over. You've built and shipped one real agent end-to-end with foundations going down to bare LLM calls and production hardening going up to deployment. You can:
- Read agent code from any 2026 framework and recognize what it's doing.
- Spec a small agent in 30 minutes with realistic scope.
- Deploy and operate one without paging an SRE.
- Push back on architectural overreach (multi-agent, framework-evangelism, premature scaling).
- Read your own traces and find failures by name.

That's the AI Engineer skill set. Where you go next is your call — depth (foundation models internals, fine-tuning, RL), breadth (multi-modal, voice, robotics), or scale (production ML platforms). Each direction has its own curriculum; this one was the on-ramp.
