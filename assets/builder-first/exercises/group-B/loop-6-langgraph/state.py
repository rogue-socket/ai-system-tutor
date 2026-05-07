"""State for the LangGraph agent.

LangGraph tracks state across nodes via a TypedDict. Each node returns a
partial state update; LangGraph merges via reducers (the `Annotated[..., op]`
pattern below). Fields without reducers get last-write-wins.

`total=False` lets us start with an incomplete state and have nodes fill it in.
"""
import operator
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage


class AgentState(TypedDict, total=False):
    user_input: str

    # Set by the router node (Stage 1) — one of: "math", "lookup", "chat".
    route: str

    # Set by the math branch (Stage 2).
    math_result: str

    # Set by the parallel search branches (Stage 3) — both backends append here.
    # The reducer merges by concatenation; without it, a parallel write would error.
    search_results: Annotated[list[str], operator.add]

    # Set by the chat branch (Stage 4 — or just the default branch).
    chat_response: str

    # The final assembled answer the synthesize node produces.
    final_answer: str

    # Conversation history (LangChain messages). Reducer = append.
    messages: Annotated[list[BaseMessage], operator.add]
