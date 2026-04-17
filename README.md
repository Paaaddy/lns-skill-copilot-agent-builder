# lns-skill-copilot-agent-builder

A skill for [Claude Cowork](https://claude.ai) and [Claude Code](https://claude.ai/code) that guides you step by step through creating a Microsoft 365 Copilot agent via the Agent Builder interface, and produces a ready-to-paste Word document at the end.

This fork supports **English and German**. The skill's very first question asks which language to use, then runs the entire flow in that language.

Ein Skill für [Claude Cowork](https://claude.ai) und [Claude Code](https://claude.ai/code), der dich Schritt für Schritt durch die Erstellung eines Microsoft 365 Copilot Agenten über den Agent Builder führt und am Ende ein einfüge-fertiges Word-Dokument erzeugt. Dieser Fork unterstützt **Englisch und Deutsch** — die Sprache wird gleich in der ersten Frage gewählt.

## What it does

The skill asks the right questions in order, then generates every Agent Builder field with validation between each step:

1. **Language selection** — English or German
2. **Discovery** — the agent's role and its users
3. **Deep dive** — tasks, tone, constraints, available data
4. **Field generation** — name, description, instructions, capabilities, knowledge sources, starter prompts, disclaimer
5. **Word document** — a formatted `.docx`, ready to paste into the Agent Builder

## Install

**One-liner (recommended):**
```bash
curl -fsSL https://raw.githubusercontent.com/Paaaddy/lns-skill-copilot-agent-builder/main/install.sh | bash
```

The script auto-detects your environment (Claude Cowork or Claude Code) and installs in the right place.

**Manually:**

*Claude Cowork:*
```bash
git clone https://github.com/Paaaddy/lns-skill-copilot-agent-builder \
  ~/Documents/Claude/Skills/copilot-agent-builder
```

*Claude Code:*
```bash
git clone https://github.com/Paaaddy/lns-skill-copilot-agent-builder \
  ~/.claude/skills/copilot-agent-builder
```

Restart Claude Cowork (or relaunch Claude Code): the skill appears automatically.

## Usage

In Claude Cowork or Claude Code, type:

```
/copilot-agent-builder
```

Or mention (in English or German): *"create a Copilot agent"*, *"new M365 agent"*, *"Copilot Agent erstellen"*, *"neuen Copilot Agent bauen"*. The skill triggers automatically.

**Example session:**
```
/copilot-agent-builder
> Would you like to run this in English or German? / Englisch oder Deutsch?
  EN
> Describe your agent in a few sentences: what is its main role, and who will use it?
  An agent to help HR draft job descriptions...
> [4 phases later] Here is the Word document, ready to paste into the Agent Builder 🎉
```

## Requirements

- [Claude Cowork](https://claude.ai) or [Claude Code](https://claude.ai/code)
- A Microsoft 365 account with Agent Builder access

## Uninstall

*Claude Cowork:*
```bash
rm -rf ~/Documents/Claude/Skills/copilot-agent-builder
```

*Claude Code:*
```bash
rm -rf ~/.claude/skills/copilot-agent-builder
```

## Fork origin

This is a fork of [VincentLNS/lns-skill-copilot-agent-builder](https://github.com/VincentLNS/lns-skill-copilot-agent-builder). The original is French-only; this fork rewrites the skill for English and German, and introduces a language-selection step as the first question.

## License

MIT
