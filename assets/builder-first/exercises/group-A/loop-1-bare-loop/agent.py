"""Loop 1 starter — the dumbest possible LLM call.

Run:    python agent.py
Read:   BREAK.md to see what's missing.
Goal:   WIN.md
"""
import os

from dotenv import find_dotenv, load_dotenv
from google import genai

load_dotenv(find_dotenv(usecwd=True))

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

user_message = "What's the capital of France?"

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=user_message,
)

print(response.text)
