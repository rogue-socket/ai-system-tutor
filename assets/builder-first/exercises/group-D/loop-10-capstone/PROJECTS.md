# Capstone Project Menu

**Pick exactly one.** Trying to combine two means you'll ship neither.

For each option below: **scope** = the v1 you commit to. **out-of-scope** = the things that look attractive and will kill your timeline. The tutor will push back on every "and also" you propose.

---

## Option A — RAG agent over a corpus you care about

**Goal.** A search-and-answer agent over a corpus you actually want to query — your meeting notes, your company docs, a textbook PDF you're studying, your codebase, an open-data set you find interesting.

**Scope (v1).**
- Corpus loaded once at startup; manual re-index by re-running setup.
- Hybrid retrieval (sparse + dense) from Loop 8.
- Single-turn Q&A — no multi-turn memory.
- One UI: CLI or `/query` HTTP endpoint. Pick one.
- 20 eval cases over the corpus.

**Out-of-scope.**
- Real-time corpus updates / streaming ingestion.
- Multi-tenant / per-user corpora.
- A web UI with auth.
- Re-ranking model fine-tuning.

**Suggested stack.** Group C deps (chromadb, rank-bm25) + Loop 8's retrievers. Optional: FastAPI from Group D for a `/query` endpoint.

**Eval shape.** 20 question-answer pairs. Use Loop 9's `evals/run_offline.py` pattern — numeric scorer for fact lookups, LLM-as-judge for free-form answers.

**Common scope-creep traps.**
- "I'll add a chat history" → multi-turn is its own project. Out.
- "I'll add user accounts" → out.
- "I want it to work on my entire Slack history (50K messages)" → start with 100 messages, scale later.

---

## Option B — Coding agent (bounded)

**Goal.** An agent that can do *one* coding task well: write a test for a Python function, refactor a file according to a rule, or fix a specific bug class.

**Scope (v1).**
- ONE coding task. Pick: test-writing OR refactor-by-rule OR bug-fix-class. Not all three.
- Sandbox: agent reads a file, writes a new one. Never modifies source in-place.
- Tool surface: `read_file`, `write_file`, `run_pytest` (or equivalent).
- 20 eval cases — each is a (input file, expected behavior of output) pair.

**Out-of-scope.**
- Multi-file edits.
- "Understanding the whole codebase" — limit to the file the user names.
- Git integration (branching, committing). Output goes to a separate dir.
- IDE integration.

**Suggested stack.** Group A deps (just google-genai). Optional: Group B for LangGraph if your agent has clear branching, but "the LangGraph version was 30% more code for no quality gain" is a possible postmortem finding.

**Eval shape.** 20 (input file, criterion) pairs. Criterion examples: *"output file has a `test_<name>` function for every public function in input"*, *"all `print(...)` calls become `logging.info(...)`"*. The criterion is what the LLM-as-judge or a small Python check evaluates.

**Common scope-creep traps.**
- "Multi-file refactors" → out.
- "Auto-PR" → out.
- "Agent decides which file to edit" → out. User specifies the file.

---

## Option C — Task agent (calendar / email / messaging)

**Goal.** An assistant that handles one personal-productivity task: schedule meetings, draft replies to emails, surface Slack threads needing your attention.

**Scope (v1).**
- Mock the external API first. Real integration is v2.
- One task type. Not "calendar AND email." One.
- 20 eval cases.

**Out-of-scope.**
- OAuth / actually connecting to a real Google account in v1. Mock JSON files representing your inbox / calendar.
- Multi-step planning beyond "look up, decide, draft."
- A UI beyond CLI.

**Suggested stack.** Group A or B. Pydantic schemas for the mock API are essential — start with the schema, build the mocks, then write the agent.

**Eval shape.** 20 (mock state, user query, expected agent action) tuples. Agent action might be "draft this reply" or "propose this calendar slot." Judge with LLM-as-judge.

**Common scope-creep traps.**
- "I'll use the real Gmail API" → real API auth is its own week. Mock first.
- "I want it to be proactive" → reactive only in v1.
- "I want it to remember preferences" → preferences-as-mock-config-file is OK; learning preferences over time is v2.

---

## Option D — Browser agent (Playwright-driven)

**Goal.** An agent that automates ONE browser workflow: fill a form, scrape a single-page table, paginate through a list.

**Scope (v1).**
- One workflow on one site (or one type of site).
- Headed mode (visible browser) for development; headless for "deployment."
- Tool surface: `goto(url)`, `click(selector)`, `fill(selector, value)`, `read_page() -> str`.
- 20 eval cases — same workflow on synthetic input variations.

**Out-of-scope.**
- Multi-tab / multi-window.
- CAPTCHA handling.
- Authentication flows beyond basic password forms.
- Generic "browse anything" — pick one task.

**Suggested stack.** Group A + `playwright` (you'll add this to a personal venv since it's not in Group D's pyproject). Group B's LangGraph helps with branching workflows.

**Eval shape.** 20 (input scenario, expected end state) pairs. End state might be *"form was submitted"*, *"first 10 results extracted"*. Verify with another `read_page()` after the agent finishes.

**Common scope-creep traps.**
- "Make it work on any e-commerce site" → out. Pick one.
- "It should retry forever on flaky pages" → bound retries hard.
- "Add visual reasoning over screenshots" → multimodal is v2.

---

## Option E — Data extraction agent

**Goal.** Structured extraction from messy text — invoice fields from PDFs, named entities from articles, structured properties from product descriptions.

**Scope (v1).**
- One source format (PDF, plain text, or HTML — pick one).
- One target schema (Pydantic model with ~5-15 fields).
- Batch processing: input is a directory of N files, output is a JSONL of structured records.
- 20 eval cases — each is a (input file, expected JSON) pair.

**Out-of-scope.**
- Multi-format ingestion.
- Active learning / human-in-the-loop correction.
- Confidence calibration beyond "what fields did the model fill?"

**Suggested stack.** Group A. Pydantic schemas + Gemini's structured output mode. Optionally PDF parsing via `pypdf` if you go the PDF route.

**Eval shape.** Field-level accuracy: for each of the 20 cases, compute % of fields the model got right. Fields that need exact match (IDs, dates) vs fields that need semantic match (descriptions) are different scorers.

**Common scope-creep traps.**
- "Handle every variation of every PDF" → start with 5 representative samples, add more after v1.
- "Learn the schema from examples" → schema is fixed, not learned.
- "Real-time as files arrive" → batch only.
