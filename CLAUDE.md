# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

A Claude skill that guides users through creating a Microsoft 365 Copilot agent. No build system — it's a skill distribution package installed via `install.sh`. The two runtime files are `SKILL.md` (conversational logic) and `scripts/generate_docx.py` (Word document generator). Supports English, French, and German.

## No Build/Test/Lint Commands

This project has none. Changes are tested by invoking the skill manually in Claude and running through the flow.

To test the doc generator in isolation:
```bash
python scripts/generate_docx.py /tmp/agent_config.json ./test_output.docx
```

`python-docx` auto-installs via `subprocess` if missing (see top of `generate_docx.py`).

## Architecture

**Two-part system:**

1. **`SKILL.md`** — Full conversational instructions for Claude. Contains three complete parallel versions: English, French, and German. Controls the 4-phase flow:
   - Phase 0: Language selection (EN/FR/DE) — always first, drives everything after
   - Phase 1: Single open discovery question
   - Phase 2: 3–4 targeted follow-up questions
   - Phase 3: Six sequential field proposals (name/description → instructions → capabilities → knowledge sources → starter prompts → disclaimer), each proposed then validated before advancing
   - Phase 4: Collects validated data, writes `/tmp/agent_config.json`, calls `generate_docx.py`

2. **`scripts/generate_docx.py`** — Reads JSON config, generates a formatted `.docx`. The `lang` field ("en"/"fr"/"de") switches all UI strings. Uses a `_get(config, *keys)` helper that falls back through multiple key names for backward compatibility with legacy French JSON keys (`nom`, `fonctionnalites`, `sources_connaissances`, `suggestions_demarrage`).

**JSON config structure** passed between skill and generator:
```json
{
  "lang": "en" | "fr" | "de",
  "name": "...",
  "description": "...",
  "instructions": "...",
  "capabilities": ["WebSearch", "OneDriveAndSharePoint", "..."],
  "knowledge_sources": ["url1", ...],
  "starters": [{"title": "...", "text": "..."}, ...],
  "disclaimer": "..."
}
```

**Design system** (hardcoded in generator): Outfit font (titles), Petrona (body), orange accent `#FF5119`, 2.5cm margins.

## Key Constraints Encoded in SKILL.md

- One field proposed at a time; wait for user validation before advancing
- Instructions field (Phase 3.2) is highest priority — structure: role, tasks, tone, constraints, request handling
- Writing agents require a mandatory anti-pattern self-review checklist before delivery (serial nominal sentences, filler vocabulary, vague attribution, generic conclusions)
- Creative/drafting agents must encode step-based workflows (propose → validate → produce)
- Agents taking briefs must include explicit clarification mechanisms with question-trigger thresholds

## Field Limits (Agent Builder)

| Field | Limit |
|---|---|
| Name | 100 chars |
| Description | 1,000 chars |
| Instructions | 8,000 chars |
| Starter prompts | 12 max |
| Disclaimer | 500 chars |

## Capabilities (Agent Builder)

All capabilities supported by the generator — use exact key strings in the JSON:

| Key | EN label |
|---|---|
| `WebSearch` | Web search |
| `OneDriveAndSharePoint` | OneDrive & SharePoint |
| `Email` | Email |
| `TeamsMessages` | Teams messages |
| `People` | People |
| `Meetings` | Meetings |
| `GraphicArt` | Image creation |
| `CodeInterpreter` | Code interpreter |
| `Dataverse` | Dataverse |

Unknown keys pass through as-is (no label translation).


## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/Paaaddy/lns-skill-copilot-agent-builder/main/install.sh | bash
```

Auto-detects Claude Cowork (`~/Documents/Claude/Skills/`) vs Claude Code (`~/.claude/skills/`).
