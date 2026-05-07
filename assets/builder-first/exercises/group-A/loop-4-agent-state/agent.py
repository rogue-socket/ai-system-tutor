"""Loop 4 starter — agent state: memory, context, tools.

Back to native function calling (Loop 3's text parsing was a deliberate
detour for ReAct mechanics). Now the focus is the *state* of an agent,
made manipulable.

The starter wires short-term history and a partial tool registry. Memory
modules and context compaction are defined but mostly UN-WIRED. Your job
is to wire them across 5 stages — see BREAK.md.

Run:    python agent.py
Goal:   WIN.md
"""
import os

from dotenv import find_dotenv, load_dotenv
from google import genai
from google.genai import types

import memory
from tools import REGISTRY

load_dotenv(find_dotenv(usecwd=True))
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SYSTEM_PROMPT_BASE = """You are a helpful assistant with memory.

When asked to remember something for later, use the `remember` tool. The user
can also edit your long-term memory directly between sessions, so always check
what you already know before asking.
"""

history: list[types.Content] = []


def system_prompt() -> str:
    """Build the system prompt for this turn.

    Stage 1: prepend a 'what we know' block from long-term memory so the
    model sees stored facts at the top of every turn.
    """
    return SYSTEM_PROMPT_BASE


def turn(user_message: str) -> str:
    history.append(types.Content(role="user", parts=[types.Part(text=user_message)]))
    while True:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt(),
                tools=list(REGISTRY.values()),
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            ),
        )
        if response.function_calls:
            history.append(response.candidates[0].content)
            tool_parts = []
            for call in response.function_calls:
                fn = REGISTRY.get(call.name)
                if fn is None:
                    result = f"ERROR: unknown tool {call.name!r}. Available: {list(REGISTRY.keys())}"
                else:
                    try:
                        result = fn(**(call.args or {}))
                    except Exception as e:
                        result = f"ERROR: {type(e).__name__}: {e}"
                tool_parts.append(types.Part.from_function_response(
                    name=call.name, response={"result": str(result)}
                ))
            history.append(types.Content(role="user", parts=tool_parts))
            continue
        text = response.text or ""
        history.append(types.Content(role="model", parts=[types.Part(text=text)]))
        return text


def main() -> None:
    print("Loop 4 starter — agent state.")
    print(f"Tools: {', '.join(sorted(REGISTRY.keys()))}")
    print(f"Long-term memory: {memory.list_memory()}")
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
