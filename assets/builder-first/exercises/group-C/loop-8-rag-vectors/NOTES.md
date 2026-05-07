# Loop 8 — Notes

*Numbers are the load-bearing content here. RAG without metrics is theater.*

## Concept

What this loop teaches in your own words. The trio of retrievers (sparse / dense / hybrid) and what each one does mechanically. Why hybrid usually wins. Why RAG isn't always the right answer.

How does this connect back to Loop 4? *(The answer should mention key-value memory.json as the small-corpus exact-key precursor.)*

## The break

Numbers across all 5 retrievers + long-context baseline:

| Retriever | Precision@5 | MRR | Avg latency | exact_term | synonym | paraphrase |
|---|---|---|---|---|---|---|
| naive | | | | | | |
| bm25 | | | | | | |
| dense | | | | | | |
| hybrid (RRF) | | | | | | |
| hybrid + cross-encoder rerank | | | | | | |
| long-context (no RAG) | | | | | | |

For each retriever, one sentence on which query type(s) it wins / loses on.

## The fix

**Chunking strategy choice:** *(which one, and why)*

For this 20-doc corpus chunking didn't help much (1 chunk per doc covers it). For a real 10K-doc corpus you'd pick ___ because ___.

**RAG-vs-long-context decision rule (the load-bearing paragraph):**

Stage 6 should land an answer like: *"For corpora under N tokens, long-context wins on latency and simplicity. Above N tokens, RAG wins on cost (one embed + one query vs sending the full corpus every time) and on freshness (cheap to re-embed changed docs vs re-indexing the prompt). For this shape of task, the threshold is around _____ tokens, beyond which RAG starts paying for itself."*

Concrete numbers, not vibes.

**Vector-DB production trade-off:**

| Choice | Pick when |
|---|---|
| pgvector | you already run Postgres |
| Pinecone | managed > self-hosted, willing to pay |
| Weaviate / Qdrant | self-hosted with extra features |
| LanceDB | embedded, on-disk, columnar |
| ChromaDB (this loop) | local-only, zero-friction development |

Pick by your existing infra, not by Twitter hype.

## What surprised you

Often: that hybrid doesn't always beat dense (when the corpus is mostly synonym-heavy). Or that cross-encoder reranking adds 100ms per query for a 5% precision gain — sometimes worth it, sometimes not. Naming the surprise calibrates your future retrieval choices.
