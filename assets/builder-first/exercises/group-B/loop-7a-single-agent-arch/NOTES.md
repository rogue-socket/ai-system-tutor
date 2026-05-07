# Loop 7a — Notes

*Numbers are the load-bearing content here. Architecture without numbers is theology.*

## Concept

What this loop teaches in your own words. Why "more architecture" is sometimes worse. Why a benchmark is required, not optional, before you can claim an architecture is helping.

What each pattern actually does in 1 sentence:
- **Reflexion** — answer, then critique, then re-answer.
- **Planner-executor** — split planning from execution.
- **Self-consistency** — sample N answers, vote.

## The break

**Pre-fix numbers** (Stage 1):

| Architecture | Accuracy | Avg latency | Total tokens | Total iterations |
|---|---|---|---|---|
| baseline | | | | |
| reflexion (broken) | | | | |
| planner_executor (broken) | | | | |
| self_consistency (broken) | | | | |

For each architecture, one sentence on the failure mode you observed:
- **Reflexion**: (e.g. "ran 5 iterations on already-correct answers, burning ~10x tokens")
- **Planner-executor**: (e.g. "over-decomposed trivial problems into 4 steps")
- **Self-consistency**: (e.g. "voted '4.0' over '4' as a minority winner")

## The fix

**Post-fix numbers** (Stage 5):

| Architecture | Accuracy | Avg latency | Total tokens | Cost ratio vs baseline | When worth it? |
|---|---|---|---|---|---|
| baseline | | | | 1.0x | trivial / latency-sensitive |
| reflexion | | | | | |
| planner_executor | | | | | |
| self_consistency | | | | | |

**Architecture decision rubric** (the most important paragraph in this loop):

> "I'd reach for **reflexion** when ___."
> "I'd reach for **planner-executor** when ___."
> "I'd reach for **self-consistency** when ___."
> "I'd stay with a **single agent** when ___."

Concrete criteria — task complexity, error-cost asymmetry, latency budget, model variance. Not vibes.

End with: **what surprised you?** Often it's that baseline beats reflexion on simple tasks, or that planner-executor adds latency without accuracy gain on math. Naming the surprise calibrates your future architecture choices.
