# AGENTS.md

This repository is a **portable tutor skill for AI systems engineering and agentic workflows**. It runs in any tool-using agent — Claude Code, OpenAI Codex, GitHub Copilot CLI, Cursor, Aider, etc.

**To run the tutor:** read `SKILL.md` in this directory and follow the protocol in it. The protocol is written in tool-agnostic prose; translate file/command references to your harness's primitives.

**Workspace location:** `~/ai-systems/`. State (progress, session, notes, exercises) lives there. This repo is the source-of-truth for the skill itself.

**Reference files** in `references/` and assets in `assets/` are loaded on demand by the protocol — don't preload them.

**Slash commands** the user may type: `/plan`, `/start`, `/quiz`, `/continue`, `/notes`, `/config`. They're just text — parse them and dispatch per `SKILL.md`.

For installation across harnesses, see `README.md`.
