# Capstone Postmortem — <Project name>

*Write this the day after you finish, not the day of. Sleep on it. Honest > eloquent.*

## What I built

One paragraph. What does it do, what's the deployed/runnable form, what was the time investment.

## What worked

3–5 bullets. Don't pad — name only the things that genuinely worked. Specific examples beat general claims.
- *e.g. "Lifting Loop 8's hybrid retriever wholesale saved ~6 hours; the by-type accuracy table from Loop 8 told me ahead of time that hybrid would be the right pick for my corpus."*

## What I over-engineered

3–5 bullets. The most useful section. Look at every "and then I added..." moment and ask whether it was needed.
- *e.g. "Built LangGraph branching for a single linear flow. Same code in plain Python is 30% shorter and clearer. Loop 6's lesson didn't stick."*
- *e.g. "Implemented retries with backoff before I'd seen any transient failures. Eval logs over 200 calls show zero retries fired."*
- *e.g. "Built a custom token-counting wrapper because I distrusted Gemini's `usage_metadata`; the SDK's value was within 2% of mine. Wasted two hours."*

## What I cut (and missed)

What you initially planned and removed mid-build, and whether you regret it. Some cuts are obviously right; some are eating you.
- *e.g. "Cut multi-turn memory in week 1. Don't regret it; v1 ships."*
- *e.g. "Cut LLM-as-judge bias controls because Loop 9's stage 4 felt complex. Probably regret — eval pass-rate is 85% but I don't know if the judge is over-counting."*

## What I'd do differently

3–5 bullets. Forward-looking, not blame-y.
- *e.g. "Write the eval cases first. I wrote 5 cases in week 1, 15 in week 4. The week-1 cases caught a scope-creep bug I would have ignored otherwise."*
- *e.g. "Pick the smaller project option. I chose RAG-over-50K-docs; should have picked RAG-over-200-docs. The corpus size dragged everything else."*

## Open questions / what's next

What you didn't resolve:
- A bug you couldn't reproduce.
- A behavior you suspect is wrong but couldn't prove.
- A scaling question you didn't get to.
- Something the eval doesn't cover but should.

## Cost (for the record)

How much did the build itself cost (your token spend during development)?
- Loop-9-style production agent: ~$_X_ over the build.
- One eval run: ~$_X_.
- Estimated cost at projected production load: ~$_X_/month.

## What this project is NOT

Be explicit about what this is and isn't. Saves future-you (or future-collaborators) from misuse.
- *e.g. "This is a single-user prototype, not a multi-tenant system."*
- *e.g. "This handles English text only; tokenization assumptions break on other languages."*

---

## A note on the postmortem itself

The postmortem is the most important deliverable in builder-first. Six weeks from now, you'll have forgotten which decisions were good and which were costly. The postmortem is a letter to that future-you.

Lessons not written down do not transfer.
