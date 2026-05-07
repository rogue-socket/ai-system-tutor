# Loop 3 — Notes

*Fill in as you go. The trace-reading you do in Stage 1 is the most important content here. Three short paragraphs each.*

## Concept

What this loop teaches in your own words. What the ReAct pattern actually is, why every agent framework has some version of it, what the *trace* gives you that the final answer alone does not.

## The break

For each of the 5 sample tasks, write 1–2 lines: what the model attempted, what broke (if anything), whether the final answer was correct.

| Task | Actions | Failure mode | Final answer correct? |
|------|---------|--------------|----------------------|
| 1. 12 + 7 | | | |
| 2. capital of France | | | |
| 3. pop. of capital × 2 | | | |
| 4. Paris × Tokyo | | | |
| 5. sum of 4 cities | | | |

Note the failure mode that surprised you most.

## The fix

What changes resolved each failure mode, and *why*. Specifically:
- What MAX_STEPS prevented (and what it did NOT — graceful failure ≠ correct answer).
- Whether malformed-output recovery worked, and what coaching message turned out to work best.
- Your choice of premature-termination handling for tool-free tasks.

End this section with your **framework wishlist** paragraph: what you'd want a framework to handle for you, with specific failure modes named. (Used as the bridge into Loop 5.)
