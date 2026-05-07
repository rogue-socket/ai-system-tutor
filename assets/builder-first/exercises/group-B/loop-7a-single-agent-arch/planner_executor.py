"""Planner-executor — split planning from execution.

A planner LLM produces a step-by-step plan. An executor LLM carries out each
step. Theoretically separates "what to do" from "how to do it"; practically,
plans can be unrealistic and execution can fail halfway.

THE STARTER HAS NO REPLANNING. The plan is generated once. If a step fails or
produces a wrong intermediate result, the plan continues anyway and the final
answer is built on bad inputs. Stage 3 of your task: detect failure and replan.
"""
import os

from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

import benchmark

load_dotenv(find_dotenv(usecwd=True))
# ChatGoogleGenerativeAI reads GOOGLE_API_KEY; alias from GEMINI_API_KEY.
os.environ.setdefault("GOOGLE_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

PLANNER_PROMPT = """Break this problem into 2-4 numbered steps.
Output only the steps, one per line, like:
1. <step>
2. <step>

Problem: {q}"""

EXECUTOR_PROMPT = """Execute this step using the prior context. Output a brief result.

Prior context:
{context}

Step: {step}

Result:"""

FINALIZER_PROMPT = """Given the original problem and the executed steps, produce ONLY the final numeric answer.

Problem: {q}
Steps and results:
{trace}

Final answer:"""


def run(question: str) -> dict:
    tokens = 0

    # Plan once
    plan_resp = llm.invoke(PLANNER_PROMPT.format(q=question))
    tokens += (plan_resp.usage_metadata or {}).get("total_tokens", 0)
    plan_text = plan_resp.content.strip()
    steps = [
        line.strip() for line in plan_text.splitlines()
        if line.strip() and line.strip()[0].isdigit()
    ]

    # Execute (no replanning — even if a step fails)
    context = ""
    trace_lines = []
    for step in steps:
        exec_resp = llm.invoke(EXECUTOR_PROMPT.format(context=context, step=step))
        tokens += (exec_resp.usage_metadata or {}).get("total_tokens", 0)
        result = exec_resp.content.strip()
        context += f"\n{step}\nResult: {result}\n"
        trace_lines.append(f"{step}\n  -> {result}")

    # Finalize
    final_resp = llm.invoke(FINALIZER_PROMPT.format(q=question, trace="\n".join(trace_lines)))
    tokens += (final_resp.usage_metadata or {}).get("total_tokens", 0)
    answer = final_resp.content.strip()

    return {
        "answer": answer,
        "tokens": tokens,
        "iterations": len(steps) + 2,  # plan + N executor + finalizer
    }


if __name__ == "__main__":
    bench = benchmark.run_benchmark("planner_executor", run)
    benchmark.print_summary(bench)
