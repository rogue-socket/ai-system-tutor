"""Loop 2 tools — starts with a single calculator.

You will add more tools here as the loop progresses (a mock get_weather, etc.).
"""


def calculator(a: float, b: float, op: str) -> float:
    """Perform a basic arithmetic operation. Raises on bad input."""
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
    raise ValueError(f"unknown op: {op!r}. Supported: +, -, *, /")
