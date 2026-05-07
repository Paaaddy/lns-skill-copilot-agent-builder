# lns-skill-copilot-agent-builder

A skill for [Claude Cowork](https://claude.ai) and [Claude Code](https://claude.ai/code) that guides you step by step through creating a Microsoft 365 Copilot agent via the Agent Builder interface, and produces a ready-to-paste Word document at the end.

This fork supports **English, French and German**. The skill's very first question asks which language to use, then runs the entire flow in that language.

## What it does

The skill asks the right questions in order, then generates every Agent Builder field with validation between each step:

1. **Language selection** — English, French or German
2. **Discovery** — the agent's role and its users
3. **Deep dive** — tasks, tone, constraints, available data
4. **Agent type** — choose from 8 templates (HR, IT, Sales, Legal, PM, Writing, Data, Custom)
5. **Field generation** — name, description, instructions, capabilities, knowledge sources, starter prompts, disclaimer
6. **Word document** — a formatted `.docx` with a **Recommended Next Steps** section tailored to the chosen agent type, ready to paste into the Agent Builder

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

Or mention (in English, French or German): *"create a Copilot agent"*, *"new M365 agent"*, *"créer un agent Copilot"*, *"nouvel agent M365"*, *"Copilot Agent erstellen"*. The skill triggers automatically.

**Example session:**
```
/copilot-agent-builder
> Would you like to run this in English, French or German?
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

# lns-skill-copilot-agent-builder

Un skill pour [Claude Cowork](https://claude.ai) et [Claude Code](https://claude.ai/code) qui vous guide pas à pas dans la création d'un agent Microsoft 365 Copilot via l'interface Agent Builder, et produit à la fin un document Word prêt à coller.

Ce fork prend en charge **l'anglais, le français et l'allemand**. La toute première question du skill demande quelle langue utiliser, puis déroule l'intégralité du flux dans la langue choisie.

## Ce que ça fait

Le skill pose les bonnes questions dans l'ordre, puis génère chaque champ de l'Agent Builder avec une validation entre chaque étape :

1. **Choix de la langue** — anglais, français ou allemand
2. **Découverte** — le rôle de l'agent et ses utilisateurs
3. **Approfondissement** — tâches, ton, contraintes, données disponibles
4. **Type d'agent** — choisir parmi 8 modèles (RH, IT, Ventes, Juridique, PM, Rédaction, Données, Personnalisé)
5. **Génération des champs** — nom, description, instructions, fonctionnalités, sources de connaissances, suggestions de démarrage, disclaimer
6. **Document Word** — un fichier `.docx` mis en forme avec une section **Prochaines étapes recommandées** adaptée au type d'agent choisi, prêt à coller dans l'Agent Builder

## Installation

**En une ligne (recommandé) :**
```bash
curl -fsSL https://raw.githubusercontent.com/Paaaddy/lns-skill-copilot-agent-builder/main/install.sh | bash
```

Le script détecte automatiquement votre environnement (Claude Cowork ou Claude Code) et installe au bon endroit.

**Manuellement :**

*Claude Cowork :*
```bash
git clone https://github.com/Paaaddy/lns-skill-copilot-agent-builder \
  ~/Documents/Claude/Skills/copilot-agent-builder
```

*Claude Code :*
```bash
git clone https://github.com/Paaaddy/lns-skill-copilot-agent-builder \
  ~/.claude/skills/copilot-agent-builder
```

Redémarrez Claude Cowork (ou relancez Claude Code) : le skill apparaît automatiquement.

## Utilisation

Dans Claude Cowork ou Claude Code, tapez :

```
/copilot-agent-builder
```

Ou mentionnez (en anglais, français ou allemand) : *« créer un agent Copilot »*, *« nouvel agent M365 »*, *"create a Copilot agent"*, *"Copilot Agent erstellen"*. Le skill se déclenche automatiquement.

**Exemple de session :**
```
/copilot-agent-builder
> Souhaitez-vous effectuer ceci en anglais, français ou allemand ?
  FR
> Décris ton agent en quelques phrases : quel est son rôle principal, et qui va l'utiliser ?
  Un agent pour aider les RH à rédiger des fiches de poste...
> [4 phases plus tard] Voici le document Word, prêt à coller dans l'Agent Builder 🎉
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

## Fork origin

This is a fork of [VincentLNS/lns-skill-copilot-agent-builder](https://github.com/VincentLNS/lns-skill-copilot-agent-builder). The original is French-only; this fork adds English and German support, and introduces a language-selection step as the first question.

## License

MIT
