"""Peer multi-agent — two agents propose, critique, converge.

Agent A proposes. Agent B critiques. If they disagree, A revises.

Compared to Loop 7a's Reflexion: same shape, two distinct prompts. Compared
to single-agent baseline: ~3x cost. Whether the "two distinct agents" buys
anything that one self-critiquing agent doesn't is the question.
"""
import os

from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

import benchmark

load_dotenv(find_dotenv(usecwd=True))
# ChatGoogleGenerativeAI reads GOOGLE_API_KEY; alias from GEMINI_API_KEY.
os.environ.setdefault("GOOGLE_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

PROPOSE_PROMPT = "Solve this problem. Output only the final numeric answer.\nProblem: {q}\nAnswer:"

CRITIQUE_PROMPT = """Another agent proposed an answer. Critique it.

Problem: {q}
Their answer: {a}

If correct, reply exactly: AGREE
If wrong or unclear, reply: DISAGREE: <one-sentence reason and your alternative answer>"""

REVISE_PROMPT = """Your answer was critiqued. Reconsider and produce a final numeric answer.

Problem: {q}
Your prior answer: {prev}
Peer critique: {critique}

Output only the final numeric answer."""


def run(question: str) -> dict:
    tokens = 0

    # A proposes
    a = llm.invoke(PROPOSE_PROMPT.format(q=question))
    tokens += (a.usage_metadata or {}).get("total_tokens", 0)
    a_answer = a.content.strip()

    # B critiques
    b = llm.invoke(CRITIQUE_PROMPT.format(q=question, a=a_answer))
    tokens += (b.usage_metadata or {}).get("total_tokens", 0)
    critique = b.content.strip()

    if critique.upper().startswith("AGREE"):
        return {"answer": a_answer, "tokens": tokens, "iterations": 2}

    # A revises
    a2 = llm.invoke(REVISE_PROMPT.format(q=question, prev=a_answer, critique=critique))
    tokens += (a2.usage_metadata or {}).get("total_tokens", 0)
    return {"answer": a2.content.strip(), "tokens": tokens, "iterations": 3}


if __name__ == "__main__":
    bench = benchmark.run_benchmark("peer", run)
    benchmark.print_summary(bench)
