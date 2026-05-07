# Loop 2 — Notes

*Fill these in as you go (especially the numbers). Three short paragraphs each. Your own words.*

## Concept

What this loop teaches in your own words. What "tool use" actually is at the wire, why function-calling APIs exist, what's hard about getting a stateless model to call functions reliably.

## The break

What specifically failed when you ran the broken text-parse version. Include the four-bucket numbers from Stage 1: `success`, `silent_fail`, `crash`, `wrong_answer`. Note which failure mode surprised you most.

## The fix

What changes resolved it, and *why*. Include the comparison numbers from Stage 2 (text-parse vs native function-call). Include the recovery numbers from Stage 6 (opaque vs descriptive errors). One sentence per: what Pydantic added, what hot-swapping taught you about the tool registry as state.
