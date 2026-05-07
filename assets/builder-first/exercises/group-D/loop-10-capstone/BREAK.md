# Loop 10 — Capstone

The capstone is integrative. There's nothing new to learn — everything you need came from Loops 1–9. The skill being built here is **shipping**: cutting scope, finishing, writing the README, owning the postmortem.

> **The most important skill of this loop is scope cut.** When the tutor pushes back on something you want to add, default to "OK, that's v2." A capstone that ships at smaller scope beats a capstone that doesn't ship.

This loop reuses Group D's venv. No new dependencies; pull in what you need from prior loops.

## Step 1 — Pick ONE project

Read `PROJECTS.md` end-to-end. Pick exactly one of the five options. Don't try to combine.

The choice should fit two criteria:
1. **You'd want to use the result.** Capstones you don't care about don't get finished.
2. **The scope fits 20–40 hours.** If you have to cut anything from PROJECTS.md's "scope (v1)" list to make it fit, you're picking the wrong option.

Tell the tutor your pick + why. The tutor will challenge you on scope-creep risks specific to that choice. Argue back if you disagree, but the default is "tutor pushes you to be smaller."

## Step 2 — Spec it (1 hour, mostly writing)

Write `SPEC.md` in the project folder with:
- **Goal.** One sentence — what does done look like?
- **In-scope.** Bullet list. Be specific.
- **Out-of-scope.** Bullet list. Each item is a thing that's tempting and you're explicitly cutting.
- **Eval shape.** What 20 test cases look like. Pick the schema now; you'll fill cases as you go.
- **Stack.** Which prior loops' code you'll lift, which group venv, which deps.

The tutor reviews `SPEC.md`. Common pushback: *"the in-scope list has 10 items, that's too many."* Cut to 5.

## Step 3 — Build it (12–20 hours)

Two ways the build typically goes wrong:

1. **Tracer bullet first, then quality.** Get an end-to-end version working (even badly) within the first 4 hours. Then improve. Don't perfect each layer before moving to the next — you'll run out of time at Layer 3.
2. **Eval cases as you build.** Write your 20 eval cases in batches of 5 across the build, not all at the end. Cases written before the implementation reveal scope-creep early.

Lift code from earlier loops — that's the point of having done them:
- LangGraph from Loop 6 if your agent has clear branching.
- Native function calling pattern from Loop 4.
- Hybrid retrieval from Loop 8 if you went with Option A.
- LangChain MCP integration from Loop 5 if your tools live behind a protocol.
- Caching, retries, cost tracking from Loop 9.

You will *not* implement Loop 9's full 12 production stages on the capstone. Pick 3–4 that matter most for your project. For Option A (RAG): caching, eval, observability. For Option C (task agent): retries, cost tracking, injection guards. Etc.

## Step 4 — Eval it (3–5 hours)

Write 20 cases in `evals/cases.json` (template in this folder). Run them via a `run_offline.py` (lift Loop 9's, modify for your project's scoring).

Pass-rate target: 80%+ on v1. If you're at 60%, debug; if you're at 95%, your cases are too easy — add harder ones.

Run the eval harness on every meaningful change. *"This change improved pass-rate from X to Y"* is the foundation of the postmortem.

## Step 5 — Deploy it (1–2 hours)

Lift Loop 9's Dockerfile. Deploy to Cloud Run / Fly / Render. The HTTPS URL is part of the WIN criteria — the tutor will hit it.

If your project is a CLI (Option E sometimes), "deploy" means it runs reliably on a fresh machine — `git clone <url>`, `cd <repo>`, `uv sync`, `python ...` (each as a separate command; works in every shell). Document the steps in README.

## Step 6 — README (1 hour)

Use `README_TEMPLATE.md` in this folder. Don't skip the deployed URL or the eval results. Include cost numbers — *"X tokens per request, ~$Y per 1K requests"*.

## Step 7 — Postmortem (1–2 hours)

Use `POSTMORTEM_TEMPLATE.md`. Five honest paragraphs. **The postmortem is non-negotiable.** This is where the curriculum becomes durable knowledge.

Write it the day after you finish, not the day of. Sleep on it.

## When you get stuck (the most common patterns)

- **You're 15 hours in and the in-scope list has 12 items.** Cut. Right now. Move 7 to "v2 ideas". Cutting in week 2 is cheaper than cutting in week 4.
- **The eval cases keep failing on edge cases that don't matter for v1.** Are those edges in your in-scope list? If not, they're out of scope; remove the failing cases from the eval, not the agent.
- **The agent works locally but not on the deployed instance.** 90% of the time it's an env-var issue (`.env` not in the deployed image, or the secret isn't set in the cloud provider's console). Read the deployed instance's logs.
- **You can't decide between LangGraph and plain Python.** Plain Python until you have a reason. The reason should be conditional routing or parallel branches. Most capstone-scope projects don't have either; default to plain Python.
- **The postmortem feels like writing a school essay.** Bullet points are fine. Honesty matters more than prose. *"I overengineered the retry logic; nothing in eval ever timed out"* is a perfect postmortem sentence.

## What you specifically should NOT do

- **Don't add a feature that's not in your SPEC.md after Step 2.** If something must change, edit SPEC and acknowledge the cost.
- **Don't skip the postmortem.** It's the most important deliverable. Curricula without postmortems produce engineers who repeat the same mistakes for years.
- **Don't ship without 20 eval cases.** Untested agents are not shipped agents.
- **Don't try to combine two projects.** Pick one.
