#!/usr/bin/env python3
"""Builder-first group helper.

Usage:

```bash
# Prepare Group B environment only (sync + instructions).
python setup/group_env.py --group B

# Run a command in that group's uv-managed environment.
python setup/group_env.py --group B --run python langchain_agent.py
```

This keeps the loop instructions focused on learning content while the skill
handles environment plumbing (group path, uv sync, runner command).
"""

from __future__ import annotations

import json
import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Sequence

Command = list[str]


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare and run Builder-first group env.")
    parser.add_argument("--group", required=True, choices=("B", "C", "D", "A"), help="Group letter")
    parser.add_argument(
        "--run",
        nargs="*",
        default=None,
        help="Run this command via `uv run` in the group directory.",
    )
    parser.add_argument(
        "--skip-sync",
        action="store_true",
        help="Skip `uv sync` (useful when you only need a one-off command).",
    )
    parser.add_argument(
        "--force-sync",
        action="store_true",
        help="Always run `uv sync` even if cache says this group is already ready.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show group-env status and exit.",
    )

    args = parser.parse_args()
    workspace = Path(__file__).resolve().parents[1]
    group_dir = workspace / "exercises" / f"group-{args.group}"
    state_path = workspace / "setup" / ".group-env-state.json"

    uv = _resolve_uv_command()
    if uv is None:
        print("FAIL: Could not find `uv`.")
        print("Run `python setup/bootstrap.py` to install uv and seed this workspace.")
        return 1

    if not group_dir.exists():
        print(f"FAIL: Missing expected group directory: {group_dir}")
        return 1

    print(f"Preparing Builder-first Group {args.group} at {group_dir}")

    if args.status:
        _print_group_status(args.group, group_dir, state_path)
        return 0

    if not args.skip_sync:
        if args.force_sync or not _group_sync_is_current(args.group, group_dir, state_path):
            if _run_command([*uv, "sync"], cwd=group_dir) != 0:
                return 1
            _mark_group_synced(args.group, group_dir, state_path)
        else:
            print("Group dependencies are already synced for this lockfile. Skipping uv sync.")
            print("Use --force-sync if you want to refresh anyway.")

    if args.run is None or len(args.run) == 0:
        print("Setup complete. To run a loop file, use:")
        print(f'  python setup/group_env.py --group {args.group} --run python <script>')
        return 0

    if args.run[0] != "python":
        args.run.insert(0, "python")

    return _run_command([*uv, "run", *args.run], cwd=group_dir)


def _resolve_uv_command() -> Optional[Command]:
    uv = shutil.which("uv")
    if uv:
        return [uv]

    if _try_python_uv():
        return [sys.executable, "-m", "uv"]

    return None


def _try_python_uv() -> bool:
    try:
        return subprocess.run([sys.executable, "-m", "uv", "--version"]).returncode == 0
    except Exception:
        return False


def _run_command(cmd: Sequence[str], cwd: Path) -> int:
    display = " ".join(str(part) for part in cmd)
    print(f"$ {display}")
    return subprocess.run(list(cmd), cwd=str(cwd)).returncode


def _state_key(group: str) -> str:
    return f"group:{group}"


def _read_group_env_state(path: Path) -> dict:
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def _write_group_env_state(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def _group_sync_is_current(group: str, group_dir: Path, state_path: Path) -> bool:
    state = _read_group_env_state(state_path)
    entry = state.get(_state_key(group))
    if not isinstance(entry, dict):
        return False

    pyproject = group_dir / "pyproject.toml"
    lock = group_dir / "uv.lock"
    if not (group_dir / ".venv").exists():
        return False
    if not pyproject.exists() or not lock.exists():
        return False

    try:
        if entry.get("pyproject_mtime") != pyproject.stat().st_mtime:
            return False
        if entry.get("lock_mtime") != lock.stat().st_mtime:
            return False
    except Exception:
        return False
    return True


def _mark_group_synced(group: str, group_dir: Path, state_path: Path) -> None:
    data = _read_group_env_state(state_path)
    pyproject = group_dir / "pyproject.toml"
    lock = group_dir / "uv.lock"
    if not (pyproject.exists() and lock.exists()):
        return

    data[_state_key(group)] = {
        "pyproject_mtime": pyproject.stat().st_mtime,
        "lock_mtime": lock.stat().st_mtime,
    }
    _write_group_env_state(state_path, data)


def _print_group_status(group: str, group_dir: Path, state_path: Path) -> None:
    print(f"Group {group} status")
    print(f"Path: {group_dir}")
    print(f"venv exists: {'yes' if (group_dir / '.venv').exists() else 'no'}")
    print(f"pyproject exists: {'yes' if (group_dir / 'pyproject.toml').exists() else 'no'}")
    print(f"uv.lock exists: {'yes' if (group_dir / 'uv.lock').exists() else 'no'}")
    if _group_sync_is_current(group, group_dir, state_path):
        print("Sync status: up to date")
    else:
        print("Sync status: unknown or stale")


if __name__ == "__main__":
    sys.exit(main())
