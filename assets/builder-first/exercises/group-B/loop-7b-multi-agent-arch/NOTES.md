# Loop 7b — Notes

*The MULTIAGENT_TRAP application + one-sentence test are the load-bearing content.*

## Concept

What this loop teaches in your own words. Why "multi-agent" is more often a costume than an architecture. Why the question "is this just one agent with bad prompts?" matters before reaching for hierarchy.

## The break

**Numbers across Loops 7a + 7b** (combined comparison table):

| Architecture | Accuracy | Avg latency | Total tokens | Iterations | Loop |
|---|---|---|---|---|---|
| baseline | | | | | 7a |
| reflexion (post-fix) | | | | | 7a |
| planner_executor (post-fix) | | | | | 7a |
| self_consistency (post-fix) | | | | | 7a |
| hierarchical | | | | | 7b |
| orchestrator | | | | | 7b |
| peer | | | | | 7b |
| well_prompted (Stage 4) | | | | | 7b |

Per-architecture failure-mode analysis (apply MULTIAGENT_TRAP.md):

**hierarchical.py:**
- Failure modes exhibited:
- Justification cases that apply:

**orchestrator.py:**
- Failure modes exhibited:
- Justification cases that apply:

**peer.py:**
- Failure modes exhibited:
- Justification cases that apply:

## The fix

**The well-prompted single-agent comparison:**

You picked `<architecture>` as the strongest multi-agent and re-implemented it as `well_prompted.py`. Side-by-side:

|  | multi-agent | well-prompted single |
|---|---|---|
| Accuracy | | |
| Total tokens | | |
| Avg latency | | |

Did the multi-agent version add anything the well-prompted single didn't? *(Answer honestly.)*

**The one-sentence test (the most important paragraph in this loop):**

> "I'd use multi-agent for ___ specifically because ___, and I've ruled out single-agent-with-better-prompts because ___."

Make the blanks concrete. If you find yourself writing "complex tasks" or "production systems," you haven't ruled anything out — those phrases describe nothing.

**End with: what surprised you?**

Often: that the well-prompted single agent matched or beat the multi-agent. Or: that the orchestrator burned 8 calls per task on problems baseline solved in 1. Naming the surprise calibrates your future architecture choices.
