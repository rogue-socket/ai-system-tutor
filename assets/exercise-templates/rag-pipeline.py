"""
Starter scaffold: minimal RAG pipeline with hybrid retrieval and reranking.

Pipeline:
    query
      -> rewrite
      -> [BM25 search, dense search]
      -> RRF merge
      -> cross-encoder rerank
      -> top-k into prompt
      -> generate

Fill in the TODOs. Goal: a 100-line end-to-end RAG that you can ablate
component-by-component to see what each step contributes.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path

# pip install rank-bm25 sentence-transformers
# from rank_bm25 import BM25Okapi
# from sentence_transformers import SentenceTransformer, CrossEncoder


@dataclass
class Doc:
    id: str
    text: str
    metadata: dict = field(default_factory=dict)


@dataclass
class ScoredDoc:
    doc: Doc
    score: float
    source: str  # "bm25" | "dense" | "merged" | "reranked"


# ---------- Index ----------

class HybridIndex:
    def __init__(self, docs: list[Doc]):
        self.docs = docs
        # TODO 1: build BM25 index over tokenized docs
        # self.bm25 = BM25Okapi([self._tokenize(d.text) for d in docs])

        # TODO 2: build dense index. Easiest: precompute embeddings and
        # do brute-force cosine. Production: use FAISS / Qdrant / sqlite-vec.
        # self.embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")
        # self.embeddings = self.embedder.encode([d.text for d in docs], normalize_embeddings=True)

        # TODO 3: optional cross-encoder for reranking
        # self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return text.lower().split()

    def bm25_search(self, query: str, k: int = 20) -> list[ScoredDoc]:
        # TODO 4
        raise NotImplementedError

    def dense_search(self, query: str, k: int = 20) -> list[ScoredDoc]:
        # TODO 5
        raise NotImplementedError

    def rerank(self, query: str, candidates: list[ScoredDoc], k: int = 5) -> list[ScoredDoc]:
        # TODO 6: cross-encoder rerank. Score each (query, doc) pair. Return top-k.
        raise NotImplementedError


# ---------- Merge ----------

def reciprocal_rank_fusion(
    rankings: list[list[ScoredDoc]],
    k: int = 60,  # RRF constant
) -> list[ScoredDoc]:
    """
    Combine multiple ranked lists into one. RRF score: sum over rankings of 1/(k+rank).
    This is the standard approach for hybrid search; doesn't need normalized scores.
    """
    # TODO 7
    raise NotImplementedError


# ---------- Query rewriting ----------

def rewrite_query(query: str) -> str:
    """
    TODO 8: optional. Use a small model to rewrite the user query for retrieval.
    For now, return as-is. When you turn this on, A/B it — sometimes rewriting hurts.
    """
    return query


# ---------- Generation ----------

PROMPT_TEMPLATE = """\
Answer the user's question using ONLY the context below. If the context is
insufficient, say so explicitly — do not guess.

Context:
{context}

Question: {question}

Answer:"""


def generate(question: str, context_docs: list[ScoredDoc]) -> str:
    context = "\n\n---\n\n".join(
        f"[{i+1}] {d.doc.text}" for i, d in enumerate(context_docs)
    )
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    # TODO 9: call your model with the prompt. Return the answer.
    raise NotImplementedError


# ---------- End-to-end ----------

def rag(question: str, index: HybridIndex, top_k: int = 5) -> dict:
    rewritten = rewrite_query(question)
    bm25_hits = index.bm25_search(rewritten, k=20)
    dense_hits = index.dense_search(rewritten, k=20)
    merged = reciprocal_rank_fusion([bm25_hits, dense_hits])
    reranked = index.rerank(rewritten, merged[:20], k=top_k)
    answer = generate(question, reranked)

    return {
        "question": question,
        "rewritten": rewritten,
        "retrieved_doc_ids": [d.doc.id for d in reranked],
        "answer": answer,
    }


if __name__ == "__main__":
    # TODO 10: load your corpus
    # docs = [Doc(id=str(i), text=line.strip()) for i, line in enumerate(Path("corpus.txt").read_text().splitlines()) if line.strip()]
    # index = HybridIndex(docs)
    # result = rag("Your question here", index)
    # print(json.dumps(result, indent=2))
    pass
