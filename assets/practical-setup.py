#!/usr/bin/env python3
"""Practical-mode exercise bootstrap: deps + optional API key capture."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Sequence


Command = list[str]

DEFAULT_DEPS = ["httpx", "pydantic", "openai", "anthropic", "numpy"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Smooth practical exercise setup.")
    parser.add_argument(
        "--deps",
        nargs="+",
        default=DEFAULT_DEPS,
        help="Packages to install (space-separated).",
    )
    parser.add_argument(
        "--require-key",
        action="append",
        default=[],
        metavar="ENV_VAR",
        help="Environment variable name(s) required for the exercise (e.g. OPENAI_API_KEY).",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Fail fast if setup needs a manual prompt.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned commands and required inputs, without running anything.",
    )
    parser.add_argument(
        "--write-keys-to-dotenv",
        action="store_true",
        help="Write prompted keys to .env in the current directory.",
    )
    parser.add_argument(
        "--skip-deps",
        action="store_true",
        help="Skip package installation.",
    )
    args = parser.parse_args()

    required_keys = _normalize_require_key_args(args.require_key)
    if args.dry_run:
        _print_dry_run(args, required_keys)
        return 0

    install_tool = _resolve_installer()
    if install_tool is None:
        print("FAIL: neither `uv` nor `python -m pip` works in this environment.")
        return 1

    if not args.skip_deps:
        if _run_command([*install_tool, "install", *args.deps]) != 0:
            return 1

    interactive = not args.non_interactive and sys.stdin.isatty()
    for key in required_keys:
        if _resolve_key(
            key,
            write_dotenv=args.write_keys_to_dotenv,
            required_keys=required_keys,
            interactive=interactive,
            args=args,
        ):
            continue
        return 1

    print("Setup complete.")
    if required_keys:
        print(f"Verified API key env vars: {', '.join(required_keys)}")
    return 0


def _normalize_require_key_args(values: Sequence[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()

    for raw in values:
        for key_name in raw.split(","):
            cleaned = key_name.strip()
            if not cleaned:
                continue
            canonical = cleaned.upper()
            if canonical not in seen:
                ordered.append(canonical)
                seen.add(canonical)
    return ordered


def _print_dry_run(args: argparse.Namespace, required_keys: list[str]) -> None:
    print("DRY RUN: no commands will run.")
    if args.skip_deps:
        print("Package install: skipped (--skip-deps)")
    else:
        install_tool = _resolve_installer()
        if install_tool:
            install_cmd = " ".join([*install_tool, "install", *args.deps])
            print(f"Planned install: $ {install_cmd}")

    if required_keys:
        print("Planned key requirements:")
        for key_name in required_keys:
            info = _key_provider_help(key_name)
            print(f"- {key_name} ({info['name']})")
            if info["url"]:
                print(f"  Get from: {info['url']}")
    else:
        print("No key required for this run.")

    print(f"Planned run command: $ python {Path(__file__).name} {_build_run_flags(args, required_keys)}")


def _build_run_flags(args: argparse.Namespace, required_keys: list[str]) -> str:
    flags: list[str] = []
    if args.skip_deps:
        flags.append("--skip-deps")
    if args.non_interactive:
        flags.append("--non-interactive")
    if args.write_keys_to_dotenv:
        flags.append("--write-keys-to-dotenv")
    if args.deps != DEFAULT_DEPS:
        flags.extend(["--deps", *args.deps])
    for key_name in required_keys:
        flags.extend(["--require-key", key_name])
    return " ".join(flags)


def _resolve_installer() -> Optional[Command]:
    uv = shutil.which("uv")
    if uv:
        return [uv, "pip"]

    if _try_python_uv():
        return [sys.executable, "-m", "uv", "pip"]

    return [sys.executable, "-m", "pip"]


def _try_python_uv() -> bool:
    try:
        return (
            subprocess.run([sys.executable, "-m", "uv", "--version"], check=False).returncode == 0
        )
    except Exception:
        return False


def _resolve_key(
    key_name: str,
    *,
    write_dotenv: bool,
    required_keys: list[str],
    interactive: bool,
    args: argparse.Namespace,
) -> bool:
    existing = os.environ.get(key_name, "").strip()
    if _looks_like_key(existing):
        return True

    candidate = _read_key_from_env_file(Path.cwd() / ".env", key_name)
    if candidate:
        os.environ[key_name] = candidate
        return True

    if not interactive:
        print(f"FAIL: {key_name} is not set.")
        _print_non_interactive_resume_hint(required_keys=required_keys, args=args)
        return False

    _print_key_lookup_prompt(key_name)
    key = input(f"{key_name} = ").strip()
    if not key:
        print(f"FAIL: empty {key_name}.")
        return False
    if not _looks_like_key(key):
        print("That value looks empty or placeholder-like. Please rerun and paste a real key.")
        return False

    os.environ[key_name] = key
    if write_dotenv:
        _append_to_dotenv(Path.cwd() / ".env", key_name, key)
    return True


def _print_non_interactive_resume_hint(required_keys: list[str], args: argparse.Namespace) -> None:
    print("Set each required key first, then re-run:")
    for key_name in required_keys:
        print(f"  {key_name}=<your_key>")
    flags = _build_run_flags(args, required_keys).strip()
    if flags:
        print(f"  python {Path(__file__).name} {flags}")
    else:
        print(f"  python {Path(__file__).name}")


def _print_key_lookup_prompt(key_name: str) -> None:
    provider = _key_provider_help(key_name)
    print(f"\nTo continue, we need {key_name} for {provider['name']}.")
    if provider["url"]:
        print(f"Get one at: {provider['url']}")
    print("Paste the raw key value when prompted (no quotes, no prefix text).")
    if provider["example"]:
        print(f"Example shape: {provider['example']}")


def _key_provider_help(key_name: str) -> dict[str, str]:
    key = key_name.upper()
    if key == "OPENAI_API_KEY":
        return {
            "name": "OpenAI",
            "url": "https://platform.openai.com/api-keys",
            "example": "sk-... / sk-proj-...",
        }
    if key == "ANTHROPIC_API_KEY":
        return {
            "name": "Anthropic",
            "url": "https://console.anthropic.com/settings/keys",
            "example": "sk-ant-...",
        }
    if key in {"GEMINI_API_KEY", "GOOGLE_API_KEY"}:
        return {
            "name": "Google Gemini",
            "url": "https://aistudio.google.com/apikey",
            "example": "AIza...",
        }
    return {
        "name": "provider",
        "url": "",
        "example": "<provider key>",
    }


def _read_key_from_env_file(dotenv_path: Path, key_name: str) -> str:
    if not dotenv_path.exists():
        return ""

    for line in dotenv_path.read_text().splitlines():
        if not line.startswith(f"{key_name}="):
            continue
        return line.split("=", 1)[1].strip().strip("\"'")
    return ""


def _append_to_dotenv(dotenv_path: Path, key_name: str, key_value: str) -> None:
    existing = dotenv_path.read_text() if dotenv_path.exists() else ""
    if f"{key_name}=" in existing:
        lines = [
            (f"{key_name}={key_value}" if line.startswith(f"{key_name}=") else line)
            for line in existing.splitlines()
        ]
        dotenv_path.write_text("\n".join(lines) + "\n")
    else:
        dotenv_path.write_text(existing.rstrip("\n") + f"\n{key_name}={key_value}\n")


def _looks_like_key(value: str) -> bool:
    value = value.strip()
    if not value or value.startswith("YOUR_") or value.startswith("your_"):
        return False
    return len(value) >= 6


def _run_command(cmd: Sequence[str]) -> int:
    display = " ".join(cmd)
    print(f"$ {display}")
    return subprocess.run(list(cmd)).returncode


if __name__ == "__main__":
    sys.exit(main())
