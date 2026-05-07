"""Loop 4 tool registry — manipulable mid-conversation.

The registry is a dict you can mutate. Loop 4's goal: hot-swap tools and
watch behavior change. Add /tools commands in agent.py to list, add, remove.

Note that `recall` is intentionally NOT in the starter REGISTRY. The agent
can write to long-term memory but cannot read it back. Stage 1 of your
task is to fix that.
"""
from collections.abc import Callable

import memory


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


def get_weather(city: str) -> str:
    """Mock weather. Returns a hardcoded string for known cities."""
    fake = {
        "paris": "Paris: 18C, partly cloudy.",
        "tokyo": "Tokyo: 22C, sunny.",
        "london": "London: 12C, raining.",
        "new york": "New York: 16C, windy.",
    }
    return fake.get(city.lower().strip(), f"No weather data for {city}")


def remember(key: str, value: str) -> str:
    """Write a fact to long-term memory. Persists across sessions."""
    return memory.remember(key, value)


# REGISTRY — mutable. Add /tools commands in agent.py to mutate this at runtime.
# Note: `recall` and the working-memory tools are intentionally absent. Add them.
REGISTRY: dict[str, Callable] = {
    "calculator": calculator,
    "get_weather": get_weather,
    "remember": remember,
}
