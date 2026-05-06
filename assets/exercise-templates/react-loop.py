"""
Starter scaffold: bounded ReAct loop with one tool.

Fill in the TODOs. Goal: a 50-line agent that answers a 2-3 step factual question
using web search, with a hard cap of 10 iterations and full trace logging.

Usage:
    export ANTHROPIC_API_KEY=...
    python react-loop.py "What's the population of the city where Anthropic is headquartered?"
"""

from __future__ import annotations
import json
import os
import sys
from dataclasses import dataclass, field

# Pick one. Adjust imports.
# from anthropic import Anthropic
# from openai import OpenAI


MAX_ITERATIONS = 10


@dataclass
class TraceStep:
    iteration: int
    thought: str
    action: str | None
    action_input: dict | None
    observation: str | None


@dataclass
class AgentRun:
    question: str
    steps: list[TraceStep] = field(default_factory=list)
    final_answer: str | None = None
    stopped_reason: str | None = None  # "answer" | "max_iterations" | "tool_error"


def search_web(query: str) -> str:
    """
    TODO 1: implement a tool. Easiest: stub out with a dict of {query: result}
    for testing, then swap to DuckDuckGo via `duckduckgo_search` or similar.

    Return a string the model can read.
    """
    raise NotImplementedError


SYSTEM_PROMPT = """\
You are a research agent. Answer the user's question by reasoning step by step
and calling the `search_web` tool when you need information.

After each thought, output exactly one of:
  ACTION: search_web {"query": "..."}
  FINAL: <your answer>

Never invent search results. If a search returns nothing useful, try a different
query or give up with FINAL: I don't know.
"""


def parse_response(text: str) -> tuple[str, dict | None, str | None]:
    """
    Parse model output into (action, action_input, final_answer).
    Exactly one of action/final_answer is non-None.

    TODO 2: handle malformed output. The model will sometimes:
      - Output prose around the ACTION/FINAL line
      - Output multiple ACTION lines (use the first)
      - Output bad JSON (return action=None, final_answer=None to signal retry)
    """
    raise NotImplementedError


def call_model(messages: list[dict]) -> str:
    """
    TODO 3: call the model. Return the assistant's text.
    """
    raise NotImplementedError


def run_agent(question: str) -> AgentRun:
    run = AgentRun(question=question)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for i in range(MAX_ITERATIONS):
        response = call_model(messages)
        action, action_input, final_answer = parse_response(response)

        # TODO 4: append a TraceStep to run.steps for every iteration,
        # whether it was an action or a final answer.

        if final_answer is not None:
            run.final_answer = final_answer
            run.stopped_reason = "answer"
            return run

        if action == "search_web":
            try:
                observation = search_web(**action_input)
            except Exception as e:
                # TODO 5: turn the exception into a structured observation
                # the model can recover from, not a Python traceback.
                observation = f"ERROR: {e}"

            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "user", "content": f"OBSERVATION: {observation}"})
        else:
            # Malformed output. Either re-prompt or abort.
            # TODO 6: decide which.
            run.stopped_reason = "tool_error"
            return run

    run.stopped_reason = "max_iterations"
    return run


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "What is the capital of France?"
    run = run_agent(question)
    print(json.dumps({
        "question": run.question,
        "steps": [s.__dict__ for s in run.steps],
        "final_answer": run.final_answer,
        "stopped_reason": run.stopped_reason,
    }, indent=2))
