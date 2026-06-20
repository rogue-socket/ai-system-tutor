#!/usr/bin/env python3
"""One-command builder-first bootstrap for non-learning setup steps.

Runs the following:
1. Ensures Python is supported (3.11, 3.12, or 3.13).
2. Ensures `uv` is available (installs with pip if missing and interactive approval).
3. Creates/refreshes `~/ai-systems/.env` from `.env.example`.
4. Guides API-key onboarding and populates `GEMINI_API_KEY` from env var or prompt.
5. Runs `uv sync` in Group A.
6. Runs `setup/sanity_check.py` in Group A.

This keeps friction out of learner setup while keeping loop content untouched.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Sequence


Command = list[str]


def main() -> int:
    workspace = (Path(__file__).resolve().parent.parent).expanduser()
    group_a = workspace / "exercises" / "group-A"

    print("Builder-first setup bootstrap")
    print(f"Workspace: {workspace}")

    if not _check_python_version():
        return 1

    uv = _ensure_uv()
    if uv is None:
        print("Could not find/install `uv`.")
        print("Manual fallback: install uv from https://astral.sh/uv and re-run this script.")
        return 1

    if not _ensure_env_file(workspace):
        return 1

    if not _run_uv_sync(uv, group_a):
        return 1

    return _run_sanity_check(uv, workspace, group_a)


def _check_python_version() -> bool:
    version = sys.version_info
    if version < (3, 11) or version >= (3, 14):
        print(
            "FAIL: Unsupported Python version "
            f"{version.major}.{version.minor}."
        )
        print("Builder-first supports Python 3.11, 3.12, or 3.13.")
        print("Use a supported interpreter and re-run this script.")
        return False
    print(f"OK: Python {version.major}.{version.minor}.{version.micro}")
    return True


def _ensure_uv() -> Optional[Command]:
    uv = shutil.which("uv")
    if uv:
        print(f"OK: uv found ({uv})")
        return [uv]

    if not sys.stdin.isatty():
        print("WARN: uv not found and this session is non-interactive.")
        return None

    print("uv is not installed, but it is required for setup.")
    if not _prompt_yes_no("Install uv with `python -m pip install uv` now", default=True):
        return None

    print("Installing uv ...")
    rc = _run_command([sys.executable, "-m", "pip", "install", "uv"])
    if rc != 0:
        print("WARN: pip install uv failed.")
        print("Please install uv manually from https://astral.sh/uv and re-run this script.")
        return None

    uv = shutil.which("uv")
    if not uv:
        if _run_command([sys.executable, "-m", "uv", "--version"]) == 0:
            print("OK: uv available as `python -m uv`.")
            return [sys.executable, "-m", "uv"]

        # pip installed; maybe needs shell restart.
        print("WARN: uv installed, but shell PATH does not expose it yet.")
        print("Re-run shell (or use `python -m uv`) and re-run this script.")
        return None

    print(f"OK: uv installed ({uv})")
    return [uv]


def _ensure_env_file(workspace: Path) -> bool:
    env_example = workspace / ".env.example"
    env_path = workspace / ".env"

    if not env_example.exists():
        print(f"FAIL: missing {env_example}")
        return False

    existing_key = _read_key_from_env(env_path)
    if existing_key:
        print(f"OK: using existing key from {env_path}")
        return True

    if key := _resolve_api_key_from_context():
        print(f"OK: using API key from environment ({len(key)} chars)")
        content = env_path.read_text() if env_path.exists() else env_example.read_text()
        _write_key(content, env_path, key)
        print(f"Wrote key to {env_path}")
        return True

    _print_api_key_setup()
    if not sys.stdin.isatty():
        return False

    key = input("Paste your Gemini API key and press Enter: ").strip()
    if not _looks_like_key(key):
        print("That key looks empty or invalid. Please rerun and paste a full key.")
        return False

    content = env_path.read_text() if env_path.exists() else env_example.read_text()
    _write_key(content, env_path, key)
    print(f"Wrote key to {env_path}")
    return True


def _resolve_api_key_from_context() -> Optional[str]:
    explicit = os.environ.get("GEMINI_API_KEY", "").strip()
    if _looks_like_key(explicit):
        return explicit

    explicit_google = os.environ.get("GOOGLE_API_KEY", "").strip()
    if explicit_google and explicit_google.startswith("AIza"):
        return explicit_google

    return None


def _read_key_from_env(path: Path) -> Optional[str]:
    if not path.exists():
        return None

    for line in path.read_text().splitlines():
        if not line.startswith("GEMINI_API_KEY="):
            continue
        value = line.split("=", 1)[1].strip().strip('"\'')
        if _looks_like_key(value):
            return value
        return None
    return None


def _looks_like_key(value: str) -> bool:
    if not value:
        return False
    value = value.strip()
    if value == "YOUR_KEY_HERE" or value.startswith("YOUR_"):
        return False
    return value.startswith("AIza") and len(value) >= 20


def _print_api_key_setup() -> None:
    print("\nTo continue, we need a Gemini API key. It is a short secret used by this course to call Gemini APIs.")
    print("You can keep it in this workspace's `.env` file; it is only used locally.")
    print("Get one now:")
    print("1) Open https://aistudio.google.com/apikey")
    print("2) Sign in with Google and click \"Create API key\"")
    print("3) Copy the key (looks like \"AIza...\") and paste it when prompted below.")


def _write_key(template: str, path: Path, key: str) -> None:
    if path.exists() and "GEMINI_API_KEY=" in template:
        updated = re.sub(
            r"^GEMINI_API_KEY=.*$",
            f"GEMINI_API_KEY={key}",
            template,
            flags=re.MULTILINE,
        )
    else:
        updated = template.rstrip("\n") + f"\nGEMINI_API_KEY={key}\n"

    path.write_text(updated)


def _run_uv_sync(uv: Command, group_dir: Path) -> bool:
    if not group_dir.exists():
        print(f"FAIL: missing group directory {group_dir}")
        return False

    print("\nInstalling dependencies for Group A (first-time sync)...")
    rc = _run_command([*uv, "sync"], cwd=group_dir)
    return rc == 0


def _run_sanity_check(uv: Command, workspace: Path, group_dir: Path) -> int:
    script = workspace / "setup" / "sanity_check.py"
    if not script.exists():
        print(f"FAIL: missing sanity check at {script}")
        return 1

    print("\nRunning setup sanity check against Gemini...")
    return _run_command([*uv, "run", "python", str(script)], cwd=group_dir)


def _run_command(cmd: Sequence[str], cwd: Optional[Path] = None) -> int:
    display = " ".join(cmd)
    print(f"$ {display}")
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None).returncode


def _prompt_yes_no(prompt: str, *, default: bool = True) -> bool:
    suffix = " [Y/n] " if default else " [y/N] "
    while True:
        choice = input(prompt + suffix).strip().lower()
        if not choice:
            return default
        if choice in {"y", "yes"}:
            return True
        if choice in {"n", "no"}:
            return False
        print("Please answer y or n.")


if __name__ == "__main__":
    sys.exit(main())
