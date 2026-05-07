"""Tiny MCP server — exposes one tool: get_random_fact.

This is the SERVER side of the protocol. Run it as a subprocess from
langchain_agent.py in Stage 5. The point is that it could equally well
be a server you didn't write — Anthropic's, GitHub's, a community one,
your colleague's. The protocol is the boundary.

Run standalone (for testing the server alone):
    python mcp_server.py

Or have your agent spawn it (Stage 5):
    StdioServerParameters(command="python", args=["mcp_server.py"])
"""
import random

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("loop-5-demo")

FACTS = [
    "An octopus has three hearts and blue blood.",
    "Honey never spoils; archaeologists have eaten 3000-year-old honey.",
    "Bananas are berries; strawberries are not.",
    "A group of flamingos is called a flamboyance.",
    "The shortest war in history lasted 38 minutes (Britain vs. Zanzibar, 1896).",
    "Wombat poop is cube-shaped.",
    "Sharks are older than trees.",
]


@mcp.tool()
def get_random_fact() -> str:
    """Return a random interesting fact."""
    return random.choice(FACTS)


@mcp.tool()
def echo(text: str) -> str:
    """Echo the input text back. Useful for verifying the connection."""
    return text


if __name__ == "__main__":
    mcp.run()
