# Loop 7b — Cheatsheet

*Fill in as you build.*

## Commands

- `python hierarchical.py` — manager + workers
- `python orchestrator.py` — step-by-step dispatcher
- `python peer.py` — propose & critique
- `python well_prompted.py` — your single-agent rewrite (Stage 4)

## Patterns

3–5 reusable code snippets. Suggestions:

- The `worker: task` line-parsing pattern for hierarchical's manager output.
- The orchestrator's `<action>: <payload>` shape and termination check.
- The peer's `AGREE` / `DISAGREE: <reason>` critique protocol.
- The "well-prompted single agent" pattern: one prompt that includes "decompose, then solve, then sanity-check" all in one pass — replaces multi-agent for many cases.

## Gotchas

3–5 traps. Suggestions:

- The manager hallucinates worker types ("compute" instead of "math"). Tighten with one example or hard-validate.
- The orchestrator never finalizes. Cap iterations harder, or add a stronger "if you have an answer, finalize" hint.
- Peer's critic suffers false-AGREEs (same as Reflexion's false-OK).
- Different system prompts on the same model is *not* multi-agent; it's role-play. Don't pretend.
- Cost compounds — 3 agents × 5 iterations × 10 tasks = 150 calls for one benchmark run.

## Numbers

Suggestions:

- Cost ratio multi-agent-vs-baseline: ~_N_x.
- Cost ratio well-prompted-vs-multi-agent: ~_N_x.
- Tasks where well-prompted matched multi-agent: _N_/10.
- Tasks where multi-agent beat well-prompted: _N_/10 (and *why*).
- Free-tier RPM hits: yes/no.
