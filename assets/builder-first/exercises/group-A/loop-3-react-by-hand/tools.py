"""Loop 3 tools — calculator (from Loop 2) + a mock search.

Search returns hardcoded results for a small set of queries. The model has to
combine them with the calculator for multi-step tasks.
"""

POPULATIONS = {
    "paris": "Paris has a population of approximately 2.1 million.",
    "tokyo": "Tokyo has a population of approximately 13.9 million.",
    "new york": "New York City has a population of approximately 8.3 million.",
    "london": "London has a population of approximately 9.0 million.",
}

CAPITALS = {
    "france": "The capital of France is Paris.",
    "japan": "The capital of Japan is Tokyo.",
    "united kingdom": "The capital of the United Kingdom is London.",
    "usa": "The capital of the United States is Washington D.C.",
}


def search(query: str) -> str:
    """Mock search. Returns hardcoded results for a small set of queries."""
    q = query.lower().strip()
    if "population" in q:
        for key, val in POPULATIONS.items():
            if key in q:
                return val
    if "capital" in q:
        for key, val in CAPITALS.items():
            if key in q:
                return val
    return f"No results for: {query!r}"


def calculator(a: float, b: float, op: str) -> float:
    """From Loop 2."""
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
