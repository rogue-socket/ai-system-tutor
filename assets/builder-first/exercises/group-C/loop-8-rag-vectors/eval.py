"""Evaluation harness for retrievers.

Computes precision@k, MRR, and latency over `queries.json`.

Each retriever module implements `search(query: str, k: int) -> list[str]` —
returns ranked doc IDs. Pass that function to `eval.run(name, fn)`.

Used by:
- naive_search.py (starter)
- bm25_search.py (Stage 1, you write)
- dense_search.py (Stage 2, you write)
- hybrid_search.py (Stage 3, you write)
- rerank.py (Stage 5, you write — typically wraps another retriever)
"""
import json
import time
from collections.abc import Callable
from pathlib import Path

QUERIES = json.loads((Path(__file__).parent / "queries.json").read_text())


def precision_at_k(retrieved: list[str], relevant: list[str], k: int = 5) -> float:
    if not retrieved:
        return 0.0
    hits = sum(1 for d in retrieved[:k] if d in relevant)
    return hits / k


def mrr(retrieved: list[str], relevant: list[str]) -> float:
    """Mean reciprocal rank — 1/rank of first relevant doc, 0 if none in top-k."""
    for i, d in enumerate(retrieved, 1):
        if d in relevant:
            return 1.0 / i
    return 0.0


def run(name: str, search_fn: Callable[[str, int], list[str]], k: int = 5, verbose: bool = True) -> dict:
    p_scores = []
    mrr_scores = []
    latencies = []
    by_type: dict[str, list[float]] = {}
    rows = []

    for q in QUERIES:
        start = time.perf_counter()
        retrieved = search_fn(q["query"], k)
        latency = (time.perf_counter() - start) * 1000

        p = precision_at_k(retrieved, q["relevant"], k)
        m = mrr(retrieved, q["relevant"])

        p_scores.append(p)
        mrr_scores.append(m)
        latencies.append(latency)
        by_type.setdefault(q["type"], []).append(p)

        rows.append((q["query"], q["type"], q["relevant"], retrieved[:k], p, m))

    summary = {
        "name": name,
        "k": k,
        "precision_at_k": sum(p_scores) / len(p_scores),
        "mrr": sum(mrr_scores) / len(mrr_scores),
        "avg_latency_ms": sum(latencies) / len(latencies),
        "by_type": {t: sum(ps) / len(ps) for t, ps in by_type.items()},
    }

    if verbose:
        print(f"\n=== {name} (k={k}) ===")
        print(f"Precision@{k}: {summary['precision_at_k']:.3f}")
        print(f"MRR:          {summary['mrr']:.3f}")
        print(f"Avg latency:  {summary['avg_latency_ms']:.1f} ms")
        print(f"By query type: {summary['by_type']}")
        for query, qtype, relevant, retrieved, p, m in rows:
            marks = "".join("+" if d in relevant else "-" for d in retrieved)
            q_short = query[:55] + ("..." if len(query) > 55 else "")
            print(f"  [{qtype:10}] P={p:.2f} MRR={m:.2f} | {q_short} -> {marks}")

    return summary
