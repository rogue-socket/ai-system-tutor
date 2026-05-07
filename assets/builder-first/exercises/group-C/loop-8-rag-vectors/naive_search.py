"""Loop 8 starter — naive search.

Regex word-overlap. Counts how many query words appear in each doc, ranks
by hit count. Works for exact terms; misses synonyms, paraphrases,
related concepts.

Run:    python naive_search.py
Read:   BREAK.md to see what's missing.
Goal:   WIN.md
"""
import json
import re
from pathlib import Path

import eval

CORPUS = json.loads((Path(__file__).parent / "corpus.json").read_text())


def search(query: str, k: int = 5) -> list[str]:
    """Return top-k doc IDs by raw query-word hit count. No stemming, no stopwords."""
    words = [w.lower() for w in re.findall(r"\w+", query) if len(w) > 2]
    scores: dict[str, int] = {}
    for doc_id, doc in CORPUS.items():
        text = (doc["title"] + " " + doc["text"]).lower()
        score = sum(text.count(w) for w in words)
        if score > 0:
            scores[doc_id] = score
    ranked = sorted(scores.items(), key=lambda x: -x[1])[:k]
    return [doc_id for doc_id, _ in ranked]


if __name__ == "__main__":
    eval.run("naive", search)
