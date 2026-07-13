# Anti-patterns with paired examples

Use this file when coaching, reviewing an agent design, or selecting a lesson. Load only the
relevant item; do not recite the whole list to a learner.

## 1. Framework-first without a loop model

**Bad:** Start with an orchestration framework before the learner can describe model input,
tool call, observation, and stop condition.

**Better:** Build or trace one small loop first, then use the framework to name the pieces it
already contains.

## 2. Treating a prompt as a safety boundary

**Bad:** Claim that a system prompt prevents prompt injection or destructive tool calls.

**Better:** Separate instruction following from authority: constrain tools, validate inputs,
require approval for side effects, and test adversarial retrieval content.

## 3. Measuring a demo instead of a behavior

**Bad:** Call an agent reliable because one happy-path conversation worked.

**Better:** Define a small evaluation set, capture traces, and test failure, recovery, cost,
and latency behavior before claiming reliability.

## 4. Multi-agent by default

**Bad:** Add more agents when one agent has unclear state, weak tools, or no evaluation.

**Better:** Make the single-agent loop observable first; introduce delegation only for a
measurable decomposition or isolation benefit.

## 5. Teaching abstractions without an artifact

**Bad:** Explain RAG, planning, or memory only in prose.

**Better:** Pair the concept with a trace, failed retrieval, small implementation, or incident
that the learner can inspect.
