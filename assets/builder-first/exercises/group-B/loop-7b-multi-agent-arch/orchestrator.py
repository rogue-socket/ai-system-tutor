"""Orchestrator-worker — central orchestrator dispatches step by step.

Different from hierarchical: the orchestrator decides the NEXT action at
each step (not all upfront). Workers execute and return; orchestrator
decides next based on results.

This is hierarchical with re-planning at every step. The cost is real:
each step is a full orchestrator round-trip.
"""
import os

from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

import benchmark

load_dotenv(find_dotenv(usecwd=True))
# ChatGoogleGenerativeAI reads GOOGLE_API_KEY; alias from GEMINI_API_KEY.
os.environ.setdefault("GOOGLE_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

MAX_STEPS = 5

ORCHESTRATOR_PROMPT = """You are an orchestrator. Given the problem and what's been done, decide the NEXT action.

Available actions:
- compute: hand off a sub-computation to the math worker. Provide the expression.
- analyze: hand off an interpretation to the reasoning worker. Provide the question.
- finalize: assemble the final numeric answer. Provide the answer.

Output ONE line, formatted: "<action>: <payload>"

Problem: {q}
Done so far:
{history}

Next action:"""

MATH_WORKER_PROMPT = "Compute. Output only a number.\nExpression: {t}"
REASON_WORKER_PROMPT = "Interpret. Output a brief plain-language insight.\nQuestion: {t}"


def run(question: str) -> dict:
    tokens = 0
    history_lines: list[str] = []
    answer = ""
    iters = 0

    for step in range(MAX_STEPS):
        iters = step + 1
        orch = llm.invoke(ORCHESTRATOR_PROMPT.format(
            q=question,
            history="\n".join(history_lines) if history_lines else "(nothing yet)",
        ))
        tokens += (orch.usage_metadata or {}).get("total_tokens", 0)

        content = orch.content.strip()
        action_line = content.splitlines()[0] if content else ""
        if ":" not in action_line:
            history_lines.append(f"orchestrator: malformed output: {action_line!r}")
            continue
        action, payload = action_line.split(":", 1)
        action = action.strip().lower()
        payload = payload.strip()

        if action == "finalize":
            answer = payload
            history_lines.append(f"finalize: {payload}")
            break
        if action == "compute":
            r = llm.invoke(MATH_WORKER_PROMPT.format(t=payload))
            tokens += (r.usage_metadata or {}).get("total_tokens", 0)
            history_lines.append(f"compute({payload}) -> {r.content.strip()}")
        elif action == "analyze":
            r = llm.invoke(REASON_WORKER_PROMPT.format(t=payload))
            tokens += (r.usage_metadata or {}).get("total_tokens", 0)
            history_lines.append(f"analyze({payload}) -> {r.content.strip()}")
        else:
            history_lines.append(f"unknown action: {action!r}")

    return {"answer": answer, "tokens": tokens, "iterations": iters}


if __name__ == "__main__":
    bench = benchmark.run_benchmark("orchestrator", run)
    benchmark.print_summary(bench)
