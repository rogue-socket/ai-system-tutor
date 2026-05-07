# Builder-First Path

The code-first orientation through the curriculum. Loaded when `learner.orientation = builder_first` in `progress.json`.

**Audience.** Engineers targeting the AI Engineer job market — shipping LLM-powered features in production. Not ML researchers, not safety researchers, not academic. The path optimizes for *can ship a working agent in 2 weeks* over *can derive attention from scratch*.

**Method.** 10 loops of structured FAFO — fuck-around-and-find-out with a defined break and a defined win per loop. Every loop is a folder of code the learner opens in their editor, runs, breaks, fixes. Theory shows up only when motivated by the code in front of them.

**Default model.** Gemini (free tier) via `google-genai`. Loops are model-agnostic via a thin `llm.py` wrapper, but Gemini is the default to remove the credit-card-and-API-key friction at lesson 1.

**Total commitment.** ~70–120 hours of focused work across the 10 loops, 8–15 weeks at part-time pace (~6–10 hrs/week). Loops 1–9 fit comfortably inside the Gemini free tier for ~95% of learners; Loop 10's capstone may exceed it depending on scope (budget $5–20 if so, or switch to Gemini Flash-Lite via `llm.py`). The curriculum is "done" when the capstone (Loop 10) ships with a README, ≥20 eval examples, and a written postmortem.

**Workspace layout under `~/ai-systems/exercises/`.** Loops live inside their group directory, sharing the group's venv:

```
~/ai-systems/exercises/
├── group-A/
│   ├── .venv/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── loop-1-bare-loop/
│   │   ├── agent.py
│   │   ├── BREAK.md
│   │   ├── WIN.md
│   │   ├── NOTES.md           # learner fills during/after the loop
│   │   ├── CHEATSHEET.md      # learner fills during/after the loop
│   │   └── quickpass.json     # 3 questions sourced from WIN criteria
│   ├── loop-2-tools-by-hand/  ...
│   ├── loop-3-react-by-hand/  ...
│   └── loop-4-agent-state/    ...
├── group-B/  (loops 5, 6, 7a, 7b — same layout)
├── group-C/  (loop 8)
└── group-D/  (loops 9, 10)
```

Activating a group (`source group-A/.venv/bin/activate`) makes all that group's loops runnable. The tutor announces the venv switch when crossing a group boundary.

---

## Setup (one-time, before Loop 1)

The setup must run in under 5 minutes for a learner with a working Python install. If it takes longer, fix the setup, not the lessons.

### Step 0a — Install `uv`

`uv` is the dependency manager. One binary, fast, replaces `pip + venv`.

- macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

### Step 0b — Get a Gemini API key

Documented in detail at `setup/get-gemini-key.md` (asset). Click-path:

1. Go to `https://aistudio.google.com/apikey`.
2. Click "Create API key" → pick a project (or create one).
3. Copy the key.
4. In the workspace root, `cp .env.example .env` and paste the key as `GEMINI_API_KEY=...`.

The free tier covers everything in Loops 1–9. The capstone (Loop 10) may exceed it depending on the project; learner can switch to paid Gemini or another provider via the `llm.py` wrapper.

### Step 0c — Pick the right group venv

Builder-first uses **four group venvs**, not per-loop. Loops share environments where dependencies don't conflict.

| Group | Loops | Adds |
|---|---|---|
| **A** | 1, 2, 3, 4 | `google-genai`, `python-dotenv`, `pydantic` |
| **B** | 5, 6, 7a, 7b | + `langchain`, `langchain-google-genai`, `langgraph`, `mcp` |
| **C** | 8 | + `chromadb`, `rank-bm25`, `sentence-transformers` |
| **D** | 9, 10 | + `fastapi`, `uvicorn`, `httpx`, `prometheus-client` |

Each group lives at `~/ai-systems/exercises/group-{A,B,C,D}/` with its own `pyproject.toml` and `uv.lock`. Activation is two separate commands: `cd` into the group dir, then `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows PowerShell). The tutor announces the group switch when the learner crosses a boundary.

### Step 0d — Sanity check

`setup/sanity_check.py` runs after group activation. Validates the Gemini key + makes one real API call. If it fails, the tutor diagnoses (key missing, network, billing, etc.) before any lesson runs.

### Step 0e — Pinning and old packages

All deps are **hard-pinned**. `uv.lock` is committed per group. The tutor reads `setup/LOOP_VERSIONS.md` on first activation and warns if the manifest is >6 months old:

> "These pins are from 2026-05. Current LangChain has different APIs. The loops are calibrated to the pinned versions — we'll use those. If you want to upgrade later, do it after Loop 9."

If `uv sync` fails (yanked dep, transitive break), fall back to `requirements-loose.txt` per group with looser pins. The tutor's recovery script.

---

## Onboarding handoff (diagnostic → Loop 1)

When a learner picks `builder_first` in Step 2.5 of `SKILL.md`, the lane's diagnostic still runs (you need to know what they know to choose where to lean in). After the diagnostic, the tutor announces builder-first explicitly — no surprise pivots:

> "Builder-first means we start writing code in your editor, right now. Ten loops, ~70–120 hours total, ~8–15 weeks part-time. Gemini Flash, free tier covers everything until the capstone. Each loop you'll open a folder, run something broken, fix it, then write notes you'll actually re-read.
>
> First, 10 minutes of setup — install `uv`, get a Gemini key, run a sanity check. Then Loop 1: the dumbest possible agent, ~30 lines. Sound good?"

If they confirm, run setup via `setup/install-uv.sh` + `setup/get-gemini-key.md` + `setup/sanity_check.py` (in that order). On sanity check pass, open `loop-1-bare-loop/agent.py` in the learner's editor and start.

If they want to redirect (e.g. "skip Loop 1, I've done this") — that's `/loop quickpass` for proof-of-knowledge or `/loop 2` to jump. Honor it.

---

## The 10 loops

Format per loop: **Goal · Group · Files · Break · Win · Time · Topics · Key beats.**

Topic codes reference layer-section IDs from `curriculum.md` (e.g. `L2 S1` = Layer 2 Section 1).

### Per-loop artifacts (applies to all 10 loops)

Every loop's WIN, in addition to the loop-specific code requirements, includes producing three artifacts in the loop folder:

- **`NOTES.md`** — learner-written with tutor help, written *after* the WIN code is running. Three sections, ~3 short paragraphs each:
  1. **Concept.** What the loop teaches in the learner's own words. No jargon copied from the tutor.
  2. **The break.** The specific failure the learner hit when running the starter. Include the actual error, what they thought was wrong, what was actually wrong.
  3. **The fix.** What change resolved it, and *why* — the underlying reason, not just the diff.
- **`CHEATSHEET.md`** — one printable page. Four sections: **Commands** (shell + Python one-liners), **Patterns** (3–5 reusable code snippets), **Gotchas** (3–5 traps), **Numbers** (token counts / latencies / costs the learner observed). Optimized for "skim this 6 months from now, get unstuck in 60 seconds."
- **`quickpass.json`** — three questions sourced from the loop's WIN criteria. Format: `[{"q": "...", "answer_outline": "..."}]`. Used by `/loop quickpass` for learners who want to skip-with-proof. Authored by the skill maintainer (not the learner); learner fills NOTES.md and CHEATSHEET.md.

The first two are *how a 10-loop journey becomes durable knowledge* instead of disposable tutorial-following. The HTML viewer (deferred work) renders these. Without them, builder-first is a series of demos that the learner forgets.

### Loop 1 — Bare loop

- **Goal.** Build the dumbest possible agent and feel that "agent" is just a while loop around an LLM call.
- **Group.** A.
- **Files.** `agent.py` (~30 lines), `BREAK.md`, `WIN.md`.
- **Break.** Starter file calls Gemini once and prints. Has no loop. Learner must (a) wrap it in a loop, (b) feed previous output back as context, (c) add a system prompt, (d) hit the realization that the model can only emit text — it can't take actions.
- **Win.** A 50-line script where the learner can have a multi-turn conversation with a Gemini model, with a system prompt, and conversation history that feeds back. Plus the explicit observation written into a comment: *"the model only outputs text; for it to do anything in the real world, something else has to act on that text."*
- **Time.** 1–2 hours.
- **Topics.** `L0 S3` (how models generate), `L0 S4` (tokens, context), `L0 S5` (prompting as steering), `L2 S1` (the agent loop).
- **Key beats.**
  - Strip the system prompt mid-conversation, observe behavior shift. Add it back.
  - Print token counts per turn. Watch context grow.
  - Force a long conversation, hit the rate limit or context limit, see what failure looks like.
  - **Streaming.** Flip from blocking to streaming output. Watch tokens arrive one at a time. Feel time-to-first-token vs total latency. Notice how streaming changes the UX even when total time is the same.

### Loop 2 — Tools by hand

- **Goal.** Feel why function-calling APIs exist by suffering through the alternative.
- **Group.** A.
- **Files.** `agent.py`, `tools.py`, `BREAK.md`, `WIN.md`.
- **Break.** Starter has a `calculator(a, b, op)` function and a system prompt that asks the model to "output JSON like `{"tool": "calculator", "args": {...}}` when you need to compute." Parse the model's text output and dispatch. It will break: model outputs prose around the JSON, model invents tool names, model puts strings where numbers go.
- **Win.** Learner replaces the brittle text parsing with Gemini's native function-calling API. Same calculator now works robustly. Learner adds a second tool (e.g. `get_weather` mock). Hot-swaps the tool registry mid-conversation and observes the agent's behavior shift.
- **Time.** 2–3 hours.
- **Topics.** `L1 S4` (structured output), `L4 S1` (tool design discipline), `L4 S2` (information tools), `L4 S3` (action tools — mocked).
- **Key beats.**
  - Quantify how often text parsing fails (run 20 turns, count broken outputs).
  - Compare text-parse vs native function-call latency and reliability side-by-side.
  - Add a tool with a side effect (e.g. `write_file`). Discuss idempotency briefly — *"what happens if the model retries this tool?"* Tee up Loop 9.
  - **Pydantic schemas for tool args and structured output.** Replace dict-based arg specs with Pydantic models. Feel the validation kick in when the model emits a wrong-typed arg. This is the dominant 2026 pattern across LangChain, OpenAI SDK, and the Anthropic SDK.
  - **Tool error contracts.** Force a tool to fail (raise an exception, return a 5xx-style error string). Compare two error styles: opaque (`"error"`) vs descriptive (`"calculator failed: division by zero. Try a non-zero divisor or a different tool."`). Watch the model recover from descriptive errors and spiral on opaque ones. The lesson: tool errors are part of the prompt; design them.

### Loop 3 — ReAct by hand

- **Goal.** Implement reason-act-observe explicitly and hit its real failure modes.
- **Group.** A.
- **Files.** `react_agent.py`, `tools.py`, `traces.py` (logs each step), `BREAK.md`, `WIN.md`.
- **Break.** Starter implements a basic ReAct loop. Run it on a multi-step task (e.g. "find the population of the capital of France, multiply by 2"). It will hit at least three of: malformed Thought/Action/Observation parsing, infinite loops, the 10-iteration degradation, premature termination, hallucinated tool names.
- **Win.** Learner adds: max-iteration cap, malformed-output recovery, an explicit termination condition. Reads their `traces.py` log to identify *which* failure mode they hit. Writes a one-paragraph reflection on what they'd want from a framework.
- **Time.** 3–4 hours.
- **Topics.** `L2 S1` (agent loop), `L2 S3` (reasoning patterns — ReAct), `L2 S4` (reflection — preview).
- **Key beats.**
  - Trace inspection is the load-bearing skill. Learner spends time *reading their own logs*, not just running.
  - The "what would I want from a framework" reflection sets up Loop 5 directly.

### Loop 4 — Agent state: memory, context, tools

- **Goal.** Make memory, context, and the tool registry first-class manipulable objects. By end of loop, the learner has touched every piece of agent state with their hands.
- **Group.** A.
- **Files.** `agent.py`, `memory.py`, `context.py`, `tools.py`, `BREAK.md`, `WIN.md`.
- **Break.** Starter has all three as plain Python data structures: short-term memory (list of messages), working memory (a dict scratchpad), long-term memory (a JSON file as a key-value store — *no vectors yet*, that's Loop 8). Tool registry is a dict. Starter agent loses information across long conversations. Learner must (a) implement context summarization when chat history exceeds N tokens, (b) add a "remember this" mechanism that writes to long-term memory, (c) make the tool registry mutable mid-conversation.
- **Win.** Learner can:
  - Edit `memory.json` directly and watch the agent's behavior change next turn.
  - Trigger context compaction on demand and verify the agent still has access to summarized state.
  - Add a new tool to the registry mid-session and have the agent use it on the next turn.
  - Remove a tool the agent expected and watch it fail gracefully (or not — that's a discussion).
  - **Persist memory across sessions.** Stop the script, restart it, watch the agent remember the previous conversation by loading `memory.json` on boot. Trivial change, but a big mental-model unlock — agent state isn't tied to process lifetime.
- **Time.** 4–6 hours.
- **Topics.** `L0 S4` (context), `L0 S8` (memory, retrieval, state — the framing version, no vectors), `L3 S1` (memory architecture), `L4 S4` (meta tooling — partial).
- **Key beats.**
  - This loop earns its name. The mental model — *"an agent is a loop with manipulable memory, context, and tools"* — is the foundation everything else hangs off.
  - Explicitly preview Loop 8: *"long-term memory as a key-value store works for ~100 entries. We'll see what breaks at scale and how vectors fix it."*

### Loop 5 — LangChain

- **Goal.** Re-implement the agent from Loops 1–4 in LangChain. See what the framework wraps and what it hides.
- **Group.** B (switch venv).
- **Files.** `langchain_agent.py`, `prompts/`, `BREAK.md`, `WIN.md`.
- **Break.** Starter is a LangChain skeleton with TODOs. Learner must wire up `ChatGoogleGenerativeAI`, prompt templates, a chain, a tool, and the equivalent of Loop 4's memory.
- **Win.** A working LangChain agent that mirrors Loop 3's ReAct + Loop 4's memory + Loop 2's tools, using LangChain's chains, prompt templates, tool decorators, and `ConversationBufferMemory` (or successor). Learner can map each LangChain abstraction back to the plain-Python equivalent from Loops 1–4. Writes a comparison table: *"this code is shorter, this code is now opaque, this is what I'd debug next."*
- **Time.** 5–6 hours.
- **Topics.** `L1 S6` (prompt engineering for production), `L2 S6` (agent architectures — LangChain ReAct), `L3 S1` (memory abstractions in LC), `L4 S5` (protocols and standards — MCP).
- **Key beats.**
  - The compare-to-Loop-4 reflection is mandatory, not optional. Skipping it produces cargo-cult LangChain users.
  - Note explicitly: *"LangChain's API churns. The version you're on is pinned in `uv.lock`. Don't `pip install -U` mid-loop."*
  - **MCP (Model Context Protocol).** After the agent works, swap one hand-built tool for a community MCP server (`mcp` Python SDK + a public server like `filesystem` or `fetch`). Agent now calls the MCP server as its tool source. Discuss why this exists — Anthropic, GitHub, Cursor, Claude Desktop all consume MCP servers as their tool layer; it's table-stakes for AI Engineer roles in 2026. The lesson: tools don't have to live in your codebase; protocols decouple tool authoring from agent authoring.

### Loop 6 — LangGraph

- **Goal.** Re-express the agent as a graph. See where graphs earn their keep over chains.
- **Group.** B.
- **Files.** `graph_agent.py`, `state.py`, `BREAK.md`, `WIN.md`.
- **Break.** Starter has the LangChain agent from Loop 5 reframed as nodes + edges + state. Adds a requirement that breaks chains: a conditional path (route to different tools based on classification) and a parallel branch (call two retrieval strategies, merge results).
- **Win.** A working LangGraph agent with: at least one conditional edge, at least one parallel branch, and a state object the learner can inspect at every node. Learner writes when graphs are worth it vs when they're overkill.
- **Time.** 3–4 hours.
- **Topics.** `L2 S2` (planning and decomposition), `L2 S6` (architectures — graph-based), `L5 S2` (orchestration patterns — preview).
- **Key beats.**
  - State inspection is the load-bearing skill. The graph's value is *visibility*; if the learner doesn't use it, they don't get the lesson.
  - Build the same agent as a chain *and* a graph in parallel. Compare LOC, debuggability, complexity.

### Loop 7a — Single-agent architectures

- **Goal.** Build the single-agent reflection patterns that turn one agent into a more reliable agent.
- **Group.** B.
- **Files.** `reflexion.py`, `planner_executor.py`, `self_consistency.py`, `BREAK.md`, `WIN.md`.
- **Break.** Three starter files, each implementing one architecture as a thin LangGraph variant on Loop 6. Each starter has a known failure mode the learner must diagnose.
  - **Reflexion:** agent self-critiques but loops forever (no convergence criterion).
  - **Planner-executor:** plan is unrealistic; executor fails halfway; no replanning.
  - **Self-consistency:** N samples are taken but voting is naive (string match).
- **Win.** All three architectures running on a benchmark task (e.g. solving 10 word problems). Learner produces a comparison: accuracy, cost, latency, failure-mode profile.
- **Time.** 5–7 hours.
- **Topics.** `L2 S3` (reasoning patterns), `L2 S4` (reflection and self-correction), `L2 S6` (architectures).
- **Key beats.**
  - Cost and latency tracking is mandatory. Reflexion ~3x cost; self-consistency ~Nx cost. Quantify it.
  - **Benchmark continuity.** The starter ships `benchmark.py` with N tasks (e.g. 20 word problems with known answers). This file is reused as-is in Loop 7b (compare multi-agent on the same tasks) and expanded in Loop 9 (becomes the eval harness with LLM-as-judge layered on). The learner builds *one* benchmark across three loops — that's the whole point of putting the eval discipline in early.

### Loop 7b — Multi-agent architectures

- **Goal.** Build hierarchical and orchestrator-worker patterns. *Then* learn when not to.
- **Group.** B.
- **Files.** `hierarchical.py`, `orchestrator.py`, `peer.py`, `MULTIAGENT_TRAP.md`, `BREAK.md`, `WIN.md`.
- **Break.** Three multi-agent starters. Each has the same task as Loop 7a (the word problems). Learner builds them and compares to Loop 7a's single-agent results.
- **Anti-pattern beat (mandatory, mid-loop).** After hierarchical and orchestrator are working, the tutor opens `MULTIAGENT_TRAP.md` and walks through *"is this just one agent with bad prompts wearing a costume?"* — a checklist of failure modes (information bottleneck at the manager, redundant context, cost explosion). Learner reruns one of their multi-agent solutions as a single agent with better prompts and compares.
- **Win.** All three architectures running. Learner writes the *one-sentence test* for when multi-agent is justified for a future project, validated against their own data.
- **Time.** 6–8 hours.
- **Topics.** `L5 S1` (when multi-agent is wrong — the load-bearing section), `L5 S2` (orchestration patterns), `L2 S6` (architectures continued).
- **Key beats.**
  - The anti-pattern beat is non-negotiable. A learner who finishes 7b without it will reach for hierarchy by default for the rest of their career.

### Loop 8 — RAG with vectors

- **Goal.** Build retrieval up from suffering. By end of loop, learner knows when to use sparse, dense, hybrid, and when to abandon RAG entirely.
- **Group.** C (switch venv).
- **Files.** `naive_search.py`, `bm25_search.py`, `dense_search.py`, `hybrid_search.py`, `chunking.py`, `rerank.py`, `corpus/`, `BREAK.md`, `WIN.md`.
- **Break.** A small corpus (~500 docs, e.g. a slice of Wikipedia or a tech blog dump). Starter has naive keyword `grep`. It misses synonyms. Learner walks through:
  1. **BM25 (sparse)** — `rank-bm25` library. Score and rank. Feel why classical IR isn't dead.
  2. **Embeddings (dense)** — Gemini's free embedding model. ChromaDB for the index. Cosine similarity. See where dense beats BM25 (paraphrases, synonyms) and where it loses (exact terms, IDs).
  3. **Hybrid** — RRF (reciprocal rank fusion) of sparse and dense.
  4. **Chunking** — fixed → semantic → hierarchical. Same query, different chunk strategies, see retrieval shift.
  5. **Re-ranking** — cross-encoder pass on the top-K. Cost vs accuracy.
  6. **When to abandon RAG** — long-context vs retrieval tradeoff in 2026. Run the same query with full corpus stuffed into context (if it fits) vs RAG, compare.
- **Win.** Learner has working sparse, dense, and hybrid retrievers, can pick the right one for a given corpus + query type, and has a written rationale for chunking choice.
- **Time.** 8–10 hours.
- **Topics.** `L3 S2` (retrieval fundamentals), `L3 S3` (chunking and indexing), `L3 S4` (RAG architectures), `L3 S5` (knowledge stores).
- **Key beats.**
  - Connect back to Loop 4 explicitly: *"this is the long-term memory from Loop 4, but semantic."*
  - Quantify everything: precision@5, MRR, latency, cost per query. RAG without metrics is theater.
  - **Vector DB production choice.** Loop 8 uses ChromaDB local because it's zero-friction. Wrap-up beat: short trade-off table for production options — pgvector (you already run Postgres), Pinecone (managed, fast, expensive), Weaviate / Qdrant (self-hosted, more features), LanceDB (embedded, columnar). One paragraph each, no code. The lesson: pick by your existing infra, not by Twitter hype.

### Loop 9 — Production reality

- **Goal.** Take the agent from "demo" to "won't page someone at 3am."
- **Group.** D (switch venv).
- **Files.** `caching.py`, `retries.py`, `cost.py`, `evals/`, `injection_guards.py`, `observability.py`, `deploy/`, `BREAK.md`, `WIN.md`.
- **Break.** Starter is the agent from Loop 7a or 8 (learner picks), wrapped in a FastAPI server with no production hardening. Run it under simulated load (`hey` or `locust`); watch it fail in twelve different ways.
- **Win.** Learner adds, in roughly this order:
  - **Caching** — prompt cache + (optional) semantic cache. Measure hit rate.
  - **Retries** — exponential backoff + jitter. Bimodal-latency-aware timeouts.
  - **Cost tracking** — per-call, per-session, running total. Hard token budget that fails loudly.
  - **Eval harness** — the benchmark from Loop 7a, expanded. Offline test set + LLM-as-judge with bias controls (position, verbosity).
  - **Prompt injection guardrails** — input scanner + output scanner + a basic dual-LLM pattern for one risky tool.
  - **Observability** — structured logs with a trace ID per request, span-level timing across the loop.
  - **Streaming with backpressure** — convert the agent's response to streaming. Handle mid-stream cancellation (client disconnect) and partial-response logging. Compare TTFT and total-latency metrics streaming vs blocking.
  - **Async / concurrent calls** — convert blocking LLM calls to `async`. Run two retrieval calls in parallel and merge. Cap concurrency with a semaphore. Discuss when async is worth the complexity (parallel retrieval, fan-out fan-in) vs when it isn't (sequential reasoning chains).
  - **Secrets** — `.env`, `.gitignore`, key rotation note. Never commit keys.
  - **Deploy** — FastAPI + Cloud Run (or equivalent serverless). One-command deploy script.
  - **Monitoring** — latency p50/p99, error rate, cost per request. Alert thresholds.
  - **Rate limiting + graceful degradation** — what happens when the upstream API is down.
  - **Model selection trade-off table.** You've been on Gemini Flash all 8 prior loops. Beat (no code, ~10 min): when Gemini Pro is worth the cost; when Anthropic Sonnet beats Gemini for tool use; when GPT-class models beat both for specific tasks; when a smaller open-weight model is enough. Decision criteria: cost per task, latency p99, tool-call reliability, structured-output reliability, context length needed, vendor lock-in tolerance.
- **Time.** 14–18 hours.
- **Topics.** `L1 S2` (model selection), `L1 S6` (prompt engineering — production), `L4 S1` (tool design — error contracts), `L6 S2` (production hardening), `L6 S3` (caching), `L6 S5` (deployment), `L6 S6` (cost), `L7 S1` (threats), `L7 S2` (defenses), `L8 S1` (eval), `L8 S2` (observability).
- **Key beats.**
  - This loop is dense. The tutor must enforce *one sub-topic per session*, not all in a sprint.
  - Every sub-topic must produce a measurable artifact (a graph, a number, a passing test). No theory-only sessions in Loop 9.

### Loop 10 — Capstone

- **Goal.** Pick a project, ship it, write the README, add evals.
- **Group.** D (same as Loop 9).
- **Files.** Learner-defined.
- **Project options.**
  - **RAG agent** — over a corpus the learner cares about (their notes, their team's docs).
  - **Coding agent** — bounded scope: refactor a single file, write a test for a function. Sandbox the tool surface.
  - **Task agent** — calendar / email / messaging assistant. Mock external APIs first.
  - **Browser agent** — a small Playwright-driven agent that automates one workflow.
  - **Data extraction agent** — structured extraction from a messy corpus.
- **Win.** Working agent + README + at least 20 eval examples + a deployed instance the tutor can hit. Learner writes a postmortem covering: what they over-engineered, what they cut, what they'd do differently.
- **Time.** 20–40 hours, depending on scope.
- **Topics.** All. The capstone is integrative.
- **Key beats.**
  - Scope cut is the lesson. The tutor pushes back on every "and also" the learner adds.
  - The postmortem is non-negotiable. It's where the curriculum becomes durable.

---

## Skip mechanism

The override map gains four commands when `orientation = builder_first`. They're additions, not replacements — the existing override map (Step 1c of SKILL.md) still applies.

| Command | Behavior |
|---|---|
| `/loop list` | Print all 10 loops with status: `not_started` / `current` / `done` / `skipped` / `quickpassed`. One-line description per loop. |
| `/loop [n]` | Jump directly to loop N. If prerequisites aren't done, warn and list the missing prereqs (see dependency map below), but honor the override if the learner confirms. |
| `/loop skip` | Skip the current loop. Tutor offers a 30-second summary of what's in the skipped loop, then marks it `skipped` and moves to the next. |
| `/loop quickpass` | Read the loop's notes/cheatsheet + answer 3 quiz questions sourced from the loop's WIN criteria. If pass, mark `done` with `quickpass: true`. If miss, run the loop normally. The "prove you know it" path. |

### Loop dependency map (for spiral-back)

When a learner skipped a loop and a later loop references it, the tutor offers an inline 2-minute refresher rather than silently assuming the prereq:

| Later loop | Depends on | What's referenced |
|---|---|---|
| Loop 4 | Loops 1, 2, 3 | Loop, tools, ReAct mechanics |
| Loop 5 | Loop 4 | Memory/context/tools as concepts to map onto LangChain |
| Loop 6 | Loop 5 | LangChain primitives reframed as nodes |
| Loop 7a | Loop 6 | LangGraph state for reflection patterns |
| Loop 7b | Loop 7a | Reflection as the precursor to multi-agent justification |
| Loop 8 | Loop 4 | Long-term memory as the concept; vectors as the implementation |
| Loop 9 | Loops 7 and 8 | Has an agent worth hardening |
| Loop 10 | Loop 9 | Has a deployable shape |

The refresher is a 2-minute teach, not a re-run of the loop. If the learner needs more, they unskip the prereq.

---

## What builder-first does NOT cover

By design — these go to the L0→L8 walk for a foundations-first learner, or to a dedicated detour:

- **L1 S1** (model internals — KV cache mechanics) beyond *"it exists, here's why long context is expensive."*
- **L1 S7** (reasoning models internals).
- **L1 S8 / L6 S8** (fine-tuning).
- **L2 S5** (metacognition).
- **L5 S3** (deep coordination mechanics).
- **L5 S4** (framework-comparison deep-dive — LangChain/LangGraph are taught directly; AutoGen, CrewAI, smolagents are skipped).
- **L7 S3** (governance / EU AI Act / compliance).
- **L7 S4** (privacy law).
- **L8 S4** (CI/CD specifics for AI).
- **L8 S5** (perf engineering at the inference-server layer).

When a learner asks about one of these mid-builder-first, the tutor: (a) gives a 2-minute pointer answer, (b) notes it's outside the builder-first scope, (c) offers to switch to foundations-first or a detour if the learner wants depth.

---

## Maintenance

Builder-first depends on real package versions. The skill author (not the learner) refreshes:

1. Every 6 months: re-run `uv sync` against latest pins for each group, validate every loop's BREAK and WIN against the new versions, update `uv.lock` files, bump `setup/LOOP_VERSIONS.md`.
2. When LangChain ships a major (0.3 → 0.4 etc.): patch Loop 5/6/7. These churn fastest.
3. When Gemini SDK changes: patch Group A and the `llm.py` wrapper. Has happened once already.

If maintenance lapses, the `LOOP_VERSIONS.md` warning kicks in at first activation and the learner gets honest framing: *"these pins are from <date>, calibrated for those versions. The lessons still teach the right concepts; the framework syntax may have moved."*

---

## Cross-platform notes

- **macOS / Linux.** Primary supported. `setup.sh` for installs. `source .venv/bin/activate`.
- **Windows.** Secondary. `setup.ps1` for installs. `.venv\Scripts\activate`. WSL2 is an acceptable fallback if a learner hits Windows-specific issues with any group's deps.
- **Cloud shells** (GitHub Codespaces, Replit, etc.). Loops 1–7 work. Loop 9's deploy step assumes shell access to a cloud provider; cloud shells often have one ready. Document the deviation in the loop if needed.

---

## Implementation status (as of 2026-05-07)

This document is the **design**. The implementation lives under `assets/builder-first/`. Status:

**Shipped (Loop 1 + Group A foundation):**
- [x] `assets/builder-first/.env.example`
- [x] `assets/builder-first/setup/README.md` — combined uv install + Gemini key + sanity check flow
- [x] `assets/builder-first/setup/sanity_check.py`
- [x] `assets/builder-first/exercises/group-A/pyproject.toml`
- [x] `assets/builder-first/exercises/group-A/uv.lock` (re-locked 2026-05-07 post-drift-pass against `requires-python = ">=3.11,<3.14"`; 27 packages)
- [x] `assets/builder-first/exercises/group-B/pyproject.toml`
- [x] `assets/builder-first/exercises/group-B/uv.lock` (re-locked 2026-05-07 post-drift-pass; `langchain 0.3.29`, `langchain-google-genai 2.1.12`, `langgraph 0.4.10`, `mcp 1.27.0`, `langchain-mcp-adapters 0.1.14` (downgraded from 0.2.0 — 0.2+ requires `langchain-core 0.4+`), `grandalf 0.8` (added so `langgraph.compiled.get_graph().draw_ascii()` works); 75 packages total)
- [x] `assets/builder-first/exercises/group-B/loop-5-langchain/{langchain_agent.py, mcp_server.py, prompts/system.txt, BREAK.md, WIN.md, NOTES.md, CHEATSHEET.md, quickpass.json}`
- [x] `assets/builder-first/exercises/group-B/loop-6-langgraph/{graph_agent.py, state.py, BREAK.md, WIN.md, NOTES.md, CHEATSHEET.md, quickpass.json}`
- [x] `assets/builder-first/exercises/group-B/loop-7a-single-agent-arch/{benchmark.py, baseline.py, reflexion.py, planner_executor.py, self_consistency.py, BREAK.md, WIN.md, NOTES.md, CHEATSHEET.md, quickpass.json}`
- [x] `assets/builder-first/exercises/group-B/loop-7b-multi-agent-arch/{benchmark.py, hierarchical.py, orchestrator.py, peer.py, MULTIAGENT_TRAP.md, BREAK.md, WIN.md, NOTES.md, CHEATSHEET.md, quickpass.json}`
- [x] `assets/builder-first/exercises/group-C/pyproject.toml`
- [x] `assets/builder-first/exercises/group-C/uv.lock` (re-locked 2026-05-07 post-drift-pass against `>=3.11,<3.14`; `chromadb 1.5.9`, `rank-bm25 0.2.2`, `sentence-transformers 5.4.1`, `torch 2.11.0`; 120 packages total — first `uv sync` is heavy, ~2GB torch download)
- [x] `assets/builder-first/exercises/group-C/loop-8-rag-vectors/{corpus.json, queries.json, eval.py, naive_search.py, BREAK.md, WIN.md, NOTES.md, CHEATSHEET.md, quickpass.json}` (learner creates `bm25_search.py`, `dense_search.py`, `hybrid_search.py`, `chunking.py`, `rerank.py` across stages)
- [x] `assets/builder-first/exercises/group-D/pyproject.toml`
- [x] `assets/builder-first/exercises/group-D/uv.lock` (re-locked 2026-05-07 post-drift-pass against `>=3.11,<3.14`; `fastapi 0.136.1`, `uvicorn 0.46.0`, `httpx 0.28.1`, `prometheus-client 0.25.0`; 34 packages total)
- [x] `assets/builder-first/exercises/group-D/loop-9-production/{agent.py, app.py, load_test.py, evals/cases.json, evals/run_offline.py, Dockerfile, .dockerignore, BREAK.md, WIN.md, NOTES.md, CHEATSHEET.md, quickpass.json}` (learner creates `caching.py`, `retries.py`, `cost.py`, `injection_guards.py`, `observability.py`, plus modifications to `app.py` and `agent.py` for streaming/async, plus a deploy script)
- [x] `assets/builder-first/exercises/group-D/loop-10-capstone/{PROJECTS.md, BREAK.md, WIN.md, README_TEMPLATE.md, POSTMORTEM_TEMPLATE.md, evals/cases.template.json, NOTES.md, CHEATSHEET.md, quickpass.json}` (learner-defined project: pick from 5 options, ship it, postmortem mandatory)
- [x] `assets/builder-first/exercises/group-A/loop-1-bare-loop/agent.py`
- [x] `assets/builder-first/exercises/group-A/loop-1-bare-loop/BREAK.md`
- [x] `assets/builder-first/exercises/group-A/loop-1-bare-loop/WIN.md`
- [x] `assets/builder-first/exercises/group-A/loop-1-bare-loop/NOTES.md` (learner-fill skeleton)
- [x] `assets/builder-first/exercises/group-A/loop-1-bare-loop/CHEATSHEET.md` (learner-fill skeleton)
- [x] `assets/builder-first/exercises/group-A/loop-1-bare-loop/quickpass.json`
- [x] `assets/builder-first/exercises/group-A/loop-2-tools-by-hand/{agent.py, tools.py, BREAK.md, WIN.md, NOTES.md, CHEATSHEET.md, quickpass.json}`
- [x] `assets/builder-first/exercises/group-A/loop-3-react-by-hand/{react_agent.py, tools.py, traces.py, BREAK.md, WIN.md, NOTES.md, CHEATSHEET.md, quickpass.json}`
- [x] `assets/builder-first/exercises/group-A/loop-4-agent-state/{agent.py, memory.py, context.py, tools.py, memory.json, BREAK.md, WIN.md, NOTES.md, CHEATSHEET.md, quickpass.json}`

**Drift-pass results (2026-05-07):**

A one-time SDK-import-and-attribute drift pass was run against fresh `uv sync` venvs for all four groups.

- **Group A** (Python 3.13, after re-lock): 14/14 SDK surface checks pass. All 4 loops' starters import cleanly (Loop 1 makes a module-level API call, fails on dummy key by design — runs correctly with a real key).
- **Group B** (Python 3.13): post-fix, 26/26 SDK surface + 13/13 starter imports pass. Three real issues caught and fixed: (1) Python 3.14 incompatible with LangChain 0.3.x's Pydantic typing; constrained all groups to `<3.14`. (2) `langchain-mcp-adapters 0.2.0` requires `langchain-core 0.4+`; downgraded to `0.1.14`. (3) `langgraph.compiled.get_graph().draw_ascii()` needs `grandalf`; added.
- **Group C** (Python 3.13): 8/8 SDK surface + 2/2 starter imports pass. Verified: `chromadb` Client + add + query roundtrip, `rank_bm25.BM25Okapi.get_scores`, `sentence_transformers.CrossEncoder`, `genai.Client.models.embed_content`.
- **Group D** (Python 3.13): 10/10 SDK surface + 4/4 starter imports pass.

**Real-learner footgun caught and fixed (Group B):** `ChatGoogleGenerativeAI` reads `GOOGLE_API_KEY`, not `GEMINI_API_KEY`. Without intervention, learners following `setup/README.md` (which only sets `GEMINI_API_KEY`) would hit `DefaultCredentialsError` at Loop 5. Patched all 9 LangChain starter files to alias `GOOGLE_API_KEY` from `GEMINI_API_KEY` at module top with explanatory comment.

**Pending — concrete deliverables:**

- [ ] **Detours catalog + `/path` command.** `references/detours.md` with 12-15 named paths (`rag-agent`, `coding-agent`, `interview-prep`, `mcp-server`, `evals-deep-dive`, `prompt-injection-redteam`, `multi-agent`, `cost-optimization`, `observability`, `fine-tuning-domain`, `voice-agent`, `browser-agent`, `data-extraction-agent`). Each: ordered layer-section sequence, what to skip, exit criteria. Wired through `/path [name]` in SKILL.md's override map. Originally in the user's 6-point list as item 3; deferred during the loop build.
- [x] **HTML viewer for notes / cheatsheets / flashcards** — *shipped 2026-05-08*. `assets/index.html` + `assets/manifest.json`, copied to workspace at first-time onboarding. Single-file viewer (vanilla JS + marked@12 from jsdelivr CDN), served via `python -m http.server` from the workspace. Three tabs: Notes (markdown render), Cheatsheets (markdown render), Flashcards (click-to-flip + Space/←/→ keyboard). Reads `manifest.json` for content discovery; tutor appends entries when notes / cheatsheets / flashcard decks are generated. Smoke-tested end-to-end against a populated test workspace: all paths (manifest, markdown, flashcard JSON) serve correctly. Browser-side JS rendering validated by inspection only — first real-learner walkthrough should confirm visual presentation. Supports legacy flashcard formats (front/back, q/a, q/answer_outline) so existing `quickpass.json` files render directly.
- [x] **Slash-command surfacing at first-time onboarding** — *shipped 2026-05-08*. `assets/COMMANDS.md` now ships and gets copied to `~/ai-systems/COMMANDS.md` at first-time onboarding (SKILL.md Step 1 sub-step 6). After workspace setup, the tutor announces the commands as a one-paragraph briefing (slash + natural-language overrides + pointer to the full file). Warm Resume on a 14+ day gap also adds a one-line reminder. Originally in the user's 6-point list as item 1.
- [ ] `setup/LOOP_VERSIONS.md` — version manifest with the 6-month refresh cadence. Cheap (~15 min) — already referenced by builder-first.md but not written.
- [ ] `setup/llm.py` — optional model-agnostic wrapper. Introduce in Loop 2 if a learner asks for it; not strictly needed since each loop uses its provider directly.

**Pending — quality concerns (not blocking, worth knowing):**

- Drift pass tested imports + SDK surface, not runtime behavior. Loop 9's streaming + tool-calls combo is specifically called out in BREAK.md as awkward; first to break in real use.
- Cost projections in Loop 9's NOTES.md template assume Gemini Flash pricing as of 2026-05. Stale within months — needs refresh during the 6-month maintenance pass.
- Stretch suggestions occasionally reference out-of-deps packages (Loop 6's checkpointer, Loop 8's pgvector, contextual retrieval, late chunking). Learners pursuing stretch will need to `uv add` themselves.
- Cross-platform (Windows) untested. Bash + Unix-style commands throughout setup/README.md and the BREAK.md files. PowerShell users will adapt but it's a friction point.

**Pending — the big one:**

- [ ] **Validate the full curriculum (Loops 1–10) end-to-end with a real learner.** Runtime correctness on actual API calls + the prompt-format / eval-scorer edge cases / Loop-9 streaming-vs-tools issue / per-loop time-on-task and stuck-points. Only a real walkthrough catches these.
