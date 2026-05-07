"""Shared benchmark for Loops 7a, 7b, and 9.

A small set of word problems with known answers. Comparable across:
- Loop 7a — single-agent architectures (baseline, reflexion, planner-executor, self-consistency)
- Loop 7b — multi-agent architectures (hierarchical, orchestrator-worker, peer)
- Loop 9 — production eval harness (LLM-as-judge layered on top)

The learner builds ONE benchmark across three loops. Don't rewrite it; extend it.
"""
import re
import time
from collections.abc import Callable
from dataclasses import dataclass, field

TASKS: list[dict] = [
    {"q": "If a train travels 60 miles in 1.5 hours, what's its average speed in mph?", "a": "40"},
    {"q": "What is 17 * 23 + 5?", "a": "396"},
    {"q": "How many minutes are there in 3.5 hours?", "a": "210"},
    {"q": "If you have 8 apples and eat 3, how many are left?", "a": "5"},
    {"q": "What's 25% of 80?", "a": "20"},
    {"q": "If x + 7 = 15, what's x?", "a": "8"},
    {"q": "How many sides does a hexagon have?", "a": "6"},
    {"q": "What's the square root of 144?", "a": "12"},
    {"q": "If a recipe needs 2 cups of flour for 4 people, how many cups for 10 people?", "a": "5"},
    {"q": "What is 2 to the 8th power?", "a": "256"},
]


@dataclass
class TaskResult:
    task: dict
    answer: str
    correct: bool
    latency_ms: float
    cost_tokens: int = 0
    iterations: int = 1
    error: str | None = None


@dataclass
class BenchmarkResult:
    architecture: str
    results: list[TaskResult] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        if not self.results:
            return 0.0
        return sum(1 for r in self.results if r.correct) / len(self.results)

    @property
    def avg_latency_ms(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.latency_ms for r in self.results) / len(self.results)

    @property
    def total_tokens(self) -> int:
        return sum(r.cost_tokens for r in self.results)

    @property
    def total_iterations(self) -> int:
        return sum(r.iterations for r in self.results)


def check_answer(predicted: str, expected: str) -> bool:
    """Loose match: extract first number from prediction, compare to expected.

    Loop 9 will replace this with LLM-as-judge for harder tasks. For Loop 7a/7b's
    numeric word problems, regex extraction is good enough.
    """
    nums = re.findall(r"-?\d+\.?\d*", predicted)
    if not nums:
        return predicted.strip() == expected.strip()
    try:
        return abs(float(nums[0]) - float(expected)) < 0.01
    except ValueError:
        return predicted.strip() == expected.strip()


def run_benchmark(
    architecture_name: str,
    agent_fn: Callable[[str], dict],
    tasks: list[dict] | None = None,
) -> BenchmarkResult:
    """Run an agent over the benchmark.

    `agent_fn(question)` must return a dict with keys: `answer` (str), `tokens` (int),
    `iterations` (int). All four starter files conform.
    """
    tasks = tasks or TASKS
    bench = BenchmarkResult(architecture=architecture_name)
    for task in tasks:
        start = time.perf_counter()
        try:
            result = agent_fn(task["q"])
            latency_ms = (time.perf_counter() - start) * 1000
            answer = str(result.get("answer", ""))
            tokens = int(result.get("tokens", 0))
            iters = int(result.get("iterations", 1))
            correct = check_answer(answer, task["a"])
            bench.results.append(TaskResult(
                task=task, answer=answer, correct=correct,
                latency_ms=latency_ms, cost_tokens=tokens, iterations=iters,
            ))
        except Exception as e:
            latency_ms = (time.perf_counter() - start) * 1000
            bench.results.append(TaskResult(
                task=task, answer="", correct=False,
                latency_ms=latency_ms, error=f"{type(e).__name__}: {e}",
            ))
    return bench


def print_summary(bench: BenchmarkResult) -> None:
    print(f"\n=== {bench.architecture} ===")
    print(f"Accuracy: {bench.accuracy:.0%} ({sum(1 for r in bench.results if r.correct)}/{len(bench.results)})")
    print(f"Avg latency: {bench.avg_latency_ms:.0f} ms")
    print(f"Total tokens: {bench.total_tokens}")
    print(f"Total iterations: {bench.total_iterations}")
    for r in bench.results:
        mark = "PASS" if r.correct else "FAIL"
        err = f" [{r.error}]" if r.error else ""
        q_short = r.task["q"][:50] + ("..." if len(r.task["q"]) > 50 else "")
        print(f"  [{mark}] ({r.iterations} iter, {r.cost_tokens} tok) {q_short} -> {r.answer[:30]}{err}")
