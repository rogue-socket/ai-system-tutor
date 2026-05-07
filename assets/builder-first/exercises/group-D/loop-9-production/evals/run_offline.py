"""Offline eval harness with LLM-as-judge.

Reads cases from cases.json. For each case:
- numeric scorer: regex-extract first number, compare to expected (Loop 7a style).
- judge scorer: an LLM judges whether the answer satisfies the rubric.

LLM-as-judge has known biases — implementing the bias controls is part of
Loop 9's task. Stage 4 of BREAK.md.

Usage (after the Loop 9 starter is running):
    python evals/run_offline.py
"""
import json
import os
import re
import sys
import time
from pathlib import Path

# Make sibling agent.py importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import agent  # noqa: E402

from dotenv import find_dotenv, load_dotenv  # noqa: E402
from google import genai  # noqa: E402

load_dotenv(find_dotenv(usecwd=True))
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

CASES = json.loads((Path(__file__).parent / "cases.json").read_text())


def numeric_match(predicted: str, expected: str) -> bool:
    nums = re.findall(r"-?\d+\.?\d*", predicted)
    if not nums:
        return False
    try:
        return abs(float(nums[0]) - float(expected)) < 0.01
    except ValueError:
        return False


JUDGE_PROMPT = """You are an evaluation judge. Decide if the answer satisfies the rubric.

Question: {q}
Rubric: {rubric}
Answer: {a}

Reply with ONLY one of:
- PASS
- FAIL: <one-line reason>

Ignore length and verbosity. Score on whether the answer satisfies the rubric."""


def judge(question: str, expected_rubric: str, predicted: str) -> bool:
    """Single-shot LLM-as-judge. Has known biases — see BREAK.md Stage 4 for bias controls."""
    prompt = JUDGE_PROMPT.format(q=question, rubric=expected_rubric, a=predicted)
    resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    verdict = (resp.text or "").strip().upper()
    return verdict.startswith("PASS")


def main() -> None:
    results = []
    for case in CASES:
        start = time.perf_counter()
        try:
            res = agent.answer(case["question"])
            ans = res["answer"]
            tokens = res["tokens"]
            err = None
        except Exception as e:
            ans = ""
            tokens = 0
            err = f"{type(e).__name__}: {e}"

        latency = (time.perf_counter() - start) * 1000

        if err:
            passed = False
        elif case["scorer"] == "numeric":
            passed = numeric_match(ans, case["expected"])
        else:
            passed = judge(case["question"], case["expected"], ans)

        results.append({
            "case": case,
            "answer": ans,
            "passed": passed,
            "latency_ms": latency,
            "tokens": tokens,
            "error": err,
        })

    print("\n=== Offline eval ===")
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    print(f"Pass: {passed}/{total} ({passed / total:.0%})")
    avg_latency = sum(r["latency_ms"] for r in results) / total
    total_tokens = sum(r["tokens"] for r in results)
    print(f"Avg latency: {avg_latency:.0f} ms")
    print(f"Total tokens: {total_tokens}")
    print()
    for r in results:
        mark = "PASS" if r["passed"] else "FAIL"
        q_short = r["case"]["question"][:50] + ("..." if len(r["case"]["question"]) > 50 else "")
        scorer = r["case"]["scorer"]
        err = f" [{r['error']}]" if r["error"] else ""
        print(f"  [{mark}] ({scorer:7}, {r['tokens']:>4} tok) {q_short} -> {r['answer'][:40]}{err}")


if __name__ == "__main__":
    main()
