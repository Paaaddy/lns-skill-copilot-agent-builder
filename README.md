# lns-skill-copilot-agent-builder

Un skill pour [Claude Cowork](https://claude.ai) et [Claude Code](https://claude.ai/code) qui guide pas à pas la création d'un agent Microsoft 365 Copilot via l'interface Agent Builder, avec génération d'un document Word prêt à coller à la fin.

Le skill prend en charge **le français, l'anglais et l'allemand**. La toute première question demande quelle langue utiliser, puis déroule l'intégralité du flux dans la langue choisie.

## Ce que ça fait

Le skill pose les bonnes questions dans l'ordre, puis génère chaque champ de l'Agent Builder avec une validation avant de passer au suivant :

1. **Choix de la langue** — français, anglais ou allemand
2. **Découverte** : le rôle de l'agent et ses utilisateurs
3. **Approfondissement** : tâches, ton, contraintes, données disponibles
4. **Génération des champs** : nom, description, instructions, fonctionnalités, sources de connaissances, suggestions de démarrage, disclaimer
5. **Document Word** : un `.docx` formaté, prêt à copier-coller dans l'Agent Builder

## Installation

**En une ligne (recommandé) :**
```bash
curl -fsSL https://raw.githubusercontent.com/VincentLNS/lns-skill-copilot-agent-builder/main/install.sh | bash
```

Le script détecte automatiquement l'environnement (Cowork ou Claude Code) et installe au bon endroit.

**Ou manuellement :**

*Claude Cowork :*
```bash
git clone https://github.com/VincentLNS/lns-skill-copilot-agent-builder \
  ~/Documents/Claude/Skills/copilot-agent-builder
```

*Claude Code :*
```bash
git clone https://github.com/VincentLNS/lns-skill-copilot-agent-builder \
  ~/.claude/skills/copilot-agent-builder
```

Redémarrer Claude Cowork ou relancer Claude Code : le skill apparaît automatiquement.

## Utilisation

Dans Claude Cowork ou Claude Code, taper :

```
/copilot-agent-builder
```

Ou mentionner (en français, anglais ou allemand) : *"créer un agent Copilot"*, *"nouvel agent M365"*, *"create a Copilot agent"*, *"Copilot Agent erstellen"*. Le skill se déclenche automatiquement.

**Exemple de session :**
```
/copilot-agent-builder
> Souhaitez-vous effectuer ceci en français, anglais ou allemand ?
  FR
> Décris-moi ton agent en quelques phrases : quel est son rôle principal, et qui va l'utiliser ?
  Un agent pour aider les RH à rédiger des fiches de poste...
> [4 phases plus tard] Voici le document Word prêt à coller dans l'Agent Builder 🎉
```

## Prérequis

- [Claude Cowork](https://claude.ai) ou [Claude Code](https://claude.ai/code)
- Un compte Microsoft 365 avec accès à l'Agent Builder

## Désinstallation

*Claude Cowork :*
```bash
rm -rf ~/Documents/Claude/Skills/copilot-agent-builder
```

*Claude Code :*
```bash
rm -rf ~/.claude/skills/copilot-agent-builder
```

---

# lns-skill-copilot-agent-builder

A skill for [Claude Cowork](https://claude.ai) and [Claude Code](https://claude.ai/code) that guides you step by step through creating a Microsoft 365 Copilot agent via the Agent Builder interface, and produces a ready-to-paste Word document at the end.

The skill supports **French, English and German**. The very first question asks which language to use, then runs the entire flow in that language.

## What it does

The skill asks the right questions in order, then generates every Agent Builder field with validation between each step:

1. **Language selection** — French, English or German
2. **Discovery** — the agent's role and its users
3. **Deep dive** — tasks, tone, constraints, available data
4. **Field generation** — name, description, instructions, capabilities, knowledge sources, starter prompts, disclaimer
5. **Word document** — a formatted `.docx`, ready to paste into the Agent Builder

## Install

**One-liner (recommended):**
```bash
curl -fsSL https://raw.githubusercontent.com/VincentLNS/lns-skill-copilot-agent-builder/main/install.sh | bash
```

The script auto-detects your environment (Claude Cowork or Claude Code) and installs in the right place.

**Manually:**

*Claude Cowork:*
```bash
git clone https://github.com/VincentLNS/lns-skill-copilot-agent-builder \
  ~/Documents/Claude/Skills/copilot-agent-builder
```

*Claude Code:*
```bash
git clone https://github.com/VincentLNS/lns-skill-copilot-agent-builder \
  ~/.claude/skills/copilot-agent-builder
```

Restart Claude Cowork (or relaunch Claude Code): the skill appears automatically.

## Usage

In Claude Cowork or Claude Code, type:

```
/copilot-agent-builder
```

Or mention (in French, English or German): *"create a Copilot agent"*, *"new M365 agent"*, *"créer un agent Copilot"*, *"Copilot Agent erstellen"*. The skill triggers automatically.

**Example session:**
```
/copilot-agent-builder
> Would you like to run this in French, English or German?
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

---

## Licence / License

MIT
