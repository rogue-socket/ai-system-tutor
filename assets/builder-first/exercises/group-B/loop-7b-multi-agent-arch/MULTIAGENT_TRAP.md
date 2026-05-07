# The Multi-Agent Trap

Most "multi-agent" systems in 2026 are one agent with bad prompts wearing a costume. This file is the checklist for telling the difference. **Apply it to every multi-agent solution before defending the architecture.**

The reason this doc exists: a learner who finishes Loop 7b without internalizing this content will reach for hierarchy by default for the rest of their career, will burn 3-5x cost on production systems that didn't need it, and will struggle to debug the "manager is hallucinating sub-tasks" failures that follow. Multi-agent is sometimes the right answer. Often it isn't.

---

## The five failure modes

### 1. Information bottleneck at the manager

In hierarchical, the manager has to summarize what each worker did before passing to the next worker. The summary loses information. The next worker is blind to context the original input had.

A single agent with the full conversation in context doesn't have this problem.

> **Test:** if your manager is just relaying messages between workers, or summarizing them so the next worker doesn't see the full picture, the architecture is buying you nothing — and probably costing you correctness.

### 2. Redundant context

Each agent in a multi-agent system needs context. Setup costs (system prompt, role definition, task framing) duplicate across N agents. Tokens 3x or 5x without proportional benefit.

> **Test:** count the tokens. If your N-agent system uses Nx the tokens of a single-agent system and accuracy hasn't improved by a meaningful margin, the cost-benefit is wrong.

### 3. Cost explosion at scale

A single LLM call is cheap. Multi-agent systems with 5 calls per task aren't — at scale, your cloud bill scales with the number of calls. If each task does 5 calls instead of 1, your bill is 5x. Nothing about your *value* is 5x.

> **Test:** project the cost at scale. Is the accuracy improvement (if any) worth 5x infrastructure?

### 4. Coordination overhead

Multi-agent systems need a coordinator (or implicit handoff convention). The coordinator is itself an LLM call (or many). It's another point of failure: the coordinator can misdispatch, miss tasks, or hallucinate sub-tasks that don't exist. Debugging a coordinator failure is harder than debugging a single-agent answer.

> **Test:** have you debugged a coordinator failure? Was it harder than debugging a single-agent answer? If yes, that's a tax. If you haven't yet — you will.

### 5. Wearing a costume

Most often: a single LLM with three different system prompts called sequentially is *not* multi-agent. It's one agent in three roles. Different roles share weights, training data, biases, and failure modes. A single, well-prompted call to the same model can usually do the same thing more cheaply.

> **Test:** if your "agents" all use the same model, the same SDK, and the same provider, you don't have multi-agent. You have one agent doing role-play. That can be useful — it's also cheaper to do explicitly with a single, well-prompted call.

---

## When multi-agent IS justified

Multi-agent earns its keep in three specific cases. Be honest about which one applies:

### A. Different models for different sub-tasks

Math worker uses a math-tuned or symbolic-computation model; reasoning worker uses a reasoning-tuned model; vision worker uses a multimodal model. The "different agents" are actually *different models*, not the same model with different prompts. Capability differences justify the architecture.

### B. Independent execution at scale (parallelism, not coordination)

Workers run in parallel and don't coordinate (e.g. embarrassingly-parallel processing of N documents). The "multi-agent" is just N copies of one agent. Parallelism is real; coordination overhead is zero. Often spelled "horizontal scaling" rather than "multi-agent."

### C. Different trust domains (process isolation matters)

Worker A runs untrusted user-supplied code; worker B is the trusted reviewer. Process-level isolation is required for security; that's a real architectural reason. **Not** "the manager is a different role" — actual sandboxing across processes, machines, or trust boundaries.

If your case isn't one of these three, write *exactly* what your multi-agent system does that a single agent with better prompts could not.

---

## The one-sentence test

> "I'd use multi-agent for ___ specifically because ___, and I've ruled out single-agent-with-better-prompts because ___."

If you can't fill in the blanks, you don't need multi-agent. Yet.

---

## What to do during Loop 7b

After you've built and benchmarked all three multi-agent architectures (hierarchical, orchestrator, peer):

1. **Run the checklist** above against each of your three architectures. For each one, identify which of the 5 failure modes it exhibits. Most will exhibit at least 2.
2. **Pick the one that performed best** on the benchmark. Re-implement it as a single-agent with deliberately-tuned prompts. Run the same benchmark. Compare.
3. **Honestly answer:** did the multi-agent version add anything the well-prompted single-agent didn't? If yes, name it precisely. If no, that's the lesson.

This is not theory. The biggest skill jump in this entire curriculum is from "I built a multi-agent system" to "I knew when not to."
