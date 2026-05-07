"""Three kinds of memory for Loop 4. Plain Python — no vectors (that's Loop 8).

- short-term: chat history (a list of Content objects). Lives in agent.py.
- working: a dict scratchpad. Ephemeral — dies when the script exits.
- long-term: a JSON file as a key-value store. Persists across sessions.
"""
import json
from pathlib import Path

# Working memory — a transient dict. The learner adds tools that read/write this.
working: dict[str, str] = {}

# Long-term memory — a JSON file. The learner can edit it directly.
LONG_TERM_PATH = Path(__file__).parent / "memory.json"


def load_long_term() -> dict[str, str]:
    if not LONG_TERM_PATH.exists():
        LONG_TERM_PATH.write_text("{}")
    return json.loads(LONG_TERM_PATH.read_text())


def save_long_term(data: dict[str, str]) -> None:
    LONG_TERM_PATH.write_text(json.dumps(data, indent=2))


def remember(key: str, value: str) -> str:
    """Write a key-value pair to long-term memory. Survives across sessions."""
    data = load_long_term()
    data[key] = value
    save_long_term(data)
    return f"Remembered: {key} = {value}"


def recall(key: str) -> str:
    """Read a value from long-term memory. The starter does NOT expose this as a tool."""
    data = load_long_term()
    return data.get(key, f"No memory of {key!r}")


def list_memory() -> str:
    """List all keys currently in long-term memory."""
    data = load_long_term()
    if not data:
        return "Long-term memory is empty."
    return "Long-term memory keys: " + ", ".join(sorted(data.keys()))
