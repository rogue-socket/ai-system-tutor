#!/usr/bin/env bash
# install.sh — wire up ai-system-tutor for Claude Code and prepare the workspace bootstrap.
#
# What this does:
#   1. Symlinks SKILL.md, references/, and assets/ into ~/.claude/skills/ai-systems-tutor/
#      so Claude Code auto-discovers the skill.
#   2. Leaves ~/ai-systems/ alone — the skill creates it on first run from assets/.
#
# For other harnesses (Codex, Copilot CLI, Cursor, Aider): they read AGENTS.md from
# whatever directory you invoke them in. No install step needed; cd to this repo or
# symlink AGENTS.md into your working dir.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${HOME}/.claude/skills/ai-systems-tutor"

echo "Repo:        ${REPO_DIR}"
echo "CC skill at: ${SKILLS_DIR}"
echo

# Sanity check expected files exist
for f in SKILL.md AGENTS.md references assets; do
  if [[ ! -e "${REPO_DIR}/${f}" ]]; then
    echo "ERROR: ${REPO_DIR}/${f} not found. Did you clone the full repo?" >&2
    exit 1
  fi
done

# Create CC skill dir parent
mkdir -p "$(dirname "${SKILLS_DIR}")"

# If the target exists and is a symlink, replace it. If it's a real dir, refuse.
if [[ -L "${SKILLS_DIR}" ]]; then
  echo "Removing existing symlink at ${SKILLS_DIR}"
  rm "${SKILLS_DIR}"
elif [[ -e "${SKILLS_DIR}" ]]; then
  echo "ERROR: ${SKILLS_DIR} exists and is not a symlink. Move or remove it manually." >&2
  exit 1
fi

ln -s "${REPO_DIR}" "${SKILLS_DIR}"
echo "Symlinked ${SKILLS_DIR} -> ${REPO_DIR}"
echo

# Verify the SKILL.md is reachable through the symlink
if [[ ! -f "${SKILLS_DIR}/SKILL.md" ]]; then
  echo "ERROR: ${SKILLS_DIR}/SKILL.md not reachable after symlink. Something is off." >&2
  exit 1
fi

echo "Done. Verify by:"
echo "  - Claude Code:  invoke 'start the AI systems tutor' — it should route to this skill."
echo "  - Other agents: cd into ${REPO_DIR} and they will read AGENTS.md automatically."
echo
echo "First run will create ~/ai-systems/ from assets/. To re-bootstrap, delete ~/ai-systems/ and re-invoke."
