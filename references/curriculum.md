# Curriculum

**Source.** This curriculum is frozen from the [AI System Engineer syllabus](https://rogue-socket.github.io/AI-System-Engineer/) (`Documents/learn_agents/AI-System-Engineer/`). Re-sync on demand when the upstream syllabus is updated.

**9 layers, ~50 sections, ~370 topics.** Layers stack from intuition (L0) → foundations (L1) → cognition (L2) → state (L3) → action (L4) → coordination (L5) → runtime (L6) → constraints (L7) → measurement (L8).

**Prerequisites are at the section level.** Topics within a section are roughly independent; sections are ordered.

**Anchor sources** (referenced as `[LW]`, `[ANT]`, `[OAI]`, `[HF]`, `[OWASP]` below):
- **[LW]** Lilian Weng — "LLM Powered Autonomous Agents", "Adversarial Attacks on LLMs", "External Memory" (lilianweng.github.io)
- **[ANT]** Anthropic engineering blog — "Building effective agents", "Prompt caching", MCP docs, "Constitutional AI"
- **[OAI]** OpenAI cookbook — tool use, structured output, evals, function calling
- **[HF]** Hugging Face Agents course — open-weight stack, smolagents, tool design
- **[OWASP]** OWASP Agentic AI Top 10 (and OWASP LLM Top 10 for prompt-injection topics)

Where a topic is best taught from a different source (a specific paper, a vLLM doc, a postmortem), the lesson cites that source inline and notes "outside the anchor list."

---

## Ordered course path

The default progression. Skill picks up here unless the diagnostic flags a specific weakness elsewhere.

```
L0  Mental Models                        (intuition baseline)
  └─ Section 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9   (prerequisites enforce this)

L1  Foundation Models
  └─ Internals → Selection → Inference → Embeddings → Structured output → Prompting → Reasoning models

L2  Reasoning & Intelligence
  └─ Agent loop → Planning → Reasoning patterns → Reflection → Metacognition → Architectures

L3  Memory & Knowledge
  └─ Memory architecture → Retrieval fundamentals → Chunking → RAG architectures → Knowledge stores

L4  Agency & Tool Use
  └─ Tool design → Information tools → Action tools → Meta tooling → Protocols → Interaction patterns → Identity

L5  Multi-Agent Systems
  └─ When multi-agent is wrong → Orchestration patterns → Coordination → Frameworks → Failure modes

L6  Infrastructure & Deployment
  └─ Serving → Hardening → Caching → Data infra → Deployment → Cost → API design → Fine-tuning

L7  Safety, Security & Governance
  └─ Threat landscape → Defenses → Governance → Privacy

L8  Evaluation, Observability & Applications
  └─ Eval frameworks → Observability → Debugging → CI/CD → Performance → Application patterns
```

Common detours:
- **Goal: ship a RAG agent in production.** L0 (skim) → L3 (deep) → L4 (tools) → L6 (serving + hardening) → L8 (eval).
- **Goal: build a coding agent.** L0 (skim) → L2 (loops + planning) → L4 (tool design) → L7 (sandboxing) → L8 (debugging).
- **Goal: pass an AI systems interview.** L0 → L1 → L2 → L3 → L4 → L8 (heavy on eval and trade-offs).

---

## L0 — Mental Models

**Kind:** Orientation. **Scope:** what models, agents, and AI systems actually are. **Anchor:** [LW] for the agent-loop framing; the syllabus's own L0 prose is the best single source.

### S1. What a model is *(no prereq)*
- A model is a file of numbers, not a program with rules
- What a neural network looks like — layers of simple math that compose into complex behavior
- What a parameter is — one adjustable number; billions of them encode everything the model "knows"
- What the transformer is — every token can attend to every other token
- What attention does — model deciding which parts of input matter for predicting the next piece
- What "large" means — parameter count, data scale, compute spent
- What a foundation model is — one pretrained model adapted to many downstream tasks
- Open-weight vs closed — file vs API endpoint
- Why a model is frozen after training — weights don't change at inference
- Model families and versions — why GPT-4, GPT-4o, GPT-4 Turbo are different

### S2. How models learn *(prereq: S1)*
- What training is — billions of examples, adjust weights to reduce prediction error
- What pretraining does — language patterns from the internet at massive scale
- The training objective in one sentence — predict the next token
- What loss means — number that goes down when prediction improves
- Why dataset matters more than architecture — garbage in, garbage out, at scale
- What RLHF does — human preference data steers from "predict text" to "be helpful"
- What instruction tuning is — teaching the model to follow directions
- What fine-tuning is — additional training on specific data
- What distillation is — small model mimics a large one
- Scaling laws — more data, parameters, compute → predictably better models
- Emergent capabilities — abilities that appear at scale without being trained
- Why training and inference are completely different phases

### S3. How models generate *(prereq: S1)*
- Generation is next-token prediction — one token at a time
- What autoregressive means
- The output is a probability distribution over every possible next token
- What temperature does — spreads or peaks the distribution
- What top-p and top-k do — different cutoffs for pruning unlikely tokens
- What greedy decoding is — always pick most probable, sounds robotic
- Why generation is inherently slow — sequential one-at-a-time bottleneck
- Time-to-first-token — pause before output streams
- Streaming — sending tokens as generated
- Stop sequences — how the model knows it's done
- Batching for inference — multiple requests share GPU compute
- Why same prompt → different outputs — sampling is stochastic

### S4. Tokens, context, the input surface *(prereq: S3)*
- What a token is — chunk of text, ~3/4 of an English word
- Why "count the r's in strawberry" fails — model never sees characters, only chunks
- What a tokenizer does — text ↔ integer IDs; differs by model
- Why code, JSON, non-English are expensive — tokenizers optimize for English prose
- Context window — fixed-size buffer of tokens per call
- Why context is not memory — rebuilt from scratch every request
- What competes for context space — system prompt, history, retrieved docs, user msg, model reply
- "Lost in the middle" — models attend more to start and end
- Why longer context isn't always better — noise, cost, latency
- Token economics — input vs output tokens priced differently

### S5. Prompting as steering *(prereq: S4)*
- What a prompt actually does — selects which patterns to activate and extend
- Why prompting works — model is a pattern completer
- System prompt — persistent framing
- Few-shot examples — demonstrate, don't describe
- Chain-of-thought — reasoning step-by-step before answer
- Why more output tokens before answer often help — generation is computation
- Why small wording changes cause large output shifts
- Structured output — constraining to JSON/XML/etc.
- Prompt injection — adversarial input hijacks instructions
- Why "just ask clearly" is necessary but not sufficient

### S6. Reasoning, planning, model limitations *(prereq: S5)*
- What "reasoning" means for a model — generating tokens that look like reasoning
- What a reasoning model is — trained to produce extended thinking before answers
- Thinking tokens — intermediate steps, may or may not be shown
- What planning looks like — model decomposes problems but can't guarantee executability
- What self-correction looks like
- Why models hallucinate — pattern completion ≠ truth verification
- What models are reliably bad at — counting, spatial, precise arithmetic, negation
- Generating vs knowing
- Why confidence and correctness are unrelated

### S7. Agents, tools, autonomy *(prereq: S6)*
- What an agent is — calls a model in a loop: observe, decide, act, repeat
- What the agent loop looks like
- What separates an agent from a single call — persistence, real-world actions, feedback
- What a tool is — function the agent can invoke
- How tool calling works — structured output → execute → feed result back
- What a multi-agent system is
- Autonomy levels — from approval-gated to fully end-to-end
- Human-in-the-loop — checkpoint for review
- Guardrails — programmatic constraints
- Why agents fail — compounding errors, hallucinated actions, infinite loops, lost goal
- What an agent framework is

### S8. Memory, retrieval, state *(prereq: S7)*
- Why models have no memory — every API call is independent
- What conversation history really is — resending prior messages
- Short-term memory for agents — context window
- Long-term memory for agents — external storage
- What an embedding is — fixed-size vector capturing meaning
- Vector similarity — search by meaning, not keywords
- What a vector database does
- What RAG is — retrieve, inject, generate
- Why RAG exists — models can't know everything; context isn't infinite
- Knowledge graphs — facts as structured relationships

### S9. The system around the model *(prereq: S7, S8)*
- What an AI system is — model + code + data + infra; model is one component
- Why most engineering effort is outside the model
- What a pipeline is — chained model calls with code in between
- What orchestration means
- Multi-model routing — small/fast for easy, expensive for hard
- What evaluation means
- What observability means
- The latency-cost-quality triangle
- What deployment means here — laptop → reliable at scale
- Why versioning everything matters — model, prompt, retrieval, eval all change independently

---

## L1 — Foundation Models

**Kind:** Foundations. **Scope:** internals, selection, inference, prompts for production. **Anchors:** [LW], [HF], vLLM docs, Anthropic prompt-caching post.

This is where vocabulary turns into mechanism. By the end of L1 you should be able to answer: *what costs what, and why?* — for tokens, latency, and GPU memory.

### S1. Model internals for system design *(no prereq)*
- KV cache — past keys/values are stored per layer per token so attention reuses them; each new token costs O(seq_len), not O(seq_len²)
- KV cache memory — linear in context, multiplicative in layers and heads; at 70B / 8k context this is ~16GB *per concurrent request* before you've batched anything
- Context window economics — every token in the window participates in compute on every decode step; "fits in context" is not "free"
- Tokenizer behavior — same text tokenizes to different ID counts across models; budget by *your model's tokens*, not characters
- Why code, JSON, and non-English are expensive — tokenizers were trained on English prose; everything else fragments into more tokens
- GQA vs MHA vs MLA — fewer KV heads → smaller cache → more concurrent requests, with a (usually small) quality cost; modern serving stacks default to GQA
- Mixture of Experts (MoE) — only N of M experts active per token; serving needs expert-aware batching or capacity sits idle while one expert is overloaded
- State-space models (Mamba, RWKV) — trade attention for recurrence; long context is cheap to *generate* but recall over the past tends to be fuzzier than transformers

### S2. Model selection *(prereq: S1)*
- Reasoning ↔ speed ↔ cost — three-way trade-off; pick the two that matter for your task and accept the third gets worse
- Open-weight vs API — open-weight wins on cost-at-scale, data residency, and customization; API wins on time-to-first-call and frontier quality
- When 7B beats 70B — for tightly-scoped tasks (classification, structured extraction, narrow-domain Q&A), a fine-tuned 7B often beats a generalist 70B at ~1/10 the cost
- Model cards — say what worked on benchmarks; rarely tell you the failure modes you'll hit in production
- Benchmark gaming — leaderboards reflect what's measured, not what you need; an MMLU score won't tell you if the model can call your tools
- Distillation — teacher model labels data, student fine-tunes on labels; useful when you have a slow/expensive model that works and need a fast one with the same behavior

### S3. Inference optimization *(prereq: S1)*
- Speculative decoding — small "draft" model proposes N tokens, big "verifier" checks them in one forward pass; ~2-3x speedup when draft accepts often
- Quantization — pack weights into fewer bits (FP16 → INT8/INT4); GPTQ for post-training, AWQ for activation-aware (better quality), GGUF for llama.cpp's portable container
- Continuous batching (vLLM) — instead of waiting for the slowest request in a static batch, dynamically pack new requests into the GPU as old ones finish; the single biggest production-serving win of the last few years
- PagedAttention — KV cache is split into pages so different requests can share memory like an OS pages RAM; eliminates fragmentation that wasted ~60-80% of cache memory under naïve batching
- KV cache eviction / compression — when memory fills, drop or compress oldest/least-attended tokens; trades quality for throughput, tunable per workload
- Prompt caching and prefix sharing — providers cache prefix KV state so identical system prompts across requests reuse compute; Anthropic charges ~10% of input rate on cache hits
- FlashAttention — recompute attention in tiled blocks that fit in SRAM; faster *and* less memory than vanilla attention, with no quality cost
- Mixed precision (FP8, BF16) — store/compute at lower precision where it doesn't hurt; FP8 is the current frontier on H100/H200, BF16 is the safe default everywhere else
- Tensor parallelism — split a single layer across GPUs (heads or hidden dim); needed when a model is too big for one GPU, costs you GPU↔GPU communication every layer
- Pipeline parallelism — split *layers* across GPUs; cheaper communication than tensor parallelism but introduces bubbles when batch is small
- Chunked prefill — process long prompts in chunks instead of one giant forward pass; smooths latency for mixed prefill+decode workloads
- Disaggregated serving — separate GPUs for prefill (compute-bound) and decode (memory-bound) so each fleet runs at its own bottleneck; maximizes utilization

### S4. Structured output *(prereq: S2)*
- JSON mode — provider-side bias toward valid JSON; not a guarantee, just a strong prior, and it can still produce truncated or schema-violating JSON
- Constrained decoding — at each step, mask logits for tokens that would violate the schema; produces guaranteed-valid output but can hurt quality if the schema is restrictive (the model "wanted" to say something else)
- Grammar-guided generation (GBNF, Outlines, llguidance) — write the schema as a grammar; the runtime enforces it during decode rather than re-prompting on failure
- Schema validation at the boundary — even with constrained decoding, validate again on the receiving side; the schema in *your code* is the source of truth, not the model's
- Failure modes — refusals, partial JSON, hallucinated fields, recursive nesting that exceeds depth, escaped quotes that confuse the parser; have a recovery path for each
- Tool-call output design — keep tool args flat (no deep nesting), use enums over free-form strings, put required fields first; deep nested schemas degrade tool-calling accuracy fast

### S5. Embedding and retrieval models *(prereq: S1)*
- Embedding selection — three axes that matter: dimensions (cost ↔ quality), domain match (general vs domain-specific), language coverage; pick by *your eval set*, not the MTEB leaderboard
- Matryoshka embeddings — single model trained to be valid at multiple dimensions (256, 512, 1024); lets you store full-dim and query at lower dim for free quality/cost tuning at retrieval time
- Bi-encoder vs cross-encoder — bi-encoder embeds query and doc independently (fast, ~ms, scalable); cross-encoder reads them together (slow, ~10x cost, better quality); use bi-encoder for retrieval, cross-encoder for reranking the top 50
- ColBERT / late interaction — embed each token separately, score by max-similarity across token pairs; better than bi-encoder, cheaper than cross-encoder, with much larger storage cost
- Embedding fine-tuning — small contrastive fine-tune on (query, relevant doc, irrelevant doc) triples; biggest wins are on domain jargon, acronyms, and rephrasing patterns
- MTEB pitfalls — useful for shortlisting embedding models, useless as a final metric; benchmark contamination is widespread and your data ≠ benchmark data
- Multimodal embeddings (CLIP, SigLIP) — joint image-text space; lets you retrieve images by text query and vice versa, with a quality floor below text-only models on either side alone

### S6. Prompt engineering for production *(prereq: S4)*
- Prompt versioning and registries — every prompt is a deployable artifact; tag it, store it, and tie outputs back to prompt version in logs
- Prompt regression testing — golden set of (input, expected) pairs; run on every prompt change before merge, just like a code test
- A/B testing in production — split traffic between prompt variants and measure on actual outcomes (clicks, completions, user-rated quality); cheaper and more honest than offline LLM-as-judge for nuanced quality
- Prompt-model co-versioning — a prompt tuned for GPT-4 frequently regresses on GPT-4o; pin prompt version *to* model version, and re-bench when either changes
- Prompt compression — shorter prompts = lower cost and latency; LLMLingua and similar can compress 5-20x with small quality loss for retrieval-heavy contexts
- System vs user prompt boundary — system for stable framing (role, format, rules), user for the request; mixing them breaks prompt caching and confuses the model
- Meta-prompting — using an LLM to write or improve prompts; works for breadth and ablation, fails on edge cases that need actual domain knowledge
- Prompt rollback and incident response — when a new prompt regresses in prod, rollback is the same as rolling back code; have the runbook (revert PR, redeploy, alert) ready before you need it

### S7. Reasoning models *(prereq: S2, S3)*
- When reasoning models are worth the cost — multi-step problems where the answer requires search or planning; *not* "summarize this" or "extract these fields"
- Thinking budget — adaptive compute: spend more thinking tokens on hard problems, fewer on easy; some models expose this as a parameter, others infer it
- Test-time compute scaling — past a point, more thinking tokens = better answers; the curve flattens, and "more" has a hard cost ceiling
- Chain-of-thought economics — thinking tokens are billed at the *output* rate (typically ~5x input rate); a 10k-thinking-token answer can cost more than the entire input context did to send
- Hybrid thinking modes — Claude Sonnet 4 and similar let you toggle thinking on/off per request; default off, opt in for hard cases, never on by default in a hot path
- Process reward models — score each reasoning step; lets you stop early when a step is wrong instead of running thinking-tokens to completion
- Outcome reward models — score only the final answer; cheaper to train, but blind to *how* the answer was reached, which makes them less useful for debugging

---

## L2 — Reasoning & Intelligence

**Kind:** Cognition. **Scope:** agent loops, planning, reasoning, self-correction. **Anchors:** [LW] "LLM Powered Autonomous Agents" is foundational here. [ANT] "Building effective agents" is the modern practical companion.

This is where "the model" becomes "the agent." Once you put a model in a loop, you have a system that fails in new ways. By the end of L2 you should be able to name three ways your agent will degrade past iteration 5, three ways it will degrade past iteration 20, and have a calibrated opinion about which planning patterns are worth their overhead.

### S1. The agent loop *(no prereq)*
- The loop itself — perceive (read context), reason (LLM call), act (tool call or final answer); everything else in agent design is decoration on these three steps
- Bounded vs unbounded — bounded agents have a hard step cap and a budget; unbounded agents are demos that haven't crashed yet
- The ReAct paper (Yao 2022) is the canonical reference — read it once, internalize the trace format (Thought / Action / Observation), then never read it again
- Deterministic replay — store {prompt, model, params, tool calls, results} per step; replay-from-trace is how you debug without burning tokens
- Resume-from-failure — when step N fails, the next run picks up at step N, not step 1; checkpoint after every successful tool call
- State persistence — for single-node agents, SQLite usually beats Redis; durable, transactional, no extra process, file is the artifact
- Event sourcing for agent traces — every action is an append-only event, current state is a fold over events; lets you time-travel and audit cleanly
- Stop conditions and escalation — explicit "I'm done" output is one stop; budget exhaustion, repeated identical tool calls, and "stuck detector" patterns are the others; without them you have AutoGPT
- The ReAct degradation curve — quality stays high for ~5-7 iterations, drops sharply past ~10; the failure modes are observation overflow, action repetition, goal drift, and context-window saturation
- Why most agents fail at iteration 11 — by then the system prompt is a small fraction of context, tool results dominate, and the model has stopped attending to the original task
- The Devin demo problem — long-running autonomous agents look great in cherry-picked demos and break on edge cases the demo skipped; expect the demo-to-prod gap to be larger here than anywhere else

### S2. Planning and decomposition *(prereq: S1)*
- Task decomposition — split a goal into subgoals before executing; prevents the agent from "working" while wandering
- Plan-and-execute vs reactive — plan-and-execute is brittle to surprises but cheaper; reactive is robust but burns more tokens; LangGraph's pattern is hybrid (plan, then react within a step)
- Hierarchical planning — high-level plan owns strategy, lower-level plans own steps; replan only the level that broke, not the whole tree
- Replanning — when an observation invalidates the plan, regenerate from current state, not from scratch; "what did I learn since the original plan" beats "start over"
- Budget-aware planning — give the planner a token/cost/time budget and have it allocate explicitly; "fit this in 5k tokens" produces different plans than "do whatever"
- Plan repair after partial failure — successful subtasks stay done, replan only the unfinished tail; the alternative is silently re-doing expensive work
- Goal prioritization — when multiple subgoals compete for budget, the planner needs an explicit ranking; without it you get strict left-to-right execution that drops the most important goal last
- Why most "planners" are just prompts — calling something a planner doesn't make it one; a real planner has a goal model, a state model, and a notion of progress

### S3. Reasoning patterns *(prereq: S1)*
- Chain-of-Thought (CoT) — generate reasoning tokens before the answer; helps on multi-step math and logic, *hurts* on trivia and simple fact retrieval
- When CoT hurts — known result: CoT degrades performance on tasks where humans don't deliberate (face-recognition analogs, simple lookups); not all problems benefit from "think first"
- Tree-of-Thought (ToT) — branch on candidate next-steps, evaluate each, prune; works when steps are scorable and branching factor is small (<5)
- Graph-of-Thought — generalization of ToT with merges and revisits; in practice the graph is a marketing diagram, the runtime is "ToT with a different prompt"
- Self-consistency via majority voting — sample N times at high temperature, take the modal answer; budget multiplies by N for a quality bump that flattens around N=5
- Tool-assisted reasoning — offload deterministic steps to tools (calculator, code interpreter, lookup); the model's job is reasoning, not arithmetic
- Verifier-guided reasoning — a separate model scores each reasoning step; advantage over CoT when wrong steps compound; still needs a verifier you trust
- Test-time compute vs fine-tuning — at some quality threshold, more inference time beats more training; the crossover depends on how often the task runs (run-once = inference, run-millions = fine-tune)

### S4. Reflection and self-correction *(prereq: S2, S3)*
- Reflection loops — agent generates, critiques its own output, revises; cost is roughly N×, quality bump tapers fast past 2 iterations
- Self-critique that actually works — needs a *separate* critique prompt, not "are you sure?"; the model agreeing with itself is the easy case
- Trajectory critique — review the whole sequence of actions, not just the last output; catches goal-drift that per-step critique misses
- Iterative refinement vs single-shot — iterative wins on creative or open-ended tasks; single-shot wins when there's a verifiable correct answer (the agent often can't tell when it's right)
- Post-action review patterns — log the (state, action, result) tuple, score it, write a "lesson" to memory; the agent reading its own history changes future behavior
- The Reflexion trick — convert failures into natural-language lessons, prepend to next attempt's context; non-trivial gains, but only on tasks where the agent can both fail *and* notice
- Why naïve "just check your work" rarely helps — the model doesn't know what it doesn't know; without an external verifier or tool result, self-checks tend to ratify the original answer with extra tokens

### S5. Metacognition *(prereq: S4)*
- Confidence calibration — does the model's stated confidence match its empirical accuracy? Usually no; LLMs are over-confident on incorrect answers and slightly under on correct ones
- Selective abstention — letting the agent say "I don't know" or "I need more info"; requires explicit prompting and a UX path that *handles* abstention (most don't)
- Out-of-distribution detection — when the user's request is unlike anything in training, the model still answers confidently; OOD detection in agent stacks is mostly vibes-based heuristics
- Knowing-when-to-stop — task completion detection is harder than task execution; many agents loop forever because nobody told them what "done" looks like
- Confidence-gated actions — only execute side-effecting actions when confidence > threshold; gate read-only actions less strictly; gate destructive actions through a human
- Resource-bounded reasoning — track tokens/cost/time per task; degrade gracefully when budget runs low (cheaper model, shorter prompt, abstain)
- The dirty secret of metacognition — current models barely have it; what we call "metacognition" in agent stacks is mostly external scaffolding (verifiers, budgets, abstention logic) wearing a fancy name

### S6. Agent architectures *(prereq: S1, S2, S3)*
- ReAct — the default; reason→act→observe in a single context; degrades past ~10 iterations as covered in S1
- Plan-and-execute — separate planner produces an explicit plan, executor runs it; handles long tasks better, brittle to mid-execution surprises
- Tool-using agents — broad category; everything from "one tool, no loop" to "MCP server with 200 tools and a router"
- Bounded vs autonomous — the spectrum runs from "approval-gated step-by-step" to "give it a goal and walk away"; the autonomous end is mostly demo-grade as of now
- Compound AI systems (Berkeley's term) — the real architecture in production is multiple specialized models + retrieval + tools wired together, not a single mega-model
- Cognitive architectures (ACT-R, SOAR) — symbolic AI's planning frameworks from the 80s; the lessons (production rules, working memory, conflict resolution) keep getting rediscovered in LLM-agent design
- LLM-as-judge in the loop — using a model to evaluate another model's output as a control signal; the well-known biases (position, verbosity, self-preference) bite hard, see L8
- Why "AI agent" is a vague term — anything that calls a model in a loop with tools is an agent; the interesting question is the autonomy level and which failures it can recover from

---

## L3 — Memory & Knowledge

**Kind:** State. **Scope:** memory, retrieval, chunking, RAG, knowledge stores. **Anchors:** [LW] external memory post, MemGPT/Letta papers, Anthropic contextual retrieval post.

A model is amnesiac. Every API call starts from zero, and the only way the agent "remembers" anything is by you stuffing it back into the next prompt. Memory and retrieval are the architecture of *what gets stuffed back in*. Most production AI systems live or die at this layer.

### S1. Memory architecture *(no prereq)*
- Working memory (in-context) — what fits in the current prompt; cheap, immediate, vanishes the instant the call returns
- Episodic memory — event log: "on 2026-05-06 the user asked X, the agent did Y, result was Z"; timestamped, append-only, queryable by recency
- Semantic memory — facts and relationships extracted from interactions, deduplicated; "user prefers terse responses", "the staging DB is at host X"
- Procedural memory — learned action patterns; "when user asks for a refund, steps are A, B, C"; rare in practice because nobody knows how to update it cleanly
- Memory promotion rules — when does a working-memory observation become an episodic event? When does an episodic event become a semantic fact? Promotion logic is most agents' weakest link
- Memory compression / summarization — long conversations get summarized into shorter context; lossy by definition; the right summary depends on what the agent needs *next*, which it doesn't yet know
- Memory pruning and forgetting policies — without forgetting, episodic memory grows unbounded and retrieval degrades; LRU is the floor, importance-weighted decay is better
- Memory versioning and rollback — when you change your memory schema, old memories migrate or get discarded; treat memory like a database, not a log file
- Context window management — even with infinite external memory, the prompt is finite; budget allocation between system prompt, retrieved context, conversation history, and the actual question is the daily problem
- MemGPT / Letta — virtual context: agent has tools to page memory in/out of the prompt explicitly; lets you simulate a larger context window at the cost of latency per page
- The "memory" in commercial products — ChatGPT's "Memory" is a paragraph of facts in the system prompt plus retrieval over chat history; not magic, just prompting; Claude Projects is the same shape

### S2. Retrieval fundamentals *(prereq: S1)*
- Vector search (ANN, HNSW) — approximate nearest neighbor; trades exactness for speed; HNSW is the default index for in-memory and disk-backed stores both
- Index tuning — HNSW knobs (M, efConstruction, efSearch) trade index build time, memory, and recall; defaults are fine until they aren't
- BM25 keyword search — pre-LLM ranking algorithm from the 90s; still beats dense for queries with rare terms, exact codes, IDs, and acronyms
- Hybrid search (BM25 + dense) — beats either alone when your corpus has both natural language *and* identifiers (product SKUs, error codes, function names); not worth the complexity for clean prose
- Query rewriting — turn vague user questions into search-friendly queries; LLM-rewritten queries can hurt retrieval — A/B before turning it on
- HyDE (Hypothetical Document Embeddings) — generate a hypothetical answer, embed it, retrieve docs near the hypothetical; counterintuitively works better than embedding the question directly for some domains
- Reciprocal Rank Fusion (RRF) — combine ranked lists from multiple retrievers without normalizing scores; the boring algorithm that wins
- Cross-encoder reranking — re-score top-K with a slow, accurate model; latency cost is roughly proportional to K, quality bump is the biggest single retrieval improvement after fixing chunking
- ColBERT / late interaction — token-level matching with max-similarity aggregation; better than bi-encoder retrieval, worse storage profile (every token gets a vector)
- Contextual retrieval (Anthropic) — prepend a one-line document context to each chunk before embedding; Anthropic claims ~50% reduction in retrieval failures; cheap and effective
- Learned sparse retrieval (SPLADE) — learn sparse term weights end-to-end; better than BM25, lighter than dense, with sparse-index tooling
- Why most "RAG isn't working" complaints are retrieval problems — the generation is fine; the retrieved docs don't contain the answer; fix retrieval *before* you tune prompts

### S3. Chunking and indexing *(prereq: S2)*
- The 512/50 default — split into 512-token chunks with 50-token overlap; the convention from early LangChain demos; works for blog posts, fails on contracts and code
- Semantic chunking — split at semantic boundaries (paragraph, section, sentence-cluster) instead of fixed sizes; better preservation of unit-of-meaning
- Fixed-size chunking — predictable cost and latency; the right call for high-volume, simple content
- Parent-child retrieval — match on small chunks (precise), serve the parent doc or section to the model (rich context); the under-used pattern that fixes most "context-too-small" complaints
- Late chunking — embed the whole doc once, *then* chunk after pooling; preserves long-range context that per-chunk embedding loses
- Metadata enrichment — title, section, author, date, source URL; lets the agent filter ("docs from this year only") and the model cite sources properly
- Multi-index strategies — separate indexes per content type (FAQs, code, prose), retrieve from each, fuse; each index gets its own chunking and embedding model
- Indexing pipeline automation — re-indexing on document update; if your pipeline is "rerun the script when something changes", you'll have stale data within a week
- Why chunking is mostly a corpus problem — there's no universal best chunker; the right strategy depends on what your docs look like and what your queries look like, which means you have to look

### S4. RAG architectures *(prereq: S2, S3)*
- Single-hop RAG — retrieve once, generate; the default, the floor; works for "factoid lookup" and breaks on "compare X to Y across docs"
- Multi-hop RAG — retrieve, reason about gaps, retrieve again; needed for compositional queries; each hop is another LLM call and another retrieval, costs add up fast
- Agentic RAG — agent decides what to retrieve and when to stop; flexible, expensive, often unnecessary; pick this only when you've already maxed out simpler patterns
- Corrective RAG (CRAG) — grade retrieval relevance, fall back to web search when low; useful when your corpus has gaps you can detect from a confidence score
- Self-RAG — model emits special tokens to control retrieval (retrieve / not / continue); requires fine-tuning, rarely worth it for most teams
- GraphRAG (Microsoft) — build a knowledge graph from docs, retrieve via graph traversal; wins for cross-document relational questions, expensive to build and maintain
- RAG vs fine-tuning vs long context — retrieval for facts that change, fine-tuning for stable behavior/format, long context for one-shot tasks where you can fit the whole doc
- RAG evaluation — three axes: faithfulness (no hallucinations), relevance (answer matches question), coverage (answer uses retrieved context); RAGAs and DeepEval implement these but the metrics are noisy
- Cache-augmented generation — cache common (query, retrieved-context) pairs as full responses; saves the generation cost when queries repeat (FAQs, support flows)
- The honest truth about RAG — most production RAG systems are 90% retrieval engineering and 10% generation; if your generation prompt is fancy and your retrieval is naive, you have it backwards

### S5. Knowledge stores *(prereq: S2)*
- sqlite-vec — vector search inside SQLite; embedded, no server, file is the database; right call for single-node, prototypes, and "tens of millions of vectors"
- pgvector — Postgres extension; right call when you already have Postgres and need transactional consistency between rows and their vectors
- Qdrant — purpose-built vector DB; good performance, decent ergonomics, self-host or managed
- Pinecone — managed-only, expensive at scale, fastest time-to-first-vector; the "throw money at it" option
- Milvus — open-source, scales horizontally, more operational overhead than Qdrant; right call when you've genuinely outgrown single-node
- Chroma — embedded vector DB; popular for prototypes, less production-tested than alternatives
- LanceDB — columnar vector DB built on Lance format; good fit for analytics-heavy workloads
- Knowledge graphs (Neo4j) vs vector — graphs win when questions are relational ("who reports to whom"); vectors win when questions are similarity-based; combining them is GraphRAG
- Multi-tenant knowledge isolation — separate index per tenant beats shared index with metadata filter at scale; cheaper than the alternative when one tenant gets noisy
- Cache invalidation — Phil Karlton's two hard problems; in RAG it's "the source doc changed, what's stale?"; the answer is usually "everything that retrieved it"
- Freshness and staleness detection — version the source, version the embedding, refuse to serve embeddings from versions older than N
- Why most teams overspend on vector DBs — sqlite-vec or pgvector handles the first 10M vectors fine; scale-out only after you've actually outgrown a single node, which most teams never do

---

## L4 — Agency & Tool Use

**Kind:** Action. **Scope:** tool design, protocols, interaction patterns, agent identity. **Anchors:** [ANT] MCP docs, [OAI] function calling cookbook, [HF] tool design chapters.

An agent without tools is a chatbot. Tools are the surface where the model meets the real world — and where most production failures happen. Core principle: every tool is an API contract you're handing to a probabilistic, occasionally-stupid caller that will retry on hiccups.

### S1. Tool design discipline *(no prereq)*
- Tools as typed functions — schema-first design; if you can't write the JSON Schema for your tool, you don't know what it does yet
- JSON Schema for tool interfaces — required fields, types, enums, descriptions; the description field is for the *model*, not for human docs
- Read-only vs side-effecting — separate the two cleanly; read-only tools can be retried freely, side-effecting ones need idempotency keys
- Idempotency keys — agent generates a unique ID per logical action, tool de-duplicates on it; without this, retries cause duplicate emails, double-charges, repeated DB inserts
- Schema validation at the boundary — validate inputs before executing, validate outputs before returning; never trust either side
- Error surfaces the model can recover from — don't return Python tracebacks; return structured errors with a "what to do next" hint ("Rate-limited; retry after 5s")
- Approval gates for paid and destructive actions — anything irreversible needs a human in the loop, full stop; cost-bounded actions can have programmatic gates ("max $0.10 per call")
- Tool allowlists vs sandboxing — allowlist is the floor (only these tools), sandbox is the ceiling (these tools, but with these constraints); use both
- Parallel tool calls — model emits N tool calls at once, runtime dispatches in parallel; cuts wall-clock latency on independent operations
- Tool result format — JSON for structured data, prose for natural language; truncate aggressively (results > a few KB hurt context); always include a "source" hint so the model can cite
- The tool description sentence — first sentence determines whether the model picks the right tool; this is prompt engineering, not docs
- Why most agent failures are tool failures — wrong tool selected, wrong args passed, confusing tool error returned, agent loops; tool design is the highest-leverage change you can make

### S2. Information tools *(prereq: S1)*
- Web search integration — search API → list of URLs → fetch → extract → return; each step has failure modes (rate limits, paywalls, JS-rendered pages, anti-bot)
- Web scraping with anti-bot — Cloudflare, CAPTCHA, browser fingerprinting; either pay for a scraping API (Bright Data, ScrapingBee) or expect to maintain a fragile pipeline forever
- API integration with rate limits — token bucket, exponential backoff, jittered retry; without these you get cascade failures and provider bans
- File ingestion (PDF, CSV, DOCX) — PDF is the worst (tables, multi-column, scanned images); pdfplumber and pymupdf are the practical floors; OCR for scanned docs
- Code interpreter sandboxes — E2B, Modal, Pyodide; let the agent run code on real data without trusting either the agent or the data
- Database query tools — read-only by default, parameterized queries always, schema introspection so the agent knows what columns exist
- Why "just hit the API" is harder than it sounds — auth, retry, pagination, rate limits, schema drift, partial failures, idempotency; every API tool is more code than the user expects

### S3. Action tools *(prereq: S1)*
- Code execution sandboxing — E2B (full VM per session), Modal (function-level), Firecracker (the microVM under E2B); the spectrum is isolation strength vs startup latency
- File system operations — permission models matter: read-only roots, scoped working directories, no symlink escapes; assume the agent will try to read /etc/passwd at some point
- Shell and CLI automation — the most powerful and most dangerous tool; a `shell()` tool with no allowlist is a "delete production" speedrun waiting to happen
- Browser automation (Playwright, Puppeteer) — automate web UIs; brittle to layout changes, fast to demo, slow to maintain
- Computer use / GUI agents (Claude Computer Use, OpenAI Operator) — model sees screenshots, emits clicks/keystrokes; impressive demos, terrible reliability for production today
- Voice and telephony tooling (Twilio + STT/TTS) — adds a real-time-ness constraint that text agents don't have; the latency budget is brutal
- Why action tools need the heaviest review — read-only mistakes cost cycles; action mistakes cost money, data, or trust; the Replit Agent that deleted a dev's database is the canonical cautionary tale

### S4. Meta tooling *(prereq: S1)*
- Dynamic tool registration — agent discovers tools at runtime instead of having them hardcoded; useful for plugin-style agents, expensive in tokens (every tool description sits in context)
- Tool ranking and selection — when there are >20 tools, the model loses accuracy at picking; rank by relevance to the query before showing the model the menu
- Capability descriptors and manifests — structured metadata about what a tool does, what it costs, what it can break
- Tool health checks — does the API respond? Is the rate limit blown? Is the auth still valid? Surface this to the agent before it fails mid-task
- Cost-aware tool selection — when two tools answer the same question, pick the cheaper; non-trivial when the cheap one is also less reliable
- Tool learning from feedback — track which tools succeeded for which query patterns, bias future selection; in practice this is a sparse signal that takes a long time to converge

### S5. Protocols and standards *(prereq: S1)*
- MCP (Model Context Protocol, Anthropic) — standard for tool/resource servers; client-server with capability discovery, sampling, and structured tool results
- What MCP solves — tool-server interop, standardized schema, capability discovery; build a tool once, use it from any compliant client
- What MCP doesn't solve — auth (delegated to transport), discoverability across the internet (no equivalent of npm yet), versioning (each server picks its own scheme)
- A2A (Agent-to-Agent, Google) — emerging standard for inter-agent communication; agent cards advertise capabilities, agents send structured messages
- MCP server ecosystem — Anthropic ships reference servers (filesystem, GitHub, Slack); community has hundreds; quality varies wildly
- Agent cards / manifest formats — capability advertisements; the "package.json" of agents
- OpenAPI for agent tools — well-known schema, mature tooling; usable today, not agent-native (no notion of cost, latency, or destructive-ness)
- Protocol bridging (MCP ↔ A2A ↔ OpenAPI) — translation layers; necessary, ugly, undermines the value of standardization
- Transport and session patterns — stdio for local, HTTP for remote, WebSocket for streaming; long-lived sessions need reconnection logic
- When to skip protocols entirely — for a single-team agent with a fixed tool set, just write the tools as Python functions; MCP is overhead until you need to share tools across agents

### S6. Interaction patterns *(prereq: S1)*
- Human-in-the-loop — human approves each action; safest, slowest, the right call for high-stakes destructive actions
- Human-on-the-loop — human watches a stream, can intervene; the practical middle ground for production
- Full autonomy — agent runs alone; only safe for read-only or tightly-bounded actions
- Approval workflows — Slack / email / in-app prompt with "approve / deny / edit"; the latency budget for human response is the bottleneck
- Streaming agents — partial results emitted as the agent works; UX win, complicates error handling and rollback
- Event-driven vs polling — event-driven (webhook on completion) is right for long-running; polling is right for unreliable transports
- Validation checkpoints — hard gates between stages ("retrieved docs look right? proceed."); the cheap version of human-in-the-loop
- Rollback and compensating actions — for actions that can't be undone (sent email), have a compensating action ready (send correction email); for actions that can be undone (DB write), rollback is the recovery path
- Adaptive autonomy — start gated, earn autonomy by track record; the pattern most "trusted agents" actually need

### S7. Agent identity and authentication *(prereq: S5)*
- OAuth flows for agents — agent acts on behalf of a user; classic OAuth dance with a twist: the agent can't sit through a captcha or 2FA prompt
- Delegated authorization — user grants the agent specific scopes; principle of least privilege; the agent should hold *less* power than the user, never equal
- Scoped permission tokens — one token per task, narrow scope, short TTL; lets you revoke without nuking long-lived credentials
- Credential rotation — long-running agents need automatic rotation; expired credentials mid-task are a common, ugly failure mode
- Machine identity (mTLS, service accounts) — agent-to-service auth via certs or service account tokens; cleaner than rotating bearer tokens
- Multi-agent trust chains — when agent A delegates to agent B, who's accountable? Audit trails need to record both the user and the chain of agents involved

---

## L5 — Multi-Agent Systems

**Kind:** Coordination. **Scope:** when multi-agent is wrong, orchestration, failure modes. **Anchors:** [ANT] "Building effective agents" (the "don't" half), Cognition.ai's "Don't build multi-agent systems" post.

The first multi-agent system you build will be worse than the single agent you replaced. The second one will probably also be worse. By L5 you should have strong opinions about *when* multi-agent is the right answer (rare) and the failure modes you'll inherit (many).

### S1. When multi-agent is wrong *(no prereq)*
- The default answer is "no" — same reason a 5-person startup usually shouldn't run microservices
- "Don't build multi-agent systems" (Cognition.ai) — the canonical post; the argument: shared context is what makes agents work, multi-agent systems shard that context
- Coordination overhead tax — every inter-agent handoff costs tokens for the message *and* tokens for the receiver to re-establish context; the tax is bigger than people expect
- Single agent with role-switching — one agent that adopts different personas per turn often beats two specialized agents because the context isn't fragmented
- Complexity budgets — debugging cost grows superlinearly with agent count; you can debug 1, struggle with 3, have no chance with 10
- The "just add another agent" antipattern — every problem looks like a missing agent; add one, problem moves elsewhere; the architecture is right-sized when adding agents stops helping
- The valid case for multi-agent — components have genuinely separate state, separate tool surfaces, and asynchronous timelines (agent A monitors a queue, agent B handles user requests, they exchange structured messages)
- Test for "is this multi-agent or one-agent-in-disguise" — can each component run alone usefully? If no, it's one agent with imaginary friends

### S2. Orchestration patterns *(prereq: S1)*
- Coordinator-worker — central coordinator dispatches to specialized workers, aggregates results; the most common pattern, the easiest to debug
- Peer mesh — agents communicate freely; expressive, debugging nightmare; rarely worth it
- Hierarchical networks — coordinator-of-coordinators; useful when the problem itself is hierarchical (multi-team org modeling, complex planning)
- Capsule / subprocess isolation — each agent runs in its own process or container; failures don't cascade through shared state; pays in latency and complexity
- StateGraph (LangGraph) — orchestration as an explicit graph; makes the state machine first-class instead of buried in prompts
- Hand-rolled orchestration — Python functions calling each other; right for <5 nodes, wrong for 20
- Router pattern — classify input, dispatch to the right specialist; the bread-and-butter pattern, often the only "multi-agent" you actually need
- Map-reduce pattern — fan out to parallel workers, fan in to a reducer; great for embarrassingly parallel sub-tasks (summarize 100 docs)
- Supervisor pattern — supervisor watches workers, intervenes on stuck/wrong; cost is the supervisor's tokens, value is failure recovery
- Critic-and-verifier — one agent generates, another critiques; the latter is often cheaper than the former; bumps quality on creative tasks
- Assembly line — sequential specialization (extract → summarize → format); each agent has a narrow job; brittle to errors propagating downstream
- Blackboard pattern — shared workspace where agents read and write; classic AI architecture from the 80s, good for problems with no fixed sequence

### S3. Coordination mechanics *(prereq: S2)*
- Message passing design — structured messages with explicit fields beat freeform; "task_id, role, content, status" beats a paragraph every time
- Shared state — single source of truth (DB, file, KV); without it, agents make conflicting decisions on stale views
- Context handoff — when agent A passes to agent B, what does B need? Usually less than A thinks and more than the message includes
- Conflict resolution — when two agents reach different conclusions, who wins? Need an explicit rule (most-recent, supervisor-decides, escalate-to-human)
- Task delegation — "you handle X, I'll handle Y"; works only if the agents have non-overlapping competence and a clean handoff
- Termination criteria — when does the system stop? "All sub-tasks done" is naive; needs an explicit "and the supervisor verified completion"
- Agent discovery and registration — for dynamic agent fleets, a registry; A2A uses agent cards, MCP uses capability discovery

### S4. Frameworks *(prereq: S2, S3)*
- LangGraph — explicit StateGraph, durable execution support, the most production-ready of the orchestration frameworks; verbose for simple flows
- OpenAI Agents SDK — Anthropic-style "agent + tools + handoffs" but tied to OpenAI ecosystem; cleanest API of the bunch
- PydanticAI — Pydantic models for agent IO, type-safe; small but growing
- CrewAI — declarative role-based agents; demos beautifully, struggles in production due to opaque control flow
- AutoGen (Microsoft) — multi-agent conversations as the primitive; powerful, hard to constrain
- Haystack — pipeline-first; heavier on retrieval than agentic loops; right call for RAG pipelines, less so for agents
- Temporal / Inngest — durable execution platforms; not agent frameworks, but the right substrate for *running* multi-agent systems for hours/days
- Framework selection criteria — three questions: (1) do you need durable execution? (2) is your control flow a graph or a tree? (3) how much do you trust your team to debug the framework's internals when it breaks?
- Why most teams pick the wrong framework first — frameworks demo well; the right test is "what does the trace look like when something fails?"

### S5. Failure modes at scale *(prereq: S3, S4)*
- Coordination collapse — deadlock (A waits for B, B waits for A) and livelock (both retry forever); needs timeouts and explicit termination conditions
- Cascade failures — one agent's bad output becomes another's bad input; without isolation, one bug ruins the chain
- Deference loops — A asks B, B asks A, they bounce; classic when responsibilities aren't clearly partitioned
- Context window exhaustion — multi-turn chains accumulate context until the receiving agent's prompt is mostly noise from earlier hops
- Hallucination amplification — A hallucinates a fact, B treats it as ground truth, C builds on it; by step 5 you've constructed a confident lie
- Silent failure / false success — agent reports "done" when it isn't; without external verification, the supervisor doesn't notice until much later
- Communication overhead explosion — N agents → up to N² messages; communication cost dominates compute cost past ~5 agents
- Goal drift — long-running multi-agent flows lose the original goal as agents focus on their narrow piece; reanchor with the goal in every message
- The Cognition.ai post-mortem pattern — most multi-agent failures trace back to "the system thought it was making progress, but it was making progress on the wrong thing"

---

## L6 — Infrastructure & Deployment

**Kind:** Runtime. **Scope:** serving, hardening, caching, deployment, cost, API design, fine-tuning. **Anchors:** vLLM docs, Anthropic prompt-caching post, [OAI] cookbook on streaming/webhooks.

This is where the prototype meets the SLO. AI infra has weirder failure modes than regular infra: long-tail latencies, non-deterministic outputs, and bills that scale with prompt length. By L6 you should be able to look at a request flow and predict where it'll page someone at 3am.

### S1. Model serving *(no prereq)*
- API providers vs self-hosted — providers win on time-to-first-call and SOTA quality; self-hosted wins past ~$10k/mo of sustained usage
- Local inference — Ollama for laptops, vLLM for serious throughput, llama.cpp for portable/embedded; pick by deployment shape, not preference
- Model routing — cheap-first cascades: try the cheap model, fall back to expensive on failure or low confidence; handles the long tail of hard queries without paying for everything
- Fallback model chains — when the primary endpoint fails, try the secondary (different provider); avoids single-vendor outages taking you down
- Token streaming — emit tokens as generated; UX win for chat, complicates downstream parsing for structured output
- GPU orchestration — Kubernetes + node selectors + device plugins; or pay someone (Modal, Replicate, Together) to do it for you
- Inference provider selection — Groq for blazing-fast inference on supported models, Together/Fireworks for breadth, Anthropic/OpenAI for frontier; multi-vendor by default
- The "build vs buy" math for inference — your infra team's loaded cost vs the provider markup; the markup is real but smaller than people expect at small scale

### S2. Production hardening *(prereq: S1)*
- Rate limiting strategies — token-bucket per-user, separate limits for input/output tokens, separate budgets per tenant; without these one user takes down everyone
- Retry policies — exponential backoff with jitter, idempotency keys for non-idempotent calls, cap total attempts; never retry on 4xx
- The retry storm — when an LLM endpoint hangs, naïve retries pile up faster than they resolve; use bulkheads (per-endpoint connection pools) to contain
- Cost ceilings per request — hard $ cap on a single agent run, abort gracefully when hit; otherwise an infinite-loop bug becomes a five-figure bill (see AutoGPT cost runaways)
- Timeout design for variable latency — naïve timeout = p99 + buffer; better: separate timeouts for time-to-first-token (TTFT) and inter-token; LLM p99 can be 10x p50
- Backpressure and queue-based handling — when traffic spikes, queue with explicit limits; better to slow down than to fail with cryptic 503s
- Circuit breakers — when an endpoint's error rate exceeds a threshold, stop trying for a cooldown window; classic pattern, often skipped, always missed in postmortems
- Health checks and readiness probes — an LLM endpoint is "healthy" if it returns within budget at p99, not if it returns *at all*; design checks accordingly
- Graceful degradation — when the primary model is down, fall back to a cheaper one with a banner ("running in degraded mode"); better than 500
- The ChatGPT March 2023 outage — a Redis race condition in the async client revealed user data across sessions; the lesson: shared infra + concurrency + LLMs makes data leakage easy

### S3. Caching and performance *(prereq: S1)*
- Semantic caching — embed query, look up nearest cached query, serve its response if similarity > threshold; works on FAQs, poisons on slightly-different-meaning queries
- When semantic caching backfires — "What's the weather in Paris?" and "What's the weather in Berlin?" embed close, the cached Paris answer ships for Berlin; the bug is silent
- Redis caching for LLM calls — straightforward keyed cache (prompt → response); only useful when prompts repeat exactly, which is rarer than you think
- Prompt caching (KV reuse) — provider caches the KV state for prefixes; identical system prompt across requests = ~10% input cost on the cached portion (Anthropic); huge win for chat
- Response caching with invalidation — for prompts whose answers change (current data, user-specific), TTL is the simple answer; explicit invalidation when the underlying source updates
- Prefix caching for shared system prompts — design system prompts to be stable; put variable content (user info, retrieved docs) at the *end* so the prefix is reusable
- Cache warming — for predictable queries, pre-compute responses off-peak; underutilized pattern
- The cache hit rate that actually matters — not "% of queries that hit cache", but "% of cost saved"; an exact-match cache with 5% hit rate can save more than a semantic cache with 50% hit rate

### S4. Data infrastructure *(prereq: S1)*
- Vector database operations at scale — sharding, replication, index rebuilding under live traffic; same problems as any other DB, with vectors
- SQL vs NoSQL for agent state — SQL when you need transactions across agent steps, NoSQL when each step is independent; SQLite is the underrated default for single-node
- Message queues for async agents — Redis Streams, Kafka, SQS; pick by durability needs; long-running agents need durable queues, full stop
- Stream processing for real-time pipelines — Flink, Materialize; usually overkill for agents, the right call for telemetry/observability *of* agents
- Feature stores for agent context — user profile, recent activity, preferences; the line between "context" and "features" is fuzzy in agent stacks
- The agent state schema problem — you'll redesign it three times; design for migration from day one

### S5. Deployment patterns *(prereq: S2)*
- Container strategies — image with Python + deps; the tricky part is GPU drivers and model weights; multi-stage builds and weight caching are your friends
- Serverless agents — cold starts hurt for stateful agents; warm pools or always-on containers for latency-sensitive flows
- Persistent agent processes — agent runs as a long-lived process with state in memory; fast, fragile, hard to scale horizontally
- Canary deployments — route 1-5% of traffic to the new model/prompt, watch metrics, roll forward or back
- Blue-green for prompt updates — two prompt versions live simultaneously, flip the routing atomically; zero-downtime prompt changes
- Agent-as-a-service — your agent is an API endpoint other teams call; design with versioning, SLOs, and rate limits from day one
- Shadow mode — run new agent in parallel with old, log both, ship when they agree; safer than canary, expensive in tokens

### S6. Cost engineering *(prereq: S1, S2)*
- Token budgeting per task — explicit max_tokens for each agent run; without it, runaway loops are five-figure bugs (this has happened to roughly every team that's run agents in prod)
- Cost-per-task modeling — log tokens-in, tokens-out, model used, per request; aggregate by feature; this is your actual cost dashboard
- Multi-step pipeline budget allocation — a 5-step pipeline at $0.02 per step is $0.10 per task; multiply by traffic; the math gets ugly fast
- Token-level cost attribution — which agent run, which step, which user, which feature; without it you can't optimize because you can't find the expensive 1%
- Reasoning token cost accounting — thinking tokens are billed at output rate, often the biggest line item for reasoning models; track separately
- Agent ROI frameworks — what does this agent do per $? What would a human do for the same money? The answer is not always favorable, especially for "AI assistant" features bolted onto cheap workflows
- FinOps for agents — same playbook as cloud FinOps: tagging, alerts, budget caps, weekly reviews; the bar is "can you stop a runaway in <5 minutes?"
- The single biggest cost optimization most teams miss — switching from frontier to mid-tier model; usually 5-10x cheaper for 5-15% quality drop on most tasks

### S7. API design for AI services *(prereq: S2, S5)*
- Streaming response design — SSE for HTTP-friendly streaming, WebSocket for bidirectional, chunked transfer for compatibility with anything
- Webhook patterns — for long-running tasks, webhook on completion; the alternative (long-polling) wastes connections
- Long-running task APIs — submit returns task_id, separate endpoint to poll or websocket-subscribe; design for cancellation and resumption from the start
- API versioning for prompt and model changes — version the *behavior*, not just the schema; same input may produce different output across model versions
- Idempotency keys for agent actions — caller provides key, server de-dupes; mandatory for non-idempotent endpoints
- Multi-tenant API isolation — separate rate limits, separate model quotas, separate logging; one tenant should not be able to starve another or read another's traces
- Why your AI API will look different from your CRUD API — variable latency, variable cost per call, structured-but-unpredictable output, streaming as table stakes

### S8. Fine-tuning and adaptation *(prereq: S1)*
- Full fine-tune vs LoRA vs QLoRA — full retrains everything (expensive, sometimes overfits), LoRA trains low-rank adapters (cheap, modular, swappable), QLoRA quantizes during training (laptop-runnable)
- When to fine-tune vs prompt engineer — prompt-engineer first; fine-tune only when you have hundreds of examples *and* prompting can't reach the quality bar
- Synthetic data generation — bigger model labels data for smaller model; quality of the smaller model is bounded by quality of the bigger
- RLHF — reward model learns from human preferences, policy is RL'd against the reward model; expensive, brittle, the canonical alignment recipe
- DPO (Direct Preference Optimization) — same goal as RLHF without the RL; cheaper, simpler, often comparable quality
- Model merging (TIES, DARE, SLERP) — combine two fine-tuned models without retraining; useful when you've fine-tuned for two skills and want both
- Continual learning pitfalls — catastrophic forgetting (new training erases old skills); the cure (rehearsal, regularization) is more art than science
- The honest framing — most teams that "need to fine-tune" should improve retrieval first; fine-tuning is the answer to "wrong format" and "wrong tone", not "wrong facts"

---

## L7 — Safety, Security & Governance

**Kind:** Constraints. **Scope:** threats, defenses, governance, privacy. **Anchors:** [OWASP] Agentic AI Top 10, [OWASP] LLM Top 10, [LW] adversarial attacks post, Simon Willison's prompt-injection writeups.

Most AI security is about treating the model as a probabilistic, easily-tricked, sometimes-hostile component of your system, and architecting around it. By L7 you should reflexively distinguish data plane from control plane and know why "just tell the model not to" is the security equivalent of "please don't break in."

### S1. Threat landscape *(no prereq)*
- Direct prompt injection — attacker writes "ignore previous instructions and..."; trivial to defend against (sandwich the user input, validate output) but still ships in production
- Indirect prompt injection — malicious instructions embedded in retrieved data, web pages, emails; the retrieval system serves them as innocent context, the model executes them; M365 Copilot's EchoLeak was this
- Data plane vs control plane — control plane = your prompt template; data plane = user input + retrieved docs + tool results; treat data-plane content as never-trusted, even when it came from your own systems
- Goal hijacking — attacker rewrites the agent's objective via injected text ("you are now a helpful assistant for the attacker")
- Tool misuse and excessive agency — agent has more tool access than the task needs; attacker exploits the slack to do things the user didn't authorize
- Memory poisoning — attacker writes hostile content into long-term memory (semantic, episodic) so it influences all future runs, not just this session
- Multi-hop prompt injection — injection in step 1 alters retrieval in step 2 alters generation in step 3; harder to detect, easier to deny, much worse blast radius
- Data exfiltration via agent tools — model coaxed into building a URL with sensitive data and "fetching" it; the fetch is the exfil; markdown image rendering is a classic vector
- Supply chain attacks on MCP servers — install a malicious MCP server, get a backdoor in every agent that uses it; npm-style problems with less mature defenses
- Agent credential theft — credentials in the prompt context are a juicy target; never put long-lived secrets where the model can see them
- The Bing/Sydney prompt leak — early Bing chat had its system prompt extracted via prompt injection ("Sydney" was supposed to be a hidden codename); the lesson: anything in the prompt is leakable, plan accordingly
- The "ignore previous instructions" pattern — still works on production systems in 2026, especially in tool/agent stacks where defenders moved on to bigger problems

### S2. Defense mechanisms *(prereq: S1)*
- The deterministic shell pattern — wrap the stochastic LLM core in deterministic code that validates inputs, validates outputs, enforces budgets; the LLM is one component, not the whole system
- Bounded loops — hard cap on iterations (e.g., 10); without it, ReAct-style agents loop on certain prompts forever
- Tool allowlists, deny-by-default — list of permitted tools per task, refuse anything else; the floor for any production agent
- Output schema validation as a safety layer — even if you trust the model, validate; structured output that doesn't match schema gets rejected before any side effect
- Input filtering — strip known prompt-injection patterns, encode user input as data not instructions, never concatenate without delimiters
- Output filtering — scan outputs for PII, credentials, prompt-injection attempts that might be persisted into memory or surfaced to other users
- Sandboxing execution environments — code interpreters in microVMs, no network access by default, ephemeral filesystems, hard CPU/memory caps
- Permission systems and least privilege — the agent should hold *less* power than the user, scoped to the current task, not equal-or-greater
- Kill switches — emergency stop; a button that disables the agent fleet; you should have one before you need one
- Human oversight checkpoints — for high-stakes decisions, a human approves; the question is *which* decisions, not whether to have any
- Canary tokens for data leakage detection — embed unique strings in your data; if they show up in outputs anywhere, you've found exfiltration
- Red teaming agents — deliberately try to break your own agent (with prompt injection, tool abuse, social engineering); if you don't, someone else will, less politely

### S3. Governance and compliance *(prereq: S2)*
- OWASP Agentic AI Top 10 — the canonical threat list for agents (LLM Top 10 covers chat, Agentic Top 10 covers tool-using agents); read it once, reference it forever
- EU AI Act — practical implications: risk-tiered obligations, transparency for high-risk, banned uses (social scoring, certain emotion recognition); your "is this high-risk" decision drives the compliance burden
- Audit trails for agents — structured logs of every model call, tool call, decision; without these, post-incident analysis is guessing
- Policy enforcement for agents — rules expressed as code (this agent can't email customers, this agent can't write to prod); enforce at the tool boundary, not in the prompt
- Zero-trust for agent architectures — every component re-authenticates; no implicit trust between agents, between agent and tool, or between agent and memory
- Agent identity management and inventories — for organizations running many agents, you need an inventory: which agents exist, who owns them, what they can do, when they last ran
- Responsible AI frameworks that actually work — opinionated take: the ones with concrete checklists (NIST AI RMF, MIT TC) beat the ones with abstract principles
- The compliance trap — most "AI compliance" tools are checkbox theater; the work that matters is auditability, access control, and incident response runbooks

### S4. Privacy and data protection *(prereq: S2)*
- PII detection and redaction — regex + ML detectors; redact before sending to model, restore (or not) on the way back
- Data minimization — only put in the prompt what's needed for the task; "user history" can be a 10-line summary instead of 100 messages
- Right-to-erasure in agent memory — GDPR/CCPA require deletion on request; agent memory (vector DB, episodic logs) needs a deletion path; "erase by user_id" is the minimum
- Consent management for agent data use — explicit consent for training, separate consent for retrieval; default-off where the law requires it
- Differential privacy for training data — add noise calibrated to a privacy budget; works for some training regimes, not all; usable for synthetic data generation
- Confidential computing for inference — run inference in a TEE (Intel SGX, AMD SEV); useful when the model provider is also a competitor; rare in practice
- The lawyer test — would you be comfortable explaining your data handling to a regulator with the system in front of them? If not, fix it before the audit, not after

---

## L8 — Evaluation, Observability & Applications

**Kind:** Measurement. **Scope:** evals, observability, debugging, CI/CD, performance, applications. **Anchors:** RAGAs/DeepEval docs, LangSmith/Langfuse/Braintrust docs, [OAI] evals cookbook, SWE-bench/AgentBench/BFCL papers.

Without measurement, every change is a vibe. L8 is how you turn "the new prompt feels better" into "the new prompt's pass rate is 84% vs 79% on the regression suite, with cost up 12%." By the end of L8 you should be skeptical of any AI feature whose owner can't show you their eval.

### S1. Evaluation frameworks *(no prereq)*
- RAGAs — opinionated metrics for RAG (faithfulness, relevance, context precision, context recall); easy to wire up, noisy unless you tune it
- DeepEval — pytest-style assertions for LLM outputs; works for unit-test-grain checks, less for end-to-end
- Hand-rolled evals — pytest + your own scoring; right call for anything beyond a basic happy path
- LLM-as-judge — use a model to score outputs; cheap, scalable, biased; the canonical biases follow
- Position bias — judge prefers whichever option is shown first (or last); detect by swapping order on half the eval set and seeing if the verdict changes
- Verbosity bias — judge prefers longer outputs even when shorter is correct; detect with a length-controlled subset
- Self-preference bias — judge prefers outputs from its own model family; detect by judging with a different family and comparing
- Calibration of LLM-as-judge — if a human and the judge agree only 70% of the time, the judge's scores have a 30% noise floor; quantify before trusting
- Golden sets and regression suites — frozen (input, expected) pairs that catch regressions; treat them like a test suite, version them, gate deploys on them
- Adversarial evaluation — deliberately hard or weird inputs to find failure modes; not a number you optimize, a portfolio you keep refreshing
- Trajectory evaluation — score the agent's *path*, not just the answer; an agent that produces the right answer for the wrong reason will fail differently next time
- Fuzzy comparison metrics — Levenshtein, token_sort_ratio, WRatio (rapidfuzz); the right call when answers vary in phrasing but mean the same thing
- End-to-end agent evaluation — score the whole pipeline, not the components; the components can pass and the whole still fail
- Multi-turn evaluation — evaluate over conversations, not single turns; harder, more realistic, the actual production setting for many systems
- SWE-bench — code-fix tasks from real GitHub issues; the most-cited coding-agent benchmark; benchmark contamination is a real concern
- AgentBench — multi-environment agent eval; useful for breadth, less useful for any specific use case
- BFCL (Berkeley Function Calling Leaderboard) — function-call accuracy across many APIs; the right thing to look at for tool-calling models specifically
- The benchmark contamination problem — public eval sets leak into training data over time, scores inflate, real-world performance lags; rotate your golden set, keep some held-out, don't trust 95%+ on public benchmarks

### S2. Observability *(prereq: S1)*
- Structured tracing — every agent run is a trace: nested spans for model calls, tool calls, retrieval; the unit of debugging
- Span hierarchies for multi-step agents — parent span = agent run, child spans = each step, grandchild spans = inside each step (model call → tool call); deep but navigable
- LangSmith vs Langfuse vs Braintrust — three flavors of "trace + eval + dataset" SaaS; LangSmith integrates deepest with LangChain, Langfuse is open-source self-hostable, Braintrust is the most opinionated about evals
- OpenTelemetry for AI agents — emerging conventions for AI semantic attributes (gen_ai.* namespace); useful for org-wide observability that doesn't lock you into a vendor
- Replay-from-trace debugging — given a trace, re-run a step with a different prompt or model; this is *the* debugging workflow once you have it
- Prompt versioning in traces — every span tags the prompt version used; without this you can't bisect regressions across prompt changes
- Cost attribution per turn — tokens in, tokens out, cost per step, rolled up to the trace; lets you find the expensive 1% of traces eating most of the budget
- Token usage dashboards — daily, weekly, by feature, by user tier; the answer to "where did this month's bill come from?"
- Alert design for agent failures — alert on rate-of-failure, not single failures; alert on cost-anomaly, not absolute cost; alert on latency-percentile shifts, not raw latency
- Why "the trace is the spec" — for AI systems, the trace tells you what actually happened in a way logs never will; design observability before features

### S3. Debugging and testing *(prereq: S1, S2)*
- Prompt debugging — inspect the rendered prompt (after templating), check token count, check that retrieved docs landed in the right slot; surprisingly often, the prompt isn't what you think
- Tool call debugging — check the JSON the model emitted, validate against schema, run the tool with the same args manually; isolate model-bug from tool-bug
- Deterministic replay — re-run a trace with the same prompts/params; should give the same output; if not, you have hidden non-determinism (provider batching, time-dependent prompts, racing tool calls)
- Failure analysis patterns — group failed runs by failure mode, not by user; "10% of runs fail" is less useful than "8% timeout on retrieval, 2% schema-violation in tool calls"
- Unit tests for agents — test individual tools, individual prompt templates, individual parsing logic; doesn't catch end-to-end issues but cheap to run on every commit
- Integration tests for tool-calling agents — full pipeline, mocked external services; slow, valuable, the test suite that gates deploys
- Regression testing for prompt changes — before merge, run the golden set; below threshold = block; above = ship
- Snapshot testing for prompt outputs — save canonical outputs, diff on change; works for deterministic-ish setups (low temp, fixed seed), poorly otherwise
- Mock tool servers — stand up a fake MCP server / fake API, control its responses, test the agent against deterministic tool behavior
- Chaos engineering for agents — kill the retrieval mid-run, return malformed tool output, return very slow responses; agents that survive chaos in test survive incidents in prod
- The single most useful debugging tool — sit with a failed trace, replay each step, ask "what would I have done?"; most agent bugs are visible in the first replay

### S4. CI/CD for AI systems *(prereq: S3)*
- Prompt testing in CI pipelines — golden set runs on every PR that touches a prompt; gate merges below threshold
- Model regression checks — when a provider updates a model, re-run your golden set; quality can shift without warning (and providers don't always tell you when they update)
- Eval-gated deployments — production deploy requires eval pass; not eval-passing-on-this-PR, eval-passing-against-a-baseline
- Shadow mode and dark launches — new agent runs in parallel with old, outputs compared; ships when divergence is acceptable
- Canary releases with eval thresholds — small traffic share to the new version, monitor eval-on-live-data, roll forward when stable
- Rollback strategies for model updates — pin model versions, have a documented downgrade path; "the new model regressed" is a 3am page you want a runbook for
- Contract testing for LLM outputs — define the schema/shape your downstream depends on, reject changes that violate it; the LLM equivalent of API contract tests

### S5. Performance engineering *(prereq: S2)*
- Latency optimization — measure first: time-to-first-token, inter-token latency, total wall-clock; optimize the bottleneck, not your guess
- Cost optimization patterns — model routing (cheap-first), prompt caching, prompt compression, batching, smaller-model fallback
- Parallel execution for independent steps — when steps don't depend on each other, fire them in parallel; cuts wall-clock without changing cost
- Batching LLM calls — for high-volume async work, batch into single calls when the API supports it; cost stays similar, throughput up
- Model routing — small/fast for easy queries (classification, simple Q&A), large/slow for hard ones; route based on a cheap classifier or rule
- Context pruning — drop low-value content from the prompt; usually retrieved docs (drop low-score ones) or conversation history (summarize old turns)

### S6. Application patterns *(prereq: S1)*
- Coding agents — architecture: indexed codebase + LSP + sandbox + LLM with file-edit tools; failure modes: spec drift, hallucinated APIs, tests that pass without doing the right thing; references: Cursor's apply model, Devin's loop, Claude Code's design
- DevOps and SRE agents — incident triage, runbook execution, log analysis; high-stakes, narrow autonomy; the right pattern is bounded execution with strong audit
- Customer support agents — RAG over product docs + ticket history + tools (refund, replace, escalate); the Air Canada chatbot precedent: the company is liable for what the bot says, design accordingly
- Research and deep-analysis agents — multi-step retrieval and synthesis; classic example: market research, competitive intel; OpenAI's Deep Research and Claude's Research are the consumer versions
- Data pipeline agents — extract, transform, validate over messy data; the agent's job is the messy parts (column inference, schema mismatch); deterministic code does the rest
- Document processing agents — invoices, contracts, forms; OCR + structured extraction; LLMs handle the cases templates can't
- The honest take on application patterns — every "AI agent" application is a thin layer over the patterns above; the differentiation is in retrieval quality, tool design, and eval discipline, not in the agent itself
