#!/usr/bin/env python3
"""
Creates the 17-slide Google Slides DevFest Keynote presentation via `gslides`,
uploads & places all 7 O'Reilly Head First infographics + 4 1080p Demo frames,
attaches clickable Google Drive HD Demo Video buttons + full Speaker Notes,
and exports local PDF & PPTX backups.
"""

from __future__ import annotations
import json
import os
import re
import subprocess
from typing import Any, Dict, List

ROOT = "/home/antigravity/cmanikandan/gdg-blr-talk-nov14-2026"
INFO_DIR = f"{ROOT}/assets/infographics"
VID_DIR = f"{ROOT}/assets/videos"

DRIVE_VIDEOS = {
    "demo1": "https://drive.google.com/file/d/1HOaMxWBm-Rd-eTYZE5AxKWrsRb6PFXeU/view",
    "demo2": "https://drive.google.com/file/d/1txCsSUKm5PROv4CjMwZXlGn9fmUwWwpU/view",
    "demo3": "https://drive.google.com/file/d/1F-HFLv6-9pQIGJQ3daiavthGJVlR-dY3/view",
    "demo4": "https://drive.google.com/file/d/1jywQPd5GISQJdftvTDHXGoFHKidGSBsa/view",
    "folder": "https://drive.google.com/drive/folders/17FSevMIs-B9Th0A3XHudNABUKQlHSgpY",
}


def add_hero_slide(
    ops: List[Dict[str, Any]],
    slide_id: str,
    is_first: bool,
    kicker: str,
    title: str,
    subtitle: str,
    pills: List[str],
    footer: str,
    notes: str,
    link_url: str = "",
) -> None:
    if is_first:
        ops.append({"op": "delete-element", "element": "i0"})
        ops.append({"op": "delete-element", "element": "i1"})
    else:
        ops.append({"op": "add-slide", "layout": "BLANK", "id": slide_id})

    ops.extend([
        {"op": "set-background", "slide": slide_id, "color": "#0F172A"},
        {"op": "add-shape", "slide": slide_id, "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 12, "height": 405, "background_color": "#4285F4"},
        {"op": "add-textbox", "slide": slide_id, "text": kicker, "x": 40, "y": 32, "width": 640, "height": 24, "font_size": 11, "bold": True, "color": "#38BDF8", "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": slide_id, "text": title, "x": 40, "y": 64, "width": 640, "height": 108, "font_size": 30, "bold": True, "color": "#FFFFFF", "font_family": "Montserrat"},
        {"op": "add-textbox", "slide": slide_id, "text": subtitle, "x": 40, "y": 178, "width": 640, "height": 54, "font_size": 16, "color": "#CBD5E1", "font_family": "Roboto"},
    ])

    xs = [40, 204, 368, 532]
    colors = ["#1E3A8A", "#065F46", "#78350F", "#312E81"]
    for i, p in enumerate(pills[:4]):
        tb: Dict[str, Any] = {
            "op": "add-textbox",
            "slide": slide_id,
            "text": p,
            "x": xs[i],
            "y": 252,
            "width": 150,
            "height": 56,
            "font_size": 11,
            "bold": True,
            "color": "#F8FAFC",
            "background_color": colors[i],
            "font_family": "Roboto",
            "alignment": "center",
            "content_alignment": "MIDDLE",
        }
        if link_url and i == 0:
            tb["link"] = link_url
        ops.append(tb)

    ops.extend([
        {"op": "add-shape", "slide": slide_id, "shape_type": "RECTANGLE", "x": 40, "y": 334, "width": 642, "height": 2, "background_color": "#334155"},
        {"op": "add-textbox", "slide": slide_id, "text": footer, "x": 40, "y": 346, "width": 642, "height": 30, "font_size": 11, "color": "#94A3B8", "font_family": "Roboto Mono"},
        {"op": "set-notes", "slide": slide_id, "text": notes},
    ])


def add_head_first_slide(
    ops: List[Dict[str, Any]],
    image_jobs: List[Dict[str, Any]],
    slide_id: str,
    time_slot: str,
    kicker: str,
    title: str,
    img_path: str,
    cards: List[str],
    takeaway: str,
    notes: str,
) -> None:
    ops.extend([
        {"op": "add-slide", "layout": "BLANK", "id": slide_id},
        {"op": "set-background", "slide": slide_id, "color": "#FAF6EC"},
        {"op": "add-shape", "slide": slide_id, "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 10, "height": 405, "background_color": "#F59E0B"},
        {"op": "add-textbox", "slide": slide_id, "text": kicker, "x": 28, "y": 14, "width": 664, "height": 18, "font_size": 10, "bold": True, "color": "#B45309", "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": slide_id, "text": title, "x": 28, "y": 32, "width": 664, "height": 36, "font_size": 18, "bold": True, "color": "#18181B", "font_family": "Montserrat"},
        # Head First comic shadow frame behind the 16:9 infographic
        {"op": "add-shape", "slide": slide_id, "shape_type": "RECTANGLE", "x": 32, "y": 81, "width": 424, "height": 238.5, "background_color": "#18181B"},
    ])

    ys = [76, 158, 240]
    bgs = ["#FFFFFF", "#FEF08A", "#FFFFFF"]
    for i, c_text in enumerate(cards[:3]):
        ops.append({
            "op": "add-textbox",
            "slide": slide_id,
            "text": c_text,
            "x": 466,
            "y": ys[i],
            "width": 226,
            "height": 75,
            "font_size": 10,
            "color": "#18181B",
            "background_color": bgs[i],
            "font_family": "Roboto",
            "content_alignment": "MIDDLE",
        })

    ops.extend([
        {"op": "add-textbox", "slide": slide_id, "text": takeaway, "x": 28, "y": 328, "width": 664, "height": 34, "font_size": 11, "bold": True, "color": "#FEF08A", "background_color": "#18181B", "font_family": "Roboto", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-textbox", "slide": slide_id, "text": f"The Periodic Table of Agents · Mani (Principal Architect, Google Cloud)   |   Pacing: {time_slot}", "x": 28, "y": 370, "width": 664, "height": 20, "font_size": 9, "color": "#52525B", "font_family": "Roboto Mono"},
        {"op": "set-notes", "slide": slide_id, "text": notes},
    ])

    image_jobs.append({
        "slide_placeholder": slide_id,
        "file": img_path,
        "x": 28,
        "y": 77,
        "width": 424,
        "height": 238.5,
    })


def add_demo_slide(
    ops: List[Dict[str, Any]],
    image_jobs: List[Dict[str, Any]],
    slide_id: str,
    time_slot: str,
    kicker: str,
    title: str,
    poster_path: str,
    drive_video_url: str,
    highlights: List[str],
    cmd_bar: str,
    notes: str,
) -> None:
    ops.extend([
        {"op": "add-slide", "layout": "BLANK", "id": slide_id},
        {"op": "set-background", "slide": slide_id, "color": "#0B1120"},
        {"op": "add-shape", "slide": slide_id, "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 10, "height": 405, "background_color": "#34A853"},
        {"op": "add-textbox", "slide": slide_id, "text": kicker, "x": 28, "y": 14, "width": 664, "height": 18, "font_size": 10, "bold": True, "color": "#4ADE80", "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": slide_id, "text": title, "x": 28, "y": 32, "width": 664, "height": 36, "font_size": 18, "bold": True, "color": "#FFFFFF", "font_family": "Montserrat"},
        {"op": "add-shape", "slide": slide_id, "shape_type": "RECTANGLE", "x": 26, "y": 75, "width": 428, "height": 242.5, "background_color": "#34A853"},
    ])

    ys = [76, 148, 220]
    for i, hl in enumerate(highlights[:3]):
        ops.append({
            "op": "add-textbox",
            "slide": slide_id,
            "text": hl,
            "x": 466,
            "y": ys[i],
            "width": 226,
            "height": 64,
            "font_size": 10,
            "color": "#E2E8F0",
            "background_color": "#131D33",
            "font_family": "Roboto",
            "content_alignment": "MIDDLE",
        })

    ops.extend([
        {
            "op": "add-textbox",
            "slide": slide_id,
            "text": "▶ OPEN RECORDED 1080P VIDEO (DRIVE)",
            "x": 466,
            "y": 290,
            "width": 226,
            "height": 28,
            "font_size": 9.5,
            "bold": True,
            "color": "#052E16",
            "background_color": "#4ADE80",
            "font_family": "Roboto Mono",
            "alignment": "center",
            "content_alignment": "MIDDLE",
            "link": drive_video_url,
        },
        {
            "op": "add-textbox",
            "slide": slide_id,
            "text": cmd_bar,
            "x": 28,
            "y": 328,
            "width": 664,
            "height": 34,
            "font_size": 10,
            "color": "#38BDF8",
            "background_color": "#131D33",
            "font_family": "Roboto Mono",
            "content_alignment": "MIDDLE",
        },
        {
            "op": "add-textbox",
            "slide": slide_id,
            "text": f"Live Stage Build + Pre-Recorded 1080p MP4 Backup   |   Pacing: {time_slot}",
            "x": 28,
            "y": 370,
            "width": 664,
            "height": 20,
            "font_size": 9,
            "color": "#94A3B8",
            "font_family": "Roboto Mono",
        },
        {"op": "set-notes", "slide": slide_id, "text": notes},
    ])

    image_jobs.append({
        "slide_placeholder": slide_id,
        "file": poster_path,
        "x": 28,
        "y": 77,
        "width": 424,
        "height": 238.5,
    })


def add_two_card_slide(
    ops: List[Dict[str, Any]],
    slide_id: str,
    time_slot: str,
    kicker: str,
    title: str,
    left_hdr: str,
    left_body: str,
    right_hdr: str,
    right_body: str,
    bottom_stat: str,
    notes: str,
) -> None:
    ops.extend([
        {"op": "add-slide", "layout": "BLANK", "id": slide_id},
        {"op": "set-background", "slide": slide_id, "color": "#0F172A"},
        {"op": "add-shape", "slide": slide_id, "shape_type": "RECTANGLE", "x": 0, "y": 0, "width": 10, "height": 405, "background_color": "#4285F4"},
        {"op": "add-textbox", "slide": slide_id, "text": kicker, "x": 28, "y": 14, "width": 664, "height": 18, "font_size": 10, "bold": True, "color": "#38BDF8", "font_family": "Roboto Mono"},
        {"op": "add-textbox", "slide": slide_id, "text": title, "x": 28, "y": 32, "width": 664, "height": 36, "font_size": 18, "bold": True, "color": "#FFFFFF", "font_family": "Montserrat"},
        # Left Card
        {"op": "add-textbox", "slide": slide_id, "text": left_hdr, "x": 28, "y": 78, "width": 322, "height": 34, "font_size": 13, "bold": True, "color": "#FFFFFF", "background_color": "#1E3A8A", "font_family": "Montserrat", "content_alignment": "MIDDLE"},
        {"op": "add-textbox", "slide": slide_id, "text": left_body, "x": 28, "y": 114, "width": 322, "height": 204, "font_size": 11, "color": "#E2E8F0", "background_color": "#131D33", "font_family": "Roboto", "line_spacing": 135},
        # Right Card
        {"op": "add-textbox", "slide": slide_id, "text": right_hdr, "x": 370, "y": 78, "width": 322, "height": 34, "font_size": 13, "bold": True, "color": "#FFFFFF", "background_color": "#065F46", "font_family": "Montserrat", "content_alignment": "MIDDLE"},
        {"op": "add-textbox", "slide": slide_id, "text": right_body, "x": 370, "y": 114, "width": 322, "height": 204, "font_size": 11, "color": "#E2E8F0", "background_color": "#131D33", "font_family": "Roboto", "line_spacing": 135},
        # Bottom Stat Banner
        {"op": "add-textbox", "slide": slide_id, "text": bottom_stat, "x": 28, "y": 328, "width": 664, "height": 34, "font_size": 11, "bold": True, "color": "#FDE047", "background_color": "#1E293B", "font_family": "Roboto Mono", "alignment": "center", "content_alignment": "MIDDLE"},
        {"op": "add-textbox", "slide": slide_id, "text": f"Plan Big · Execute Fast · Decide Small · Review Everything   |   Pacing: {time_slot}", "x": 28, "y": 370, "width": 664, "height": 20, "font_size": 9, "color": "#94A3B8", "font_family": "Roboto Mono"},
        {"op": "set-notes", "slide": slide_id, "text": notes},
    ])


def main() -> None:
    ops: List[Dict[str, Any]] = []
    image_jobs: List[Dict[str, Any]] = []

    # Slide 1: Hero Title
    add_hero_slide(
        ops,
        slide_id="p",
        is_first=True,
        kicker="DEVFEST 2026 KEYNOTE · 30-MINUTE LIVE ENGINEERING BUILD",
        title="The Periodic Table of Agents:\nBuilding with Gemini 4 & Antigravity",
        subtitle="How Carbon, Argon, Hydrogen, Decision-1, Live 3.8, ADK 2.0 & the Agentic Data Cloud turn prompts into shipped Pull Requests.",
        pills=["1. PLAN BIG\nCarbon & Argon", "2. EXECUTE FAST\nHydrogen + /swarm", "3. DECIDE SMALL\ngemini-decision-1", "4. REVIEW ALL\nRemote Agents + PR"],
        footer="Manikandan (Mani) · Principal Architect, Google Cloud   |   github.com/cmanikandan/gdg-blr-talk-nov14-2026",
        notes=(
            "[00:00–01:00 | HIGH ENERGY WALK-ON]\n"
            "Good morning DevFest!! Show of hands: how many of you paired with an AI coding agent this week? "
            "Keep your hand up if you closed your laptop, hopped into Bengaluru traffic, checked on that agent by voice, "
            "and came back to a verified Pull Request with 14 passing tests and zero regressions! "
            "No slideware promises today: in minute two we kick off a real build, check on it by voice mid-talk, and review the shipped PR before we wrap!"
        ),
    )

    # Slide 2: Fresh Badge Joke + 6-Month Shift (Head First #1)
    add_head_first_slide(
        ops, image_jobs,
        slide_id="SLIDE_1",
        time_slot="01:00 – 02:15",
        kicker="CONFESSIONS OF A BRAND-NEW GOOGLER · THE 6-MONTH SHIFT",
        title="From Babysitting Prompts to Autonomous Cloud Squads",
        img_path=f"{INFO_DIR}/01_hf_badge_shift.jpg",
        cards=[
            "🪪 FRESH BADGE DISCLAIMER:\nI'm so new to Google Cloud the lamination on my badge is still warm—I used Hydrogen just to find the micro-kitchen!",
            "⏪ 6 MONTHS AGO:\nSmart pair programmer chained to 1 giant slow model and your open laptop battery.",
            "⏩ TODAY:\nOne session plans with Carbon, sprints in parallel with Hydrogen, and keeps shipping in the cloud.",
        ],
        takeaway="MANTRA: Plan Big · Execute Fast · Decide Small · Review Everything",
        notes=(
            "[01:00–02:15 | LAND THE FRESH BADGE JOKE!]\n"
            "Before we run live code on stage, full disclosure: I'm a Principal Architect at Google Cloud, and I am SO new to Google "
            "that I literally just got my badge! Look at it—the ink hasn't dried, my badge photo still has hope in its eyes, and if our live demo "
            "crashes today, HR hasn't even replicated my manager ID into Spanner yet! "
            "Six months ago, AI coding meant babysitting one giant model line-by-line. Today, you orchestrate a team of specialized models."
        ),
    )

    # Slide 3: DEMO 1 (Minute-One /swarm Kickoff)
    add_demo_slide(
        ops, image_jobs,
        slide_id="SLIDE_2",
        time_slot="02:15 – 05:00",
        kicker="⚡ LIVE DEMO 1 · MINUTE-ONE ENGINEERING KICKOFF",
        title="Kick Off `/swarm` on Remote Agents — Close Your Laptop!",
        poster_path=f"{VID_DIR}/demo1_antigravity_swarm_kickoff_poster.png",
        drive_video_url=DRIVE_VIDEOS["demo1"],
        highlights=[
            "1️⃣ Attach Repo in Cloud VM:\n`agy --remote-agent` mounts GitHub + scoped OAuth handles in an isolated Google VM.",
            "2️⃣ Orchestrator + /swarm:\nCarbon writes `plan.md` & assigns non-overlapping files to 3 Hydrogen workers.",
            "3️⃣ Snap the Laptop Shut:\nDisconnect local UI—cloud VM keeps coding, testing & auditing in background!",
        ],
        cmd_bar="$ agy --remote-agent  >>  /swarm Build OmniPulse ADK 2.0 + Decisions API + Spanner Omni MCP & PR",
        notes=(
            "[02:15–05:00 | DEMO 1: KICK OFF THE REAL BUILD]\n"
            "Let's kick off our real engineering build right now! We launch `agy --remote-agent` against our DevFest GitHub repo, "
            "select `Orchestrator (Carbon)`, and run `/swarm`. Watch Carbon synthesize the repo graph, lock `plan.md`, and dispatch "
            "three parallel Hydrogen workers plus an adversarial cyber verifier. Now—watch this—we disconnect our laptop! The Remote Agent VM keeps building."
        ),
    )

    # Slide 4: Periodic Table of Agents (Head First #2)
    add_head_first_slide(
        ops, image_jobs,
        slide_id="SLIDE_3",
        time_slot="05:00 – 07:00",
        kicker="ESCAPING THE ONE-MODEL TRAP · GEMINI 4 + SPECIALISTS",
        title="Meet the Periodic Table of Agents",
        img_path=f"{INFO_DIR}/02_hf_periodic_table.jpg",
        cards=[
            "🧱 [C] CARBON (#6) & [Ar] ARGON (#18):\nDeep long-horizon reasoning across 1M-token codebases, blueprints & cyber.",
            "⚡ [H] HYDROGEN (#1):\nHigh-velocity everyday execution across 4 thinking tiers ($1.50 / 1M flat).",
            "🎯 [Dc] DECISION-1 & [Lv] LIVE 3.8:\n150ms single-pass routing ($0 out!) + voice agents that reason while speaking.",
        ],
        takeaway="GEEK BITS: Stop paying Carbon prices & latency to rename a CSS variable!",
        notes=(
            "[05:00–07:00 | THE PERIODIC TABLE MENTAL MODEL]\n"
            "Most teams fall into the One-Model Trap: they pick one model for everything, either overpaying in latency and quota for trivial edits "
            "or under-powering complex architectural refactors. Chemistry works because different elements have distinct bonding properties. "
            "Here are the 5 elements powering modern agentic architectures."
        ),
    )

    # Slide 5: Carbon & Argon Deep Dive
    add_two_card_slide(
        ops,
        slide_id="SLIDE_4",
        time_slot="07:00 – 09:00",
        kicker="PLAN BIG · FRONTIER LONG-HORIZON INTELLIGENCE",
        title="Carbon `[C]` (#6) & Argon `[Ar]` (#18) Under the Hood",
        left_hdr="🧱 Gemini 4 Carbon (`gemini-4-carbon`)",
        left_body=(
            "• 1M unified input context + up to 1M output tokens\n"
            "• #1 CursorBench 4.0, WANDR & AutomationBench (>2x lower cost)\n"
            "• 94% bug resolution across 14,000-test repos (0 regressions)\n"
            "• 0% Indirect Prompt Injection on Gray Swan IPI benchmark\n"
            "• Frontier Cyber (Fairwind) + AlphaProof Code formal proofs"
        ),
        right_hdr="🛡️ Gemini 4 Argon (`gemini-4-argon`)",
        right_body=(
            "• Noble, non-reactive workhorse for 80% of engineering work\n"
            "• Same 1M unified context & native tool ecosystem\n"
            "• Intro pricing parity: $2 / 1M input · $10 / 1M output\n"
            "• Excels at multi-package services, SQL & enterprise docs\n"
            "• Selectable directly via `Orchestrator (Argon)`"
        ),
        bottom_stat="RULE #1 — PLAN BIG: Spend deep reasoning tokens upfront where architectural mistakes are 100x costlier!",
        notes=(
            "[07:00–09:00 | CARBON & ARGON]\n"
            "Argon is your noble gas—rock-solid for 80% of daily microservices and data engineering. Carbon is your diamond-hard frontier planner: "
            "#1 on CursorBench 4.0 at half the cost per task of competitors, 94% resolution on 14k-test legacy repos with zero regressions, "
            "and the first model to hit 0% indirect prompt injection success on Gray Swan IPI!"
        ),
    )

    # Slide 6: Hydrogen Deep Dive
    add_two_card_slide(
        ops,
        slide_id="SLIDE_5",
        time_slot="09:00 – 10:30",
        kicker="EXECUTE FAST · DISCIPLINED HIGH-VELOCITY ENGINE",
        title="Hydrogen `[H]` (#1): Everyday Speed Meets Frontier Brains",
        left_hdr="⚡ Why Hydrogen (`gemini-4-hydrogen`) Wins",
        left_body=(
            "• Adapted from Carbon: $1.50 in / $7.50 out flat across 1M ctx\n"
            "• 2.5x faster than 3.8 Flash · 3.1x Terminal-Bench 4.1 (57%)\n"
            "• Natively batches parallel file-reads & code searches\n"
            "• 43/43 perfect score on PlotlyDataAnalyticsBench\n"
            "• 99.9% chain-of-thought legibility · 5x fewer fabrications"
        ),
        right_hdr="🎚️ 4 Configurable Thinking Levels",
        right_body=(
            "• `low`: Sub-second lint repairs, boilerplate & instant UI tweaks\n"
            "• `medium`: Everyday repo Q&A, unit test suites & docs\n"
            "• `high` (Default): 51 on AA Index (beats Argon's 50!)\n"
            "• `xhigh`: 54 on AA Index for surgical SWE-sweep debugging\n"
            "• Smooth cost/latency dial inside one unified model!"
        ),
        bottom_stat="PLOT TWIST: At default `high` thinking, Hydrogen surpasses Argon (51 vs 50 AA Index) at lower cost!",
        notes=(
            "[09:00–10:30 | HYDROGEN]\n"
            "Hydrogen just launched days ago and completely changes agent economics. Adapted from Carbon, it natively batches parallel file reads "
            "instead of inspecting files one-by-one, scores 43 out of 43 on PlotlyDataAnalyticsBench, and gives you 4 configurable thinking levels "
            "from `low` up to `xhigh`!"
        ),
    )

    # Slide 7: Inside Google Antigravity (Head First #3)
    add_head_first_slide(
        ops, image_jobs,
        slide_id="SLIDE_6",
        time_slot="10:30 – 12:30",
        kicker="GOOGLE ANTIGRAVITY · MULTI-MODEL & MULTI-AGENT HARNESS",
        title="Orchestrator, `/swarm`, `/teamwork` & Remote Agents",
        img_path=f"{INFO_DIR}/03_hf_antigravity_architecture.jpg",
        cards=[
            "🎼 ORCHESTRATOR:\nSwitches Carbon (Planner) ↔ Hydrogen (Workers) mid-session: -24% quota & +19% faster!",
            "🐝 /SWARM & /TEAMWORK:\nParallel workers in isolated git worktrees + Adversarial Verifier checking every diff.",
            "☁️ REMOTE AGENTS:\nIsolated Google Cloud VM + `agy-plugin-proxy` OAuth injection—ships while laptop sleeps!",
        ],
        takeaway="BENCHMARK (Terminal-Bench 4.0): Near-Carbon accuracy · 24% Less Quota · 19% Faster Completion",
        notes=(
            "[10:30–12:30 | ANTIGRAVITY ARCHITECTURE]\n"
            "Here's how Antigravity wires the Periodic Table together automatically: Orchestrator dynamically delegates planning to Carbon and execution "
            "to Hydrogen—saving 24% quota and finishing 19% faster on Terminal-Bench 4.0. `/swarm` gives each worker exclusive file ownership on a live "
            "message board so you get zero git merge conflicts, backed by an Adversarial Verifier!"
        ),
    )

    # Slide 8: Gemini Decisions API (Head First #4)
    add_head_first_slide(
        ops, image_jobs,
        slide_id="SLIDE_7",
        time_slot="12:30 – 14:00",
        kicker="DECIDE SMALL · THE LOW-LATENCY MULTIMODAL CONTROL PLANE",
        title="Gemini Decisions API (`gemini-decision-1`)",
        img_path=f"{INFO_DIR}/04_hf_decisions_api.jpg",
        cards=[
            "🚀 SINGLE FORWARD PASS:\nZero token-by-token decoding! 150–250ms E2E across text, images, audio, video & PDFs.",
            "🎛️ UP TO 1,000 QUESTIONS:\nMix `noul` (Yes/No), `choice` (2–255 routes) & `score` (ordered rubric) in 1 API call!",
            "💸 RADICAL ECONOMICS:\n$0.10 / 1M input tokens (billed once per shared input) and $0.00 OUTPUT TOKENS!",
        ],
        takeaway="5x cheaper than Flash-Lite Interactions API · Lowest calibration error across routing & safety!",
        notes=(
            "[12:30–14:00 | GEMINI DECISIONS API]\n"
            "Now let's bring this multi-model architecture into YOUR production code! Before an agent calls Carbon or touches Spanner, "
            "you have bounded decisions: Is this prompt injection? Did the user leak an API key? Which model tier fits? "
            "`gemini-decision-1` answers up to 1,000 questions in a single 150ms forward pass at $0.10/1M input and ZERO output token charges!"
        ),
    )

    # Slide 9: DEMO 2 (Decisions API Control Plane)
    add_demo_slide(
        ops, image_jobs,
        slide_id="SLIDE_8",
        time_slot="14:00 – 16:15",
        kicker="⚡ LIVE DEMO 2 · PRODUCTION ROUTING & GUARDRAILS IN 167ms",
        title="Evaluating 32 Safety & Routing Decisions (`$0` Output!)",
        poster_path=f"{VID_DIR}/demo2_decisions_api_167ms_poster.png",
        drive_video_url=DRIVE_VIDEOS["demo2"],
        highlights=[
            "🛡️ Guardrails First (162ms):\nCatches hidden prompt injection (`noul=0.99`) & raw `AKIA...` AWS keys (`0.98`).",
            "⚡ Calibrated Model Router:\nUI retry ticket → `Hydrogen` (`0.94`) | Multi-cloud spike → `Carbon` (`0.91`).",
            "🗄️ MCP Toolset Selector:\nBinds `spanner_omni_plus_iceberg` (`0.95`) only when cross-cloud correlation holds!",
        ],
        cmd_bar="$ python3 demos/omnipulse_decisions_router.py   # 167ms median vs 2,380ms LLM JSON router (13.9x faster!)",
        notes=(
            "[14:00–16:15 | DEMO 2: GEMINI DECISIONS API]\n"
            "Look at the latency race: `gemini-decision-1` finishes all 8 parallel questions in 167 milliseconds while a traditional token-decoding "
            "router takes 2.4 seconds! In 4 events—32 calibrated probabilities—we quarantine an injection, redact a leaked AWS key, route routine work "
            "to Hydrogen, and dispatch our cross-cloud outage to Carbon!"
        ),
    )

    # Slide 10: Google ADK 2.0 + Gemini 3.8 Live (Head First #5)
    add_head_first_slide(
        ops, image_jobs,
        slide_id="SLIDE_9",
        time_slot="16:15 – 18:00",
        kicker="DETERMINISTIC WORKFLOW GRAPHS + REAL-TIME VOICE",
        title="Google ADK 2.0 + Gemini 3.8 Live Extended Thinking",
        img_path=f"{INFO_DIR}/05_hf_adk2_and_live38.jpg",
        cards=[
            "🕸️ GOOGLE ADK 2.0 (GA):\nPython, TypeScript & Go `Workflow Runtime`—agents, MCP tools & functions run as `BaseNode` graphs!",
            "🔒 PRODUCTION CONTROLS:\nTyped `routes`, `isolationScope` prompt sandboxing, native `RetryConfig`, HITL pauses & A2A.",
            "🎙️ GEMINI 3.8 LIVE:\n#1 Speech-to-Speech (82.6)—reasons WHILE speaking across 97 languages + async tools!",
        ],
        takeaway="NO DEAD AIR: Voice track speaks in ~190ms while Extended Thinking runs ADK 2.0 & MCP tools in parallel!",
        notes=(
            "[16:15–18:00 | ADK 2.0 & GEMINI 3.8 LIVE]\n"
            "How do you wire these elements into deterministic enterprise production? Google ADK 2.0—now GA across Python, TypeScript, and Go! "
            "ADK 2.0 replaces brittle agent hierarchies with the `BaseNode` Workflow Graph runtime, complete with `isolationScope` and native HITL pauses. "
            "Pair that with Gemini 3.8 Live Extended Thinking, which reasons and calls async tools in the background *while* speaking naturally!"
        ),
    )

    # Slide 11: DEMO 3 (Mid-Talk Voice Check-In + Multicloud ADK)
    add_demo_slide(
        ops, image_jobs,
        slide_id="SLIDE_10",
        time_slot="18:00 – 20:30",
        kicker="⚡ LIVE DEMO 3 · MID-KEYNOTE VOICE CHECK-IN + MULTICLOUD MCP",
        title="Checking Our Remote `/swarm` Build by Voice Mid-Talk!",
        poster_path=f"{VID_DIR}/demo3_live38_voice_multicloud_adk_poster.png",
        drive_video_url=DRIVE_VIDEOS["demo3"],
        highlights=[
            "🎤 Natural Turn-Taking (190ms):\n'Let me check your remote swarm board while we talk...' (SynthID watermarked).",
            "🕸️ ADK 2.0 BaseNode Execution:\nRuns `KnowledgeCatalog` → `SpannerOmniMCP` → `IcebergLakehouse` concurrently.",
            "📉 Root Cause Resolved:\nEnvoy S3 retry storm fixed—checkout p99 drops 390ms → 13.4ms; PR #1 queued!",
        ],
        cmd_bar="$ python3 demos/omnipulse_live38_voice_checkin.py && python3 demos/omnipulse_adk2_multicloud_agent.py",
        notes=(
            "[18:00–20:30 | DEMO 3: VOICE CHECK-IN MID-TALK]\n"
            "Remember the build we started in minute two before closing the laptop? Let's check on it by voice right now! "
            "Watch the dual tracks: Gemini 3.8 Live acknowledges us in 190ms with zero awkward pause while the ADK 2.0 graph queries our Remote `/swarm` "
            "board, Knowledge Catalog, Spanner Omni across GCP and AWS, and our S3 Iceberg tables!"
        ),
    )

    # Slide 12: Google Agentic Data Cloud & Multicloud (Head First #6)
    add_head_first_slide(
        ops, image_jobs,
        slide_id="SLIDE_11",
        time_slot="20:30 – 22:30",
        kicker="GROUNDING AGENTS WHERE DATA LIVES · ZERO-COPY MULTICLOUD",
        title="Google's Agentic Data Cloud: True Multicloud Freedom",
        img_path=f"{INFO_DIR}/06_hf_agentic_data_cloud.jpg",
        cards=[
            "🌍 SPANNER OMNI (GA):\nDeploy Spanner on GCP, AWS, Azure, OCI, K8s or Laptop Docker with Software TrueTime (2M+ downloads)!",
            "🧊 BORDERLESS ICEBERG:\nBigQuery Omni queries AWS S3 & Azure Blob zero-copy; federates AWS Glue, Unity & Snowflake!",
            "🕸️ UNIFIED MULTI-MODEL:\nBigQuery Graph (GA) + Spanner Graph + Vector + Columnar Engine (200x scan speedup).",
        ],
        takeaway="ARCHITECT'S LAW: Move the agent's query to the data—never copy petabytes across clouds just to prompt!",
        notes=(
            "[20:30–22:30 | AGENTIC DATA CLOUD & MULTICLOUD]\n"
            "Every enterprise architect in Bengaluru knows reality is multicloud: your checkout app is on GCP, telemetry lands in AWS S3 Iceberg, "
            "and regulated workloads sit on-prem or Azure. With Spanner Omni now GA—using software-synchronized error-bounded TrueTime—and "
            "BigQuery's borderless Apache Iceberg lakehouse, your agents reason across AWS, Azure, and GCP without data movement!"
        ),
    )

    # Slide 13: AlloyDB Express + Knowledge Catalog + Data Agent Kit
    add_two_card_slide(
        ops,
        slide_id="SLIDE_12",
        time_slot="22:30 – 24:15",
        kicker="AGENT-SCALE DATABASES & SEMANTIC GROUNDING",
        title="AlloyDB Express, Knowledge Catalog & Data Agent Kit",
        left_hdr="🚀 AlloyDB Express & PG for Agents",
        left_body=(
            "• <2-second instance boot for coding agents' throwaway branches\n"
            "• Scale-to-zero compute ($0.00 when idle; 50 CU-hr/mo free tier)\n"
            "• Scales to 10 Billion vectors with ScaNN (6x faster than HNSW)\n"
            "• PostgreSQL for Agents: 3M+ QPS with session workload isolation\n"
            "• Join live PostgreSQL tables directly with Cloud Storage Iceberg"
        ),
        right_hdr="🧭 Knowledge Catalog + Data Agent Kit",
        right_body=(
            "• Knowledge Catalog (formerly Dataplex) maps enterprise semantics\n"
            "• Resolves verified join paths BEFORE Gemini writes SQL\n"
            "• 4x higher agent SQL accuracy · 33% lower latency · -75% tokens\n"
            "• Data Agent Kit (GA): Native MCP server for Spanner, AlloyDB, BQ\n"
            "• Plugs straight into Antigravity, ADK 2.0, and VS Code"
        ),
        bottom_stat="RESULT: Disposable <2s DB sandboxes for `/swarm` workers + 4x SQL accuracy over MCP!",
        notes=(
            "[22:30–24:15 | ALLOYDB EXPRESS & DATA AGENT KIT]\n"
            "When `/swarm` spins up 4 parallel workers, give each worker its own AlloyDB Express database in under 2 seconds that scales to $0 when done! "
            "And instead of dumping 500 table schemas into your prompt, Knowledge Catalog + Data Agent Kit over MCP gives agents 4x higher SQL accuracy "
            "with 75% fewer tokens!"
        ),
    )

    # Slide 14: Bonus Innovations ("Other Interesting Things")
    add_two_card_slide(
        ops,
        slide_id="SLIDE_13",
        time_slot="24:15 – 25:45",
        kicker="SILICON TO FORMAL PROOFS · MORE GOOGLE CLOUD FIREPOWER",
        title="TPU v8, Oracle Multicloud, Generative UI & AlphaProof Code",
        left_hdr="⚡ TPU 8t / 8i & Multicloud Bridges",
        left_body=(
            "• 8th-Gen TPUs: `TPU 8t` (training) + `TPU 8i` (agent inference)\n"
            "• Processing 16+ Billion tokens/minute via customer API calls\n"
            "• Oracle AI Database@Google Cloud: Zero-copy Gemini reasoning\n"
            "  over 97% of Fortune 100 mission-critical Oracle workloads\n"
            "• Partner Cross-Cloud Interconnect to AWS & Azure"
        ),
        right_hdr="🎨 Spatial AI & AlphaProof Code",
        right_body=(
            "• Nano Banana 2.1 + Gemini Omni 1.2 Flash multimodal skills\n"
            "• Antigravity `/generative_ui`: Inline live HTML/WebGL widgets\n"
            "• AlphaProof Code: Carbon agents wrote millions of lines of Lean\n"
            "  mathematical proofs to formally verify Signal's crypto in weeks!\n"
            "• Gemini Enterprise Agent Platform for fleet governance & IAM"
        ),
        bottom_stat="SCALE: 16B+ tokens/min on Google Cloud · Formal Lean proofs in weeks instead of years!",
        notes=(
            "[24:15–25:45 | BONUS HIGHLIGHTS]\n"
            "Four more breakthroughs worth putting on your radar: 8th-generation TPUs (`8t` & `8i`) powering 16 billion tokens a minute; "
            "Oracle AI Database@Google Cloud; Nano Banana 2.1 + `/generative_ui` for rich visual artifacts; and AlphaProof Code using Carbon "
            "to mathematically prove real-world cryptographic protocols in Lean!"
        ),
    )

    # Slide 15: DEMO 4 (Review Everything — Shipped PR #1)
    add_demo_slide(
        ops, image_jobs,
        slide_id="SLIDE_14",
        time_slot="25:45 – 28:00",
        kicker="⚡ LIVE DEMO 4 · CLOSING THE LOOP: REVIEW EVERYTHING",
        title="Re-Attach, Audit the Diff & Ship Pull Request #1!",
        poster_path=f"{VID_DIR}/demo4_review_shipped_pr_poster.png",
        drive_video_url=DRIVE_VIDEOS["demo4"],
        highlights=[
            "📄 Structured Artifact Review:\nInspect `walkthrough.md` & surgical diff—not 10,000 raw tool log lines!",
            "🕵️ Adversarial Verification:\n`verifier-cyber` confirms 14/14 pytest green, 0 regressions, 0% prompt injection.",
            "✅ Real Shipped GitHub PR #1:\nLive on `cmanikandan/gdg-blr-talk-nov14-2026`—human architect clicks Approve!",
        ],
        cmd_bar="$ agy --resume   >>   gh pr view 1 --repo cmanikandan/gdg-blr-talk-nov14-2026",
        notes=(
            "[25:45–28:00 | DEMO 4 FINALE: REVIEW THE SHIPPED PR]\n"
            "Let's bring it home! Minute 26: we re-open our session with `agy --resume`. Look at the Artifact Review pane—clean surgical diff "
            "tuning the Envoy circuit breaker and Spanner Omni stale-read fallback, 14/14 unit tests passing, adversarial cyber audit clean, "
            "and Pull Request #1 live on GitHub waiting for human sign-off. Autonomy proposes; architects verify!"
        ),
    )

    # Slide 16: Mental Model Cheat Sheet (Head First #7)
    add_head_first_slide(
        ops, image_jobs,
        slide_id="SLIDE_15",
        time_slot="28:00 – 29:15",
        kicker="MONDAY-MORNING ARCHITECTURE POSTER · PHONES OUT! 📸",
        title="The Agentic Architect Cheat Sheet",
        img_path=f"{INFO_DIR}/07_hf_mental_model_blueprint.jpg",
        cards=[
            "1️⃣ PLAN BIG (Carbon / Argon):\nInvest frontier tokens upfront on architecture, schemas & security boundaries.",
            "2️⃣ EXECUTE FAST (Hydrogen + /swarm):\nFan out parallel workers in isolated worktrees & <2s AlloyDB Express DBs.",
            "3️⃣ DECIDE SMALL + 4️⃣ REVIEW ALL:\n150ms `gemini-decision-1` gates ($0 out!) + Adversarial Verifier + Human PR!",
        ],
        takeaway="STACK: Gemini 4 (C/Ar/H) + Decision-1 + Live 3.8 + Antigravity + ADK 2.0 + Agentic Data Cloud",
        notes=(
            "[28:00–29:15 | THE CHEAT SHEET — PAUSE 5 SECONDS FOR PHOTOS]\n"
            "Pull your phones out—this is the single slide to bring to your team on Monday! "
            "Plan Big with Carbon and Argon. Execute Fast with Hydrogen and `/swarm`. Decide Small in 150ms with `gemini-decision-1`. "
            "And Review Everything with adversarial verifiers, structured artifacts, and human PR approval!"
        ),
    )

    # Slide 17: Closing CTA
    add_hero_slide(
        ops,
        slide_id="SLIDE_16",
        is_first=False,
        kicker="THANK YOU DEVFEST! · GO BUILD YOUR AGENT SQUAD",
        title="Close Your Laptop.\nKeep Shipping.",
        subtitle="All slides, Head First infographics, ADK 2.0 + Decisions API demos, 1080p videos & PR #1 are live in the GitHub repo!",
        pills=[
            "📦 GITHUB REPO\ngdg-blr-talk-nov14-2026",
            "🚀 ANTIGRAVITY\nantigravity.google",
            "🎯 AI STUDIO\naistudio.google.com",
            "🕸️ GOOGLE ADK 2.0\nadk.dev/2.0",
        ],
        footer="Manikandan (Mani) · Principal Architect, Google Cloud (Badge Age: Freshly Minted! 😄) · @cmanikandan",
        notes=(
            "[29:15–30:00 | BIG ENERGETIC FINISH]\n"
            "Everything you saw today—the 7 Head First infographics, the Decisions API router, the ADK 2.0 multicloud graph, the recorded videos, "
            "and Pull Request #1—is live on GitHub right now! Please star the repo so Google Cloud lets the new guy with the shiny 48-hour-old badge "
            "come back next DevFest! Thank you everyone—have an awesome DevFest!!"
        ),
        link_url="https://github.com/cmanikandan/gdg-blr-talk-nov14-2026",
    )

    batch_path = "/tmp/keynote_batch.json"
    with open(batch_path, "w", encoding="utf-8") as f:
        json.dump(ops, f, indent=2)

    print("1. Creating Google Slides presentation...")
    create_out = subprocess.check_output(
        ["gslides", "mutate", "create", "--title", "The Periodic Table of Agents: Building with Gemini 4 & Antigravity (DevFest Keynote)"],
        text=True,
    ).strip()
    print("Create output:", create_out)
    m = re.search(r"([a-zA-Z0-9_-]{25,})", create_out)
    if not m:
        raise RuntimeError(f"Could not parse presentation ID from: {create_out}")
    pres_id = m.group(1)
    print("PRESENTATION_ID:", pres_id)

    print("2. Applying 17-slide batch layout, cards, links & speaker notes...")
    batch_out = subprocess.check_output(
        ["gslides", "mutate", "batch", pres_id, "-f", batch_path, "--json"],
        text=True,
    )
    batch_res = json.loads(batch_out)
    resolved = batch_res.get("resolved_ids", {})
    print("Resolved slide IDs:", json.dumps(resolved, indent=2))

    print(f"3. Uploading & placing {len(image_jobs)} high-res Head First infographics & 1080p demo posters...")
    for idx, job in enumerate(image_jobs, 1):
        real_slide_id = resolved.get(job["slide_placeholder"], job["slide_placeholder"])
        rel_path = os.path.relpath(job["file"], ROOT)
        signed_url = subprocess.check_output(
            ["gh", "api", f"repos/cmanikandan/gdg-blr-talk-nov14-2026/contents/{rel_path}", "--jq", ".download_url"],
            text=True,
        ).strip()
        subprocess.check_call([
            "gslides", "mutate", "add-image", pres_id,
            "--slide", real_slide_id,
            "--url", signed_url,
            "--x", str(job["x"]),
            "--y", str(job["y"]),
            "--width", str(job["width"]),
            "--height", str(job["height"]),
        ])
        print(f"   [{idx}/{len(image_jobs)}] Inserted {os.path.basename(job['file'])} onto {job['slide_placeholder']} ({real_slide_id})")

    subprocess.check_call([
        "gslides", "mutate", "replace-all-text", pres_id,
        "--find", "`",
        "--replace", "",
    ])

    pdf_out = f"{ROOT}/presentation/Periodic_Table_of_Agents_DevFest_Keynote.pdf"
    pptx_out = f"{ROOT}/presentation/Periodic_Table_of_Agents_DevFest_Keynote.pptx"
    print("4. Exporting local PDF & PPTX backups...")
    subprocess.check_call(["gslides", "readonly", "export", pres_id, pdf_out, "--format", "pdf"])
    subprocess.check_call(["gslides", "readonly", "export", pres_id, pptx_out, "--format", "pptx"])

    meta = {
        "presentation_id": pres_id,
        "presentation_url": f"https://docs.google.com/presentation/d/{pres_id}/edit",
        "drive_videos_folder": DRIVE_VIDEOS["folder"],
        "drive_videos": DRIVE_VIDEOS,
        "resolved_slides": resolved,
    }
    with open(f"{ROOT}/presentation/google_slides_metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print("DONE! URL:", meta["presentation_url"])


if __name__ == "__main__":
    main()
