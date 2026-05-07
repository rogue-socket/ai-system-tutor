# install.ps1 — wire up ai-system-tutor for Claude Code on Windows.
#
# What this does:
#   1. Creates a directory junction at %USERPROFILE%\.claude\skills\ai-systems-tutor
#      pointing at this repo, so Claude Code auto-discovers the skill.
#   2. Leaves %USERPROFILE%\ai-systems\ alone — the skill creates it on first run.
#
# Junctions don't require admin or developer mode (unlike symbolic links).
# Junctions only work for directories, which is what we want here.
#
# For other harnesses (Codex CLI, Copilot CLI, Cursor, Aider): they read AGENTS.md
# from whatever directory you invoke them in. No install step needed; cd to this
# repo or copy AGENTS.md into your working dir.
#
# Usage (from PowerShell, no admin required):
#   cd path\to\ai-system-tutor
#   .\install.ps1
#
# If PowerShell complains about execution policy:
#   PowerShell -ExecutionPolicy Bypass -File .\install.ps1

$ErrorActionPreference = "Stop"

$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsParent = Join-Path $env:USERPROFILE ".claude\skills"
$SkillsDir = Join-Path $SkillsParent "ai-systems-tutor"

Write-Host "Repo:        $RepoDir"
Write-Host "CC skill at: $SkillsDir"
Write-Host ""

# Sanity check: required entries in repo
$Required = @("SKILL.md", "AGENTS.md", "references", "assets")
foreach ($f in $Required) {
    $p = Join-Path $RepoDir $f
    if (-not (Test-Path $p)) {
        Write-Error "ERROR: $p not found. Did you clone the full repo?"
        exit 1
    }
}

# Create the parent dir for the skill (~/.claude/skills/)
if (-not (Test-Path $SkillsParent)) {
    New-Item -ItemType Directory -Path $SkillsParent -Force | Out-Null
    Write-Host "Created $SkillsParent"
}

# Handle existing entry at $SkillsDir
if (Test-Path $SkillsDir) {
    $item = Get-Item $SkillsDir -Force
    # Junctions show up as ReparsePoint
    $isReparse = ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0
    if ($isReparse) {
        Write-Host "Removing existing junction/symlink at $SkillsDir"
        # Remove-Item on a junction in PowerShell: use cmd /c rmdir to be safe
        cmd /c rmdir "$SkillsDir" | Out-Null
    } else {
        Write-Error "ERROR: $SkillsDir exists and is not a junction/symlink. Move or remove it manually."
        exit 1
    }
}

# Create the directory junction
# /J flag = junction (no admin needed). Avoid New-Item -SymbolicLink because that
# requires admin or Developer Mode on most Windows installs.
$result = cmd /c mklink /J "$SkillsDir" "$RepoDir" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "ERROR: Failed to create junction. mklink output: $result"
    exit 1
}
Write-Host "Junction created: $SkillsDir -> $RepoDir"
Write-Host ""

# Verify SKILL.md is reachable through the junction
$check = Join-Path $SkillsDir "SKILL.md"
if (-not (Test-Path $check)) {
    Write-Error "ERROR: $check not reachable after junction. Something is off."
    exit 1
}

Write-Host "Done. Verify by:"
Write-Host "  - Claude Code:  invoke 'start the AI systems tutor' — it should route to this skill."
Write-Host "  - Other agents: cd into $RepoDir and they will read AGENTS.md automatically."
Write-Host ""
Write-Host "First run will create $env:USERPROFILE\ai-systems\ from assets/."
Write-Host "To re-bootstrap, delete that directory and re-invoke the tutor."
