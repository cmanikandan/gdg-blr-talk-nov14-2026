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
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
DIAG_DIR = ROOT / "assets" / "diagrams"
VID_DIR = ROOT / "assets" / "videos"
TRACES_DIR = ROOT / "demos" / "traces"
PRES_DIR = ROOT / "presentation"
DRIVE_META_PATH = PRES_DIR / "drive_videos_v2.json"

LINKEDIN_URL = "https://www.linkedin.com/in/cmanikandan"
GITHUB_URL = "https://github.com/cmanikandan/gdg-blr-talk-nov14-2026"
NEON_BLOG_URL = "https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/"
CELL_BLOG_URL = "https://discuss.google.dev/t/how-to-isolate-multi-tenant-workloads-on-google-cloud-with-cell-based-architecture-and-shuffle-sharding/413515"
CELL_BLOG_SHORT_URL = "https://discuss.google.dev/t/413515"
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


def add_qr_pair_ops(
    ops: List[Dict[str, Any]],
    img_jobs: List[Dict[str, Any]],
    slide_id: str,
    x_start: float,
    y_top: float,
    card_w: float,
    card_h: float,
    qr_size: float,
    gap: float,
) -> None:
    """Adds two crisp scannable QR code cards (LinkedIn + GitHub) with clickable captions."""
    cards = [
        ("SCAN · LINKEDIN", "/in/cmanikandan", NEON, NEON_BRIGHT, "qr_linkedin.png", LINKEDIN_URL),
        ("SCAN · GITHUB", "Code & Stage UI", BLUE, BLUE_BRIGHT, "qr_github.png", GITHUB_URL),
    ]
    title_fs = 7.4 if card_w < 98 else 8.0
    sub_fs = 6.5 if card_w < 98 else 7.0
    for i, (label, sub, accent_bar, label_col, img_name, url) in enumerate(cards):
        cx = round(x_start + i * (card_w + gap), 2)
        qr_x = round(cx + (card_w - qr_size) / 2.0, 2)
        qr_y = round(y_top + 7.5, 2)
        label_y = round(qr_y + qr_size + 2.5, 2)
        sub_y = round(label_y + 12.0, 2)
        ops.extend([
            {
                "op": "add-shape",
                "slide": slide_id,
                "shape_type": "RECTANGLE",
                "x": cx,
                "y": y_top,
                "width": card_w,
                "height": card_h,
                "background_color": SURFACE_2,
            },
            {
                "op": "add-shape",
                "slide": slide_id,
                "shape_type": "RECTANGLE",
                "x": cx,
                "y": y_top,
                "width": card_w,
                "height": 2.5,
                "background_color": accent_bar,
            },
            {
                "op": "add-textbox",
                "slide": slide_id,
                "text": label,
                "x": cx + 2,
                "y": label_y,
                "width": card_w - 4,
                "height": 13,
                "font_size": title_fs,
                "bold": True,
                "color": label_col,
                "font_family": "Roboto Mono",
                "alignment": "center",
                "link": url,
            },
            {
                "op": "add-textbox",
                "slide": slide_id,
                "text": sub,
                "x": cx + 2,
                "y": sub_y,
                "width": card_w - 4,
                "height": 12,
                "font_size": sub_fs,
                "color": MUTED,
                "font_family": "Roboto",
                "alignment": "center",
                "link": url,
            },
        ])
        img_jobs.append({
            "slide": slide_id,
            "file": str(DIAG_DIR / img_name),
            "x": qr_x,
            "y": qr_y,
            "width": qr_size,
            "height": qr_size,
        })


def add_qr_trio_ops(
    ops: List[Dict[str, Any]],
    img_jobs: List[Dict[str, Any]],
    slide_id: str,
    x_start: float,
    y_top: float,
    card_w: float,
    card_h: float,
    qr_size: float,
    gap: float,
) -> None:
    """Adds three matched scannable QR cards (LinkedIn + GitHub + Cell-Based Blog) for Slide 20 Closing."""
    cards = [
        ("LINKEDIN", "/in/cmanikandan", NEON, NEON_BRIGHT, "qr_linkedin.png", LINKEDIN_URL),
        ("GITHUB REPO", "Demos & Offline PPTX", BLUE, BLUE_BRIGHT, "qr_github.png", GITHUB_URL),
        ("CELL BLOG", "discuss.google.dev", GREEN, GREEN_BRIGHT, "qr_cell_blog.png", CELL_BLOG_URL),
    ]
    for i, (label, sub, accent_bar, label_col, img_name, url) in enumerate(cards):
        cx = round(x_start + i * (card_w + gap), 2)
        qr_x = round(cx + (card_w - qr_size) / 2.0, 2)
        qr_y = round(y_top + 7.5, 2)
        label_y = round(qr_y + qr_size + 3.0, 2)
        sub_y = round(label_y + 12.5, 2)
        ops.extend([
            {
                "op": "add-shape",
                "slide": slide_id,
                "shape_type": "RECTANGLE",
                "x": cx,
                "y": y_top,
                "width": card_w,
                "height": card_h,
                "background_color": SURFACE_2,
            },
            {
                "op": "add-shape",
                "slide": slide_id,
                "shape_type": "RECTANGLE",
                "x": cx,
                "y": y_top,
                "width": card_w,
                "height": 2.5,
                "background_color": accent_bar,
            },
            {
                "op": "add-textbox",
                "slide": slide_id,
                "text": label,
                "x": cx + 2,
                "y": label_y,
                "width": card_w - 4,
                "height": 13,
                "font_size": 7.8,
                "bold": True,
                "color": label_col,
                "font_family": "Roboto Mono",
                "alignment": "center",
                "link": url,
            },
            {
                "op": "add-textbox",
                "slide": slide_id,
                "text": sub,
                "x": cx + 2,
                "y": sub_y,
                "width": card_w - 4,
                "height": 12,
                "font_size": 6.6,
                "color": MUTED,
                "font_family": "Roboto",
                "alignment": "center",
                "link": url,
            },
        ])
        img_jobs.append({
            "slide": slide_id,
            "file": str(DIAG_DIR / img_name),
            "x": qr_x,
            "y": qr_y,
            "width": qr_size,
            "height": qr_size,
        })


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
        "text": "Offline-ready: Click video to play natively inside PPTX & HTML5 Keynote (zero internet needed)",
        "x": 320,
        "y": 340,
        "width": 368,
        "height": 22,
        "font_size": 7.6,
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
    gf5 = d5.get("golden_falsifier", {"total_net_payout_paise": 5623206619, "sha256_parity_digest": "93a9313ee3d5e807"})
    payout_cr = f"{gf5.get('total_net_payout_paise', 5623206619) / 100 / 1e7:.2f}"
    sha5_short = str(gf5.get("sha256_parity_digest", "93a9313ee3d5"))[:12]
    rules5 = (d5.get("neon_analysis") or d5.get("carbon_analysis") or {}).get("plan", {}).get("hidden_invariants", [])[:5]

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

    # Demo 3 / Use Case 4 metrics
    sql3 = d3.get("lakehouse_finding") or d3["multicloud_finding"]
    sql3_ms = int(round(sql3["query_latency_ms"]))
    sql3_rows = int(sql3["rows_correlated"])
    reg3 = sql3.get("regional_breakdown") or [
        {"cloud_region": "gcp:asia-south2", "p99_commit_ms": 431.8, "total_sync_retries": 18006, "envoy_pool_limit": 64, "avg_truetime_drift_ms": 2.75},
        {"cloud_region": "gcp:asia-south1", "p99_commit_ms": 16.1, "total_sync_retries": 0, "envoy_pool_limit": 64, "avg_truetime_drift_ms": 2.75},
    ]
    delhi3 = next((r for r in reg3 if "south2" in r.get("cloud_region", "")), reg3[0])
    mumbai3 = next((r for r in reg3 if "south1" in r.get("cloud_region", "")), reg3[-1])

    # Demo 4 / Slide 17 Neon Cyber Screening metrics
    sla4 = d4["sla_benchmark"]
    bef4, aft4, drop4 = sla4["before"]["p99_ms"], sla4["after"]["p99_ms"], sla4["p99_reduction_pct"]
    tests4 = d4["pytest"]["passed_count"]
    audit4 = (d4.get("neon_security_audit") or d4.get("carbon_security_audit") or {}).get("audit", {})
    verdict4 = str(audit4.get("overall_verdict", "APPROVE_WITH_NOTE")).replace("_", " ")
    raw_checks4 = audit4.get("checks", [])
    check_titles = [
        "Prompt-Attack & Approval Safety",
        "API Key & Secret Protection",
        "TrueTime Clock & Data Safety",
        "Circuit Breaker Overload Shedding",
    ]
    checks4 = []
    for idx_c, title_c in enumerate(check_titles):
        src_c = raw_checks4[idx_c] if idx_c < len(raw_checks4) else {}
        checks4.append({
            "title": src_c.get("category") or title_c,
            "status": str(src_c.get("status", "PASS")).upper(),
            "finding": src_c.get("finding", "Verified clean against production security controls."),
        })
    warn_checks = [c for c in checks4 if c["status"] != "PASS"]
    warn_finding = warn_checks[0]["finding"] if warn_checks else "Catches subtle approval gaps before merge."

    ops: List[Dict[str, Any]] = []
    imgs: List[Dict[str, Any]] = []
    video_jobs: List[Dict[str, Any]] = []

    # ── SLIDE 01 (`p`): COVER ──────────────────────────────────────────────────
    add_blank_slide(ops, "p", BG, is_first=True)
    ops.extend([
        {"op": "add-shape", "slide": "p", "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 7, "height": 405, "background_color": NEON},
        {"op": "add-textbox", "slide": "p", "text": "DEVFEST BENGALURU 2026  ·  KEYNOTE", "x": 44, "y": 28, "width": 430, "height": 18, "font_size": 9.5, "bold": True, "color": NEON_BRIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "p", "text": "The Periodic Table\nof Agents", "x": 44, "y": 50, "width": 430, "height": 94, "font_size": 36, "bold": True, "color": WHITE, "font_family": "Montserrat", "line_spacing": 106},
        {"op": "add-textbox", "slide": "p", "text": "Building Production AI Systems with Gemini 4 Neon & Google Antigravity", "x": 44, "y": 146, "width": 632, "height": 26, "font_size": 13.5, "color": SOFT, "font_family": "Roboto"},
    ])
    add_qr_pair_ops(ops, imgs, "p", x_start=482.0, y_top=22.0, card_w=92.0, card_h=112.0, qr_size=74.0, gap=10.0)
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

    # ── SLIDE 09: 1M CONTEXT, LONG DECODE & BIT-EXACT PROOF ────────────────────
    add_blank_slide(ops, "S09", BG)
    add_header(
        ops, "S09",
        "06 · ENTERPRISE CODE MODERNIZATION",
        "1M Context, Long Decode & Bit-Exact Proof (₹0.00 Drift)",
        dark=True,
    )
    ops.extend([
        {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": 36, "y": 68, "width": 648, "height": 48, "background_color": RED_BG},
        {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": 36, "y": 68, "width": 5, "height": 48, "background_color": RED},
        {
            "op": "add-textbox",
            "slide": "S09",
            "text": "WHY LEGACY REWRITES FAILED BEFORE: Small context windows missed RBI rules 600 lines away · Short outputs truncated mid-file · Python's default round(2.5) == 2 (Banker's rounding) causes 1-paisa GST drift across millions of UPI txns!",
            "x": 50,
            "y": 72,
            "width": 624,
            "height": 40,
            "font_size": 9.1,
            "color": WHITE,
            "font_family": "Roboto",
            "line_spacing": 126,
            "content_alignment": "MIDDLE",
        },
    ])
    mod_steps = [
        (
            "STEP 1 · GOLDEN FALSIFIER",
            "Lock Legacy SHA-256 First",
            (
                f"▸  BEFORE AI touches a line, run the ugly legacy engine on 8,000 realistic Indian UPI payments.\n\n"
                f"▸  Freeze its exact total payout (₹{payout_cr} Cr) & cryptographic fingerprint (SHA-256: {sha5_short}…) as an immutable test oracle."
            ),
            AMBER,
            AMBER_BRIGHT,
        ),
        (
            "STEP 2 · 1M CONTEXT + LONG DECODE",
            "Neon Discovers & Rewrites",
            (
                "▸  1M-token context reads the entire payment module + tests at once (7.1 s).\n\n"
                "▸  Uncovers all 5 undocumented rules (duplicates, reversals, ₹0 MDR ≤ ₹2k, RBI ≥ ₹50k, half-up paise GST) and emits the full modern engine on Attempt 1."
            ),
            NEON,
            NEON_BRIGHT,
        ),
        (
            "STEP 3 · BIT-EXACT CI GATE",
            "Prove ₹0.00 Financial Drift",
            (
                f"▸  CI replays the exact same 8,000 UPI payments through Neon's new engine.\n\n"
                f"▸  Even a 1-paisa mismatch fails the build — passes ONLY at 100.000% SHA-256 bit-exact parity ({b5['speedup_factor']}× faster!)."
            ),
            GREEN,
            GREEN_BRIGHT,
        ),
    ]
    for i, (k_step, h_step, body_step, bar_c, lbl_c) in enumerate(mod_steps):
        mx = 36 + i * 221
        ops.extend([
            {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": mx, "y": 130, "width": 206, "height": 254, "background_color": SURFACE},
            {"op": "add-shape", "slide": "S09", "shape_type": "RECTANGLE", "x": mx, "y": 130, "width": 206, "height": 3.5, "background_color": bar_c},
            {"op": "add-textbox", "slide": "S09", "text": k_step, "x": mx + 12, "y": 144, "width": 182, "height": 16, "font_size": 7.8, "bold": True, "color": lbl_c, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "S09", "text": h_step, "x": mx + 12, "y": 164, "width": 182, "height": 34, "font_size": 12.8, "bold": True, "color": WHITE, "font_family": "Montserrat", "line_spacing": 115},
            {"op": "add-textbox", "slide": "S09", "text": body_step, "x": mx + 12, "y": 204, "width": 182, "height": 170, "font_size": 9.1, "color": SOFT, "font_family": "Roboto", "line_spacing": 132},
        ])
    ops.append({"op": "set-notes", "slide": "S09", "text": ""})

    # ── SLIDE 10: LIVE DEMO 2 — LEGACY UPI MODERNIZATION ───────────────────────
    add_demo_split_slide(
        ops, imgs, video_jobs,
        slide_id="S10", slide_index=9,
        kicker="LIVE DEMO 02 · GEMINI 4 NEON MODERNIZATION",
        title=f"{b5['speedup_factor']}× Faster UPI Engine. ₹0.00 Error.",
        kpi1=(f"{round(b5['legacy_ms'])} → {b5['modern_ms']:.1f} ms", "8,000 Indian UPI Payments", NEON_BRIGHT),
        kpi2=("₹0.00 Drift", f"SHA-256 {sha5_short}… · ₹{payout_cr} Cr", GREEN_BRIGHT),
        bullets=[
            "5 Hidden Rules Found (7.1 s): Duplicate UTR skip, reversals, ₹0 MDR ≤ ₹2k, RBI ≥ ₹50k & 18% GST half-up.",
            "Caught Banker's Rounding Bug: Avoided Python round(2.5) → 2 trap on Attempt 1!",
            f"Bit-Exact Proof: Legacy vs Neon SHA-256 output hash matches 100.000% across ₹{payout_cr} Cr.",
        ],
        poster_filename="demo5_code_modernization_poster.png",
        video_filename="demo5_code_modernization.mp4",
        bar_label="Embedded Offline · Live gemini-4-neon Rewrite + SHA-256 Proof",
        drive_url=vids.get("demo5_code_modernization", ""),
        notes="",
        accent=NEON,
    )

    # ── SLIDE 11: DECISIONS API — HOW IT WORKS + ACTUAL RULE SNIPPET + TABLE ───
    add_blank_slide(ops, "S11", BG)
    add_header(
        ops, "S11",
        "07 · DECIDE SMALL · HOW DECISIONS API WORKS",
        "Gemini Decisions API: 50+ Rules in 1 Pass, $0 Output Tokens",
        dark=True,
    )
    # Left column: How it works + Actual JSON rule snippet
    ops.extend([
        {"op": "add-shape", "slide": "S11", "shape_type": "RECTANGLE", "x": 36, "y": 70, "width": 316, "height": 74, "background_color": BLUE_BG},
        {"op": "add-shape", "slide": "S11", "shape_type": "RECTANGLE", "x": 36, "y": 70, "width": 4.5, "height": 74, "background_color": BLUE},
        {
            "op": "add-textbox",
            "slide": "S11",
            "text": (
                "HOW POST /v1beta/decisions WORKS:\n"
                "Skips text generation completely! Runs 1 single forward pass over text, image, audio, or PDF and scores up to 1,000 rules at $0 output cost ($0.10/1M input only)."
            ),
            "x": 48,
            "y": 74,
            "width": 296,
            "height": 66,
            "font_size": 8.6,
            "color": WHITE,
            "font_family": "Roboto",
            "line_spacing": 126,
            "content_alignment": "MIDDLE",
        },
        {"op": "add-shape", "slide": "S11", "shape_type": "RECTANGLE", "x": 36, "y": 152, "width": 316, "height": 236, "background_color": "#0B0E15"},
        {"op": "add-shape", "slide": "S11", "shape_type": "RECTANGLE", "x": 36, "y": 152, "width": 316, "height": 3, "background_color": NEON},
        {"op": "add-shape", "slide": "S11", "shape_type": "RECTANGLE", "x": 36, "y": 155, "width": 316, "height": 22, "background_color": SURFACE_2},
        {
            "op": "add-textbox",
            "slide": "S11",
            "text": "ACTUAL LIVE RULES · monsoonpay/decisions_gate.py",
            "x": 44,
            "y": 157,
            "width": 300,
            "height": 18,
            "font_size": 7.6,
            "bold": True,
            "color": NEON_BRIGHT,
            "font_family": "Roboto Mono",
            "content_alignment": "MIDDLE",
        },
        {
            "op": "add-textbox",
            "slide": "S11",
            "text": (
                '"questions": {\n'
                '  "prompt_injection": {\n'
                '    "type": "noul",  // Yes/No prob (0.0→1.0)\n'
                '    "instructions": "Override or tool hijack?"\n'
                '  },\n'
                '  "leaked_secret_or_pii": {\n'
                '    "type": "noul",  // Catches AIza/sk_live/PAN\n'
                '    "instructions": "Exposes raw keys or PAN?"\n'
                '  },\n'
                '  "target_element": {\n'
                '    "type": "choice", // Hydrogen vs Neon\n'
                '    "criteria": {"hydrogen":"UI","neon":"SEV-1"}\n'
                '  },\n'
                '  "blast_severity": { "type": "score" } // 0→3\n'
                '}'
            ),
            "x": 44,
            "y": 182,
            "width": 302,
            "height": 176,
            "font_size": 7.5,
            "color": SOFT,
            "font_family": "Roboto Mono",
            "line_spacing": 122,
        },
        {
            "op": "add-textbox",
            "slide": "S11",
            "text": "→ Returns calibrated probabilities in 240–283 ms · 0 output tokens!",
            "x": 44,
            "y": 364,
            "width": 302,
            "height": 18,
            "font_size": 7.6,
            "bold": True,
            "color": GREEN_BRIGHT,
            "font_family": "Roboto Mono",
        },
    ])
    # Right column: Compact methodology + 4x4 live benchmark table + green impact callout
    ops.extend([
        {"op": "add-shape", "slide": "S11", "shape_type": "RECTANGLE", "x": 364, "y": 70, "width": 320, "height": 42, "background_color": SURFACE_2},
        {
            "op": "add-textbox",
            "slide": "S11",
            "text": "LIVE TEST: Identical Delhi outage sent to 3 live APIs asking 8 & 50 RBI/PCI checks in 1 request.",
            "x": 374,
            "y": 74,
            "width": 300,
            "height": 34,
            "font_size": 8.4,
            "color": SOFT,
            "font_family": "Roboto",
            "line_spacing": 122,
            "content_alignment": "MIDDLE",
        },
        {"op": "add-table", "slide": "S11", "rows": 4, "cols": 4, "x": 364, "y": 120, "width": 320, "height": 198, "id": "TBL_DEC"},
    ])
    headers11 = ["Test", "Decisions API", "3.8 Flash", "4 Hydrogen"]
    rows11 = [
        ["8 Rules\n(Live)", f"{d1_8_ms} ms\n$0 output", f"{fl_8_ms/1000:.1f}s\n108 out tok", f"{hy_8_ms/1000:.1f}s\n108 out tok"],
        ["50 Rules\n(1 call!)", f"{d1_50_ms} ms\n${d1_50_cost:,.0f}/1M", f"{fl_50_ms/1000:.1f}s\n${fl_50_cost:,.0f}/1M", f"{hy_50_ms/1000:.1f}s\n${hy_50_cost:,.0f}/1M"],
        ["100 Rules\n(Google Pub)", f"{pub100.get('gemini_decision_1_ms', 359)} ms\n$0 output", f"{pub100.get('gemini_3_8_flash_ms', 7200)/1000:.1f}s\n20× slower", f"{pub100.get('gemini_4_hydrogen_ms', 8600)/1000:.1f}s\n24× slower"],
    ]
    for c, h in enumerate(headers11):
        ops.append({
            "op": "set-table-cell",
            "table": "TBL_DEC",
            "row": 0,
            "col": c,
            "text": h,
            "color": MUTED,
            "bold": True,
            "font_size": 8.2,
            "font_family": "Roboto Mono",
            "background_color": SURFACE_2,
        })
    for r_idx, row in enumerate(rows11, start=1):
        bg_row = SURFACE if r_idx % 2 == 1 else "#0E1118"
        for c, cell in enumerate(row):
            col_txt = WHITE if c == 0 else (NEON_BRIGHT if c == 1 else SOFT)
            ops.append({
                "op": "set-table-cell",
                "table": "TBL_DEC",
                "row": r_idx,
                "col": c,
                "text": cell,
                "color": col_txt,
                "bold": c in (0, 1),
                "font_size": 8.5,
                "font_family": "Roboto",
                "background_color": bg_row,
            })
    ops.extend([
        {"op": "add-shape", "slide": "S11", "shape_type": "RECTANGLE", "x": 364, "y": 328, "width": 320, "height": 60, "background_color": GREEN_BG},
        {"op": "add-shape", "slide": "S11", "shape_type": "RECTANGLE", "x": 364, "y": 328, "width": 4.5, "height": 60, "background_color": GREEN},
        {
            "op": "add-textbox",
            "slide": "S11",
            "text": f"LIVE 50-RULE WIN:  {sp50_fl}× faster vs Flash · {cs50_hy}× cheaper vs Hydrogen!\nStop paying generative LLMs to type {{\"ok\": true}} token by token.",
            "x": 376,
            "y": 333,
            "width": 300,
            "height": 50,
            "font_size": 8.8,
            "bold": True,
            "color": GREEN_BRIGHT,
            "font_family": "Roboto",
            "line_spacing": 128,
            "content_alignment": "MIDDLE",
        },
        {"op": "set-notes", "slide": "S11", "text": ""},
    ])

    # ── SLIDE 12: LIVE DEMO 3 — DECISIONS API ARENA ────────────────────────────
    add_demo_split_slide(
        ops, imgs, video_jobs,
        slide_id="S12", slide_index=11,
        kicker="LIVE DEMO 03 · GEMINI DECISIONS API ARENA",
        title="3-Round Live Firewall & 50-Rule Speed Race",
        kpi1=(f"{cs50_hy}×", "Cheaper vs 4 Hydrogen (50 Rules)", NEON_BRIGHT),
        kpi2=(f"{sp50_fl}×", f"Faster vs 3.8 Flash ({d1_50_ms} ms)", GREEN_BRIGHT),
        bullets=[
            "Round A (4 Events × 8 Rules): Blocks prompt attack, masks leaked key, routes UI→Hydrogen & SEV-1→Neon.",
            f"Round B (50 RBI/PCI Rules Race): Finishes in {d1_50_ms} ms (${d1_50_cost:,.0f}/1M) vs 6.3s Flash & 4.9s Hydrogen (${hy_50_cost:,.0f}/1M).",
            f"Round C (Multimodal Bonus): Audits our Google Cloud diagram JPEG for leaked passwords in {mm2['latency_ms']} ms ($0 output!).",
        ],
        poster_filename="demo2_decisions_api_arena_poster.png",
        video_filename="demo2_decisions_api_arena.mp4",
        bar_label="Embedded Offline · Live 3-Round Decisions API Arena",
        drive_url=vids.get("demo2_decisions_api_arena", ""),
        notes="",
        accent=AMBER,
    )

    # ── SLIDE 13: GOVERNED DATA & GOOGLE ADK 2.0 ───────────────────────────────
    add_visual_slide(
        ops, imgs, "S13",
        "08 · GOOGLE CLOUD DATA + ADK 2.0",
        "Zero-Copy Live Data Joins with Built-In Human Approval",
        "07_gcp_data_cloud_v4.jpg",
        "",
        dark=True,
    )

    # ── SLIDE 14: USE CASE 4 DEEP DIVE (NO VIDEO — RICH SELF-SUPPORTING!) ──────
    add_blank_slide(ops, "S14", BG)
    add_header(
        ops, "S14",
        "USE CASE 04 · VOICE CHECK-IN + GOOGLE ADK 2.0 + ZERO-COPY DATA",
        f"Close Your Laptop. Check In by Voice. Isolate Root Cause in {sql3_ms} ms.",
        dark=True,
    )
    ops.extend([
        {"op": "add-shape", "slide": "S14", "shape_type": "RECTANGLE", "x": 36, "y": 68, "width": 648, "height": 40, "background_color": BLUE_BG},
        {"op": "add-shape", "slide": "S14", "shape_type": "RECTANGLE", "x": 36, "y": 68, "width": 5, "height": 40, "background_color": BLUE},
        {
            "op": "add-textbox",
            "slide": "S14",
            "text": 'THE USE CASE: During the Diwali flash sale, you close your laptop to grab filter coffee and ask your remote agent by voice: "Why is Delhi checkout spiking, and is PR #1 ready?"',
            "x": 50,
            "y": 71,
            "width": 624,
            "height": 34,
            "font_size": 9.3,
            "color": WHITE,
            "font_family": "Roboto",
            "line_spacing": 124,
            "content_alignment": "MIDDLE",
        },
    ])
    uc4_steps = [
        ("1 · DUAL-TRACK VOICE", "Zero Dead Air", "Gemini 3.8 responds right away while cloud tools run in the background.", BLUE, BLUE_BRIGHT),
        ("2 · KNOWLEDGE CATALOG", "Verified Join Key", "Hands Google ADK 2.14.1 the exact transaction_id contract — zero SQL guesses.", NEON, NEON_BRIGHT),
        ("3 · ZERO-COPY SQL", f"{sql3_ms} ms · 0 Copies", "Joins 10k Spanner Omni commits + 40k BigQuery Iceberg Envoy logs in place.", GREEN, GREEN_BRIGHT),
        ("4 · ADK 2.0 GATE", "Human Sign-Off", "Calls require_confirmation=True and pauses PR #1 cleanly until Mani approves.", AMBER, AMBER_BRIGHT),
    ]
    for i, (st_lbl, st_head, st_body, bar_c, txt_c) in enumerate(uc4_steps):
        ux = 36 + i * 165
        ops.extend([
            {"op": "add-shape", "slide": "S14", "shape_type": "RECTANGLE", "x": ux, "y": 118, "width": 153, "height": 106, "background_color": SURFACE},
            {"op": "add-shape", "slide": "S14", "shape_type": "RECTANGLE", "x": ux, "y": 118, "width": 153, "height": 3, "background_color": bar_c},
            {"op": "add-textbox", "slide": "S14", "text": st_lbl, "x": ux + 10, "y": 127, "width": 133, "height": 14, "font_size": 7.4, "bold": True, "color": txt_c, "font_family": "Roboto Mono"},
            {"op": "add-textbox", "slide": "S14", "text": st_head, "x": ux + 10, "y": 143, "width": 133, "height": 22, "font_size": 11.2, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S14", "text": st_body, "x": ux + 10, "y": 168, "width": 133, "height": 50, "font_size": 8.2, "color": SOFT, "font_family": "Roboto", "line_spacing": 124},
        ])
    # Bottom Left: Live Regional Root-Cause Table (x=36..446, y=236..388)
    ops.append({"op": "add-table", "slide": "S14", "rows": 3, "cols": 5, "x": 36, "y": 236, "width": 412, "height": 150, "id": "TBL_UC4"})
    h_uc4 = ["Cloud Region", "p99 Commit", "Sync Retries", "Envoy Pool", "TrueTime Drift"]
    r_uc4 = [
        ["Delhi\nasia-south2", f"{delhi3['p99_commit_ms']} ms", f"{delhi3['total_sync_retries']:,}", f"{delhi3['envoy_pool_limit']} slots\n(CHOKED)", f"{delhi3['avg_truetime_drift_ms']} ms\n(OK)"],
        ["Mumbai\nasia-south1", f"{mumbai3['p99_commit_ms']} ms", f"{mumbai3['total_sync_retries']}", f"{mumbai3['envoy_pool_limit']} slots\n(OK)", f"{mumbai3['avg_truetime_drift_ms']} ms\n(OK)"],
    ]
    for c, h in enumerate(h_uc4):
        ops.append({
            "op": "set-table-cell", "table": "TBL_UC4", "row": 0, "col": c, "text": h,
            "color": MUTED, "bold": True, "font_size": 7.8, "font_family": "Roboto Mono", "background_color": SURFACE_2,
        })
    for r_i, row in enumerate(r_uc4, start=1):
        bg_r = SURFACE if r_i == 1 else "#0E1118"
        for c, cell in enumerate(row):
            if r_i == 1 and c in (1, 2):
                ct = RED_BRIGHT
            elif (r_i == 2 and c in (1, 2)) or c == 4:
                ct = GREEN_BRIGHT
            else:
                ct = WHITE if c == 0 else SOFT
            ops.append({
                "op": "set-table-cell", "table": "TBL_UC4", "row": r_i, "col": c, "text": cell,
                "color": ct, "bold": c in (0, 1, 2, 4), "font_size": 8.4, "font_family": "Roboto", "background_color": bg_r,
            })
    # Bottom Right: Verified Root Cause Verdict Card (x=458..684, y=236..388)
    ops.extend([
        {"op": "add-shape", "slide": "S14", "shape_type": "RECTANGLE", "x": 458, "y": 236, "width": 226, "height": 150, "background_color": GREEN_BG},
        {"op": "add-shape", "slide": "S14", "shape_type": "RECTANGLE", "x": 458, "y": 236, "width": 226, "height": 3, "background_color": GREEN},
        {"op": "add-textbox", "slide": "S14", "text": "VERIFIED ROOT CAUSE", "x": 470, "y": 246, "width": 202, "height": 16, "font_size": 8.0, "bold": True, "color": GREEN_BRIGHT, "font_family": "Roboto Mono"},
        {
            "op": "add-textbox",
            "slide": "S14",
            "text": (
                "▸  Spanner TrueTime stayed healthy (2.75 ms drift) — database was NOT broken!\n\n"
                "▸  Delhi's 64-slot Envoy queue choked under Diwali burst → 18,006 sync retries.\n\n"
                "▸  ADK 2.0 paused PR #1 (512-slot + circuit breaker) awaiting Mani's sign-off."
            ),
            "x": 470,
            "y": 266,
            "width": 202,
            "height": 114,
            "font_size": 8.4,
            "color": WHITE,
            "font_family": "Roboto",
            "line_spacing": 124,
        },
        {"op": "set-notes", "slide": "S14", "text": ""},
    ])

    # ── SLIDE 15: REAL VOICE AI (PART A) — CAMERA + VOICE FLIGHT REBOOKING ─────
    add_voice_arch_video_slide(
        ops, imgs, video_jobs,
        slide_id="S15", slide_index=14,
        kicker="REAL VOICE AI · PART A · GEMINI 3.8 LIVE EXTENDED THINKING",
        title="Live Camera + Voice Concierge — Zero Dead Air",
        badge_text="OFFLINE VIDEO · ARCH + DEMO",
        badge_color=GREEN,
        arch_filename="09_arch_live_flight.jpg",
        poster_filename="demo4a_gemini38_live_flight_poster.png",
        video_filename="demo4a_gemini38_live_flight.mp4",
        video_ratio=1360.0 / 720.0,
        video_caption="Embedded Offline (2:40) · Live Boarding Pass + BigQuery & Firestore",
        video_highlights=[
            "1 FPS live camera reads the stranded boarding pass (LH8942X) while conversing naturally.",
            "Non-blocking background tools query BigQuery flights, calculate EU261, and commit Firestore.",
            "Zero dead air: speaks calmly while extended thinking runs multi-step enterprise actions.",
        ],
        drive_url=DRIVE_FLIGHT_URL,
        notes="",
    )

    # ── SLIDE 16: REAL VOICE AI (PART B) — INDIAN PSTN TELEPHONY ───────────────
    add_voice_arch_video_slide(
        ops, imgs, video_jobs,
        slide_id="S16", slide_index=15,
        kicker="REAL VOICE AI · PART B · INDIAN PSTN TELEPHONY ON GOOGLE CLOUD",
        title="Real Indian Phone Calls Across 6 Languages",
        badge_text="OFFLINE VIDEO · ARCH + DEMO",
        badge_color=NEON,
        arch_filename="10_arch_voice_pstn.jpg",
        poster_filename="demo4b_gemini_voiceai_pstn_poster.png",
        video_filename="demo4b_gemini_voiceai_pstn.mp4",
        video_ratio=1280.0 / 590.0,
        video_caption="Embedded Offline (3:03) · 6 Indian Languages on Cloud Run Mumbai",
        video_highlights=[
            "Real Indian PSTN phone calls routed via Cloud Armor + Load Balancing + Cloud Run Mumbai.",
            "Supports BOTH Direct Speech-to-Speech (Gemini Live) AND Cascaded Listen-Think-Speak.",
            "Handles English, Hindi, Tamil, Kannada, Telugu & Hinglish with live Firestore call state.",
        ],
        drive_url=DRIVE_PSTN_URL,
        notes="",
    )

    # ── SLIDE 17: LIVE DEMO 5 — HOW GEMINI 4 NEON DOES CYBER SCREENING ─────────
    add_blank_slide(ops, "S17", BG)
    ops.extend([
        {"op": "add-shape", "slide": "S17", "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 6, "height": 405, "background_color": GREEN},
        {"op": "add-textbox", "slide": "S17", "text": "LIVE DEMO 05 · INDEPENDENT GEMINI 4 NEON CYBER SCREENING", "x": 34, "y": 14, "width": 650, "height": 15, "font_size": 8.4, "bold": True, "color": NEON_BRIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S17", "text": f"-{drop4}% Delay & {tests4}/{tests4} Green — Still Screened by Neon Cyber.", "x": 34, "y": 30, "width": 650, "height": 26, "font_size": 17.0, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-shape", "slide": "S17", "shape_type": "RECTANGLE", "x": 34, "y": 59, "width": 652, "height": 1.0, "background_color": BORDER},
    ])
    # Left panel (x=34..372, w=338): 2 compact KPI cards + 4 Neon security check cards + Golden Rule pill
    for idx_k, (kv, kl, kc) in enumerate([
        (f"{round(bef4)} → {aft4:.1f} ms", "500-User Diwali Burst (-97.1%)", GREEN_BRIGHT),
        ("90.5% · 0% IPI", "SEC-bench Pro · Independent Agent", NEON_BRIGHT),
    ]):
        kx = 34 + idx_k * 172
        ops.extend([
            {"op": "add-shape", "slide": "S17", "shape_type": "RECTANGLE", "x": kx, "y": 68, "width": 164, "height": 48, "background_color": SURFACE},
            {"op": "add-textbox", "slide": "S17", "text": kv, "x": kx + 10, "y": 73, "width": 144, "height": 22, "font_size": 13.5, "bold": True, "color": kc, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S17", "text": kl, "x": kx + 10, "y": 96, "width": 144, "height": 16, "font_size": 7.4, "color": MUTED, "font_family": "Roboto"},
        ])
    ops.append({
        "op": "add-textbox",
        "slide": "S17",
        "text": "HOW NEON SCREENS PR #1 (NEVER GRADES ITS OWN CODE):",
        "x": 34, "y": 122, "width": 338, "height": 15, "font_size": 7.6, "bold": True, "color": MUTED, "font_family": "Roboto Mono",
    })
    for idx_c, chk in enumerate(checks4[:4]):
        cy = 140 + idx_c * 52
        is_warn = chk["status"] != "PASS"
        row_bg = NEON_BG if is_warn else SURFACE
        badge_bg = NEON if is_warn else GREEN
        badge_fg = "#111319" if is_warn else "#07140C"
        ops.extend([
            {"op": "add-shape", "slide": "S17", "shape_type": "RECTANGLE", "x": 34, "y": cy, "width": 338, "height": 46, "background_color": row_bg},
            {"op": "add-textbox", "slide": "S17", "text": chk["status"], "x": 42, "y": cy + 12, "width": 40, "height": 20, "font_size": 7.4, "bold": True, "color": badge_fg, "background_color": badge_bg, "font_family": "Roboto Mono", "alignment": "center", "content_alignment": "MIDDLE"},
            {"op": "add-textbox", "slide": "S17", "text": f"{chk['title']}: {chk['finding']}", "x": 88, "y": cy + 5, "width": 278, "height": 36, "font_size": 8.0, "color": WHITE if is_warn else SOFT, "font_family": "Roboto", "line_spacing": 120, "content_alignment": "MIDDLE"},
        ])
    ops.extend([
        {"op": "add-shape", "slide": "S17", "shape_type": "RECTANGLE", "x": 34, "y": 352, "width": 338, "height": 34, "background_color": NEON_BG},
        {"op": "add-shape", "slide": "S17", "shape_type": "RECTANGLE", "x": 34, "y": 352, "width": 4, "height": 34, "background_color": NEON},
        {"op": "add-textbox", "slide": "S17", "text": f"VERDICT: {verdict4} · AI writes & audits — Humans own Merge!", "x": 44, "y": 356, "width": 322, "height": 26, "font_size": 8.2, "bold": True, "color": NEON_BRIGHT, "font_family": "Roboto Mono", "content_alignment": "MIDDLE"},
    ])
    # Right panel (x=384..688, w=304): Video player container + 3-step summary
    ops.extend([
        {"op": "add-shape", "slide": "S17", "shape_type": "RECTANGLE", "x": 384, "y": 68, "width": 304, "height": 318, "background_color": SURFACE},
        {"op": "add-shape", "slide": "S17", "shape_type": "RECTANGLE", "x": 384, "y": 68, "width": 304, "height": 3, "background_color": GREEN},
    ])
    v17_x, v17_y, v17_w, v17_h = 392.0, 78.0, 288.0, 162.0
    imgs.append({"slide": "S17", "file": str(VID_DIR / "demo4_review_shipped_pr_poster.png"), "x": v17_x, "y": v17_y, "width": v17_w, "height": v17_h})
    video_jobs.append({
        "slide_index": 16,
        "video": str(VID_DIR / "demo4_review_shipped_pr.mp4"),
        "poster": str(VID_DIR / "demo4_review_shipped_pr_poster.png"),
        "x": v17_x, "y": v17_y, "width": v17_w, "height": v17_h,
    })
    cta17: Dict[str, Any] = {
        "op": "add-textbox",
        "slide": "S17",
        "text": "▶  Embedded Offline · Load Test + Pytest + Neon Audit",
        "x": 392, "y": 248, "width": 288, "height": 28,
        "font_size": 8.2, "bold": True, "color": WHITE, "background_color": SURFACE_2,
        "font_family": "Roboto Mono", "alignment": "center", "content_alignment": "MIDDLE",
    }
    if vids.get("demo4_review_shipped_pr"):
        cta17["link"] = vids["demo4_review_shipped_pr"]
    ops.append(cta17)
    ops.extend([
        {
            "op": "add-textbox",
            "slide": "S17",
            "text": (
                "WHAT DEMO 5 RUNS LIVE:\n"
                "1. Deterministic 500-user Diwali burst (before vs after)\n"
                "2. Full pytest suite verification (10/10 green)\n"
                "3. Independent gemini-4-neon session audits PR #1 diffs"
            ),
            "x": 394, "y": 284, "width": 284, "height": 94,
            "font_size": 8.3, "color": SOFT, "font_family": "Roboto", "line_spacing": 132,
        },
        {"op": "set-notes", "slide": "S17", "text": ""},
    ])

    # ── SLIDE 18: COMEDY PLOT-TWIST TEASER — "AND THEN...?" ────────────────────
    add_blank_slide(ops, "S18", "#05080D")
    ops.extend([
        {"op": "add-shape", "slide": "S18", "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 6, "height": 405, "background_color": NEON},
        {"op": "add-textbox", "slide": "S18", "text": "WAIT A SECOND  ·  DUDE, WHERE'S MY BLAST RADIUS?!", "x": 38, "y": 30, "width": 324, "height": 18, "font_size": 8.6, "bold": True, "color": NEON_BRIGHT, "font_family": "Roboto Mono"},
        {
            "op": "add-textbox",
            "slide": "S18",
            "text": (
                "✓  Fixed Delhi flash-sale latency (-97.1% p99)\n\n"
                "✓  Modernized legacy UPI (100.5× faster, ₹0 error)\n\n"
                "✓  Blocked attacks at $0 output (Decisions API)\n\n"
                "✓  Passed Gemini 4 Neon independent cyber audit"
            ),
            "x": 38, "y": 64, "width": 320, "height": 132,
            "font_size": 10.6, "color": SOFT, "font_family": "Roboto", "line_spacing": 122,
        },
        {
            "op": "add-textbox",
            "slide": "S18",
            "text": "“NO ‘AND THEN’!”",
            "x": 38, "y": 208, "width": 324, "height": 48,
            "font_size": 27.0, "bold": True, "color": WHITE, "font_family": "Montserrat",
        },
        {"op": "add-shape", "slide": "S18", "shape_type": "RECTANGLE", "x": 38, "y": 274, "width": 318, "height": 98, "background_color": NEON_BG},
        {"op": "add-shape", "slide": "S18", "shape_type": "RECTANGLE", "x": 38, "y": 274, "width": 5, "height": 98, "background_color": NEON},
        {"op": "add-textbox", "slide": "S18", "text": "“AND THENNN...”", "x": 52, "y": 284, "width": 292, "height": 22, "font_size": 11.5, "bold": True, "color": NEON_BRIGHT, "font_family": "Roboto Mono"},
        {
            "op": "add-textbox",
            "slide": "S18",
            "text": "What happens at 2:00 PM on a Tuesday when ONE noisy neighbor, bad config push, or cyber attack hits your shared cluster?",
            "x": 52, "y": 310, "width": 292, "height": 54,
            "font_size": 10.2, "color": WHITE, "font_family": "Roboto", "line_spacing": 128,
        },
        {"op": "set-notes", "slide": "S18", "text": ""},
    ])
    # Exact cropped right-panel neon speaker artwork (696x768, ratio 0.90625 -> 367.0 x 405.0 at x=353, y=0) — ZERO z-order overlap with left text!
    imgs.append({
        "slide": "S18",
        "file": str(DIAG_DIR / "12_and_then_teaser_right.jpg"),
        "x": 353.0,
        "y": 0.0,
        "width": 367.0,
        "height": 405.0,
    })

    # ── SLIDE 19: CELL-BASED ARCHITECTURE & SHUFFLE SHARDING BLOG SLIDE ────────
    add_blank_slide(ops, "S19", BG)
    add_header(
        ops, "S19",
        "BONUS · CONTAINING 2026 OUTAGES & CYBER BLAST RADIUS",
        "Cell-Based Architecture & Shuffle Sharding on Google Cloud",
        dark=True,
        right_label="discuss.google.dev/t/413515",
        right_link=CELL_BLOG_URL,
    )
    # Left main white mat for Mani's exact 2360x1300 blog architecture diagram (ratio 1.81538 -> 444.0 x 244.6 at x=38, y=75)
    ops.extend([
        {"op": "add-shape", "slide": "S19", "shape_type": "RECTANGLE", "x": 34, "y": 70, "width": 452, "height": 254, "background_color": "#FFFFFF"},
        # Bottom blast-radius comparison strip (x=34..486, y=332..388)
        {"op": "add-shape", "slide": "S19", "shape_type": "RECTANGLE", "x": 34, "y": 332, "width": 134, "height": 56, "background_color": RED_BG},
        {"op": "add-shape", "slide": "S19", "shape_type": "RECTANGLE", "x": 34, "y": 332, "width": 134, "height": 2.5, "background_color": RED},
        {"op": "add-textbox", "slide": "S19", "text": "100% Down", "x": 40, "y": 340, "width": 122, "height": 22, "font_size": 13.0, "bold": True, "color": RED_BRIGHT, "font_family": "Montserrat", "alignment": "center"},
        {"op": "add-textbox", "slide": "S19", "text": "1 Shared Cluster", "x": 40, "y": 364, "width": 122, "height": 16, "font_size": 7.6, "color": SOFT, "font_family": "Roboto Mono", "alignment": "center"},

        {"op": "add-shape", "slide": "S19", "shape_type": "RECTANGLE", "x": 176, "y": 332, "width": 134, "height": 56, "background_color": SURFACE},
        {"op": "add-shape", "slide": "S19", "shape_type": "RECTANGLE", "x": 176, "y": 332, "width": 134, "height": 2.5, "background_color": AMBER},
        {"op": "add-textbox", "slide": "S19", "text": "12.5% Impact", "x": 182, "y": 340, "width": 122, "height": 22, "font_size": 13.0, "bold": True, "color": AMBER_BRIGHT, "font_family": "Montserrat", "alignment": "center"},
        {"op": "add-textbox", "slide": "S19", "text": "8 Normal Cells (1/8)", "x": 182, "y": 364, "width": 122, "height": 16, "font_size": 7.6, "color": SOFT, "font_family": "Roboto Mono", "alignment": "center"},

        {"op": "add-shape", "slide": "S19", "shape_type": "RECTANGLE", "x": 318, "y": 332, "width": 168, "height": 56, "background_color": GREEN_BG},
        {"op": "add-shape", "slide": "S19", "shape_type": "RECTANGLE", "x": 318, "y": 332, "width": 168, "height": 2.5, "background_color": GREEN},
        {"op": "add-textbox", "slide": "S19", "text": "<1.8% (98.2% Online)", "x": 322, "y": 340, "width": 160, "height": 22, "font_size": 12.2, "bold": True, "color": GREEN_BRIGHT, "font_family": "Montserrat", "alignment": "center"},
        {"op": "add-textbox", "slide": "S19", "text": "3-Cell Shuffle · 56 Hands", "x": 322, "y": 364, "width": 160, "height": 16, "font_size": 7.4, "color": SOFT, "font_family": "Roboto Mono", "alignment": "center"},
    ])
    imgs.append({
        "slide": "S19",
        "file": str(DIAG_DIR / "11_cell_based_architecture.png"),
        "x": 38.0,
        "y": 74.7,
        "width": 444.0,
        "height": 244.6,
    })
    # Right column (x=496..686, w=190): Why Cells Matter card + Chunky Scannable Blog QR Card
    ops.extend([
        {"op": "add-shape", "slide": "S19", "shape_type": "RECTANGLE", "x": 496, "y": 70, "width": 190, "height": 176, "background_color": SURFACE},
        {"op": "add-shape", "slide": "S19", "shape_type": "RECTANGLE", "x": 496, "y": 70, "width": 190, "height": 3, "background_color": BLUE},
        {"op": "add-textbox", "slide": "S19", "text": "WHY CELLS MATTER IN 2026", "x": 506, "y": 80, "width": 170, "height": 16, "font_size": 7.8, "bold": True, "color": BLUE_BRIGHT, "font_family": "Roboto Mono"},
        {
            "op": "add-textbox",
            "slide": "S19",
            "text": (
                "▸  Watertight Bulkheads: Dedicated GCP Project, Cloud Run/GKE, Spanner & VPC/KMS per cell — zero sideways traffic.\n\n"
                "▸  Stops Cyber & Outages: Contains bad rollouts, poison-pill requests, ransomware & rogue AI agents to <2%.\n\n"
                "▸  Stateless Hot Path: ALB Wasm router retries a healthy backup cell (200 OK)."
            ),
            "x": 506, "y": 100, "width": 170, "height": 140,
            "font_size": 8.0, "color": SOFT, "font_family": "Roboto", "line_spacing": 120,
        },
        # Scannable QR Card for Mani's Blog (x=496..686, y=254..388, h=134)
        {"op": "add-shape", "slide": "S19", "shape_type": "RECTANGLE", "x": 496, "y": 254, "width": 190, "height": 134, "background_color": SURFACE_2},
        {"op": "add-shape", "slide": "S19", "shape_type": "RECTANGLE", "x": 496, "y": 254, "width": 190, "height": 3, "background_color": NEON},
        {"op": "add-textbox", "slide": "S19", "text": "SCAN · READ MANI'S BLOG", "x": 502, "y": 355, "width": 178, "height": 14, "font_size": 8.0, "bold": True, "color": NEON_BRIGHT, "font_family": "Roboto Mono", "alignment": "center", "link": CELL_BLOG_URL},
        {"op": "add-textbox", "slide": "S19", "text": "discuss.google.dev/t/413515", "x": 502, "y": 370, "width": 178, "height": 14, "font_size": 7.2, "color": MUTED, "font_family": "Roboto Mono", "alignment": "center", "link": CELL_BLOG_URL},
        {"op": "set-notes", "slide": "S19", "text": ""},
    ])
    imgs.append({
        "slide": "S19",
        "file": str(DIAG_DIR / "qr_cell_blog.png"),
        "x": 546.0,
        "y": 262.0,
        "width": 90.0,
        "height": 90.0,
    })

    # ── SLIDE 20: CLOSING (5 TAKEAWAYS + ALL 3 SCANNABLE QR CODES!) ────────────
    add_blank_slide(ops, "S20", BG)
    ops.extend([
        {"op": "add-shape", "slide": "S20", "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 7, "height": 405, "background_color": NEON},
        {"op": "add-textbox", "slide": "S20", "text": "THANK YOU  ·  DEVFEST BENGALURU 2026", "x": 44, "y": 24, "width": 632, "height": 18, "font_size": 9.2, "bold": True, "color": NEON_BRIGHT, "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": "S20", "text": "Plan Big. Build Fast. Decide Instant.\nShip Safe. Contain Blast Radius.", "x": 44, "y": 46, "width": 632, "height": 84, "font_size": 27.5, "bold": True, "color": WHITE, "font_family": "Montserrat", "line_spacing": 108},
    ])
    takeaways20 = [
        ("1 · Neon", "Plan, modernize & audit at $3/$15", NEON),
        ("2 · Hydrogen", "Parallel /swarm in sandboxes", BLUE),
        ("3 · Decisions", "50+ rules at $0 output cost", AMBER),
        ("4 · Humans", "ADK 2.0 gates on prod merge", GREEN),
        ("5 · Cells", "Shuffle sharding <1.8% blast", NEON),
    ]
    for i, (head, desc, col) in enumerate(takeaways20):
        tx = 44 + i * 128
        ops.extend([
            {"op": "add-shape", "slide": "S20", "shape_type": "RECTANGLE", "x": tx, "y": 144, "width": 120, "height": 86, "background_color": SURFACE},
            {"op": "add-shape", "slide": "S20", "shape_type": "RECTANGLE", "x": tx, "y": 144, "width": 120, "height": 3, "background_color": col},
            {"op": "add-textbox", "slide": "S20", "text": head, "x": tx + 9, "y": 156, "width": 102, "height": 20, "font_size": 10.6, "bold": True, "color": WHITE, "font_family": "Montserrat"},
            {"op": "add-textbox", "slide": "S20", "text": desc, "x": tx + 9, "y": 180, "width": 102, "height": 42, "font_size": 8.0, "color": SOFT, "font_family": "Roboto", "line_spacing": 124},
        ])
    # Closing speaker card + buttons + ALL 3 matched QR cards (LinkedIn + GitHub + Cell Blog)
    ops.extend([
        {"op": "add-shape", "slide": "S20", "shape_type": "RECTANGLE", "x": 44, "y": 246, "width": 632, "height": 142, "background_color": SURFACE},
        {"op": "add-shape", "slide": "S20", "shape_type": "RECTANGLE", "x": 44, "y": 246, "width": 5, "height": 142, "background_color": NEON},
        {"op": "add-textbox", "slide": "S20", "text": "Mani", "x": 62, "y": 258, "width": 266, "height": 28, "font_size": 21, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": "S20", "text": "Principal Architect, Google Cloud", "x": 62, "y": 288, "width": 268, "height": 18, "font_size": 11.0, "color": SOFT, "font_family": "Roboto"},
        {"op": "add-textbox", "slide": "S20", "text": "Come say hi — look for the brand-new badge!", "x": 62, "y": 308, "width": 268, "height": 18, "font_size": 8.8, "color": MUTED, "font_family": "Roboto"},
        {
            "op": "add-textbox",
            "slide": "S20",
            "text": "LinkedIn · Connect",
            "x": 62, "y": 336, "width": 134, "height": 28,
            "font_size": 8.0, "bold": True, "color": "#111319", "background_color": NEON_BRIGHT,
            "font_family": "Roboto Mono", "alignment": "center", "content_alignment": "MIDDLE", "link": LINKEDIN_URL,
        },
        {
            "op": "add-textbox",
            "slide": "S20",
            "text": "GitHub · Offline Deck",
            "x": 202, "y": 336, "width": 128, "height": 28,
            "font_size": 7.8, "bold": True, "color": WHITE, "background_color": SURFACE_2,
            "font_family": "Roboto Mono", "alignment": "center", "content_alignment": "MIDDLE", "link": GITHUB_URL,
        },
        {"op": "set-notes", "slide": "S20", "text": ""},
    ])
    add_qr_trio_ops(ops, imgs, "S20", x_start=344.0, y_top=255.0, card_w=100.0, card_h=124.0, qr_size=80.0, gap=11.0)

    # Synchronize all 20 slides with the rich, jovial Principal Architect speaker notes from build_html_keynote.py
    from presentation.build_html_keynote import build_slides as build_html_slides
    rich_notes = [s["notes"] for s in build_html_slides(tr)]
    slide_keys = ["p"] + [f"S{n:02d}" for n in range(2, 21)]
    notes_by_slide = dict(zip(slide_keys, rich_notes))
    for op in ops:
        if op.get("op") == "set-notes" and op.get("slide") in notes_by_slide:
            op["text"] = notes_by_slide[op["slide"]]

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


def sync_qr_and_notes_in_place(pres_id: str, tr: Dict[str, Any], drive: Dict[str, Any]) -> None:
    """Updates an existing 18-slide v4 deck in-place with Slide 1 & 18 QR cards + rich speaker notes, then re-exports PDF/PPTX."""
    from presentation.build_html_keynote import build_slides as build_html_slides

    slides_json = json.loads(run_cmd(["gslides", "readonly", "list-slides", pres_id, "--json"]))
    slide_ids = [s["objectId"] for s in slides_json]
    if len(slide_ids) != 18:
        raise RuntimeError(f"Expected 18 slides on {pres_id}, found {len(slide_ids)}")
    resolved = {"p": slide_ids[0]}
    for n in range(2, 19):
        resolved[f"S{n:02d}"] = slide_ids[n - 1]

    # 1. Inspect Slide 18 bottom panel elements (y > 245pt => translateY > 3111500 EMU) to cleanly replace with bio + QR pair
    s18_id = resolved["S18"]
    s18_elems = json.loads(run_cmd(["gslides", "readonly", "list-elements", pres_id, "17", "--json"]))
    delete_ops: List[Dict[str, Any]] = []
    for el in s18_elems:
        ty = el.get("transform", {}).get("translateY", 0)
        oid = el.get("objectId", "")
        if oid and ty > 3_100_000:
            delete_ops.append({"op": "delete-element", "element": oid})

    # Also remove any existing QR elements on Slide 1 (x > 460pt and y < 145pt) if re-running idempotently
    s01_elems = json.loads(run_cmd(["gslides", "readonly", "list-elements", pres_id, "0", "--json"]))
    for el in s01_elems:
        tx = el.get("transform", {}).get("translateX", 0)
        ty = el.get("transform", {}).get("translateY", 0)
        oid = el.get("objectId", "")
        if oid and tx > 5_800_000 and ty < 1_900_000:
            delete_ops.append({"op": "delete-element", "element": oid})

    patch_ops: List[Dict[str, Any]] = list(delete_ops)
    qr_imgs: List[Dict[str, Any]] = []

    # 2. Add QR pair to Slide 1 (`p`)
    add_qr_pair_ops(patch_ops, qr_imgs, "p", x_start=482.0, y_top=22.0, card_w=92.0, card_h=112.0, qr_size=74.0, gap=10.0)

    # 3. Rebuild Slide 18 closing panel with Mani bio + buttons + large QR pair
    patch_ops.extend([
        {"op": "add-shape", "slide": s18_id, "shape_type": "RECTANGLE", "x": 44, "y": 252, "width": 632, "height": 134, "background_color": SURFACE},
        {"op": "add-shape", "slide": s18_id, "shape_type": "RECTANGLE", "x": 44, "y": 252, "width": 5, "height": 134, "background_color": NEON},
        {"op": "add-textbox", "slide": s18_id, "text": "Mani", "x": 64, "y": 264, "width": 320, "height": 28, "font_size": 21, "bold": True, "color": WHITE, "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": s18_id, "text": "Principal Architect, Google Cloud", "x": 64, "y": 294, "width": 340, "height": 20, "font_size": 11.2, "color": SOFT, "font_family": "Roboto"},
        {"op": "add-textbox", "slide": s18_id, "text": "Come say hi — look for the brand-new badge!", "x": 64, "y": 315, "width": 340, "height": 18, "font_size": 9.2, "color": MUTED, "font_family": "Roboto"},
        {"op": "add-textbox", "slide": s18_id, "text": "LinkedIn · /in/cmanikandan", "x": 64, "y": 342, "width": 172, "height": 28, "font_size": 9.0, "bold": True, "color": "#111319", "background_color": NEON_BRIGHT, "font_family": "Roboto Mono", "alignment": "center", "content_alignment": "MIDDLE", "link": LINKEDIN_URL},
        {"op": "add-textbox", "slide": s18_id, "text": "GitHub · Code & Stage UI", "x": 244, "y": 342, "width": 172, "height": 28, "font_size": 9.0, "bold": True, "color": WHITE, "background_color": SURFACE_2, "font_family": "Roboto Mono", "alignment": "center", "content_alignment": "MIDDLE", "link": GITHUB_URL},
    ])
    add_qr_pair_ops(patch_ops, qr_imgs, s18_id, x_start=442.0, y_top=260.0, card_w=104.0, card_h=118.0, qr_size=82.0, gap=12.0)

    # 4. Update all 18 slides' speaker notes
    rich_notes = [s["notes"] for s in build_html_slides(tr)]
    for sid, note_text in zip(slide_ids, rich_notes):
        patch_ops.append({"op": "set-notes", "slide": sid, "text": note_text})

    # 5. Add the 4 QR code images on top of the cards via signed GitHub URLs
    for job in qr_imgs:
        patch_ops.append({
            "op": "add-image",
            "slide": job["slide"],
            "url": github_signed_url(job["file"]),
            "x": job["x"],
            "y": job["y"],
            "width": job["width"],
            "height": job["height"],
        })

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
        json.dump(patch_ops, tf, indent=2)
        patch_file = tf.name
    try:
        print(f"Syncing QR codes (Slides 1 & 18) + rich speaker notes (all 18 slides) on {pres_id}...")
        run_cmd(["gslides", "mutate", "batch", pres_id, "-f", patch_file, "--json"])
        print("  ✔ In-place Google Slides QR & speaker notes update complete!")
    finally:
        Path(patch_file).unlink(missing_ok=True)

    _, _, video_jobs = build_deck_ops(tr, drive)
    pdf_path = PRES_DIR / "Periodic_Table_of_Agents_DevFest_Keynote.pdf"
    pptx_path = PRES_DIR / "Periodic_Table_of_Agents_DevFest_Keynote.pptx"
    run_cmd(["gslides", "readonly", "export", pres_id, str(pdf_path), "--format", "pdf"])
    run_cmd(["gslides", "readonly", "export", pres_id, str(pptx_path), "--format", "pptx"])
    print(f"  ✔ Re-exported PDF ({pdf_path.stat().st_size // 1024} KB) & base PPTX ({pptx_path.stat().st_size // 1024} KB)")
    embed_videos_into_pptx(pptx_path, video_jobs)
    print(f"  ✔ Final self-contained PPTX with 7 embedded videos + QRs: {pptx_path.stat().st_size // 1024} KB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pres-id", default="", help="Existing Google Slides presentation ID")
    parser.add_argument("--images-only", action="store_true", help="Place images on an existing 18-slide deck and export PDF/PPTX")
    parser.add_argument("--sync-qr-and-notes", action="store_true", help="Update an existing 18-slide deck in-place with QR cards + rich speaker notes and re-export PDF/PPTX")
    args = parser.parse_args()

    tr = load_traces()
    drive = load_drive_links()

    if args.sync_qr_and_notes:
        if not args.pres_id:
            meta = json.loads((PRES_DIR / "google_slides_metadata.json").read_text(encoding="utf-8"))
            pres_id = meta["presentation_id"]
        else:
            pres_id = args.pres_id
        sync_qr_and_notes_in_place(pres_id, tr, drive)
        return

    ops, img_jobs, video_jobs = build_deck_ops(tr, drive)

    title = "The Periodic Table of Agents — Gemini 4 Neon Keynote v5 (DevFest Bengaluru 2026)"
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
        if len(slide_ids) != 20:
            raise RuntimeError(f"Expected 20 slides on {pres_id}, found {len(slide_ids)}")
        resolved = {"p": slide_ids[0]}
        for n in range(2, 21):
            resolved[f"S{n:02d}"] = slide_ids[n - 1]
    else:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tf:
            json.dump(ops, tf, indent=2)
            batch_file = tf.name
        try:
            print(f"Applying {len(ops)} batch operations across 20 slides...")
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

    print(f"Fetching signed GitHub URLs & placing {len(img_jobs)} crisp diagrams, QR codes & video frames...")
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
    pptx_offline_path = PRES_DIR / "Periodic_Table_of_Agents_DevFest_Keynote_Offline_v5.pptx"
    run_cmd(["gslides", "readonly", "export", pres_id, str(pdf_path), "--format", "pdf"])
    run_cmd(["gslides", "readonly", "export", pres_id, str(pptx_path), "--format", "pptx"])
    print(f"  ✔ Exported PDF ({pdf_path.stat().st_size // 1024} KB) & base PPTX ({pptx_path.stat().st_size // 1024} KB)")

    embed_videos_into_pptx(pptx_path, video_jobs)
    shutil.copy2(pptx_path, pptx_offline_path)
    print(f"  ✔ Final 100% offline self-contained PPTX ({len(video_jobs)} embedded MP4 videos): {pptx_offline_path.name} ({pptx_offline_path.stat().st_size // 1024} KB)")

    meta = {
        "presentation_id": pres_id,
        "presentation_url": f"https://docs.google.com/presentation/d/{pres_id}/edit",
        "title": title,
        "version": "v5-gemini-4-neon-offline",
        "slide_count": 20,
        "embedded_offline_videos": len(video_jobs),
        "offline_pptx": str(pptx_offline_path.relative_to(ROOT)),
        "cell_architecture_blog": CELL_BLOG_URL,
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
    print(f"🎉 DONE! Google Slides v5 URL: {meta['presentation_url']}")


if __name__ == "__main__":
    main()
