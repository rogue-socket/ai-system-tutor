# Loop 9 — Notes

*Production agents are graded on numbers. Fill them in.*

## Concept

What this loop teaches in your own words. Why "the agent works in dev" is a long way from "the agent won't page someone at 3am." The dozen production concerns and how they relate to each other.

If a coworker asked "we have a working LangGraph agent — what's left to do before launch?", the answer is some subset of this loop's stages. Be ready to give that answer.

## The break — broken-state baseline

Numbers from the first `load_test.py` run, before any hardening:

| Metric | Broken state |
|---|---|
| Success rate | _N_/30 |
| p50 latency | _N_ ms |
| p95 latency | _N_ ms |
| p99 latency | _N_ ms |
| Total time | _N_ s (req/s = _N_) |
| Sample failure modes | (e.g. 429s, timeouts, hangs) |

## The fix — by stage

For each stage, one or two metrics + one sentence on what surprised you.

| # | Stage | Key metric | Result | Note |
|---|---|---|---|---|
| 1 | Caching | hit rate | | |
| 2 | Retries | success rate | | |
| 3 | Cost tracking | $/load_test, projected $/month at 1000 RPS | | |
| 4 | Eval w/ judge bias controls | pass rate, uncertainty count | | |
| 5 | Injection guardrails | %blocked of injection attempts | | |
| 6 | Observability | counters populated, trace IDs in logs | yes/no | |
| 7 | Streaming | TTFT, total latency | | |
| 8 | Async | parallel fan-out latency vs sequential | | |
| 9 | Secrets | rotation procedure documented | yes/no | |
| 10 | Deploy | provider, cold start | | |
| 11 | Monitoring | alert thresholds defined | yes/no | |
| 12 | Rate limit + graceful degradation | bad-key behavior | | |

## Model selection trade-off table

| Model | Cost / 1M tokens | p99 latency | Tool-call reliability | Long context | When to reach for it | When overkill |
|---|---|---|---|---|---|---|
| `gemini-2.0-flash-lite` | | | | | very cost-sensitive | reasoning |
| `gemini-2.0-flash` | | | | | default | n/a |
| `gemini-2.5-pro` | | | | | reasoning, long context | trivial Q&A |
| `claude-sonnet-4` | | | | | tool use, long structured output | fast classification |
| GPT-class | | | | | | |
| Open-weight (llama-3, qwen) | | | | | privacy, on-prem | no GPUs |

Decision criteria: cost per task, p99 latency, tool-call reliability, structured-output reliability, context length needed, vendor lock-in tolerance.

## What surprised you

Often: that the cost projection at scale is way higher than you'd guessed. Or that streaming changed UX dramatically without changing total latency at all. Or that LLM-as-judge agreed with itself less than you thought before bias controls. Naming the surprise is what makes the lesson stick.

## What you still wouldn't ship

Be honest. Production-readiness is a spectrum, not a binary. After this loop you have most of the moving parts — you don't have all the moving parts. What's still missing for a real customer-facing system? (e.g. multi-region, blue-green deploy, on-call rotation, SLO contracts, content moderation, SOC 2 controls.) One paragraph.
