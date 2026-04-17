# Changelog

## [2.0.0] — 2026-04-17 (fork)

### Changed
- Forked from `VincentLNS/lns-skill-copilot-agent-builder`.
- Skill rewritten to support **English and German** only (French removed).
- Skill's first question is now a language picker (`EN` / `DE`); the entire flow, including the generated Word document, runs in the selected language.
- `scripts/generate_docx.py` now reads a top-level `lang` field (`"en"` or `"de"`) and switches all document labels, hints, checklist and capability names accordingly. Legacy French JSON keys (`nom`, `fonctionnalites`, `sources_connaissances`, `suggestions_demarrage`) are still accepted as fallbacks.
- JSON config now uses English keys: `name`, `capabilities`, `knowledge_sources`, `starters` (with `title`/`text`).
- `README.md` and `install.sh` rewritten in English; install URLs point at the fork.

## [1.0.0] — 2026-04-14

### Added
- Initial release
- 4-phase interactive workflow (Discovery → Deep dive → Field generation → Word doc)
- Anti-pattern checklist for writing agents
- Clarification-before-production mechanism
- Progressive workflow encoding for creative agents
- Word document generation via `generate_docx.py`
