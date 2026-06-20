# Builder-First Setup

One-command bootstrap (recommended). ~10 minutes including first-time package install.

Run this from your workspace:

```bash
cd ~/ai-systems
python setup/bootstrap.py
```

That script handles:
1. `uv` install if missing (non-interactive prompt if you allow it)
2. `.env` setup from `.env.example`
3. `GEMINI_API_KEY` capture
4. Group A install + sanity check

If you prefer manual steps, continue below.

---

Three steps. ~10 minutes. Do them once, in order.

> **Path note for Windows users.** These instructions use Unix-style paths (`~/ai-systems`). On Windows PowerShell 5.1+, `~` expands to `$env:USERPROFILE`, so `cd ~/ai-systems` works directly. On Windows cmd, replace with `%USERPROFILE%\ai-systems\`. Forward-slashes in paths work in both shells.

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

What you'll provide here is a credential for your local workspace, not a password:

- It lets this course call Google Gemini APIs from your machine.
- It is only needed for setup and loop execution in this project.
- It is safe to keep in `~/ai-systems/.env` (git-ignored).

1. Go to **https://aistudio.google.com/apikey**.
2. Sign in with any Google account.
3. Click **"Create API key"**. Pick or create a project — "Generative Language Client" is the default and works fine.
4. Copy the resulting key string now (format starts with `AIza...`).
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

The `.env` file is git-ignored — don't commit it. If you are running `python setup/bootstrap.py`, you can paste it when prompted instead of editing this file directly.

### Free tier (as of 2026-05)

- ~1500 requests/day on `gemini-2.0-flash`
- ~15 requests/minute
- Plenty for Loops 1–9. Capstone (Loop 10) may exceed; switch to a cheaper model in `llm.py` or upgrade billing.

## 3. Install Group A dependencies + run sanity check

Group A is the venv for Loops 1–4. Install once:

**macOS / Linux:**
```bash
cd ~/ai-systems
python setup/group_env.py --group A
```

**Windows PowerShell:**
```powershell
cd $env:USERPROFILE\ai-systems
python setup/group_env.py --group A
```

Then sanity-check that Gemini works:

```bash
python setup/group_env.py --group A --run python setup/sanity_check.py
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

## Switching groups after bootstrap

At Loop 5+, use the same helper:

```bash
python setup/group_env.py --group B
python setup/group_env.py --group C
python setup/group_env.py --group D
```

Once set up, run loop code with:

```bash
python setup/group_env.py --group B --run python langchain_agent.py
```

## Why this helper

The helper avoids repeating manual venv pathing. The whole point is to keep your setup commands predictable and identical across groups, shells, and learners.
