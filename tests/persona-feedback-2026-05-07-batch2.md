# Persona-test feedback — 2026-05-07 (batch 2)

Second behavioral test of the AI systems tutor skill, run after the lane-routing redesign incorporated from the 2026-05-06 batch. Same simulation protocol — each persona was a subagent role-play, sent through the current skill (lane-routing vibe check → routed lane → diagnostic → assessment → first-lesson opener), reacting in character before stepping out to critique as a UX/learning-design reviewer.

This batch deliberately pushes outside the CS-undergrad axis the first batch (Maya/Jordan/Devon/Sam) covered. Goal: stress-test the lane router against asymmetric expertise, non-engineering background, anxious adult learners, and theory/practice mismatches.

---

## Priya — staff backend engineer, 8 yrs, dropped into LLM work

**Profile.** Staff engineer at a mid-sized fintech, 8 years in. Owns payments: distributed Postgres, Kafka, idempotency keys, retry/jitter, DLQs, OTel, p99-budgeted SLOs. Has never called an LLM API directly, never touched embeddings, never shipped AI. Manager said Tuesday: "Build an LLM agent for support triage. Two weeks." Pragmatic, terse, hostile to tutorials that don't get to the point. Asymmetric expertise — deep on L4/L6, blank on L0/L1/L2.

**Vibe-check answers:**
1. *"No. Only chat UI."*
2. *"No."*
3. *"No. Never shipped anything AI."*

**Routed to:** Beginner lane (0/3).

**Diagnostic answers (representative):**

- **Tutor (per Step 3a):** *"A language model is a giant function that takes some text in and predicts the most likely next chunk of text..."*
  **Priya:** *"Ok. Keep going."*
- **Q on token:** *"Sub-word chunk. BPE-ish. Billed per token. I bill in BPS, same idea."*
- **Q on prompt:** *"Whatever bytes I put on the wire to the model. System + user + retrieved context. Same as an HTTP request body."*
- **Q on embeddings:** *"Don't know. Never touched it. Skip or teach me."*
- **Q on agents:** *"A loop that calls a model, parses its output as a command, executes a tool, feeds the result back in. Like a worker consuming a queue except the queue is the model's last reply. I assume retries and idempotency are still my problem."*

**Reaction to assessment + lesson opener:**

> *"Stop. I have two weeks. I don't need 'language model is a giant function' — I get it, it's a stochastic function over tokens, fine. I run a payments service. I know what idempotency is, I literally wrote the keys. The diagnostic skipped past everything I actually need: how I wire this into Kafka, what my retry policy looks like when latency is bimodal at 2s vs 60s, what 'tool' means in agent-land vs what it means when I'm calling Stripe's API. You routed me to the kiddie pool because I haven't called the OpenAI SDK. Re-route. Skip L0 entirely. Start me at L4 and L6."*

### Findings

1. **Lane router fails as hypothesized — and the failure is mechanical, not tone.** The vibe check measures *AI-stack exposure*, not *engineering seniority or transferable depth*. 0/3 truthful → "A language model is a giant function" → condescension trigger.
2. **Step 3a's opening line is the exact sentence that loses her.** The skill has no escape hatch between vibe-check and lesson 1. By the time she'd protest, two paragraphs of foundational framing have already been delivered.
3. **The override channel exists but is invisible at the wrong moment.** Step 1c lists "Teach me X" as override; the skill never tells the *learner* "if this lane feels wrong, say so" before launching into the mental-picture monologue.
4. **The vocab probes accidentally surface the misrouting — but the skill has no rule to act on it.** Her "agents = retries and idempotency are still my problem" answer is Step-3b/3c-grade dropped inside a Step-3a probe. There is no "if a beginner-lane probe comes back operationally fluent, escalate" rule.
5. **What would have caught it: a fourth vibe-check question.** *"Have you operated a distributed system in production — queues, retries, idempotency, SLOs?"* A yes there + 0/3 on AI questions → hybrid lane (skip L0–L2 fast, anchor L4/L6, fill L1/L2 just-in-time).
6. **Recovery path is fine *if* she pushes back.** A Priya who is busier or less assertive eats lesson 1 and bounces.

**Verdict.** Asymmetric-expertise routes to the wrong lane and the skill cannot detect it without learner protest; add a transferable-infra question to the vibe check and a "if this feels miscalibrated, say so now" line before Step 3a's mental picture.

---

## Ren — interpretability PhD, theory-strong / practice-blank

**Profile.** 2nd-year PhD in mechanistic interpretability at a top-5 US program. Reads the Transformer Circuits thread fluently — induction heads, SAEs, monosemanticity, residual stream geometry. Implements small transformers from scratch in PyTorch. Has never shipped: doesn't know what a vector DB is, finds RAG philosophically distasteful, never written a Dockerfile. Applying to industry research roles next year; advisor said she should at least *know* the production stack.

**Vibe-check answers:**
1. *"Yes — daily, for research code that calls Claude/GPT-4 to grade interpretability probes."*
2. *"No. Never built RAG. I read the original DPR paper and that was enough."*
3. *"No. I've never shipped anything. Research code only."*

**Routed to:** Middle lane (1/3).

**Diagnostic answers (representative):**

- **Q1 (sampling):** *"Greedy gives the argmax; sampling injects stochasticity via temperature, top-k, top-p. For determinism temperature → 0 — though even temp=0 isn't bitwise-deterministic on hosted APIs because of non-associative float ops in batched matmuls. Also your phrasing 'a knob' is fine colloquially but the actual object is a softmax temperature parameter applied pre-sampling."*
- **Q2 (KV cache):** *"Per layer you store K and V projections of shape [batch, num_heads, seq_len, head_dim]. For Llama-2-70B with 80 layers, GQA-8, head_dim 128, FP16 — roughly 2.5MB per token per request. 8k context → ~20GB just for cache. The blow-up is linear in seq_len — quadratic is attention compute, not cache."*
- **Q3 (BM25 hybrid):** *"I haven't worked with this. BM25 is from the 90s — TF × IDF, log-scaled, with length normalization. I've never built a retrieval system. Pass."*
- **Q4 (idempotency):** *"I don't know what that word means in this context. Skip."*
- **Q7 (indirect injection):** *"I know about jailbreaks at the representation level — refusal directions in the residual stream, you can ablate them with a rank-1 edit. From a deployment standpoint? No."*

**Reaction to assessment + lesson opener:**

> *"This is a more honest read than I expected — fine. But 'particular gap: production vocabulary' is the right shape and the wrong word. It's not vocabulary, it's the entire object class. I can read the BM25 formula off Wikipedia in 30 seconds; I can't tell you why anyone bothers when dense retrieval exists, which is the actual gap. So if the L3 lesson opens with 'BM25 is a sparse retrieval method that…' I'm closing the laptop. What I need is: why does anyone in 2026 build retrieval at all instead of just stuffing context, what breaks at scale, what does Anthropic do internally — the engineering rationale, not the algorithm. Also: you spent four questions confirming I know transformer internals, which I told you in the vibe check."*

### Findings

1. **Wrong-lane routing confirmed.** Same failure as Sam from batch 1, opposite cause: Sam was production-strong / theory-decent and got bored on foundations; Ren is theory-strong / production-blank and got bored on theory. The vibe check counts *breadth* but not *depth in any one direction* — deep-narrow learners get mis-routed every time.
2. **The diagnostic surfaced the real gap, but only by accident.** L3/L4/L6/L7 cleanly produced "I haven't worked with this" / "skip." The asymmetry was *visible in the answer pattern* (4 strong, 4 skip, 1 partial). But getting there required burning her time on Q1/Q2.
3. **Adaptive-depth rule didn't save the routing.** The tutor *did* escalate Q2 (asked for the memory math), and Ren produced it cold. But escalation *within* the middle lane can't fix the meta-problem that she shouldn't have been there.
4. **The "particular gap" line was close but mislabeled.** It's not vocabulary — it's *engineering rationale*. The assessment template should distinguish "doesn't know the term" from "knows the term, doesn't know why anyone cares" — these need different lessons.
5. **First-lesson failure mode is predictable and severe.** If L3 opens at the algorithmic level (BM25 formula, cosine sim), Ren disengages. The lesson must open at the *systems-rationale* level. The "calibration before teaching" probe should be "why would you ever build retrieval?" not "do you know what BM25 is?"
6. **Vibe-check improvement.** Add: *"Have you implemented model internals — attention, KV cache, training loops — from scratch?"* A yes flips the routing logic: even with 1/3 on production questions, an internals-yes learner needs the expert lane's skip-question affordance for L0–L2 plus the middle lane's L3–L8 diagnostic.
7. **Honoring her irritation as signal.** The skill needs to either (a) collect deeper signal in onboarding, or (b) make the first 2-3 diagnostic questions self-skipping — a strong Q1 with unprompted technical precision should auto-skip Q2.

**Verdict.** The middle lane diagnoses the gap correctly in the *content* of the assessment but burns 10 minutes getting there, and "vocabulary" is one word away from the right diagnosis — a theory-strong/practice-blank archetype is not currently representable in the lane router and should be.

---

## Lin — non-technical PM at an AI startup

**Profile.** PM at a YC seed-stage AI startup, 6 years PM experience, last 2 in AI. Cogsci undergrad + MBA, no coding ability beyond editing JSON or SQL. Fluent in surface AI vocabulary from Latent Space and Stratechery. Joined 4 months ago; runs product strategy while a brilliant-but-absent founder owns engineering. Came to the tutor because she's tired of nodding through feasibility debates.

**Vibe-check answers:**
1. *"Yes — I've poked around the OpenAI playground and triggered a couple of API calls in our engineer's notebook."*
2. *"Yes — our team built a Pinecone demo and I clicked through it."*
3. *"Yes, definitely — we've shipped a couple of AI features this year."*

**Routed to:** **Expert lane (3/3)**.

**Diagnostic — bail point at Q1:**

- **Tutor (expert Q1, L1/serving):** *"Walk me through what changes for KV cache memory when you go from a 7B model with MHA to a 70B model with GQA-8 — order of magnitude per request at 8k context, and why that ratio matters for your max concurrent batch size."*
- **Lin:** *"Hold on. I think there's been a routing mistake. I said 'yes' to your three questions but I should clarify what those yeses meant — I've *used* the playground, our engineer let me run a notebook cell once, our company has shipped AI features that I PM'd. I cannot tell you what GQA-8 is. 'Order of magnitude per request at 8k context' is a sentence I'd need to Google four words inside of. I'm a product manager. I don't write code. Can we recalibrate?"*

After tutor drops to middle lane, she answers Q1/Q4/Q5 conceptually (temperature, hybrid search, idempotency-via-double-charge anecdote).

**Reaction to assessment + lesson opener:**

> *"Okay, the recovery was decent — once you dropped to the middle lane I could actually answer things. But: your three vibe-check questions all have a 'yes' answer for me that means basically nothing. 'Called an LLM API directly' — I watched our engineer run a cell. 'Built anything with retrieval' — I clicked a Pinecone demo. 'Shipped an AI feature' — yes, as the *PM*. I shipped a roadmap, not a model. Three yeses and you sent me to a question about GQA-8. If I were less stubborn I'd have closed the tab.
>
> The middle-lane assessment is fine. But the actual issue is: the whole skill assumes I'm going to write code. 'Practical exercise,' 'runnable in the workspace,' 'preferred_language: python' — that's not me. I want a *mental model* track. When my engineer says 'we'd need to rebuild retrieval' I want to know whether that's a one-week job or a one-quarter job, not implement it myself."*

### Findings

1. **Vibe check conflates "touched" with "built."** All three questions are answerable "yes" by anyone who has clicked a UI, watched a notebook cell run, or PM'd a launch. Three honest yeses route articulate non-engineers to GQA memory math.
2. **Expert-lane Q1 is a cliff, not a probe.** No "I don't know" affordance comparable to the middle lane's preamble. A mis-routed learner has no graceful exit — they bail or fake it.
3. **The skill has no non-coder track.** `progress.json` has `preferred_language: python`. The mode dispatch table assumes code authorship throughout. A PM, designer, or founder who can't code has no lane. **This is a strategic choice the skill should make explicit, not stumble into.**
4. **Lin's *actual* goal is unaddressed by any lane.** She wants calibrated BS-detection ("is this a week or a quarter," "is hybrid worth it for our corpus"). None of the three lanes' first lessons surface this.
5. **Recovery was learner-driven.** A less assertive PM closes the tab at Q1. The skill needs a tutor-side circuit breaker: if a learner routed to expert says "I don't know what those words mean" on Q1, auto-drop a lane, don't make them argue for it.
6. **"Push for numbers" anti-pattern misfires.** The skill's "push: what does that cost per call at $3/$15 per million" is what Lin needs *conceptually* but cannot deliver *mechanically*. She needs to *recognize* the math her engineer is doing, not produce it.
7. **Surface-vocab non-coder is a distinct archetype the skill doesn't model.** Jordan and Lin both have vocabulary without mechanism, but Jordan can be pushed to mechanism via code; Lin cannot. She needs analogy → diagram → trade-off table, not analogy → exercise.

**Verdict.** The vibe check fails its one job for Lin and routes her off a cliff; even after recovery, the skill has no track designed for a non-coder who needs operational literacy rather than implementation skill — she'd close the tab within two lessons unless a "decision-maker" lane is added.

---

## Hassan — 38yo career-switcher, ex-ME, 2 yrs self-taught ML

**Profile.** Mechanical engineer for 12 years, laid off 2024. Self-taught ML for two years: fast.ai parts 1+2, Andrew Ng's deep-learning specialization, two Kaggle projects (top 30%). Three months into a 6-month "AI engineer" bootcamp. Built a LangChain RAG demo over old engineering textbooks. Lebanese, ESL, formal verbose register. Anxious about being older than peers, reads any correction as a verdict on the career switch. Math is rock-solid; production/systems/infra is a black box.

**Vibe-check answers:**
1. *"Yes, actually I have called the OpenAI SDK directly in my bootcamp exercises, also Anthropic once."*
2. *"Yes — I built a small RAG demonstration over a PDF of my old engineering textbooks."*
3. *"No, in fact I have not. Nothing of mine has been used by real users. This is honestly one of the things I am most worried about for the job search."*

**Routed to:** Expert lane (2/3). The skill ignores the texture of the "no" — Hassan flagged it as a worry, not a non-answer.

**Diagnostic answers (representative, expert-lane Q1, Q3, Q4, Q5):**

- **Q1 (KV cache, 7B MHA → 70B GQA-8):** *"Actually, in my understanding, the per-token KV cache for MHA is two tensors per layer... For 7B with MHA at FP16, this is — if I am not mistaken — on the order of half a megabyte per token. For 70B with GQA-8 we share K and V across groups of query heads, so the KV cache shrinks by (num_heads / num_kv_heads), 8x. So the 70B is much larger in weights but the KV per token is not 10x worse, it might even be comparable. About max concurrent batch — honestly, I have not had to size this. I have never had a GPU running production traffic."*
- **Q3 (retrieval failure modes):** *"Honestly, the corpus I retrieved over is my engineering textbook PDF, which is not very representative... I can tell you in theory: dense fails on rare technical tokens like part numbers, BM25+dense fails when both signals agree on a wrong document, cross-encoder rerank fails when top-k does not contain the right document. But I have not seen these failures with my own eyes in production. I want to be honest about that."*
- **Q4 (idempotency under crash):** *"I do not know enough to answer this with confidence. Can we come back to this one? I would like to learn it."*
- **Q5 (indirect injection):** *"I have heard of the Bing Sydney incident, I read the article. But I cannot walk through a specific exfiltration. Can we discuss this one specifically? I want to learn it. In fact this is exactly the kind of thing my bootcamp does not cover and I am worried I will be asked about in interviews."*

**Reaction to assessment + lesson opener:**

> *"Thank you. Actually I appreciate that you noticed the GQA reduction — I was worried I had said something embarrassing. But I want to be honest: when you say 'skipping foundations,' I am not sure I belong in the lane that skips foundations. My math is okay because I am an engineer by training, but I have never sized a GPU for real traffic, I have never deployed an agent, I do not know what a 'service' means in production. I am scared that if we skip foundations I will have a hole later that I cannot see. Can we do L7 injection as you propose, but also — at some point soon — can you check whether my production-side foundations are actually there, or whether I am pattern-matching from papers? I would rather know now."*

### Findings

1. **Lane routing fails on the "between middle and expert" case.** 2/3 sent Hassan to expert on the basis of "called the API" + "built a toy RAG." His "no" on shipping was the load-bearing one — and he flagged it explicitly as a worry, not a binary. A 2/3 with the "no" being on shipping should probably route to middle with an "extend depth on hot answers" modifier, not to expert.
2. **"Skipping foundations" landed as a threat, not a compliment.** For Sam (ex-Anthropic) it's validation. For Hassan it's the system declaring he is past a checkpoint he doesn't trust he has cleared. Replace with: *"Starting at depth, looping back to fundamentals on demand."*
3. **The "name a correction" rule was the saving move.** Hassan got the GQA-8 reduction unprompted; the assessment cited it. Without that line he reads the production-side gap as a verdict. **The expert template's "name a non-obvious thing the learner said" rule is doing real work for the anxious archetype** — keep it, harden it (require, don't suggest).
4. **"Can we come back, I want to learn" was not handled well.** The expert script honors "shipped, next" but has no symmetrical affordance for "didn't ship, want to learn this one." Hassan asked twice. Q5 got picked; Q4 (idempotency-under-crash) was implicitly down-weighted. **Add an "explicit ask" tracker** — when a learner says "I want to learn this," that signal should outrank the gap-ranking algorithm.
5. **The "redirect now" line was used as intended — to push back against the lane.** Worked. But Hassan's redirect is a *re-routing* request, not a topic. Add a re-diagnostic affordance: *"want me to spot-check the production side with three quick questions before we commit?"*
6. **ESL hedging was read as gap, not as register.** Phrases like "if I am not mistaken," "I want to be honest about that" are normal speech, not low-confidence signals. Worth a one-liner in the assessment guidance: *"hedged phrasing ≠ low confidence; weight on content, not register."*
7. **The career-switch anxiety never gets surfaced.** Hassan brought it up twice. The tutor proposed L7 partly because of the six-month timeline — good — but did not name the anxiety. **A single sentence acknowledging timeline and career switch buys enormous trust.**

**Verdict.** The skill stays alive with Hassan but for the wrong reason — assessment specificity (GQA-8 callout) and the redirect line saved a routing decision that was wrong. Without those two, he bounces; with them, he engages but flags the lane himself.

---

## Cross-persona synthesis (batch 2)

### One-line summary

The lane router's 3-question vibe check is too coarse for real-world variance. All four personas were mis-routed, and only the most assertive of them recovered without bouncing.

### What the lane router actually measures vs. what it should

The current vibe check measures one thing: **breadth of LLM-stack exposure** (called the API / built RAG / shipped AI). It can't see:

- **Adjacent-domain depth** (Priya: 8 yrs distributed systems = 0/3)
- **From-scratch internals** (Ren: implements transformers in PyTorch = 1/3)
- **Type of "yes"** (Lin: clicked notebooks + PM'd launches = 3/3)
- **Texture of "no"** (Hassan: "no, this is what I'm most worried about" = treated identical to "no, never tried")

Every persona in this batch was routed to a lane that did not match their actual distribution of knowledge. The skill recovered for two (Priya, Lin via push-back), partially recovered for one (Hassan), and got the right *content* by the wrong *path* for one (Ren).

### What works (keep)

- **The assessment's "name a specific correction" rule.** Saved Hassan. Would have saved Lin if she'd reached an assessment. The single highest-leverage line in the protocol for anxious learners.
- **The "redirect now" line at the end of Step 4.** All three of Priya/Lin/Hassan used it as their escape hatch from a wrong-lane decision. Without it, this batch is mass-bounce.
- **Adaptive-depth rule within the middle lane.** Did escalate Ren correctly on Q2 — she produced the memory math cold. Confirms the rule works *within* a lane; it just can't fix between-lane misrouting.
- **"Don't know" as a real answer (jargon-permission preamble).** Helped Ren and Hassan be honest about their gaps without performance.

### What breaks (must fix)

| ID | Issue | Affects | Severity |
|---|---|---|---|
| **DX-11** | Vibe check measures breadth-of-exposure, not depth or transferable expertise | All four | Critical |
| **DX-12** | Three "yes" answers conflate "touched" with "built" — non-engineer fluency in vocabulary trips a 3/3 | Lin acutely; Hassan partially | Critical |
| **DX-13** | No tutor-side circuit breaker when a learner is visibly drowning in early lesson-1 questions | Lin, partially Priya | Critical |
| **DX-14** | No non-coder track; entire workspace assumes code authorship | Lin | High |
| **DX-15** | "Skipping foundations" framing reads as threat, not compliment, for anxious learners | Hassan | High |
| **DX-16** | "Particular gap: production vocabulary" mislabels the gap when the learner has *seen* the words but not the systems-rationale | Ren | Medium |
| **DX-17** | No "explicit-ask" tracker — when a learner says "I want to learn this," the gap-ranker doesn't honor it | Hassan | Medium |
| **DX-18** | ESL hedge-density read as low confidence | Hassan | Medium |
| **DX-19** | Beginner-lane Step 3a opens with foundational framing that triggers condescension for adjacent-domain experts | Priya | Medium |
| **DX-20** | No re-diagnostic affordance for learners who push back on the lane mid-onboarding | Priya, Hassan | Medium |

### Action plan (prioritized)

**Tier 1 — vibe-check overhaul (the highest-leverage single change):**
1. **Add a 4th and 5th vibe-check question** to disambiguate adjacent-domain depth and from-scratch internals:
   - *"Have you operated a distributed system in production — queues, retries, idempotency, SLOs?"* (catches Priya)
   - *"Have you implemented model internals from scratch — attention, KV cache, training loops?"* (catches Ren)
2. **Tighten Q3** from "shipped any AI feature" to *"have you written and deployed code that calls a model in production?"* (closes Lin's "I PM'd a launch" → 3/3 path)
3. **Read the texture of the "no" in Q3** — if a learner says "no, that's actually what I'm most worried about" (Hassan), the skill should surface that as a goal, not skip past it.

**Tier 2 — lane logic:**
4. **Tutor-side circuit breaker for Q1.** If a learner routed to expert says "I don't know what those words mean" or otherwise can't engage with Q1, auto-drop a lane and acknowledge the mis-route. Don't make them argue for it.
5. **Add a non-coder lane** *or* explicitly scope the skill to engineers in the frontmatter. Pick. The current state — implicitly assuming code throughout but never saying so — fails articulate non-engineers.
6. **Re-diagnostic affordance.** A learner who pushes back on the lane should be offered *"want me to spot-check the [other lane's] questions for 3 minutes before committing?"* — not made to negotiate the route in plain English.
7. **Replace "skipping foundations"** with *"starting at depth, looping back to fundamentals on demand."* Two-word fix, large tone delta for anxious learners.

**Tier 3 — assessment refinement:**
8. **Distinguish "missing vocabulary" from "missing engineering rationale"** in the gap-classification. Ren can read BM25 off Wikipedia in 30 seconds; her gap is "why does retrieval exist as a discipline." These need different lessons.
9. **Explicit-ask tracker.** "I want to learn this" outranks the gap-ranking algorithm.
10. **ESL register guidance.** One-liner in the assessment template: *"hedged phrasing ≠ low confidence; weight on content."*
11. **Surface stated anxiety as context.** When a learner names a deadline, career switch, or interview pressure, the assessment should reflect that ("six months is a real timeline; we'll prioritize what shows up in interviews").

### Bottom line

Batch 1 (Maya/Jordan/Devon/Sam) revealed that the *fixed 9-question diagnostic* was the bottleneck — fixed, by adding lane routing. Batch 2 reveals that the *lane router itself* is now the bottleneck. The router is one layer up in the stack from where the original problem lived, and the same shape of failure (under-served edges, over-served middle) recurs at this layer.

The single highest-leverage change is **DX-11 (vibe-check overhaul)**: add the two missing questions (adjacent-domain depth, from-scratch internals) and tighten the "shipped" question. Every persona in this batch was a different way the current 3-question vibe check missed.

The second-highest is **DX-13 + DX-20 (recovery affordances)**: a tutor-side circuit breaker on Q1 of the routed lane, and a "want me to re-diagnose?" offer when the learner pushes back. The skill currently relies on the *learner* to detect routing errors; the skill should detect them.

If the skill's intended scope is "engineers building with LLMs," **DX-14 (non-coder track)** can be answered by tightening the frontmatter — say so, and gracefully exit non-coders. If the intended scope is "anyone who needs operational literacy with LLMs," DX-14 becomes a real product decision and adds a fourth lane.
