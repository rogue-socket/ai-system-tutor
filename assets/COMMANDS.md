# Tutor Commands

The tutor takes both natural language ("teach me X", "review this", "stop for today") and a small set of slash commands. Either works — slash commands are faster.

You don't have to memorize this. Run `cat ~/ai-systems/COMMANDS.md` anytime to come back to this list.

## Anytime

| Command | What it does |
|---|---|
| `/plan` | Show the full curriculum and your current position |
| `/start [topic]` | Begin a lesson on a specific topic |
| `/continue` | Resume from where you left off (`session-state.md`) |
| `/quiz` | Run today's spaced-repetition review |
| `/notes [topic]` | Generate or update reference notes for a topic |
| `/config` | Show or edit your learner profile in `progress.json` |

## Builder-first only (the 10-loop code path)

These work when your `learner.orientation` in `progress.json` is `builder_first`. Foundations-first learners ignore them.

| Command | What it does |
|---|---|
| `/loop list` | Print all 10 loops with status: not-started / current / done / skipped / quickpassed |
| `/loop [n]` | Jump directly to loop N — warns on missing prereqs but honors the override |
| `/loop skip` | Skip the current loop after a 30-second summary; mark as `skipped` |
| `/loop quickpass` | 3 questions from the loop's WIN criteria; pass = mark `done` without doing the loop |

## Natural-language overrides (no slash needed)

Any of these work as plain English:

- *"teach me X"* / *"design Y"* / *"review Z"* — detour to that topic; current proposal queues for later
- *"quiz me"* / *"review first"* — same as `/quiz`
- *"give me notes"* / *"write this up"* / *"summarize this topic"* — same as `/notes`
- *"what's the plan?"* / *"where are we?"* — same as `/plan`
- *"pause"* / *"I have to go"* / *"stop for today"* — clean end-of-session protocol

## Other handy paths

- **`~/ai-systems/README.md`** — workspace layout and what's in each file.
- **`~/ai-systems/index.html`** — viewer for your notes / cheatsheets / flashcards. Run `python viewer.py` from `~/ai-systems`, then open `http://localhost:8000`. Use `python -m http.server 8000` as fallback.
- **`~/ai-systems/progress.json`** — your full course state. Don't edit by hand unless you know what you're doing.
- **`~/ai-systems/session-state.md`** — where you left off last session. The tutor reads this on Warm Resume.

## When in doubt

Just type what you want. The tutor parses natural language. Slash commands are shortcuts, not requirements.
