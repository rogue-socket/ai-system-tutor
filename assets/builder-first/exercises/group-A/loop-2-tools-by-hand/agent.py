"""Loop 2 starter — tools by hand.

The model is told to emit JSON when it wants to use a tool. We parse that JSON
with a regex and dispatch. This works *sometimes* and breaks a lot. That's
the point — read BREAK.md.

Run:    python agent.py
Goal:   WIN.md
"""
import json
import os
import re

from dotenv import find_dotenv, load_dotenv
from google import genai
from google.genai import types

from tools import calculator

load_dotenv(find_dotenv(usecwd=True))
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SYSTEM_PROMPT = """You are a helpful assistant with a calculator tool.

When you need to compute something, output ONLY a JSON object on its own line, like:
{"tool": "calculator", "args": {"a": 12, "b": 7, "op": "+"}}

Available ops: +, -, *, /
After the tool result comes back, give the final answer in plain language.
"""

history: list[types.Content] = []


def parse_tool_call(text: str) -> dict | None:
    """Try to extract a JSON tool call from the model's output. Brittle on purpose."""
    match = re.search(r"\{.*?\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def dispatch(call: dict) -> str:
    """Run the tool and return its result as a string."""
    if call.get("tool") == "calculator":
        result = calculator(**call["args"])
        return f"Tool result: {result}"
    return "Tool result: error"


def turn(user_message: str) -> str:
    history.append(types.Content(role="user", parts=[types.Part(text=user_message)]))
    while True:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=history,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        text = (response.text or "").strip()
        history.append(types.Content(role="model", parts=[types.Part(text=text)]))
        call = parse_tool_call(text)
        if call is None:
            return text
        result = dispatch(call)
        history.append(types.Content(role="user", parts=[types.Part(text=result)]))


def main() -> None:
    print("Loop 2 starter — tools by hand.")
    print("Try: 'what's 12 + 7?', 'multiply 9 by 11', 'square root of 144'.")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            user = input("you> ")
        except EOFError:
            return
        if user.strip().lower() in {"exit", "quit"}:
            return
        if not user.strip():
            continue
        try:
            print(f"agent> {turn(user)}\n")
        except Exception as e:
            print(f"crash> {type(e).__name__}: {e}\n")


if __name__ == "__main__":
    main()
