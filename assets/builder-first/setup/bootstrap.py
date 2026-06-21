#!/usr/bin/env python3
"""One-command builder-first bootstrap for non-learning setup steps.

Runs the following:
1. Ensures Python is supported (3.11, 3.12, or 3.13).
2. Ensures `uv` is available (installs with pip if missing and interactive approval).
3. Creates/refreshes `~/ai-systems/.env` from `.env.example`.
4. Guides API-key onboarding and populates `GEMINI_API_KEY` + `GOOGLE_API_KEY` from env var or prompt.
5. Runs `uv sync` in Group A.
6. Runs `setup/sanity_check.py` in Group A.
7. Skips sync and sanity if already complete when `--fast` is enabled.

This keeps friction out of learner setup while keeping loop content untouched.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Sequence


Command = list[str]


def main() -> int:
    parser = argparse.ArgumentParser(description="Builder-first bootstrap.")
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Fail fast if setup requires a user prompt.",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Skip sync and sanity when setup is already current.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force dependency/sanity refresh even when cache says ready.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the plan and skip all side effects.",
    )
    args = parser.parse_args()

    workspace = (Path(__file__).resolve().parent.parent).expanduser()
    group_a = workspace / "exercises" / "group-A"
    state_file = workspace / ".bootstrap-state.json"

    print("Builder-first setup bootstrap")
    print(f"Workspace: {workspace}")

    if args.dry_run:
        print("DRY RUN: no files will be written, no commands will execute.")
        _print_bootstrap_plan()
        return 0

    if not _check_python_version():
        return 1

    uv = _ensure_uv(non_interactive=args.non_interactive)
    if uv is None:
        print("Could not find/install `uv`.")
        print("Manual fallback: install uv from https://astral.sh/uv and re-run this script.")
        return 1

    key = _ensure_env_file(workspace, interactive=not args.non_interactive)
    if not key:
        return 1

    if args.fast and not args.force and _is_already_bootstrap_ready(group_a, state_file, uv, key):
        print("Builder-first setup already complete. Re-run with --force to refresh uv/sanity.")
        return 0

    if not _run_uv_sync(uv, group_a):
        return 1

    if _run_sanity_check(uv, workspace, group_a) != 0:
        return 1

    _write_bootstrap_state(state_file, uv, group_a, key)
    return 0


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


def _ensure_uv(non_interactive: bool) -> Optional[Command]:
    uv = shutil.which("uv")
    if uv:
        print(f"OK: uv found ({uv})")
        return [uv]

    if non_interactive:
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


def _ensure_env_file(workspace: Path, interactive: bool) -> Optional[str]:
    env_example = workspace / ".env.example"
    env_path = workspace / ".env"

    if not env_example.exists():
        print(f"FAIL: missing {env_example}")
        return None

    existing_key = _read_key_from_env(env_path)
    if existing_key:
        print(f"OK: using existing key from {env_path}")
        return existing_key

    if key := _resolve_api_key_from_context():
        print(f"OK: using API key from environment ({len(key)} chars)")
        content = env_path.read_text() if env_path.exists() else env_example.read_text()
        _write_key(content, env_path, key)
        print(f"Wrote key to {env_path}")
        return key

    _print_api_key_setup()
    if not interactive:
        print("WARN: API key is required in non-interactive mode.")
        print("Set both keys first, then rerun exactly:")
        print("  export GEMINI_API_KEY=<your_key>")
        print("  export GOOGLE_API_KEY=$GEMINI_API_KEY")
        print("  python setup/bootstrap.py --non-interactive --force")
        return None

    key = input("Paste your Gemini API key and press Enter: ").strip()
    if not _looks_like_key(key):
        print("That key looks empty or invalid. Please rerun and paste a full key.")
        return None

    content = env_path.read_text() if env_path.exists() else env_example.read_text()
    _write_key(content, env_path, key)
    print(f"Wrote key to {env_path}")
    return key


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

    google_only = None
    for line in path.read_text().splitlines():
        if line.startswith("GEMINI_API_KEY="):
            value = line.split("=", 1)[1].strip().strip("\"'")
            if _looks_like_key(value):
                return value
        if line.startswith("GOOGLE_API_KEY="):
            value = line.split("=", 1)[1].strip().strip("\"'")
            if _looks_like_key(value):
                google_only = value

    return google_only


def _looks_like_key(value: str) -> bool:
    if not value:
        return False
    value = value.strip()
    if value == "YOUR_KEY_HERE" or value.startswith("YOUR_"):
        return False
    return value.startswith("AIza") and len(value) >= 20


def _print_api_key_setup() -> None:
    print("\nTo continue, we need a Gemini API key. It is a local secret for this workspace and only used to run loops.")
    print("Get one now:")
    print("1) Open https://aistudio.google.com/apikey")
    print("2) Sign in with Google and click \"Create API key\"")
    print("3) Copy the key (looks like \"AIza...\") and paste it when prompted below.")
    print("4) The script writes it to both names below so all loop starters can read it:")
    print("   - GEMINI_API_KEY")
    print("   - GOOGLE_API_KEY")


def _write_key(template: str, path: Path, key: str) -> None:
    updated = template

    if "GEMINI_API_KEY=" in updated:
        updated = re.sub(
            r"^GEMINI_API_KEY=.*$",
            f"GEMINI_API_KEY={key}",
            updated,
            flags=re.MULTILINE,
        )
    else:
        updated = updated.rstrip("\n") + f"\nGEMINI_API_KEY={key}\n"

    if "GOOGLE_API_KEY=" in updated:
        updated = re.sub(
            r"^GOOGLE_API_KEY=.*$",
            f"GOOGLE_API_KEY={key}",
            updated,
            flags=re.MULTILINE,
        )
    else:
        updated = updated.rstrip("\n") + f"\nGOOGLE_API_KEY={key}\n"

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


def _print_bootstrap_plan() -> None:
    print("Planned steps:")
    print("1) Verify Python version support (3.11–3.13).")
    print("2) Resolve uv (or show manual install path if missing).")
    print("3) Read .env.example and prepare ~/ai-systems/.env.")
    print("4) Capture Gemini key and write GEMINI_API_KEY + GOOGLE_API_KEY.")
    print("5) Run `uv sync` in Group A.")
    print("6) Run setup/sanity_check.py in Group A.")


def _is_already_bootstrap_ready(
    group_a: Path,
    state_path: Path,
    uv: Sequence[str],
    key: str,
) -> bool:
    if not state_path.exists():
        return False

    if not (group_a / ".venv").exists():
        return False

    pyproject = group_a / "pyproject.toml"
    lock = group_a / "uv.lock"
    if not pyproject.exists() or not lock.exists():
        return False

    try:
        state = json.loads(state_path.read_text())
    except Exception:
        return False

    if state.get("env_key_prefix") != key[:8]:
        return False
    if state.get("uv") != uv[0]:
        return False
    if state.get("pyproject_mtime") != pyproject.stat().st_mtime:
        return False
    if state.get("lock_mtime") != lock.stat().st_mtime:
        return False
    return True


def _write_bootstrap_state(state_path: Path, uv: Sequence[str], group_a: Path, key: str) -> None:
    data = {
        "env_key_prefix": key[:8],
        "uv": uv[0],
        "pyproject_mtime": (group_a / "pyproject.toml").stat().st_mtime,
        "lock_mtime": (group_a / "uv.lock").stat().st_mtime,
        "updated_at": datetime.now().isoformat(),
    }
    state_path.write_text(json.dumps(data))


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
