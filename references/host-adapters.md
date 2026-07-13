# Host adapters

The course protocol is host-neutral. These adapters only describe discovery and session entry;
the workspace and curriculum stay identical across hosts.

| Host | Discovery file | Start instruction |
|---|---|---|
| Claude Code | `SKILL.md` and `CLAUDE.md` | `start the AI systems tutor` |
| Codex | `AGENTS.md` or `~/.codex/skills/ai-systems-tutor` | `start the AI systems tutor` |
| GitHub Copilot | `.github/copilot-instructions.md` | `Use the ai-systems-tutor skill in this repo and start the course.` |

All hosts create or resume `~/ai-systems/`. If that path is unavailable, use `./ai-systems/`
and state the fallback. Load `SKILL.md` first, then lazy-load only the reference needed by the
active orientation or mode.
