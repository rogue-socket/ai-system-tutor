# AGENTS.md

This repository is a **portable tutor skill for AI systems engineering and agentic workflows**. It runs in any tool-using agent — Claude Code, OpenAI Codex CLI, GitHub Copilot CLI, Cursor, Aider, etc.

**To run the tutor:** read `SKILL.md` in this directory and follow the protocol. The protocol is tool-agnostic prose ("read the file at X", "run command Y"); translate to your harness's primitives.

**Workspace location:** `~/ai-systems/`. Course state (progress, session-state, notes, exercises, flashcards) lives there. This repo is the source-of-truth for the skill itself.

**Two orientations,** picked during onboarding (Step 2.5 of `SKILL.md`):

- **`foundations_first`** — walk L0 → L8 of the AI System Engineer syllabus. Reference files: `references/curriculum.md`, `references/exercise-bank.md`.
- **`builder_first`** — 10 hands-on coding loops over ~70–120 hours, on Gemini's free tier. Reference: `references/builder-first.md`. When this orientation is picked, copy `assets/builder-first/` into the workspace.

**Reference files** in `references/` and assets in `assets/` are loaded **on demand** by the protocol — don't preload them.

**Slash commands** the user may type (parse and dispatch per `SKILL.md`):

| Command | When |
|---|---|
| `/plan`, `/start`, `/quiz`, `/continue`, `/notes`, `/config` | Anytime |
| `/loop list`, `/loop [n]`, `/loop skip`, `/loop quickpass` | Builder-first only |

Plain English also works: *"teach me X"*, *"design Y"*, *"pause"*. Full reference at `assets/COMMANDS.md` (copied to workspace as `~/ai-systems/COMMANDS.md` at first-time onboarding).

**Workspace viewer:** `assets/index.html` + `assets/manifest.json` are copied to the workspace at first-time onboarding. The learner runs `python -m http.server 8000` from `~/ai-systems/` and opens `http://localhost:8000` to read notes / cheatsheets / flashcards as a styled site. The tutor appends to `manifest.json` whenever a new note, cheatsheet, or flashcard deck is generated.

**Python version:** the curriculum's pinned dependencies require **Python 3.11, 3.12, or 3.13** (not 3.14 — LangChain 0.3.x typing-eval incompatibility).

For installation across harnesses, see `README.md`.
