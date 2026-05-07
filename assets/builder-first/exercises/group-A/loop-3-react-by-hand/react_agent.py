"""Loop 3 starter — ReAct by hand.

Reason-Act-Observe with text parsing. No native function calling here — that
was Loop 2's win. ReAct is *deliberately* parsing structured text, because
the lesson is what goes wrong with that.

It works on simple tasks. It breaks on complex ones. Read BREAK.md.

Run:    python react_agent.py
Goal:   WIN.md
"""
import os
import re

from dotenv import find_dotenv, load_dotenv
from google import genai
from google.genai import types

import traces
from tools import calculator, search

load_dotenv(find_dotenv(usecwd=True))
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SYSTEM_PROMPT = """You are a reasoning agent. For each task, alternate:

Thought: <one-sentence reasoning about what to do next>
Action: <tool>(<args>)
Observation: <will be filled in for you, do NOT write this yourself>

Available tools:
- search(query: str) — look up a fact, returns a string
- calculator(a: float, b: float, op: str) — compute. op is one of: +, -, *, /

When you have the final answer, output:
Final Answer: <your answer>

Output ONE Thought + Action at a time, then wait for the Observation. Do not predict the Observation yourself.
"""

ACTION_RE = re.compile(r"Action:\s*(\w+)\((.*)\)", re.IGNORECASE)
FINAL_RE = re.compile(r"Final Answer:\s*(.+)", re.IGNORECASE | re.DOTALL)


def parse_action(text: str) -> tuple[str, str] | None:
    """Try to extract Action: tool(args). Brittle on purpose."""
    m = ACTION_RE.search(text)
    if not m:
        return None
    return m.group(1), m.group(2)


def run_action(tool: str, args_str: str) -> str:
    """Dispatch the action. Brittle parsing of args."""
    if tool == "search":
        q = args_str.strip().strip('"').strip("'")
        return search(q)
    if tool == "calculator":
        parts = [p.strip().strip('"').strip("'") for p in args_str.split(",")]
        a = float(parts[0])
        b = float(parts[1])
        op = parts[2]
        return str(calculator(a, b, op))
    raise ValueError(f"unknown tool: {tool}")


def react(task: str) -> str:
    trace_path = traces.new_trace(task)
    history: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=task)])
    ]
    while True:  # No max-iteration cap. That's part of what's broken.
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=history,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        text = (response.text or "").strip()
        history.append(types.Content(role="model", parts=[types.Part(text=text)]))

        for line in text.splitlines():
            if line.lower().startswith("thought:"):
                traces.log(trace_path, "thought", text=line.split(":", 1)[1].strip())

        m = FINAL_RE.search(text)
        if m:
            answer = m.group(1).strip()
            traces.log(trace_path, "final", text=answer)
            return answer

        action = parse_action(text)
        if action is None:
            traces.log(trace_path, "error", kind="no_action_found", msg=text[:200])
            history.append(types.Content(
                role="user",
                parts=[types.Part(text="Observation: (no action found, continue)")],
            ))
            continue

        tool, args_str = action
        traces.log(trace_path, "action", tool=tool, args=args_str)

        try:
            result = run_action(tool, args_str)
        except Exception as e:
            result = f"ERROR: {type(e).__name__}: {e}"
            traces.log(trace_path, "error", kind=type(e).__name__, msg=str(e))

        traces.log(trace_path, "observation", text=result)
        history.append(types.Content(
            role="user",
            parts=[types.Part(text=f"Observation: {result}")],
        ))


def main() -> None:
    print("Loop 3 starter — ReAct by hand.")
    print("Try: 'find the population of the capital of France, then multiply by 2'.")
    print("After each task, run `python traces.py` to inspect the latest trace.")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            task = input("task> ")
        except EOFError:
            return
        if task.strip().lower() in {"exit", "quit"}:
            return
        if not task.strip():
            continue
        try:
            answer = react(task)
            print(f"answer> {answer}\n")
        except KeyboardInterrupt:
            print("\n(interrupted — check traces/)")
        except Exception as e:
            print(f"crash> {type(e).__name__}: {e}\n")


if __name__ == "__main__":
    main()
