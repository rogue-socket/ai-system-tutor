"""
Starter scaffold: minimal eval harness for agent outputs.

Runs N test cases through your agent, scores each with fuzzy comparison,
prints pass rate and per-case details. Fill in the TODOs.

Why fuzzy comparison? Agent outputs vary in phrasing — "8.5 million" vs
"8,500,000" vs "around 8.5M". Exact match is too strict; LLM-as-judge is
overkill for factual recall. token_sort_ratio is a good middle ground.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path

# pip install rapidfuzz
from rapidfuzz import fuzz


# TODO 1: import or define your agent. Should be a callable taking a question
# string and returning an answer string.
# from my_agent import run_agent


@dataclass
class TestCase:
    id: str
    question: str
    expected: str
    tags: list[str] = field(default_factory=list)  # e.g., ["happy-path", "edge", "adversarial"]


@dataclass
class CaseResult:
    case_id: str
    question: str
    expected: str
    actual: str | None
    score: float          # 0-100
    passed: bool          # score >= threshold
    error: str | None = None


PASS_THRESHOLD = 80.0  # token_sort_ratio threshold for "passed"


def load_cases(path: Path) -> list[TestCase]:
    """Load test cases from JSONL. One {id, question, expected, tags?} per line."""
    cases = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            cases.append(TestCase(**obj))
    return cases


def score(actual: str, expected: str) -> float:
    """token_sort_ratio: case-insensitive, whitespace-insensitive, order-insensitive."""
    return fuzz.token_sort_ratio(actual, expected)


def run_one(case: TestCase) -> CaseResult:
    try:
        # TODO 2: replace with your agent's entry point.
        # actual = run_agent(case.question)
        actual: str = ...  # noqa
        s = score(actual, case.expected)
        return CaseResult(
            case_id=case.id,
            question=case.question,
            expected=case.expected,
            actual=actual,
            score=s,
            passed=s >= PASS_THRESHOLD,
        )
    except Exception as e:
        return CaseResult(
            case_id=case.id,
            question=case.question,
            expected=case.expected,
            actual=None,
            score=0,
            passed=False,
            error=str(e),
        )


def run_all(cases: list[TestCase]) -> list[CaseResult]:
    # TODO 3: parallelize with concurrent.futures if your agent is I/O bound
    # and your provider's rate limits allow it.
    return [run_one(c) for c in cases]


def report(results: list[CaseResult]) -> None:
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    errored = sum(1 for r in results if r.error)
    avg_score = sum(r.score for r in results) / total if total else 0

    print(f"Pass rate: {passed}/{total} ({passed / total * 100:.1f}%)")
    print(f"Errors:    {errored}")
    print(f"Avg score: {avg_score:.1f}")
    print()

    for r in results:
        marker = "[PASS]" if r.passed else "[FAIL]"
        print(f"{marker} {r.case_id}  score={r.score:.0f}")
        if not r.passed:
            print(f"  Q:        {r.question}")
            print(f"  Expected: {r.expected}")
            print(f"  Actual:   {r.actual}")
            if r.error:
                print(f"  Error:    {r.error}")


if __name__ == "__main__":
    import sys
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("cases.jsonl")
    cases = load_cases(path)
    results = run_all(cases)
    report(results)

    # TODO 4: write results to a dated file under ~/ai-systems/exercises/
    # so you have a regression baseline.
