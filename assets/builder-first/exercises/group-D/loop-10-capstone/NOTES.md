# Loop 10 — Notes

*This is the final notes file in builder-first. Treat it as the curriculum-level reflection, not a per-loop one.*

## Concept (capstone-level)

What did *shipping* (versus *learning*) feel like? What changed in your approach when "demo works" wasn't good enough?

## What you brought from prior loops

For your capstone, name 3–5 specific patterns or files you lifted from prior loops:
- *e.g. "Loop 4's three-tier memory model — used short-term for chat history, long-term JSON for user preferences."*
- *e.g. "Loop 8's hybrid retrieval — RRF over BM25 + dense, basically copy-pasted."*
- *e.g. "Loop 9's retry decorator — used as-is."*
- *e.g. "Loop 7b's MULTIAGENT_TRAP checklist — talked myself out of going multi-agent. Stayed single-agent. Right call."*

This list is the proof that builder-first is *cumulative* — by Loop 10 you should be reusing, not re-deriving.

## Scope cut log

Every time the tutor (or you) cut a feature out of v1, log it:

| Date | Cut | Why | Verdict (v1+) |
|---|---|---|---|
| | | | |

The verdict column is filled in *after* you ship — was the cut right or wrong in retrospect?

## Cross-curriculum reflection

Three honest paragraphs:

1. **Which loop's lessons stuck the best?** Often: Loop 4 (state as files) or Loop 7b (multi-agent trap). Why those, in your case?

2. **Which loop's lessons did you almost forget?** What scope creep / over-engineering did you almost commit because the loop's lesson hadn't fully internalized?

3. **What would you tell yourself before Loop 1?** One paragraph. The thing that — if you'd known on day one — would have changed your trajectory through 10 loops.

## What's next for you

After Loop 10 you have the AI Engineer skill set. Three directions to consider:

- **Depth.** Foundation models internals, fine-tuning, RL. fast.ai, Karpathy lectures, the LLM360 release notes.
- **Breadth.** Multi-modal, voice, robotics, real-time. Different SDKs, different latency profiles, different failure modes.
- **Scale.** Production ML platforms — Kubeflow, Vertex AI, Modal, custom inference servers. Cost optimization at the inference layer rather than the prompt layer.

Pick one. The others can wait.
