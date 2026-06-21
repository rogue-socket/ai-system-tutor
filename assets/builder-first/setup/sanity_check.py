"""Sanity check: validates Gemini API key + makes one real call.

Run from any group env:
    python ~/ai-systems/setup/group_env.py --group <A|B|C|D> --run python setup/sanity_check.py
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
        print("Run `python setup/group_env.py --group <X> --run python setup/sanity_check.py` for your group.")
        return 1

    env_path = find_dotenv(usecwd=True) or str(Path.home() / "ai-systems" / ".env")
    if not Path(env_path).exists():
        print(f"FAIL: no .env found (looked at {env_path}).")
        print("Rerun:")
        print("  python setup/bootstrap.py")
        print("If you are in a non-interactive environment, set GEMINI_API_KEY first, then run:")
        print("  python setup/group_env.py --group A --run python setup/sanity_check.py")
        print("Manual fallback (legacy): copy .env.example to .env at ~/ai-systems/, then add your GEMINI_API_KEY.")
        print("See setup/README.md step 2 for the legacy click-path.")
        return 1

    load_dotenv(env_path)
    key = _read_api_key_from_env()
    if not key or key.startswith("YOUR_"):
        print("FAIL: API key missing or unset in .env")
        print("Use one of:")
        print("  1) python setup/bootstrap.py (recommended)")
        print("  2) set GEMINI_API_KEY or GOOGLE_API_KEY in your environment and rerun")
        print(f"  3) manual fallback: edit {env_path} and replace YOUR_KEY_HERE with your real key.")
        return 1

    print(f"Found API key (length {len(key)}).")
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


def _read_api_key_from_env() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key and key != "YOUR_KEY_HERE" and not key.startswith("YOUR_"):
        return key

    return os.environ.get("GOOGLE_API_KEY", "").strip()


if __name__ == "__main__":
    sys.exit(main())
