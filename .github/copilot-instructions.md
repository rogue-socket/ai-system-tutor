# GitHub Copilot Instructions

This repository packages the `ai-systems-tutor` skill.

When the user asks to start, continue, review, quiz, or practice AI systems engineering or agentic workflows, load `SKILL.md` and follow its session controller. Load `references/` lazily by mode. Create or resume the course workspace at `~/ai-systems/` unless the environment cannot write there; in that case use `./ai-systems/` and tell the user.

When the user asks to maintain this repository, do not run the course. Follow `AGENTS.md` for repository guidance.
