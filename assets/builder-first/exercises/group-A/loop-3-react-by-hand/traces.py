"""Trace logging for the ReAct loop.

Each task gets one JSONL file under `traces/`. Read these after every run —
the trace is the artifact you debug. Reading traces is the load-bearing skill
of Loop 3.
"""
import json
from datetime import datetime
from pathlib import Path

TRACE_DIR = Path(__file__).parent / "traces"


def new_trace(task: str) -> Path:
    """Create a new trace file for one task. Returns its path."""
    TRACE_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    path = TRACE_DIR / f"{stamp}.jsonl"
    with path.open("w") as f:
        f.write(json.dumps({"event": "task", "task": task}) + "\n")
    return path


def log(path: Path, event: str, **fields) -> None:
    """Append a structured event to the trace."""
    entry = {"event": event, **fields}
    with path.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def show(path: Path) -> None:
    """Pretty-print a trace file. Edit this freely — the format is yours."""
    print(f"\n=== {path.name} ===")
    with path.open() as f:
        for line in f:
            entry = json.loads(line)
            ev = entry.pop("event")
            if ev == "task":
                print(f"[task] {entry['task']}")
            elif ev == "thought":
                print(f"  [thought] {entry['text']}")
            elif ev == "action":
                print(f"  [action] {entry['tool']}({entry['args']})")
            elif ev == "observation":
                print(f"  [obs] {entry['text']}")
            elif ev == "final":
                print(f"[final] {entry['text']}")
            elif ev == "error":
                print(f"  [ERROR] {entry['kind']}: {entry['msg']}")
            else:
                print(f"  [{ev}] {entry}")


def latest() -> Path | None:
    """Return the most recent trace file, or None if there are none."""
    if not TRACE_DIR.exists():
        return None
    files = sorted(TRACE_DIR.glob("*.jsonl"))
    return files[-1] if files else None


if __name__ == "__main__":
    p = latest()
    if p is None:
        print("No traces yet. Run react_agent.py first.")
    else:
        show(p)
