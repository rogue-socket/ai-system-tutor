# ~/ai-systems — your AI systems engineering workspace

This directory was created by the `ai-systems-tutor` skill on first run. It holds **all your course state**: progress, lesson notes, exercises, mock interviews, and the spaced-repetition queue.

You don't need to edit anything by hand. The skill writes here on every meaningful interaction. But knowing the layout helps when you want to grep for an old note or rerun an exercise.

## Layout

```
~/ai-systems/
├── README.md             ← this file
├── progress.json         ← learner profile, topic statuses, SR queue, session/exercise/review logs
├── session-state.md      ← last-session checkpoint (where you left off, what's next)
├── index.html            ← workspace viewer (open with `python -m http.server 8000`)
├── manifest.json         ← index for the viewer; tutor maintains
├── COMMANDS.md           ← slash commands and natural-language overrides cheat-sheet
├── notes/                ← one .md per topic + diagnostic-YYYY-MM-DD.md
│   └── diagrams/         ← interactive HTML diagrams generated during lessons
├── cheatsheets/          ← one .md per topic, short-form reference
├── exercises/            ← one dir per dated exercise: YYYY-MM-DD-<topic-slug>/
├── reviews/              ← mock interviews and design reviews: YYYY-MM-DD-<system>.md
├── flashcards/           ← one .json per topic
└── meta/                 ← logs, traces, anything not user-facing
```

## Viewing your notes / cheatsheets / flashcards

Run from this directory:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000` in any browser. You'll see a styled, navigable view of your notes, cheatsheets, and flashcards — the same files the tutor wrote to disk, just renderable. Three tabs (Notes / Cheatsheets / Flashcards) with click-to-flip on flashcards.

The viewer reads `manifest.json` to discover content. The tutor maintains it: every time a new note, cheatsheet, or flashcard deck is generated, it's appended to the manifest. You don't edit the manifest by hand.

If you've shipped a builder-first loop, the per-loop `NOTES.md` and `CHEATSHEET.md` files in `exercises/group-X/loop-N-<slug>/` show up in the viewer too.

## What's in each file

- **`progress.json`** — the source of truth for your course state. Schema in `<skill>/references/spaced-repetition.md`. Status values per topic: `not_started`, `in_progress`, `shaky`, `solid`, `mastered`.
- **`session-state.md`** — short markdown the skill reads at the start of every session to figure out where you were. Schema in `<skill>/references/session-control.md`.
- **`notes/<topic>.md`** — reference notes for a topic. One file per topic; updated on revisit, not duplicated.
- **`notes/diagnostic-<date>.md`** — your initial diagnostic answers and the skill's assessment.
- **`exercises/<date>-<topic>/`** — runnable code for a practical exercise (Python by default).
- **`reviews/<date>-<system>.md`** — mock interview transcripts and design reviews with scoring.
- **`flashcards/<topic>.json`** — flashcards used by the SR scheduler.

## Tutor commands

In any agent harness (Claude Code, Codex, Copilot CLI, etc.), invoke the tutor with one of:

| Command | What it does |
|---|---|
| `start the AI systems tutor` | First-time onboarding (already done if you're reading this) |
| `continue the course` / `/continue` | Resume from where you left off |
| `/plan` | Show full curriculum + your current position |
| `/start [topic]` | Begin a lesson on a topic |
| `/quiz` | Run today's spaced-repetition review |
| `/notes [topic]` | Generate or update reference notes for a topic |
| `/config` | Show or edit your learner profile in `progress.json` |
| `pause` / `stop for today` | End-of-session protocol — saves state cleanly |

## If something looks wrong

- If `progress.json` gets corrupted, the skill will refuse to start. Restore from your last git commit (you DID `git init` this dir, right?), or delete `progress.json` and re-run the diagnostic.
- If `session-state.md` is missing, the skill falls back to "Cold Resume" — short rediagnostic, then continues.
- If the whole workspace is broken, delete `~/ai-systems` and run `start the AI systems tutor` again. Your repo source-of-truth is the skill itself, not this workspace.
  - macOS / Linux: `rm -rf ~/ai-systems`
  - Windows PowerShell: `Remove-Item -Recurse -Force $env:USERPROFILE\ai-systems`

## Versioning your workspace

Recommended: `cd ~/ai-systems && git init && git add . && git commit -m "init"`. The skill commits nothing automatically — that's on you. But having git here means you can roll back a bad edit or see your trajectory over months.
