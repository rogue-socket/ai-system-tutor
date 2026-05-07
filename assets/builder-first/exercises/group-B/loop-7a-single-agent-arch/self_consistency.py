"""Self-consistency — sample N answers, vote on the most common.

Theoretically reduces variance from temperature/sampling. Practically, naive
voting (exact-string match) misses semantically equivalent answers ("4" vs
"four", "40" vs "40 mph", "256" vs "256.0").

THE STARTER USES STRING-MATCH VOTING. Stage 4 of your task: smarter voting.
"""
from collections import Counter

import os

from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

import benchmark

load_dotenv(find_dotenv(usecwd=True))
# ChatGoogleGenerativeAI reads GOOGLE_API_KEY; alias from GEMINI_API_KEY.
os.environ.setdefault("GOOGLE_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
# Higher temperature so samples actually vary.
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

N_SAMPLES = 5

ANSWER_PROMPT = "Solve this problem. Output only the final numeric answer.\nProblem: {q}\nAnswer:"


def run(question: str) -> dict:
    samples = []
    tokens = 0
    for _ in range(N_SAMPLES):
        resp = llm.invoke(ANSWER_PROMPT.format(q=question))
        tokens += (resp.usage_metadata or {}).get("total_tokens", 0)
        samples.append(resp.content.strip())

    # Naive voting: most common exact string. Misses semantically-equivalent variants.
    counts = Counter(samples)
    answer, _ = counts.most_common(1)[0]

    return {"answer": answer, "tokens": tokens, "iterations": N_SAMPLES}


if __name__ == "__main__":
    bench = benchmark.run_benchmark("self_consistency", run)
    benchmark.print_summary(bench)
