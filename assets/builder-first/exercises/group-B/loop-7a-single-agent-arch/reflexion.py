"""Reflexion — single-agent self-critique pattern.

The agent answers, then a critic agent reviews. If the critic finds issues,
the agent tries again. Theoretically converges to a better answer; practically
may loop forever or burn budget on already-correct answers.

THE STARTER HAS NO QUALITY-BASED CONVERGENCE. It runs to MAX_ITERS regardless
of whether the critic said the answer was OK. Stage 2 of your task is to fix
that — terminate when the critic approves.
"""
import os

from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

import benchmark

load_dotenv(find_dotenv(usecwd=True))
# ChatGoogleGenerativeAI reads GOOGLE_API_KEY; alias from GEMINI_API_KEY.
os.environ.setdefault("GOOGLE_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

MAX_ITERS = 5  # Hard cap to prevent runaway cost. NOT a quality cap.

ANSWER_PROMPT = "Solve this problem. Output only the final numeric answer.\nProblem: {q}\nAnswer:"
ANSWER_RETRY_PROMPT = """Solve this problem. Your previous attempt was critiqued.
Problem: {q}
Previous answer: {prev}
Critic said: {critique}

Output only the final numeric answer."""

CRITIC_PROMPT = """Review this answer for correctness. Reply with ONE line:
- If correct, reply exactly: OK
- If wrong, reply: REVISE: <one-sentence reason>

Problem: {q}
Answer: {a}"""


def run(question: str) -> dict:
    answer = ""
    iterations = 0
    tokens = 0
    last_critique = ""
    for i in range(MAX_ITERS):
        iterations = i + 1

        # Generate / regenerate answer
        if i == 0:
            prompt = ANSWER_PROMPT.format(q=question)
        else:
            prompt = ANSWER_RETRY_PROMPT.format(q=question, prev=answer, critique=last_critique)
        resp = llm.invoke(prompt)
        answer = resp.content.strip()
        tokens += (resp.usage_metadata or {}).get("total_tokens", 0)

        # Critic
        critic_resp = llm.invoke(CRITIC_PROMPT.format(q=question, a=answer))
        last_critique = critic_resp.content.strip()
        tokens += (critic_resp.usage_metadata or {}).get("total_tokens", 0)

        # NO convergence — loop runs to MAX_ITERS regardless of "OK".
        # Stage 2: terminate when last_critique starts with "OK".

    return {"answer": answer, "tokens": tokens, "iterations": iterations}


if __name__ == "__main__":
    bench = benchmark.run_benchmark("reflexion", run)
    benchmark.print_summary(bench)
