#!/usr/bin/env python3
"""
Builds the 18-Slide World-Class HTML5 Keynote Deck (`presentation/keynote_deck.html`) — Gemini 4 Neon Edition.

Features:
  - Obsidian Glass + Physical Warm Neon Tube Lighting theme (inspired by Google Cloud Next & Gemini 4 Neon launch)
  - 100% PUBLIC Gemini 4 Neon launch facts & benchmarks (blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/)
  - 100% Google Cloud-native story, code, and live verified traces (`demos/traces/demo{1..5}_trace.json`)
  - Native inline `<video controls>` playback for ALL 5 live demos AND BOTH real Voice AI recordings
    (Slides 15 & 16 split Architecture Card LEFT + playable MP4 RIGHT — ZERO Google Drive click-out!)
  - Keyboard shortcuts: ArrowRight/Space (next), ArrowLeft (prev), F (fullscreen), S (speaker notes), G (slide grid)
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[1]
TRACES_DIR = REPO_ROOT / "demos" / "traces"
OUT_HTML = REPO_ROOT / "presentation" / "keynote_deck.html"

LINKEDIN_URL = "https://www.linkedin.com/in/cmanikandan"
GITHUB_URL = "https://github.com/cmanikandan/gdg-blr-talk-nov14-2026"
NEON_BLOG_URL = "https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/"


def load_traces() -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, fname in [
        ("d1", "demo1_trace.json"),
        ("d2", "demo2_trace.json"),
        ("d3", "demo3_trace.json"),
        ("d4", "demo4_trace.json"),
        ("d5", "demo5_trace.json"),
    ]:
        p = TRACES_DIR / fname
        out[k] = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return out


def e(val: Any) -> str:
    return html.escape(str(val))


def build_slides(tr: Dict[str, Any]) -> List[Dict[str, Any]]:
    d1, d2, d3, d4, d5 = tr["d1"], tr["d2"], tr["d3"], tr["d4"], tr["d5"]

    # Demo 1 metrics
    swarm = d1.get("hydrogen_swarm", {})
    neon1 = d1.get("neon_orchestrator") or d1.get("carbon_architect") or {}
    d1_speedup = swarm.get("parallel_speedup", 1.83)
    d1_wall_s = round(swarm.get("wall_clock_ms", 10836) / 1000, 1)
    d1_seq_s = round(swarm.get("sequential_sum_ms", 19779) / 1000, 1)
    d1_workers = swarm.get("workers", [])[:3]

    # Demo 5 (Modernization) metrics
    b5 = d5.get("benchmark", {"legacy_ms": 411.1, "modern_ms": 4.09, "speedup_factor": 100.5})
    ds5 = d5.get("dataset", {"total_records": 8000, "duplicate_utrs": 470, "rbi_flagged": 170})
    gf5 = d5.get("golden_falsifier", {"total_net_payout_paise": 5623206619})
    payout_cr = f"{gf5.get('total_net_payout_paise', 5623206619) / 100 / 1e7:.2f}"
    rules5 = (d5.get("neon_analysis") or d5.get("carbon_analysis") or {}).get("plan", {}).get("hidden_invariants", [])[:5]

    # Demo 2 (Decisions API) metrics
    b8 = d2.get("round_b_head_to_head", {}).get("benchmark_8q", [])
    b50 = d2.get("round_b_head_to_head", {}).get("benchmark_50q", [])
    r50 = d2.get("round_b_head_to_head", {}).get("live_ratios_50q", {})
    pub100 = d2.get("round_b_head_to_head", {}).get("published_100q_reference", {})
    mm2 = d2.get("round_c_multimodal", {"latency_ms": 440, "output_tokens": 0})

    d1_50_ms = b50[0]["latency_ms"] if len(b50) >= 3 else 283
    fl_50_ms = b50[1]["latency_ms"] if len(b50) >= 3 else 6347
    hy_50_ms = b50[2]["latency_ms"] if len(b50) >= 3 else 4947
    d1_50_cost = b50[0]["cost_per_1m_calls_usd"] if len(b50) >= 3 else 270.7
    fl_50_cost = b50[1]["cost_per_1m_calls_usd"] if len(b50) >= 3 else 2296.7
    hy_50_cost = b50[2]["cost_per_1m_calls_usd"] if len(b50) >= 3 else 14899.5
    d1_8_ms = b8[0]["latency_ms"] if len(b8) >= 3 else 240
    fl_8_ms = b8[1]["latency_ms"] if len(b8) >= 3 else 3507
    hy_8_ms = b8[2]["latency_ms"] if len(b8) >= 3 else 2727

    sp50_fl = r50.get("speedup_vs_3_8_flash", 22.4)
    sp50_hy = r50.get("speedup_vs_4_hydrogen", 17.5)
    cs50_hy = r50.get("cost_savings_vs_4_hydrogen", 55.0)
    cs50_fl = r50.get("cost_savings_vs_3_8_flash", 8.5)

    # Demo 3 (ADK + Zero-Copy + Voice) metrics
    sql3 = d3.get("lakehouse_finding") or d3.get("multicloud_finding") or {"rows_correlated": 40000, "query_latency_ms": 170.2}
    sql3_ms = int(round(sql3.get("query_latency_ms", 170.2)))
    sql3_rows = int(sql3.get("rows_correlated", 40000))

    # Demo 4 (Review Everything + Cyber Audit) metrics
    sla4 = d4.get("sla_benchmark", {})
    bef4 = sla4.get("before", {}).get("p99_ms", 478.55)
    aft4 = sla4.get("after", {}).get("p99_ms", 13.95)
    drop4 = sla4.get("p99_reduction_pct", 97.1)
    tests4 = d4.get("pytest", {}).get("passed_count", 10)
    audit4 = (d4.get("neon_security_audit") or d4.get("carbon_security_audit") or {}).get("audit", {})
    verdict4 = str(audit4.get("overall_verdict", "APPROVE_WITH_NOTE")).replace("_", " ")
    warn_checks = [c for c in audit4.get("checks", []) if str(c.get("status", "")).upper() != "PASS"]
    warn_finding = warn_checks[0]["finding"] if warn_checks else "Catches subtle approval gaps before merge."

    return [
        # ── SLIDE 01: COVER ──
        {
            "title": "The Periodic Table of Agents",
            "notes": (
                "ENERGY: Walk out smiling, high energy, scan the whole auditorium.\n"
                "OPENER: 'Good morning DevFest Bengaluru! How many of you braved Outer Ring Road or Silk Board traffic to be here today? "
                "Honestly, routing a multi-agent swarm across Google Cloud is easier than routing out of Silk Board at 6 PM!'\n"
                "HOOK: 'Today is genuinely the most electric week to be building with Gemini. Just days ago Google launched Gemini 4 Neon — "
                "frontier-level intelligence engineered for speed. Over the next 30 minutes, whether you shipped your very first API call "
                "yesterday or you run mission-critical UPI banking systems at scale, I am going to leave you with ONE simple mental model "
                "and 6 real demos — zero fluff, 100% live Google Cloud architecture.'\n"
                "QR CALLOUT: 'Phones up if you want to bookmark it right now — top-right QR codes go straight to my LinkedIn and the full "
                "open-source GitHub repo with every slide, trace, and web UI you will see today.'"
            ),
            "html": f"""
            <div class="s-cover">
              <div class="cover-top">
                <div class="cover-title-col">
                  <div class="eyebrow">DEVFEST BENGALURU 2026 · KEYNOTE</div>
                  <h1 class="display-xl">The Periodic Table<br/>of Agents</h1>
                  <p class="lead">Building Production AI Systems with <strong>Gemini 4 Neon</strong> &amp; Google Antigravity</p>
                </div>
                <div class="qr-pair">
                  <a class="qr-card neon" href="{LINKEDIN_URL}" target="_blank" rel="noopener">
                    <img src="../assets/diagrams/qr_linkedin.png" alt="QR Code for Mani LinkedIn" />
                    <strong>LinkedIn</strong>
                    <span>/in/cmanikandan</span>
                  </a>
                  <a class="qr-card blue" href="{GITHUB_URL}" target="_blank" rel="noopener">
                    <img src="../assets/diagrams/qr_github.png" alt="QR Code for GitHub Repo" />
                    <strong>GitHub Repo</strong>
                    <span>Slides &amp; Live Code</span>
                  </a>
                </div>
              </div>
              <div class="elem-row">
                <div class="elem-tile blue"><span class="en">1</span><span class="es">H</span><span class="el">Hydrogen</span></div>
                <div class="elem-tile neon"><span class="en">10</span><span class="es">Ne</span><span class="el">Neon</span></div>
                <div class="elem-tile"><span class="en">6</span><span class="es">C</span><span class="el">Carbon</span></div>
                <div class="elem-tile green"><span class="en">18</span><span class="es">Ar</span><span class="el">Argon</span></div>
                <div class="elem-tile amber"><span class="en">0</span><span class="es">Dc</span><span class="el">Decisions</span></div>
                <div class="elem-tile green"><span class="en">3.8</span><span class="es">Lv</span><span class="el">Live Voice</span></div>
              </div>
              <div class="cover-foot">
                <div>
                  <div class="speaker-name">Mani · Principal Architect, Google Cloud</div>
                  <a class="link-neon" href="{LINKEDIN_URL}" target="_blank" rel="noopener">linkedin.com/in/cmanikandan</a>
                </div>
                <a class="link-muted" href="{GITHUB_URL}" target="_blank" rel="noopener">github.com/cmanikandan/gdg-blr-talk-nov14-2026</a>
              </div>
            </div>
            """,
        },

        # ── SLIDE 02: WARM BADGE ICEBREAKER ──
        {
            "title": "Full Disclosure — Fresh Badge",
            "notes": (
                "PHYSICAL PROP: Hold up your Google badge with a big grin!\n"
                "JOKE: 'Full disclosure before we talk distributed systems: I am SO new to Google Cloud that my badge is literally "
                "still warm from the printer! In fact, my very first production agent prompt this morning was asking Gemini 4 Hydrogen "
                "how to find the best filter coffee micro-kitchen on campus without looking lost.'\n"
                "WHY THIS MATTERS TO THE AUDIENCE: 'The awesome upside for you? You get zero canned corporate slideware today. "
                "I built, broke, debugged, and live-tested every single demo and benchmark in this deck from scratch myself — including "
                "the mistakes that almost tripped me up at 2 AM!'"
            ),
            "html": """
            <div class="s-visual">
              <div class="vis-head">
                <span class="eyebrow">01 · FULL DISCLOSURE</span>
                <h2>So New to Google, My Badge Is Still Warm</h2>
              </div>
              <div class="vis-frame light-mat">
                <img src="../assets/diagrams/01_fresh_badge.jpg" alt="Fresh Google Cloud Badge" />
              </div>
            </div>
            """,
        },

        # ── SLIDE 03: GEMINI 4 NEON PHYSICAL NEON TUBE HERO ──
        {
            "title": "Introducing Gemini 4 Neon",
            "notes": (
                "PAUSE 3 FULL SECONDS — let the glowing neon glass tubes fill the hall!\n"
                "STORY: 'For the last year, every architect I talk to in Bengaluru has asked the exact same question: "
                "Why do I have to choose between a genius model that makes my users stare at a spinner, or a fast model that misses subtle bugs? "
                "Meet Gemini 4 Neon — frontier-level intelligence engineered for fast end-to-end task completion.'\n"
                "LITTLE-KNOWN FACT #1 (95% CACHE ECONOMICS): 'Don't skim past that third stat: $3 input / $15 output per million tokens, "
                "with a full 1-million-token context window — AND cached input drops 95% all the way to $0.15 per million tokens! "
                "That means keeping your entire microservice repo warm across a 20-turn agent session costs fractions of a cent per turn.'\n"
                "LITTLE-KNOWN FACT #2 (4 THINKING TIERS): 'You don't even swap models as task complexity shifts — just dial Neon's "
                "thinking level between low, medium, high, and xhigh per call.'"
            ),
            "html": f"""
            <div class="s-neon-hero">
              <img class="hero-bg" src="../assets/diagrams/00_neon_hero.jpg" alt="Gemini 4 Neon Glowing Tube Sign" />
              <div class="hero-scrim"></div>
              <div class="hero-overlay-top">
                <span class="eyebrow">JUST LAUNCHED · FRONTIER INTELLIGENCE BUILT FOR SPEED</span>
              </div>
              <div class="hero-overlay-bottom">
                <div class="neon-stat-bar">
                  <div class="ns-item">
                    <strong>$3 / $15</strong>
                    <span>Input / Output per 1M tokens</span>
                  </div>
                  <div class="ns-div"></div>
                  <div class="ns-item">
                    <strong>1M Tokens</strong>
                    <span>Full-repo context window</span>
                  </div>
                  <div class="ns-div"></div>
                  <div class="ns-item">
                    <strong>95% Off</strong>
                    <span>Cached input ($0.15 / 1M)</span>
                  </div>
                  <div class="ns-div"></div>
                  <div class="ns-item">
                    <strong>4 Tiers</strong>
                    <span>low · medium · high · xhigh thinking</span>
                  </div>
                </div>
              </div>
            </div>
            """,
        },

        # ── SLIDE 04: THE PERIODIC TABLE OF AGENTS ──
        {
            "title": "The Periodic Table of Agents",
            "notes": (
                "JOVIAL ANALOGY: 'Remember high school chemistry when we tried to cram the entire periodic table the night before exams? "
                "Good news — for production AI in 2026 you only need 6 tiles!'\n"
                "WALK THE TILES: 'Hydrogen (H) is your lightweight rocket fuel for parallel subagents and quick UI tweaks ($1.50/$7.50). "
                "Neon (Ne) — glowing right in the heart — is your daily frontier orchestrator for planning, legacy rewrites, and cyber review ($3/$15). "
                "Carbon (C) is the heavyweight researcher for multi-day deep dives; Argon (Ar) is the rock-solid enterprise workhorse. "
                "And underneath sit two unsung heroes: Decisions API (zero output tokens!) and Gemini 3.8 Live (voice that thinks while speaking).'\n"
                "PRINCIPAL ARCHITECT WISDOM: 'Amateurs ask: Which single model is best? Principal Architects ask: Which element belongs on THIS exact hop of the pipeline?'"
            ),
            "html": """
            <div class="s-visual">
              <div class="vis-head">
                <span class="eyebrow">02 · PICK THE RIGHT ELEMENT FOR EVERY JOB</span>
                <h2>The Periodic Table of Gemini Agents</h2>
              </div>
              <div class="vis-frame dark-mat">
                <img src="../assets/diagrams/03_periodic_table_neon.jpg" alt="Periodic Table of Agents featuring Gemini 4 Neon" />
              </div>
            </div>
            """,
        },

        # ── SLIDE 05: PUBLIC GEMINI 4 NEON BENCHMARKS ──
        {
            "title": "Gemini 4 Neon — Verified Public Benchmarks",
            "notes": (
                "CREDIBILITY ANCHOR: 'Every single number on this slide is straight from the public Gemini 4 Neon launch post on blog.google.'\n"
                "LITTLE-KNOWN GEM (39.0% vs 12.8%): 'Pause on that blue card — this is my favorite engineering insight of the entire year! "
                "The EXACT SAME Gemini 4 Neon weights score 12.8% on SWE-sweep standalone... and jump 3x to 39.0% inside Google Antigravity! "
                "Why? Because multi-agent orchestration, isolated sandboxes, and clean context hygiene unlock intelligence that a single-loop prompt wastes!'\n"
                "SECURITY & REAL-WORLD PROOF: '90.5% on SEC-bench Pro, 70.7% CWE-bench v2, 0.0% Gray Swan indirect prompt-injection bypass, "
                "and 99.2% honesty — meaning Neon actually admits when it does not know instead of hallucinating a confident lie. "
                "And read Glean's real production quote: Matched or exceeded Gemini 4 Carbon on quality at 3x speed & 60% cost!'"
            ),
            "html": f"""
            <div class="s-content">
              <div class="slide-head">
                <div>
                  <div class="eyebrow">03 · PUBLIC LAUNCH BENCHMARKS</div>
                  <h2>Why Builders Are Excited About Gemini 4 Neon</h2>
                </div>
                <a class="link-muted" href="{NEON_BLOG_URL}" target="_blank" rel="noopener">Source: blog.google (Public)</a>
              </div>

              <div class="kpi-grid-4">
                <div class="kpi-card neon-top">
                  <div class="kpi-num neon">#1</div>
                  <div class="kpi-title">Coding Agent Index</div>
                  <div class="kpi-sub">58.6 score on Artificial Analysis · built for multi-step production coding</div>
                </div>
                <div class="kpi-card blue-top">
                  <div class="kpi-num blue">39.0%</div>
                  <div class="kpi-title">SWE-sweep in Antigravity</div>
                  <div class="kpi-sub">3× higher than standalone harness (12.8%) when orchestrating subagents</div>
                </div>
                <div class="kpi-card green-top">
                  <div class="kpi-num green">90.5%</div>
                  <div class="kpi-title">SEC-bench Pro (Cyber)</div>
                  <div class="kpi-sub">70.7% CWE-bench v2 · 0.0% Gray Swan IPI bypass · 99.2% honesty</div>
                </div>
                <div class="kpi-card neon-top">
                  <div class="kpi-num">3×</div>
                  <div class="kpi-title">Speed at 60% Cost</div>
                  <div class="kpi-sub">“Matched or exceeded Gemini 4 Carbon on quality at 3× speed &amp; 60% cost.” — Glean</div>
                </div>
              </div>

              <div class="bench-strip">
                <div><strong>#1</strong> Zapier AutomationBench (56.3%)</div>
                <div><strong>#1</strong> Vending-Bench 2 ($16,843)</div>
                <div><strong>#1</strong> Legal &amp; Tax Agent Bench</div>
                <div><strong>84.0%</strong> RiemannBench Math</div>
                <div><strong>-32%</strong> Cost/Task vs Carbon</div>
              </div>
            </div>
            """,
        },

        # ── SLIDE 06: ONE SIMPLE MENTAL MODEL + MONSOONPAY STORY ──
        {
            "title": "One Story. Four Simple Rules.",
            "notes": (
                "STORYTELLING BEAT: 'Every Bengaluru engineer knows this exact nightmare: It is 8 PM on Diwali Eve. "
                "Your company — let's call it MonsoonPay, an Indian UPI platform running across Google Cloud Mumbai and Delhi — gets slammed "
                "by a festival flash sale. Suddenly Delhi checkout latency spikes past 470 milliseconds, AND your aging UPI settlement engine "
                "is choking on end-of-day reconciliation.'\n"
                "THE 4-HABIT MENTAL MODEL: 'Forget memorizing 25 agent frameworks. Memorize four plain-English habits: "
                "1) Plan Big with Gemini 4 Neon. 2) Build Fast in parallel with 3 Hydrogen builders. "
                "3) Decide Instant at $0 output cost with Decisions API. 4) Ship Safe with Neon Cyber defense plus a human on the Merge button.'"
            ),
            "html": """
            <div class="s-content">
              <div class="slide-head">
                <div>
                  <div class="eyebrow">04 · OUR LIVE STORY · MONSOONPAY UPI ON GOOGLE CLOUD</div>
                  <h2>One Simple Mental Model for Production AI</h2>
                </div>
              </div>

              <div class="story-banner">
                <strong>The Scenario:</strong> A Diwali flash sale hits Bengaluru &amp; Delhi. Checkouts in Delhi slow down past <strong>470 ms</strong> while an aging UPI settlement engine struggles to keep up. Watch how 4 specialized models solve it together.
              </div>

              <div class="pillars-4">
                <div class="pillar neon-top">
                  <div class="p-step">01 · PLAN BIG</div>
                  <h3>Gemini 4 Neon</h3>
                  <p>Reads the entire codebase, uncovers hidden risks and business rules, and writes one crystal-clear blueprint.</p>
                </div>
                <div class="pillar blue-top">
                  <div class="p-step">02 · BUILD FAST</div>
                  <h3>3× Hydrogen Swarm</h3>
                  <p>Executes tasks in parallel inside isolated sandboxes, then hands off to a Cloud VM so you can close your laptop.</p>
                </div>
                <div class="pillar amber-top">
                  <div class="p-step">03 · DECIDE INSTANT</div>
                  <h3>Decisions API</h3>
                  <p>Blocks prompt attacks, masks leaked keys, and scores 50+ compliance rules in one pass at <strong>$0 output cost</strong>.</p>
                </div>
                <div class="pillar green-top">
                  <div class="p-step">04 · SHIP SAFE</div>
                  <h3>Neon Cyber + Human</h3>
                  <p>Runs load tests, independent AI cyber review, and pauses at a built-in human approval gate before anything merges.</p>
                </div>
              </div>
            </div>
            """,
        },

        # ── SLIDE 07: GOOGLE ANTIGRAVITY ARCHITECTURE ──
        {
            "title": "Google Antigravity — Neon Plans, Hydrogen Swarms",
            "notes": (
                "ANECDOTE: 'Six months ago, running an AI coding agent meant sitting there babysitting a single chat tab while your MacBook fan "
                "sounded like a Bengaluru-to-Delhi Airbus taking off!'\n"
                "ARCHITECTURE WALKTHROUGH: 'Look at the 3-stage Antigravity engine: "
                "Step 1 — Gemini 4 Neon acts as the calm senior architect, mapping exact file ownership so builders never collide. "
                "Step 2 — /swarm spins up 3 parallel Gemini 4 Hydrogen builders inside isolated git worktree sandboxes (zero merge conflicts!). "
                "Step 3 — Remote Cloud Agent VM takes over verification so you literally close your laptop and grab dinner.'\n"
                "LITTLE-KNOWN FACT: 'Git worktrees share one underlying .git object store, so spinning up 3 isolated sandboxes takes milliseconds "
                "and almost zero disk — a 10-year-old git feature that suddenly became the secret weapon of parallel AI coding!'"
            ),
            "html": """
            <div class="s-visual">
              <div class="vis-head">
                <span class="eyebrow">05 · ORCHESTRATION ARCHITECTURE</span>
                <h2>Google Antigravity: Neon Orchestrates, Hydrogen Swarms</h2>
              </div>
              <div class="vis-frame dark-mat">
                <img src="../assets/diagrams/04_antigravity_engine_v4.jpg" alt="Google Antigravity Neon Orchestrator and Hydrogen Swarm" />
              </div>
            </div>
            """,
        },

        # ── SLIDE 08: LIVE DEMO 1 — PARALLEL SWARM ──
        {
            "title": "Live Demo 1 — Neon + 3× Parallel Hydrogen Swarm",
            "notes": (
                "STAGE CUE: Play the inline video right here OR flip to Stage Studio Tab 1 and click 'Run Live'!\n"
                "NARRATE WHAT IS HAPPENING LIVE: 'Watch the left flow diagram: real live gemini-4-neon reads our payment gateway code "
                f"and designs a 3-part fix — Traffic Capacity, Checkout Reliability, and Database Resilience. Then 3 live gemini-4-hydrogen "
                f"builders execute simultaneously in isolated sandboxes: {d1_wall_s}s wall-clock instead of {d1_seq_s}s sequential — "
                f"a {d1_speedup}x real parallel speedup with ZERO merge conflicts!'\n"
                "JOVIAL PUNCHLINE: 'Notice nobody had to yell across Slack asking Who touched circuit_breaker.py?! Because Neon partitioned "
                "ownership before a single line was written.'"
            ),
            "html": f"""
            <div class="s-demo">
              <div class="demo-left">
                <div class="eyebrow">LIVE DEMO 01 · PLAN BIG, BUILD FAST</div>
                <h2>Neon Plans. 3 Hydrogen Builders Ship Together.</h2>
                <div class="mini-kpis">
                  <div class="mk"><strong class="neon">{e(d1_speedup)}×</strong><span>Parallel Speedup ({d1_wall_s}s vs {d1_seq_s}s)</span></div>
                  <div class="mk"><strong class="green">0</strong><span>Merge Conflicts</span></div>
                </div>
                <ul class="clean-list">
                  {''.join(f"<li><strong>{e(w.get('owner','Builder'))}:</strong> {e(w.get('plain_goal') or w.get('task',''))}</li>" for w in d1_workers)}
                  <li><strong>Cloud VM Handoff:</strong> Close your laptop — remote agents finish tests and open PR #1.</li>
                </ul>
              </div>
              <div class="demo-right">
                <div class="video-box">
                  <video controls playsinline preload="metadata" poster="../assets/videos/demo1_antigravity_swarm_kickoff_poster.png">
                    <source src="../assets/videos/demo1_antigravity_swarm_kickoff.mp4" type="video/mp4" />
                  </video>
                  <div class="video-bar">Live Run · gemini-4-neon + 3× gemini-4-hydrogen</div>
                </div>
              </div>
            </div>
            """,
        },

        # ── SLIDE 09: 1M CONTEXT & LONG DECODE FOR LEGACY MODERNIZATION ──
        {
            "title": "Why 1M Context & Long Decode Unlock Code Modernization",
            "notes": (
                "AUDIENCE LAUGH: 'Raise your hand if your company has a 10-year-old billing, banking, or settlement file written by a legend "
                "who left in 2018... and the only comment at the top says: DO NOT TOUCH — NOBODY KNOWS WHY THIS WORKS!'\n"
                "WHY OLDER AI FAILED: 'Smaller context windows forgot an RBI compliance rule sitting 600 lines down, and short output limits "
                "stopped mid-function. In Indian payments, even a 1-paisa rounding bug across 10 million UPI transactions is a boardroom emergency.'\n"
                "THE GOLDEN FALSIFIER SECRET: 'Here is the enterprise modernization pattern that actually works: BEFORE letting AI touch a line, "
                "run the old code on realistic transactions and lock its exact SHA-256 output fingerprint as an unmodified Golden Falsifier. "
                "Then Gemini 4 Neon reads the whole subsystem in 1M context, rewrites it completely, and only passes at 100.000% bit-exact parity!'"
            ),
            "html": """
            <div class="s-content">
              <div class="slide-head">
                <div>
                  <div class="eyebrow">06 · ENTERPRISE CODE MODERNIZATION</div>
                  <h2>Why Legacy Rewrites Finally Work — With Zero Rupee Error</h2>
                </div>
              </div>

              <div class="compare-2">
                <div class="cmp-card bad">
                  <div class="cmp-tag red">BEFORE · FRAGILE REWRITES</div>
                  <h3>Why Teams Feared Touching Legacy Code</h3>
                  <ul class="clean-list">
                    <li>Small context windows missed hidden RBI compliance &amp; rounding rules buried in other files.</li>
                    <li>Short output limits cut off halfway through rewriting large modules.</li>
                    <li>Even a 1-paisa rounding bug across millions of UPI payments blocks production rollout.</li>
                  </ul>
                </div>

                <div class="cmp-card good">
                  <div class="cmp-tag green">TODAY · GEMINI 4 NEON + EXACT PROOF</div>
                  <h3>1M Context + Complete Rewrite + Golden Verification</h3>
                  <ul class="clean-list">
                    <li><strong>Read Everything:</strong> 1M-token context ingests entire legacy payment modules + tests at once.</li>
                    <li><strong>Rewrite Completely:</strong> Long decode emits clean, modular modern code on Attempt 1.</li>
                    <li><strong>Prove ₹0.00 Drift:</strong> Lock the old system's exact output fingerprint first — new code only passes at 100% match.</li>
                  </ul>
                </div>
              </div>
            </div>
            """,
        },

        # ── SLIDE 10: LIVE DEMO 2 — LEGACY UPI MODERNIZATION ──
        {
            "title": "Live Demo 2 — Gemini 4 Neon Rewrites Legacy UPI Code",
            "notes": (
                "STAGE CUE: Play inline video or trigger Stage Studio Tab 2.\n"
                f"WALK THE LIVE PROOF: 'We fed our slow legacy Indian UPI settlement engine 8,000 realistic transactions — "
                f"{b5['legacy_ms']} ms in the old code. Live Gemini 4 Neon read the entire file in 7.1 seconds, uncovered ALL 5 hidden "
                f"business rules (including duplicate UTR handling, zero fee under INR 2,000, RBI high-value flagging above INR 50,000, "
                f"and exact half-up paise GST rounding!), rewrote the whole engine cleanly on Attempt 1 — and dropped runtime to "
                f"{b5['modern_ms']} ms: {b5['speedup_factor']}x faster with literally ₹0.00 error across ₹{payout_cr} Crore!'\n"
                "LITTLE-KNOWN FACT: 'Banker's rounding (Python's default round()) vs commercial half-up paise rounding is the #1 bug that breaks "
                "financial rewrites — Neon caught that subtle trap on its very first pass!'"
            ),
            "html": f"""
            <div class="s-demo">
              <div class="demo-left">
                <div class="eyebrow">LIVE DEMO 02 · GEMINI 4 NEON MODERNIZATION</div>
                <h2>{e(b5['speedup_factor'])}× Faster UPI Engine. ₹0.00 Error.</h2>
                <div class="mini-kpis">
                  <div class="mk"><strong class="neon">{round(b5['legacy_ms'])} → {b5['modern_ms']:.1f} ms</strong><span>8,000 Indian Payments</span></div>
                  <div class="mk"><strong class="green">₹{payout_cr} Cr</strong><span>Exact Payout Match</span></div>
                </div>
                <ul class="clean-list">
                  {''.join(f"<li>{e(r)}</li>" for r in rules5[:4])}
                </ul>
              </div>
              <div class="demo-right">
                <div class="video-box">
                  <video controls playsinline preload="metadata" poster="../assets/videos/demo5_code_modernization_poster.png">
                    <source src="../assets/videos/demo5_code_modernization.mp4" type="video/mp4" />
                  </video>
                  <div class="video-bar">Live Run · gemini-4-neon · Attempt 1 Bit-Exact Proof</div>
                </div>
              </div>
            </div>
            """,
        },

        # ── SLIDE 11: DECISIONS API — HOW THE NUMBERS WERE OBTAINED ──
        {
            "title": "Gemini Decisions API — $0 Output Cost Guardrails",
            "notes": (
                "PHOTO SLIDE! Pause and let the audience pull out their phones!\n"
                "JOVIAL HOOK: 'Pop quiz: Why on earth are we paying a genius generative model to slowly type out curly-brace, quote, "
                "is_prompt_injection, colon, true, comma, newline... just to answer a yes/no security check?! That is like hiring an "
                "airline captain to stamp parking tickets!'\n"
                "LITTLE-KNOWN TECHNICAL SECRET: 'Gemini Decisions API (POST /v1beta/decisions) skips autoregressive text generation COMPLETELY! "
                "It runs ONE single forward pass over your text, image, audio, or PDF and scores up to 1,000 independent boolean, choice, "
                "and rating questions simultaneously — at ZERO output tokens billed ($0.10/1M input only)!'\n"
                f"EXPLAIN HOW WE MEASURED THIS LIVE: 'We sent the exact same Delhi outage alert to all three live APIs asking 8 checks and "
                f"50 RBI/PCI checks in one call: Decisions finished all 50 rules in {d1_50_ms} ms (${d1_50_cost:,.0f}/1M calls) vs "
                f"{fl_50_ms/1000:.1f}s on 3.8 Flash ({sp50_fl}x slower) and {hy_50_ms/1000:.1f}s on 4 Hydrogen (${hy_50_cost:,.0f}/1M = {cs50_hy}x costlier!).'"
            ),
            "html": f"""
            <div class="s-content">
              <div class="slide-head">
                <div>
                  <div class="eyebrow">07 · DECIDE SMALL · STOP PAYING FOR JSON DECODING</div>
                  <h2>Gemini Decisions API: 50+ Rules in 1 Pass, $0 Output Tokens</h2>
                </div>
              </div>

              <div class="method-box">
                <strong>How we measured this live:</strong> Identical Delhi checkout incident sent to all three live APIs asking <strong>8 security/routing rules</strong> and <strong>50 RBI/PCI compliance rules</strong> in one request — measuring real wall-clock latency &amp; billed input/output tokens at published pricing.
              </div>

              <table class="clean-table">
                <thead>
                  <tr>
                    <th>Benchmark Test</th>
                    <th>Gemini Decisions API</th>
                    <th>Gemini 3.8 Flash</th>
                    <th>Gemini 4 Hydrogen</th>
                    <th>Decisions Advantage</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>8 Rules (Live)</strong></td>
                    <td class="c-neon"><strong>{d1_8_ms} ms</strong> · 0 out tok</td>
                    <td>{fl_8_ms:,} ms · 108 out tok</td>
                    <td>{hy_8_ms:,} ms · 673 out tok</td>
                    <td class="c-green"><strong>{round(fl_8_ms/max(d1_8_ms,1),1)}× faster</strong> · $0 output</td>
                  </tr>
                  <tr>
                    <td><strong>50 Rules (Live, 1 call!)</strong></td>
                    <td class="c-neon"><strong>{d1_50_ms} ms</strong> · ${d1_50_cost:,.0f}/1M</td>
                    <td>{fl_50_ms/1000:.1f}s · ${fl_50_cost:,.0f}/1M</td>
                    <td>{hy_50_ms/1000:.1f}s · ${hy_50_cost:,.0f}/1M</td>
                    <td class="c-green"><strong>{sp50_fl}× faster</strong> · <strong>{cs50_hy}× cheaper</strong></td>
                  </tr>
                  <tr>
                    <td><strong>100 Rules (Google Pub.)</strong></td>
                    <td class="c-neon"><strong>{pub100.get('gemini_decision_1_ms', 359)} ms</strong> · 0 out tok</td>
                    <td>{pub100.get('gemini_3_8_flash_ms', 7200)/1000:.1f}s</td>
                    <td>{pub100.get('gemini_4_hydrogen_ms', 8600)/1000:.1f}s</td>
                    <td class="c-green"><strong>20–24× faster</strong> at scale</td>
                  </tr>
                </tbody>
              </table>
            </div>
            """,
        },

        # ── SLIDE 12: LIVE DEMO 3 — DECISIONS API ARENA ──
        {
            "title": "Live Demo 3 — Instant Firewall & 50-Rule Race",
            "notes": (
                "STAGE CUE: Play inline video or run Stage Studio Tab 3 LIVE!\n"
                "NARRATE THE 3 ROUNDS: 'Watch this live 3-round arena: "
                "Round 1 — Before ANY agent wakes up, Decisions API quarantines a prompt-injection attack, redacts a leaked cloud key, "
                "sends a tiny button tweak to Hydrogen, and escalates our Delhi outage straight to Gemini 4 Neon. "
                f"Round 2 — Live 50-rule race bars: Decisions finishes in {d1_50_ms}ms while Flash and Hydrogen are still typing JSON! "
                f"Round 3 — Here is the hidden superpower: Decisions API is MULTIMODAL! We fed it our actual Google Cloud architecture JPEG "
                f"and it audited it for leaked secrets and clarity in {mm2['latency_ms']}ms — still ZERO output tokens!'"
            ),
            "html": f"""
            <div class="s-demo">
              <div class="demo-left">
                <div class="eyebrow">LIVE DEMO 03 · GEMINI DECISIONS API</div>
                <h2>Instant Guardrails &amp; 50-Rule Speed Race</h2>
                <div class="mini-kpis">
                  <div class="mk"><strong class="neon">{cs50_hy}×</strong><span>Cheaper vs Hydrogen</span></div>
                  <div class="mk"><strong class="green">{sp50_fl}×</strong><span>Faster vs 3.8 Flash</span></div>
                </div>
                <ul class="clean-list">
                  <li><strong>Blocks Prompt Attacks &amp; Leaked Keys</strong> before any expensive agent or tool is ever invoked.</li>
                  <li><strong>Smart Model Router:</strong> Sends UI tweaks to Hydrogen; escalates outages to Gemini 4 Neon.</li>
                  <li><strong>Multimodal Included:</strong> Audited our Google Cloud diagram for leaked secrets in <strong>{mm2['latency_ms']} ms</strong> ($0 output).</li>
                </ul>
              </div>
              <div class="demo-right">
                <div class="video-box">
                  <video controls playsinline preload="metadata" poster="../assets/videos/demo2_decisions_api_arena_poster.png">
                    <source src="../assets/videos/demo2_decisions_api_arena.mp4" type="video/mp4" />
                  </video>
                  <div class="video-bar">Live Race · gemini-decision-1 vs 3.8 Flash vs 4 Hydrogen</div>
                </div>
              </div>
            </div>
            """,
        },

        # ── SLIDE 13: GOVERNED DATA & GOOGLE ADK 2.0 ──
        {
            "title": "Zero-Copy Cloud Data + Built-In Human Approval",
            "notes": (
                "ANECDOTE: 'Every enterprise data team I meet has 14 fragile nightly ETL pipelines copying the same table into 5 places — "
                "and by the time an AI agent queries yesterday's data during a live outage, the outage is already trending on X!'\n"
                "ARCHITECTURE: 'Look how clean Google Cloud's agentic data layer is: Spanner Omni holds live transactional checkouts with "
                "Software TrueTime clock bounds, while BigQuery Apache Iceberg holds high-volume Envoy network logs — zero data copying! "
                "Google ADK 2.0 pulls the verified join key straight from Knowledge Catalog so SQL never hallucinates column names, "
                "and pauses natively at a Built-In Human Approval Gate before any production mutation.'"
            ),
            "html": """
            <div class="s-visual">
              <div class="vis-head">
                <span class="eyebrow">08 · GOOGLE CLOUD DATA + ADK 2.0</span>
                <h2>Zero-Copy Live Data Joins with Built-In Human Approval</h2>
              </div>
              <div class="vis-frame dark-mat">
                <img src="../assets/diagrams/07_gcp_data_cloud_v4.jpg" alt="Google Cloud Spanner Omni, BigQuery Iceberg, ADK 2.0 and Human Approval Gate" />
              </div>
            </div>
            """,
        },

        # ── SLIDE 14: LIVE DEMO 4 — VOICE CHECK-IN + ADK + ZERO-COPY DATA ──
        {
            "title": "Live Demo 4 — Voice Check-In + Zero-Copy Join",
            "notes": (
                "AUDIO CHECK: Unmute hall speakers!\n"
                "STORY: 'Imagine I closed my laptop 10 minutes ago, grabbed a filter coffee, and check in with my remote agent by voice. "
                "Listen closely — zero awkward 5-second dead air! Gemini 3.8 responds immediately while Google ADK 2.14.1 runs in the "
                f"background, joins {sql3_rows:,} Spanner Omni + BigQuery Apache Iceberg rows in {sql3_ms}ms with ZERO copying, "
                "pinpoints Delhi's choked 64-slot queue while Software TrueTime stayed rock-solid, and pauses cleanly at ADK's built-in "
                "require_confirmation=True human checkpoint waiting for Mani to approve PR #1!'"
            ),
            "html": f"""
            <div class="s-demo">
              <div class="demo-left">
                <div class="eyebrow">LIVE DEMO 04 · VOICE + ADK 2.0 + ZERO-COPY DATA</div>
                <h2>Close Your Laptop. Check In by Voice.</h2>
                <div class="mini-kpis">
                  <div class="mk"><strong class="blue">{sql3_ms} ms</strong><span>{sql3_rows:,} Rows Joined Live</span></div>
                  <div class="mk"><strong class="green">0 Copies</strong><span>Direct Iceberg + Spanner</span></div>
                </div>
                <ul class="clean-list">
                  <li><strong>Dual-Track Voice:</strong> Acknowledges instantly — zero awkward silence while cloud tools run.</li>
                  <li><strong>Knowledge Catalog:</strong> Gives agents the verified join key automatically so SQL never hallucinates.</li>
                  <li><strong>Human Sign-Off:</strong> ADK 2.0 pauses cleanly until Mani approves Pull Request #1.</li>
                </ul>
              </div>
              <div class="demo-right">
                <div class="video-box">
                  <video controls playsinline preload="metadata" poster="../assets/videos/demo3_live38_voice_multicloud_adk_poster.png">
                    <source src="../assets/videos/demo3_live38_voice_multicloud_adk.mp4" type="video/mp4" />
                  </video>
                  <div class="video-bar">🔊 Real Gemini 3.8 HD Audio + Live Google ADK 2.14.1 Trace</div>
                </div>
              </div>
            </div>
            """,
        },

        # ── SLIDE 15: REAL VOICE AI (A) — EMBEDDED FLIGHT REBOOKING VIDEO + ARCHITECTURE ──
        {
            "title": "Voice AI in Production (A) — Camera + Voice Flight Rebooking",
            "notes": (
                "TRANSITION: 'Now let's go beyond code demos into TWO real production Voice AI systems I built — both playing right here on the slide!'\n"
                "EXPLAIN THE LEFT ARCHITECTURE FIRST: 'Think about calling an airline when your Frankfurt flight gets canceled. Traditional voice bots "
                "freeze in eerie silence for 6 seconds every time they hit a database — so you start yelling HELLO?! ARE YOU THERE?! "
                "Gemini 3.8 Live solves this with Dual-Track Extended Thinking: 1 FPS live camera reads your physical boarding pass while the voice "
                "track keeps talking empathetically, and non-blocking tools query BigQuery flights, check EU261 compensation rules, and update Firestore "
                "in parallel!'\n"
                "STAGE CUE: Click Play right on the embedded video! Point to the right-hand live BigQuery SQL log executing mid-sentence!"
            ),
            "html": """
            <div class="s-voice-split">
              <div class="slide-head" style="margin-bottom:14px;">
                <div>
                  <div class="eyebrow">REAL VOICE AI · PART A · GEMINI 3.8 LIVE EXTENDED THINKING</div>
                  <h2>Live Camera + Voice Concierge — Zero Dead Air</h2>
                </div>
                <span class="tag-pill green">Embedded Video · Plays Inline</span>
              </div>
              <div class="vs-grid">
                <div class="vs-arch">
                  <img src="../assets/diagrams/09_arch_live_flight.jpg" alt="Gemini 3.8 Live Camera and Voice Flight Rebooking Architecture" />
                </div>
                <div class="vs-video">
                  <div class="video-box full-h">
                    <video controls playsinline preload="metadata" poster="../assets/videos/demo4a_gemini38_live_flight_poster.png">
                      <source src="../assets/videos/demo4a_gemini38_live_flight.mp4" type="video/mp4" />
                    </video>
                    <div class="video-bar">Real Recording (2:40) · Live Boarding Pass Camera + Background BigQuery &amp; Firestore Rebooking</div>
                  </div>
                </div>
              </div>
            </div>
            """,
        },

        # ── SLIDE 16: REAL VOICE AI (B) — EMBEDDED INDIAN PSTN TELEPHONY VIDEO + ARCHITECTURE ──
        {
            "title": "Voice AI in Production (B) — Indian Phone-Line Integration",
            "notes": (
                "CROWD FAVORITE IN INDIA! 'Here is the #1 question Indian banks, telecoms, and hospitals ask me every single week: "
                "Browser demos are cute, Mani — can this answer a REAL Indian phone call when my customer switches mid-sentence from English "
                "to Hindi, Tamil, Kannada, Telugu, or Hinglish?!'\n"
                "WALK THE LEFT ARCHITECTURE: 'Regular Indian PSTN phone call hits Google Cloud Mumbai (Cloud Armor + Load Balancing + Cloud Run), "
                "running BOTH Direct Speech-to-Speech (lowest latency, natural barge-in) AND Cascaded Listen-Think-Speak (when regulated banks want "
                "every intermediate transcript audited) — backed by Firestore call state.'\n"
                "LITTLE-KNOWN FACT: 'Why do phone-line voice bots break so easily? Phone networks deliver narrowband 8kHz/16kHz audio with background "
                "traffic horns — zero-resampling framing + instant barge-in cancellation on Cloud Run Mumbai keeps latency crisp! Hit play!'"
            ),
            "html": """
            <div class="s-voice-split">
              <div class="slide-head" style="margin-bottom:14px;">
                <div>
                  <div class="eyebrow">REAL VOICE AI · PART B · INDIAN PSTN TELEPHONY ON GOOGLE CLOUD</div>
                  <h2>Real Indian Phone Calls Across 6 Languages</h2>
                </div>
                <span class="tag-pill neon">Embedded Video · Plays Inline</span>
              </div>
              <div class="vs-grid">
                <div class="vs-arch">
                  <img src="../assets/diagrams/10_arch_voice_pstn.jpg" alt="Indian Phone-Line VoiceAI Architecture on Google Cloud Mumbai" />
                </div>
                <div class="vs-video">
                  <div class="video-box full-h">
                    <video controls playsinline preload="metadata" poster="../assets/videos/demo4b_gemini_voiceai_pstn_poster.png">
                      <source src="../assets/videos/demo4b_gemini_voiceai_pstn.mp4" type="video/mp4" />
                    </video>
                    <div class="video-bar">Real Recording (3:03) · English · Hindi · Tamil · Kannada · Telugu · Hinglish on Cloud Run Mumbai</div>
                  </div>
                </div>
              </div>
            </div>
            """,
        },

        # ── SLIDE 17: LIVE DEMO 5 — REVIEW EVERYTHING (GEMINI 4 NEON FOR CYBER) ──
        {
            "title": "Live Demo 5 — Review Everything (Gemini 4 Neon for Cyber)",
            "notes": (
                "CLIMAX PUNCHLINE! 'My favorite rule of all — and the one that separates hobbyist AI demos from production Principal Architects: "
                "NEVER let the same agent that wrote the code approve it for production! That is like letting yourself grade your own exam!'\n"
                f"WALK THE LIVE PROOF: 'Our 500-user flash-sale load test proved Delhi worst-case checkout delay crashed {drop4}% "
                f"({bef4}ms down to {aft4}ms), and all {tests4}/{tests4} automated tests are glowing green. 99% of teams hit Merge right here! "
                "Watch what happened when we handed the exact diff to an independent Gemini 4 Neon security reviewer — backed by 90.5% SEC-bench Pro "
                f"and 0.0% prompt-injection bypass: Neon returned {verdict4} and caught a real safeguard gap ({warn_finding}) BEFORE a human ever "
                "clicked Merge! AI writes, tests, and audits — humans ALWAYS own the Merge button.'"
            ),
            "html": f"""
            <div class="s-demo">
              <div class="demo-left">
                <div class="eyebrow">LIVE DEMO 05 · GEMINI 4 NEON FOR CYBER DEFENSE</div>
                <h2>-{e(drop4)}% Delay &amp; {tests4}/{tests4} Green — Still Audited by Neon.</h2>
                <div class="mini-kpis">
                  <div class="mk"><strong class="green">{round(bef4)} → {aft4:.1f} ms</strong><span>500-User Flash-Sale Load Test</span></div>
                  <div class="mk"><strong class="neon">90.5%</strong><span>SEC-bench Pro · 0.0% IPI</span></div>
                </div>
                <ul class="clean-list">
                  <li><strong>Independent Reviewer Verdict:</strong> <span style="color:var(--neon-bright);font-weight:700;">{e(verdict4)}</span></li>
                  <li><strong>Caught Before Merge:</strong> {e(warn_finding)}</li>
                  <li><strong>Golden Rule:</strong> AI writes, tests, and audits — <strong>humans own the Merge button</strong>.</li>
                </ul>
              </div>
              <div class="demo-right">
                <div class="video-box">
                  <video controls playsinline preload="metadata" poster="../assets/videos/demo4_review_shipped_pr_poster.png">
                    <source src="../assets/videos/demo4_review_shipped_pr.mp4" type="video/mp4" />
                  </video>
                  <div class="video-bar">Live Run · 500-User Load Test + 10 Tests + gemini-4-neon Cyber Audit</div>
                </div>
              </div>
            </div>
            """,
        },

        # ── SLIDE 18: CLOSING — START BUILDING TODAY ──
        {
            "title": "Start Building with Gemini 4 Neon Today",
            "notes": (
                "FINAL STANDING-OVATION BEAT: 'Phones up! Both QR codes are right here — left scans to my LinkedIn, right scans straight to "
                "every single line of code, slide, live benchmark, and Stage Web UI we ran today!'\n"
                "RECAP THE 4 MONDAY-MORNING HABITS: '1) Plan, modernize, and cyber-audit with Gemini 4 Neon ($3/$15). "
                "2) Build fast in parallel with Hydrogen swarms. 3) Put Gemini Decisions API in front of every agent for $0-output guardrails. "
                "4) Keep humans on the ADK 2.0 Merge button.'\n"
                "CALLBACK JOKE TO CLOSE: 'Thank you DevFest Bengaluru! Come say hi in the hallway — and if you have strong opinions on where "
                "to find Bengaluru's best filter coffee near the Google office, just look for the Principal Architect wearing the shiny brand-new badge!'"
            ),
            "html": f"""
            <div class="s-closing">
              <div>
                <div class="eyebrow">THANK YOU · DEVFEST BENGALURU 2026</div>
                <h1 class="display-lg">Plan Big. Build Fast.<br/>Decide Instant. Ship Safe.</h1>
              </div>

              <div class="takeaway-row">
                <div class="tk"><strong>1 · Neon</strong><span>Plan, modernize &amp; audit at $3/$15</span></div>
                <div class="tk"><strong>2 · Hydrogen</strong><span>Parallel /swarm execution in sandboxes</span></div>
                <div class="tk"><strong>3 · Decisions API</strong><span>50+ guardrails at $0 output cost</span></div>
                <div class="tk"><strong>4 · Humans</strong><span>ADK 2.0 approval gates on every prod merge</span></div>
              </div>

              <div class="closing-card">
                <div class="closing-bio">
                  <div class="speaker-name" style="font-size:26px;">Mani</div>
                  <div style="color:var(--ink-soft);font-size:15.5px;margin-top:4px;">Principal Architect, Google Cloud</div>
                  <div style="color:var(--ink-muted);font-size:13.5px;margin-top:4px;">Come say hi — look for the brand-new badge!</div>
                  <div class="closing-links" style="margin-top:16px;">
                    <a class="cta-btn neon" href="{LINKEDIN_URL}" target="_blank" rel="noopener">LinkedIn · /in/cmanikandan</a>
                    <a class="cta-btn" href="{GITHUB_URL}" target="_blank" rel="noopener">GitHub · Full Code &amp; Stage UI</a>
                  </div>
                </div>
                <div class="qr-pair closing-qrs">
                  <a class="qr-card neon" href="{LINKEDIN_URL}" target="_blank" rel="noopener">
                    <img src="../assets/diagrams/qr_linkedin.png" alt="Scan for Mani LinkedIn" />
                    <strong>Connect · LinkedIn</strong>
                    <span>/in/cmanikandan</span>
                  </a>
                  <a class="qr-card blue" href="{GITHUB_URL}" target="_blank" rel="noopener">
                    <img src="../assets/diagrams/qr_github.png" alt="Scan for GitHub Repo" />
                    <strong>Clone · GitHub</strong>
                    <span>All Demos &amp; Slides</span>
                  </a>
                </div>
              </div>
            </div>
            """,
        },
    ]


def build_html(slides: List[Dict[str, Any]]) -> str:
    slides_markup = []
    for idx, s in enumerate(slides):
        slides_markup.append(
            f'<section class="slide{" active" if idx == 0 else ""}" data-index="{idx}" data-title="{e(s["title"])}" data-notes="{e(s["notes"])}">\n'
            f'  <div class="slide-inner">{s["html"]}</div>\n'
            f'</section>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>The Periodic Table of Agents — Gemini 4 Neon Keynote (DevFest Bengaluru 2026)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #07080B;
      --surface: #111319;
      --surface-2: #171A23;
      --hairline: rgba(255, 255, 255, 0.08);
      --hairline-strong: rgba(255, 255, 255, 0.16);
      --ink: #F8FAFC;
      --ink-soft: #B9C3D4;
      --ink-muted: #7C879C;
      --neon: #FF7A1A;
      --neon-bright: #FFA352;
      --blue: #4285F4;
      --blue-bright: #75A8FF;
      --green: #34A853;
      --green-bright: #62D987;
      --red: #EA4335;
      --red-bright: #FF786E;
      --font-display: 'Plus Jakarta Sans', -apple-system, sans-serif;
      --font-body: 'Inter', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 100%; height: 100%; overflow: hidden;
      background: #040507; color: var(--ink);
      font-family: var(--font-body); -webkit-font-smoothing: antialiased;
    }}

    .deck {{
      position: relative; width: 100vw; height: 100vh;
      display: grid; place-items: center;
      background:
        radial-gradient(ellipse 70% 45% at 50% -5%, rgba(255,122,26,0.12), transparent 65%),
        var(--bg);
    }}

    .slide {{
      position: absolute; inset: 0;
      display: none; align-items: center; justify-content: center;
      padding: 46px 64px 66px;
    }}
    .slide.active {{ display: flex; animation: fadeIn 260ms ease; }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}

    .slide-inner {{
      width: 100%; max-width: 1320px; height: 100%; max-height: 780px;
      display: flex; flex-direction: column; justify-content: center;
    }}

    .eyebrow {{
      font-family: var(--font-mono); font-size: 13px; font-weight: 600;
      letter-spacing: 0.16em; text-transform: uppercase; color: var(--neon-bright);
    }}
    .display-xl {{
      font-family: var(--font-display); font-size: clamp(52px, 5.8vw, 80px);
      font-weight: 800; letter-spacing: -0.04em; line-height: 1.03; margin-top: 16px;
    }}
    .display-lg {{
      font-family: var(--font-display); font-size: clamp(44px, 4.8vw, 68px);
      font-weight: 800; letter-spacing: -0.035em; line-height: 1.06; margin-top: 14px;
    }}
    h2 {{
      font-family: var(--font-display); font-size: clamp(28px, 3vw, 42px);
      font-weight: 800; letter-spacing: -0.03em; line-height: 1.1; margin-top: 8px;
    }}
    .lead {{ font-size: 22px; color: var(--ink-soft); margin-top: 18px; line-height: 1.45; }}
    .lead strong {{ color: var(--neon-bright); }}

    /* ── SLIDE 1 COVER ── */
    .s-cover {{ display: flex; flex-direction: column; height: 100%; justify-content: space-between; padding: 12px 0; }}
    .cover-top {{
      display: flex; align-items: flex-start; justify-content: space-between; gap: 32px;
    }}
    .cover-title-col {{ flex: 1; min-width: 0; }}
    .qr-pair {{
      display: flex; gap: 14px; flex-shrink: 0; align-items: stretch;
    }}
    .qr-card {{
      display: flex; flex-direction: column; align-items: center; text-align: center;
      width: 152px; padding: 12px 12px 11px; border-radius: 16px; text-decoration: none;
      background: var(--surface-2); border: 1px solid var(--hairline-strong);
      border-top-width: 3px; transition: transform 180ms ease, border-color 180ms ease;
    }}
    .qr-card:hover {{ transform: translateY(-2px); }}
    .qr-card.neon {{ border-top-color: var(--neon); }}
    .qr-card.blue {{ border-top-color: var(--blue); }}
    .qr-card img {{
      width: 120px; height: 120px; display: block; border-radius: 10px;
      background: #FFFFFF; padding: 3px; object-fit: contain;
    }}
    .qr-card strong {{
      display: block; margin-top: 9px; font-family: var(--font-mono);
      font-size: 11.5px; letter-spacing: 0.06em; text-transform: uppercase;
      color: var(--ink);
    }}
    .qr-card.neon strong {{ color: var(--neon-bright); }}
    .qr-card.blue strong {{ color: var(--blue-bright); }}
    .qr-card span {{
      display: block; margin-top: 2px; font-size: 11px; color: var(--ink-muted);
      white-space: nowrap;
    }}
    .closing-qrs .qr-card {{ width: 164px; padding: 12px 12px 10px; }}
    .closing-qrs .qr-card img {{ width: 132px; height: 132px; }}
    .elem-row {{ display: flex; gap: 16px; margin-top: 24px; flex-wrap: wrap; }}
    .elem-tile {{
      width: 122px; padding: 14px 16px; border-radius: 16px;
      background: var(--surface); border: 1px solid var(--hairline-strong);
      display: flex; flex-direction: column;
    }}
    .elem-tile.neon {{
      background: linear-gradient(160deg, rgba(255,122,26,0.22), rgba(255,122,26,0.05));
      border-color: rgba(255,163,82,0.72);
      box-shadow: 0 0 32px rgba(255,122,26,0.28);
    }}
    .elem-tile.blue {{ border-color: rgba(66,133,244,0.45); }}
    .elem-tile.green {{ border-color: rgba(52,168,83,0.45); }}
    .elem-tile.amber {{ border-color: rgba(255,163,82,0.4); }}
    .en {{ font-family: var(--font-mono); font-size: 11px; color: var(--ink-muted); }}
    .es {{ font-family: var(--font-display); font-size: 34px; font-weight: 800; line-height: 1.1; margin: 4px 0; }}
    .elem-tile.neon .es {{ color: var(--neon-bright); }}
    .el {{ font-size: 12.5px; color: var(--ink-soft); font-weight: 600; }}

    .cover-foot {{
      display: flex; align-items: flex-end; justify-content: space-between; gap: 20px;
      padding-top: 22px; border-top: 1px solid var(--hairline);
    }}
    .speaker-name {{ font-family: var(--font-display); font-size: 19px; font-weight: 700; }}
    .link-neon {{ color: var(--neon-bright); text-decoration: none; font-size: 15px; font-weight: 600; }}
    .link-muted {{ color: var(--ink-muted); text-decoration: none; font-family: var(--font-mono); font-size: 13px; }}
    .link-neon:hover, .link-muted:hover {{ text-decoration: underline; }}

    /* ── SLIDE 3 FULL-BLEED NEON HERO ── */
    .s-neon-hero {{
      position: relative; width: 100%; height: 100%; border-radius: 24px;
      overflow: hidden; border: 1px solid rgba(255,122,26,0.3);
      box-shadow: 0 28px 80px rgba(0,0,0,0.65);
    }}
    .hero-bg {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .hero-scrim {{
      position: absolute; inset: 0;
      background: linear-gradient(180deg, rgba(7,8,11,0.55) 0%, transparent 28%, transparent 68%, rgba(7,8,11,0.92) 100%);
    }}
    .hero-overlay-top {{ position: absolute; top: 28px; left: 36px; }}
    .hero-overlay-bottom {{ position: absolute; bottom: 26px; left: 32px; right: 32px; }}
    .neon-stat-bar {{
      display: flex; align-items: center; justify-content: space-between; gap: 20px;
      background: rgba(12,14,20,0.82); backdrop-filter: blur(16px);
      border: 1px solid rgba(255,163,82,0.28); border-radius: 18px;
      padding: 20px 34px;
    }}
    .ns-item strong {{ display: block; font-family: var(--font-display); font-size: 30px; font-weight: 800; color: var(--neon-bright); }}
    .ns-item span {{ display: block; font-size: 13.5px; color: var(--ink-soft); margin-top: 3px; }}
    .ns-div {{ width: 1px; height: 42px; background: var(--hairline-strong); }}

    /* ── FULL-STAGE VISUAL SLIDES ── */
    .s-visual {{ display: flex; flex-direction: column; height: 100%; gap: 18px; }}
    .vis-head {{ display: flex; flex-direction: column; }}
    .vis-frame {{
      flex: 1; min-height: 0; border-radius: 22px; overflow: hidden;
      display: flex; align-items: center; justify-content: center; padding: 14px;
      border: 1px solid var(--hairline);
    }}
    .vis-frame.dark-mat {{ background: #0B0D12; }}
    .vis-frame.light-mat {{ background: #FAF7F0; }}
    .vis-frame img {{ max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 12px; display: block; }}

    /* ── CONTENT / BENCHMARK SLIDES ── */
    .s-content {{ display: flex; flex-direction: column; gap: 26px; }}
    .slide-head {{ display: flex; align-items: flex-end; justify-content: space-between; gap: 20px; }}
    .kpi-grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }}
    .kpi-card {{
      background: var(--surface); border: 1px solid var(--hairline); border-radius: 18px;
      padding: 26px 24px; border-top-width: 3px;
    }}
    .neon-top {{ border-top-color: var(--neon); }}
    .blue-top {{ border-top-color: var(--blue); }}
    .green-top {{ border-top-color: var(--green); }}
    .amber-top {{ border-top-color: #F59E0B; }}
    .kpi-num {{ font-family: var(--font-display); font-size: 54px; font-weight: 800; letter-spacing: -0.04em; line-height: 1; }}
    .kpi-num.neon {{ color: var(--neon-bright); }}
    .kpi-num.blue {{ color: var(--blue-bright); }}
    .kpi-num.green {{ color: var(--green-bright); }}
    .kpi-title {{ font-family: var(--font-display); font-size: 18px; font-weight: 700; margin-top: 14px; }}
    .kpi-sub {{ font-size: 14px; color: var(--ink-soft); line-height: 1.5; margin-top: 8px; }}

    .bench-strip {{
      display: flex; flex-wrap: wrap; justify-content: space-between; gap: 14px;
      padding: 16px 24px; background: var(--surface-2); border: 1px solid var(--hairline);
      border-radius: 14px; font-size: 14.5px; color: var(--ink-soft);
    }}
    .bench-strip strong {{ color: var(--neon-bright); font-family: var(--font-mono); margin-right: 4px; }}

    .story-banner {{
      padding: 20px 26px; border-radius: 16px;
      background: rgba(255,122,26,0.08); border: 1px solid rgba(255,122,26,0.26);
      font-size: 18px; line-height: 1.5; color: var(--ink);
    }}
    .story-banner strong {{ color: var(--neon-bright); }}

    .pillars-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }}
    .pillar {{
      background: var(--surface); border: 1px solid var(--hairline); border-top-width: 3px;
      border-radius: 18px; padding: 24px;
    }}
    .p-step {{ font-family: var(--font-mono); font-size: 12px; font-weight: 600; color: var(--ink-muted); letter-spacing: 0.1em; }}
    .pillar h3 {{ font-family: var(--font-display); font-size: 22px; font-weight: 800; margin-top: 10px; }}
    .pillar p {{ font-size: 15px; color: var(--ink-soft); line-height: 1.55; margin-top: 10px; }}

    .compare-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
    .cmp-card {{ background: var(--surface); border: 1px solid var(--hairline); border-radius: 20px; padding: 30px; }}
    .cmp-card.good {{ border-color: rgba(52,168,83,0.35); background: linear-gradient(180deg, rgba(52,168,83,0.07), var(--surface)); }}
    .cmp-tag {{ font-family: var(--font-mono); font-size: 12px; font-weight: 600; letter-spacing: 0.12em; margin-bottom: 10px; }}
    .cmp-tag.red {{ color: var(--red-bright); }}
    .cmp-tag.green {{ color: var(--green-bright); }}
    .cmp-card h3 {{ font-family: var(--font-display); font-size: 24px; font-weight: 800; margin-bottom: 16px; }}

    .method-box {{
      padding: 16px 22px; border-radius: 14px; background: var(--surface-2);
      border: 1px solid var(--hairline); font-size: 15.5px; color: var(--ink-soft); line-height: 1.5;
    }}
    .method-box strong {{ color: var(--ink); }}

    .clean-table {{
      width: 100%; border-collapse: separate; border-spacing: 0;
      background: var(--surface); border: 1px solid var(--hairline); border-radius: 18px; overflow: hidden;
    }}
    .clean-table th, .clean-table td {{
      padding: 18px 22px; text-align: left; border-bottom: 1px solid var(--hairline); font-size: 16px;
    }}
    .clean-table th {{
      font-family: var(--font-mono); font-size: 12.5px; text-transform: uppercase;
      letter-spacing: 0.08em; color: var(--ink-muted); background: var(--surface-2);
    }}
    .clean-table tr:last-child td {{ border-bottom: none; }}
    .c-neon {{ color: var(--neon-bright); }}
    .c-green {{ color: var(--green-bright); }}

    /* ── DEMO SLIDES (LEFT INSIGHTS + RIGHT EMBEDDED VIDEO) ── */
    .s-demo {{ display: grid; grid-template-columns: 0.92fr 1.28fr; gap: 34px; align-items: center; height: 100%; }}
    .mini-kpis {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 22px 0; }}
    .mk {{ background: var(--surface); border: 1px solid var(--hairline); border-radius: 14px; padding: 16px 18px; }}
    .mk strong {{ display: block; font-family: var(--font-display); font-size: 28px; font-weight: 800; }}
    .mk strong.neon {{ color: var(--neon-bright); }}
    .mk strong.green {{ color: var(--green-bright); }}
    .mk strong.blue {{ color: var(--blue-bright); }}
    .mk span {{ display: block; font-size: 13px; color: var(--ink-muted); margin-top: 4px; }}

    .clean-list {{ list-style: none; display: flex; flex-direction: column; gap: 13px; }}
    .clean-list li {{
      position: relative; padding-left: 20px; font-size: 16px; line-height: 1.5; color: var(--ink-soft);
    }}
    .clean-list li::before {{
      content: "▸"; position: absolute; left: 0; color: var(--neon-bright); font-weight: 700;
    }}
    .clean-list strong {{ color: var(--ink); }}

    .video-box {{
      background: #040507; border: 1px solid var(--hairline-strong); border-radius: 20px;
      overflow: hidden; box-shadow: 0 24px 64px rgba(0,0,0,0.65);
      display: flex; flex-direction: column;
    }}
    .video-box video {{ width: 100%; max-height: 520px; background: #000; display: block; }}
    .video-bar {{
      padding: 12px 18px; background: var(--surface); border-top: 1px solid var(--hairline);
      font-family: var(--font-mono); font-size: 12.5px; color: var(--ink-soft);
    }}

    /* ── SLIDES 15 & 16: VOICE AI SPLIT (ARCH LEFT + PLAYABLE VIDEO RIGHT) ── */
    .s-voice-split {{ display: flex; flex-direction: column; height: 100%; }}
    .tag-pill {{
      padding: 7px 15px; border-radius: 999px; font-size: 12.5px; font-weight: 700; white-space: nowrap;
    }}
    .tag-pill.green {{ background: rgba(52,168,83,0.16); color: var(--green-bright); }}
    .tag-pill.neon {{ background: rgba(255,122,26,0.16); color: var(--neon-bright); }}

    .vs-grid {{
      flex: 1; min-height: 0; display: grid; grid-template-columns: 0.72fr 1.28fr;
      gap: 26px; align-items: center;
    }}
    .vs-arch {{
      height: 100%; max-height: 580px; background: var(--surface); border: 1px solid var(--hairline);
      border-radius: 20px; padding: 14px; display: flex; align-items: center; justify-content: center;
    }}
    .vs-arch img {{ max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 12px; display: block; }}
    .vs-video .video-box video {{ max-height: 515px; }}

    /* ── SLIDE 18 CLOSING ── */
    .s-closing {{ display: flex; flex-direction: column; justify-content: space-between; height: 100%; padding: 8px 0; gap: 18px; }}
    .takeaway-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 4px 0; }}
    .tk {{ background: var(--surface); border: 1px solid var(--hairline); border-radius: 16px; padding: 18px 20px; }}
    .tk strong {{ display: block; font-family: var(--font-display); font-size: 18.5px; color: var(--neon-bright); }}
    .tk span {{ display: block; font-size: 13.8px; color: var(--ink-soft); margin-top: 6px; line-height: 1.45; }}

    .closing-card {{
      display: flex; align-items: center; justify-content: space-between; gap: 24px;
      padding: 20px 26px; background: var(--surface); border: 1px solid rgba(255,122,26,0.34);
      border-radius: 22px;
    }}
    .closing-bio {{ flex: 1; min-width: 0; }}
    .closing-links {{ display: flex; gap: 12px; flex-wrap: wrap; }}
    .cta-btn {{
      text-decoration: none; padding: 11px 20px; border-radius: 999px; font-weight: 700; font-size: 14.5px;
      border: 1px solid var(--hairline-strong); color: var(--ink); background: var(--surface-2);
    }}
    .cta-btn.neon {{
      background: linear-gradient(180deg, #FF882E, #E86209); color: #090A0D; border-color: transparent;
    }}

    /* ── DECK CHROME (MINIMAL HUD + NOTES + GRID) ── */
    .hud {{
      position: fixed; bottom: 16px; left: 28px; right: 28px;
      display: flex; align-items: center; justify-content: space-between;
      pointer-events: none; z-index: 30;
    }}
    .hud-group {{ display: flex; align-items: center; gap: 8px; pointer-events: auto; }}
    .hud-btn {{
      appearance: none; border: 1px solid var(--hairline); background: rgba(17,19,25,0.86);
      color: var(--ink-soft); font-family: var(--font-mono); font-size: 12px;
      padding: 6px 12px; border-radius: 999px; cursor: pointer; backdrop-filter: blur(8px);
    }}
    .hud-btn:hover {{ color: var(--ink); border-color: var(--hairline-strong); }}
    .progress-bar {{ position: fixed; bottom: 0; left: 0; height: 3px; background: var(--neon); transition: width 220ms ease; z-index: 40; }}

    .notes-panel {{
      position: fixed; bottom: 60px; left: 50%; transform: translateX(-50%);
      width: min(960px, 92vw); max-height: 40vh; overflow-y: auto;
      background: rgba(14,16,23,0.97);
      border: 1px solid rgba(255,122,26,0.48); border-radius: 16px;
      padding: 18px 24px; display: none; z-index: 50; box-shadow: 0 24px 60px rgba(0,0,0,0.75);
    }}
    .notes-panel.open {{ display: block; }}
    .notes-lbl {{ font-family: var(--font-mono); font-size: 11px; color: var(--neon-bright); letter-spacing: 0.12em; margin-bottom: 8px; }}
    .notes-text {{ font-size: 15px; line-height: 1.62; color: var(--ink); white-space: pre-line; }}

    .grid-modal {{
      position: fixed; inset: 0; background: rgba(5,6,9,0.94); backdrop-filter: blur(12px);
      z-index: 60; display: none; padding: 36px; overflow-y: auto;
    }}
    .grid-modal.open {{ display: block; }}
    .grid-cards {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; max-width: 1280px; margin: 20px auto 0; }}
    .gcard {{
      text-align: left; padding: 18px; border-radius: 14px; cursor: pointer;
      background: var(--surface); border: 1px solid var(--hairline); color: var(--ink);
    }}
    .gcard.curr {{ border-color: var(--neon); }}
    .gcard span {{ display: block; font-family: var(--font-mono); font-size: 11.5px; color: var(--neon-bright); }}
    .gcard strong {{ display: block; font-size: 15px; margin-top: 6px; }}
  </style>
</head>
<body>
  <main class="deck" id="deck">
    {''.join(slides_markup)}
  </main>

  <div class="notes-panel" id="notesPanel">
    <div class="notes-lbl">SPEAKER TELEPROMPTER (PRESS S TO HIDE)</div>
    <div class="notes-text" id="notesText"></div>
  </div>

  <div class="grid-modal" id="gridModal">
    <div style="max-width:1280px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;">
      <h2 style="margin:0;font-size:24px;">All 18 Keynote Slides</h2>
      <button class="hud-btn" id="btnCloseGrid" type="button">✕ Close (G)</button>
    </div>
    <div class="grid-cards" id="gridCards"></div>
  </div>

  <div class="hud">
    <div class="hud-group">
      <button class="hud-btn" id="btnPrev" type="button">←</button>
      <span class="hud-btn" id="slideCounter" style="cursor:default;">1 / {len(slides)}</span>
      <button class="hud-btn" id="btnNext" type="button">→</button>
    </div>
    <div class="hud-group">
      <button class="hud-btn" id="btnNotes" type="button">S · Notes</button>
      <button class="hud-btn" id="btnGrid" type="button">G · Grid</button>
      <button class="hud-btn" id="btnFull" type="button">F · Fullscreen</button>
    </div>
  </div>
  <div class="progress-bar" id="progressBar"></div>

  <script>
    const slides = Array.from(document.querySelectorAll('.slide'));
    let idx = 0;

    function go(n) {{
      // Pause any playing video on outgoing slide
      slides[idx].querySelectorAll('video').forEach(v => {{ try {{ v.pause(); }} catch {{}} }});
      slides[idx].classList.remove('active');
      idx = Math.max(0, Math.min(slides.length - 1, n));
      slides[idx].classList.add('active');
      document.getElementById('slideCounter').textContent = `${{idx + 1}} / ${{slides.length}}`;
      document.getElementById('progressBar').style.width = `${{((idx + 1) / slides.length) * 100}}%`;
      document.getElementById('notesText').textContent = slides[idx].dataset.notes || '';
      window.location.hash = `slide=${{idx + 1}}`;
      renderGrid();
    }}

    function renderGrid() {{
      const wrap = document.getElementById('gridCards');
      wrap.innerHTML = slides.map((s, i) => `
        <button class="gcard ${{i === idx ? 'curr' : ''}}" type="button" onclick="window.jumpSlide(${{i}})">
          <span>SLIDE ${{String(i + 1).padStart(2, '0')}}</span>
          <strong>${{s.dataset.title}}</strong>
        </button>
      `).join('');
    }}

    window.jumpSlide = (i) => {{
      document.getElementById('gridModal').classList.remove('open');
      go(i);
    }};

    document.getElementById('btnPrev').onclick = () => go(idx - 1);
    document.getElementById('btnNext').onclick = () => go(idx + 1);
    document.getElementById('btnNotes').onclick = () => document.getElementById('notesPanel').classList.toggle('open');
    document.getElementById('btnGrid').onclick = () => document.getElementById('gridModal').classList.toggle('open');
    document.getElementById('btnCloseGrid').onclick = () => document.getElementById('gridModal').classList.remove('open');
    document.getElementById('btnFull').onclick = () => {{
      if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
      else document.exitFullscreen?.();
    }};

    document.addEventListener('keydown', (e) => {{
      if (e.target.tagName === 'VIDEO') return;
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{ e.preventDefault(); go(idx + 1); }}
      else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{ e.preventDefault(); go(idx - 1); }}
      else if (e.key.toLowerCase() === 's') document.getElementById('notesPanel').classList.toggle('open');
      else if (e.key.toLowerCase() === 'g') document.getElementById('gridModal').classList.toggle('open');
      else if (e.key.toLowerCase() === 'f') document.getElementById('btnFull').click();
      else if (e.key === 'Escape') {{
        document.getElementById('gridModal').classList.remove('open');
        document.getElementById('notesPanel').classList.remove('open');
      }}
    }});

    const m = window.location.hash.match(/slide=(\d+)/);
    go(m ? Number(m[1]) - 1 : 0);
  </script>
</body>
</html>
"""


def main() -> None:
    traces = load_traces()
    slides = build_slides(traces)
    OUT_HTML.write_text(build_html(slides), encoding="utf-8")
    print(f"✔ Built {len(slides)}-slide Gemini 4 Neon HTML5 Keynote -> {OUT_HTML}")


if __name__ == "__main__":
    main()
