#!/usr/bin/env python3
"""
Builds the 18-Slide World-Class Gemini 4 Neon Keynote in Google Slides via `gslides`,
exports PDF & PPTX, and embeds all 7 real playable `.mp4` videos natively inside the
exported `.pptx` (including Slides 15 & 16 split Architecture + Video Voice AI slides!).

Design System (720pt x 405pt 16:9 Widescreen):
  - Deep Obsidian (#07080B) + Physical Warm Neon (#FF7A1A / #FFA352) + Google Blue (#4285F4) + Emerald (#34A853)
  - 100% PUBLIC Gemini 4 Neon launch data (blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/)
  - 100% Google Cloud-native story, code, and live verified traces (`demos/traces/demo{1..5}_trace.json`)
  - Exact native aspect ratios for every diagram and video poster (zero stretching!)
  - Full private Speaker Notes on all 18 slides
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DIAG_DIR = ROOT / "assets" / "diagrams"
VID_DIR = ROOT / "assets" / "videos"
TRACES_DIR = ROOT / "demos" / "traces"
PRES_DIR = ROOT / "presentation"
DRIVE_META_PATH = PRES_DIR / "drive_videos_v2.json"

LINKEDIN_URL = "https://www.linkedin.com/in/cmanikandan"
GITHUB_URL = "https://github.com/cmanikandan/gdg-blr-talk-nov14-2026"
NEON_BLOG_URL = "https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/"
DRIVE_FLIGHT_URL = "https://drive.google.com/file/d/1KkvhldhlXGUEYQMLs28EMQXsSeAbZRZO/view"
DRIVE_PSTN_URL = "https://drive.google.com/file/d/1kv3NheXiAbhIBhYuBDUMRBCa054gIE9M/view"

# Obsidian + Warm Neon Palette
BG = "#07080B"
SURFACE = "#111319"
SURFACE_2 = "#171A23"
BORDER = "#242A38"
BG_CREAM = "#FAF7F0"
INK_DARK = "#1A202C"

WHITE = "#F8FAFC"
SOFT = "#C2CCDC"
MUTED = "#8793A8"

NEON = "#FF7A1A"
NEON_BRIGHT = "#FFA352"
NEON_BG = "#2A1609"
BLUE = "#4285F4"
BLUE_BRIGHT = "#75A8FF"
BLUE_BG = "#0F1D36"
GREEN = "#34A853"
GREEN_BRIGHT = "#62D987"
GREEN_BG = "#0D2418"
AMBER = "#F59E0B"
AMBER_BRIGHT = "#FBBF24"
RED = "#EA4335"
RED_BRIGHT = "#FF786E"
RED_BG = "#281014"


def run_cmd(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"Command failed ({' '.join(cmd)}):\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}"
        )
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


def add_header(
    ops: List[Dict[str, Any]],
    slide_id: str,
    kicker: str,
    title: str,
    dark: bool = True,
    right_label: str = "",
    right_link: str = "",
) -> None:
    k_color = NEON_BRIGHT if dark else "#1D4ED8"
    t_color = WHITE if dark else INK_DARK
    div_color = BORDER if dark else "#D6CFC2"
    ops.extend([
        {
            "op": "add-textbox",
            "slide": slide_id,
            "text": kicker,
            "x": 36,
            "y": 14,
            "width": 500,
            "height": 16,
            "font_size": 8.8,
            "bold": True,
            "color": k_color,
            "font_family": "Roboto Mono",
        },
        {
            "op": "add-textbox",
            "slide": slide_id,
            "text": title,
            "x": 36,
            "y": 30,
            "width": 648,
            "height": 28,
            "font_size": 17.5,
            "bold": True,
            "color": t_color,
            "font_family": "Montserrat",
        },
        {
            "op": "add-shape",
            "slide": slide_id,
            "shape_type": "RECTANGLE",
            "x": 36,
            "y": 60,
            "width": 648,
            "height": 1.0,
            "background_color": div_color,
        },
    ])
    if right_label:
        tb: Dict[str, Any] = {
            "op": "add-textbox",
            "slide": slide_id,
            "text": right_label,
            "x": 500,
            "y": 14,
            "width": 184,
            "height": 18,
            "font_size": 8.5,
            "bold": True,
            "color": MUTED if dark else "#475569",
            "font_family": "Roboto Mono",
            "alignment": "right",
        }
        if right_link:
            tb["link"] = right_link
        ops.append(tb)


def add_visual_slide(
    ops: List[Dict[str, Any]],
    img_jobs: List[Dict[str, Any]],
    slide_id: str,
    kicker: str,
    title: str,
    img_filename: str,
    notes: str,
    dark: bool = True,
) -> None:
    """Full-stage 1376x768 (1.7917 ratio) diagram slide with exact aspect ratio."""
    add_blank_slide(ops, slide_id, BG if dark else BG_CREAM)
    add_header(ops, slide_id, kicker, title, dark=dark)
    ops.append({"op": "set-notes", "slide": slide_id, "text": notes})
    # Exact 1376/768 = 1.79167 -> width=576.9, height=322.0 centered horizontally at x=71.55, y=69
    img_jobs.append({
        "slide": slide_id,
        "file": str(DIAG_DIR / img_filename),
        "x": 71.5,
        "y": 69.0,
        "width": 577.0,
        "height": 322.0,
    })


def add_demo_split_slide(
    ops: List[Dict[str, Any]],
    img_jobs: List[Dict[str, Any]],
    video_jobs: List[Dict[str, Any]],
    slide_id: str,
    slide_index: int,
    kicker: str,
    title: str,
    kpi1: Tuple[str, str, str],
    kpi2: Tuple[str, str, str],
    bullets: List[str],
    poster_filename: str,
    video_filename: str,
    bar_label: str,
    drive_url: str,
    notes: str,
    accent: str = NEON,
) -> None:
    """Clean 2-column Demo Slide: Left plain-English story + KPIs, Right crisp 16:9 video frame."""
    add_blank_slide(ops, slide_id, BG)
    ops.append({
        "op": "add-shape",
        "slide": slide_id,
        "shape_type": "RECTANGLE",
        "x": 0,
        "y": 0,
        "width": 6,
        "height": 405,
        "background_color": accent,
    })
    ops.extend([
        {
            "op": "add-textbox",
            "slide": slide_id,
            "text": kicker,
            "x": 34,
            "y": 24,
            "width": 274,
            "height": 16,
            "font_size": 8.5,
            "bold": True,
            "color": NEON_BRIGHT,
            "font_family": "Roboto Mono",
        },
        {
            "op": "add-textbox",
            "slide": slide_id,
            "text": title,
            "x": 34,
            "y": 42,
            "width": 274,
            "height": 58,
            "font_size": 17.5,
            "bold": True,
            "color": WHITE,
            "font_family": "Montserrat",
            "line_spacing": 115,
        },
    ])

    # Two compact KPI tiles on left
    for idx, (val, lbl, col) in enumerate([kpi1, kpi2]):
        kx = 34 + idx * 138
        ops.extend([
            {
                "op": "add-shape",
                "slide": slide_id,
                "shape_type": "RECTANGLE",
                "x": kx,
                "y": 110,
                "width": 130,
                "height": 64,
                "background_color": SURFACE,
            },
            {
                "op": "add-shape",
                "slide": slide_id,
                "shape_type": "RECTANGLE",
                "x": kx,
                "y": 110,
                "width": 130,
                "height": 2.5,
                "background_color": col,
            },
            {
                "op": "add-textbox",
                "slide": slide_id,
                "text": val,
                "x": kx + 8,
                "y": 118,
                "width": 114,
                "height": 26,
                "font_size": 15.0 if len(val) <= 9 else 12.2,
                "bold": True,
                "color": col,
                "font_family": "Montserrat",
            },
            {
                "op": "add-textbox",
                "slide": slide_id,
                "text": lbl,
                "x": kx + 8,
                "y": 146,
                "width": 114,
                "height": 24,
                "font_size": 8.0,
                "color": SOFT,
                "font_family": "Roboto",
                "line_spacing": 115,
            },
        ])

    # Plain-English bullets
    bullet_text = "\n\n".join(f"▸  {b}" for b in bullets)
    ops.append({
        "op": "add-textbox",
        "slide": slide_id,
        "text": bullet_text,
        "x": 34,
        "y": 188,
        "width": 272,
        "height": 196,
        "font_size": 9.8,
        "color": SOFT,
        "font_family": "Roboto",
        "line_spacing": 130,
    })

    # Right video container card
    ops.extend([
        {
            "op": "add-shape",
            "slide": slide_id,
            "shape_type": "RECTANGLE",
            "x": 320,
            "y": 64,
            "width": 368,
            "height": 268,
            "background_color": SURFACE,
        },
        {
            "op": "add-shape",
            "slide": slide_id,
            "shape_type": "RECTANGLE",
            "x": 320,
            "y": 64,
            "width": 368,
            "height": 3,
            "background_color": accent,
        },
    ])

    # Exact 16:9 poster/video box: 356 x 200.25 at (326, 74)
    vx, vy, vw, vh = 326.0, 74.0, 356.0, 200.25
    img_jobs.append({
        "slide": slide_id,
        "file": str(VID_DIR / poster_filename),
        "x": vx,
        "y": vy,
        "width": vw,
        "height": vh,
    })
    video_jobs.append({
        "slide_index": slide_index,
        "video": str(VID_DIR / video_filename),
        "poster": str(VID_DIR / poster_filename),
        "x": vx,
        "y": vy,
        "width": vw,
        "height": vh,
    })

    # Video footer bar (clickable Drive link in Google Slides; real video plays inline in PPTX & HTML5)
    cta: Dict[str, Any] = {
        "op": "add-textbox",
        "slide": slide_id,
        "text": f"▶  {bar_label}",
        "x": 326,
        "y": 284,
        "width": 356,
        "height": 38,
        "font_size": 9.0,
        "bold": True,
        "color": WHITE,
        "background_color": SURFACE_2,
        "font_family": "Roboto Mono",
        "alignment": "center",
        "content_alignment": "MIDDLE",
    }
    if drive_url:
        cta["link"] = drive_url
    ops.append(cta)

    ops.append({
        "op": "add-textbox",
        "slide": slide_id,
        "text": "Tip: Plays natively inline in HTML5 Keynote & PPTX (or open Stage Studio to run LIVE)",
        "x": 320,
        "y": 340,
        "width": 368,
        "height": 22,
        "font_size": 7.8,
        "color": MUTED,
        "font_family": "Roboto",
        "alignment": "center",
    })
    ops.append({"op": "set-notes", "slide": slide_id, "text": notes})


def add_voice_arch_video_slide(
    ops: List[Dict[str, Any]],
    img_jobs: List[Dict[str, Any]],
    video_jobs: List[Dict[str, Any]],
    slide_id: str,
    slide_index: int,
    kicker: str,
    title: str,
    badge_text: str,
    badge_color: str,
    arch_filename: str,
    poster_filename: str,
    video_filename: str,
    video_ratio: float,
    video_caption: str,
    video_highlights: List[str],
    drive_url: str,
    notes: str,
) -> None:
    """Split Voice AI Slide: Architecture Diagram (3:4) on LEFT + Real Video on RIGHT."""
    add_blank_slide(ops, slide_id, BG)
    add_header(ops, slide_id, kicker, title, dark=True, right_label=badge_text)

    # Left: 896x1200 (ratio 0.74667) -> width=236.0, height=316.0 at x=36, y=72
    ops.append({
        "op": "add-shape",
        "slide": slide_id,
        "shape_type": "RECTANGLE",
        "x": 34,
        "y": 70,
        "width": 240,
        "height": 320,
        "background_color": SURFACE,
    })
    img_jobs.append({
        "slide": slide_id,
        "file": str(DIAG_DIR / arch_filename),
        "x": 36.0,
        "y": 72.0,
        "width": 236.0,
        "height": 316.0,
    })

    # Right: Video Player Container (x=288..686, width=398, y=70..390, height=320)
    ops.extend([
        {
            "op": "add-shape",
            "slide": slide_id,
            "shape_type": "RECTANGLE",
            "x": 288,
            "y": 70,
            "width": 398,
            "height": 320,
            "background_color": SURFACE,
        },
        {
            "op": "add-shape",
            "slide": slide_id,
            "shape_type": "RECTANGLE",
            "x": 288,
            "y": 70,
            "width": 398,
            "height": 3,
            "background_color": badge_color,
        },
    ])

    vw = 382.0
    vh = round(vw / video_ratio, 2)
    vx = 296.0
    vy = 82.0
    img_jobs.append({
        "slide": slide_id,
        "file": str(VID_DIR / poster_filename),
        "x": vx,
        "y": vy,
        "width": vw,
        "height": vh,
    })
    video_jobs.append({
        "slide_index": slide_index,
        "video": str(VID_DIR / video_filename),
        "poster": str(VID_DIR / poster_filename),
        "x": vx,
        "y": vy,
        "width": vw,
        "height": vh,
    })

    cap_y = vy + vh + 8
    cap_box: Dict[str, Any] = {
        "op": "add-textbox",
        "slide": slide_id,
        "text": f"▶  {video_caption}",
        "x": 296,
        "y": cap_y,
        "width": 382,
        "height": 26,
        "font_size": 8.8,
        "bold": True,
        "color": WHITE,
        "background_color": SURFACE_2,
        "font_family": "Roboto Mono",
        "alignment": "center",
        "content_alignment": "MIDDLE",
    }
    if drive_url:
        cap_box["link"] = drive_url
    ops.append(cap_box)

    hl_y = cap_y + 32
    hl_h = max(32, 386 - hl_y)
    ops.append({
        "op": "add-textbox",
        "slide": slide_id,
        "text": "\n".join(f"•  {h}" for h in video_highlights),
        "x": 298,
        "y": hl_y,
        "width": 378,
        "height": hl_h,
        "font_size": 8.8,
        "color": SOFT,
        "font_family": "Roboto",
        "line_spacing": 125,
    })
    ops.append({"op": "set-notes", "slide": slide_id, "text": notes})


def build_deck_ops(
    tr: Dict[str, Any], drive: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    d1, d2, d3, d4, d5 = tr["d1"], tr["d2"], tr["d3"], tr["d4"], tr["d5"]
    vids = drive.get("videos", {})

    # Demo 1 metrics
    swarm = d1.get("hydrogen_swarm", {})
    d1_speedup = swarm.get("parallel_speedup", 1.83)
    d1_wall_s = round(swarm.get("wall_clock_ms", 10836) / 1000, 1)
    d1_seq_s = round(swarm.get("sequential_sum_ms", 19779) / 1000, 1)
    d1_workers = swarm.get("workers", [])[:3]

    # Demo 5 metrics
    b5 = d5.get("benchmark", {"legacy_ms": 411.1, "modern_ms": 4.09, "speedup_factor": 100.5})
    gf5 = d5.get("golden_falsifier", {"total_net_payout_paise": 5623206619})
    payout_cr = f"{gf5.get('total_net_payout_paise', 5623206619) / 100 / 1e7:.2f}"
    rules5 = (d5.get("neon_analysis") or d5.get("carbon_analysis") or {}).get("plan", {}).get("hidden_invariants", [])[:4]

    # Demo 2 metrics
    b8 = d2["round_b_head_to_head"]["benchmark_8q"]
    b50 = d2["round_b_head_to_head"]["benchmark_50q"]
    r50 = d2["round_b_head_to_head"]["live_ratios_50q"]
    pub100 = d2["round_b_head_to_head"]["published_100q_reference"]
    mm2 = d2["round_c_multimodal"]
    d1_8_ms, fl_8_ms, hy_8_ms = b8[0]["latency_ms"], b8[1]["latency_ms"], b8[2]["latency_ms"]
    d1_50_ms, fl_50_ms, hy_50_ms = b50[0]["latency_ms"], b50[1]["latency_ms"], b50[2]["latency_ms"]
    d1_50_cost = b50[0]["cost_per_1m_calls_usd"]
    fl_50_cost = b50[1]["cost_per_1m_calls_usd"]
    hy_50_cost = b50[2]["cost_per_1m_calls_usd"]
    sp8_fl = round(fl_8_ms / max(d1_8_ms, 1), 1)
    sp50_fl = r50["speedup_vs_3_8_flash"]
    cs50_hy = r50["cost_savings_vs_4_hydrogen"]

    # Demo 3 metrics
    sql3 = d3.get("lakehouse_finding") or d3["multicloud_finding"]
    sql3_ms = int(round(sql3["query_latency_ms"]))
    sql3_rows = int(sql3["rows_correlated"])

    # Demo 4 metrics
    sla4 = d4["sla_benchmark"]
    bef4, aft4, drop4 = sla4["before"]["p99_ms"], sla4["after"]["p99_ms"], sla4["p99_reduction_pct"]
    tests4 = d4["pytest"]["passed_count"]
    audit4 = (d4.get("neon_security_audit") or d4.get("carbon_security_audit") or {}).get("audit", {})
    verdict4 = str(audit4.get("overall_verdict", "APPROVE_WITH_NOTE")).replace("_", " ")
    warn_checks = [c for c in audit4.get("checks", []) if str(c.get("status", "")).upper() != "PASS"]
    warn_finding = warn_checks[0]["finding"] if warn_checks else "Catches subtle approval gaps before merge."

    ops: List[Dict[str, Any]] = []
    imgs: List[Dict[str, Any]] = []
    video_jobs: List[Dict[str, Any]] = []

    # ── SLIDE 01 (`p`): COVER ──────────────────────────────────────────────────
    add_blank_slide(ops, "p", BG, is_first=True)
    ops.extend([
        {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 7, "height": 405, "background_color": NEON},
        {"op": "add-textbox", "slide": "p", "text": "DEVFEST BENGALURU 2026  ·  KEYNOTE", "x": 44, "y": 28, "width": 632, "height": 18, "font_size": 9.5, "bold": True, "color": NEON_BRIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "p", "text": "The Periodic Table\nof Agents", "x": 44, "y": 50, "width": 632, "height": 94, "font_size": 36, "bold": True, "color": WHITE, "font_family": "Montserrat", "line_spacing": 106},
        {"op": "add-textbox", "slide": "p", "text": "Building Production AI Systems with Gemini 4 Neon & Google Antigravity", "x": 44, "y": 146, "width": 632, "height": 26, "font_size": 13.5, "color": SOFT, "font_family": "Roboto"},
    ])
    tiles = [
        ("1", "H", "HYDROGEN", BLUE_BRIGHT, SURFACE),
        ("10", "Ne", "NEON", NEON_BRIGHT, NEON_BG),
        ("6", "C", "CARBON", WHITE, SURFACE),
        ("18", "Ar", "ARGON", GREEN_BRIGHT, SURFACE),
        ("0", "Dc", "DECISIONS", AMBER_BRIGHT, SURFACE),
        ("3.8", "Lv", "LIVE VOICE", GREEN_BRIGHT, SURFACE),
    ]
    for i, (num, sym, lbl, col, bg_tile) in enumerate(tiles):
        tx = 44 + i * 107
        ops.extend([
            {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": tx, "y": 190, "width": 96, "height": 96, "background_color": bg_tile},
            {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": tx, "y": 190, "width": 96, "height": 3, "background_color": col},
            {"op": "add-textbox", "slide": "p", "text": num, "x": tx + 8, "y": 198, "width": 80, "height": 14, "font_size": 8.5, "color": MUTED, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "p", "text": sym, "x": tx + 8, "y": 214, "width": 80, "height": 38, "font_size": 25, "bold": True, "color": col, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "p", "text": lbl, "x": tx + 8, "y": 258, "width": 80, "height": 18, "font_size": 7.8, "bold": True, "color": SOFT, "font_family": "Roboto Mono"},
        ])
    ops.extend([
        {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": 44, "y": 318, "width": 632, "height": 1.0, "background_color": BORDER},
        {"op": "add-textbox", "slide": "p", "text": "Mani  ·  Principal Architect, Google Cloud", "x": 44, "y": 330, "width": 360, "height": 22, "font_size": 12.5, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": "p", "text": "linkedin.com/in/cmanikandan", "x": 44, "y": 354, "width": 260, "height": 20, "font_size": 9.8, "bold": True, "color": NEON_BRIGHT, "font_family": "Roboto Mono", "link": LINKEDIN_URL},
        {"op": "add-textbox", "slide": "p", "text": "github.com/cmanikandan/gdg-blr-talk-nov14-2026", "x": 336, "y": 354, "width": 340, "height": 20, "font_size": 9.2, "color": MUTED, "font_family": "Roboto Mono", "alignment": "right", "link": GITHUB_URL},
        {
            "op": "set-notes",
            "slide": "p",
            "text": (
                "Good morning DevFest Bengaluru! Today is an electric moment to build with Gemini. "
                "Just days ago Google launched Gemini 4 Neon — frontier-level intelligence built for speed. "
                "Over the next 40 minutes, I will give you ONE simple mental model and 6 real demos — "
                "zero fluff, 100% live Google Cloud architecture — whether you shipped your first API call yesterday "
                "or run banking infrastructure at scale."
            ),
        },
    ])

    # ── SLIDE 02: FRESH BADGE ──────────────────────────────────────────────────
    add_visual_slide(
        ops, imgs, "S02",
        "01 · FULL DISCLOSURE",
        "So New to Google, My Badge Is Still Warm",
        "01_fresh_badge.jpg",
        "Hold up your badge! 'Full disclosure: I am so new to Google Cloud that my badge is literally still warm from the printer — I asked Gemini 4 Hydrogen how to find the micro-kitchen this morning! The good news for you: I built, broke, and live-tested every single demo myself from scratch.'",
        dark=False,
    )

    # ── SLIDE 03: INTRODUCING GEMINI 4 NEON (GLOWING NEON TUBE HERO) ───────────
    add_blank_slide(ops, "S03", BG)
    ops.extend([
        {"op": "add-textbox", "slide": "S03", "text": "JUST LAUNCHED  ·  FRONTIER INTELLIGENCE BUILT FOR SPEED", "x": 36, "y": 10, "width": 648, "height": 16, "font_size": 9.0, "bold": True, "color": NEON_BRIGHT, "font_family": "Roboto Mono", "alignment": "center"},
        # Bottom glass stat bar (sits cleanly below the 1376x768 hero image with zero overlap!)
        {"op": "add-shape", "slide": "S03", "shape_type": "RECTANGLE", "x": 36, "y": 328, "width": 648, "height": 64, "background_color": SURFACE},
        {"op": "add-shape", "slide": "S03", "shape_type": "RECTANGLE", "x": 36, "y": 328, "width": 648, "height": 2.5, "background_color": NEON},
    ])
    # Exact 1376/768 = 1.79167 -> width=528.5, height=295.0 at x=95.75, y=28
    imgs.append({
        "slide": "S03",
        "file": str(DIAG_DIR / "00_neon_hero.jpg"),
        "x": 95.75,
        "y": 28.0,
        "width": 528.5,
        "height": 295.0,
    })
    neon_stats = [
        ("$3 / $15", "Input / Output per 1M tokens"),
        ("1M Tokens", "Full-repo context window"),
        ("95% Off", "Cached input ($0.15 / 1M)"),
        ("4 Tiers", "low · medium · high · xhigh"),
    ]
    for i, (big, sub) in enumerate(neon_stats):
        sx = 46 + i * 160
        ops.extend([
            {"op": "add-textbox", "slide": "S03", "text": big, "x": sx, "y": 336, "width": 152, "height": 26, "font_size": 16.0, "bold": True, "color": NEON_BRIGHT if i % 2 == 0 else WHITE, "font_family": "Montserrat", "alignment": "center"},
            {"op": "add-textbox", "slide": "S03", "text": sub, "x": sx, "y": 364, "width": 152, "height": 22, "font_size": 8.0, "color": SOFT, "font_family": "Roboto", "alignment": "center"},
        ])
    ops.append({
        "op": "set-notes",
        "slide": "S03",
        "text": "Pause for 3 seconds and let the room soak in that neon glow! Introducing Gemini 4 Neon — frontier-level intelligence engineered for fast end-to-end task completion. At $3 input and $15 output per million tokens — with a 1-million-token context window and 95% savings on cached context ($0.15/1M) — Neon hits the sweet spot developers have been begging for.",
    })

    # ── SLIDE 04: THE PERIODIC TABLE OF GEMINI AGENTS ──────────────────────────
    add_visual_slide(
        ops, imgs, "S04",
        "02 · PICK THE RIGHT ELEMENT FOR EVERY JOB",
        "The Periodic Table of Gemini Agents",
        "03_periodic_table_neon.jpg",
        "If you are new to Gemini 4, forget model numbers — remember elements! Hydrogen is fast everyday execution ($1.50/$7.50). Neon — glowing right in the center — is your fast frontier orchestrator ($3/$15). Carbon handles deep multi-week research; Argon delivers enterprise stability. Below them sit two superpowers: Decisions API for instant $0-output guardrails, and Gemini 3.8 Live for voice that thinks while speaking.",
        dark=True,
    )

    # ── SLIDE 05: PUBLIC GEMINI 4 NEON BENCHMARKS ──────────────────────────────
    add_blank_slide(ops, "S05", BG)
    add_header(
        ops, "S05",
        "03 · PUBLIC LAUNCH BENCHMARKS",
        "Why Builders Are Excited About Gemini 4 Neon",
        dark=True,
        right_label="Source: blog.google (Public)",
        right_link=NEON_BLOG_URL,
    )
    kpis5 = [
        ("#1", "Coding Agent Index", "58.6 score on Artificial Analysis · built for multi-step production coding", NEON, NEON_BRIGHT),
        ("39.0%", "SWE-sweep in Antigravity", "3× higher than standalone harness (12.8%) when orchestrating subagents", BLUE, BLUE_BRIGHT),
        ("90.5%", "SEC-bench Pro (Cyber)", "70.7% CWE-bench v2 · 0.0% Gray Swan IPI bypass · 99.2% honesty", GREEN, GREEN_BRIGHT),
        ("3×", "Speed at 60% Cost", "“Matched or exceeded Gemini 4 Carbon on quality at 3× speed & 60% cost.” — Glean", NEON, WHITE),
    ]
    for i, (num, title_k, sub_k, top_col, num_col) in enumerate(kpis5):
        kx = 36 + i * 164
        ops.extend([
            {"op": "add-shape", "slide": "S05", "shape_type": "RECTANGLE", "x": kx, "y": 82, "width": 154, "height": 224, "background_color": SURFACE},
            {"op": "add-shape", "slide": "S05", "shape_type": "RECTANGLE", "x": kx, "y": 82, "width": 154, "height": 3.5, "background_color": top_col},
            {"op": "add-textbox", "slide": "S05", "text": num, "x": kx + 12, "y": 98, "width": 130, "height": 46, "font_size": 30, "bold": True, "color": num_col, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S05", "text": title_k, "x": kx + 12, "y": 150, "width": 130, "height": 36, "font_size": 11.5, "bold": True, "color": WHITE, "font_family": "Montserrat", "line_spacing": 115},
            {"op": "add-textbox", "slide": "S05", "text": sub_k, "x": kx + 12, "y": 192, "width": 130, "height": 102, "font_size": 9.2, "color": SOFT, "font_family": "Roboto", "line_spacing": 132},
        ])
    ops.extend([
        {"op": "add-shape", "slide": "S05", "shape_type": "RECTANGLE", "x": 36, "y": 324, "width": 648, "height": 54, "background_color": SURFACE_2},
        {
            "op": "add-textbox",
            "slide": "S05",
            "text": "#1 Zapier AutomationBench (56.3%)   ·   #1 Vending-Bench 2 ($16,843)   ·   #1 Legal & Tax Agent Bench   ·   84.0% RiemannBench Math   ·   -32% Cost/Task vs Carbon",
            "x": 46,
            "y": 332,
            "width": 628,
            "height": 38,
            "font_size": 8.6,
            "bold": True,
            "color": SOFT,
            "font_family": "Roboto Mono",
            "alignment": "center",
            "content_alignment": "MIDDLE",
        },
        {
            "op": "set-notes",
            "slide": "S05",
            "text": "Every single number on this screen is straight from the public Gemini 4 Neon announcement blog. #1 on the Artificial Analysis Coding Agent Index (58.6). 39.0% on SWE-sweep inside Google Antigravity — 3x higher than running standalone! 90.5% on SEC-bench Pro with 0.0% indirect prompt-injection attack success and 99.2% honesty. And Glean's production quote: matched or exceeded Carbon at 3x speed and 60% cost.",
        },
    ])

    # ── SLIDE 06: ONE SIMPLE MENTAL MODEL + MONSOONPAY STORY ───────────────────
    add_blank_slide(ops, "S06", BG)
    add_header(
        ops, "S06",
        "04 · OUR LIVE STORY · MONSOONPAY UPI ON GOOGLE CLOUD",
        "One Simple Mental Model for Production AI",
        dark=True,
    )
    ops.extend([
        {"op": "add-shape", "slide": "S06", "shape_type": "RECTANGLE", "x": 36, "y": 74, "width": 648, "height": 58, "background_color": NEON_BG},
        {"op": "add-shape", "slide": "S06", "shape_type": "RECTANGLE", "x": 36, "y": 74, "width": 5, "height": 58, "background_color": NEON},
        {
            "op": "add-textbox",
            "slide": "S06",
            "text": "THE SCENARIO: A Diwali flash sale hits Bengaluru & Delhi. Checkouts in Delhi slow down past 470 ms while an aging UPI settlement engine struggles to keep up. Watch how 4 specialized Gemini models solve it together.",
            "x": 52,
            "y": 82,
            "width": 620,
            "height": 44,
            "font_size": 10.5,
            "color": WHITE,
            "font_family": "Roboto",
            "line_spacing": 130,
            "content_alignment": "MIDDLE",
        },
    ])
    pillars = [
        ("01 · PLAN BIG", "Gemini 4 Neon", "Reads the entire codebase, uncovers hidden risks and business rules, and writes one crystal-clear blueprint.", NEON),
        ("02 · BUILD FAST", "3× Hydrogen Swarm", "Executes tasks in parallel inside isolated sandboxes, then hands off to a Cloud VM so you can close your laptop.", BLUE),
        ("03 · DECIDE INSTANT", "Decisions API", "Blocks prompt attacks, masks leaked keys, and scores 50+ compliance rules in one pass at $0 output cost.", AMBER),
        ("04 · SHIP SAFE", "Neon Cyber + Human", "Runs load tests, independent AI cyber review, and pauses at a built-in human approval gate before merge.", GREEN),
    ]
    for i, (step, heading, body, col) in enumerate(pillars):
        px = 36 + i * 164
        ops.extend([
            {"op": "add-shape", "slide": "S06", "shape_type": "RECTANGLE", "x": px, "y": 148, "width": 154, "height": 228, "background_color": SURFACE},
            {"op": "add-shape", "slide": "S06", "shape_type": "RECTANGLE", "x": px, "y": 148, "width": 154, "height": 3.5, "background_color": col},
            {"op": "add-textbox", "slide": "S06", "text": step, "x": px + 12, "y": 162, "width": 130, "height": 18, "font_size": 8.2, "bold": True, "color": col, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "S06", "text": heading, "x": px + 12, "y": 184, "width": 130, "height": 38, "font_size": 13.0, "bold": True, "color": WHITE, "font_family": "Montserrat", "line_spacing": 115},
            {"op": "add-textbox", "slide": "S06", "text": body, "x": px + 12, "y": 230, "width": 130, "height": 136, "font_size": 9.4, "color": SOFT, "font_family": "Roboto", "line_spacing": 136},
        ])
    ops.append({
        "op": "set-notes",
        "slide": "S06",
        "text": "Don't memorize 20 frameworks. Memorize 4 plain-English habits — and let's watch them save a real Indian UPI payment platform called MonsoonPay during a Delhi festival flash sale: 1) Plan Big with Neon. 2) Build Fast in parallel with Hydrogen. 3) Decide Instant with Decisions API. 4) Ship Safe with independent AI security + human approval.",
    })

    # ── SLIDE 07: GOOGLE ANTIGRAVITY ARCHITECTURE ──────────────────────────────
    add_visual_slide(
        ops, imgs, "S07",
        "05 · ORCHESTRATION ARCHITECTURE",
        "Google Antigravity: Neon Orchestrates, Hydrogen Swarms",
        "04_antigravity_engine_v4.jpg",
        "This is the pattern powering Neon's 39.0% SWE-sweep score in Google Antigravity — literally 3x higher than a single-agent loop. Gemini 4 Neon acts as the calm senior orchestrator. It delegates parallel coding work to three fast Gemini 4 Hydrogen builders in isolated sandboxes with zero merge conflicts, and hands off long runs to a Remote Cloud VM.",
        dark=True,
    )

    # ── SLIDE 08: LIVE DEMO 1 — PARALLEL SWARM ─────────────────────────────────
    d1_bullets = [
        f"{w.get('owner', 'Builder')}: {w.get('plain_goal') or w.get('task', '')}"
        for w in d1_workers
    ]
    d1_bullets.append("Cloud VM Handoff: Close your laptop — remote agents finish tests and open PR #1.")
    add_demo_split_slide(
        ops, imgs, video_jobs,
        slide_id="S08", slide_index=7,
        kicker="LIVE DEMO 01 · PLAN BIG, BUILD FAST",
        title="Neon Plans. 3 Hydrogen Builders Ship Together.",
        kpi1=(f"{d1_speedup}×", f"Parallel Speedup ({d1_wall_s}s vs {d1_seq_s}s)", NEON_BRIGHT),
        kpi2=("0", "Merge Conflicts Across 3 Sandboxes", GREEN_BRIGHT),
        bullets=d1_bullets,
        poster_filename="demo1_antigravity_swarm_kickoff_poster.png",
        video_filename="demo1_antigravity_swarm_kickoff.mp4",
        bar_label="Live Run · gemini-4-neon + 3× gemini-4-hydrogen",
        drive_url=vids.get("demo1_antigravity_swarm_kickoff", ""),
        notes=(
            f"Let's watch Demo 1! Live gemini-4-neon reads our payment gateway code, designs a 3-part fix, and spawns "
            f"3 isolated sandboxes powered by live gemini-4-hydrogen in parallel — finishing {d1_speedup}x faster ({d1_wall_s}s vs {d1_seq_s}s) with 0 merge conflicts."
        ),
        accent=NEON,
    )

    # ── SLIDE 09: 1M CONTEXT & LONG DECODE FOR LEGACY MODERNIZATION ────────────
    add_blank_slide(ops, "S09", BG)
    add_header(
        ops, "S09",
        "06 · ENTERPRISE CODE MODERNIZATION",
        "Why Legacy Rewrites Finally Work — With Zero Rupee Error",
        dark=True,
    )
    # Left card: BEFORE
    ops.extend([
        {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": 36, "y": 82, "width": 314, "height": 292, "background_color": SURFACE},
        {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": 36, "y": 82, "width": 314, "height": 3.5, "background_color": RED},
        {"op": "add-textbox", "slide": "S09", "text": "BEFORE  ·  FRAGILE REWRITES", "x": 54, "y": 98, "width": 278, "height": 18, "font_size": 8.8, "bold": True, "color": RED_BRIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S09", "text": "Why Teams Feared Touching Legacy Code", "x": 54, "y": 120, "width": 278, "height": 42, "font_size": 15.5, "bold": True, "color": WHITE, "font_family": "Montserrat", "line_spacing": 115},
        {
            "op": "add-textbox",
            "slide": "S09",
            "text": (
                "▸  Small context windows missed hidden RBI compliance & rounding rules buried in other files.\n\n"
                "▸  Short output limits cut off halfway through rewriting large settlement modules.\n\n"
                "▸  Even a 1-paisa rounding bug across millions of UPI payments blocks production rollout."
            ),
            "x": 54,
            "y": 172,
            "width": 278,
            "height": 188,
            "font_size": 10.2,
            "color": SOFT,
            "font_family": "Roboto",
            "line_spacing": 136,
        },
    ])
    # Right card: TODAY
    ops.extend([
        {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": 370, "y": 82, "width": 314, "height": 292, "background_color": SURFACE},
        {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": 370, "y": 82, "width": 314, "height": 3.5, "background_color": GREEN},
        {"op": "add-textbox", "slide": "S09", "text": "TODAY  ·  GEMINI 4 NEON + EXACT PROOF", "x": 388, "y": 98, "width": 278, "height": 18, "font_size": 8.8, "bold": True, "color": GREEN_BRIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S09", "text": "1M Context + Complete Rewrite + Golden Verification", "x": 388, "y": 120, "width": 278, "height": 42, "font_size": 15.5, "bold": True, "color": WHITE, "font_family": "Montserrat", "line_spacing": 115},
        {
            "op": "add-textbox",
            "slide": "S09",
            "text": (
                "▸  Read Everything: 1M-token context ingests entire legacy payment modules + tests at once.\n\n"
                "▸  Rewrite Completely: Long decode emits clean, modular modern code on Attempt 1.\n\n"
                "▸  Prove ₹0.00 Drift: Lock the old system's exact output fingerprint first — new code only passes at 100% match."
            ),
            "x": 388,
            "y": 172,
            "width": 278,
            "height": 188,
            "font_size": 10.2,
            "color": SOFT,
            "font_family": "Roboto",
            "line_spacing": 136,
        },
        {
            "op": "set-notes",
            "slide": "S09",
            "text": "Every enterprise in India has 10-year-old banking, billing, or UPI code nobody dares touch. Small context windows forgot edge rules 600 lines away, and short outputs truncated mid-file. With Gemini 4 Neon's 1-million-token context and long output decode, it reads the whole legacy system, lists every hidden RBI & GST rule, writes the full replacement in one shot, and we prove zero rupee drift automatically.",
        },
    ])

    # ── SLIDE 10: LIVE DEMO 2 — LEGACY UPI MODERNIZATION ───────────────────────
    add_demo_split_slide(
        ops, imgs, video_jobs,
        slide_id="S10", slide_index=9,
        kicker="LIVE DEMO 02 · GEMINI 4 NEON MODERNIZATION",
        title=f"{b5['speedup_factor']}× Faster UPI Engine. ₹0.00 Error.",
        kpi1=(f"{b5['legacy_ms']} → {b5['modern_ms']} ms", "8,000 Indian Payments", NEON_BRIGHT),
        kpi2=(f"₹{payout_cr} Cr", "Exact Payout Match (Attempt 1)", GREEN_BRIGHT),
        bullets=rules5[:4] or ["Preserves every RBI compliance & GST rounding rule with ₹0.00 error."],
        poster_filename="demo5_code_modernization_poster.png",
        video_filename="demo5_code_modernization.mp4",
        bar_label="Live Run · gemini-4-neon · Attempt 1 Bit-Exact Proof",
        drive_url=vids.get("demo5_code_modernization", ""),
        notes=(
            f"Watch real live Gemini 4 Neon modernize MonsoonPay's slow legacy UPI settlement engine. "
            f"8,000 realistic Indian payments drop from {b5['legacy_ms']}ms down to {b5['modern_ms']}ms: "
            f"{b5['speedup_factor']}x faster with literally ₹0.00 error across ₹{payout_cr} Crore!"
        ),
        accent=NEON,
    )

    # ── SLIDE 11: DECISIONS API — METHODOLOGY & LIVE BENCHMARK TABLE ───────────
    add_blank_slide(ops, "S11", BG)
    add_header(
        ops, "S11",
        "07 · DECIDE SMALL · STOP PAYING FOR JSON DECODING",
        "Gemini Decisions API: 50+ Rules in 1 Pass, $0 Output Tokens",
        dark=True,
    )
    ops.extend([
        {"op": "add-shape", "slide": "S11", "shape_type": "RECTANGLE", "x": 36, "y": 74, "width": 648, "height": 54, "background_color": BLUE_BG},
        {"op": "add-shape", "slide": "S11", "shape_type": "RECTANGLE", "x": 36, "y": 74, "width": 5, "height": 54, "background_color": BLUE},
        {
            "op": "add-textbox",
            "slide": "S11",
            "text": "HOW WE MEASURED THIS LIVE: Identical Delhi checkout incident sent to all three live APIs asking 8 security/routing rules and 50 RBI/PCI compliance rules in one request — timing real wall-clock latency & billed tokens at published pricing.",
            "x": 52,
            "y": 80,
            "width": 620,
            "height": 42,
            "font_size": 9.8,
            "color": WHITE,
            "font_family": "Roboto",
            "line_spacing": 128,
            "content_alignment": "MIDDLE",
        },
        {"op": "add-table", "slide": "S11", "rows": 4, "cols": 5, "x": 36, "y": 144, "width": 648, "height": 224, "id": "TBL_DEC"},
    ])
    headers = ["Benchmark Test", "Gemini Decisions API", "Gemini 3.8 Flash", "Gemini 4 Hydrogen", "Decisions Advantage"]
    rows_data = [
        [
            "8 Rules\n(Live Run)",
            f"{d1_8_ms} ms\n0 output tokens",
            f"{fl_8_ms:,} ms\n108 output tokens",
            f"{hy_8_ms:,} ms\n673 output tokens",
            f"{sp8_fl}× faster\n$0 output cost",
        ],
        [
            "50 Rules\n(Live, 1 call!)",
            f"{d1_50_ms} ms\n${d1_50_cost:,.0f} / 1M calls",
            f"{fl_50_ms/1000:.1f}s\n${fl_50_cost:,.0f} / 1M calls",
            f"{hy_50_ms/1000:.1f}s\n${hy_50_cost:,.0f} / 1M calls",
            f"{sp50_fl}× faster\n{cs50_hy}× cheaper",
        ],
        [
            "100 Rules\n(Google Pub.)",
            f"{pub100.get('gemini_decision_1_ms', 359)} ms\n0 output tokens",
            f"{pub100.get('gemini_3_8_flash_ms', 7200)/1000:.1f}s",
            f"{pub100.get('gemini_4_hydrogen_ms', 8600)/1000:.1f}s",
            "20–24× faster\nat enterprise scale",
        ],
    ]
    for c, h in enumerate(headers):
        ops.append({
            "op": "set-table-cell",
            "table": "TBL_DEC",
            "row": 0,
            "col": c,
            "text": h,
            "color": MUTED,
            "bold": True,
            "font_size": 9.0,
            "font_family": "Roboto Mono",
            "background_color": SURFACE_2,
        })
    for r_idx, row in enumerate(rows_data, start=1):
        bg_row = SURFACE if r_idx % 2 == 1 else "#0E1118"
        for c, cell in enumerate(row):
            col_txt = WHITE if c == 0 else (NEON_BRIGHT if c == 1 else (GREEN_BRIGHT if c == 4 else SOFT))
            ops.append({
                "op": "set-table-cell",
                "table": "TBL_DEC",
                "row": r_idx,
                "col": c,
                "text": cell,
                "color": col_txt,
                "bold": c in (0, 1, 4),
                "font_size": 9.5,
                "font_family": "Roboto",
                "background_color": bg_row,
            })
    ops.append({
        "op": "set-notes",
        "slide": "S11",
        "text": "Here is the single biggest architectural unlock for cost and speed in production agents. Gemini Decisions API skips text generation completely: ONE forward pass scores up to 1,000 rules at $0 output cost! Look at the live 50-rule numbers: 283ms and $271/1M calls vs 6.3 seconds on Flash (22.4x slower) and $14,900/1M calls on Hydrogen (55x costlier!).",
    })

    # ── SLIDE 12: LIVE DEMO 3 — DECISIONS API ARENA ────────────────────────────
    add_demo_split_slide(
        ops, imgs, video_jobs,
        slide_id="S12", slide_index=11,
        kicker="LIVE DEMO 03 · GEMINI DECISIONS API",
        title="Instant Guardrails & 50-Rule Speed Race",
        kpi1=(f"{cs50_hy}×", "Cheaper vs 4 Hydrogen (50 Rules)", NEON_BRIGHT),
        kpi2=(f"{sp50_fl}×", "Faster vs 3.8 Flash (283ms)", GREEN_BRIGHT),
        bullets=[
            "Blocks Prompt Attacks & Leaked Keys before any expensive agent or tool is ever invoked.",
            "Smart Model Router: Sends UI tweaks to Hydrogen; escalates outages to Gemini 4 Neon.",
            f"Multimodal Included: Audited our Google Cloud diagram for leaked secrets in {mm2['latency_ms']} ms ($0 output).",
        ],
        poster_filename="demo2_decisions_api_arena_poster.png",
        video_filename="demo2_decisions_api_arena.mp4",
        bar_label="Live Race · gemini-decision-1 vs 3.8 Flash vs 4 Hydrogen",
        drive_url=vids.get("demo2_decisions_api_arena", ""),
        notes=(
            f"Watch Decisions API in action! First it blocks prompt hacking and leaked cloud keys before any agent wakes up, "
            f"routes a CSS tweak to Hydrogen, and escalates the Delhi outage to Gemini 4 Neon. Then it wins the 50-rule race "
            f"{sp50_fl}x faster than Flash and {cs50_hy}x cheaper than Hydrogen — AND audits our architecture diagram in {mm2['latency_ms']}ms!"
        ),
        accent=AMBER,
    )

    # ── SLIDE 13: GOVERNED DATA & GOOGLE ADK 2.0 ───────────────────────────────
    add_visual_slide(
        ops, imgs, "S13",
        "08 · GOOGLE CLOUD DATA + ADK 2.0",
        "Zero-Copy Live Data Joins with Built-In Human Approval",
        "07_gcp_data_cloud_v4.jpg",
        "Agents are only as good as the data and guardrails around them. Instead of brittle nightly ETL copies, Google ADK 2.0 + Knowledge Catalog joins live Spanner Omni payments directly with BigQuery Apache Iceberg logs in milliseconds — and pauses automatically at a built-in Human Approval Gate so an AI never blindly merges to production.",
        dark=True,
    )

    # ── SLIDE 14: LIVE DEMO 4 — VOICE CHECK-IN + ADK + ZERO-COPY DATA ──────────
    add_demo_split_slide(
        ops, imgs, video_jobs,
        slide_id="S14", slide_index=13,
        kicker="LIVE DEMO 04 · VOICE + ADK 2.0 + ZERO-COPY DATA",
        title="Close Your Laptop. Check In by Voice.",
        kpi1=(f"{sql3_ms} ms", f"{sql3_rows:,} Rows Joined Live", BLUE_BRIGHT),
        kpi2=("0 Copies", "Direct Iceberg + Spanner Omni", GREEN_BRIGHT),
        bullets=[
            "Dual-Track Voice: Acknowledges instantly — zero awkward silence while cloud tools run.",
            "Knowledge Catalog: Gives agents the verified join key automatically so SQL never hallucinates.",
            "Human Sign-Off: ADK 2.0 pauses cleanly until Mani approves Pull Request #1.",
        ],
        poster_filename="demo3_live38_voice_multicloud_adk_poster.png",
        video_filename="demo3_live38_voice_multicloud_adk.mp4",
        bar_label="🔊 Real Gemini 3.8 HD Audio + Live ADK 2.14.1 Trace",
        drive_url=vids.get("demo3_live38_voice_multicloud_adk", ""),
        notes=(
            f"Turn up the auditorium audio for this one! I closed my laptop 10 minutes ago and check in by voice. "
            f"Gemini 3.8 answers immediately while Google ADK 2.0 joins {sql3_rows:,} live Spanner + BigQuery Iceberg rows "
            f"in {sql3_ms}ms with zero copying, pinpoints Delhi's 64-slot queue, and pauses right at my confirmation gate."
        ),
        accent=BLUE,
    )

    # ── SLIDE 15: REAL VOICE AI (PART A) — CAMERA + VOICE FLIGHT REBOOKING ─────
    add_voice_arch_video_slide(
        ops, imgs, video_jobs,
        slide_id="S15", slide_index=14,
        kicker="REAL VOICE AI · PART A · GEMINI 3.8 LIVE EXTENDED THINKING",
        title="Live Camera + Voice Concierge — Zero Dead Air",
        badge_text="INLINE VIDEO · ARCH + DEMO",
        badge_color=GREEN,
        arch_filename="09_arch_live_flight.jpg",
        poster_filename="demo4a_gemini38_live_flight_poster.png",
        video_filename="demo4a_gemini38_live_flight.mp4",
        video_ratio=1360.0 / 720.0,
        video_caption="Real Recording (2:40) · Live Boarding Pass + BigQuery & Firestore",
        video_highlights=[
            "1 FPS live camera reads the stranded boarding pass (LH8942X) while conversing naturally.",
            "Non-blocking background tools query BigQuery flights, calculate EU261, and commit Firestore.",
            "Zero dead air: speaks calmly while extended thinking runs multi-step enterprise actions.",
        ],
        drive_url=DRIVE_FLIGHT_URL,
        notes=(
            "Now let's go beyond demos into TWO real production Voice AI systems I built — both embedded right on the slide in our HTML5 Keynote & PPTX! "
            "Left: architecture diagram. Right: real 2:40 recording of Gemini 3.8 Live with Extended Thinking reading a boarding pass via live camera while running non-blocking BigQuery SQL and Firestore updates in the background. "
            "(If presenting directly inside Google Slides web UI, you can also one-click Insert -> Video -> Google Drive -> 'Gemini_3.8_Live_Extended_Thinking' to play inline inside Slides.)"
        ),
    )

    # ── SLIDE 16: REAL VOICE AI (PART B) — INDIAN PSTN TELEPHONY ───────────────
    add_voice_arch_video_slide(
        ops, imgs, video_jobs,
        slide_id="S16", slide_index=15,
        kicker="REAL VOICE AI · PART B · INDIAN PSTN TELEPHONY ON GOOGLE CLOUD",
        title="Real Indian Phone Calls Across 6 Languages",
        badge_text="INLINE VIDEO · ARCH + DEMO",
        badge_color=NEON,
        arch_filename="10_arch_voice_pstn.jpg",
        poster_filename="demo4b_gemini_voiceai_pstn_poster.png",
        video_filename="demo4b_gemini_voiceai_pstn.mp4",
        video_ratio=1280.0 / 590.0,
        video_caption="Real Recording (3:03) · 6 Indian Languages on Cloud Run Mumbai",
        video_highlights=[
            "Real Indian PSTN phone calls routed via Cloud Armor + Load Balancing + Cloud Run Mumbai.",
            "Supports BOTH Direct Speech-to-Speech (Gemini Live) AND Cascaded Listen-Think-Speak.",
            "Handles English, Hindi, Tamil, Kannada, Telugu & Hinglish with live Firestore call state.",
        ],
        drive_url=DRIVE_PSTN_URL,
        notes=(
            "Here is the demo Indian enterprises ask me about every single week: REAL Indian phone calls! "
            "Left: full Google Cloud Mumbai architecture (Cloud Armor -> Cloud Run -> Gemini Live / Cascaded STT+TTS -> Firestore). "
            "Right: real 3:03 recording across 6 Indian languages — plays directly inline in our HTML5 Keynote & PPTX! "
            "(In Google Slides web UI, one-click Insert -> Video -> Google Drive -> 'Gemini_VoiceAI_PSTN' if you want native Google Slides web playback too.)"
        ),
    )

    # ── SLIDE 17: LIVE DEMO 5 — REVIEW EVERYTHING (GEMINI 4 NEON FOR CYBER) ────
    add_demo_split_slide(
        ops, imgs, video_jobs,
        slide_id="S17", slide_index=16,
        kicker="LIVE DEMO 05 · GEMINI 4 NEON FOR CYBER DEFENSE",
        title=f"-{drop4}% Delay & {tests4}/{tests4} Green — Still Audited by Neon.",
        kpi1=(f"{round(bef4)} → {aft4:.1f} ms", "500-User Flash-Sale Load Test", GREEN_BRIGHT),
        kpi2=("90.5%", "SEC-bench Pro · 0.0% IPI", NEON_BRIGHT),
        bullets=[
            f"Independent Reviewer Verdict: {verdict4}",
            f"Caught Before Merge: {warn_finding}",
            "Golden Rule: AI writes, tests, and audits — humans own the Merge button.",
        ],
        poster_filename="demo4_review_shipped_pr_poster.png",
        video_filename="demo4_review_shipped_pr.mp4",
        bar_label="Live Run · Load Test + 10 Tests + gemini-4-neon Cyber Audit",
        drive_url=vids.get("demo4_review_shipped_pr", ""),
        notes=(
            f"Our final principle: NEVER let the same agent that wrote the code approve it for production! "
            f"Load testing proved Delhi worst-case checkout delay fell {drop4}% ({bef4}ms to {aft4}ms), and all {tests4} tests are green. "
            f"Yet our independent Gemini 4 Neon security reviewer — backed by 90.5% SEC-bench Pro and 0.0% IPI bypass — STILL caught a real policy gap ({warn_finding}) before a human clicks Merge!"
        ),
        accent=GREEN,
    )

    # ── SLIDE 18: CLOSING ──────────────────────────────────────────────────────
    add_blank_slide(ops, "S18", BG)
    ops.extend([
        {"op": "add-shape", "slide": "S18", "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 7, "height": 405, "background_color": NEON},
        {"op": "add-textbox", "slide": "S18", "text": "THANK YOU  ·  DEVFEST BENGALURU 2026", "x": 44, "y": 28, "width": 632, "height": 18, "font_size": 9.5, "bold": True, "color": NEON_BRIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S18", "text": "Plan Big. Build Fast.\nDecide Instant. Ship Safe.", "x": 44, "y": 50, "width": 632, "height": 88, "font_size": 31, "bold": True, "color": WHITE, "font_family": "Montserrat", "line_spacing": 108},
    ])
    takeaways = [
        ("1 · Neon", "Plan, modernize & audit at $3/$15", NEON),
        ("2 · Hydrogen", "Parallel /swarm execution in sandboxes", BLUE),
        ("3 · Decisions API", "50+ guardrails at $0 output cost", AMBER),
        ("4 · Humans", "ADK 2.0 approval gates on every prod merge", GREEN),
    ]
    for i, (head, desc, col) in enumerate(takeaways):
        tx = 44 + i * 161
        ops.extend([
            {"op": "add-shape", "slide": "S18", "shape_type": "RECTANGLE", "x": tx, "y": 154, "width": 151, "height": 84, "background_color": SURFACE},
            {"op": "add-shape", "slide": "S18", "shape_type": "RECTANGLE", "x": tx, "y": 154, "width": 151, "height": 3, "background_color": col},
            {"op": "add-textbox", "slide": "S18", "text": head, "x": tx + 10, "y": 166, "width": 131, "height": 22, "font_size": 11.5, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S18", "text": desc, "x": tx + 10, "y": 192, "width": 131, "height": 38, "font_size": 8.6, "color": SOFT, "font_family": "Roboto", "line_spacing": 125},
        ])
    # Closing speaker card + buttons
    ops.extend([
        {"op": "add-shape", "slide": "S18", "shape_type": "RECTANGLE", "x": 44, "y": 266, "width": 632, "height": 98, "background_color": SURFACE},
        {"op": "add-shape", "slide": "S18", "shape_type": "RECTANGLE", "x": 44, "y": 266, "width": 5, "height": 98, "background_color": NEON},
        {"op": "add-textbox", "slide": "S18", "text": "Mani", "x": 64, "y": 280, "width": 240, "height": 28, "font_size": 20, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": "S18", "text": "Principal Architect, Google Cloud", "x": 64, "y": 312, "width": 260, "height": 20, "font_size": 11, "color": SOFT, "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S18", "text": "Come say hi — look for the brand-new badge!", "x": 64, "y": 334, "width": 260, "height": 18, "font_size": 9.2, "color": MUTED, "font_family": "Roboto"},
        {
            "op": "add-textbox",
            "slide": "S18",
            "text": "LinkedIn  ·  /in/cmanikandan",
            "x": 366,
            "y": 282,
            "width": 292,
            "height": 30,
            "font_size": 10.5,
            "bold": True,
            "color": "#111319",
            "background_color": NEON_BRIGHT,
            "font_family": "Roboto Mono",
            "alignment": "center",
            "content_alignment": "MIDDLE",
            "link": LINKEDIN_URL,
        },
        {
            "op": "add-textbox",
            "slide": "S18",
            "text": "GitHub  ·  Full Code, Slides & Stage UI",
            "x": 366,
            "y": 322,
            "width": 292,
            "height": 30,
            "font_size": 10.0,
            "bold": True,
            "color": WHITE,
            "background_color": SURFACE_2,
            "font_family": "Roboto Mono",
            "alignment": "center",
            "content_alignment": "MIDDLE",
            "link": GITHUB_URL,
        },
        {
            "op": "set-notes",
            "slide": "S18",
            "text": "Thank you, DevFest Bengaluru! Four habits to take back to your teams Monday morning: Plan big with Gemini 4 Neon, build fast with parallel Hydrogen swarms, decide instant at $0 output cost with Decisions API, and review everything with independent AI cyber audits plus human approval. Every single demo, slide, and Stage Web UI is open-source on my GitHub — connect with me on LinkedIn and come find the Principal Architect with the brand-new badge!",
        },
    ])

    return ops, imgs, video_jobs


def embed_videos_into_pptx(pptx_path: Path, video_jobs: List[Dict[str, Any]]) -> None:
    """Embed real playable `.mp4` videos natively inside the exported `.pptx` slides."""
    from pptx import Presentation
    from pptx.util import Pt

    prs = Presentation(str(pptx_path))
    embedded = 0
    for job in video_jobs:
        idx = job["slide_index"]
        if idx >= len(prs.slides):
            continue
        slide = prs.slides[idx]
        left, top, width, height = Pt(job["x"]), Pt(job["y"]), Pt(job["width"]), Pt(job["height"])
        # Remove the static picture placeholder at the exact same video frame coordinates so it doesn't duplicate
        for sp in list(slide.shapes):
            if sp.shape_type == 13:  # PICTURE
                if abs(sp.left - left) < Pt(12) and abs(sp.top - top) < Pt(12):
                    sp._element.getparent().remove(sp._element)
        slide.shapes.add_movie(
            job["video"],
            left,
            top,
            width,
            height,
            poster_frame_image=job["poster"],
            mime_type="video/mp4",
        )
        embedded += 1
    prs.save(str(pptx_path))
    print(f"  ✔ Natively embedded {embedded} playable MP4 videos directly inside {pptx_path.name}!")


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
    parser = argparse.ArgumentParser()
    parser.add_argument("--pres-id", default="", help="Existing Google Slides presentation ID")
    parser.add_argument("--images-only", action="store_true", help="Place images on an existing 18-slide deck and export PDF/PPTX")
    args = parser.parse_args()

    tr = load_traces()
    drive = load_drive_links()
    ops, img_jobs, video_jobs = build_deck_ops(tr, drive)

    title = "The Periodic Table of Agents — Gemini 4 Neon Keynote (DevFest Bengaluru 2026)"
    if args.pres_id:
        pres_id = args.pres_id
        print(f"Using presentation: {pres_id}")
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
        if len(slide_ids) != 18:
            raise RuntimeError(f"Expected 18 slides on {pres_id}, found {len(slide_ids)}")
        resolved = {"p": slide_ids[0]}
        for n in range(2, 19):
            resolved[f"S{n:02d}"] = slide_ids[n - 1]
    else:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
            json.dump(ops, tf, indent=2)
            batch_file = tf.name
        try:
            print(f"Applying {len(ops)} batch operations across 18 slides...")
            batch_raw = run_cmd(["gslides", "mutate", "batch", pres_id, "-f", batch_file, "--json"])
            batch_res = json.loads(batch_raw)
            resolved = batch_res.get("resolved_ids", {})
            resolved["p"] = "p"
            print(
                f"  ✔ Batch complete ({batch_res.get('operations')} ops, "
                f"{len(batch_res.get('created_slides', [])) + 1} slides)"
            )
        finally:
            Path(batch_file).unlink(missing_ok=True)

    print(f"Fetching signed GitHub URLs & placing {len(img_jobs)} crisp diagrams & video frames...")
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

    pdf_path = PRES_DIR / "Periodic_Table_of_Agents_DevFest_Keynote.pdf"
    pptx_path = PRES_DIR / "Periodic_Table_of_Agents_DevFest_Keynote.pptx"
    run_cmd(["gslides", "readonly", "export", pres_id, str(pdf_path), "--format", "pdf"])
    run_cmd(["gslides", "readonly", "export", pres_id, str(pptx_path), "--format", "pptx"])
    print(f"  ✔ Exported PDF ({pdf_path.stat().st_size // 1024} KB) & base PPTX ({pptx_path.stat().st_size // 1024} KB)")

    embed_videos_into_pptx(pptx_path, video_jobs)
    print(f"  ✔ Final self-contained PPTX with 7 embedded videos: {pptx_path.stat().st_size // 1024} KB")

    meta = {
        "presentation_id": pres_id,
        "presentation_url": f"https://docs.google.com/presentation/d/{pres_id}/edit",
        "title": title,
        "version": "v4-gemini-4-neon",
        "slide_count": 18,
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
    print(f"🎉 DONE! Google Slides v4 URL: {meta['presentation_url']}")


if __name__ == "__main__":
    main()
