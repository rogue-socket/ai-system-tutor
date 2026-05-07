# Loop 7b — Win Criteria

You're done when:

- [ ] You ran `hierarchical.py`, `orchestrator.py`, `peer.py` and recorded numbers (accuracy, latency, tokens, iterations) for all three in `NOTES.md`, alongside Loop 7a's numbers.
- [ ] You read `MULTIAGENT_TRAP.md` and applied the 5-failure-mode checklist to each of your three architectures. Concrete findings are in `NOTES.md`.
- [ ] You wrote `well_prompted.py` — a single-LLM-call alternative to whichever multi-agent architecture performed best. You ran it on the same benchmark and compared.
- [ ] Your `NOTES.md` answers honestly: did the multi-agent version add anything the well-prompted single didn't? If yes, name it precisely. If no, that's the lesson.
- [ ] The one-sentence test is filled in: *"I'd use multi-agent for ___ specifically because ___, and I've ruled out single-agent-with-better-prompts because ___."* Concrete blanks, defensible against critique.

When all five are checked, finish `CHEATSHEET.md`. Then `/loop next` for Loop 8 — RAG with vectors. **Switch to Group C's venv first** (Loop 8 needs `chromadb`, `rank-bm25`, `sentence-transformers`).

## Stretch (optional)

- Add a "hard" multi-step task set to `benchmark.TASKS` — problems requiring genuine decomposition (e.g. "if a train leaves Boston at 60mph and another leaves NYC at 80mph, both heading toward each other, when do they meet given a 200-mile separation?"). Re-run all three architectures + baseline. Does multi-agent now earn its keep?
- Mix models: orchestrator on `gemini-2.0-flash-thinking-exp` (reasoning-tuned), workers on `gemini-2.0-flash` (cheap). Does this version of "multi-agent" pay for itself?
- Run the well-prompted single agent on Loop 7a's benchmark. Compare its numbers to Loop 7a's reflexion. Is "better prompting" the cheaper version of Reflexion?

## How the tutor will check

When you say you're done:
1. Show the comparison table — Loop 7a + Loop 7b + well_prompted, all on the same benchmark.
2. Walk through the 5 failure modes against (say) `hierarchical.py` — point at the specific cost-explosion / context-bottleneck / costume-wearing examples in your run.
3. Read aloud the one-sentence test answer.
4. Be honest: do you still believe in multi-agent for the case you described? Or did the exercise convince you the answer was "no, this case doesn't need it"?

The answer "no" is a passing grade.
