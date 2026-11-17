#!/usr/bin/env python3
"""
Builds the Brand-New, Principal-Architect-Grade 22-Slide Google Slides Keynote via `gslides`.

Design System (720pt x 405pt 16:9 Widescreen):
  - Alternating Deep Obsidian (#0B101B) Editorial Slides & Warm Cream (#FAF7F0) Full-Stage Head First Infographics
  - Exact 16:9 aspect-ratio placement for all 8 Head First infographics & 4 1080p Demo poster frames (zero stretching!)
  - ZERO redundant bullet boxes next to infographics, ZERO emoji spam, ZERO audience-visible pacing timestamps
  - All benchmark stats loaded dynamically from live `demos/traces/demo{1..4}_trace.json`
  - Full private Speaker Notes on every single slide
  - Exports local PDF & PPTX backups for visual verification and offline safety
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path("/home/antigravity/cmanikandan/gdg-blr-talk-nov14-2026")
INFO_DIR = ROOT / "assets" / "infographics"
VID_DIR = ROOT / "assets" / "videos"
TRACES_DIR = ROOT / "demos" / "traces"
PRES_DIR = ROOT / "presentation"
DRIVE_META_PATH = PRES_DIR / "drive_videos_v2.json"

BG_DARK = "#0B101B"
SURF_DARK = "#131C2E"
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
        ]
    }


def load_drive_links() -> Dict[str, Any]:
    if DRIVE_META_PATH.exists():
        return json.loads(DRIVE_META_PATH.read_text(encoding="utf-8"))
    return {
        "folder_id": "17FSevMIs-B9Th0A3XHudNABUKQlHSgpY",
        "folder_url": "https://drive.google.com/drive/folders/17FSevMIs-B9Th0A3XHudNABUKQlHSgpY",
        "videos": {},
    }


def add_blank_slide(ops: List[Dict[str, Any]], slide_id: str, bg: str, is_first: bool = False) -> None:
    if is_first:
        ops.append({"op": "delete-element", "element": "i0"})
        ops.append({"op": "delete-element", "element": "i1"})
    else:
        ops.append({"op": "add-slide", "layout": "BLANK", "id": slide_id})
    ops.append({"op": "set-background", "slide": slide_id, "color": bg})


def add_head_first_slide(
    ops: List[Dict[str, Any]],
    img_jobs: List[Dict[str, Any]],
    slide_id: str,
    kicker: str,
    title: str,
    img_filename: str,
    notes: str,
) -> None:
    """Full-stage 16:9 O'Reilly Head First infographic on warm cream with zero clutter."""
    add_blank_slide(ops, slide_id, BG_CREAM)
    ops.extend([
        {"op": "add-textbox", "slide": slide_id, "text": kicker, "x": 36, "y": 11, "width": 648, "height": 16, "font_size": 9, "bold": True, "color": "#1D4ED8", "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": slide_id, "text": title, "x": 36, "y": 25, "width": 648, "height": 26, "font_size": 17, "bold": True, "color": INK_CREAM, "font_family": "Montserrat"},
        {"op": "add-shape", "slide": slide_id, "shape_type": "RECTANGLE", "x": 36, "y": 54, "width": 648, "height": 1.2, "background_color": "#D6CFC2"},
        {"op": "set-notes", "slide": slide_id, "text": notes},
    ])
    # Exact 16:9 ratio: 584pt x 328.5pt centered on 720pt width
    img_jobs.append({
        "slide": slide_id,
        "file": str(INFO_DIR / img_filename),
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
) -> None:
    add_blank_slide(ops, slide_id, BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": slide_id, "text": kicker, "x": 38, "y": 14, "width": 644, "height": 16, "font_size": 9, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": slide_id, "text": title, "x": 38, "y": 30, "width": 644, "height": 28, "font_size": 14, "bold": True, "color": WHITE, "font_family": "Montserrat"},
    ])
    # Exact 16:9 ratio: 534pt x 300.4pt centered at x=93
    img_jobs.append({
        "slide": slide_id,
        "file": str(VID_DIR / poster_filename),
        "x": 93,
        "y": 64,
        "width": 534,
        "height": 300.4,
    })
    cta_box: Dict[str, Any] = {
        "op": "add-textbox",
        "slide": slide_id,
        "text": cta_label,
        "x": 93,
        "y": 370,
        "width": 534,
        "height": 24,
        "font_size": 10.5,
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
    d1, d2, d3, d4 = tr["d1"], tr["d2"], tr["d3"], tr["d4"]
    b8 = d2["round_b_head_to_head"]["benchmark_8q"]
    b50 = d2["round_b_head_to_head"]["benchmark_50q"]
    pub100 = d2["round_b_head_to_head"]["published_100q_reference"]
    r50 = d2["round_b_head_to_head"]["live_ratios_50q"]
    sp8_f = round(b8[1]["latency_ms"] / max(b8[0]["latency_ms"], 1), 1)
    sp8_h = round(b8[2]["latency_ms"] / max(b8[0]["latency_ms"], 1), 1)
    c8_h = round(b8[2]["cost_per_1m_calls_usd"] / max(b8[0]["cost_per_1m_calls_usd"], 0.01), 1)
    sla = d4["sla_benchmark"]
    sql = d3["multicloud_finding"]
    ca = d4["carbon_security_audit"]
    vids = drive.get("videos", {})

    ops: List[Dict[str, Any]] = []
    imgs: List[Dict[str, Any]] = []

    # ── SLIDE 01: HERO TITLE (`p`) ─────────────────────────────────────────────
    add_blank_slide(ops, "p", BG_DARK, is_first=True)
    ops.extend([
        {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 8, "height": 405, "background_color": BLUE},
        {"op": "add-textbox", "slide": "p", "text": "DEVFEST BENGALURU 2026  ·  OPENING KEYNOTE", "x": 46, "y": 38, "width": 620, "height": 20, "font_size": 10, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "p", "text": "The Periodic Table of Agents", "x": 46, "y": 64, "width": 630, "height": 58, "font_size": 38, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": "p", "text": "Building Production Agentic Systems with Gemini 4 & Google Antigravity", "x": 46, "y": 124, "width": 620, "height": 34, "font_size": 16, "color": TEXT_SOFT, "font_family": "Roboto"},
    ])
    elems = [
        ("1", "H", "Hydrogen", GREEN_LIGHT),
        ("6", "C", "Carbon", BLUE_LIGHT),
        ("18", "Ar", "Argon", MUTED),
        ("0", "Dc", "Decisions", AMBER_LIGHT),
        ("3.8", "Lv", "Live Voice", RED_LIGHT),
    ]
    for i, (num, sym, lbl, col) in enumerate(elems):
        x = 46 + i * 116
        ops.extend([
            {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": x, "y": 182, "width": 102, "height": 96, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": x, "y": 182, "width": 102, "height": 3, "background_color": col},
            {"op": "add-textbox", "slide": "p", "text": num, "x": x + 8, "y": 190, "width": 86, "height": 16, "font_size": 9, "color": MUTED, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "p", "text": sym, "x": x + 8, "y": 208, "width": 86, "height": 38, "font_size": 26, "bold": True, "color": col, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "p", "text": lbl.upper(), "x": x + 8, "y": 252, "width": 86, "height": 18, "font_size": 8.5, "bold": True, "color": TEXT_SOFT, "font_family": "Roboto Mono"},
        ])
    ops.extend([
        {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": 46, "y": 328, "width": 628, "height": 1.2, "background_color": "#25334D"},
        {"op": "add-textbox", "slide": "p", "text": "Manikandan (Mani)  ·  Principal Architect, Google Cloud", "x": 46, "y": 342, "width": 360, "height": 24, "font_size": 12, "bold": True, "color": WHITE, "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "p", "text": "github.com/cmanikandan/gdg-blr-talk-nov14-2026", "x": 386, "y": 342, "width": 288, "height": 24, "font_size": 9.5, "color": MUTED, "font_family": "Roboto Mono", "alignment": "right", "link": "https://github.com/cmanikandan/gdg-blr-talk-nov14-2026"},
        {"op": "set-notes", "slide": "p", "text": "[00:00 - 01:00] High-energy opening! Good morning DevFest Bengaluru! Six months ago an AI coding agent was a smart pair programmer. Today a single session plans with one model, builds in parallel with another, decides with zero output tokens, and ships in the cloud long after you shut your laptop."},
    ])

    # ── SLIDE 02: HEAD FIRST FRESH BADGE ───────────────────────────────────────
    add_head_first_slide(
        ops, imgs, "S02",
        "01 · FULL DISCLOSURE",
        "So New to Google, My Badge Is Still Warm",
        "01_hf_fresh_badge.jpg",
        "[01:00 - 02:15] BADGE JOKE! Hold up your physical Google badge! 'Full transparency: I am SO new to Google Cloud that I just got my badge—it is literally still warm from the printer. I used Gemini 4 Hydrogen this morning just to find the micro-kitchen! The good news: everything I'm showing today I built and verified from scratch myself.'",
    )

    # ── SLIDE 03: HEAD FIRST SIX-MONTH SHIFT ───────────────────────────────────
    add_head_first_slide(
        ops, imgs, "S03",
        "02 · THE ARCHITECTURAL INFLECTION",
        "Six Months Ago vs. Today",
        "02_hf_six_month_shift.jpg",
        "[02:15 - 03:30] Pause and let the room absorb the contrast. Single-model synchronous chat tabs are over. Modern agentic architectures specialize every model to its exact latency, reasoning horizon, and cost envelope.",
    )

    # ── SLIDE 04: NO SLIDEWARE PROMISES ────────────────────────────────────────
    add_blank_slide(ops, "S04", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S04", "text": "THE LIVE KEYNOTE CONTRACT", "x": 42, "y": 26, "width": 636, "height": 18, "font_size": 10, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S04", "text": "No Slideware Promises — One Real Engineering Arc", "x": 42, "y": 48, "width": 636, "height": 34, "font_size": 20, "bold": True, "color": WHITE, "font_family": "Montserrat"},
    ])
    acts = [
        ("ACT I · MINUTE 1", "Kick Off & Close Laptop", "Gemini 4 Carbon architects the MonsoonPay AWS Mumbai tail-latency fix. Three parallel Hydrogen workers build inside isolated git worktrees, then hand off to a Remote Agent VM.", BLUE),
        ("ACT II · MID-TALK", "Voice Check-In Over Multicloud", "Ask Gemini 3.8 Live for status by voice. While it responds, Google ADK 2.0 runs a zero-copy SQL join across Spanner Omni and 40,000 AWS S3 Iceberg rows—then pauses at a HITL gate.", GREEN),
        ("ACT III · WRAP-UP", "Adversarial Audit & PR Review", "Verify the 97.1% p99 drop and green pytest suite—then watch Gemini 4 Carbon run an adversarial security audit and still catch 5 edge cases before a human merges.", AMBER),
    ]
    for i, (k, h, body, col) in enumerate(acts):
        x = 42 + i * 218
        ops.extend([
            {"op": "add-shape", "slide": "S04", "shape_type": "RECTANGLE", "x": x, "y": 102, "width": 202, "height": 212, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S04", "shape_type": "RECTANGLE", "x": x, "y": 102, "width": 202, "height": 4, "background_color": col},
            {"op": "add-textbox", "slide": "S04", "text": k, "x": x + 14, "y": 116, "width": 174, "height": 16, "font_size": 9, "bold": True, "color": col, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "S04", "text": h, "x": x + 14, "y": 136, "width": 174, "height": 34, "font_size": 14, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S04", "text": body, "x": x + 14, "y": 176, "width": 174, "height": 128, "font_size": 10.5, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 135},
        ])
    ops.extend([
        {"op": "add-shape", "slide": "S04", "shape_type": "RECTANGLE", "x": 42, "y": 334, "width": 636, "height": 42, "background_color": "#10192B"},
        {"op": "add-shape", "slide": "S04", "shape_type": "RECTANGLE", "x": 42, "y": 334, "width": 5, "height": 42, "background_color": BLUE},
        {"op": "add-textbox", "slide": "S04", "text": "MENTAL MODEL:   Plan big  ·  Execute fast  ·  Decide small  ·  Review everything.", "x": 58, "y": 342, "width": 610, "height": 26, "font_size": 13, "bold": True, "color": WHITE, "font_family": "Montserrat", "content_alignment": "MIDDLE"},
        {"op": "set-notes", "slide": "S04", "text": "[03:30 - 04:30] Introduce MonsoonPay, our real multi-cloud checkout service running on Spanner Omni across GCP & AWS with Envoy telemetry on AWS S3 Apache Iceberg. Commit to the 3-act live loop."},
    ])

    # ── SLIDE 05: DEMO 1 VIDEO ─────────────────────────────────────────────────
    add_demo_slide(
        ops, imgs, "S05",
        "DEMO 01 · REAL LIVE GEMINI 4 API + ISOLATED GIT WORKTREES",
        f"Minute 1: Carbon Plans, Parallel Hydrogen /swarm ({d1['hydrogen_swarm']['parallel_speedup']}x), Remote VM",
        "demo1_antigravity_swarm_kickoff_poster.png",
        "▶  Watch 1080p 30fps Demo 1 Recording (Google Drive)",
        vids.get("demo1_antigravity_swarm_kickoff", drive.get("folder_url", "")),
        f"[04:30 - 06:30] DEMO 1! Carbon analyzed monsoonpay/circuit_breaker.py in {round(d1['carbon_architect']['latency_ms']/1000,1)}s and caught real architectural risks. Three parallel Hydrogen workers ran inside isolated `git worktree add --detach` sandboxes ({d1['hydrogen_swarm']['parallel_speedup']}x speedup), then we launch `agy --remote-agent` and close the laptop lid!",
    )

    # ── SLIDE 06: HEAD FIRST PERIODIC TABLE ────────────────────────────────────
    add_head_first_slide(
        ops, imgs, "S06",
        "03 · THE CORE ARCHITECTURE",
        "The Periodic Table of Agents",
        "03_hf_periodic_table.jpg",
        "[06:30 - 08:00] Walk through the five elements. Hydrogen = abundant sub-second fuel; Carbon = diamond-strength architect & adversarial verifier; Argon = inert enterprise workhorse; Decisions = zero-output-token control plane; Live 3.8 = voice that reasons while speaking.",
    )

    # ── SLIDE 07: GEMINI 4 MODEL MATRIX ────────────────────────────────────────
    add_blank_slide(ops, "S07", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S07", "text": "GEMINI 4 FAMILY · PRODUCTION SELECTION GUIDE", "x": 42, "y": 24, "width": 636, "height": 18, "font_size": 10, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S07", "text": "Match the Element to the Reasoning Horizon", "x": 42, "y": 46, "width": 636, "height": 32, "font_size": 24, "bold": True, "color": WHITE, "font_family": "Montserrat"},
    ])
    specs = [
        ("C", "Gemini 4 Carbon", "Deep Architect & Verifier", "$2 / $10 per 1M (intro thru Nov 30)", "• Long-horizon reasoning across 1M-token repos\n• 0% bypass on Gray Swan indirect prompt injection\n• #1 CursorBench 4.0 on complex multi-file diffs\n• Use for: Architecture, RCA, adversarial review", BLUE_LIGHT),
        ("Ar", "Gemini 4 Argon", "Enterprise Workhorse", "$2 / $10 per 1M · 1M context", "• 50 AA Intelligence Index with low variance\n• Predictable multi-package refactors & SQL\n• Balanced throughput for regulated pipelines\n• Use for: Core services, migrations, domain RAG", MUTED),
        ("H", "Gemini 4 Hydrogen", "Sub-Second Fuel", "$1.50 / $7.50 flat · 1M context", "• 4 Thinking Tiers: low · medium · high · xhigh\n• 54 AA Index at xhigh · 43/43 PlotlyAnalytics\n• 2.5x faster than Gemini 3.8 Flash\n• Use for: Parallel /swarm workers, tests, UI", GREEN_LIGHT),
    ]
    for i, (sym, name, role, price, bullets, col) in enumerate(specs):
        x = 42 + i * 218
        ops.extend([
            {"op": "add-shape", "slide": "S07", "shape_type": "RECTANGLE", "x": x, "y": 94, "width": 202, "height": 282, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S07", "shape_type": "RECTANGLE", "x": x, "y": 94, "width": 202, "height": 4, "background_color": col},
            {"op": "add-textbox", "slide": "S07", "text": sym, "x": x + 14, "y": 108, "width": 44, "height": 36, "font_size": 22, "bold": True, "color": col, "font_family": "Montserrat", "background_color": BG_DARK, "alignment": "center", "content_alignment": "MIDDLE"},
            {"op": "add-textbox", "slide": "S07", "text": name, "x": x + 64, "y": 108, "width": 128, "height": 20, "font_size": 11, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S07", "text": role, "x": x + 64, "y": 130, "width": 128, "height": 18, "font_size": 8.5, "color": MUTED, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "S07", "text": price, "x": x + 14, "y": 154, "width": 174, "height": 24, "font_size": 8.8, "bold": True, "color": WHITE, "font_family": "Roboto Mono"},
            {"op": "add-shape", "slide": "S07", "shape_type": "RECTANGLE", "x": x + 14, "y": 184, "width": 174, "height": 1, "background_color": "#25334D"},
            {"op": "add-textbox", "slide": "S07", "text": bullets, "x": x + 14, "y": 192, "width": 174, "height": 174, "font_size": 9.8, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 138},
        ])
    ops.append({"op": "set-notes", "slide": "S07", "text": "[08:00 - 09:30] Walk through exact 2026 specs: Hydrogen's 4 thinking tiers let you dial reasoning up to 54 AA Index at flat $1.50/$7.50 pricing across 1M tokens. Carbon holds 0% Gray Swan IPI and #1 CursorBench 4.0."})

    # ── SLIDE 08: HEAD FIRST ANTIGRAVITY ENGINE ────────────────────────────────
    add_head_first_slide(
        ops, imgs, "S08",
        "04 · MULTI-AGENT EXECUTION",
        "Inside Google Antigravity: Orchestrator, /swarm & Remote Agents",
        "04_hf_antigravity_engine.jpg",
        "[09:30 - 11:00] Show how Orchestrator plans with Carbon, `/swarm` executes with parallel Hydrogen workers inside isolated git worktrees, and Remote Agents keep shipping inside dedicated Cloud VMs.",
    )

    # ── SLIDE 09: STOP USING AN LLM AS AN IF-STATEMENT ─────────────────────────
    add_blank_slide(ops, "S09", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S09", "text": "PRODUCTION CONTROL PLANE ANTI-PATTERN", "x": 42, "y": 28, "width": 636, "height": 18, "font_size": 10, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S09", "text": "Stop Burning Output Tokens on Routing & Guardrails", "x": 42, "y": 50, "width": 636, "height": 34, "font_size": 20, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        # Left Bad Card
        {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": 42, "y": 108, "width": 304, "height": 250, "background_color": SURF_DARK},
        {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": 42, "y": 108, "width": 304, "height": 5, "background_color": RED},
        {"op": "add-textbox", "slide": "S09", "text": "THE OLD WAY · AUTOREGRESSIVE JSON", "x": 62, "y": 128, "width": 264, "height": 18, "font_size": 9.5, "bold": True, "color": RED_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S09", "text": "2–8 sec", "x": 62, "y": 156, "width": 264, "height": 56, "font_size": 42, "bold": True, "color": RED_LIGHT, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": "S09", "text": "Decodes one JSON token at a time. Ask 50 compliance checks and you pay for 750–1,700 output tokens + uncalibrated strings.", "x": 62, "y": 224, "width": 264, "height": 112, "font_size": 12.5, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 145},
        # Right Good Card
        {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": 374, "y": 108, "width": 304, "height": 250, "background_color": SURF_DARK},
        {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": 374, "y": 108, "width": 304, "height": 5, "background_color": GREEN},
        {"op": "add-textbox", "slide": "S09", "text": "GEMINI DECISIONS API · SINGLE FORWARD PASS", "x": 394, "y": 128, "width": 264, "height": 18, "font_size": 9.5, "bold": True, "color": GREEN_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S09", "text": "0 out tok", "x": 394, "y": 156, "width": 264, "height": 56, "font_size": 42, "bold": True, "color": GREEN_LIGHT, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": "S09", "text": "Evaluates up to 1,000 independent questions in ONE forward pass. Returns calibrated probabilities at $0.10 / 1M input and $0.00 output.", "x": 394, "y": 224, "width": 264, "height": 112, "font_size": 12.5, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 145},
        {"op": "set-notes", "slide": "S09", "text": "[11:00 - 12:15] Frame the production control-plane tax before revealing the Decisions API prism and our live benchmark showdown."},
    ])

    # ── SLIDE 10: HEAD FIRST DECISIONS API ─────────────────────────────────────
    add_head_first_slide(
        ops, imgs, "S10",
        "05 · DECIDE SMALL",
        "How Gemini Decisions API Eliminates Output-Token Latency",
        "05_hf_decisions_api.jpg",
        "[12:15 - 13:30] Walk through `noul` (calibrated Yes/No probability), `choice` (2 to 255 options), and `score` (rubric expectation), plus multimodal image/audio/PDF support in a single forward pass.",
    )

    # ── SLIDE 11: LIVE BENCHMARK SHOWDOWN (DECISION-1 VS FLASH VS HYDROGEN) ───
    add_blank_slide(ops, "S11", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S11", "text": "HEAD-TO-HEAD BENCHMARK  ·  DECISION-1 VS 3.8 FLASH VS 4 HYDROGEN", "x": 42, "y": 20, "width": 636, "height": 16, "font_size": 9.5, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S11", "text": "Why \"Decide Small\" Changes Production Unit Economics", "x": 42, "y": 40, "width": 636, "height": 30, "font_size": 19, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        # Table 1 Title
        {"op": "add-textbox", "slide": "S11", "text": "8-QUESTION CONTROL PLANE (MEASURED LIVE)   vs.   50-QUESTION COMPLIANCE MATRIX (1 CALL)", "x": 42, "y": 78, "width": 636, "height": 18, "font_size": 9.5, "bold": True, "color": MUTED, "font_family": "Roboto Mono"},
        {"op": "add-table", "slide": "S11", "rows": 4, "cols": 6, "id": "TBL_BENCH", "x": 42, "y": 100, "width": 636, "height": 182},
    ])
    headers = ["Model", "8Q Latency", "8Q Out Tok", "8Q $/1M Calls", "50Q Out Tok", "50Q $/1M Calls"]
    rows_data = [
        [
            "gemini-decision-1",
            f"{b8[0]['latency_ms']} ms (1.0x)",
            "0",
            f"${b8[0]['cost_per_1m_calls_usd']:,.0f}",
            "0",
            f"${b50[0]['cost_per_1m_calls_usd']:,.0f} (Base)",
        ],
        [
            "gemini-3.8-flash (budget=0)",
            f"{b8[1]['latency_ms']:,} ms ({sp8_f}x)",
            str(b8[1]["billed_output_tokens"]),
            f"${b8[1]['cost_per_1m_calls_usd']:,.0f}",
            str(b50[1]["billed_output_tokens"]),
            f"${b50[1]['cost_per_1m_calls_usd']:,.0f} ({r50['cost_savings_vs_3_8_flash']}x)",
        ],
        [
            "gemini-4-hydrogen (low)",
            f"{b8[2]['latency_ms']:,} ms ({sp8_h}x)",
            str(b8[2]["billed_output_tokens"]),
            f"${b8[2]['cost_per_1m_calls_usd']:,.0f} ({c8_h}x)",
            f"{b50[2]['billed_output_tokens']:,}",
            f"${b50[2]['cost_per_1m_calls_usd']:,.0f} ({r50['cost_savings_vs_4_hydrogen']}x)",
        ],
    ]
    for c_idx, h_txt in enumerate(headers):
        ops.append({"op": "set-table-cell", "table": "TBL_BENCH", "row": 0, "col": c_idx, "text": h_txt, "bold": True, "font_size": 9.5, "color": BLUE_LIGHT, "background_color": "#162238", "font_family": "Roboto Mono"})
    for r_idx, r_vals in enumerate(rows_data, start=1):
        is_win = r_idx == 1
        bg = "#0E291A" if is_win else ("#121B2D" if r_idx == 2 else "#172033")
        fg = GREEN_LIGHT if is_win else TEXT_SOFT
        for c_idx, val in enumerate(r_vals):
            ops.append({"op": "set-table-cell", "table": "TBL_BENCH", "row": r_idx, "col": c_idx, "text": val, "bold": is_win or c_idx == 0, "font_size": 10, "color": fg, "background_color": bg, "font_family": "Roboto Mono" if c_idx > 0 else "Roboto"})

    # Bottom 100-question published scaling banner
    ops.extend([
        {"op": "add-shape", "slide": "S11", "shape_type": "RECTANGLE", "x": 42, "y": 310, "width": 636, "height": 62, "background_color": "#0F1D2E"},
        {"op": "add-shape", "slide": "S11", "shape_type": "RECTANGLE", "x": 42, "y": 310, "width": 5, "height": 62, "background_color": GREEN},
        {"op": "add-textbox", "slide": "S11", "text": "GOOGLE PUBLISHED 100-QUESTION SINGLE-REQUEST BENCHMARK (NOV 2026)", "x": 58, "y": 318, "width": 608, "height": 16, "font_size": 9, "bold": True, "color": GREEN_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S11", "text": f"Decision-1: {pub100['gemini_decision_1_ms']} ms   ·   3.8 Flash: {pub100['gemini_3_8_flash_ms']/1000:.1f}s ({pub100['speedup_vs_flash']}x slower)   ·   4 Hydrogen: {pub100['gemini_4_hydrogen_ms']/1000:.1f}s ({pub100['speedup_vs_hydrogen']}x slower)", "x": 58, "y": 338, "width": 608, "height": 26, "font_size": 13, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "set-notes", "slide": "S11", "text": f"[13:30 - 15:15] MONEY SLIDE! Compare live measured numbers: on 8Q control plane, Decision-1 runs in {b8[0]['latency_ms']}ms ({sp8_f}x faster than Flash, {sp8_h}x faster & {c8_h}x cheaper than Hydrogen). On 50 simultaneous compliance checks, Decision-1 is {r50['cost_savings_vs_3_8_flash']}x cheaper than Flash and {r50['cost_savings_vs_4_hydrogen']}x cheaper than Hydrogen ($270 vs $15,150 per 1M calls). At 100Q: 359ms vs 7.2s Flash (20x) and 8.6s Hydrogen (24x)!"},
    ])

    # ── SLIDE 12: DEMO 2 VIDEO ─────────────────────────────────────────────────
    add_demo_slide(
        ops, imgs, "S12",
        "DEMO 02 · LIVE DECISIONS API ARENA",
        "4 Production Events x 8 Qs · Live Flash/Hydrogen Race · Multimodal Single-Pass",
        "demo2_decisions_api_arena_poster.png",
        "▶  Watch 1080p 30fps Demo 2 Recording (Google Drive)",
        vids.get("demo2_decisions_api_arena", drive.get("folder_url", "")),
        "[15:15 - 17:15] DEMO 2! Point out all 4 events caught accurately at 0 output tokens, the live race against 3.8 Flash and 4 Hydrogen, and Round C scoring our own Head First infographic image + text in one forward pass!",
    )

    # ── SLIDE 13: HEAD FIRST LIVE 3.8 VOICE ────────────────────────────────────
    add_head_first_slide(
        ops, imgs, "S13",
        "06 · REASON WHILE SPEAKING",
        "Gemini 3.8 Live Extended Thinking + Async Tool Execution",
        "06_hf_live38_voice.jpg",
        "[17:15 - 18:30] Explain Dual-Track voice: Gemini 3.8 speaks immediately in 97 languages (with Live Avatar GA & SynthID) while firing ADK 2.0 multicloud tools asynchronously in the background—eliminating dead air.",
    )

    # ── SLIDE 14: GOOGLE ADK 2.0 WORKFLOW RUNTIME ──────────────────────────────
    add_blank_slide(ops, "S14", BG_DARK)
    code_snippet = (
        "from google.adk import Workflow, Event\n"
        "from google.adk.workflow import Edge, RetryConfig, START, node\n\n"
        "@node(name=\"decision_gate_node\")\n"
        "async def decision_gate(ctx):\n"
        "    v = apply_policy_gate(call_decisions_api(ctx.state[\"alert\"]))\n"
        "    yield Event(output=v, route=v.adk_route)\n\n"
        "@node(name=\"multicloud_mcp_sql\", retry_config=RetryConfig(max_attempts=3))\n"
        "async def multicloud_sql(ctx):\n"
        "    return query_spanner_omni_x_s3_iceberg()\n\n"
        "@node(name=\"hitl_pr_approval\", require_confirmation=True)\n"
        "async def approve_pr(ctx):   # Native durable HITL pause\n"
        "    return {\"status\": \"APPROVED_AND_SHIPPED\"}"
    )
    ops.extend([
        {"op": "add-textbox", "slide": "S14", "text": "GOOGLE ADK 2.0 (GA · PYTHON / GO / TS / JAVA / C#)", "x": 42, "y": 22, "width": 636, "height": 16, "font_size": 9.5, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S14", "text": "Deterministic Control Flow Around Autonomous Agents", "x": 42, "y": 42, "width": 636, "height": 30, "font_size": 19, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": "S14", "text": code_snippet, "x": 42, "y": 88, "width": 392, "height": 286, "font_size": 9.5, "color": "#DCE8FA", "background_color": SURF_CODE, "font_family": "Roboto Mono", "line_spacing": 145, "content_alignment": "MIDDLE"},
    ])
    adk_pillars = [
        ("Explicit DAG Routing", "Edge(..., route='quarantine') enforces security boundaries in Python/Go/TS code—not hopes inside a prompt.", BLUE),
        ("Native HITL Checkpoints", "require_confirmation=True emits adk_request_input and suspends execution until a human architect approves.", AMBER),
        ("Open Protocol Native", "First-class MCP (Model Context Protocol) toolsets + A2A (Agent-to-Agent) orchestration across 5 languages.", GREEN),
    ]
    for i, (h, body, col) in enumerate(adk_pillars):
        y = 88 + i * 98
        ops.extend([
            {"op": "add-shape", "slide": "S14", "shape_type": "RECTANGLE", "x": 452, "y": y, "width": 226, "height": 88, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S14", "shape_type": "RECTANGLE", "x": 452, "y": y, "width": 4, "height": 88, "background_color": col},
            {"op": "add-textbox", "slide": "S14", "text": h, "x": 466, "y": y + 10, "width": 202, "height": 20, "font_size": 12, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S14", "text": body, "x": 466, "y": y + 32, "width": 202, "height": 50, "font_size": 9.8, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 130},
        ])
    ops.append({"op": "set-notes", "slide": "S14", "text": "[18:30 - 20:00] Real running code from `monsoonpay/adk_workflow.py` on `google-adk==2.14.1`. Highlight deterministic routing, `RetryConfig(max_attempts=3)`, and native `require_confirmation=True` HITL pause."})

    # ── SLIDE 15: HEAD FIRST DATA CLOUD ────────────────────────────────────────
    add_head_first_slide(
        ops, imgs, "S15",
        "07 · ENTERPRISE DATA GRAVITY SOLVED",
        "Google Cloud's Agentic & Multicloud Data Platform",
        "07_hf_agentic_data_cloud.jpg",
        "[20:00 - 21:30] Walk through the temple: Knowledge Catalog + 50+ Managed MCP Servers sitting across Spanner Omni, Borderless Iceberg / BQ Omni, AlloyDB Express, and BigQuery Graph.",
    )

    # ── SLIDE 16: MULTICLOUD DATA BLUEPRINT ────────────────────────────────────
    add_blank_slide(ops, "S16", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S16", "text": "NEW GOOGLE CLOUD DATA OFFERINGS  ·  MULTICLOUD BY DEFAULT", "x": 42, "y": 24, "width": 636, "height": 16, "font_size": 9.5, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S16", "text": "Zero-Copy Data Access Across GCP, AWS & Azure", "x": 42, "y": 44, "width": 636, "height": 30, "font_size": 23, "bold": True, "color": WHITE, "font_family": "Montserrat"},
    ])
    data_cards = [
        ("TRANSACTIONAL EVERYWHERE", "Spanner Omni (GA)", "Distributed SQL with Software TrueTime running natively across GCP, AWS, Azure, OCI, Kubernetes, and Docker.", BLUE),
        ("ZERO-COPY LAKEHOUSE", "Borderless Iceberg & BigQuery Omni", "Query Apache Iceberg on AWS S3 & Azure Blob while federating AWS Glue, Unity Catalog, and Snowflake Horizon with zero egress.", GREEN),
        ("EPHEMERAL AGENT SANDBOXES", "AlloyDB Express + ScaNN", "Serverless PostgreSQL booting in <2 seconds, scaling to zero between swarm runs, with 10B-scale vector search.", AMBER),
        ("SEMANTIC GROUNDING", "Knowledge Catalog + 50+ Managed MCPs", "Universal Context Engine resolves verified cross-cloud joins before SQL generation: 4x SQL accuracy, -75% tokens.", BLUE_LIGHT),
    ]
    for i, (k, h, body, col) in enumerate(data_cards):
        x = 42 + (i % 2) * 326
        y = 94 + (i // 2) * 144
        ops.extend([
            {"op": "add-shape", "slide": "S16", "shape_type": "RECTANGLE", "x": x, "y": y, "width": 310, "height": 128, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S16", "shape_type": "RECTANGLE", "x": x, "y": y, "width": 310, "height": 4, "background_color": col},
            {"op": "add-textbox", "slide": "S16", "text": k, "x": x + 16, "y": y + 14, "width": 278, "height": 16, "font_size": 8.5, "bold": True, "color": col, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "S16", "text": h, "x": x + 16, "y": y + 32, "width": 278, "height": 24, "font_size": 11.8, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S16", "text": body, "x": x + 16, "y": y + 60, "width": 278, "height": 58, "font_size": 10.5, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 135},
        ])
    ops.append({"op": "set-notes", "slide": "S16", "text": "[21:30 - 22:45] Highlight how Spanner Omni, Borderless Iceberg, AlloyDB Express, and Knowledge Catalog remove multi-cloud data friction for production agents."})

    # ── SLIDE 17: DEMO 3 VIDEO (WITH REAL GEMINI 3.8 HD AUDIO!) ────────────────
    add_demo_slide(
        ops, imgs, "S17",
        f"DEMO 03 · REAL GEMINI 3.8 HD AUDIO + GOOGLE ADK {d3['adk_version']} + DUCKDB ZERO-COPY",
        f"Voice Check-In: {sql['rows_correlated']:,} Cross-Cloud Rows Joined in {sql['query_latency_ms']} ms + HITL Pause",
        "demo3_live38_voice_multicloud_adk_poster.png",
        "▶  Play 1080p Demo 3 WITH REAL Gemini 3.8 HD Voice Audio (Google Drive)",
        vids.get("demo3_live38_voice_multicloud_adk", drive.get("folder_url", "")),
        f"[22:45 - 24:45] DEMO 3 — TURN UP AUDIO! Real Gemini 3.8 HD voices (`Orus` & `Puck`) synced to our live ADK 2.14.1 DAG ({d3['adk_total_ms']}ms total). Zero-copy DuckDB joins 40,000 AWS S3 Iceberg rows with Spanner Omni in {sql['query_latency_ms']}ms, isolating the 64-slot Envoy retry storm while TrueTime holds 2.75ms!",
        cta_bg="#065F46",
    )

    # ── SLIDE 18: BEYOND CODE 2026 BREAKTHROUGHS ───────────────────────────────
    add_blank_slide(ops, "S18", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S18", "text": "THE WIDER 2026 PLATFORM  ·  PRINCIPAL ARCHITECT RADAR", "x": 42, "y": 24, "width": 636, "height": 16, "font_size": 9.5, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S18", "text": "Four Force Multipliers Beyond Code Generation", "x": 42, "y": 44, "width": 636, "height": 30, "font_size": 23, "bold": True, "color": WHITE, "font_family": "Montserrat"},
    ])
    extras = [
        ("CUSTOM SILICON", "8th-Gen TPUs (TPU 8t & 8i)", "Purpose-built AI silicon driving 16B+ tokens/minute globally—making parallel sub-second Hydrogen swarms affordable at scale.", BLUE),
        ("ENTERPRISE GRAVITY", "Oracle AI Database@Google Cloud", "Zero-latency Exadata & Autonomous Database inside Google Cloud regions—connecting legacy core banking directly to ADK 2.0.", AMBER),
        ("AGENTIC INTERFACES", "Nano Banana 2.1 · Omni 1.2 · /generative_ui", "Agents move beyond Markdown text walls—synthesizing rich diagrams, HD audio, and live interactive HTML widgets on demand.", GREEN),
        ("FORMAL VERIFICATION", "AlphaProof Code", "Pairs neural code generation with formal Lean mathematical proofs for consensus, cryptography, and financial invariants.", BLUE_LIGHT),
    ]
    for i, (k, h, body, col) in enumerate(extras):
        x = 42 + (i % 2) * 326
        y = 94 + (i // 2) * 144
        ops.extend([
            {"op": "add-shape", "slide": "S18", "shape_type": "RECTANGLE", "x": x, "y": y, "width": 310, "height": 128, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S18", "shape_type": "RECTANGLE", "x": x, "y": y, "width": 310, "height": 4, "background_color": col},
            {"op": "add-textbox", "slide": "S18", "text": k, "x": x + 16, "y": y + 14, "width": 278, "height": 16, "font_size": 8.5, "bold": True, "color": col, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "S18", "text": h, "x": x + 16, "y": y + 32, "width": 278, "height": 24, "font_size": 11.8, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S18", "text": body, "x": x + 16, "y": y + 60, "width": 278, "height": 58, "font_size": 10.5, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 135},
        ])
    ops.append({"op": "set-notes", "slide": "S18", "text": "[24:45 - 26:00] Fast 60-second Principal Architect tour of 8th-gen TPUs, Oracle@GCP, Nano Banana 2.1 + `/generative_ui`, and AlphaProof Code."})

    # ── SLIDE 19: DEMO 4 VIDEO ─────────────────────────────────────────────────
    add_demo_slide(
        ops, imgs, "S19",
        "DEMO 04 · ADVERSARIAL VERIFICATION & PULL REQUEST #1",
        f"p99 Dropped {sla['p99_reduction_pct']}% & Pytest Passed — Yet Carbon Still Caught 5 Edge Cases",
        "demo4_review_shipped_pr_poster.png",
        "▶  Watch 1080p 30fps Demo 4 Recording (Google Drive)",
        vids.get("demo4_review_shipped_pr", drive.get("folder_url", "")),
        f"[26:00 - 27:45] DEMO 4! Even after p99 dropped from {sla['before']['p99_ms']}ms to {sla['after']['p99_ms']}ms and all 9 unit tests went green, live `gemini-4-carbon` returned `{ca['audit']['overall_verdict']}`—flagging 5 subtle edge cases (unused autonomy_readiness, low-res multimodal IPI, negative/NaN TrueTime guard, HALF_OPEN race). That is why Rule 4 is Review Everything!",
        cta_bg="#92400E",
    )

    # ── SLIDE 20: VERIFIED PRODUCTION IMPACT ───────────────────────────────────
    add_blank_slide(ops, "S20", BG_DARK)
    ops.extend([
        {"op": "add-textbox", "slide": "S20", "text": "VERIFIED LIVE KEYNOTE OUTCOMES", "x": 42, "y": 28, "width": 636, "height": 18, "font_size": 10, "bold": True, "color": BLUE_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S20", "text": "What the Periodic Table Architecture Actually Buys You", "x": 42, "y": 50, "width": 636, "height": 34, "font_size": 19, "bold": True, "color": WHITE, "font_family": "Montserrat"},
    ])
    kpis = [
        (f"-{sla['p99_reduction_pct']}%", "Checkout p99 Latency", f"{sla['before']['p99_ms']} ms -> {sla['after']['p99_ms']} ms verified across 500-request AWS ap-south-1 flash-sale burst.", GREEN_LIGHT),
        (f"{r50['cost_savings_vs_4_hydrogen']}x", "Cheaper Control Plane", "50-question compliance matrix: $270 / 1M calls on Decision-1 vs $15,150 / 1M on Hydrogen (0 output tokens).", BLUE_LIGHT),
        ("5", "Bugs Caught Pre-Merge", "Subtle security & concurrency edge cases caught by live Gemini 4 Carbon even after 9/9 unit tests passed.", AMBER_LIGHT),
    ]
    for i, (num, head, desc, col) in enumerate(kpis):
        x = 42 + i * 218
        ops.extend([
            {"op": "add-shape", "slide": "S20", "shape_type": "RECTANGLE", "x": x, "y": 110, "width": 202, "height": 244, "background_color": SURF_DARK},
            {"op": "add-shape", "slide": "S20", "shape_type": "RECTANGLE", "x": x, "y": 110, "width": 202, "height": 5, "background_color": col},
            {"op": "add-textbox", "slide": "S20", "text": num, "x": x + 16, "y": 132, "width": 170, "height": 56, "font_size": 38, "bold": True, "color": col, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S20", "text": head, "x": x + 16, "y": 196, "width": 170, "height": 26, "font_size": 13.5, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S20", "text": desc, "x": x + 16, "y": 240, "width": 170, "height": 102, "font_size": 10.5, "color": TEXT_SOFT, "font_family": "Roboto", "line_spacing": 140},
        ])
    ops.append({"op": "set-notes", "slide": "S20", "text": "[27:45 - 28:30] Pause on these three verified numbers measured directly on our live codebase today."})

    # ── SLIDE 21: HEAD FIRST MENTAL MODEL POSTER ───────────────────────────────
    add_head_first_slide(
        ops, imgs, "S21",
        "08 · TAKE A PHOTO",
        "The Battle-Tested Mental Model for Agentic Systems",
        "08_hf_mental_model_poster.jpg",
        "[28:30 - 29:15] Phones up! If you take ONE poster back to your engineering team on Monday: Plan Big, Execute Fast, Decide Small, Review Everything.",
    )

    # ── SLIDE 22: CLOSING & REPO CTA ───────────────────────────────────────────
    add_blank_slide(ops, "S22", BG_DARK)
    ops.extend([
        {"op": "add-shape", "slide": "S22", "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 8, "height": 405, "background_color": GREEN},
        {"op": "add-textbox", "slide": "S22", "text": "ALL CODE · REAL ADK 2.0 GRAPH · LIVE BENCHMARKS · OPEN SOURCE", "x": 48, "y": 46, "width": 624, "height": 18, "font_size": 10, "bold": True, "color": GREEN_LIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S22", "text": "Plan Big. Execute Fast.\nDecide Small. Review Everything.", "x": 48, "y": 76, "width": 624, "height": 98, "font_size": 34, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-shape", "slide": "S22", "shape_type": "RECTANGLE", "x": 48, "y": 204, "width": 540, "height": 74, "background_color": SURF_DARK},
        {"op": "add-shape", "slide": "S22", "shape_type": "RECTANGLE", "x": 48, "y": 204, "width": 5, "height": 74, "background_color": BLUE},
        {"op": "add-textbox", "slide": "S22", "text": "CLONE THE KEYNOTE REPOSITORY & ALL 4 DEMOS", "x": 68, "y": 216, "width": 500, "height": 16, "font_size": 9, "bold": True, "color": MUTED, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S22", "text": "github.com/cmanikandan/gdg-blr-talk-nov14-2026", "x": 68, "y": 236, "width": 500, "height": 30, "font_size": 16, "bold": True, "color": WHITE, "font_family": "Roboto Mono", "link": "https://github.com/cmanikandan/gdg-blr-talk-nov14-2026"},
        {"op": "add-shape", "slide": "S22", "shape_type": "RECTANGLE", "x": 48, "y": 324, "width": 624, "height": 1.2, "background_color": "#25334D"},
        {"op": "add-textbox", "slide": "S22", "text": "Manikandan (Mani)  ·  Principal Architect, Google Cloud  ·  DevFest Bengaluru 2026", "x": 48, "y": 340, "width": 624, "height": 26, "font_size": 12, "color": TEXT_SOFT, "font_family": "Roboto"},
        {"op": "set-notes", "slide": "S22", "text": "[29:15 - 30:00] Closing badge callback! 'Thank you DevFest Bengaluru! Everything is open-sourced at this repo—and if anyone knows where the best filter coffee is at Google Bengaluru, come find the Principal Architect with the brand-new badge!'"},
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
    parser.add_argument("--images-only", action="store_true", help="Only place 12 images on an existing 22-slide deck and export PDF/PPTX")
    args = parser.parse_args()

    tr = load_traces()
    drive = load_drive_links()
    ops, img_jobs = build_deck_ops(tr, drive)

    title = "The Periodic Table of Agents: Building with Gemini 4 & Antigravity — DevFest Bengaluru 2026 Keynote (v2)"
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
        if len(slide_ids) != 22:
            raise RuntimeError(f"Expected 22 slides on {pres_id}, found {len(slide_ids)}")
        resolved = {"p": slide_ids[0]}
        for n in range(2, 23):
            resolved[f"S{n:02d}"] = slide_ids[n - 1]
    else:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
            json.dump(ops, tf, indent=2)
            batch_file = tf.name
        try:
            print(f"Applying {len(ops)} batch operations across 22 slides...")
            batch_raw = run_cmd(["gslides", "mutate", "batch", pres_id, "-f", batch_file, "--json"])
            batch_res = json.loads(batch_raw)
            resolved = batch_res.get("resolved_ids", {})
            resolved["p"] = "p"
            print(f"  ✔ Batch complete ({batch_res.get('operations')} ops, {len(batch_res.get('created_slides', []))+1} slides)")
        finally:
            Path(batch_file).unlink(missing_ok=True)

    print(f"Fetching signed GitHub URLs & placing {len(img_jobs)} crisp 16:9 Head First infographics & demo posters...")
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
        "slide_count": 22,
        "drive_videos_folder_id": drive.get("folder_id", ""),
        "drive_videos_folder_url": drive.get("folder_url", ""),
        "drive_videos": drive.get("videos", {}),
        "resolved_slide_ids": resolved,
    }
    (PRES_DIR / "google_slides_metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"🎉 DONE! Google Slides URL: {meta['presentation_url']}")


if __name__ == "__main__":
    main()
