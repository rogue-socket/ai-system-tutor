# Loop 8 — What's Broken

Switch to **Group C** first:

```bash
cd ~/ai-systems/exercises/group-C
uv sync   # heavy: torch ~2GB on first sync, 5–15 min on slow connections
# macOS / Linux:
source .venv/bin/activate

# Windows PowerShell:
# .venv\Scripts\activate
```

If you don't want the torch download (Stage 5 needs it for cross-encoder reranking), defer Stage 5 — Stages 1–4 use Gemini embeddings + chromadb + rank-bm25 only, no torch.

---

The starter is a corpus of 20 short docs about distributed systems and databases, plus a 15-query benchmark with known-relevant doc IDs. `naive_search.py` is regex grep — counts query-word hits per doc. It works for exact terms, fails on synonyms.

**Connect this to Loop 4.** This is the long-term memory from Loop 4 — but semantic. The key-value `memory.json` you edited by hand was a tiny corpus with exact-key lookup; this is the same idea, scaled to N entries with similarity-based retrieval.

## Run it first

```bash
python naive_search.py
```

You'll see precision@5, MRR, average latency, and per-query results. Note where it does well (exact-term queries) and where it does badly (synonym queries: *"semantic search"* doesn't find `embeddings`; *"how can multiple machines agree on a value despite failures?"* doesn't find `raft` or `paxos` if those words aren't in the query).

Save the four numbers (precision@5, MRR, latency, and any by-type breakdowns) in `NOTES.md` under "the break."

## Your task — six stages

Each stage produces a new file you'll write. Do not modify `corpus.json`, `queries.json`, or `eval.py` — they're shared across all retrievers so comparisons are fair.

### Stage 1 — BM25 (sparse retrieval)

Create `bm25_search.py`. Use `rank_bm25.BM25Okapi`:

```python
from rank_bm25 import BM25Okapi

# Tokenize each doc once at module load.
tokenized = [(doc["title"] + " " + doc["text"]).lower().split() for doc in CORPUS.values()]
bm25 = BM25Okapi(tokenized)

def search(query: str, k: int = 5) -> list[str]:
    tokens = query.lower().split()
    scores = bm25.get_scores(tokens)
    # Map back to doc IDs, sort, return top-k
    ...
```

Run it. Compare to naive:
- Where does BM25 win? (Probably exact-term queries: better ranking by rare-word weight.)
- Where does it tie? (Single-term queries with one obvious doc.)
- Where does it still lose? (Synonym queries.)

Numbers go in `NOTES.md`.

### Stage 2 — Dense retrieval (embeddings)

Create `dense_search.py`. Use Gemini's embedding model + ChromaDB.

```python
from google import genai
import chromadb

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def embed(text: str) -> list[float]:
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
    )
    return result.embeddings[0].values

# Index each doc once at module load.
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("docs")
for doc_id, doc in CORPUS.items():
    text = doc["title"] + " " + doc["text"]
    collection.add(ids=[doc_id], embeddings=[embed(text)], documents=[text])

def search(query: str, k: int = 5) -> list[str]:
    q_emb = embed(query)
    results = collection.query(query_embeddings=[q_emb], n_results=k)
    return results["ids"][0]
```

(Embedding the corpus runs 20 API calls once — within free tier. The query is one more.)

Run it. Compare to BM25:
- **Where dense wins:** synonyms (*"semantic search"* should now find `embeddings`), paraphrases (*"machines agreeing on a value"* should find `raft`/`paxos`).
- **Where dense loses:** rare exact terms — *"BM25"* might not return the `bm25` doc as top-1 because dense embeddings dilute exact tokens.

Numbers in `NOTES.md`. By-type breakdown is the most useful column here (`by_type` from `eval.run`).

### Stage 3 — Hybrid (sparse + dense via RRF)

Create `hybrid_search.py`. Reciprocal Rank Fusion:

```python
def rrf(ranked_lists: list[list[str]], k_const: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, doc_id in enumerate(ranked, 1):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k_const + rank)
    return sorted(scores.items(), key=lambda x: -x[1])

def search(query: str, k: int = 5) -> list[str]:
    bm25_results = bm25_search.search(query, k=10)
    dense_results = dense_search.search(query, k=10)
    fused = rrf([bm25_results, dense_results])
    return [doc_id for doc_id, _ in fused[:k]]
```

Run it. Compare to BM25 and dense alone. Hybrid should be best-or-tied across all query types.

### Stage 4 — Chunking

So far each doc is one chunk. Real corpora have long docs that need splitting. Create `chunking.py` with three strategies:

1. **Fixed-size:** split at every N characters (e.g. 200 with 50-char overlap).
2. **Semantic:** split at sentence boundaries with a max chunk size.
3. **Hierarchical:** keep both the chunk text *and* a parent-doc reference; on retrieval, fetch the parent for context.

For each strategy, re-index the corpus and re-run hybrid search. The corpus here is small enough that fixed-size with N=400 should give 1-chunk-per-doc; lower N to 80 to force chunking. Compare:

- Fixed-size with small chunks: retrieval finds the *exact* chunk but the surrounding context is lost.
- Semantic: better readability, but same retrieval recall.
- Hierarchical: precision@k drops on short chunks but recall improves when you fetch parents.

Pick one strategy and write a paragraph in `NOTES.md` about *why* — what you'd change for a real 10K-doc corpus.

### Stage 5 — Cross-encoder reranking

Create `rerank.py`. Use `sentence-transformers`:

```python
from sentence_transformers import CrossEncoder
ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, candidates: list[str], k: int = 5) -> list[str]:
    pairs = [(query, CORPUS[doc_id]["title"] + " " + CORPUS[doc_id]["text"]) for doc_id in candidates]
    scores = ce.predict(pairs)
    ranked = sorted(zip(candidates, scores), key=lambda x: -x[1])
    return [doc_id for doc_id, _ in ranked[:k]]

def search(query: str, k: int = 5) -> list[str]:
    candidates = hybrid_search.search(query, k=20)  # over-fetch for reranking
    return rerank(query, candidates, k)
```

First run downloads the model (~80MB) and is slow (model load). Subsequent calls are fast.

Compare to hybrid alone. Reranking usually improves precision@5 by 5–20% but adds 50–200ms latency per query.

Note: **cross-encoder is expensive at scale.** It's `O(query_doc_pairs)` so you can't rerank 1M candidates. The pattern is *retrieve top-K cheaply, rerank top-K thoroughly*.

### Stage 6 — When to abandon RAG

The corpus here is 20 docs. Total tokens: ~5K. Easily fits in Gemini's 1M context.

Try the **long-context alternative**: stuff the entire corpus into the system prompt, ask the model to answer directly. No retrieval at all. Compare:

```python
context = "\n\n".join(f"[{doc_id}] {doc['title']}: {doc['text']}" for doc_id, doc in CORPUS.items())
# Send query + context to model, parse which doc IDs it cites.
```

Compare:
- **Latency:** which is faster — RAG (retrieve + small prompt) or long-context (huge prompt, no retrieve)?
- **Token cost per query:** RAG sends 5 docs; long-context sends 20.
- **Accuracy:** does the model find the right docs when given everything?

In 2026, with Gemini 1.5 Pro's 2M context and falling token prices, **the threshold for RAG-vs-long-context has moved.** RAG is still right for very large corpora (>100K docs), corpora with frequent updates (cheaper to re-embed than re-prompt), and cost-sensitive workloads. Long-context is increasingly viable for small-corpus high-quality use cases.

Write your conclusion in `NOTES.md`: at what corpus size does RAG start earning its keep over long-context for *this* shape of task?

### Wrap-up — Vector DB production choice

`chromadb` is local and zero-friction; perfect for this loop. Production options:
- **pgvector** — Postgres extension. Pick this if you already run Postgres.
- **Pinecone** — managed, fast, expensive.
- **Weaviate / Qdrant** — self-hosted, more features.
- **LanceDB** — embedded, columnar, on-disk.

Write a one-paragraph trade-off comparison in `NOTES.md`: pick by your existing infra, not by Twitter hype.

## When you get stuck

- **Embedding API errors.** Gemini's `text-embedding-004` is on the free tier but has its own quota. Embedding all 20 docs is one call per doc (or batch via `contents=[...]`).
- **ChromaDB persistence.** `chromadb.Client()` is in-memory; restart the script and you re-embed. For Loop 8 that's fine. Production uses `chromadb.PersistentClient(path=...)`.
- **`rank_bm25` tokenization is naive** — just `.split()`. For real use you'd want stemming + stopwords. The Loop 8 corpus is small enough to skip those.
- **Cross-encoder model download is slow.** First run takes ~30s for the ~80MB download. Subsequent runs cache locally.

## What you specifically should NOT use

- **`langchain.retrievers.*`** — Loop 8 is hand-built. The point is to feel sparse vs dense vs hybrid as different algorithms, not as drop-in framework abstractions.
- **A different corpus.** The shared corpus + queries are how comparisons stay honest.
- **`pip install -U`** — same warning.
