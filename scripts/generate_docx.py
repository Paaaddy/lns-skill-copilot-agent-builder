#!/usr/bin/env python3
"""
generate_docx.py — Word document generator for Microsoft 365 Copilot agents.
Bilingual labels: English ("en") and German ("de"), chosen via the top-level
`lang` field in the JSON config. Defaults to "en" when unset.

Usage: python generate_docx.py <config.json> <output.docx>
"""

import json
import sys
from pathlib import Path
from datetime import datetime

try:
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print("Installing python-docx...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "python-docx", "--break-system-packages", "-q"])
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement


# ── Palette ────────────────────────────────────────────────────────────────────
ORANGE      = RGBColor(0xFF, 0x51, 0x19)
DARK        = RGBColor(0x1A, 0x1A, 0x1A)
GRAY        = RGBColor(0x88, 0x88, 0x88)
LIGHT_GRAY  = RGBColor(0xF5, 0xF5, 0xF5)
RULE_COLOR  = "DDDDDD"

# ── Typography ─────────────────────────────────────────────────────────────────
FONT_TITLE  = "Outfit"
FONT_BODY   = "Petrona"
SIZE_HERO   = 28
SIZE_H1     = 16
SIZE_H2     = 12
SIZE_BODY   = 11
SIZE_META   = 9
SIZE_SMALL  = 8

# ── Capability labels per language ──────────────────────────────────────────────
CAPABILITIES_LABELS = {
    "en": {
        "WebSearch":             "🔍 Web search",
        "OneDriveAndSharePoint": "📁 OneDrive & SharePoint",
        "Email":                 "📧 Email",
        "TeamsMessages":         "💬 Teams messages",
        "People":                "👥 People",
        "Meetings":              "📅 Meetings",
        "GraphicArt":            "🎨 Image creation",
        "CodeInterpreter":       "💻 Code interpreter",
        "Dataverse":             "🗄️ Dataverse",
    },
    "de": {
        "WebSearch":             "🔍 Websuche",
        "OneDriveAndSharePoint": "📁 OneDrive & SharePoint",
        "Email":                 "📧 E-Mail",
        "TeamsMessages":         "💬 Teams-Nachrichten",
        "People":                "👥 Personen",
        "Meetings":              "📅 Besprechungen",
        "GraphicArt":            "🎨 Bilderstellung",
        "CodeInterpreter":       "💻 Code-Interpreter",
        "Dataverse":             "🗄️ Dataverse",
    },
}

# ── UI text per language ────────────────────────────────────────────────────────
LABELS = {
    "en": {
        "default_agent_name":   "My Copilot Agent",
        "date_format":          "%Y-%m-%d",
        "supertitle":           "MICROSOFT 365 COPILOT — AGENT BUILDER",
        "subtitle":             "Complete configuration — ready to paste into Agent Builder",
        "generated_on":         "Generated on {date}   ·   https://m365.cloud.microsoft/chat/agent/new",
        "not_set":              "(not set)",
        "char_unit":            "chars",
        "section_identity":     "Agent identity",
        "section_instructions": "Instructions",
        "section_capabilities": "Capabilities to enable",
        "section_sources":      "Knowledge sources",
        "section_starters":     "Starter prompts",
        "section_disclaimer":   "Disclaimer",
        "field_name":           "Name",
        "field_description":    "Description",
        "field_instructions":   "Instructions",
        "field_capabilities":   "Capabilities",
        "field_sources":        "Sources (SharePoint URLs / websites)",
        "field_starters":       "Starter prompts",
        "field_disclaimer":     "Message shown at start",
        "hint_name":            "Copy this name into the \"Name\" field of the Agent Builder.",
        "hint_description":     "This description is shown to users browsing the agent list.",
        "hint_instructions":    "The most important field. Paste the whole content into the \"Instructions\" field. Refine after your first tests.",
        "hint_capabilities":    "Enable these capabilities in the \"Capabilities\" tab of the Agent Builder.",
        "hint_sources":         "Add these sources in the \"Knowledge\" tab. Make sure your users have access to the underlying documents.",
        "hint_disclaimer":      "This text is shown to the user at the start of every conversation.",
        "no_capabilities":      "(no capabilities specified)",
        "starter_count":        "{n} starter prompts configured   ·   max 12",
        "checklist_title":      "GO-LIVE CHECKLIST",
        "checklist_items": [
            ("Open the Agent Builder",         "https://m365.cloud.microsoft/chat/agent/new"),
            ("Fill in Name and Description",   "Fields 1 and 2"),
            ("Paste the Instructions",         "The most important field — paste in full"),
            ("Enable the Capabilities",        "\"Capabilities\" tab"),
            ("Add the Knowledge sources",      "SharePoint / OneDrive — \"Knowledge\" tab"),
            ("Enter the Starter prompts",      "Up to 12 starter prompts"),
            ("Test in Preview mode",           "Run a few starters, refine as needed"),
            ("Publish and share",              "Share with your target users"),
        ],
        "footer":               "Document generated on {date}   ·   Microsoft 365 Copilot Agent Builder   ·   https://m365.cloud.microsoft/chat/agent/new",
        "success":              "✅ Document generated: {path}",
    },
    "de": {
        "default_agent_name":   "Mein Copilot-Agent",
        "date_format":          "%d.%m.%Y",
        "supertitle":           "MICROSOFT 365 COPILOT — AGENT BUILDER",
        "subtitle":             "Vollständige Konfiguration — bereit zum Einfügen in den Agent Builder",
        "generated_on":         "Erstellt am {date}   ·   https://m365.cloud.microsoft/chat/agent/new",
        "not_set":              "(nicht angegeben)",
        "char_unit":            "Zeichen",
        "section_identity":     "Identität des Agenten",
        "section_instructions": "Anweisungen",
        "section_capabilities": "Zu aktivierende Funktionen",
        "section_sources":      "Wissensquellen",
        "section_starters":     "Startvorschläge",
        "section_disclaimer":   "Disclaimer",
        "field_name":           "Name",
        "field_description":    "Beschreibung",
        "field_instructions":   "Anweisungen",
        "field_capabilities":   "Funktionen",
        "field_sources":        "Quellen (SharePoint-URLs / Websites)",
        "field_starters":       "Startvorschläge",
        "field_disclaimer":     "Nachricht zu Beginn",
        "hint_name":            "Kopiere diesen Namen in das Feld „Name“ des Agent Builders.",
        "hint_description":     "Diese Beschreibung sehen die Nutzer:innen in der Agentenliste.",
        "hint_instructions":    "Das wichtigste Feld. Füge den gesamten Inhalt in das Feld „Anweisungen“ ein. Nach den ersten Tests feinjustieren.",
        "hint_capabilities":    "Aktiviere diese Funktionen im Tab „Funktionen“ des Agent Builders.",
        "hint_sources":         "Füge diese Quellen im Tab „Wissen“ hinzu. Stelle sicher, dass die Nutzer:innen Zugriff auf die Dokumente haben.",
        "hint_disclaimer":      "Dieser Text wird den Nutzer:innen zu Beginn jeder Unterhaltung angezeigt.",
        "no_capabilities":      "(keine Funktionen angegeben)",
        "starter_count":        "{n} Startvorschläge konfiguriert   ·   Maximum 12",
        "checklist_title":      "GO-LIVE-CHECKLISTE",
        "checklist_items": [
            ("Agent Builder öffnen",           "https://m365.cloud.microsoft/chat/agent/new"),
            ("Name und Beschreibung eintragen","Felder 1 und 2"),
            ("Anweisungen einfügen",           "Wichtigstes Feld — vollständig einfügen"),
            ("Funktionen aktivieren",          "Tab „Funktionen“"),
            ("Quellen hinzufügen",             "SharePoint / OneDrive — Tab „Wissen“"),
            ("Startvorschläge eintragen",      "Bis zu 12 Startvorschläge"),
            ("Im Preview-Modus testen",        "Startvorschläge ausprobieren, bei Bedarf anpassen"),
            ("Veröffentlichen und teilen",     "An die Zielnutzer:innen verteilen"),
        ],
        "footer":               "Dokument erstellt am {date}   ·   Microsoft 365 Copilot Agent Builder   ·   https://m365.cloud.microsoft/chat/agent/new",
        "success":              "✅ Dokument erstellt: {path}",
    },
}


# ── XML helpers ─────────────────────────────────────────────────────────────────

def set_run_font(run, font_name, size_pt, bold=False, color=None, italic=False):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'),   font_name)
    rFonts.set(qn('w:hAnsi'),   font_name)
    rFonts.set(qn('w:eastAsia'),font_name)
    rFonts.set(qn('w:cs'),      font_name)
    existing = rPr.find(qn('w:rFonts'))
    if existing is not None:
        rPr.remove(existing)
    rPr.insert(0, rFonts)


def add_rule(doc, before_pt=6, after_pt=12, color=RULE_COLOR):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before_pt)
    p.paragraph_format.space_after  = Pt(after_pt)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'),   'single')
    bottom.set(qn('w:sz'),    '4')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), color)
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def set_para_shading(para, fill_hex):
    pPr = para._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  fill_hex)
    existing = pPr.find(qn('w:shd'))
    if existing is not None:
        pPr.remove(existing)
    pPr.append(shd)


def add_left_border(para, color_hex="FF5119", size="12"):
    pPr = para._p.get_or_add_pPr()
    pBdr = pPr.find(qn('w:pBdr'))
    if pBdr is None:
        pBdr = OxmlElement('w:pBdr')
        pPr.append(pBdr)
    left = OxmlElement('w:left')
    left.set(qn('w:val'),   'single')
    left.set(qn('w:sz'),    size)
    left.set(qn('w:space'), '12')
    left.set(qn('w:color'), color_hex)
    existing = pBdr.find(qn('w:left'))
    if existing is not None:
        pBdr.remove(existing)
    pBdr.append(left)


# ── Content components ──────────────────────────────────────────────────────────

def add_section_title(doc, text, emoji=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after  = Pt(4)
    label = f"{emoji}  {text.upper()}" if emoji else text.upper()
    run = p.add_run(label)
    set_run_font(run, FONT_TITLE, SIZE_H1, bold=True, color=ORANGE)

    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'),   'single')
    bottom.set(qn('w:sz'),    '6')
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), 'FF5119')
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def add_field_block(doc, field_name, content, char_limit=None, hint=None,
                    not_set_text="(not set)", char_unit="chars"):
    label_p = doc.add_paragraph()
    label_p.paragraph_format.space_before = Pt(12)
    label_p.paragraph_format.space_after  = Pt(3)

    label_run = label_p.add_run(field_name.upper())
    set_run_font(label_run, FONT_TITLE, SIZE_H2, bold=True, color=GRAY)

    if char_limit and content:
        count = len(content)
        sep = label_p.add_run(f"   {count} / {char_limit} {char_unit}")
        set_run_font(sep, FONT_TITLE, SIZE_META, color=GRAY)

    lines = (content or not_set_text).split('\n')
    for i, line in enumerate(lines):
        cp = doc.add_paragraph()
        cp.paragraph_format.space_before = Pt(2) if i > 0 else Pt(0)
        cp.paragraph_format.space_after  = Pt(2)
        cp.paragraph_format.left_indent  = Cm(0.4)
        cp.paragraph_format.right_indent = Cm(0.2)

        run = cp.add_run(line if line.strip() else " ")
        is_empty = not content
        set_run_font(
            run,
            FONT_BODY,
            SIZE_BODY,
            color=GRAY if is_empty else DARK,
            italic=is_empty
        )
        set_para_shading(cp, "F5F5F5")
        add_left_border(cp)

    if hint:
        hp = doc.add_paragraph()
        hp.paragraph_format.space_before = Pt(3)
        hp.paragraph_format.space_after  = Pt(2)
        hp.paragraph_format.left_indent  = Cm(0.4)
        hr = hp.add_run(f"↗  {hint}")
        set_run_font(hr, FONT_TITLE, SIZE_META, color=GRAY, italic=True)


def add_suggestion_block(doc, index, title, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(2)

    num = p.add_run(f"{index}. ")
    set_run_font(num, FONT_TITLE, SIZE_BODY, bold=True, color=ORANGE)

    title_run = p.add_run(title)
    set_run_font(title_run, FONT_TITLE, SIZE_BODY, bold=True, color=DARK)

    tp = doc.add_paragraph()
    tp.paragraph_format.space_before = Pt(0)
    tp.paragraph_format.space_after  = Pt(4)
    tp.paragraph_format.left_indent  = Cm(0.5)
    tr = tp.add_run(f'"{text}"')
    set_run_font(tr, FONT_BODY, SIZE_BODY, color=GRAY, italic=True)


# ── Main generator ──────────────────────────────────────────────────────────────

def _get(config, *keys, default=""):
    """Return the first present non-empty value among keys in config."""
    for k in keys:
        if k in config and config[k] not in (None, ""):
            return config[k]
    return default


def generate_document(config: dict, output_path: str):
    lang = str(config.get("lang", "en")).lower()
    if lang not in LABELS:
        lang = "en"
    L = LABELS[lang]
    caps_labels = CAPABILITIES_LABELS[lang]

    doc = Document()

    for section in doc.sections:
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin   = Cm(2.5)
        section.right_margin  = Cm(2.5)

    agent_name = _get(config, "name", "nom", default=L["default_agent_name"])
    date_str   = datetime.now().strftime(L["date_format"])

    # ══════════════════════════════════════════════════
    # COVER
    # ══════════════════════════════════════════════════

    sup = doc.add_paragraph()
    sup.paragraph_format.space_before = Pt(0)
    sup.paragraph_format.space_after  = Pt(6)
    sup.alignment = WD_ALIGN_PARAGRAPH.LEFT
    sup_run = sup.add_run(L["supertitle"])
    set_run_font(sup_run, FONT_TITLE, SIZE_META, bold=True, color=GRAY)

    hero = doc.add_paragraph()
    hero.paragraph_format.space_before = Pt(4)
    hero.paragraph_format.space_after  = Pt(8)
    hero.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hero_run = hero.add_run(agent_name)
    set_run_font(hero_run, FONT_TITLE, SIZE_HERO, bold=True, color=ORANGE)

    sub = doc.add_paragraph()
    sub.paragraph_format.space_before = Pt(0)
    sub.paragraph_format.space_after  = Pt(6)
    sub_run = sub.add_run(L["subtitle"])
    set_run_font(sub_run, FONT_BODY, SIZE_BODY, color=GRAY)

    meta = doc.add_paragraph()
    meta.paragraph_format.space_before = Pt(0)
    meta.paragraph_format.space_after  = Pt(16)
    meta_run = meta.add_run(L["generated_on"].format(date=date_str))
    set_run_font(meta_run, FONT_TITLE, SIZE_META, color=GRAY)

    add_rule(doc, before_pt=4, after_pt=20, color="FF5119")

    # ══════════════════════════════════════════════════
    # 1. IDENTITY
    # ══════════════════════════════════════════════════
    add_section_title(doc, L["section_identity"], "🤖")

    add_field_block(doc, L["field_name"], _get(config, "name", "nom"),
                    char_limit=100, hint=L["hint_name"],
                    not_set_text=L["not_set"], char_unit=L["char_unit"])

    add_field_block(doc, L["field_description"], _get(config, "description"),
                    char_limit=1000, hint=L["hint_description"],
                    not_set_text=L["not_set"], char_unit=L["char_unit"])

    # ══════════════════════════════════════════════════
    # 2. INSTRUCTIONS
    # ══════════════════════════════════════════════════
    add_section_title(doc, L["section_instructions"], "📋")

    add_field_block(doc, L["field_instructions"], _get(config, "instructions"),
                    char_limit=8000, hint=L["hint_instructions"],
                    not_set_text=L["not_set"], char_unit=L["char_unit"])

    # ══════════════════════════════════════════════════
    # 3. CAPABILITIES
    # ══════════════════════════════════════════════════
    add_section_title(doc, L["section_capabilities"], "⚙️")

    caps = _get(config, "capabilities", "fonctionnalites", default=[]) or []
    caps_text = "\n".join([f"✅  {caps_labels.get(c, c)}" for c in caps]) \
        if caps else L["no_capabilities"]

    add_field_block(doc, L["field_capabilities"], caps_text,
                    hint=L["hint_capabilities"],
                    not_set_text=L["not_set"], char_unit=L["char_unit"])

    # ══════════════════════════════════════════════════
    # 4. KNOWLEDGE SOURCES
    # ══════════════════════════════════════════════════
    sources = _get(config, "knowledge_sources", "sources_connaissances", default=[]) or []
    if sources:
        add_section_title(doc, L["section_sources"], "📚")
        sources_text = "\n".join([f"•  {s}" for s in sources])
        add_field_block(doc, L["field_sources"], sources_text,
                        hint=L["hint_sources"],
                        not_set_text=L["not_set"], char_unit=L["char_unit"])

    # ══════════════════════════════════════════════════
    # 5. STARTER PROMPTS
    # ══════════════════════════════════════════════════
    starters = _get(config, "starters", "suggestions_demarrage", default=[]) or []
    if starters:
        add_section_title(doc, L["section_starters"], "💬")

        count_p = doc.add_paragraph()
        count_p.paragraph_format.space_before = Pt(2)
        count_p.paragraph_format.space_after  = Pt(8)
        count_run = count_p.add_run(L["starter_count"].format(n=len(starters)))
        set_run_font(count_run, FONT_TITLE, SIZE_META, color=GRAY)

        for i, s in enumerate(starters, 1):
            title = s.get("title") or s.get("titre") or f"{L['field_starters']} {i}"
            text  = s.get("text")  or s.get("texte")  or ""
            add_suggestion_block(doc, i, title, text)

    # ══════════════════════════════════════════════════
    # 6. DISCLAIMER
    # ══════════════════════════════════════════════════
    disclaimer = _get(config, "disclaimer")
    if disclaimer:
        add_section_title(doc, L["section_disclaimer"], "⚠️")
        add_field_block(doc, L["field_disclaimer"], disclaimer,
                        char_limit=500, hint=L["hint_disclaimer"],
                        not_set_text=L["not_set"], char_unit=L["char_unit"])

    # ══════════════════════════════════════════════════
    # CHECKLIST
    # ══════════════════════════════════════════════════
    add_rule(doc, before_pt=24, after_pt=16, color="FF5119")

    cl_title = doc.add_paragraph()
    cl_title.paragraph_format.space_before = Pt(0)
    cl_title.paragraph_format.space_after  = Pt(10)
    cl_run = cl_title.add_run(L["checklist_title"])
    set_run_font(cl_run, FONT_TITLE, SIZE_H1, bold=True, color=ORANGE)

    for label, detail in L["checklist_items"]:
        cp = doc.add_paragraph()
        cp.paragraph_format.space_before = Pt(4)
        cp.paragraph_format.space_after  = Pt(4)
        cp.paragraph_format.left_indent  = Cm(0.2)

        checkbox = cp.add_run("☐  ")
        set_run_font(checkbox, FONT_TITLE, SIZE_BODY, bold=True, color=ORANGE)

        label_run = cp.add_run(label)
        set_run_font(label_run, FONT_TITLE, SIZE_BODY, bold=True, color=DARK)

        detail_run = cp.add_run(f"  —  {detail}")
        set_run_font(detail_run, FONT_BODY, SIZE_BODY, color=GRAY)

    foot = doc.add_paragraph()
    foot.paragraph_format.space_before = Pt(24)
    foot.paragraph_format.space_after  = Pt(0)
    foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    foot_run = foot.add_run(L["footer"].format(date=date_str))
    set_run_font(foot_run, FONT_TITLE, SIZE_SMALL, color=GRAY)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    print(L["success"].format(path=output_path))
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_docx.py <config.json> <output.docx>")
        sys.exit(1)

    config_path  = sys.argv[1]
    output_path  = sys.argv[2]

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    generate_document(config, output_path)
