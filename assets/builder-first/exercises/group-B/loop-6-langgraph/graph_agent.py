"""Loop 6 starter — LangGraph.

The same kind of agent as Loop 5, but expressed as a graph. The starter
builds a 2-node linear graph that doesn't need to be a graph — it could be
a chain. That's the point. Your task across 5 stages is to make it earn its
graph-ness with conditional routing and parallel branches.

Run:    python graph_agent.py
Goal:   WIN.md
"""
import os

from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph

from state import AgentState

load_dotenv(find_dotenv(usecwd=True))
# ChatGoogleGenerativeAI reads GOOGLE_API_KEY; alias from GEMINI_API_KEY.
os.environ.setdefault("GOOGLE_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


def receive(state: AgentState) -> dict:
    """Wrap the user input as a HumanMessage."""
    return {"messages": [HumanMessage(content=state["user_input"])]}


def llm_call(state: AgentState) -> dict:
    """Send to the LLM, capture the response into final_answer."""
    response = llm.invoke(state["messages"])
    return {
        "messages": [response],
        "final_answer": response.content,
    }


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("receive", receive)
    g.add_node("llm", llm_call)
    g.add_edge(START, "receive")
    g.add_edge("receive", "llm")
    g.add_edge("llm", END)
    return g.compile()


graph = build_graph()


def main() -> None:
    print("Loop 6 starter — LangGraph.")
    print("This graph is currently a chain in disguise. Add branches.")
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
            result = graph.invoke({"user_input": user})
            print(f"agent> {result.get('final_answer', '<no answer>')}\n")
        except Exception as e:
            print(f"crash> {type(e).__name__}: {e}\n")


if __name__ == "__main__":
    main()
