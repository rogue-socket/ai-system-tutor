"""Sanity check: validates Gemini API key + makes one real call.

Run from any group venv after `uv sync`:
    python ~/ai-systems/setup/sanity_check.py
"""
import os
import sys
from pathlib import Path


def main() -> int:
    try:
        from dotenv import find_dotenv, load_dotenv
        from google import genai
    except ImportError as e:
        print(f"FAIL: missing package — {e.name}")
        print("Run `uv sync` from your active group directory first, then re-run this.")
        return 1

    env_path = find_dotenv(usecwd=True) or str(Path.home() / "ai-systems" / ".env")
    if not Path(env_path).exists():
        print(f"FAIL: no .env found (looked at {env_path}).")
        print("Copy .env.example to .env at ~/ai-systems/, then add your GEMINI_API_KEY.")
        print("See setup/README.md step 2 for the click-path.")
        return 1

    load_dotenv(env_path)
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key or key.startswith("YOUR_"):
        print("FAIL: GEMINI_API_KEY missing or unset in .env")
        print(f"Edit {env_path} and replace YOUR_KEY_HERE with your real key.")
        return 1

    print(f"Found GEMINI_API_KEY (length {len(key)}).")
    print("Making one test call to gemini-2.0-flash...")

    try:
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Reply with exactly: OK",
        )
        text = (response.text or "").strip()
        print(f"Response: {text}")
        print("\nPASS: Gemini works. Setup is complete.")
        return 0
    except Exception as e:
        print(f"FAIL: API call errored — {type(e).__name__}: {e}")
        print("Common causes: invalid key, billing not enabled, rate limit, network.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
