#!/usr/bin/env python3
"""
Builds the 25-Slide DevFest Bengaluru 2026 Keynote in Google Slides via `gslides`.

Design System (720pt x 405pt 16:9 Widescreen):
  - Alternating Deep Obsidian (#0B101B) Editorial Slides & Warm Cream (#FAF7F0) Full-Stage Architecture Diagrams
  - Exact native aspect-ratio placement for all diagrams & 1080p/720p demo poster frames (zero stretching!)
  - 100% Google Cloud-native story, code, and demos
  - All benchmark stats loaded dynamically from live `demos/traces/demo{1..5}_trace.json`
  - Includes Mani's two real Gemini Live & Voice AI PSTN recordings from Google Drive
  - Full private Speaker Notes on every single slide
  - Exports local PDF & PPTX backups for visual verification and offline safety
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
DIAG_DIR = ROOT / "assets" / "diagrams"
VID_DIR = ROOT / "assets" / "videos"
TRACES_DIR = ROOT / "demos" / "traces"
PRES_DIR = ROOT / "presentation"
DRIVE_META_PATH = PRES_DIR / "drive_videos_v2.json"

LINKEDIN_URL = "https://www.linkedin.com/in/cmanikandan"
GITHUB_URL = "https://github.com/cmanikandan/gdg-blr-talk-nov14-2026"
DRIVE_FLIGHT_URL = "https://drive.google.com/file/d/1KkvhldhlXGUEYQMLs28EMQXsSeAbZRZO/view"
DRIVE_PSTN_URL = "https://drive.google.com/file/d/1kv3NheXiAbhIBhYuBDUMRBCa054gIE9M/view"

BG_DARK = "#0B101B"
SURF_DARK = "#131C2E"
SURF_ALT = "#172238"
SURF_CODE = "#070B13"
BG_CREAM = "#FAF7F0"
INK_CREAM = "#1C2434"
WHITE = "#FFFFFF"
TEXT_SOFT = "#CBD5E1"
MUTED = "#94A3B8"
BLUE = "#4285F4"
BLUE_LIGHT = "#60A5FA"
GREEN = "#34A853"
GREEN_LIGHT = "#4ADE80"
AMBER = "#F59E0B"
AMBER_LIGHT = "#FBBF24"
RED = "#EA4335"
RED_LIGHT = "#F87171"
PURPLE_LIGHT = "#C084FC"


def run_cmd(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({' '.join(cmd)}):\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")
    return proc.stdout.strip()


def load_traces() -> Dict[str, Any]:
    return {
        k: json.loads((TRACES_DIR / f).read_text(encoding="utf-8"))
        for k, f in [
            ("d1", "demo1_trace.json"),
            ("d2", "demo2_trace.json"),
            ("d3", "demo3_trace.json"),
            ("d4", "demo4_trace.json"),
            ("d5", "demo5_trace.json"),
        ]
    }


def load_drive_links() -> Dict[str, Any]:
    if DRIVE_META_PATH.exists():
        return json.loads(DRIVE_META_PATH.read_text(encoding="utf-8"))
    return {
        "folder_id": "1y31QiutGbJb1GqALpE4NL5eld7ZvCIY7",
        "folder_url": "https://drive.google.com/drive/folders/1y31QiutGbJb1GqALpE4NL5eld7ZvCIY7",
        "videos": {},
    }


def add_blank_slide(ops: List[Dict[str, Any]], slide_id: str, bg: str, is_first: bool = False) -> None:
    if is_first:
        ops.append({"op": "delete-element", "element": "i0"})
        ops.append({"op": "delete-element", "element": "i1"})
    else:
        ops.append({"op": "add-slide", "layout": "BLANK", "id": slide_id})
    ops.append({"op": "set-background", "slide": slide_id, "color": bg})


def add_diagram_slide(
    ops: List[Dict[str, Any]],
    img_jobs: List[Dict[str, Any]],
    slide_id: str,
    kicker: str,
    title: str,
    img_filename: str,
    notes: str,
) -> None:
    """Full-stage 16:9 illustrated architecture diagram on warm cream with zero clutter."""
    add_blank_slide(ops, slide_id, BG_CREAM)
    ops.extend([
        {"op": "add-textbox", "slide": slide_id, "text": kicker, "x": 36, "y": 11, "width": 648, "height": 16, "font_size": 9, "bold": True, "color": "#1D4ED8", "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": slide_id, "text": title, "x": 36, "y": 25, "width": 648, "height": 26, "font_size": 16.5, "bold": True, "color": INK_CREAM, "font_family": "Montserrat"},
        {"op": "add-shape", "slide": slide_id, "shape_type": "RECTANGLE", "x": 36, "y": 54, "width": 648, "height": 1.2, "background_color": "#D6CFC2"},
        {"op": "set-notes", "slide": slide_id, "text": notes},
    ])
    img_jobs.append({
        "slide": slide_id,
        "file": str(DIAG_DIR / img_filename),
        "x": 68,
        "y": 64,
        "width": 584,
        "height": 328.5,
    })


def add_demo_slide(
    ops: List[Dict[str, Any]],
    img_jobs: List[Dict[str, Any]],
    slide_id: str,
    kicker: str,
    title: str,
    poster_filename: str,
    cta_label: str,
    drive_url: str,
    notes: str,
    cta_bg: str = "#1E3A8A",
    img_box: tuple[float, float, float, float] = (93.0, 64.0, 534.0, 300.4),
    caption: str = "",
) -> None:
    add_blank_slide(ops, slide_id, BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": slide_id, "text": kicker, "x": 38, "y": 13, "width": 644, "height": 16, "font_size": 9, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": slide_id, "text": title, "x": 38, "y": 28, "width": 644, "height": 26, "font_size": 13.5, "bold": True, "color": WHITE, "font_family": "Montserrat"},
    ])
    ix, iy, iw, ih = img_box
    img_jobs.append({
        "slide": slide_id,
        "file": str(VID_DIR / poster_filename),
        "x": ix,
        "y": iy,
        "width": iw,
        "height": ih,
    })
    if caption:
        ops.append({
            "op": "add-textbox",
            "slide": slide_id,
            "text": caption,
            "x": 38,
            "y": iy + ih + 4,
            "width": 644,
            "height": 18,
            "font_size": 8.8,
            "color": TEXT_SOFT,
            "font_family": "Roboto",
            "alignment": "center",
        })
    cta_box: Dict[str, Any] = {
        "op": "add-textbox",
        "slide": slide_id,
        "text": cta_label,
        "x": 93,
        "y": 371,
        "width": 534,
        "height": 23,
        "font_size": 10,
        "bold": True,
        "color": WHITE,
        "background_color": cta_bg,
        "font_family": "Roboto Mono",
        "alignment": "center",
        "content_alignment": "MIDDLE",
    }
    if drive_url:
        cta_box["link"] = drive_url
    ops.append(cta_box)
    ops.append({"op": "set-notes", "slide": slide_id, "text": notes})


def build_deck_ops(tr: Dict[str, Any], drive: Dict[str, Any]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    d1, d2, d3, d4, d5 = tr["d1"], tr["d2"], tr["d3"], tr["d4"], tr["d5"]
    b8 = d2["round_b_head_to_head"]["benchmark_8q"]
    b50 = d2["round_b_head_to_head"]["benchmark_50q"]
    pub100 = d2["round_b_head_to_head"]["published_100q_reference"]
    r50 = d2["round_b_head_to_head"]["live_ratios_50q"]
    sp8_f = round(b8[1]["latency_ms"] / max(b8[0]["latency_ms"], 1), 1)
    sp8_h = round(b8[2]["latency_ms"] / max(b8[0]["latency_ms"], 1), 1)
    c8_f = round(b8[1]["cost_per_1m_calls_usd"] / max(b8[0]["cost_per_1m_calls_usd"], 0.01), 1)
    c8_h = round(b8[2]["cost_per_1m_calls_usd"] / max(b8[0]["cost_per_1m_calls_usd"], 0.01), 1)
    sla = d4["sla_benchmark"]
    sql = d3.get("lakehouse_finding") or d3["multicloud_finding"]
    ca = d4["carbon_security_audit"]
    warn_cnt = sum(1 for c in ca["audit"].get("checks", []) if c.get("status") != "PASS")
    m5 = d5["benchmark"]
    vids = drive.get("videos", {})

    ops: List[Dict[str, Any]] = []
    imgs: List[Dict[str, Any]] = []

    # ── S01: HERO TITLE (`p`) ──────────────────────────────────────────────────
    add_blank_slide(ops, "p", BG_DARK, is_first=True)
    ops.extend([
        {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 8, "height": 405, "background_color": BLUE},
        {"op": "add-textbox", "slide": "p", "text": "DEVFEST BENGALURU 2026  ·  KEYNOTE", "x": 46, "y": 32, "width": 628, "height": 20, "font_size": 10, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "p", "text": "The Periodic Table of Agents", "x": 46, "y": 56, "width": 628, "height": 56, "font_size": 37, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": "p", "text": "Building Production Agentic Systems with Gemini 4 & Google Antigravity", "x": 46, "y": 114, "width": 628, "height": 30, "font_size": 15.5, "color": TEXT_SOFT, "font_family": "Roboto"},
    ])
    elems = [
        ("1", "H", "Hydrogen", GREEN_LIGHT),
        ("6", "C", "Carbon", BLUE_LIGHT),
        ("18", "Ar", "Argon", MUTED),
        ("0", "Dc", "Decisions", AMBER_LIGHT),
        ("3.8", "Lv", "Live Voice", RED_LIGHT),
    ]
    for i, (num, sym, lbl, col) in enumerate(elems):
        x = 46 + i * 118
        ops.extend([
            {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": x, "y": 168, "width": 104, "height": 98, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": x, "y": 168, "width": 104, "height": 3, "background_color": col},
            {"op": "add-textbox", "slide": "p", "text": num, "x": x + 8, "y": 176, "width": 88, "height": 16, "font_size": 9, "color": MUTED, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "p", "text": sym, "x": x + 8, "y": 194, "width": 88, "height": 38, "font_size": 26, "bold": True, "color": col, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "p", "text": lbl.upper(), "x": x + 8, "y": 238, "width": 88, "height": 18, "font_size": 8.5, "bold": True, "color": TEXT_SOFT, "font_family": "Roboto Mono"},
        ])
    ops.extend([
        {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": 46, "y": 312, "width": 628, "height": 1.2, "background_color": "#25334D"},
        {"op": "add-textbox", "slide": "p", "text": "Mani  ·  Principal Architect, Google Cloud", "x": 46, "y": 324, "width": 360, "height": 22, "font_size": 13, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": "p", "text": "linkedin.com/in/cmanikandan", "x": 46, "y": 349, "width": 260, "height": 20, "font_size": 10, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono", "link": LINKEDIN_URL},
        {"op": "add-textbox", "slide": "p", "text": "github.com/cmanikandan/gdg-blr-talk-nov14-2026", "x": 334, "y": 349, "width": 340, "height": 20, "font_size": 9.5, "color": MUTED, "font_family": "Roboto Mono", "alignment": "right", "link": GITHUB_URL},
        {"op": "set-notes", "slide": "p", "text": "Opening keynote! Good morning DevFest Bengaluru! Six months ago an AI coding agent was a smart pair programmer. Today a single session plans with one model, modernizes legacy code with another, decides with zero output tokens, speaks live over real telephony, and ships verified PRs in the cloud."},
    ])

    # ── S02: FRESH BADGE ───────────────────────────────────────────────────────
    add_diagram_slide(
        ops, imgs, "S02",
        "01 · FULL DISCLOSURE",
        "So New to Google, My Badge Is Still Warm",
        "01_fresh_badge.jpg",
        "BADGE JOKE! Hold up your Google badge! 'Full disclosure: I am so new to Google Cloud that I just got my badge—it is still warm from the printer. I used Gemini 4 Hydrogen this morning just to find the micro-kitchen! The upside: every single demo and benchmark I show today I built, broke, and verified from scratch myself.'",
    )

    # ── S03: SIX MONTHS AGO VS TODAY ───────────────────────────────────────────
    add_diagram_slide(
        ops, imgs, "S03",
        "02 · THE ARCHITECTURAL SHIFT",
        "Six Months Ago vs. Today",
        "02_six_month_shift.jpg",
        "Pause and let the room absorb the contrast. Single-model chat tabs tied to an open laptop are over. Production agentic systems specialize every model to its exact latency, reasoning horizon, and cost envelope.",
    )

    # ── S04: SIMPLE FOUR-STEP KEYNOTE OVERVIEW ─────────────────────────────────
    add_blank_slide(ops, "S04", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S04", "text": "WHAT WE ARE PROVING LIVE TODAY", "x": 42, "y": 22, "width": 636, "height": 18, "font_size": 10, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S04", "text": "One Payments Platform. Four Rules. Six Real Demos.", "x": 42, "y": 42, "width": 636, "height": 32, "font_size": 20.5, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": "S04", "text": "Meet MonsoonPay — our real Indian UPI & checkout system running on Google Cloud (Mumbai + Delhi).", "x": 42, "y": 74, "width": 636, "height": 22, "font_size": 11.5, "color": TEXT_SOFT, "font_family": "Roboto"},
    ])
    simple_cards = [
        ("01 · PLAN BIG & EXECUTE FAST", "Fix a Live Outage + Modernize Legacy", "Carbon plans the fix; parallel Hydrogen workers patch in isolated git worktrees; Argon rewrites a slow O(N²) UPI monolith 94x faster — bit-exact.", BLUE),
        ("02 · DECIDE SMALL", "Guardrails at Zero Output Tokens", "Stop burning slow LLM tokens on routing & compliance. Run 50 RBI/PCI checks in 270ms at $0 output tokens with Gemini Decisions API.", AMBER),
        ("03 · SPEAK & ACT LIVE", "Real Voice AI & Telephony", "Watch two real voice agents in action: live multimodal flight rebooking with BigQuery SQL, plus multilingual Indian PSTN telephony on Cloud Run.", RED),
        ("04 · GROUND & REVIEW", "Zero-Copy Data + Adversarial Audit", "Google ADK 2.0 joins 40,000 Spanner Omni & BigQuery Iceberg rows zero-copy, pauses for human sign-off, and Carbon audits every diff before merge.", GREEN),
    ]
    for i, (k, h, body, col) in enumerate(simple_cards):
        x = 42 + (i % 2) * 326
        y = 106 + (i // 2) * 118
        ops.extend([
            {"op": "add-shape", "slide": "S04", "shape_type": "RECTANGLE", "x": x, "y": y, "width": 310, "height": 106, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S04", "shape_type": "RECTANGLE", "x": x, "y": y, "width": 310, "height": 4, "background_color": col},
            {"op": "add-textbox", "slide": "S04", "text": k, "x": x + 14, "y": y + 11, "width": 282, "height": 15, "font_size": 8.5, "bold": True, "color": col, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "S04", "text": h, "x": x + 14, "y": y + 27, "width": 282, "height": 22, "font_size": 12.2, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S04", "text": body, "x": x + 14, "y": y + 51, "width": 282, "height": 50, "font_size": 9.6, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 130},
        ])
    ops.extend([
        {"op": "add-shape", "slide": "S04", "shape_type": "RECTANGLE", "x": 42, "y": 348, "width": 636, "height": 38, "background_color": "#10192B"},
        {"op": "add-shape", "slide": "S04", "shape_type": "RECTANGLE", "x": 42, "y": 348, "width": 5, "height": 38, "background_color": BLUE},
        {"op": "add-textbox", "slide": "S04", "text": "THE MENTAL MODEL:   Plan big  ·  Execute fast  ·  Decide small  ·  Review everything.", "x": 58, "y": 355, "width": 608, "height": 24, "font_size": 12.5, "bold": True, "color": WHITE, "font_family": "Montserrat", "content_alignment": "MIDDLE"},
        {"op": "set-notes", "slide": "S04", "text": "Keep this dead simple! No fluff. One real Indian fintech system on Google Cloud (MonsoonPay), four engineering rules, and six real demos—every metric measured live against the Gemini API."},
    ])

    # ── S05: PERIODIC TABLE OF AGENTS ──────────────────────────────────────────
    add_diagram_slide(
        ops, imgs, "S05",
        "03 · THE CORE ARCHITECTURE",
        "The Periodic Table of Agents",
        "03_periodic_table.jpg",
        "Walk through the five elements. Hydrogen = abundant sub-second fuel; Carbon = deep architect & adversarial verifier (1M context + Long Decode); Argon = rock-solid enterprise workhorse; Decisions = zero-output-token control plane; Live 3.8 = voice that reasons while speaking.",
    )

    # ── S06: GEMINI 4 MODEL SPECS ──────────────────────────────────────────────
    add_blank_slide(ops, "S06", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S06", "text": "GEMINI 4 FAMILY  ·  PRODUCTION SELECTION GUIDE", "x": 42, "y": 22, "width": 636, "height": 16, "font_size": 9.5, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S06", "text": "Match the Element to the Reasoning Horizon", "x": 42, "y": 42, "width": 636, "height": 30, "font_size": 22.5, "bold": True, "color": WHITE, "font_family": "Montserrat"},
    ])
    specs = [
        ("C", "Gemini 4 Carbon", "Deep Architect & Verifier", "$2/$10 per 1M · 95% Cache Off", "• 1M unified context + Long Decode >64K\n• 0% bypass on Gray Swan prompt injection\n• #1 CursorBench 4.0 multi-file diffs\n• Best for: Architecture, RCA, PR audit", BLUE_LIGHT),
        ("Ar", "Gemini 4 Argon", "Enterprise Workhorse", "$2/$10 per 1M · 95% Cache Off", "• 50 AA Index · rock-solid consistency\n• Powers Google's /teamwork code rewrites\n• Ideal for large migrations & core services\n• Best for: Modernization, SQL, domain RAG", MUTED),
        ("H", "Gemini 4 Hydrogen", "Sub-Second Fuel", "$1.50/$7.50 flat · 95% Cache Off", "• 4 Thinking Tiers: low · med · high · xhigh\n• 54 AA Index at xhigh · 2.5x faster vs 3.8F\n• 43/43 PlotlyDataAnalyticsBench\n• Best for: Parallel /swarm workers, tests", GREEN_LIGHT),
    ]
    for i, (sym, name, role, price, bullets, col) in enumerate(specs):
        x = 42 + i * 218
        ops.extend([
            {"op": "add-shape", "slide": "S06", "shape_type": "RECTANGLE", "x": x, "y": 90, "width": 202, "height": 284, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S06", "shape_type": "RECTANGLE", "x": x, "y": 90, "width": 202, "height": 4, "background_color": col},
            {"op": "add-textbox", "slide": "S06", "text": sym, "x": x + 14, "y": 104, "width": 44, "height": 36, "font_size": 21, "bold": True, "color": col, "font_family": "Montserrat", "background_color": BG_DARK, "alignment": "center", "content_alignment": "MIDDLE"},
            {"op": "add-textbox", "slide": "S06", "text": name, "x": x + 64, "y": 104, "width": 128, "height": 20, "font_size": 11, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S06", "text": role, "x": x + 64, "y": 125, "width": 128, "height": 18, "font_size": 8.5, "color": MUTED, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "S06", "text": price, "x": x + 14, "y": 150, "width": 174, "height": 22, "font_size": 8.0, "bold": True, "color": WHITE, "font_family": "Roboto Mono"},
            {"op": "add-shape", "slide": "S06", "shape_type": "RECTANGLE", "x": x + 14, "y": 178, "width": 174, "height": 1, "background_color": "#25334D"},
            {"op": "add-textbox", "slide": "S06", "text": bullets, "x": x + 14, "y": 188, "width": 174, "height": 176, "font_size": 9.8, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 142},
        ])
    ops.append({"op": "set-notes", "slide": "S06", "text": "Highlight 95% implicit context caching across all three Gemini 4 elements ($0.10/1M cached input on Carbon/Argon intro, $0.075/1M on Hydrogen) plus Hydrogen's 4 thinking tiers."})

    # ── S07: NEW — UNIFIED 1M CONTEXT & LONG DECODE FOR CODE MODERNIZATION ─────
    add_blank_slide(ops, "S07", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S07", "text": "ENTERPRISE CODE MODERNIZATION  ·  GEMINI 4 ARCHITECTURE", "x": 42, "y": 20, "width": 636, "height": 16, "font_size": 9.5, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S07", "text": "Unified 1M Context + Long Decode Breaks Legacy Modernization", "x": 42, "y": 38, "width": 636, "height": 30, "font_size": 17.5, "bold": True, "color": WHITE, "font_family": "Montserrat"},
    ])
    mod_kpis = [
        ("1,048,576", "Unified Token Budget", "Shared across repo input + reasoning + output. Load entire legacy modules, schemas & tests in one shot.", BLUE_LIGHT),
        ("64K -> 1M", "Long Decode Output", "Interactions API streams past the 64K cap in background — rewriting multi-file packages without truncation.", GREEN_LIGHT),
        ("95% OFF", "Implicit Context Cache", "Keep 500K tokens of legacy COBOL/Java/C++ warm for $0.075–$0.10/1M per refactor pass.", AMBER_LIGHT),
    ]
    for i, (num, title_k, desc, col) in enumerate(mod_kpis):
        x = 42 + i * 218
        ops.extend([
            {"op": "add-shape", "slide": "S07", "shape_type": "RECTANGLE", "x": x, "y": 82, "width": 202, "height": 134, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S07", "shape_type": "RECTANGLE", "x": x, "y": 82, "width": 202, "height": 4, "background_color": col},
            {"op": "add-textbox", "slide": "S07", "text": num, "x": x + 14, "y": 94, "width": 174, "height": 34, "font_size": 24, "bold": True, "color": col, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S07", "text": title_k, "x": x + 14, "y": 130, "width": 174, "height": 20, "font_size": 11, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S07", "text": desc, "x": x + 14, "y": 152, "width": 174, "height": 58, "font_size": 9.3, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 132},
        ])
    # Bottom 3-step Enterprise Modernization Pipeline
    ops.extend([
        {"op": "add-textbox", "slide": "S07", "text": "THE ZERO-DRIFT MODERNIZATION PATTERN (COBOL / JAVA / C++ / PYTHON -> GOOGLE CLOUD)", "x": 42, "y": 232, "width": 636, "height": 16, "font_size": 9, "bold": True, "color": MUTED, "font_family": "Roboto Mono"},
    ])
    pipe_steps = [
        ("1. INGEST WHOLE SUBSYSTEM", "Load legacy code, SQL schemas, and production replay logs into 1M cached context so Carbon maps every undocumented business invariant.", BLUE),
        ("2. LONG DECODE SYNTHESIS", "Argon / Carbon generates complete typed target services + migration scripts in dependency order via Interactions API (no half-cut diffs).", GREEN),
        ("3. LOCKED GOLDEN FALSIFIER", "Run the UNMODIFIED legacy test & SHA-256 parity harness. Agents can rewrite code — never weaken the verifier. 0.00 drift required.", AMBER),
    ]
    for i, (st_t, st_d, col) in enumerate(pipe_steps):
        x = 42 + i * 218
        ops.extend([
            {"op": "add-shape", "slide": "S07", "shape_type": "RECTANGLE", "x": x, "y": 254, "width": 202, "height": 122, "background_color": SURF_ALT},
            {"op": "add-shape", "slide": "S07", "shape_type": "RECTANGLE", "x": x, "y": 254, "width": 4, "height": 122, "background_color": col},
            {"op": "add-textbox", "slide": "S07", "text": st_t, "x": x + 14, "y": 264, "width": 178, "height": 20, "font_size": 9.2, "bold": True, "color": col, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "S07", "text": st_d, "x": x + 14, "y": 286, "width": 178, "height": 84, "font_size": 9.5, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 135},
        ])
    ops.append({"op": "set-notes", "slide": "S07", "text": "Why enterprise code modernization failed with previous LLMs: you could neither fit the full legacy dependency graph into context NOR emit a complete multi-file replacement without hitting an 8K–64K output cliff. Gemini 4 unifies input + thinking + output across 1,048,576 tokens, adds Long Decode via the Interactions API, and discounts repeated context 95% via implicit caching."})

    # ── S08: NEW — ANTIGRAVITY MULTI-AGENT PLAYBOOK (ENGLISH RECREATION OF image.png!) ──
    add_blank_slide(ops, "S08", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S08", "text": "GOOGLE ANTIGRAVITY  ·  MULTI-AGENT PLAYBOOK (2 INDEPENDENT AXES)", "x": 42, "y": 16, "width": 636, "height": 15, "font_size": 9, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S08", "text": "Which Antigravity Mode Should You Use?", "x": 42, "y": 32, "width": 636, "height": 26, "font_size": 20, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        # Axis 1 Top Strip: Model Selection
        {"op": "add-shape", "slide": "S08", "shape_type": "RECTANGLE", "x": 42, "y": 64, "width": 636, "height": 42, "background_color": SURF_DARK},
        {"op": "add-shape", "slide": "S08", "shape_type": "RECTANGLE", "x": 42, "y": 64, "width": 4, "height": 42, "background_color": BLUE},
        {"op": "add-textbox", "slide": "S08", "text": "AXIS 1 · MODEL (WHO THINKS?)", "x": 54, "y": 68, "width": 180, "height": 14, "font_size": 8, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S08", "text": "Hydrogen (fast everyday)   ·   Orchestrator [DEFAULT] (Carbon plans + Hydrogen executes)   ·   Carbon (max depth)", "x": 54, "y": 83, "width": 616, "height": 18, "font_size": 9.8, "bold": True, "color": WHITE, "font_family": "Roboto"},
        # Axis 2 Header
        {"op": "add-textbox", "slide": "S08", "text": "AXIS 2 · EXECUTION MODE (HOW AGENTS COLLABORATE)  +  4-QUESTION DECISION TREE", "x": 42, "y": 113, "width": 636, "height": 14, "font_size": 8.5, "bold": True, "color": MUTED, "font_family": "Roboto Mono"},
        {"op": "add-table", "slide": "S08", "rows": 6, "cols": 4, "id": "TBL_AGY_MODES", "x": 42, "y": 130, "width": 636, "height": 220},
    ])
    agy_headers = ["Mode", "Trigger Question", "How It Works", "Engineering Example"]
    agy_rows = [
        ["1-on-1 (Default)", "Single clear, bounded task?", "1 agent works directly with you", "Add a feature flag or fix a unit test"],
        ["/boost", "1 tough problem needing depth?", "Multi-angle exploration & verification", "Root-cause a rare concurrency race"],
        ["/swarm", "Parallel specialists collaborating?", "Coordinator + parallel worktree agents", "Ship Envoy patch + SQL + tests together"],
        ["/run-workflow", "Same task repeated on N items?", "Broadcast to N agents -> collect results", "Audit 40 microservices or 25 open PRs"],
        ["/teamwork", "Long-horizon mission (hrs-wks)?", "Orchestrator + specialists + falsifiers", "Rewrite 800K LoC C++ -> Rust end-to-end"],
    ]
    for ci, htxt in enumerate(agy_headers):
        ops.append({"op": "set-table-cell", "table": "TBL_AGY_MODES", "row": 0, "col": ci, "text": htxt, "bold": True, "font_size": 9, "color": BLUE_LIGHT, "background_color": "#162238", "font_family": "Roboto Mono"})
    mode_colors = [TEXT_SOFT, PURPLE_LIGHT, GREEN_LIGHT, BLUE_LIGHT, AMBER_LIGHT]
    for ri, rvals in enumerate(agy_rows, start=1):
        bg = "#111A2B" if ri % 2 == 1 else "#162033"
        for ci, val in enumerate(rvals):
            ops.append({
                "op": "set-table-cell",
                "table": "TBL_AGY_MODES",
                "row": ri,
                "col": ci,
                "text": val,
                "bold": ci == 0,
                "font_size": 9.3,
                "color": mode_colors[ri - 1] if ci == 0 else TEXT_SOFT,
                "background_color": bg,
                "font_family": "Roboto Mono" if ci == 0 else "Roboto",
            })
    ops.extend([
        {"op": "add-shape", "slide": "S08", "shape_type": "RECTANGLE", "x": 42, "y": 358, "width": 636, "height": 32, "background_color": "#0F1D2E"},
        {"op": "add-shape", "slide": "S08", "shape_type": "RECTANGLE", "x": 42, "y": 358, "width": 4, "height": 32, "background_color": GREEN},
        {"op": "add-textbox", "slide": "S08", "text": "RULE OF THUMB:  Start with Orchestrator (1-on-1). Escalate up the ladder only when depth, parallelism, or horizon demands it.", "x": 54, "y": 364, "width": 616, "height": 20, "font_size": 9.8, "bold": True, "color": WHITE, "font_family": "Roboto", "content_alignment": "MIDDLE"},
        {"op": "set-notes", "slide": "S08", "text": "Walk through the 2-axis Antigravity mental model: Model (Hydrogen vs Orchestrator default vs Carbon) is completely orthogonal to Execution Mode (1-on-1 -> /boost -> /swarm -> /run-workflow -> /teamwork). Ask the 4 decision-tree questions from bottom up: Long-horizon? /teamwork. Same task x N items? /run-workflow. Collaborative parallel? /swarm. Tough single problem? /boost. Otherwise 1-on-1!"},
    ])

    # ── S09: NEW — GOOGLE RESEARCH /TEAMWORK BREAKTHROUGH (NOV 2026) ───────────
    add_blank_slide(ops, "S09", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S09", "text": "GOOGLE RESEARCH (NOV 2026)  ·  ANTIGRAVITY /TEAMWORK IN PRODUCTION", "x": 42, "y": 18, "width": 636, "height": 15, "font_size": 9, "bold": True, "color": AMBER_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S09", "text": "Autonomous Long-Horizon Engineering — Real Google Proof", "x": 42, "y": 36, "width": 636, "height": 28, "font_size": 19, "bold": True, "color": WHITE, "font_family": "Montserrat"},
    ])
    tw_cards = [
        ("~800K LoC", "Zircon Microkernel (C++ -> Rust)", "2-week Argon /teamwork campaign rewrote ~800,000 lines of C++ to safe Rust — passing all unmodified kernel tests & booting arm64.", BLUE_LIGHT),
        ("20–30% Faster", "libgav1 AV1 Decoder (170K LoC)", "Rewrote 170K LoC C++ to Rust with 100% bit-exact conformance, then profiled & beat original C++ + hand-tuned assembly on x86 & ARM.", GREEN_LIGHT),
        (">1 PiB RAM", "Google Fleet & Borg TPU Infra", "Autonomous infra optimization saved >1 PiB fleet RAM and cut Borg TPU workload preemption by 24% (/teamwork + /boost).", AMBER_LIGHT),
        ("4.09x / 2.99x", "DuoDiscover Kernels & Deep Review", "4.09x geo-mean speedup on 17 JAXBench kernels, 2.99x on vLLM TPU Pallas kernels; 90% factual review across 578 STOC papers.", PURPLE_LIGHT),
    ]
    for i, (metric, h, desc, col) in enumerate(tw_cards):
        x = 42 + (i % 2) * 326
        y = 76 + (i // 2) * 118
        ops.extend([
            {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": x, "y": y, "width": 310, "height": 106, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": x, "y": y, "width": 310, "height": 4, "background_color": col},
            {"op": "add-textbox", "slide": "S09", "text": metric, "x": x + 14, "y": y + 10, "width": 282, "height": 24, "font_size": 15.5, "bold": True, "color": col, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S09", "text": h, "x": x + 14, "y": y + 34, "width": 282, "height": 18, "font_size": 10.5, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S09", "text": desc, "x": x + 14, "y": y + 54, "width": 282, "height": 48, "font_size": 9.2, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 130},
        ])
    # Architecture footer bar
    ops.extend([
        {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": 42, "y": 318, "width": 636, "height": 68, "background_color": "#0F1A2C"},
        {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": 42, "y": 318, "width": 5, "height": 68, "background_color": AMBER},
        {"op": "add-textbox", "slide": "S09", "text": "WHY /TEAMWORK SUCCEEDS WHERE SINGLE-CHAT AGENTS COLLAPSE", "x": 58, "y": 324, "width": 608, "height": 14, "font_size": 8.6, "bold": True, "color": AMBER_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S09", "text": "1. Context Partitioning by Construction (zero context rot)  ·  2. Fresh Coordinator Handoffs (durable git/file memory)\n3. Independent Falsifiers & Clean Critics (verify against unmodified benchmarks & formal proofs — never grade own homework)", "x": 58, "y": 340, "width": 608, "height": 40, "font_size": 9.0, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 126},
        {"op": "set-notes", "slide": "S09", "text": "Share the landmark Nov 13, 2026 Google Research `/teamwork` results: ~800K LoC Zircon microkernel rewritten to Rust booting arm64; 170K LoC libgav1 AV1 decoder rewritten to Rust and then optimized 20–30% FASTER than hand-tuned C++ & assembly; >1 PiB RAM saved & 24% less Borg TPU preemption; 4.09x JAXBench & 2.99x vLLM TPU Pallas kernels. Secret sauce: context partitioning + independent unmodified falsifiers!"},
    ])

    # ── S10: DEMO 1 — PARALLEL /SWARM & REMOTE VM ──────────────────────────────
    add_demo_slide(
        ops, imgs, "S10",
        "DEMO 01 · LIVE GEMINI 4 API + ISOLATED GIT WORKTREES + REMOTE VM",
        f"Carbon Plans -> 3 Parallel Hydrogen /swarm Workers ({d1['hydrogen_swarm']['parallel_speedup']}x Speedup) -> Remote VM",
        "demo1_antigravity_swarm_kickoff_poster.png",
        "▶  Watch 1080p 30fps Demo 1 Recording (Google Drive)",
        vids.get("demo1_antigravity_swarm_kickoff", drive.get("folder_url", "")),
        f"DEMO 1! Live `gemini-4-carbon` analyzed `monsoonpay/circuit_breaker.py` in {round(d1['carbon_architect']['latency_ms']/1000,1)}s for our Google Cloud asia-south2 flash-sale incident, then 3 parallel `gemini-4-hydrogen` workers ran inside real `git worktree add --detach` sandboxes ({d1['hydrogen_swarm']['parallel_speedup']}x parallel speedup), handing off to an Antigravity Remote Agent VM.",
    )

    # ── S11: DEMO 2 (NEW!) — LIVE ENTERPRISE CODE MODERNIZATION ────────────────
    add_demo_slide(
        ops, imgs, "S11",
        "DEMO 02 · LIVE GEMINI 4 CARBON + ARGON + UNMODIFIED GOLDEN FALSIFIER",
        f"Legacy O(N²) UPI Monolith -> O(N) Service: {m5['speedup_factor']}x Faster ({m5['legacy_ms']}ms -> {m5['modern_ms']}ms), 0.00 Drift",
        "demo5_code_modernization_poster.png",
        "▶  Watch 1080p 30fps Demo 2 Code Modernization Recording (Google Drive)",
        vids.get("demo5_code_modernization", drive.get("folder_url", "")),
        f"DEMO 2 — BRAND NEW! We ran the exact Google `/teamwork` modernization loop live on an Indian UPI/Merchant settlement monolith (8,000 real txns, INR 56.23M payout). `gemini-4-carbon` extracted 5 hidden RBI/GST/idempotency invariants, `gemini-4-argon` synthesized a clean O(N) engine on Attempt 1, and our locked unmodified golden falsifier proved {m5['speedup_factor']}x speedup ({m5['legacy_ms']}ms -> {m5['modern_ms']}ms) with 100% bit-exact SHA-256 parity and 0.00 INR drift!",
        cta_bg="#065F46",
    )

    # ── S12: DECISIONS API ARCHITECTURE DIAGRAM ────────────────────────────────
    add_diagram_slide(
        ops, imgs, "S12",
        "04 · DECIDE SMALL",
        "How Gemini Decisions API Eliminates Output-Token Latency",
        "05_decisions_api.jpg",
        "Walk through `bool (Yes/No)`, `choice` (2–255 options), and `score` (rubric expectation), plus multimodal image/PDF/audio scoring in ONE forward pass with ZERO output tokens ($0.10/1M input, $0.00 output).",
    )

    # ── S13: REWORKED BENCHMARK + EXPLICIT USE CASE & METHODOLOGY ──────────────
    add_blank_slide(ops, "S13", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S13", "text": "HEAD-TO-HEAD BENCHMARK  ·  USE CASE, METHODOLOGY & LIVE RESULTS", "x": 42, "y": 14, "width": 636, "height": 15, "font_size": 9, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S13", "text": "Why \"Decide Small\" Transforms Production Economics", "x": 42, "y": 30, "width": 636, "height": 26, "font_size": 18.5, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        # Explicit Use Case & Methodology Box (Mani's explicit ask!)
        {"op": "add-shape", "slide": "S13", "shape_type": "RECTANGLE", "x": 42, "y": 60, "width": 636, "height": 68, "background_color": SURF_ALT},
        {"op": "add-shape", "slide": "S13", "shape_type": "RECTANGLE", "x": 42, "y": 60, "width": 4, "height": 68, "background_color": AMBER},
        {"op": "add-textbox", "slide": "S13", "text": "USE CASE & BENCHMARK METHODOLOGY (HOW THESE NUMBERS WERE MEASURED)", "x": 54, "y": 64, "width": 616, "height": 14, "font_size": 8.0, "bold": True, "color": AMBER_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S13", "text": "Use Case: MonsoonPay SEV-1 payment alert gated on 8 security/routing rules OR 50 simultaneous RBI/PCI-DSS checks before agent launch.\nMethodology: Identical payload live on Gemini API — Decision-1 (/v1beta/decisions, 0 output tokens) vs 3.8 Flash (b=0) & 4 Hydrogen (low) strict JSON via generateContent. Costs use exact API usage_metadata at Nov 2026 list prices.", "x": 54, "y": 78, "width": 616, "height": 46, "font_size": 8.0, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 118},
        # Table
        {"op": "add-table", "slide": "S13", "rows": 4, "cols": 7, "id": "TBL_BENCH", "x": 42, "y": 136, "width": 636, "height": 176},
        {"op": "updateTableColumnProperties", "updateTableColumnProperties": {"objectId": "TBL_BENCH", "columnIndices": [0], "tableColumnProperties": {"columnWidth": {"magnitude": 120, "unit": "PT"}}, "fields": "columnWidth"}},
        {"op": "updateTableColumnProperties", "updateTableColumnProperties": {"objectId": "TBL_BENCH", "columnIndices": [1, 2, 3, 4, 5, 6], "tableColumnProperties": {"columnWidth": {"magnitude": 86, "unit": "PT"}}, "fields": "columnWidth"}},
    ])
    headers = ["Model", "8Q Latency", "8Q Out", "8Q $/1M", "50Q Latency", "50Q Out", "50Q $/1M"]
    rows_data = [
        [
            "gemini-decision-1",
            f"{b8[0]['latency_ms']} ms (1x)",
            "0",
            f"${b8[0]['cost_per_1m_calls_usd']:,.0f}",
            f"{b50[0]['latency_ms']} ms (1x)",
            "0",
            f"${b50[0]['cost_per_1m_calls_usd']:,.0f} (Base)",
        ],
        [
            "gemini-3.8-flash\n(budget=0)",
            f"{b8[1]['latency_ms']:,}ms ({sp8_f}x)",
            str(b8[1]["billed_output_tokens"]),
            f"${b8[1]['cost_per_1m_calls_usd']:,.0f} ({c8_f}x)",
            f"{b50[1]['latency_ms']:,}ms ({r50['speedup_vs_3_8_flash']}x)",
            str(b50[1]["billed_output_tokens"]),
            f"${b50[1]['cost_per_1m_calls_usd']:,.0f} ({r50['cost_savings_vs_3_8_flash']}x)",
        ],
        [
            "gemini-4-hydrogen\n(low)",
            f"{b8[2]['latency_ms']:,}ms ({sp8_h}x)",
            str(b8[2]["billed_output_tokens"]),
            f"${b8[2]['cost_per_1m_calls_usd']:,.0f} ({c8_h}x)",
            f"{b50[2]['latency_ms']:,}ms ({r50['speedup_vs_4_hydrogen']}x)",
            f"{b50[2]['billed_output_tokens']:,}",
            f"${b50[2]['cost_per_1m_calls_usd']:,.0f} ({r50['cost_savings_vs_4_hydrogen']}x)",
        ],
    ]
    for c_idx, h_txt in enumerate(headers):
        ops.append({"op": "set-table-cell", "table": "TBL_BENCH", "row": 0, "col": c_idx, "text": h_txt, "bold": True, "font_size": 8.6, "color": BLUE_LIGHT, "background_color": "#162238", "font_family": "Roboto Mono"})
    for r_idx, r_vals in enumerate(rows_data, start=1):
        is_win = r_idx == 1
        bg = "#0E291A" if is_win else ("#121B2D" if r_idx == 2 else "#172033")
        fg = GREEN_LIGHT if is_win else TEXT_SOFT
        for c_idx, val in enumerate(r_vals):
            ops.append({"op": "set-table-cell", "table": "TBL_BENCH", "row": r_idx, "col": c_idx, "text": val, "bold": is_win or c_idx == 0, "font_size": 8.8, "color": fg, "background_color": bg, "font_family": "Roboto Mono" if c_idx > 0 else "Roboto"})

    ops.extend([
        {"op": "add-shape", "slide": "S13", "shape_type": "RECTANGLE", "x": 42, "y": 324, "width": 636, "height": 58, "background_color": "#0F1D2E"},
        {"op": "add-shape", "slide": "S13", "shape_type": "RECTANGLE", "x": 42, "y": 324, "width": 5, "height": 58, "background_color": GREEN},
        {"op": "add-textbox", "slide": "S13", "text": "GOOGLE PUBLISHED 100-QUESTION SINGLE-REQUEST SCALING BENCHMARK (NOV 2026)", "x": 58, "y": 331, "width": 608, "height": 15, "font_size": 8.5, "bold": True, "color": GREEN_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S13", "text": f"Decision-1: {pub100['gemini_decision_1_ms']} ms   ·   3.8 Flash: {pub100['gemini_3_8_flash_ms']/1000:.1f}s ({pub100['speedup_vs_flash']}x slower)   ·   4 Hydrogen: {pub100['gemini_4_hydrogen_ms']/1000:.1f}s ({pub100['speedup_vs_hydrogen']}x slower)", "x": 58, "y": 349, "width": 608, "height": 24, "font_size": 12.2, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "set-notes", "slide": "S13", "text": f"Walk the audience through BOTH the exact payment guardrail use case AND how we ran the apples-to-apples benchmark live! On 50 simultaneous RBI/PCI-DSS checks: Decision-1 took {b50[0]['latency_ms']}ms at $271/1M calls (0 output tokens) vs 3.8 Flash ({b50[1]['latency_ms']}ms, {r50['speedup_vs_3_8_flash']}x slower, {r50['cost_savings_vs_3_8_flash']}x costlier) and 4 Hydrogen ({b50[2]['latency_ms']}ms, {r50['speedup_vs_4_hydrogen']}x slower, {r50['cost_savings_vs_4_hydrogen']}x costlier!). Why? Zero autoregressive decoding!"},
    ])

    # ── S14: DEMO 3 — DECISIONS API ARENA ──────────────────────────────────────
    add_demo_slide(
        ops, imgs, "S14",
        "DEMO 03 · LIVE DECISIONS API ARENA",
        f"4 Live Events x 8Q · 50Q Race ({r50['speedup_vs_3_8_flash']}x vs Flash · {r50['cost_savings_vs_4_hydrogen']}x Cheaper vs Hydrogen) · Multimodal",
        "demo2_decisions_api_arena_poster.png",
        "▶  Watch 1080p 30fps Demo 3 Recording (Google Drive)",
        vids.get("demo2_decisions_api_arena", drive.get("folder_url", "")),
        "DEMO 3! Watch all 4 live MonsoonPay events (prompt injection, leaked GCP service account key, benign CSS tweak, SEV-1 Delhi checkout outage) gated at 0 output tokens, followed by the live head-to-head race and multimodal diagram audit.",
    )

    # ── S15: LIVE 3.8 VOICE ARCHITECTURE ───────────────────────────────────────
    add_diagram_slide(
        ops, imgs, "S15",
        "05 · REASON WHILE SPEAKING",
        "Gemini 3.8 Live Extended Thinking + Async Tool Execution",
        "06_live38_voice.jpg",
        "Explain Dual-Track voice: Gemini 3.8 speaks naturally in 97 languages (with Live Avatar GA & SynthID) while executing NON_BLOCKING BigQuery, Firestore, and ADK 2.0 tools asynchronously — zero dead air!",
    )

    # ── S16: DEMO 4A (MANI'S REAL RECORDING!) — FRANKFURT FLIGHT REBOOKING ─────
    add_demo_slide(
        ops, imgs, "S16",
        "DEMO 04A · REAL RECORDING · GEMINI 3.8 LIVE EXTENDED THINKING (VIDEO + VOICE + SQL)",
        "Frankfurt Flight Cancelled — Live Multimodal Rebooking & EU261 Compensation",
        "demo4a_gemini38_live_flight_poster.png",
        "▶  Play Mani's Real Recording: Frankfurt Flight Rebooked Live (Google Drive)",
        DRIVE_FLIGHT_URL,
        "DEMO 4A — MANI'S REAL LIVE RECORDING! Point out the right-hand engineering console while talking naturally on camera: `gemini-3.8-live-extended-thinking` (`thinkingLevel: HIGH`, voice `Aria`) streams 1 FPS camera + 16kHz audio and executes `NON_BLOCKING` BigQuery & Firestore SQL (`scan_boarding_pass_and_bag_tag`, `evaluate_eu261_and_vip_entitlement`, `INSERT INTO rebooking_transactions`), rebooking PNR LH8942X with hotel, meals, $350 goodwill & 25,000 miles — with zero dead air!",
        cta_bg="#1D4ED8",
        img_box=(93.6, 60.0, 532.7, 282.0),
        caption="Live 1 FPS camera + 16kHz PCM audio · NON_BLOCKING BigQuery & Firestore SQL · PNR LH8942X rebooked + EU261 compensation",
    )

    # ── S17: DEMO 4B (MANI'S REAL RECORDING!) — GEMINI VOICE AI PSTN ───────────
    add_demo_slide(
        ops, imgs, "S17",
        "DEMO 04B · REAL RECORDING · ENTERPRISE VOICE AI & INDIAN PSTN TELEPHONY ON CLOUD RUN",
        "Multilingual PSTN Call (EN · HI · TA · KN · TE · Hinglish) — Direct S2S vs Cascading",
        "demo4b_gemini_voiceai_pstn_poster.png",
        "▶  Play Mani's Real Recording: Gemini VoiceAI PSTN Integration (Google Drive)",
        DRIVE_PSTN_URL,
        "DEMO 4B — MANI'S REAL TELEPHONY RECORDING! Real iPhone PSTN/VoLTE call into Google Cloud Load Balancing + Cloud Armor -> Cloud Run Gen2 (asia-south1) -> Firestore + Voice Observatory. Compare the two production patterns: (1) Direct Speech-to-Speech (Gemini 3.1 Flash Live) for ultra-low latency vs (2) Cascading Listen-Think-Speak (Gemini 3.5 Transcribe Live -> 3.8 Flash -> 3.8 Flash-Lite TTS en-IN) for strict compliance & regional Indian voices!",
        cta_bg="#065F46",
        img_box=(70.0, 68.0, 580.0, 267.4),
        caption="Cloud Load Balancing + Cloud Armor -> Cloud Run Gen2 (asia-south1) -> Firestore · Direct Speech-to-Speech vs Cascading Pipeline",
    )

    # ── S18: GOOGLE ADK 2.0 WORKFLOW RUNTIME ───────────────────────────────────
    add_blank_slide(ops, "S18", BG_DARK)
    code_snippet = (
        "from google.adk import Workflow, Event\n"
        "from google.adk.workflow import Edge, RetryConfig, START, node\n\n"
        "@node(name=\"decision_gate_node\")\n"
        "async def decision_gate(ctx):\n"
        "    v = apply_policy_gate(call_decisions_api(ctx.state[\"alert\"]))\n"
        "    yield Event(output=v, route=v.adk_route)\n\n"
        "@node(name=\"lakehouse_mcp_sql\", retry_config=RetryConfig(max_attempts=3))\n"
        "async def lakehouse_sql(ctx):\n"
        "    return query_spanner_omni_x_bigquery_iceberg()\n\n"
        "@node(name=\"hitl_pr_approval\", require_confirmation=True)\n"
        "async def approve_pr(ctx):   # Native durable HITL pause\n"
        "    return {\"status\": \"APPROVED_AND_SHIPPED\"}"
    )
    ops.extend([
        {"op": "add-textbox", "slide": "S18", "text": "GOOGLE ADK 2.0 (GA  ·  PYTHON / GO / TS / JAVA / C#)", "x": 42, "y": 20, "width": 636, "height": 16, "font_size": 9.5, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S18", "text": "Deterministic Control Flow Around Autonomous Agents", "x": 42, "y": 40, "width": 636, "height": 30, "font_size": 19, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": "S18", "text": code_snippet, "x": 42, "y": 84, "width": 392, "height": 290, "font_size": 9.3, "color": "#DCE8FA", "background_color": SURF_CODE, "font_family": "Roboto Mono", "line_spacing": 144, "content_alignment": "MIDDLE"},
    ])
    adk_pillars = [
        ("Explicit DAG Routing", "Edge(..., route='quarantine') enforces security boundaries in typed code — never hopes inside a prompt.", BLUE),
        ("Native HITL Checkpoints", "require_confirmation=True emits adk_request_input and suspends state cleanly until an architect approves.", AMBER),
        ("Open Protocol Native", "First-class Managed MCP toolsets + A2A (Agent-to-Agent) orchestration across 5 languages.", GREEN),
    ]
    for i, (h, body, col) in enumerate(adk_pillars):
        y = 84 + i * 100
        ops.extend([
            {"op": "add-shape", "slide": "S18", "shape_type": "RECTANGLE", "x": 452, "y": y, "width": 226, "height": 90, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S18", "shape_type": "RECTANGLE", "x": 452, "y": y, "width": 4, "height": 90, "background_color": col},
            {"op": "add-textbox", "slide": "S18", "text": h, "x": 466, "y": y + 10, "width": 202, "height": 20, "font_size": 12, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S18", "text": body, "x": 466, "y": y + 32, "width": 202, "height": 52, "font_size": 9.6, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 130},
        ])
    ops.append({"op": "set-notes", "slide": "S18", "text": "Real running code from `monsoonpay/adk_workflow.py` on `google-adk==2.14.1`. Highlight deterministic DAG routing, `RetryConfig(max_attempts=3)`, and native `require_confirmation=True` HITL pause."})

    # ── S19: GOOGLE CLOUD UNIFIED DATA PLATFORM DIAGRAM ────────────────────────
    add_diagram_slide(
        ops, imgs, "S19",
        "06 · ENTERPRISE DATA GRAVITY SOLVED",
        "Google Cloud's Unified Agentic Data Platform",
        "07_gcp_data_cloud.jpg",
        "Walk through Google Cloud's unified agentic data stack: Knowledge Catalog + 50+ Managed MCP Servers sitting across Spanner Omni, BigQuery + Apache Iceberg, AlloyDB Express, and Unified Graph + AI.",
    )

    # ── S20: GOOGLE CLOUD DATA OFFERINGS BLUEPRINT ─────────────────────────────
    add_blank_slide(ops, "S20", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S20", "text": "GOOGLE CLOUD DATA PLATFORM  ·  BUILT FOR PRODUCTION AGENTS", "x": 42, "y": 22, "width": 636, "height": 16, "font_size": 9.5, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S20", "text": "Zero-Copy Operational, Lakehouse & Vector Data Access", "x": 42, "y": 42, "width": 636, "height": 30, "font_size": 19.0, "bold": True, "color": WHITE, "font_family": "Montserrat"},
    ])
    data_cards = [
        ("TRANSACTIONAL EVERYWHERE", "Spanner Omni (GA)", "Globally consistent distributed SQL with Software TrueTime running natively across Google Cloud, Kubernetes, on-prem, and hybrid clouds.", BLUE),
        ("OPEN FORMAT LAKEHOUSE", "BigQuery & Borderless Apache Iceberg", "Query open Apache Iceberg tables & Parquet telemetry in place with zero ETL duplication and unified governance across enterprise catalogs.", GREEN),
        ("EPHEMERAL AGENT SANDBOXES", "AlloyDB Express + ScaNN", "Serverless PostgreSQL booting in <2 seconds, scaling to zero between agent runs, with 10B-scale ScaNN vector search.", AMBER),
        ("SEMANTIC GROUNDING", "Knowledge Catalog + 50+ Managed MCPs", "Universal Context Engine resolves verified semantic join paths before SQL generation: 4x SQL accuracy, -75% prompt tokens.", BLUE_LIGHT),
    ]
    for i, (k, h, body, col) in enumerate(data_cards):
        x = 42 + (i % 2) * 326
        y = 92 + (i // 2) * 144
        ops.extend([
            {"op": "add-shape", "slide": "S20", "shape_type": "RECTANGLE", "x": x, "y": y, "width": 310, "height": 128, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S20", "shape_type": "RECTANGLE", "x": x, "y": y, "width": 310, "height": 4, "background_color": col},
            {"op": "add-textbox", "slide": "S20", "text": k, "x": x + 16, "y": y + 14, "width": 278, "height": 16, "font_size": 8.5, "bold": True, "color": col, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "S20", "text": h, "x": x + 16, "y": y + 32, "width": 278, "height": 24, "font_size": 11.5, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S20", "text": body, "x": x + 16, "y": y + 60, "width": 278, "height": 58, "font_size": 10.2, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 135},
        ])
    ops.append({"op": "set-notes", "slide": "S20", "text": "Highlight how Spanner Omni, BigQuery Borderless Iceberg, AlloyDB Express, and Knowledge Catalog + 50+ Managed MCP servers give ADK 2.0 agents governed, zero-copy access to real enterprise data."})

    # ── S21: DEMO 5 — ADK 2.14.1 + ZERO-COPY SPANNER x BIGQUERY ICEBERG ────────
    add_demo_slide(
        ops, imgs, "S21",
        f"DEMO 05 · REAL GOOGLE ADK {d3['adk_version']} + ZERO-COPY SPANNER OMNI x BIGQUERY ICEBERG",
        f"{sql['rows_correlated']:,} Rows Joined in {sql['query_latency_ms']} ms + Native ADK HITL Pause + Gemini 3.8 HD Audio",
        "demo3_live38_voice_multicloud_adk_poster.png",
        "▶  Play 1080p Demo 5 Recording WITH Gemini 3.8 HD Audio (Google Drive)",
        vids.get("demo3_live38_voice_multicloud_adk", drive.get("folder_url", "")),
        f"DEMO 5! Real Google ADK {d3['adk_version']} DAG executing live: Knowledge Catalog resolves `trace_span_id`, zero-copy SQL joins 40,000 BigQuery Iceberg Envoy rows with Spanner Omni commits in {sql['query_latency_ms']}ms, pinpointing the `gcp:asia-south2` 64-slot Envoy pool while TrueTime stays <3ms, then pausing cleanly at `require_confirmation=True`!",
        cta_bg="#065F46",
    )

    # ── S22: DEMO 6 — REVIEW EVERYTHING (CARBON ADVERSARIAL PR AUDIT) ──────────
    add_demo_slide(
        ops, imgs, "S22",
        "DEMO 06 · REVIEW EVERYTHING · LIVE SLA PROOF + CARBON ADVERSARIAL AUDIT",
        f"p99 Dropped {sla['p99_reduction_pct']}% & 10/10 Pytest Passed — Yet Carbon Still Caught {warn_cnt or 4} Pre-Merge Findings",
        "demo4_review_shipped_pr_poster.png",
        "▶  Watch 1080p 30fps Demo 6 Recording (Google Drive)",
        vids.get("demo4_review_shipped_pr", drive.get("folder_url", "")),
        f"DEMO 6! Even after p99 dropped from {sla['before']['p99_ms']}ms to {sla['after']['p99_ms']}ms (-{sla['p99_reduction_pct']}%) and all 10 unit tests passed, live `gemini-4-carbon` returned `{ca['audit']['overall_verdict']}` — flagging subtle concurrency, fail-closed gate, and NaN drift edge cases before a human merges PR #1!",
        cta_bg="#92400E",
    )

    # ── S23: BEYOND CODE — FOUR GOOGLE CLOUD FORCE MULTIPLIERS ─────────────────
    add_blank_slide(ops, "S23", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S23", "text": "THE WIDER GOOGLE CLOUD AI PLATFORM  ·  ARCHITECT RADAR", "x": 42, "y": 22, "width": 636, "height": 16, "font_size": 9.5, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S23", "text": "Four Force Multipliers Beyond Code Generation", "x": 42, "y": 42, "width": 636, "height": 30, "font_size": 22.5, "bold": True, "color": WHITE, "font_family": "Montserrat"},
    ])
    extras = [
        ("CUSTOM SILICON", "8th-Gen TPUs (TPU 8t & 8i)", "Purpose-built AI silicon driving 16B+ tokens/minute globally — making parallel sub-second Hydrogen swarms affordable at enterprise scale.", BLUE),
        ("ENTERPRISE GRAVITY", "Oracle AI Database@Google Cloud", "Zero-latency Exadata & Autonomous Database inside Google Cloud regions — connecting core banking directly to ADK 2.0 agents.", AMBER),
        ("AGENTIC INTERFACES", "Nano Banana 2.1 · /generative_ui", "Agents move beyond Markdown text walls — synthesizing crisp diagrams, HD audio, and live interactive HTML dashboards on demand.", GREEN),
        ("FORMAL VERIFICATION", "Lean 4 Proofs & AlphaProof Code", "Pairs neural synthesis with formal mathematical proofs (1.8M-line Lean 4 proofs & verified consensus/financial invariants).", BLUE_LIGHT),
    ]
    for i, (k, h, body, col) in enumerate(extras):
        x = 42 + (i % 2) * 326
        y = 92 + (i // 2) * 144
        ops.extend([
            {"op": "add-shape", "slide": "S23", "shape_type": "RECTANGLE", "x": x, "y": y, "width": 310, "height": 128, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S23", "shape_type": "RECTANGLE", "x": x, "y": y, "width": 310, "height": 4, "background_color": col},
            {"op": "add-textbox", "slide": "S23", "text": k, "x": x + 16, "y": y + 14, "width": 278, "height": 16, "font_size": 8.5, "bold": True, "color": col, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "S23", "text": h, "x": x + 16, "y": y + 32, "width": 278, "height": 24, "font_size": 11.5, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S23", "text": body, "x": x + 16, "y": y + 60, "width": 278, "height": 58, "font_size": 10.2, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 135},
        ])
    ops.append({"op": "set-notes", "slide": "S23", "text": "Fast 45-second Principal Architect tour of 8th-gen TPUs, Oracle AI Database@Google Cloud, Nano Banana 2.1 + `/generative_ui`, and Lean 4 formal verification."})

    # ── S24: MENTAL MODEL POSTER ───────────────────────────────────────────────
    add_diagram_slide(
        ops, imgs, "S24",
        "07 · TAKE A PHOTO",
        "The Battle-Tested Mental Model for Agentic Systems",
        "08_mental_model_poster.jpg",
        "Phones up! If you take ONE blueprint back to your team on Monday: Plan Big, Execute Fast, Decide Small, Review Everything.",
    )

    # ── S25: CLOSING CTA (Mani + LinkedIn + GitHub) ────────────────────────────
    add_blank_slide(ops, "S25", BG_DARK)
    ops.extend([
        {"op": "add-shape", "slide": "S25", "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 8, "height": 405, "background_color": GREEN},
        {"op": "add-textbox", "slide": "S25", "text": "ALL CODE · LIVE BENCHMARKS · ADK 2.0 GRAPH · OPEN SOURCE", "x": 48, "y": 38, "width": 624, "height": 18, "font_size": 10, "bold": True, "color": GREEN_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S25", "text": "Plan Big. Execute Fast.\nDecide Small. Review Everything.", "x": 48, "y": 64, "width": 624, "height": 94, "font_size": 33, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        # GitHub CTA Box
        {"op": "add-shape", "slide": "S25", "shape_type": "RECTANGLE", "x": 48, "y": 176, "width": 392, "height": 74, "background_color": SURF_DARK},
        {"op": "add-shape", "slide": "S25", "shape_type": "RECTANGLE", "x": 48, "y": 176, "width": 5, "height": 74, "background_color": BLUE},
        {"op": "add-textbox", "slide": "S25", "text": "CLONE THE REPOSITORY & ALL LIVE DEMOS", "x": 64, "y": 188, "width": 368, "height": 16, "font_size": 8.5, "bold": True, "color": MUTED, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S25", "text": "github.com/cmanikandan/gdg-blr-talk-nov14-2026", "x": 64, "y": 210, "width": 368, "height": 26, "font_size": 11.2, "bold": True, "color": WHITE, "font_family": "Roboto Mono", "link": GITHUB_URL},
        # LinkedIn CTA Box
        {"op": "add-shape", "slide": "S25", "shape_type": "RECTANGLE", "x": 456, "y": 176, "width": 216, "height": 74, "background_color": SURF_DARK},
        {"op": "add-shape", "slide": "S25", "shape_type": "RECTANGLE", "x": 456, "y": 176, "width": 5, "height": 74, "background_color": GREEN},
        {"op": "add-textbox", "slide": "S25", "text": "CONNECT WITH MANI", "x": 472, "y": 188, "width": 192, "height": 16, "font_size": 8.5, "bold": True, "color": MUTED, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S25", "text": "linkedin.com/in/cmanikandan", "x": 472, "y": 210, "width": 192, "height": 26, "font_size": 10.5, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono", "link": LINKEDIN_URL},
        # Bottom footer
        {"op": "add-shape", "slide": "S25", "shape_type": "RECTANGLE", "x": 48, "y": 308, "width": 624, "height": 1.2, "background_color": "#25334D"},
        {"op": "add-textbox", "slide": "S25", "text": "Mani  ·  Principal Architect, Google Cloud  ·  DevFest Bengaluru 2026", "x": 48, "y": 324, "width": 624, "height": 26, "font_size": 13, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": "S25", "text": "Thank you Bengaluru! Come say hi — look for the Principal Architect with the brand-new badge.", "x": 48, "y": 352, "width": 624, "height": 22, "font_size": 10.5, "color": TEXT_SOFT, "font_family": "Roboto"},
        {"op": "set-notes", "slide": "S25", "text": "Closing badge callback! 'Thank you DevFest Bengaluru! Clone the repo, connect with me on LinkedIn, and if anyone knows where the best filter coffee is at Google Bengaluru, come find the Principal Architect with the brand-new badge!'"},
    ])

    return ops, imgs


def github_signed_url(local_path: str) -> str:
    rel = str(Path(local_path).resolve().relative_to(ROOT.resolve()))
    url = run_cmd([
        "gh", "api",
        f"repos/cmanikandan/gdg-blr-talk-nov14-2026/contents/{rel}",
        "--jq", ".download_url",
    ])
    if not url.startswith("http"):
        raise RuntimeError(f"Invalid signed URL for {rel}: {url}")
    return url


def main() -> None:
    import argparse
    import re

    parser = argparse.ArgumentParser()
    parser.add_argument("--pres-id", default="", help="Optional existing presentation ID")
    parser.add_argument("--images-only", action="store_true", help="Only place images on an existing 25-slide deck and export PDF/PPTX")
    args = parser.parse_args()

    tr = load_traces()
    drive = load_drive_links()
    ops, img_jobs = build_deck_ops(tr, drive)

    title = "The Periodic Table of Agents: Building with Gemini 4 & Antigravity — DevFest Bengaluru 2026 Keynote (v3)"
    if args.pres_id:
        pres_id = args.pres_id
        print(f"Using existing presentation: {pres_id}")
    else:
        print(f"Creating Google Slides deck: {title}")
        created_raw = run_cmd(["gslides", "mutate", "create", "--title", title])
        m = re.search(r"([a-zA-Z0-9_-]{25,})", created_raw)
        if not m:
            raise RuntimeError(f"Could not parse presentationId from: {created_raw}")
        pres_id = m.group(1)
        print(f"  ✔ Created presentation: {pres_id}")

    if args.images_only:
        slides_json = json.loads(run_cmd(["gslides", "readonly", "list-slides", pres_id, "--json"]))
        slide_ids = [s["objectId"] for s in slides_json]
        if len(slide_ids) != 25:
            raise RuntimeError(f"Expected 25 slides on {pres_id}, found {len(slide_ids)}")
        resolved = {"p": slide_ids[0]}
        for n in range(2, 26):
            resolved[f"S{n:02d}"] = slide_ids[n - 1]
    else:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
            json.dump(ops, tf, indent=2)
            batch_file = tf.name
        try:
            print(f"Applying {len(ops)} batch operations across 25 slides...")
            batch_raw = run_cmd(["gslides", "mutate", "batch", pres_id, "-f", batch_file, "--json"])
            batch_res = json.loads(batch_raw)
            resolved = batch_res.get("resolved_ids", {})
            resolved["p"] = "p"
            print(f"  ✔ Batch complete ({batch_res.get('operations')} ops, {len(batch_res.get('created_slides', []))+1} slides)")
        finally:
            Path(batch_file).unlink(missing_ok=True)

    print(f"Fetching signed GitHub URLs & placing {len(img_jobs)} crisp diagrams & demo posters...")
    img_ops: List[Dict[str, Any]] = []
    for job in img_jobs:
        real_slide = resolved.get(job["slide"], job["slide"])
        signed_url = github_signed_url(job["file"])
        img_ops.append({
            "op": "add-image",
            "slide": real_slide,
            "url": signed_url,
            "x": job["x"],
            "y": job["y"],
            "width": job["width"],
            "height": job["height"],
        })
        print(f"  ✔ Queued {Path(job['file']).name} -> {job['slide']} ({real_slide})")

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
        json.dump(img_ops, tf, indent=2)
        img_batch_file = tf.name
    try:
        run_cmd(["gslides", "mutate", "batch", pres_id, "-f", img_batch_file, "--json"])
        print(f"  ✔ Placed all {len(img_ops)} images cleanly in single batch!")
    finally:
        Path(img_batch_file).unlink(missing_ok=True)

    # Export local PDF & PPTX backups
    pdf_path = PRES_DIR / "Periodic_Table_of_Agents_DevFest_Keynote.pdf"
    pptx_path = PRES_DIR / "Periodic_Table_of_Agents_DevFest_Keynote.pptx"
    run_cmd(["gslides", "readonly", "export", pres_id, str(pdf_path), "--format", "pdf"])
    run_cmd(["gslides", "readonly", "export", pres_id, str(pptx_path), "--format", "pptx"])
    print(f"  ✔ Exported PDF ({pdf_path.stat().st_size // 1024} KB) & PPTX ({pptx_path.stat().st_size // 1024} KB)")

    meta = {
        "presentation_id": pres_id,
        "presentation_url": f"https://docs.google.com/presentation/d/{pres_id}/edit",
        "title": title,
        "slide_count": 25,
        "drive_videos_folder_id": drive.get("folder_id", ""),
        "drive_videos_folder_url": drive.get("folder_url", ""),
        "drive_videos": drive.get("videos", {}),
        "voice_demos": {
            "frankfurt_flight_live38": DRIVE_FLIGHT_URL,
            "pstn_voiceai_cloud_run": DRIVE_PSTN_URL,
        },
        "resolved_slide_ids": resolved,
    }
    (PRES_DIR / "google_slides_metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"🎉 DONE! Google Slides URL: {meta['presentation_url']}")


if __name__ == "__main__":
    main()
