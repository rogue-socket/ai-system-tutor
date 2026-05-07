"""Loop 9 starter agent — minimal, single-turn, blocking.

The point of Loop 9 is not the agent — it's making *this simple agent*
production-ready. The agent is intentionally thin so production concerns
stand out. One tool (calculator), no memory, blocking I/O.

Your task is in BREAK.md. Don't extend this file's logic; wrap it.
"""
import os

from dotenv import find_dotenv, load_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv(usecwd=True))
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SYSTEM_PROMPT = "You are a helpful assistant. Use the calculator tool when math is involved. Reply concisely."


def calculator(a: float, b: float, op: str) -> float:
    """Compute. op is one of: +, -, *, /"""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("cannot divide by zero")
        return a / b
    raise ValueError(f"unknown op: {op!r}")


def answer(question: str) -> dict:
    """Single-turn query. Returns {answer, tokens, tool_calls}."""
    history = [types.Content(role="user", parts=[types.Part(text=question)])]
    tokens = 0
    tool_calls = 0

    while True:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[calculator],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            ),
        )
        usage = response.usage_metadata
        if usage:
            tokens += getattr(usage, "total_token_count", 0) or 0

        if response.function_calls:
            history.append(response.candidates[0].content)
            parts = []
            for call in response.function_calls:
                tool_calls += 1
                if call.name == "calculator":
                    try:
                        result = calculator(**(call.args or {}))
                    except Exception as e:
                        result = f"ERROR: {type(e).__name__}: {e}"
                else:
                    result = f"ERROR: unknown tool {call.name}"
                parts.append(types.Part.from_function_response(
                    name=call.name, response={"result": str(result)}
                ))
            history.append(types.Content(role="user", parts=parts))
            continue

        return {
            "answer": response.text or "",
            "tokens": tokens,
            "tool_calls": tool_calls,
        }
