"""Hierarchical multi-agent — manager + specialized workers.

Manager decomposes the task and delegates to specialized workers (math,
reasoning). Manager assembles the final answer.

This is the canonical multi-agent shape. It also looks suspiciously like
Loop 7a's planner-executor — the difference is that "workers" have
distinct system prompts intended to give them specialized roles. Whether
that distinction earns its keep is the question MULTIAGENT_TRAP.md asks.
"""
import os

from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

import benchmark

load_dotenv(find_dotenv(usecwd=True))
# ChatGoogleGenerativeAI reads GOOGLE_API_KEY; alias from GEMINI_API_KEY.
os.environ.setdefault("GOOGLE_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

MANAGER_PROMPT = """You are a manager. Decompose this problem into 1-3 sub-tasks for specialized workers.

Available workers:
- math: pure arithmetic computation
- reason: word-problem interpretation, units, real-world context

Output format: one line per sub-task: "<worker>: <sub-task>"
Use the smallest number of sub-tasks needed.

Problem: {q}"""

MATH_WORKER_PROMPT = """You are a math worker. Compute the result of this expression. Output ONLY a number.

Task: {t}"""

REASON_WORKER_PROMPT = """You are a reasoning worker. Interpret this word problem and produce a brief insight (no final numeric answer).

Task: {t}"""

ASSEMBLE_PROMPT = """You are a manager. Given the original problem and the workers' results, produce ONLY the final numeric answer.

Problem: {q}
Worker results:
{results}

Final answer:"""


def run(question: str) -> dict:
    tokens = 0

    # Manager decomposes
    decomp = llm.invoke(MANAGER_PROMPT.format(q=question))
    tokens += (decomp.usage_metadata or {}).get("total_tokens", 0)

    sub_tasks: list[tuple[str, str]] = []
    for line in decomp.content.strip().splitlines():
        if ":" not in line:
            continue
        worker, task = line.split(":", 1)
        sub_tasks.append((worker.strip().lower(), task.strip()))

    # Workers execute
    results: list[str] = []
    for worker, task in sub_tasks:
        if worker == "math":
            prompt = MATH_WORKER_PROMPT.format(t=task)
        elif worker == "reason":
            prompt = REASON_WORKER_PROMPT.format(t=task)
        else:
            results.append(f"({worker}): unknown worker")
            continue
        resp = llm.invoke(prompt)
        tokens += (resp.usage_metadata or {}).get("total_tokens", 0)
        results.append(f"{worker}: {resp.content.strip()}")

    # Manager assembles
    assemble = llm.invoke(ASSEMBLE_PROMPT.format(q=question, results="\n".join(results)))
    tokens += (assemble.usage_metadata or {}).get("total_tokens", 0)
    answer = assemble.content.strip()

    return {
        "answer": answer,
        "tokens": tokens,
        "iterations": len(sub_tasks) + 2,  # decompose + N workers + assemble
    }


if __name__ == "__main__":
    bench = benchmark.run_benchmark("hierarchical", run)
    benchmark.print_summary(bench)
