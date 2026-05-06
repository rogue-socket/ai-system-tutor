# Persona-test feedback — 2026-05-06

Behavioral test of the AI systems tutor skill against four simulated learner personas (1st–4th year CS undergrads with varying intelligence and interest profiles). Each persona was a subagent role-play. Each was sent the same 10-message tutor sequence: workspace setup, 9-question diagnostic (one per layer L0–L8), then assessment + first-lesson opener with two calibration questions. After reacting in character, each persona stepped out and critiqued the experience as a UX/learning-design reviewer.

---

## Maya — 1st-year, vague-curious, true beginner

**Profile.** First-year CS, finished intro Python, currently in data structures. Saw a "how ChatGPT works" guest lecture and left confused. Used ChatGPT as smart autocomplete. Vague goal: build a "study buddy bot." Casual writing, easily overwhelmed, ~30-min attention span.

**Diagnostic answers (representative):**
- Q1: *"its because the model is like.. random? idk what knob tho. is there a randomness slider somewhere?"*
- Q2: *"wait what is KV cache 😅 like key-value? sorry this one i dont really know"*
- Q3: *"is that like react.js?? lol probably not."*
- Q4: *"BM25 idk what that is. skip i got nothing"*
- Q8: *"this one is a LOT of words. data plane vs control plane sounds like networking class which i havent taken. im lost"*

**Reaction to assessment + lesson opener:**
> "'below intermediate' stings a little but i guess yeah that tracks lol. but also.. more questions?? i thought we were starting the lesson... can we do an actual explanation next pls. my brain is tired"

### Findings
1. **Diagnostic mis-calibrated for true beginners.** Realistic quit point in the wild: **Q3 or Q4**.
2. **Assessment tone is honest-crushing.** "Calibrated for intermediate, your answers are below that" reads as a graded test.
3. **First lesson opener feels like the diagnostic continuing.** Two more questions before any teaching, after 9 of feeling dumb.
4. **"SR items" undefined** — sounds like homework piling up.
5. **Verdict.** Not for 1st-year today. Skill works as designed (says "intermediate"), but no on-ramp for true beginners.

---

## Jordan — 2nd-year, average, "I built a chatbot"

**Profile.** 2nd-year CS sophomore. B+ in intro ML. Built one Flask + OpenAI chatbot, got an A. Knows the words: tokens, embeddings, RAG, fine-tuning. Doesn't know mechanics. Confident-but-shallow personality, will BS plausible answers, joined the AI club to "build something cool."

**Diagnostic answers (representative):**
- Q1 (temperature): *"Oh yeah, that's temperature... turn it down to 0 and then it's deterministic. That's basically it."* — clean
- Q2 (KV cache): *"K and V, that's like keys and values from attention right? I'm pretty sure it's quadratic actually because attention is quadratic."* — confused KV cache scaling with attention compute
- Q4 (hybrid): *"Like searching code or product SKUs maybe. If someone searches 'error E1234'..."* — solid concrete answer
- Q5 (idempotency): *"Like sending a payment — definitely needs idempotency, you don't want to charge someone twice."* — correct
- Q6 (multi-agent): *"Honestly not sure, I've heard of CrewAI but never used it."* — acknowledges limit
- Q9 (judge bias): named position + verbosity, gave detection methods — *"the best answer of the set"* per the assessment

**Reaction to assessment + lesson opener:**
> "Q2 — 7B params, that's like 14GB at fp16? KV cache for 2500 tokens... want to say smaller than model weights but I genuinely don't know... I'll commit to: KV cache is smaller than model weights, but not as small as I'd guess — maybe within an order of magnitude? That's my answer and I'm sticking to it until you tell me I'm wrong."

### Findings
1. **Calibration mostly right.** Q1, Q4, Q5, Q9 were in the zone. Q2 and Q7 a half-step too deep. **Q8 (data/control plane) was the worst-calibrated** — required a frame Jordan didn't have, so he just guessed from networking.
2. **Specificity of the assessment is the killer feature.** Calling out "you confused KV cache scaling with attention compute" is the kind of correction that engages a confident-but-shallow learner. Without the "you have surface vocab further than most" opener buying credit, three corrections in a row would read as a takedown.
3. **Starting point (L1) was right, but justification matters more than level.** "Your L1 gap is upstream of your L6/L7 confusion" reframes it as unblocking, not remediation.
4. **Specific jargon traps for Jordan:** "prefill," "speculative decoding," "continuous batching," "MoE," "KV cache quantization." Jordan will nod through these without flagging — he won't ask. Tutor needs forced check-ins ("in your own words, what's prefill?").
5. **Stickiness contract:** the diagnostic sets a "let me poke your mental model until it breaks" cadence. If subsequent lessons revert to topic-by-topic explanation, Jordan drifts back to confident-shallow. **The diagnostic sets a contract — keep it or lose him.**
6. **Verdict.** Yes, this serves the "built a chatbot, now what?" segment well. The diagnosis (missing mechanics underneath the vocabulary he has) is correct and would be missed by a generic intermediate-slot.

---

## Devon — 3rd-year, smart, NLP thesis-track

**Profile.** 3rd-year CS junior. Senior thesis on retrieval-augmented QA for biomedical literature. Has read RAG paper, ReAct, parts of "Attention Is All You Need." Built a working single-hop RAG with sentence-transformers + ChromaDB + an eval set. Pushes back on hand-waves. Going to grad school in NLP/IR.

**Diagnostic answers (representative):**
- Q1: *"sampling. temperature scales the logits before the softmax... I've noticed even temp=0 isn't fully reproducible across calls on hosted APIs — I think it's because of batching nondeterminism on the GPU"* — sophisticated, self-corrects
- Q4: gave a concrete biomedical example with `BRCA1`, `pembrolizumab` and explained why dense smears rare tokens
- Q6: *"a lot of 'multi-agent' setups are one model called multiple times with different system prompts, passing strings to each other... I'd want to see an ablation: does removing the second agent measurably hurt? If not, it was prompt theater."*
- Q8: walked through `fetch_url` + `email` exfil, named control-plane vs data-plane fusion as the structural problem
- Q9: named position bias + verbosity bias with detection protocols (order-swap, length regression)

**Reaction to assessment + lesson opener:**
> "I appreciate that the assessment named things I actually got wrong rather than just saying 'good job.' The KV cache callout is fair; I was bluffing and you saw it. The ReAct one stings a little because I think I was closer than you're crediting, but 'observation pollution' is a cleaner name than 'error compounding' so fine... calibration before explanation is the right move. I've had advisors who explain for 20 minutes and *then* ask if I followed, and by then I've nodded my way past the actual confusion."

Devon then attempted the KV-cache memory math (Llama-2-70B, 80 layers, 8 KV heads via GQA → ~2.6 GB per request) and the prefill/decode/memory scaling question correctly. *"I'm probably off by a factor of 2 somewhere. Tell me where."*

### Findings
1. **Diagnostic under-probes a stronger learner.** Devon clearly above the median this protocol seems written for. Fixed 9-question script means a strong learner spends 15 minutes proving they know things instead of being stress-tested at the boundary of what they know.
2. **Assessment was mostly precise but generic on strengths.** Naming the missing memory math (Q2) was actionable. *"You're guessing where you should have a model"* (Q3) and *"you've heard the words, you don't have the reflexes"* (Q7) are the best lines — they distinguish vocabulary from operational knowledge, the whole game for an academic-strong, industry-naive learner. **Strengths section was generic** ("you have real grounding in retrieval"). Should be as specific as gaps.
3. **The skip was correct and well-justified.** Going to KV-cache first (deepest gap, sits under cost/latency/context budgeting) instead of re-teaching L0 sampling was the right call. **One concern:** jumping straight without first asking *what Devon wants for the thesis* misses adult-learner sequencing. Better move: "here's where I'd start, here's why — does that match what your thesis needs, or do you want to prioritize differently?"
4. **Pushback handled well.** *"Noted."* between questions is *good* — doesn't validate or correct mid-diagnostic, prevents gaming. **Risk:** less confident learner reads it as cold. Add a one-line norm-setter at start: *"I won't react during the diagnostic — that's deliberate, not a verdict."*
5. **Recommend-vs-dismiss bar:** every lesson should reference what Devon specifically said earlier. If the tutor doesn't update its model of the learner as they go, Devon dismisses it as another tutorial.
6. **Verdict.** Well-targeted at this archetype. The Q6/Q7/Q8 cluster (multi-agent skepticism, production reflexes, prompt injection) is exactly where this learner most needs sharpening, and the diagnostic surfaces it cleanly. Risk for this archetype: condescension. They will tolerate being wrong, will not tolerate being explained-to.

---

## Sam — 4th-year, near-pro, ex-Anthropic intern

**Profile.** 4th-year CS senior. Last summer at Anthropic on the inference team (KV cache eviction policies). Side-project agent in prod doing GitHub PR triage at ~1k req/day on Modal. Knows transformer internals deeply. Going to grad school for RL. Terse, skeptical of tutorials, will challenge bad framings.

**Diagnostic answers (representative):**
- Q1: corrected the framing — *"'deterministic' is doing a lot of work there — even at temp=0 you'll see drift across providers because of non-associative float ops on GPU, batch-size-dependent kernels, MoE routing"*
- Q2: gave the formula `2 * num_layers * num_heads * head_dim * seq_len * batch * dtype_bytes`, the ~2.5MB/token estimate, named GQA + PagedAttention + prefill-vs-decode regimes, all unprompted
- Q5: named the gotcha — *"The gotcha is 'looks-like-a-read' tools that mutate, like `get_or_create_session`. Those bite you."*
- Q6: cited Cognition.ai's "Don't Build Multi-Agents" post by name
- Q8: explicitly flagged what they don't know — *"the specific token-level evasions people use to bypass instruction-hierarchy training — I haven't dug into that yet"*
- Q9: named position bias + verbosity, gave detection protocols, mentioned self-preference as a third

**Reaction to assessment (which skipped foundations and proposed L7 indirect injection deep-dive):**
> "Okay, this is more like it."

Sam then engaged with calibration questions about his own PR-triage agent — analyzed the exfil paths (none to third parties, but reputation/integrity risk), named which mitigations he'd ship first vs which are theater (output filters scanning for "ignore previous instructions" → trivially bypassed; smaller-model guards → attackers route around). Asked the tutor to push back: *"Tell me if I'm wrong."*

### Findings
1. **Q1, Q2, Q5, Q7 were wasted on Sam.** These are warmup questions for someone who's shipped. **The diagnostic should branch:** a strong Q1 answer should escalate Q2 to something harder ("80GB HBM, 70B model, what's your max concurrent context budget at FP8 with GQA-8?"). **Fixed-script diagnostics burn trust with experts.** The right gaps did surface — but only because the questions were open enough to expose "haven't dug into that yet." That's lucky, not designed.
2. **Assessment did respect prior knowledge.** Explicit "skipping foundations" + naming three specific gaps from Sam's answers is the right move. **Citing the actual corrections** ("you corrected the determinism framing on Q1") would land even better; Sam wants to be seen.
3. **L7 indirect injection is a defensible pick** — real gap with production stakes, ties to grad school RL research (reward hacking shares structure), Sam's own agent is the lab. **Calibration questions were good** — grounded in Sam's actual project, asked for trade-offs not definitions, invited disagreement ("which is theater?").
4. **The "Noted" cadence is the protocol's biggest failure for experts.** Sam corrected Q1 framing, named GQA/PagedAttention unprompted on Q2, cited Cognition.ai on Q6 — tutor said *"Noted."* every time. *"For a strong learner it reads as deaf. A diagnostic mode that can't react isn't neutral, it's flat."*
5. **Skill needs an expert mode.** What Sam wants and isn't getting:
   - Diagnostic that adapts within the session
   - Skip-question option ("I've shipped this, next")
   - Lessons framed as gap-fill against stated project, not curriculum slots
   - Primary-source pointers (papers, postmortems) over re-explained concepts
   - Tutor that pushes back when Sam is wrong
6. **Verdict.** Marginal. First 9 questions almost lost Sam — Q1/Q2/Q5 beneath their level, "Noted" cadence grating. Recovery (skipping foundations, picking L7, project-grounded calibration) was strong enough that Sam is engaged at the end. **If lesson 1 delivers actual depth on injection mechanics, they stay. If it opens with "prompt injection is when an attacker…" they're gone by minute three.**

---

## Cross-persona synthesis

### What works (keep)

- **Specificity of the assessment.** Across all four personas, naming *specific* mistakes (with the wrong concept named correctly) was the highest-leverage thing the skill did. Generic feedback would have flattened it for Jordan, Devon, and Sam. Maya's complaint was deficit-framing, not specificity.
- **Calibration-before-explanation pattern.** Devon and Sam both flagged this as the single strongest signal that this isn't another tutorial. Jordan implicitly engaged with it. Only Maya bounced off — because she needed a *win* first.
- **Skip decisions when justified.** Devon and Sam both explicitly approved the skip-foundations move. Devon: "the skip was correct and well-justified." Sam: "okay, this is more like it."
- **The 9-layer mental model.** No persona criticized the curriculum *structure* — the L0–L8 spine landed across all four levels.
- **`Noted.` between questions for the middle band.** Maya/Jordan didn't notice; works as a token-saver and prevents gaming.

### What breaks (must fix)

| ID | Issue | Affects | Severity |
|---|---|---|---|
| **DX-1** | Diagnostic is non-adaptive — same 9 questions regardless of signal | All four | Critical |
| **DX-2** | No on-ramp for true beginners — diagnostic uses jargon to probe but provides no anchor | Maya | Critical |
| **DX-3** | No expert lane — strong learners spend 15 min proving they know things | Sam (mostly), Devon (somewhat) | High |
| **DX-4** | Assessment leads with deficit, not strengths — burns confidence in beginners | Maya | High |
| **DX-5** | First lesson opens with two more questions, no concrete picture first | Maya (acutely), others (mildly) | Medium |
| **DX-6** | "Noted" cadence reads as deaf to experts, cold to anxious beginners | Sam, potentially Maya | Medium |
| **DX-7** | Strengths section in assessment is generic; gaps section is specific — asymmetric | Devon | Medium |
| **DX-8** | No ask-the-learner-what-they-want before announcing path — disrespects adult learner agency | Devon, Sam | Medium |
| **DX-9** | Confident-shallow learners (Jordan) won't flag undefined jargon — protocol needs forced check-ins | Jordan | Medium |
| **DX-10** | "SR items" used in user-facing output without definition | Maya | Trivial |

### Action plan (prioritized)

**Tier 1 — fix now (small effort, high impact):**
1. **Add jargon-permission preamble to the diagnostic:** *"I'm going to use technical terms to probe — if any term is unfamiliar, just say so. The diagnostic uses jargon to find your edge, not to gatekeep."* Fixes DX-2 partially, DX-6 partially. **Trivial.**
2. **Define "SR" or rename to "review queue" in user-facing output.** Fixes DX-10. **Trivial.**
3. **Define each acronym/term once when first appearing in any diagnostic question** (e.g., "ReAct (a popular reason-act-observe agent loop pattern)"). Fixes DX-2 partially. **Trivial.**
4. **Rewrite assessment template to lead with specific strengths, then specific gaps.** Both sections must be equally specific. Drop the word "intermediate." Fixes DX-4, DX-7. **Small.**
5. **Add "does that match your priorities, or do you want to redirect?" after path proposal.** Fixes DX-8. **Trivial.**

**Tier 2 — design changes (medium effort, structural):**
6. **Adaptive diagnostic depth.** Strong answer → next question escalates. Weak answer → next question scaffolds. Skip-question option for experts. Fixes DX-1, DX-3 partially. **Medium-large.**
7. **Beginner branch.** Pre-diagnostic 3-question vibe check; if signals say beginner, route to vocab-first L0 mode that opens with concrete pictures before any probing. Fixes DX-2, DX-5. **Medium.**
8. **Forced check-ins for confident-shallow learners.** Periodically: "in your own words, what's [term]?" Catches Jordan-mode passive nodding. Fixes DX-9. **Small.**
9. **Expert lane.** Skip-question affordance, primary-source pointers (papers/postmortems) instead of re-explanations, project-grounded calibration questions, tutor pushback when expert is wrong. Fixes DX-3. **Medium.**

**Tier 3 — nice-to-have:**
10. **Replace "Noted" with "Got it" or similar, add a one-line norm-setter at start of diagnostic** ("I won't react during the diagnostic — that's deliberate, not a verdict"). Partial fix for DX-6. **Trivial.**

### Bottom line

The skill works well for the **middle band** (Jordan and Devon — built something, now want depth). The diagnostic, assessment, and calibration-first lesson opener are *correctly designed* for that audience. The skill **fails at the edges** — Maya bounces off because there's no on-ramp, Sam almost bounces off because there's no fast lane.

If the skill stays scoped to "intermediate" (per the SKILL.md frontmatter), Tier 1 fixes are mandatory and Tiers 2/3 are optional polish. If the skill aims to handle "anyone who builds with LLMs" — including bright beginners and shipping engineers — Tiers 1 and 2 both become required.

The single highest-leverage change is **DX-1 (adaptive diagnostic)**. Every persona flagged it — for opposite reasons.
