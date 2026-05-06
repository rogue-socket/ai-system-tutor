# ai-system-tutor

A portable, agent-driven course on **AI systems engineering and agentic workflows**. Modeled on the [system-design-tutor](https://github.com/anthropics/skills) pattern but built to run in any tool-using agent — Claude Code, OpenAI Codex, GitHub Copilot CLI, Cursor, Aider, anywhere.

The skill OWNS the curriculum: it onboards you with a 9-question diagnostic, picks your starting layer, drives lessons, schedules spaced-repetition reviews, runs practical exercises, and checkpoints state across sessions. You steer when you want a detour; the default is forward motion through the syllabus.

**Curriculum source:** the [AI System Engineer](https://rogue-socket.github.io/AI-System-Engineer/) syllabus — 9 layers, ~370 topics:

- **L0** Mental Models — what models, agents, and AI systems actually are
- **L1** Foundation Models — internals, selection, inference, prompts for production
- **L2** Reasoning & Intelligence — agent loops, planning, reflection, metacognition
- **L3** Memory & Knowledge — retrieval, chunking, RAG architectures, knowledge stores
- **L4** Agency & Tool Use — tool design, protocols (MCP, A2A), interaction patterns, identity
- **L5** Multi-Agent Systems — orchestration patterns, coordination, failure modes
- **L6** Infrastructure & Deployment — serving, hardening, caching, cost engineering
- **L7** Safety, Security & Governance — threats, defenses, OWASP Agentic Top 10, privacy
- **L8** Evaluation, Observability & Applications — eval frameworks, tracing, CI/CD

## Install

```sh
git clone <this-repo> ~/code/ai-system-tutor
cd ~/code/ai-system-tutor
./install.sh
```

`install.sh` does two things:
1. Symlinks `SKILL.md` and `references/` into `~/.claude/skills/ai-systems-tutor/` so Claude Code auto-discovers it.
2. Copies workspace bootstrap files (`assets/workspace-README.md`, `assets/progress-template.json`) so the first run can initialize `~/ai-systems/` cleanly.

For other harnesses (Codex, Copilot CLI, Cursor, Aider): they read `AGENTS.md` automatically when you run them in this directory. To run the tutor from anywhere, either `cd` into this repo first, or symlink `AGENTS.md` into the project the agent runs in.

## Usage

Once installed, in any harness:

- **Claude Code:** `start the AI systems tutor` (auto-routes via skill description)
- **Codex / Copilot CLI / Cursor:** invoke the agent in this directory; it reads `AGENTS.md` → `SKILL.md` and proceeds
- **Anywhere else:** paste the contents of `SKILL.md` as the system prompt

After the first session, `~/ai-systems/` exists. From that point on, just say `continue the course` or `/continue` and the skill resumes from `session-state.md`.

## Slash commands

User-typed text shortcuts that work in any harness:

| Command | What it does |
|---|---|
| `/plan` | Show full curriculum + current position |
| `/start [topic]` | Begin lesson for the given topic, or the next planned one |
| `/quiz` | Run today's spaced-repetition review |
| `/continue` | Resume from `session-state.md` |
| `/notes [topic]` | Generate or update topic notes in `~/ai-systems/notes/` |
| `/config` | Show or edit learner profile in `progress.json` |

## Repo layout

```
ai-system-tutor/
├── SKILL.md                     # router + protocol (source of truth)
├── AGENTS.md                    # 3-line pointer for non-CC harnesses
├── README.md                    # this file
├── install.sh                   # symlinks into ~/.claude/skills/, prepares workspace
├── references/
│   ├── curriculum.md            # L0-L8 topic tree, prerequisites, anchor sources
│   ├── theory-modes.md          # explain/visualize/socratic/build/auto-quiz cycle
│   ├── practical-mode.md        # runnable agent exercise playbook
│   ├── exercise-bank.md         # exercises per layer
│   ├── incidents.md             # real agent failure stories
│   ├── spaced-repetition.md     # SR scheduler + progress.json schema
│   └── session-control.md       # pause/resume + session-state.md schema
└── assets/
    ├── workspace-README.md      # README copied to ~/ai-systems/
    ├── progress-template.json   # initial progress.json
    └── exercise-templates/      # Python scaffolds for common exercises
```

## Workspace layout (after first run)

```
~/ai-systems/
├── README.md                    # from assets/workspace-README.md
├── progress.json                # learner profile, topic statuses, SR queue
├── session-state.md             # last-session checkpoint
├── notes/                       # one .md per topic + diagnostics + diagrams/
├── exercises/                   # one dir per dated exercise
├── reviews/                     # mock interviews, design reviews
├── flashcards/                  # one .json per topic
└── meta/                        # logs, debug traces, etc.
```

## Design notes

- **Tool-agnostic protocol.** `SKILL.md` and reference files use prose like "read the file at X" / "run the command Y" — no `Read`/`Edit`/`Bash` tool names baked in. Works on any harness.
- **State as files.** No MCP server, no database. Every harness already has filesystem access.
- **Curriculum is frozen at build time** from the upstream syllabus. Re-sync on demand; don't read the live JS at runtime.
- **Source anchors:** Lilian Weng "LLM Powered Autonomous Agents", Anthropic engineering blog, OpenAI cookbook, Hugging Face Agents course, OWASP Agentic AI Top 10.
