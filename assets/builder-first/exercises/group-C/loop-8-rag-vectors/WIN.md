# Loop 8 — Win Criteria

You're done when:

- [ ] `bm25_search.py` exists, runs, and produces precision@5 / MRR / latency numbers in `NOTES.md`. You can name a query type where BM25 beats naive.
- [ ] `dense_search.py` exists, runs, uses Gemini embeddings + ChromaDB. You can name a query type where dense beats BM25 (and vice versa).
- [ ] `hybrid_search.py` exists, runs, uses RRF over BM25 + dense. Hybrid's by-type accuracy table is in `NOTES.md`.
- [ ] `chunking.py` exists with at least one of the three strategies implemented. You picked one strategy and wrote *why* in `NOTES.md`.
- [ ] `rerank.py` exists, uses cross-encoder over hybrid's top-20. Latency vs accuracy delta is recorded.
- [ ] You ran the long-context alternative (Stage 6) and wrote your **RAG-vs-long-context decision rule** in `NOTES.md` with a corpus-size threshold.
- [ ] Vector-DB production trade-off paragraph in `NOTES.md`.

When all seven are checked, finish `CHEATSHEET.md`. Then `/loop next` for Loop 9 — production reality. **Switch to Group D's venv first.**

## Stretch (optional)

- Add 100 more docs to the corpus (different domain — recipes, song lyrics, anything). Re-run all retrievers. Does hybrid still win?
- Write a *contextual retrieval* version of dense search (Anthropic's pattern): prepend a one-sentence summary to each chunk before embedding. Compare retrieval quality.
- Implement *late chunking* (chunk the embeddings, not the text — embed the whole doc, then split the embedding sequence). Note where it helps vs hurts.
- Replace ChromaDB with pgvector (you'll need a local Postgres). Same retrieval, different infra. Where does the latency change?
- Add a query-type analyzer: classify queries as `exact_term` / `synonym` / `paraphrase` and route to BM25 vs dense vs hybrid. Pure dispatch, no fusion. How does it compare to RRF?

## How the tutor will check

When you say you're done:
1. Run all 5 retrievers (`naive`, `bm25`, `dense`, `hybrid`, `hybrid+rerank`). Show the by-type accuracy table.
2. Show your chunking strategy choice + rationale in NOTES.
3. Show your RAG-vs-long-context conclusion with a concrete corpus-size threshold.
4. Read aloud the vector-DB-pick paragraph.

The numbers and the by-type breakdowns are the work product. RAG without metrics is theater.
