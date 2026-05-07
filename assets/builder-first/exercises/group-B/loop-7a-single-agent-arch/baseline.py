"""Baseline — single LLM call, no architecture.

The control group. If a fancier architecture isn't beating this on a given
task class, the architecture isn't earning its keep.
"""
import os

from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

import benchmark

load_dotenv(find_dotenv(usecwd=True))
# ChatGoogleGenerativeAI reads GOOGLE_API_KEY; alias from GEMINI_API_KEY.
os.environ.setdefault("GOOGLE_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

PROMPT = "Solve this problem. Output only the final numeric answer.\nProblem: {q}\nAnswer:"


def run(question: str) -> dict:
    resp = llm.invoke(PROMPT.format(q=question))
    tokens = (resp.usage_metadata or {}).get("total_tokens", 0)
    return {"answer": resp.content.strip(), "tokens": tokens, "iterations": 1}


if __name__ == "__main__":
    bench = benchmark.run_benchmark("baseline", run)
    benchmark.print_summary(bench)
