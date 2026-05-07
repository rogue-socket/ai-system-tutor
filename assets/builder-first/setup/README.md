# Builder-First Setup

Three steps. ~10 minutes. Do them once, in order.

> **Path note for Windows users.** These instructions use Unix-style paths (`~/ai-systems`). On Windows PowerShell 5.1+, `~` expands to `$env:USERPROFILE`, so `cd ~/ai-systems` works directly. On Windows cmd, replace with `%USERPROFILE%\ai-systems\`. Forward-slashes in paths work in both shells. The activation command `source .venv/bin/activate` (Linux/macOS) becomes `.venv\Scripts\activate` on Windows.

## 1. Install `uv`

`uv` is the Python package manager builder-first uses. One command:

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify: `uv --version` should print something like `uv 0.5.x`.

## 2. Get a Gemini API key (free tier)

1. Go to **https://aistudio.google.com/apikey**.
2. Sign in with any Google account.
3. Click **"Create API key"**. Pick or create a project — "Generative Language Client" is the default and works fine.
4. Copy the key. It looks like `AIzaSy...` (~39 characters).

Save it in your workspace:

```bash
cd ~/ai-systems
cp .env.example .env
```

Open `.env` and replace the placeholder with your real key:

```
GEMINI_API_KEY=AIzaSy...your-real-key
```

The `.env` file is git-ignored — don't commit it.

### Free tier (as of 2026-05)

- ~1500 requests/day on `gemini-2.0-flash`
- ~15 requests/minute
- Plenty for Loops 1–9. Capstone (Loop 10) may exceed; switch to a cheaper model in `llm.py` or upgrade billing.

## 3. Install Group A dependencies + run sanity check

Group A is the venv for Loops 1–4. Install once:

```bash
cd ~/ai-systems/exercises/group-A
uv sync
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows PowerShell
```

Then sanity-check that Gemini works:

```bash
python ~/ai-systems/setup/sanity_check.py
```

Expected output:
```
Found GEMINI_API_KEY (length 39).
Making one test call to gemini-2.0-flash...
Response: OK
PASS: Gemini works. Setup is complete.
```

If you see `FAIL`, the script tells you what's wrong. Common causes:
- `.env` not at `~/ai-systems/.env` → check the path
- Key copied with extra whitespace → re-copy carefully
- 403 / billing error → re-create the key in AI Studio

When it passes, you're ready for Loop 1.

## Switching groups later

When you reach Loop 5, you'll switch to Group B's venv. The tutor will tell you when. Same flow as Group A — `cd ~/ai-systems/exercises/group-B && uv sync && source .venv/bin/activate`.
