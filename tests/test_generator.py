"""
Tests for scripts/generate_docx.py
Run: pytest tests/test_generator.py
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from generate_docx import (
    CAPABILITIES_LABELS,
    NEXT_STEPS,
    VERSION,
    _get,
    _validate_config,
    generate_document,
)


# ── Fixtures ────────────────────────────────────────────────────────────────────

def minimal_config(lang="en", agent_type="custom"):
    return {
        "lang": lang,
        "name": "Test Agent",
        "description": "A test agent.",
        "instructions": "Do things professionally.",
        "capabilities": ["WebSearch"],
        "knowledge_sources": [],
        "starters": [],
        "disclaimer": "",
        "agent_type": agent_type,
    }


# ── Unit: _get helper ──────────────────────────────────────────────────────────

def test_get_first_key():
    assert _get({"name": "Alice", "nom": "Bob"}, "name", "nom") == "Alice"

def test_get_fallback_key():
    assert _get({"nom": "Bob"}, "name", "nom") == "Bob"

def test_get_default_when_missing():
    assert _get({}, "name", default="fallback") == "fallback"

def test_get_skips_none():
    assert _get({"name": None, "nom": "Bob"}, "name", "nom") == "Bob"


# ── Unit: _validate_config ─────────────────────────────────────────────────────

def test_validate_missing_name_raises():
    with pytest.raises(ValueError, match="name"):
        _validate_config({"lang": "en", "instructions": "Do things."})

def test_validate_missing_instructions_raises():
    with pytest.raises(ValueError, match="instructions"):
        _validate_config({"lang": "en", "name": "Agent"})

def test_validate_both_missing_raises():
    with pytest.raises(ValueError):
        _validate_config({"lang": "en"})

def test_validate_valid_config_passes():
    _validate_config({"lang": "en", "name": "Agent", "instructions": "Do things."})


# ── Integration: generate_document ────────────────────────────────────────────

@pytest.mark.integration
def test_minimal_config_generates_docx(tmp_path):
    out = tmp_path / "agent_test.docx"
    result = generate_document(minimal_config(), str(out))
    assert Path(result).exists()
    assert Path(result).suffix == ".docx"

@pytest.mark.integration
def test_collision_prevention(tmp_path):
    out = tmp_path / "agent_test.docx"
    result1 = generate_document(minimal_config(), str(out))
    out.touch()  # simulate a pre-existing file at original path
    result2 = generate_document(minimal_config(), str(out))
    assert result1 != result2
    assert Path(result2).exists()

@pytest.mark.integration
def test_json_export_created_alongside_docx(tmp_path):
    out = tmp_path / "agent_test.docx"
    config = minimal_config()
    result = generate_document(config, str(out))
    json_out = Path(result).with_suffix(".json")
    assert json_out.exists()
    exported = json.loads(json_out.read_text())
    assert exported["name"] == config["name"]

@pytest.mark.integration
def test_all_capabilities_all_languages(tmp_path):
    all_caps = list(CAPABILITIES_LABELS["en"].keys())
    for lang in ("en", "fr", "de"):
        config = minimal_config(lang=lang)
        config["capabilities"] = all_caps
        result = generate_document(config, str(tmp_path / f"agent_{lang}.docx"))
        assert Path(result).exists()

@pytest.mark.integration
def test_agent_type_next_steps_all_types(tmp_path):
    for agent_type in NEXT_STEPS["en"].keys():
        config = minimal_config(agent_type=agent_type)
        result = generate_document(config, str(tmp_path / f"agent_{agent_type}.docx"))
        assert Path(result).exists()

@pytest.mark.integration
def test_unknown_agent_type_falls_back_to_custom(tmp_path):
    config = minimal_config()
    config["agent_type"] = "nonexistent_type"
    result = generate_document(config, str(tmp_path / "agent_unknown.docx"))
    assert Path(result).exists()

@pytest.mark.integration
def test_french_legacy_keys_accepted(tmp_path):
    config = {
        "lang": "fr",
        "nom": "Agent Test",
        "description": "Un agent de test.",
        "instructions": "Faire des choses professionnellement.",
        "fonctionnalites": ["WebSearch"],
        "sources_connaissances": [],
        "suggestions_demarrage": [],
        "agent_type": "custom",
    }
    result = generate_document(config, str(tmp_path / "agent_fr_legacy.docx"))
    assert Path(result).exists()

@pytest.mark.integration
def test_max_length_fields_no_crash(tmp_path):
    config = minimal_config()
    config["name"] = "A" * 100
    config["description"] = "B" * 1000
    config["instructions"] = "C" * 8000
    config["disclaimer"] = "D" * 500
    config["starters"] = [
        {"title": f"Starter {i}", "text": f"Text for starter {i}"}
        for i in range(12)
    ]
    result = generate_document(config, str(tmp_path / "agent_maxlen.docx"))
    assert Path(result).exists()

@pytest.mark.integration
def test_unknown_lang_defaults_to_en(tmp_path):
    config = minimal_config()
    config["lang"] = "zz"
    result = generate_document(config, str(tmp_path / "agent_badlang.docx"))
    assert Path(result).exists()

def test_version_is_2_0_0():
    assert VERSION == "2.0.0"
