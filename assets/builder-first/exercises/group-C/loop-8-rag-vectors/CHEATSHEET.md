# Loop 8 — Cheatsheet

*Fill in as you build.*

## Commands

- `python naive_search.py` — regex grep baseline
- `python bm25_search.py` — sparse retrieval (Stage 1)
- `python dense_search.py` — embeddings + ChromaDB (Stage 2)
- `python hybrid_search.py` — RRF fusion (Stage 3)
- `python rerank.py` — cross-encoder rerank over hybrid (Stage 5)
- `python -c "import json; d = json.load(open('corpus.json')); print(len(d))"` — count docs

## Patterns

3–5 reusable code snippets. Suggestions:

- The BM25 init shape: tokenize once at module load, query is `bm25.get_scores(tokens)`.
- The Gemini embed call: `client.models.embed_content(model="text-embedding-004", contents=text).embeddings[0].values`.
- The ChromaDB usage: `Client → create_collection → add(ids, embeddings, documents) → query(query_embeddings, n_results)`.
- The RRF formula: `score(d) = Σ 1/(k_const + rank_i(d))` over each input ranking.
- The cross-encoder pattern: over-fetch K with cheap retriever, rerank top-K with expensive cross-encoder.

## Gotchas

3–5 traps. Suggestions:

- ChromaDB's `Client()` is in-memory — restart re-embeds. Use `PersistentClient(path=...)` for prod.
- `rank_bm25` tokenizes naively (`.split()`). Real use needs stemming + stopwords.
- Cross-encoder model loads slowly (~30s first time, ~80MB download). Cache it module-level.
- `text-embedding-004` returns 768-dim vectors. ChromaDB infers dimension from the first add — don't mix dimensions in one collection.
- Long-context wins on small corpora — *don't reach for RAG by default*.

## Numbers

Suggestions:

- Naive Precision@5: _N_
- BM25 Precision@5: _N_
- Dense Precision@5: _N_
- Hybrid Precision@5: _N_
- Hybrid + rerank Precision@5: _N_
- Long-context (full corpus in prompt) Precision@5: _N_
- Latency: naive _a_ ms, BM25 _b_ ms, dense _c_ ms (incl. embedding), rerank _d_ ms.
- Tokens per query: RAG ~_X_, long-context ~_Y_.
- Threshold corpus size at which RAG starts paying for itself: ~_N_K tokens.
