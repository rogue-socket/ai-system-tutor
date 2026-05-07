# Loop Versions Manifest

The tutor reads this on first activation. If `last_refresh` is >6 months old, the tutor warns the learner before starting Loop 1 — see `references/builder-first.md` § Maintenance.

```
last_refresh: 2026-05-07
next_refresh_due: 2026-11-07
python: ">=3.11,<3.14"
```

## Per-group pinned versions

Sourced from each group's `uv.lock` at the date of last refresh. Authoritative pins live in the lock files; this file is the human-readable summary the tutor cites in its warning.

### Group A — Loops 1–4
Last re-locked: 2026-05-07 (27 packages)
- `google-genai`
- `python-dotenv`
- `pydantic`

### Group B — Loops 5, 6, 7a, 7b
Last re-locked: 2026-05-07 (75 packages)
- `langchain 0.3.29`
- `langchain-google-genai 2.1.12`
- `langgraph 0.4.10`
- `mcp 1.27.0`
- `langchain-mcp-adapters 0.1.14` (held below 0.2.0; 0.2+ requires `langchain-core 0.4+`)
- `grandalf 0.8` (transitive: `langgraph.compiled.get_graph().draw_ascii()` needs it)

### Group C — Loop 8
Last re-locked: 2026-05-07 (120 packages; first `uv sync` is heavy — ~2GB torch download)
- `chromadb 1.5.9`
- `rank-bm25 0.2.2`
- `sentence-transformers 5.4.1`
- `torch 2.11.0`

### Group D — Loops 9, 10
Last re-locked: 2026-05-07 (34 packages)
- `fastapi 0.136.1`
- `uvicorn 0.46.0`
- `httpx 0.28.1`
- `prometheus-client 0.25.0`

## Refresh procedure

Owner-side, every 6 months (see `references/builder-first.md` § Maintenance):

1. For each group: `cd assets/builder-first/exercises/group-{A,B,C,D}` and re-run `uv sync --upgrade`.
2. Run the drift pass: import every starter, exercise the SDK surface each loop touches.
3. Validate every loop's BREAK and WIN against the new versions.
4. Commit the new `uv.lock` files and bump `last_refresh` / `next_refresh_due` above.

When LangChain ships a major (e.g. 0.3 → 0.4), Loops 5/6/7 churn first — patch them out-of-cadence. Same for Gemini SDK breaking changes (Group A + the optional `llm.py` wrapper).
