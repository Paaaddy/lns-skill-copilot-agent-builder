#!/usr/bin/env bash
set -e

command -v curl >/dev/null 2>&1    || { echo "Error: curl is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Error: Python 3 is required but not installed."; exit 1; }

SKILL_NAME="copilot-agent-builder"
BASE_URL="https://raw.githubusercontent.com/Paaaddy/lns-skill-copilot-agent-builder/main"

# Environment auto-detection
COWORK_DIR="$HOME/Documents/Claude/Skills/$SKILL_NAME"
CLAUDE_CODE_DIR="$HOME/.claude/skills/$SKILL_NAME"

if [ -d "$HOME/Documents/Claude/Skills" ]; then
  INSTALL_DIR="$COWORK_DIR"
  ENV_NAME="Claude Cowork"
elif [ -d "$HOME/.claude/skills" ]; then
  INSTALL_DIR="$CLAUDE_CODE_DIR"
  ENV_NAME="Claude Code"
else
  echo "No environment detected automatically."
  echo "Where should the skill be installed?"
  echo "  1) Claude Cowork  ($COWORK_DIR)"
  echo "  2) Claude Code    ($CLAUDE_CODE_DIR)"
  read -rp "Choice [1/2]: " choice
  if [ "$choice" = "2" ]; then
    INSTALL_DIR="$CLAUDE_CODE_DIR"
    ENV_NAME="Claude Code"
  else
    INSTALL_DIR="$COWORK_DIR"
    ENV_NAME="Claude Cowork"
  fi
fi

echo "Installing skill '$SKILL_NAME' for $ENV_NAME..."

mkdir -p "$INSTALL_DIR/scripts"

curl -fsSL "$BASE_URL/SKILL.md"                    -o "$INSTALL_DIR/SKILL.md"
curl -fsSL "$BASE_URL/scripts/generate_docx.py"    -o "$INSTALL_DIR/scripts/generate_docx.py"

echo ""
echo "✅ Skill installed at: $INSTALL_DIR"
echo "   Restart $ENV_NAME: the skill will appear automatically."
echo ""
echo "   Trigger: /copilot-agent-builder"
echo "   Or mention: \"create a Copilot agent\", \"M365 agent\", \"Copilot Agent erstellen\", \"neuen Copilot Agent\""
echo ""
echo "   The skill's first question will ask whether to run in English, French or German."
