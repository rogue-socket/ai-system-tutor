"""Loop 5 starter — LangChain.

Minimal LangChain agent with one tool. It runs out of the box. It has no
memory yet, no second tool, and no MCP integration. Your task across 5
stages is to extend it — see BREAK.md.

Run:    python langchain_agent.py
Goal:   WIN.md
"""
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(find_dotenv(usecwd=True))
# ChatGoogleGenerativeAI reads GOOGLE_API_KEY; the rest of builder-first uses
# GEMINI_API_KEY. Alias so learners only have to set one in .env.
os.environ.setdefault("GOOGLE_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


@tool
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


SYSTEM_PROMPT = (Path(__file__).parent / "prompts" / "system.txt").read_text()

# Stage 3 hint: add MessagesPlaceholder("chat_history") here once you wire
# memory into the prompt.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

tools = [calculator]
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def main() -> None:
    print("Loop 5 starter — LangChain.")
    print(f"Tools: {[t.name for t in tools]}")
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
            result = executor.invoke({"input": user})
            print(f"agent> {result['output']}\n")
        except Exception as e:
            print(f"crash> {type(e).__name__}: {e}\n")


if __name__ == "__main__":
    main()
