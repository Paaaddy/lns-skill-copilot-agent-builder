# Changelog

## [2.0.0] — 2026-05-02

### Added
- **Template picker (Phase 2b)** — 8 agent types (HR, IT, Sales, Legal, PM, Writing, Data, Custom) presented after Phase 2; sets `agent_type` in the JSON config
- **Recommended Next Steps section** in the generated document — 4 tailored action items per agent type, trilingual (EN/FR/DE)
- **Config validation** in `generate_docx.py` — raises `ValueError` for missing `name` or `instructions` fields
- **Output collision prevention** — appends microsecond timestamp to filename if the target path already exists
- **JSON export alongside `.docx`** — config written as `.json` next to the document for reference
- **Error recovery block** in Phase 4 (all 3 languages) — if the generator fails, the skill shows the raw JSON for manual copy-paste
- **`agent_type` field** in JSON config contract

### Changed
- **Fonts**: `Outfit` → `Calibri`, `Petrona` → `Georgia` — universally available without custom font installation
- **pip install flag**: `--break-system-packages` → `--user` — safe on modern Debian/Ubuntu/macOS
- **Footer** includes version string (`v2.0.0`)
- **`install.sh`** checks for `curl` and `python3` before download

### Fixed
- Generator crash on systems where `--break-system-packages` is rejected
- Document font rendering on systems without Outfit/Petrona installed
- `subprocess.run()` pip bootstrap now raises on failure instead of silently proceeding to a cryptic `ImportError`

### Performance
- Pre-computed XML namespace `qn()` values cached at module level — eliminates repeated namespace resolution per paragraph

### Tests
- 18-test pytest suite (`tests/test_generator.py`) — unit tests for `_get` and `_validate_config`, integration tests covering all 3 languages, all 8 agent types, collision prevention, JSON export, legacy French keys, max-length fields, and unknown lang/type fallbacks

## [1.1.0] — 2026-04-17 (fork)

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
