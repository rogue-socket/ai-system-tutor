# Windows Quickstart

5 steps. ~10 minutes total. Tested on Windows 10 and 11; PowerShell 5.1+ (the default).

This gets you from "fresh clone" to "the tutor is driving you through Loop 1." Everything after that, the tutor handles — including walking you through each loop's venv activation when you reach builder-first.

## 1. Install prerequisites

You need three things. All free; all native Windows.

### Python 3.13

If you don't have it: download from [python.org/downloads](https://www.python.org/downloads/). Pick **3.13.x** (not 3.14 — LangChain has a typing-eval incompatibility on 3.14).

Verify in PowerShell:

```powershell
python --version
# Should print: Python 3.13.x
```

### `uv`

The Python package manager builder-first uses. One PowerShell command:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:

```powershell
uv --version
# Should print: uv 0.x.x
```

You may need to restart PowerShell after installing.

### A Gemini API key

Free tier, no credit card needed.

1. Go to **https://aistudio.google.com/apikey**.
2. Sign in with any Google account.
3. Click **"Create API key"** → pick or create a project (the default is fine).
4. Copy the key. Looks like `AIzaSy...` (~39 characters).

Hold onto it — step 4 below uses it.

## 2. Clone the repo

```powershell
git clone https://github.com/rogue-socket/ai-system-tutor $env:USERPROFILE\code\ai-system-tutor
cd $env:USERPROFILE\code\ai-system-tutor
```

## 3. Run the installer

```powershell
.\install.ps1
```

This creates a directory junction at `%USERPROFILE%\.claude\skills\ai-systems-tutor` pointing at the repo. **No admin or Developer Mode required** — junctions work on standard Windows.

If PowerShell complains about execution policy:

```powershell
PowerShell -ExecutionPolicy Bypass -File .\install.ps1
```

You should see `Done. Verify by: ...`

## 4. Start the tutor

Open whatever agent you use:

### Claude Code

```
> start the AI systems tutor
```

The skill auto-routes. It'll ask the diagnostic questions, then (if you pick builder-first) walk you through setting up the workspace and saving your Gemini key into `.env`.

### OpenAI Codex CLI

```powershell
cd $env:USERPROFILE\code\ai-system-tutor
codex "start the AI systems tutor"
```

Codex reads `AGENTS.md` from the cwd, which points it at `SKILL.md`.

### GitHub Copilot CLI

```powershell
cd $env:USERPROFILE\code\ai-system-tutor
gh copilot suggest "start the AI systems tutor"
```

### Cursor / Aider / others

Same shape. They read `AGENTS.md` from your project's working directory. Either `cd` into this repo or copy `AGENTS.md` into the project where you're running the agent.

## 5. Save your Gemini key when the tutor asks

The tutor will create `~/ai-systems/` (which on Windows is `%USERPROFILE%\ai-systems\`) and prompt you to copy `.env.example` to `.env` and paste your key. Two PowerShell lines:

```powershell
cd $env:USERPROFILE\ai-systems
Copy-Item .env.example .env
notepad .env   # paste your key after GEMINI_API_KEY=
```

Save and close. Tutor takes it from there.

## You're set

From this point, the tutor drives. It'll:

- Detect the workspace on every invocation and resume from `session-state.md`
- Walk you through each builder-first loop's venv setup (`uv sync`, `.venv\Scripts\activate`)
- Generate notes / cheatsheets / flashcards into `~/ai-systems/`
- Update `manifest.json` so the workspace viewer (run `python -m http.server 8000` in the workspace) shows them

Just say **"continue the course"** or **`/continue`** any time you come back.

## Common Windows snags

- **`install.ps1` fails with "execution of scripts is disabled"** — use `PowerShell -ExecutionPolicy Bypass -File .\install.ps1` (one-time bypass, doesn't change global policy).
- **Long-path errors during `uv sync`** — Windows defaults to a 260-char path limit. Enable long paths once: `git config --system core.longpaths true` (run PowerShell as admin) or set `HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled = 1` in the registry. Reboot after.
- **`python` is not recognized** — Python wasn't added to PATH at install time. Re-run the Python installer and check "Add to PATH". Or use `py -3.13` as a substitute.
- **`uv: command not found` after install** — the installer added uv to a PowerShell-specific PATH that needs a restart. Close and reopen PowerShell.
- **"DefaultCredentialsError" at Loop 5** — `ChatGoogleGenerativeAI` reads `GOOGLE_API_KEY`, not `GEMINI_API_KEY`. The starter files alias automatically; if you removed the alias line, set both env vars in `.env` to your key.
- **Workspace viewer shows "Could not load manifest.json"** — you opened `index.html` via `file://`. Browsers block `fetch()` from disk. Run `python -m http.server 8000` from `%USERPROFILE%\ai-systems\` and open `http://localhost:8000`.
- **Group C's `uv sync` is slow (5–15 min)** — that's the torch download (~2GB). Stages 1–4 of Loop 8 don't need torch; defer the heavy install until Stage 5 if you need to.

If something else breaks, check `README.md` → Troubleshooting, or paste the error to the tutor — it can usually diagnose.
