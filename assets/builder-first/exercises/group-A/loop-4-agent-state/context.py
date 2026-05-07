"""Context budgeting and compaction.

Tracks token count across the conversation. When over budget, you compact
older messages into a summary so the conversation can continue without
hitting the context window.

The starter has the SHAPE of compaction but doesn't WIRE it in. Stage 3 of
your task is to wire it.
"""
from google import genai
from google.genai import types

# Soft limit. Trigger compaction when exceeded.
TOKEN_BUDGET = 3000

# How many recent messages to keep verbatim after compaction.
KEEP_RECENT = 4


def estimate_tokens(history: list[types.Content]) -> int:
    """Rough token count. ~4 chars per token. Replace with the SDK's count_tokens for accuracy."""
    total = 0
    for content in history:
        for part in content.parts or []:
            if part.text:
                total += len(part.text) // 4
    return total


def compact(client: genai.Client, history: list[types.Content]) -> list[types.Content]:
    """Summarize older messages, keep the recent ones verbatim.

    Returns a new history list. Does NOT mutate the input.
    Wire this into agent.py's turn loop in Stage 3.
    """
    if len(history) <= KEEP_RECENT:
        return history

    older = history[:-KEEP_RECENT]
    recent = history[-KEEP_RECENT:]

    summary_prompt_parts = [
        "Summarize the following conversation in 3-5 short bullet points.",
        "Keep facts, decisions, and any references to long-term memory keys.",
        "Drop pleasantries and tool-call mechanics.",
        "",
    ]
    for content in older:
        role = content.role or "user"
        for part in content.parts or []:
            if part.text:
                summary_prompt_parts.append(f"{role}: {part.text}")
    summary_prompt = "\n".join(summary_prompt_parts)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=summary_prompt,
    )
    summary_text = (response.text or "").strip()

    summary_message = types.Content(
        role="user",
        parts=[types.Part(text=f"[Earlier conversation summary]:\n{summary_text}")],
    )
    return [summary_message] + recent
