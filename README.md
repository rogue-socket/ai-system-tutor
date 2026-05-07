# ai-system-tutor

A portable, agent-driven course on **AI systems engineering and agentic workflows**. Modeled on the [system-design-tutor](https://github.com/anthropics/skills) pattern, built to run in any tool-using agent — Claude Code, OpenAI Codex CLI, GitHub Copilot CLI, Cursor, Aider, anywhere with file-read + file-write + shell.

The skill OWNS the curriculum: it onboards you (with optional **builder-first** code-first orientation), drives lessons, schedules spaced-repetition reviews, runs practical exercises, and checkpoints state across sessions. You steer when you want a detour; the default is forward motion.

## Two orientations, one curriculum

After a short vibe-check, you pick how to walk the course:

- **Foundations-first** — walk L0 → L8, build mental models before agents. Source: the [AI System Engineer](https://rogue-socket.github.io/AI-System-Engineer/) syllabus, 9 layers, ~370 topics.
- **Builder-first** — 10 hands-on loops over ~70–120 hours, on Gemini's free tier. Each loop is a folder of code you open, run, break, fix. By the end you've shipped a deployed agent.

Builder-first loops:

| # | What you build |
|---|---|
| 1 | Bare loop — Gemini call wrapped in a while loop |
| 2 | Tools by hand — brittle JSON dispatch → native function calling |
| 3 | ReAct by hand — reason-act-observe with structured traces |
| 4 | Agent state — memory / context / tools as manipulable files |
| 5 | LangChain — re-implement Loops 1–4 in LangChain + consume an MCP server |
| 6 | LangGraph — make a graph earn its graph-ness |
| 7a | Single-agent architectures — reflexion / planner-executor / self-consistency |
| 7b | Multi-agent architectures — hierarchical / orchestrator / peer + the *trap* |
| 8 | RAG with vectors — sparse / dense / hybrid / reranking + when to abandon RAG |
| 9 | Production reality — caching / retries / cost / evals / observability / deploy |
| 10 | Capstone — pick a project, ship it, write the postmortem |

Foundations-first source curriculum:

- **L0** Mental Models — what models, agents, and AI systems actually are
- **L1** Foundation Models — internals, selection, inference, prompts for production
- **L2** Reasoning & Intelligence — agent loops, planning, reflection, metacognition
- **L3** Memory & Knowledge — retrieval, chunking, RAG architectures, knowledge stores
- **L4** Agency & Tool Use — tool design, protocols (MCP, A2A), interaction patterns, identity
- **L5** Multi-Agent Systems — orchestration patterns, coordination, failure modes
- **L6** Infrastructure & Deployment — serving, hardening, caching, cost engineering
- **L7** Safety, Security & Governance — threats, defenses, OWASP Agentic Top 10, privacy
- **L8** Evaluation, Observability & Applications — eval frameworks, tracing, CI/CD

## Requirements

- **Python 3.11, 3.12, or 3.13** (not 3.14 — LangChain 0.3.x has a typing-eval incompatibility under 3.14's stricter annotation handling)
- **`uv`** — for builder-first venvs. Install: `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux) or `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows)
- **A Gemini API key** (free tier) — for builder-first. Get one at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- A tool-using agent (see Usage below)

## Install

```sh
git clone https://github.com/rogue-socket/ai-system-tutor ~/code/ai-system-tutor
cd ~/code/ai-system-tutor
./install.sh
```

`install.sh`:

1. Symlinks this repo into `~/.claude/skills/ai-systems-tutor/` so Claude Code auto-discovers the skill.
2. Verifies `SKILL.md`, `AGENTS.md`, `references/`, and `assets/` are reachable.

The script is bash. On Windows, run via WSL or Git Bash; the symlinking model assumes Unix-style filesystems. The skill itself is cross-platform once installed — `python` and `uv` work on all three OS families.

For non-Claude-Code harnesses, you don't strictly need `install.sh` — you only need `AGENTS.md` reachable from the directory you run the agent in. See per-harness instructions below.

## Usage

### Claude Code

In a fresh shell:

```
> start the AI systems tutor
```

The skill description routes to it automatically. After the first session, `~/ai-systems/` exists. From then on, `continue the course` or `/continue` resumes from the last checkpoint.

### OpenAI Codex CLI

Codex CLI reads `AGENTS.md` from the working directory automatically. Two ways:

**Option 1 — `cd` into the repo:**

```sh
cd ~/code/ai-system-tutor
codex "start the AI systems tutor"
```

**Option 2 — symlink `AGENTS.md` into the project you're working in:**

```sh
ln -s ~/code/ai-system-tutor/AGENTS.md AGENTS.md
codex "start the AI systems tutor"
```

The agent reads `AGENTS.md` → `SKILL.md` → proceeds with onboarding. Same for `continue the course` later.

### GitHub Copilot CLI

Copilot CLI also reads `AGENTS.md` (or `.github/copilot-instructions.md`) from the working dir:

```sh
cd ~/code/ai-system-tutor
gh copilot suggest "start the AI systems tutor"
```

Or symlink `AGENTS.md` into your project, same as Codex.

### Cursor

Cursor reads `AGENTS.md` and `.cursor/rules/`. From an open project that has `AGENTS.md` (real or symlinked), prompt the agent:

```
> start the AI systems tutor
```

### Aider

Aider reads `CONVENTIONS.md` or `AGENTS.md`. Symlink + invoke:

```sh
ln -s ~/code/ai-system-tutor/AGENTS.md AGENTS.md
aider "start the AI systems tutor"
```

### Plain ChatGPT / Claude.ai (no harness)

Paste the contents of `SKILL.md` as the system prompt. The agent will follow the protocol, but won't have filesystem access — notes and progress need to be copy-pasted by you. Workable for foundations-first lessons; awkward for builder-first (which requires running code).

## Slash commands

User-typed text shortcuts that work in any harness:

| Command | What it does |
|---|---|
| `/plan` | Show full curriculum + current position |
| `/start [topic]` | Begin lesson for the given topic, or the next planned one |
| `/quiz` | Run today's spaced-repetition review |
| `/continue` | Resume from `session-state.md` |
| `/notes [topic]` | Generate or update topic notes |
| `/config` | Show or edit learner profile in `progress.json` |
| `/loop list` | *(builder-first only)* Show all 10 loops with status |
| `/loop [n]` | *(builder-first only)* Jump to loop N (warns on missing prereqs) |
| `/loop skip` | *(builder-first only)* Skip the current loop |
| `/loop quickpass` | *(builder-first only)* 3-question check; pass = mark done |

Plain English works too: *"teach me X"*, *"design Y"*, *"review Z"*, *"pause"*, *"stop for today"*. Full reference at `~/ai-systems/COMMANDS.md` after first run.

## Repo layout

```
ai-system-tutor/
├── SKILL.md                            # router + protocol (source of truth)
├── AGENTS.md                           # short pointer for non-CC harnesses
├── README.md                           # this file
├── install.sh                          # symlinks into ~/.claude/skills/
├── .gitignore
├── references/
│   ├── curriculum.md                   # L0–L8 topic tree + anchor sources
│   ├── builder-first.md                # 10-loop code-first curriculum spec
│   ├── theory-modes.md                 # explain/visualize/socratic/build/quiz cycle
│   ├── practical-mode.md               # runnable agent exercise playbook
│   ├── exercise-bank.md                # exercises per layer (foundations-first)
│   ├── incidents.md                    # real agent failure stories
│   ├── spaced-repetition.md            # SR scheduler + progress.json schema
│   └── session-control.md              # pause/resume + session-state.md schema
└── assets/
    ├── workspace-README.md             # README copied to ~/ai-systems/
    ├── progress-template.json          # initial progress.json
    ├── COMMANDS.md                     # slash-command + natural-language reference card
    ├── index.html                      # workspace viewer (notes / cheatsheets / flashcards)
    ├── manifest.json                   # viewer index, tutor maintains
    ├── exercise-templates/             # Python scaffolds for foundations-first exercises
    └── builder-first/                  # builder-first scaffolding (copied if orientation = builder_first)
        ├── .env.example
        ├── setup/
        │   ├── README.md               # uv install + Gemini key + sanity check
        │   └── sanity_check.py
        └── exercises/
            ├── group-A/                # Loops 1–4: bare LLM stack
            ├── group-B/                # Loops 5–7: LangChain / LangGraph / MCP
            ├── group-C/                # Loop 8: retrieval stack
            └── group-D/                # Loops 9–10: production
```

## Workspace layout (after first run)

```
~/ai-systems/
├── README.md                           # from assets/workspace-README.md
├── COMMANDS.md                         # slash-command reference card
├── progress.json                       # learner profile, statuses, SR queue
├── session-state.md                    # last-session checkpoint
├── index.html                          # viewer — open via python -m http.server
├── manifest.json                       # content index for the viewer
├── notes/                              # one .md per topic + diagnostic-YYYY-MM-DD.md
│   └── diagrams/
├── cheatsheets/                        # one .md per topic, short-form reference
├── exercises/                          # foundations-first dated dirs;
│                                       # builder-first group-A/B/C/D subdirs with venvs + loops
├── reviews/                            # mock interviews, design reviews
├── flashcards/                         # one .json per deck
└── meta/                               # logs, traces
```

To view your notes / cheatsheets / flashcards as a styled site:

```sh
cd ~/ai-systems
python -m http.server 8000
# open http://localhost:8000 in any browser
```

## Design notes

- **Tool-agnostic protocol.** `SKILL.md` and reference files use prose like "read the file at X" / "run the command Y" — no `Read`/`Edit`/`Bash` tool names baked in. Translate to your harness's primitives.
- **State as files.** No MCP server, no database. Every harness already has filesystem access.
- **Curriculum is frozen at build time** from the upstream syllabus. Re-sync on demand; don't read the live JS at runtime.
- **Builder-first locks pinned dependencies** (`uv.lock` per group). The tutor reads `setup/LOOP_VERSIONS.md` (when present) on activation and warns if the manifest is >6 months old.
- **Source anchors:** Lilian Weng "LLM Powered Autonomous Agents", Anthropic engineering blog, OpenAI cookbook, Hugging Face Agents course, OWASP Agentic AI Top 10.

## Troubleshooting

- **`from langchain.agents import AgentExecutor` raises `TypeError`** on Loop 5+: you're on Python 3.14. Switch to 3.11–3.13. The constraint is in `requires-python = ">=3.11,<3.14"`; if you're seeing this, `uv` may be overriding — set `UV_PYTHON=3.13` or install Python 3.13 explicitly.
- **`DefaultCredentialsError` on Loop 5+:** `ChatGoogleGenerativeAI` reads `GOOGLE_API_KEY`. The starter files alias it from `GEMINI_API_KEY` at module top. If you removed the alias line, set both env vars to your key.
- **First-time `uv sync` for Group C is slow (~5–15 min):** that's torch (~2GB). Stages 1–4 of Loop 8 don't need torch; you can defer the heavy install until Stage 5 (cross-encoder reranking).
- **Workspace viewer shows "Could not load `manifest.json`":** you opened `index.html` via `file://`. Browsers block `fetch()` from disk. Run `python -m http.server 8000` from the workspace root and open `http://localhost:8000`.
- **Skill not auto-discovered in Claude Code:** check `~/.claude/skills/ai-systems-tutor/SKILL.md` exists (symlink or real file). If symlink is broken, re-run `./install.sh`.
- **Codex / Copilot CLI doesn't pick up `AGENTS.md`:** ensure you're in a directory where `AGENTS.md` is reachable (real file or symlink). `ls -la AGENTS.md` should show it.
