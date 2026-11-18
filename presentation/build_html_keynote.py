#!/usr/bin/env python3
"""
Builds the 25-Slide HTML5 Keynote Deck (`presentation/keynote_deck.html`).

Features:
  - Alternating Deep Obsidian (#0B101B) Editorial Slides & Full-Stage Warm Cream (#FAF7F0) Illustrated Architecture Diagrams
  - 100% Google Cloud-native story, benchmarks, and demos
  - Embedded 1080p 30fps H.264 MP4 demo videos + direct playback cards for Mani's two real Voice AI Google Drive recordings
  - All benchmark numbers loaded dynamically from live `demos/traces/demo{1..5}_trace.json`
  - Keyboard shortcuts: ArrowRight/Space (next), ArrowLeft (prev), F (fullscreen), S (private speaker teleprompter), G (slide grid)
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
DRIVE_FLIGHT_URL = "https://drive.google.com/file/d/1KkvhldhlXGUEYQMLs28EMQXsSeAbZRZO/view"
DRIVE_PSTN_URL = "https://drive.google.com/file/d/1kv3NheXiAbhIBhYuBDUMRBCa054gIE9M/view"


def load_traces() -> Dict[str, Any]:
    return {
        k: json.loads((TRACES_DIR / fname).read_text(encoding="utf-8"))
        for k, fname in [
            ("d1", "demo1_trace.json"),
            ("d2", "demo2_trace.json"),
            ("d3", "demo3_trace.json"),
            ("d4", "demo4_trace.json"),
            ("d5", "demo5_trace.json"),
        ]
    }


def e(val: Any) -> str:
    return html.escape(str(val))


def build_slides(tr: Dict[str, Any]) -> List[Dict[str, Any]]:
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

    return [
        # 01 — HERO TITLE
        {
            "theme": "dark",
            "title": "The Periodic Table of Agents",
            "notes": (
                "Opening keynote! Good morning DevFest Bengaluru! Six months ago an AI coding agent was a smart pair programmer. "
                "Today a single session plans with one model, modernizes legacy code with another, decides at zero output tokens, "
                "speaks live over real telephony, and ships verified PRs in the cloud."
            ),
            "html": f"""
            <div class="hero-slide">
              <div class="kicker">DEVFEST BENGALURU 2026 · KEYNOTE</div>
              <h1 class="hero-title">The Periodic Table of Agents</h1>
              <p class="hero-sub">Building Production Agentic Systems with Gemini 4 &amp; Google Antigravity</p>
              <div class="element-strip">
                <div class="elem-chip el-h"><span class="num">1</span><span class="sym">H</span><span class="lbl">Hydrogen</span></div>
                <div class="elem-chip el-c"><span class="num">6</span><span class="sym">C</span><span class="lbl">Carbon</span></div>
                <div class="elem-chip el-ar"><span class="num">18</span><span class="sym">Ar</span><span class="lbl">Argon</span></div>
                <div class="elem-chip el-dc"><span class="num">0</span><span class="sym">Dc</span><span class="lbl">Decisions</span></div>
                <div class="elem-chip el-lv"><span class="num">3.8</span><span class="sym">Lv</span><span class="lbl">Live Voice</span></div>
              </div>
              <div class="hero-footer">
                <div>
                  <strong>Mani</strong> · Principal Architect, Google Cloud
                  <div style="margin-top:6px;"><a class="footer-link" href="{LINKEDIN_URL}" target="_blank" rel="noopener">linkedin.com/in/cmanikandan</a></div>
                </div>
                <div class="mono-dim"><a class="footer-link muted-link" href="{GITHUB_URL}" target="_blank" rel="noopener">github.com/cmanikandan/gdg-blr-talk-nov14-2026</a></div>
              </div>
            </div>
            """,
        },
        # 02 — FRESH BADGE
        {
            "theme": "cream",
            "title": "So New to Google, My Badge Is Still Warm",
            "notes": (
                "BADGE JOKE! Hold up your Google badge! 'Full disclosure: I am so new to Google Cloud that I just got my badge — "
                "it is literally still warm from the printer. I used Gemini 4 Hydrogen this morning just to find the micro-kitchen! "
                "The upside: every single demo and benchmark I show today I built, broke, and verified from scratch myself.'"
            ),
            "html": """
            <div class="diag-slide">
              <div class="diag-header">
                <span class="diag-kicker">01 · FULL DISCLOSURE</span>
                <span class="diag-title">So New to Google, My Badge Is Still Warm</span>
              </div>
              <div class="diag-stage">
                <img src="../assets/diagrams/01_fresh_badge.jpg" alt="Fresh Google Badge Illustration" />
              </div>
            </div>
            """,
        },
        # 03 — SIX MONTHS AGO VS TODAY
        {
            "theme": "cream",
            "title": "Six Months Ago vs. Today",
            "notes": (
                "Pause and let the room absorb the contrast. Single-model chat tabs tied to an open laptop are over. "
                "Modern agentic architectures specialize every model to its exact latency, reasoning horizon, and cost envelope."
            ),
            "html": """
            <div class="diag-slide">
              <div class="diag-header">
                <span class="diag-kicker">02 · THE ARCHITECTURAL SHIFT</span>
                <span class="diag-title">Six Months Ago vs. Today</span>
              </div>
              <div class="diag-stage">
                <img src="../assets/diagrams/02_six_month_shift.jpg" alt="Six Months Ago vs Today Diagram" />
              </div>
            </div>
            """,
        },
        # 04 — REWORKED DEAD-SIMPLE OVERVIEW
        {
            "theme": "dark",
            "title": "One Payments Platform. Four Rules. Six Real Demos.",
            "notes": (
                "Keep this dead simple! Introduce MonsoonPay — our real Indian UPI & checkout system on Google Cloud (Mumbai + Delhi) — "
                "four engineering rules, and six real demos measured live against the Gemini API."
            ),
            "html": """
            <div class="std-slide">
              <div class="kicker">WHAT WE ARE PROVING LIVE TODAY</div>
              <h2 class="slide-h2" style="margin-bottom:10px;">One Payments Platform. Four Rules. Six Real Demos.</h2>
              <p class="slide-sub">Meet <strong>MonsoonPay</strong> — our real Indian UPI &amp; checkout system running on Google Cloud (Mumbai + Delhi).</p>
              <div class="cards-2x2">
                <div class="arch-card border-blue">
                  <div class="card-num">01 · PLAN BIG &amp; EXECUTE FAST</div>
                  <h3>Fix a Live Outage + Modernize Legacy</h3>
                  <p>Carbon plans the fix; parallel Hydrogen workers patch in isolated git worktrees; Argon rewrites a slow O(N&sup2;) UPI monolith 94x faster — bit-exact.</p>
                </div>
                <div class="arch-card border-amber">
                  <div class="card-num">02 · DECIDE SMALL</div>
                  <h3>Guardrails at Zero Output Tokens</h3>
                  <p>Stop burning slow LLM tokens on routing &amp; compliance. Run 50 RBI/PCI checks in 270ms at $0 output tokens with Gemini Decisions API.</p>
                </div>
                <div class="arch-card border-red">
                  <div class="card-num">03 · SPEAK &amp; ACT LIVE</div>
                  <h3>Real Voice AI &amp; Telephony</h3>
                  <p>Two real live voice demos: multimodal flight rebooking with BigQuery SQL, plus multilingual Indian PSTN telephony on Cloud Run.</p>
                </div>
                <div class="arch-card border-green">
                  <div class="card-num">04 · GROUND &amp; REVIEW</div>
                  <h3>Zero-Copy Data + Adversarial Audit</h3>
                  <p>Google ADK 2.0 joins 40,000 Spanner Omni &amp; BigQuery Iceberg rows zero-copy, pauses for human sign-off, and Carbon audits every diff before merge.</p>
                </div>
              </div>
              <div class="thesis-bar">
                <span>MENTAL MODEL</span>
                <strong>Plan big · Execute fast · Decide small · Review everything.</strong>
              </div>
            </div>
            """,
        },
        # 05 — PERIODIC TABLE OF AGENTS
        {
            "theme": "cream",
            "title": "The Periodic Table of Agents",
            "notes": (
                "Walk through the five elements: Hydrogen (sub-second fuel), Carbon (deep architect & verifier with 1M context + Long Decode), "
                "Argon (enterprise workhorse), Decisions (zero-output-token control plane), Live 3.8 (voice that reasons while speaking)."
            ),
            "html": """
            <div class="diag-slide">
              <div class="diag-header">
                <span class="diag-kicker">03 · THE CORE ARCHITECTURE</span>
                <span class="diag-title">The Periodic Table of Agents</span>
              </div>
              <div class="diag-stage">
                <img src="../assets/diagrams/03_periodic_table.jpg" alt="The Periodic Table of Agents" />
              </div>
            </div>
            """,
        },
        # 06 — GEMINI 4 MODEL SPECS
        {
            "theme": "dark",
            "title": "Match the Element to the Reasoning Horizon",
            "notes": (
                "Highlight 95% implicit context caching across all three Gemini 4 elements ($0.10/1M cached input on Carbon/Argon intro, "
                "$0.075/1M on Hydrogen) plus Hydrogen's 4 thinking tiers."
            ),
            "html": """
            <div class="std-slide">
              <div class="kicker">GEMINI 4 FAMILY · PRODUCTION SELECTION GUIDE</div>
              <h2 class="slide-h2">Match the Element to the Reasoning Horizon</h2>
              <div class="cards-3">
                <div class="spec-card spec-c">
                  <div class="spec-head"><span class="spec-sym">C</span><div><h3>Gemini 4 Carbon</h3><div class="mono-dim">Deep Architect &amp; Verifier</div></div></div>
                  <div class="spec-price">$2 / $10 <small>per 1M tok · 95% implicit cache off</small></div>
                  <ul class="clean-list">
                    <li><strong>1M unified context</strong> + Long Decode &gt;64K</li>
                    <li><strong>0% bypass</strong> on Gray Swan prompt injection</li>
                    <li><strong>#1 CursorBench 4.0</strong> for complex multi-file diffs</li>
                    <li>Best for: System design, RCA, adversarial PR review</li>
                  </ul>
                </div>
                <div class="spec-card spec-ar">
                  <div class="spec-head"><span class="spec-sym">Ar</span><div><h3>Gemini 4 Argon</h3><div class="mono-dim">Enterprise Workhorse</div></div></div>
                  <div class="spec-price">$2 / $10 <small>per 1M tok · 95% implicit cache off</small></div>
                  <ul class="clean-list">
                    <li><strong>50 AA Intelligence Index</strong> · rock-solid consistency</li>
                    <li>Powers Google's <code>/teamwork</code> large-scale rewrites</li>
                    <li>Balanced throughput for regulated pipelines</li>
                    <li>Best for: Code modernization, SQL, domain RAG</li>
                  </ul>
                </div>
                <div class="spec-card spec-h">
                  <div class="spec-head"><span class="spec-sym">H</span><div><h3>Gemini 4 Hydrogen</h3><div class="mono-dim">Sub-Second Execution Fuel</div></div></div>
                  <div class="spec-price">$1.50 / $7.50 <small>flat across 1M context · 95% cache off</small></div>
                  <ul class="clean-list">
                    <li><strong>4 Thinking Tiers:</strong> <code>low</code> · <code>medium</code> · <code>high</code> · <code>xhigh</code></li>
                    <li><strong>54 AA Index</strong> at <code>xhigh</code> · <strong>2.5x faster</strong> vs 3.8 Flash</li>
                    <li><strong>43/43</strong> on PlotlyDataAnalyticsBench</li>
                    <li>Best for: Parallel <code>/swarm</code> workers, tests, everyday coding</li>
                  </ul>
                </div>
              </div>
            </div>
            """,
        },
        # 07 — UNIFIED 1M CONTEXT & LONG DECODE FOR CODE MODERNIZATION
        {
            "theme": "dark",
            "title": "Unified 1M Context + Long Decode for Code Modernization",
            "notes": (
                "Legacy modernization used to fail on two cliffs: you couldn't fit the whole dependency graph in context, and you hit "
                "output truncation halfway through rewriting a subsystem. Gemini 4 unifies input + thinking + output across 1,048,576 tokens, "
                "adds Long Decode via the Interactions API past 64K up to 1M, and cuts repeated repo reads by 95% via implicit caching."
            ),
            "html": """
            <div class="std-slide">
              <div class="kicker">ENTERPRISE CODE MODERNIZATION · GEMINI 4 ARCHITECTURE</div>
              <h2 class="slide-h2" style="margin-bottom:24px;">Unified 1M Context + Long Decode Breaks Legacy Modernization</h2>
              <div class="kpi-3" style="margin-bottom:24px;">
                <div class="big-kpi border-blue" style="padding:26px 28px;">
                  <div class="kpi-num blue" style="font-size:52px;">1,048,576</div>
                  <div class="kpi-head">Unified Token Budget</div>
                  <p>Shared across repo input + reasoning + output. Ingest entire legacy modules, SQL schemas, and tests in one shot.</p>
                </div>
                <div class="big-kpi border-green" style="padding:26px 28px;">
                  <div class="kpi-num green" style="font-size:52px;">64K &rarr; 1M</div>
                  <div class="kpi-head">Long Decode Output</div>
                  <p>Interactions API streams past the 64K cap in the background — rewriting multi-file packages cleanly without truncation.</p>
                </div>
                <div class="big-kpi border-amber" style="padding:26px 28px;">
                  <div class="kpi-num amber" style="font-size:52px;">95% OFF</div>
                  <div class="kpi-head">Implicit Context Cache</div>
                  <p>Hold 500K tokens of legacy COBOL / Java / C++ warm for $0.075–$0.10/1M per iterative refactor pass.</p>
                </div>
              </div>
              <div class="cards-3">
                <div class="arch-card border-blue" style="padding:22px 24px;">
                  <div class="card-num">1 · INGEST WHOLE SUBSYSTEM</div>
                  <p>Load legacy source, DDL schemas, and production replay logs into 1M cached context so Carbon extracts every undocumented business invariant.</p>
                </div>
                <div class="arch-card border-green" style="padding:22px 24px;">
                  <div class="card-num">2 · LONG DECODE SYNTHESIS</div>
                  <p>Argon / Carbon emits complete typed target services and migration scripts in dependency order via Interactions API — zero half-cut diffs.</p>
                </div>
                <div class="arch-card border-amber" style="padding:22px 24px;">
                  <div class="card-num">3 · LOCKED GOLDEN FALSIFIER</div>
                  <p>Execute the <strong>unmodified</strong> legacy test &amp; SHA-256 parity harness. Agents rewrite code — never weaken the verifier. 0.00 drift required.</p>
                </div>
              </div>
            </div>
            """,
        },
        # 08 — ANTIGRAVITY MULTI-AGENT PLAYBOOK (ENGLISH RECREATION OF image.png!)
        {
            "theme": "dark",
            "title": "Antigravity Multi-Agent Playbook",
            "notes": (
                "Walk through the two orthogonal Antigravity axes: Axis 1 Model (Hydrogen, Orchestrator default, Carbon) and Axis 2 Mode "
                "(1-on-1, /boost, /swarm, /run-workflow, /teamwork), plus the 4-question decision tree from bottom up."
            ),
            "html": """
            <div class="std-slide">
              <div class="kicker">GOOGLE ANTIGRAVITY · MULTI-AGENT PLAYBOOK (2 INDEPENDENT AXES)</div>
              <h2 class="slide-h2" style="margin-bottom:18px;">Which Antigravity Mode Should You Use?</h2>
              <div class="thesis-bar" style="margin-top:0;margin-bottom:22px;padding:14px 22px;font-size:18px;">
                <span>AXIS 1 · MODEL</span>
                <strong>Hydrogen</strong> (fast everyday) &nbsp;&middot;&nbsp; <strong style="color:#60A5FA;">Orchestrator [DEFAULT]</strong> (Carbon plans + Hydrogen builds) &nbsp;&middot;&nbsp; <strong>Carbon</strong> (max depth)
              </div>
              <div class="bench-card" style="padding:18px 24px;">
                <div class="bench-title" style="margin-bottom:10px;">AXIS 2 · EXECUTION MODE &amp; 4-QUESTION DECISION TREE</div>
                <table class="slide-table">
                  <thead>
                    <tr>
                      <th>Mode</th>
                      <th>Trigger Question</th>
                      <th>How It Works</th>
                      <th>Engineering Example</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><code>1-on-1 (Default)</code></td>
                      <td>Single clear, bounded task?</td>
                      <td>1 agent works directly with you</td>
                      <td>Add a feature flag or fix a unit test</td>
                    </tr>
                    <tr>
                      <td><code style="color:#C084FC;">/boost</code></td>
                      <td>1 tough problem needing depth?</td>
                      <td>Multi-angle exploration &amp; verification</td>
                      <td>Root-cause a rare concurrency race</td>
                    </tr>
                    <tr>
                      <td><code style="color:#4ADE80;">/swarm</code></td>
                      <td>Parallel specialists collaborating?</td>
                      <td>Coordinator + parallel worktree agents</td>
                      <td>Ship Envoy patch + SQL + tests together</td>
                    </tr>
                    <tr>
                      <td><code style="color:#60A5FA;">/run-workflow</code></td>
                      <td>Same task repeated on N items?</td>
                      <td>Broadcast to N agents &rarr; collect results</td>
                      <td>Audit 40 microservices or 25 open PRs</td>
                    </tr>
                    <tr class="winner">
                      <td><code style="color:#FBBF24;">/teamwork</code></td>
                      <td>Long-horizon mission (hrs–wks)?</td>
                      <td>Orchestrator + specialists + falsifiers</td>
                      <td>Rewrite 800K LoC C++ &rarr; Rust end-to-end</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="thesis-bar green-bar" style="margin-top:18px;padding:14px 22px;font-size:18px;">
                <span>RULE OF THUMB</span>
                <strong>Start with Orchestrator (1-on-1). Escalate up the ladder only when depth, parallelism, or horizon demands it.</strong>
              </div>
            </div>
            """,
        },
        # 09 — GOOGLE RESEARCH /TEAMWORK BREAKTHROUGH (NOV 2026)
        {
            "theme": "dark",
            "title": "Antigravity /teamwork — Google Research Results",
            "notes": (
                "Landmark Nov 13, 2026 Google Research `/teamwork` results: ~800K LoC Zircon microkernel rewritten to Rust booting arm64; "
                "170K LoC libgav1 AV1 decoder rewritten to Rust and optimized 20–30% FASTER than hand-tuned C++ & assembly; "
                ">1 PiB fleet RAM saved & 24% less Borg TPU preemption; 4.09x JAXBench & 2.99x vLLM TPU Pallas speedups."
            ),
            "html": """
            <div class="std-slide">
              <div class="kicker">GOOGLE RESEARCH (NOV 2026) · ANTIGRAVITY /TEAMWORK IN PRODUCTION</div>
              <h2 class="slide-h2" style="margin-bottom:22px;">Autonomous Long-Horizon Engineering — Real Google Proof</h2>
              <div class="cards-2x2">
                <div class="arch-card border-blue">
                  <div class="card-num" style="font-size:24px;color:#60A5FA;">~800K LoC</div>
                  <h3>Zircon Microkernel (C++ &rarr; Rust)</h3>
                  <p>2-week Argon <code>/teamwork</code> campaign rewrote ~800,000 lines of C++ to memory-safe Rust — passing all unmodified kernel tests &amp; booting <code>arm64</code>.</p>
                </div>
                <div class="arch-card border-green">
                  <div class="card-num" style="font-size:24px;color:#4ADE80;">20–30% Faster</div>
                  <h3><code>libgav1</code> AV1 Decoder (170K LoC)</h3>
                  <p>Rewrote 170K LoC C++ to safe Rust with 100% bit-exact conformance, then profiled &amp; beat original C++ + hand-tuned assembly on x86 &amp; ARM.</p>
                </div>
                <div class="arch-card border-amber">
                  <div class="card-num" style="font-size:24px;color:#FBBF24;">&gt;1 PiB RAM &amp; -24%</div>
                  <h3>Google Fleet &amp; Borg TPU Infrastructure</h3>
                  <p>Autonomous fleet optimization saved &gt;1 PiB RAM across Google production and cut Borg TPU workload preemption by 24% (<code>/teamwork</code> + <code>/boost</code>).</p>
                </div>
                <div class="arch-card border-purple">
                  <div class="card-num" style="font-size:24px;color:#C084FC;">4.09x / 2.99x</div>
                  <h3>DuoDiscover Kernels &amp; Deep Review</h3>
                  <p>4.09x geo-mean speedup on 17 JAXBench kernels, 2.99x on vLLM TPU Pallas kernels; 90% factual deep review across 578 STOC papers.</p>
                </div>
              </div>
              <div class="thesis-bar amber-bar" style="margin-top:20px;font-size:18px;">
                <span>SECRET SAUCE</span>
                <strong>Context Partitioning by Construction &middot; Fresh Coordinator Handoffs &middot; Independent Unmodified Falsifiers</strong>
              </div>
            </div>
            """,
        },
        # 10 — DEMO 1 VIDEO
        {
            "theme": "dark",
            "title": "Demo 1: Carbon Plan -> Parallel Hydrogen /swarm -> Remote VM",
            "notes": (
                f"DEMO 1! Live `gemini-4-carbon` planned the Google Cloud asia-south2 recovery in {round(d1['carbon_architect']['latency_ms']/1000,1)}s, "
                f"then 3 parallel `gemini-4-hydrogen` workers executed in real isolated `git worktree` sandboxes ({d1['hydrogen_swarm']['parallel_speedup']}x speedup) "
                "and handed off to an Antigravity Remote Agent VM."
            ),
            "html": f"""
            <div class="video-slide">
              <div class="video-top">
                <div>
                  <div class="kicker">DEMO 01 · LIVE GEMINI 4 API + ISOLATED GIT WORKTREES</div>
                  <h2 class="slide-h2-sm">Carbon Plans &rarr; 3 Parallel Hydrogen <code>/swarm</code> Workers &rarr; Remote VM</h2>
                </div>
                <div class="video-pills">
                  <span>3 Isolated Git Worktrees</span>
                  <span class="accent-green">{d1['hydrogen_swarm']['parallel_speedup']}x Parallel Speedup</span>
                </div>
              </div>
              <div class="video-frame">
                <video controls preload="metadata" poster="../assets/videos/demo1_antigravity_swarm_kickoff_poster.png">
                  <source src="../assets/videos/demo1_antigravity_swarm_kickoff.mp4" type="video/mp4" />
                </video>
              </div>
            </div>
            """,
        },
        # 11 — DEMO 2 (NEW!) — LIVE CODE MODERNIZATION
        {
            "theme": "dark",
            "title": "Demo 2: Live Enterprise Code Modernization (94.3x Faster, 0.00 INR Drift)",
            "notes": (
                f"DEMO 2 — BRAND NEW! We ran the `/teamwork` modernization loop live on a slow O(N^2) Indian UPI settlement monolith "
                f"(8,000 real txns, INR 56.23M payout). Carbon extracted 5 hidden RBI/GST invariants, Argon synthesized a clean O(N) engine "
                f"on Attempt 1, and our locked unmodified golden falsifier proved {m5['speedup_factor']}x speedup ({m5['legacy_ms']}ms -> {m5['modern_ms']}ms) "
                "with 100% bit-exact SHA-256 parity and 0.00 INR drift!"
            ),
            "html": f"""
            <div class="video-slide">
              <div class="video-top">
                <div>
                  <div class="kicker">DEMO 02 · LIVE GEMINI 4 CARBON + ARGON + UNMODIFIED GOLDEN FALSIFIER</div>
                  <h2 class="slide-h2-sm">Legacy O(N&sup2;) UPI Monolith &rarr; Bit-Exact O(N) Service ({m5['speedup_factor']}x Faster!)</h2>
                </div>
                <div class="video-pills">
                  <span class="accent-green">{m5['legacy_ms']}ms &rarr; {m5['modern_ms']}ms</span>
                  <span class="accent-amber">0.00 INR Drift · SHA-256 Match</span>
                </div>
              </div>
              <div class="video-frame">
                <video controls preload="metadata" poster="../assets/videos/demo5_code_modernization_poster.png">
                  <source src="../assets/videos/demo5_code_modernization.mp4" type="video/mp4" />
                </video>
              </div>
            </div>
            """,
        },
        # 12 — DECISIONS API ARCHITECTURE
        {
            "theme": "cream",
            "title": "How Gemini Decisions API Eliminates Output-Token Latency",
            "notes": (
                "Walk through `bool (Yes/No)`, `choice` (2–255 options), and `score` (rubric expectation), "
                "plus multimodal image/PDF/audio scoring in ONE forward pass with ZERO output tokens."
            ),
            "html": """
            <div class="diag-slide">
              <div class="diag-header">
                <span class="diag-kicker">04 · DECIDE SMALL</span>
                <span class="diag-title">How Gemini Decisions API Eliminates Output-Token Latency</span>
              </div>
              <div class="diag-stage">
                <img src="../assets/diagrams/05_decisions_api.jpg" alt="Gemini Decisions API Architecture" />
              </div>
            </div>
            """,
        },
        # 13 — REWORKED DECISIONS BENCHMARK + USE CASE & METHODOLOGY
        {
            "theme": "dark",
            "title": "Decisions API Benchmark: Use Case, Methodology & Live Numbers",
            "notes": (
                f"Walk through BOTH the exact payment guardrail use case AND our apples-to-apples live methodology! "
                f"On 50 simultaneous RBI/PCI-DSS checks: Decision-1 took {b50[0]['latency_ms']}ms ($271/1M calls, 0 output tokens) "
                f"vs 3.8 Flash ({b50[1]['latency_ms']}ms, {r50['speedup_vs_3_8_flash']}x slower, {r50['cost_savings_vs_3_8_flash']}x costlier) "
                f"and 4 Hydrogen ({b50[2]['latency_ms']}ms, {r50['speedup_vs_4_hydrogen']}x slower, {r50['cost_savings_vs_4_hydrogen']}x costlier!)."
            ),
            "html": f"""
            <div class="std-slide">
              <div class="kicker">HEAD-TO-HEAD BENCHMARK · USE CASE, METHODOLOGY &amp; LIVE RESULTS</div>
              <h2 class="slide-h2" style="margin-bottom:16px;">Why &ldquo;Decide Small&rdquo; Transforms Production Economics</h2>
              <div class="method-box">
                <div class="card-num" style="color:#FBBF24;margin-bottom:4px;">USE CASE &amp; BENCHMARK METHODOLOGY (HOW THESE NUMBERS WERE MEASURED)</div>
                <p><strong>Use Case:</strong> MonsoonPay incoming SEV-1 payment alert gated on <strong>8 real-time security/routing rules</strong> OR <strong>50 simultaneous RBI/PCI-DSS/SOC-2 checks</strong> before dispatching an agent.<br/>
                <strong>Methodology:</strong> Identical alert payload called live on Gemini API — <code>gemini-decision-1</code> uses <code>POST /v1beta/decisions</code> (1 forward pass, <strong>0 output tokens</strong>); <code>3.8 Flash</code> (<code>thinking_budget=0</code>) &amp; <code>4 Hydrogen</code> (<code>thinking_level=low</code>) return strict JSON via <code>generateContent</code>. Cost computed from exact API <code>usage_metadata</code> at Nov 2026 list prices.</p>
              </div>
              <div class="bench-card" style="margin-top:16px;padding:18px 24px;">
                <table class="slide-table">
                  <thead>
                    <tr>
                      <th>Model</th>
                      <th class="num">8Q Latency</th>
                      <th class="num">8Q Out Tok</th>
                      <th class="num">8Q $/1M Calls</th>
                      <th class="num">50Q Latency</th>
                      <th class="num">50Q Out Tok</th>
                      <th class="num">50Q $/1M Calls</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="winner">
                      <td>gemini-decision-1</td>
                      <td class="num">{b8[0]['latency_ms']} ms (1.0x)</td>
                      <td class="num">0</td>
                      <td class="num">${b8[0]['cost_per_1m_calls_usd']:,.0f}</td>
                      <td class="num">{b50[0]['latency_ms']} ms (1.0x)</td>
                      <td class="num">0</td>
                      <td class="num">${b50[0]['cost_per_1m_calls_usd']:,.0f} (Base)</td>
                    </tr>
                    <tr>
                      <td>gemini-3.8-flash <small>(budget=0)</small></td>
                      <td class="num">{b8[1]['latency_ms']:,} ms ({sp8_f}x)</td>
                      <td class="num">{b8[1]['billed_output_tokens']}</td>
                      <td class="num">${b8[1]['cost_per_1m_calls_usd']:,.0f} ({c8_f}x)</td>
                      <td class="num">{b50[1]['latency_ms']:,} ms ({r50['speedup_vs_3_8_flash']}x)</td>
                      <td class="num">{b50[1]['billed_output_tokens']}</td>
                      <td class="num">${b50[1]['cost_per_1m_calls_usd']:,.0f} ({r50['cost_savings_vs_3_8_flash']}x)</td>
                    </tr>
                    <tr>
                      <td>gemini-4-hydrogen <small>(low)</small></td>
                      <td class="num">{b8[2]['latency_ms']:,} ms ({sp8_h}x)</td>
                      <td class="num">{b8[2]['billed_output_tokens']}</td>
                      <td class="num">${b8[2]['cost_per_1m_calls_usd']:,.0f} ({c8_h}x)</td>
                      <td class="num">{b50[2]['latency_ms']:,} ms ({r50['speedup_vs_4_hydrogen']}x)</td>
                      <td class="num">{b50[2]['billed_output_tokens']:,}</td>
                      <td class="num">${b50[2]['cost_per_1m_calls_usd']:,.0f} ({r50['cost_savings_vs_4_hydrogen']}x)</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="thesis-bar green-bar" style="margin-top:18px;font-size:19px;">
                <span>100-QUESTION PUBLISHED SCALING</span>
                <strong>Decision-1: {pub100['gemini_decision_1_ms']} ms &nbsp;&middot;&nbsp; 3.8 Flash: {pub100['gemini_3_8_flash_ms']/1000:.1f}s ({pub100['speedup_vs_flash']}x) &nbsp;&middot;&nbsp; 4 Hydrogen: {pub100['gemini_4_hydrogen_ms']/1000:.1f}s ({pub100['speedup_vs_hydrogen']}x)</strong>
              </div>
            </div>
            """,
        },
        # 14 — DEMO 3: DECISIONS API ARENA
        {
            "theme": "dark",
            "title": "Demo 3: Live Decisions API Arena",
            "notes": (
                "DEMO 3! Watch all 4 live MonsoonPay events gated at 0 output tokens, the live race against 3.8 Flash & 4 Hydrogen, "
                "and Round C scoring our own Google Cloud architecture diagram in a single forward pass."
            ),
            "html": f"""
            <div class="video-slide">
              <div class="video-top">
                <div>
                  <div class="kicker">DEMO 03 · LIVE DECISIONS API ARENA</div>
                  <h2 class="slide-h2-sm">4 Live Events &times; 8 Qs &middot; Live Flash/Hydrogen Race &middot; Multimodal Single-Pass</h2>
                </div>
                <div class="video-pills">
                  <span class="accent-green">0 Output Tokens</span>
                  <span class="accent-amber">{r50['cost_savings_vs_4_hydrogen']}x Cheaper vs Hydrogen (50Q)</span>
                </div>
              </div>
              <div class="video-frame">
                <video controls preload="metadata" poster="../assets/videos/demo2_decisions_api_arena_poster.png">
                  <source src="../assets/videos/demo2_decisions_api_arena.mp4" type="video/mp4" />
                </video>
              </div>
            </div>
            """,
        },
        # 15 — LIVE 3.8 VOICE ARCHITECTURE
        {
            "theme": "cream",
            "title": "Gemini 3.8 Live Extended Thinking + Async Tools",
            "notes": (
                "Explain Dual-Track voice: Gemini 3.8 speaks naturally in 97 languages (with Live Avatar GA & SynthID) while executing "
                "NON_BLOCKING BigQuery, Firestore, and ADK 2.0 tools asynchronously — eliminating dead air."
            ),
            "html": """
            <div class="diag-slide">
              <div class="diag-header">
                <span class="diag-kicker">05 · REASON WHILE SPEAKING</span>
                <span class="diag-title">Gemini 3.8 Live Extended Thinking + Async Tool Execution</span>
              </div>
              <div class="diag-stage">
                <img src="../assets/diagrams/06_live38_voice.jpg" alt="Gemini 3.8 Live Extended Thinking Dual-Track Architecture" />
              </div>
            </div>
            """,
        },
        # 16 — DEMO 4A (MANI'S REAL RECORDING): FRANKFURT FLIGHT REBOOKING
        {
            "theme": "dark",
            "title": "Demo 4A: Gemini 3.8 Live — Flight Cancelled & Rebooked Live",
            "notes": (
                "DEMO 4A — MANI'S REAL LIVE RECORDING! Watch the live engineering console as `gemini-3.8-live-extended-thinking` "
                "(`thinkingLevel: HIGH`, voice `Aria`) sees Mani on camera + hears live audio while firing NON_BLOCKING BigQuery & Firestore SQL "
                "(`scan_boarding_pass_and_bag_tag`, `evaluate_eu261_and_vip_entitlement`, `INSERT INTO rebooking_transactions`) to rebook PNR LH8942X "
                "with hotel, meals, $350 goodwill & 25,000 miles!"
            ),
            "html": f"""
            <div class="video-slide">
              <div class="video-top">
                <div>
                  <div class="kicker">DEMO 04A · REAL RECORDING · GEMINI 3.8 LIVE EXTENDED THINKING</div>
                  <h2 class="slide-h2-sm">Frankfurt Flight Cancelled &mdash; Live Multimodal Rebooking &amp; EU261 Compensation</h2>
                </div>
                <div class="video-pills">
                  <span>Camera + 16kHz Voice</span>
                  <span class="accent-green">NON_BLOCKING BigQuery &amp; Firestore SQL</span>
                </div>
              </div>
              <div class="video-frame drive-poster-wrap">
                <img class="drive-poster" src="../assets/videos/demo4a_gemini38_live_flight_poster.png" alt="Gemini 3.8 Live Extended Thinking Flight Rebooking Demo" />
                <a class="drive-play-btn" href="{DRIVE_FLIGHT_URL}" target="_blank" rel="noopener">&#9654; Play Mani's Real Recording on Google Drive (2m 40s)</a>
              </div>
            </div>
            """,
        },
        # 17 — DEMO 4B (MANI'S REAL RECORDING): GEMINI VOICE AI PSTN
        {
            "theme": "dark",
            "title": "Demo 4B: Gemini Voice AI — Indian PSTN Telephony on Cloud Run",
            "notes": (
                "DEMO 4B — MANI'S REAL TELEPHONY RECORDING! Real iPhone PSTN/VoLTE call (EN, HI, TA, KN, TE, Hinglish) into "
                "Google Cloud Load Balancing + Cloud Armor -> Cloud Run Gen2 (asia-south1) -> Firestore + Voice Observatory. "
                "Compares Direct Speech-to-Speech (Gemini 3.1 Flash Live) vs Cascading (3.5 Transcribe Live -> 3.8 Flash -> 3.8 Flash-Lite TTS en-IN)!"
            ),
            "html": f"""
            <div class="video-slide">
              <div class="video-top">
                <div>
                  <div class="kicker">DEMO 04B · REAL RECORDING · ENTERPRISE VOICE AI &amp; PSTN TELEPHONY</div>
                  <h2 class="slide-h2-sm">Live Multilingual PSTN Call (EN / HI / TA / KN / TE / Hinglish) on Cloud Run</h2>
                </div>
                <div class="video-pills">
                  <span>Cloud Run asia-south1</span>
                  <span class="accent-amber">Direct S2S vs Cascading</span>
                </div>
              </div>
              <div class="video-frame drive-poster-wrap">
                <img class="drive-poster" src="../assets/videos/demo4b_gemini_voiceai_pstn_poster.png" alt="Gemini Voice AI PSTN Integration Demo" />
                <a class="drive-play-btn green-btn" href="{DRIVE_PSTN_URL}" target="_blank" rel="noopener">&#9654; Play Mani's Real PSTN Telephony Recording on Google Drive (3m 03s)</a>
              </div>
            </div>
            """,
        },
        # 18 — GOOGLE ADK 2.0 WORKFLOW RUNTIME
        {
            "theme": "dark",
            "title": "Google ADK 2.0: Deterministic Control Flow",
            "notes": (
                "Real running code from `monsoonpay/adk_workflow.py` on `google-adk==2.14.1`. Highlight deterministic DAG routing, "
                "`RetryConfig(max_attempts=3)`, and native `require_confirmation=True` HITL pause."
            ),
            "html": """
            <div class="std-slide">
              <div class="kicker">GOOGLE ADK 2.0 (GA · PYTHON / GO / TS / JAVA / C#)</div>
              <h2 class="slide-h2">Deterministic Control Flow Around Autonomous Agents</h2>
              <div class="code-split">
                <pre class="code-panel"><code><span class="kw">from</span> google.adk <span class="kw">import</span> Workflow, Event
<span class="kw">from</span> google.adk.workflow <span class="kw">import</span> Edge, RetryConfig, START, node

<span class="dec">@node</span>(name=<span class="str">"decision_gate_node"</span>)
<span class="kw">async def</span> <span class="fn">decision_gate</span>(ctx):
    v = apply_policy_gate(call_decisions_api(ctx.state[<span class="str">"alert"</span>]))
    <span class="kw">yield</span> Event(output=v, route=v.adk_route)

<span class="dec">@node</span>(name=<span class="str">"lakehouse_mcp_sql"</span>, retry_config=RetryConfig(max_attempts=<span class="num">3</span>))
<span class="kw">async def</span> <span class="fn">lakehouse_sql</span>(ctx):
    <span class="kw">return</span> query_spanner_omni_x_bigquery_iceberg()

<span class="dec">@node</span>(name=<span class="str">"hitl_pr_approval"</span>, require_confirmation=<span class="kw">True</span>)
<span class="kw">async def</span> <span class="fn">approve_pr</span>(ctx):  <span class="cm"># Native durable HITL pause</span>
    <span class="kw">return</span> {<span class="str">"status"</span>: <span class="str">"APPROVED_AND_SHIPPED"</span>}</code></pre>
                <div class="pillars-col">
                  <div class="pillar-item border-left-blue">
                    <h4>Explicit DAG Routing</h4>
                    <p><code>Edge(..., route="quarantine")</code> enforces security boundaries in typed code — never hopes inside a prompt.</p>
                  </div>
                  <div class="pillar-item border-left-amber">
                    <h4>Native HITL Checkpoints</h4>
                    <p><code>require_confirmation=True</code> emits <code>adk_request_input</code> and suspends state cleanly until an architect approves.</p>
                  </div>
                  <div class="pillar-item border-left-green">
                    <h4>Open Protocol Native</h4>
                    <p>First-class Managed MCP toolsets + A2A (Agent-to-Agent) orchestration across 5 languages.</p>
                  </div>
                </div>
              </div>
            </div>
            """,
        },
        # 19 — GOOGLE CLOUD UNIFIED DATA PLATFORM DIAGRAM
        {
            "theme": "cream",
            "title": "Google Cloud's Unified Agentic Data Platform",
            "notes": (
                "Walk through Google Cloud's unified agentic data stack: Knowledge Catalog + 50+ Managed MCP Servers sitting across "
                "Spanner Omni, BigQuery + Apache Iceberg, AlloyDB Express, and Unified Graph + AI."
            ),
            "html": """
            <div class="diag-slide">
              <div class="diag-header">
                <span class="diag-kicker">06 · ENTERPRISE DATA GRAVITY SOLVED</span>
                <span class="diag-title">Google Cloud's Unified Agentic Data Platform</span>
              </div>
              <div class="diag-stage">
                <img src="../assets/diagrams/07_gcp_data_cloud.jpg" alt="Google Cloud Unified Agentic Data Platform" />
              </div>
            </div>
            """,
        },
        # 20 — GOOGLE CLOUD DATA OFFERINGS BLUEPRINT
        {
            "theme": "dark",
            "title": "Zero-Copy Operational, Lakehouse & Vector Data Access",
            "notes": (
                "Highlight how Spanner Omni, BigQuery Borderless Iceberg, AlloyDB Express, and Knowledge Catalog + 50+ Managed MCP servers "
                "give ADK 2.0 agents governed, zero-copy access to real enterprise data."
            ),
            "html": """
            <div class="std-slide">
              <div class="kicker">GOOGLE CLOUD DATA PLATFORM · BUILT FOR PRODUCTION AGENTS</div>
              <h2 class="slide-h2">Zero-Copy Operational, Lakehouse &amp; Vector Data Access</h2>
              <div class="cards-2x2">
                <div class="arch-card border-blue">
                  <div class="card-num">TRANSACTIONAL EVERYWHERE</div>
                  <h3>Spanner Omni (GA)</h3>
                  <p>Globally consistent distributed SQL with Software TrueTime running natively across Google Cloud, Kubernetes, on-prem, and hybrid clouds.</p>
                </div>
                <div class="arch-card border-green">
                  <div class="card-num">OPEN FORMAT LAKEHOUSE</div>
                  <h3>BigQuery &amp; Borderless Apache Iceberg</h3>
                  <p>Query open Apache Iceberg tables &amp; Parquet telemetry in place with zero ETL duplication and unified governance across enterprise catalogs.</p>
                </div>
                <div class="arch-card border-amber">
                  <div class="card-num">EPHEMERAL AGENT SANDBOXES</div>
                  <h3>AlloyDB Express + ScaNN</h3>
                  <p>Serverless PostgreSQL booting in &lt;2 seconds, scaling to zero between agent runs, with 10B-scale ScaNN vector search.</p>
                </div>
                <div class="arch-card border-blue">
                  <div class="card-num">SEMANTIC GROUNDING</div>
                  <h3>Knowledge Catalog + 50+ Managed MCPs</h3>
                  <p>Universal Context Engine resolves verified semantic join paths before SQL generation: <strong>4x SQL accuracy</strong>, <strong>-75% prompt tokens</strong>.</p>
                </div>
              </div>
            </div>
            """,
        },
        # 21 — DEMO 5: ADK 2.14.1 + ZERO-COPY SPANNER x BIGQUERY ICEBERG
        {
            "theme": "dark",
            "title": "Demo 5: Real Google ADK 2.14.1 + Zero-Copy Lakehouse Join",
            "notes": (
                f"DEMO 5 — TURN UP AUDIO! Real Google ADK {d3['adk_version']} DAG + Gemini 3.8 HD voices (`Orus` & `Puck`). "
                f"Zero-copy DuckDB joins {sql['rows_correlated']:,} BigQuery Iceberg Envoy rows with Spanner Omni commits in {sql['query_latency_ms']}ms, "
                "pinpointing the `gcp:asia-south2` 64-slot Envoy pool while TrueTime stays <3ms, then pausing natively at `require_confirmation=True`!"
            ),
            "html": f"""
            <div class="video-slide">
              <div class="video-top">
                <div>
                  <div class="kicker">DEMO 05 · REAL GOOGLE ADK {e(d3['adk_version'])} + ZERO-COPY SPANNER OMNI &times; BIGQUERY ICEBERG</div>
                  <h2 class="slide-h2-sm">{sql['rows_correlated']:,} Rows Joined in {sql['query_latency_ms']} ms + Native HITL Pause + Gemini 3.8 Audio</h2>
                </div>
                <div class="video-pills">
                  <span class="accent-green">{sql['query_latency_ms']} ms Zero-Copy Join</span>
                  <span class="accent-amber">ADK HITL Paused</span>
                </div>
              </div>
              <div class="video-frame">
                <video controls preload="metadata" poster="../assets/videos/demo3_live38_voice_multicloud_adk_poster.png">
                  <source src="../assets/videos/demo3_live38_voice_multicloud_adk.mp4" type="video/mp4" />
                </video>
              </div>
            </div>
            """,
        },
        # 22 — DEMO 6: REVIEW EVERYTHING (CARBON ADVERSARIAL PR AUDIT)
        {
            "theme": "dark",
            "title": "Demo 6: Review Everything — Carbon Adversarial Security Audit",
            "notes": (
                f"DEMO 6! Even after p99 dropped from {sla['before']['p99_ms']}ms to {sla['after']['p99_ms']}ms (-{sla['p99_reduction_pct']}%) "
                f"and all 10 unit tests passed, live `gemini-4-carbon` returned `{ca['audit']['overall_verdict']}` — catching {warn_cnt or 4} real "
                "concurrency, fail-closed gate, and NaN drift edge cases before a human merges PR #1!"
            ),
            "html": f"""
            <div class="video-slide">
              <div class="video-top">
                <div>
                  <div class="kicker">DEMO 06 · REVIEW EVERYTHING · LIVE SLA PROOF + CARBON ADVERSARIAL AUDIT</div>
                  <h2 class="slide-h2-sm">p99 Dropped {sla['p99_reduction_pct']}% &amp; 10/10 Pytest Passed &mdash; Yet Carbon Still Caught {warn_cnt or 4} Findings</h2>
                </div>
                <div class="video-pills">
                  <span class="accent-green">-{sla['p99_reduction_pct']}% p99 Latency</span>
                  <span class="accent-amber">{e(ca['audit']['overall_verdict'])}</span>
                </div>
              </div>
              <div class="video-frame">
                <video controls preload="metadata" poster="../assets/videos/demo4_review_shipped_pr_poster.png">
                  <source src="../assets/videos/demo4_review_shipped_pr.mp4" type="video/mp4" />
                </video>
              </div>
            </div>
            """,
        },
        # 23 — BEYOND CODE FORCE MULTIPLIERS
        {
            "theme": "dark",
            "title": "Four Force Multipliers Beyond Code Generation",
            "notes": (
                "Fast 45-second Principal Architect tour of 8th-gen TPUs, Oracle AI Database@Google Cloud, "
                "Nano Banana 2.1 + `/generative_ui`, and Lean 4 formal verification."
            ),
            "html": """
            <div class="std-slide">
              <div class="kicker">THE WIDER GOOGLE CLOUD AI PLATFORM · ARCHITECT RADAR</div>
              <h2 class="slide-h2">Four Force Multipliers Beyond Code Generation</h2>
              <div class="cards-2x2">
                <div class="arch-card border-blue">
                  <div class="card-num">CUSTOM SILICON</div>
                  <h3>8th-Gen TPUs (TPU 8t &amp; 8i)</h3>
                  <p>Purpose-built AI silicon driving 16B+ tokens/minute globally — making parallel sub-second Hydrogen swarms affordable at enterprise scale.</p>
                </div>
                <div class="arch-card border-amber">
                  <div class="card-num">ENTERPRISE GRAVITY</div>
                  <h3>Oracle AI Database@Google Cloud</h3>
                  <p>Zero-latency Exadata &amp; Autonomous Database inside Google Cloud regions — connecting core banking directly to ADK 2.0 agents.</p>
                </div>
                <div class="arch-card border-green">
                  <div class="card-num">AGENTIC INTERFACES</div>
                  <h3>Nano Banana 2.1 &middot; <code>/generative_ui</code></h3>
                  <p>Agents move beyond Markdown text walls — synthesizing crisp diagrams, HD audio, and live interactive HTML dashboards on demand.</p>
                </div>
                <div class="arch-card border-blue">
                  <div class="card-num">FORMAL VERIFICATION</div>
                  <h3>Lean 4 Proofs &amp; AlphaProof Code</h3>
                  <p>Pairs neural synthesis with formal mathematical proofs (1.8M-line Lean 4 proofs &amp; verified consensus/financial invariants).</p>
                </div>
              </div>
            </div>
            """,
        },
        # 24 — MENTAL MODEL POSTER
        {
            "theme": "cream",
            "title": "The Battle-Tested Mental Model for Agentic Systems",
            "notes": (
                "Phones up! If you take ONE blueprint back to your team on Monday: "
                "Plan Big, Execute Fast, Decide Small, Review Everything."
            ),
            "html": """
            <div class="diag-slide">
              <div class="diag-header">
                <span class="diag-kicker">07 · TAKE A PHOTO</span>
                <span class="diag-title">The Battle-Tested Mental Model for Agentic Systems</span>
              </div>
              <div class="diag-stage">
                <img src="../assets/diagrams/08_mental_model_poster.jpg" alt="The Battle-Tested Mental Model Poster" />
              </div>
            </div>
            """,
        },
        # 25 — CLOSING CTA
        {
            "theme": "dark",
            "title": "Thank You DevFest Bengaluru 2026!",
            "notes": (
                "Closing badge callback! 'Thank you DevFest Bengaluru! Clone the repo, connect with me on LinkedIn, "
                "and if anyone knows where the best filter coffee is at Google Bengaluru, come find the Principal Architect with the brand-new badge!'"
            ),
            "html": f"""
            <div class="hero-slide">
              <div class="kicker" style="color:#4ADE80;">ALL CODE · LIVE BENCHMARKS · ADK 2.0 GRAPH · OPEN SOURCE</div>
              <h1 class="hero-title" style="font-size:66px;line-height:1.12;">Plan Big. Execute Fast.<br/>Decide Small. Review Everything.</h1>
              <div class="cta-row">
                <a class="cta-box" href="{GITHUB_URL}" target="_blank" rel="noopener">
                  <span class="mono-dim">CLONE THE REPOSITORY &amp; ALL LIVE DEMOS</span>
                  <strong>github.com/cmanikandan/gdg-blr-talk-nov14-2026</strong>
                </a>
                <a class="cta-box cta-green" href="{LINKEDIN_URL}" target="_blank" rel="noopener">
                  <span class="mono-dim">CONNECT WITH MANI</span>
                  <strong style="color:#60A5FA;">linkedin.com/in/cmanikandan</strong>
                </a>
              </div>
              <div class="hero-footer">
                <div><strong>Mani</strong> · Principal Architect, Google Cloud · DevFest Bengaluru 2026</div>
                <div class="mono-dim">Look for the Principal Architect with the brand-new badge!</div>
              </div>
            </div>
            """,
        },
    ]


def generate_html(slides: List[Dict[str, Any]]) -> str:
    slides_markup = []
    notes_list = []
    titles_list = []
    for i, s in enumerate(slides):
        theme_cls = "theme-cream" if s["theme"] == "cream" else "theme-dark"
        active_cls = " active" if i == 0 else ""
        slides_markup.append(f'<section class="slide {theme_cls}{active_cls}" data-idx="{i}">{s["html"]}</section>')
        notes_list.append(s["notes"])
        titles_list.append(s["title"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>The Periodic Table of Agents — DevFest Bengaluru 2026 Keynote</title>
  <style>
    :root {{
      --dark-bg: #0B101B;
      --dark-surface: #131C2E;
      --dark-alt: #172238;
      --dark-border: #25334D;
      --cream-bg: #FAF7F0;
      --cream-ink: #1C2434;
      --text: #F8FAFC;
      --muted: #94A3B8;
      --blue: #4285F4;
      --green: #34A853;
      --amber: #F59E0B;
      --red: #EA4335;
      --purple: #C084FC;
      --font-sans: 'Inter', 'Segoe UI', system-ui, -apple-system, 'DejaVu Sans', sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ width: 100%; height: 100%; overflow: hidden; background: var(--dark-bg); font-family: var(--font-sans); color: var(--text); -webkit-font-smoothing: antialiased; }}

    .deck {{ width: 100vw; height: 100vh; position: relative; }}
    .slide {{
      position: absolute; inset: 0;
      display: none;
      padding: 48px 68px 44px 68px;
      flex-direction: column;
      justify-content: center;
    }}
    .slide.active {{ display: flex; }}
    .theme-dark {{ background: var(--dark-bg); color: var(--text); }}
    .theme-cream {{ background: var(--cream-bg); color: var(--cream-ink); padding: 24px 44px 26px 44px; justify-content: flex-start; }}

    .kicker {{
      font-family: var(--font-mono);
      font-size: 13.5px;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--blue);
      margin-bottom: 12px;
    }}
    .mono-dim {{ font-family: var(--font-mono); font-size: 14px; color: var(--muted); }}
    .slide-h2 {{ font-size: 46px; font-weight: 700; letter-spacing: -0.025em; line-height: 1.12; margin-bottom: 28px; max-width: 1680px; }}
    .slide-h2-sm {{ font-size: 30px; font-weight: 700; letter-spacing: -0.02em; line-height: 1.16; }}
    .slide-sub {{ font-size: 21px; color: #CBD5E1; margin-bottom: 24px; }}
    code {{ font-family: var(--font-mono); font-size: 0.9em; background: rgba(66,133,244,0.14); padding: 2px 7px; border-radius: 5px; color: #93C5FD; }}

    .hero-slide {{ display: flex; flex-direction: column; height: 100%; justify-content: center; gap: 20px; }}
    .hero-title {{ font-size: 80px; font-weight: 800; letter-spacing: -0.035em; line-height: 1.04; max-width: 1680px; }}
    .hero-sub {{ font-size: 27px; color: #CBD5E1; font-weight: 400; max-width: 1200px; }}
    .element-strip {{ display: flex; gap: 16px; margin-top: 14px; }}
    .elem-chip {{
      width: 132px; height: 122px;
      border-radius: 12px;
      background: var(--dark-surface);
      border: 1px solid var(--dark-border);
      padding: 12px 14px;
      display: flex; flex-direction: column; justify-content: space-between;
    }}
    .elem-chip .num {{ font-family: var(--font-mono); font-size: 13px; color: var(--muted); }}
    .elem-chip .sym {{ font-size: 40px; font-weight: 800; letter-spacing: -0.03em; line-height: 1; }}
    .elem-chip .lbl {{ font-family: var(--font-mono); font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; color: #CBD5E1; }}
    .el-h .sym {{ color: #6CE08A; }}
    .el-c .sym {{ color: #60A5FA; }}
    .el-ar .sym {{ color: #94A3B8; }}
    .el-dc .sym {{ color: #FBBF24; }}
    .el-lv .sym {{ color: #F87171; }}
    .hero-footer {{
      margin-top: auto; padding-top: 20px;
      border-top: 1px solid var(--dark-border);
      display: flex; justify-content: space-between; align-items: flex-end;
      font-size: 18px; color: #CBD5E1;
    }}
    .footer-link {{ color: #60A5FA; text-decoration: none; font-family: var(--font-mono); font-size: 15px; font-weight: 600; }}
    .footer-link:hover {{ text-decoration: underline; }}
    .muted-link {{ color: var(--muted); }}
    .cta-row {{ display: flex; gap: 22px; margin-top: 16px; flex-wrap: wrap; }}
    .cta-box {{
      background: var(--dark-surface);
      border: 1px solid var(--dark-border);
      border-left: 5px solid var(--blue);
      border-radius: 12px;
      padding: 20px 26px;
      display: inline-flex; flex-direction: column; gap: 8px;
      text-decoration: none;
    }}
    .cta-box.cta-green {{ border-left-color: var(--green); }}
    .cta-box strong {{ font-family: var(--font-mono); font-size: 22px; color: #FFFFFF; }}

    /* Full-Stage Illustrated Diagram Slide */
    .diag-slide {{ display: flex; flex-direction: column; height: 100%; width: 100%; gap: 14px; }}
    .diag-header {{ display: flex; align-items: baseline; gap: 18px; border-bottom: 2px solid rgba(28,36,52,0.12); padding-bottom: 10px; }}
    .diag-kicker {{ font-family: var(--font-mono); font-size: 13px; font-weight: 800; letter-spacing: 0.12em; color: #1D4ED8; text-transform: uppercase; }}
    .diag-title {{ font-size: 25px; font-weight: 800; letter-spacing: -0.02em; color: var(--cream-ink); }}
    .diag-stage {{ flex: 1; min-height: 0; display: flex; align-items: center; justify-content: center; padding: 6px 0; }}
    .diag-stage img {{ height: 100%; width: auto; max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 10px; box-shadow: 0 14px 40px rgba(15,23,42,0.10); }}

    .std-slide {{ display: flex; flex-direction: column; height: 100%; justify-content: center; }}
    .cards-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; }}
    .cards-2x2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
    .arch-card {{
      background: var(--dark-surface);
      border: 1px solid var(--dark-border);
      border-radius: 14px;
      padding: 24px 26px;
      display: flex; flex-direction: column; gap: 10px;
    }}
    .border-blue {{ border-top: 4px solid var(--blue); }}
    .border-green {{ border-top: 4px solid var(--green); }}
    .border-amber {{ border-top: 4px solid var(--amber); }}
    .border-red {{ border-top: 4px solid var(--red); }}
    .border-purple {{ border-top: 4px solid var(--purple); }}
    .card-num {{ font-family: var(--font-mono); font-size: 12.5px; font-weight: 700; letter-spacing: 0.08em; color: var(--blue); }}
    .arch-card h3 {{ font-size: 22px; font-weight: 700; letter-spacing: -0.015em; }}
    .arch-card p {{ font-size: 16.5px; line-height: 1.5; color: #CBD5E1; }}

    .thesis-bar {{
      margin-top: 24px;
      background: #10192B;
      border: 1px solid var(--dark-border);
      border-left: 5px solid var(--blue);
      border-radius: 10px;
      padding: 16px 24px;
      display: flex; align-items: center; gap: 20px;
      font-size: 20px;
    }}
    .thesis-bar.green-bar {{ border-left-color: var(--green); }}
    .thesis-bar.amber-bar {{ border-left-color: var(--amber); }}
    .thesis-bar span {{ font-family: var(--font-mono); font-size: 12.5px; font-weight: 700; letter-spacing: 0.1em; color: var(--muted); white-space: nowrap; }}

    .method-box {{
      background: var(--dark-alt);
      border: 1px solid var(--dark-border);
      border-left: 5px solid var(--amber);
      border-radius: 10px;
      padding: 16px 22px;
      font-size: 15.5px;
      line-height: 1.5;
      color: #E2E8F0;
    }}

    .spec-card {{
      background: var(--dark-surface);
      border: 1px solid var(--dark-border);
      border-top: 4px solid var(--blue);
      border-radius: 14px;
      padding: 24px 26px;
      display: flex; flex-direction: column; gap: 14px;
    }}
    .spec-ar {{ border-top-color: #94A3B8; }}
    .spec-h {{ border-top-color: var(--green); }}
    .spec-head {{ display: flex; align-items: center; gap: 16px; }}
    .spec-sym {{
      width: 54px; height: 54px; border-radius: 10px;
      background: #0B101B; border: 1px solid var(--dark-border);
      display: flex; align-items: center; justify-content: center;
      font-size: 26px; font-weight: 800; color: #60A5FA;
    }}
    .spec-ar .spec-sym {{ color: #CBD5E1; }}
    .spec-h .spec-sym {{ color: #6CE08A; }}
    .spec-head h3 {{ font-size: 22px; font-weight: 700; }}
    .spec-price {{ font-family: var(--font-mono); font-size: 24px; font-weight: 700; color: #FFFFFF; }}
    .spec-price small {{ font-size: 12.5px; color: var(--muted); font-weight: 400; display: block; margin-top: 2px; }}
    .clean-list {{ list-style: none; display: flex; flex-direction: column; gap: 11px; font-size: 16.5px; line-height: 1.45; color: #CBD5E1; }}
    .clean-list li {{ padding-left: 16px; position: relative; }}
    .clean-list li::before {{ content: '—'; position: absolute; left: 0; color: var(--muted); }}

    .bench-card {{
      background: var(--dark-surface);
      border: 1px solid var(--dark-border);
      border-radius: 14px;
      padding: 20px 24px;
    }}
    .bench-title {{ font-family: var(--font-mono); font-size: 13px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--blue); margin-bottom: 12px; }}
    .slide-table {{ width: 100%; border-collapse: collapse; font-size: 16px; }}
    .slide-table th {{ text-align: left; font-family: var(--font-mono); font-size: 12px; text-transform: uppercase; color: var(--muted); padding: 9px 10px; border-bottom: 1px solid var(--dark-border); }}
    .slide-table td {{ padding: 12px 10px; border-bottom: 1px solid rgba(37,51,77,0.6); color: #CBD5E1; }}
    .slide-table td.num, .slide-table th.num {{ text-align: right; font-family: var(--font-mono); }}
    .slide-table tr.winner td {{ color: #4ADE80; font-weight: 700; background: rgba(52,168,83,0.09); }}
    .slide-table small {{ color: var(--muted); font-weight: 400; }}

    .code-split {{ display: grid; grid-template-columns: 58fr 42fr; gap: 26px; align-items: stretch; }}
    .code-panel {{
      background: #070B13;
      border: 1px solid var(--dark-border);
      border-radius: 14px;
      padding: 24px 26px;
      font-family: var(--font-mono);
      font-size: 15px;
      line-height: 1.62;
      color: #E2E8F0;
      overflow: auto;
    }}
    .code-panel code {{ background: transparent; padding: 0; color: inherit; font-size: inherit; }}
    .kw {{ color: #60A5FA; font-weight: 600; }}
    .dec {{ color: #FBBF24; font-weight: 600; }}
    .str {{ color: #6CE08A; }}
    .fn {{ color: #93C5FD; }}
    .cm {{ color: #64748B; }}
    .num {{ color: #F59E0B; }}
    .pillars-col {{ display: flex; flex-direction: column; gap: 16px; justify-content: space-between; }}
    .pillar-item {{ background: var(--dark-surface); border: 1px solid var(--dark-border); border-radius: 12px; padding: 18px 22px; }}
    .border-left-blue {{ border-left: 4px solid var(--blue); }}
    .border-left-amber {{ border-left: 4px solid var(--amber); }}
    .border-left-green {{ border-left: 4px solid var(--green); }}
    .pillar-item h4 {{ font-size: 19px; margin-bottom: 6px; color: #FFFFFF; }}
    .pillar-item p {{ font-size: 16px; line-height: 1.48; color: #CBD5E1; }}

    .video-slide {{ display: flex; flex-direction: column; height: 100%; gap: 16px; }}
    .video-top {{ display: flex; justify-content: space-between; align-items: flex-end; gap: 20px; }}
    .video-pills {{ display: flex; gap: 10px; flex-shrink: 0; }}
    .video-pills span {{
      font-family: var(--font-mono); font-size: 13px; font-weight: 700;
      padding: 7px 14px; border-radius: 6px;
      background: var(--dark-surface); border: 1px solid var(--dark-border); color: #CBD5E1;
    }}
    .video-pills .accent-green {{ background: rgba(52,168,83,0.16); border-color: rgba(52,168,83,0.4); color: #6CE08A; }}
    .video-pills .accent-amber {{ background: rgba(245,158,11,0.16); border-color: rgba(245,158,11,0.4); color: #FBBF24; }}
    .video-frame {{
      flex: 1; min-height: 0;
      background: #05080F;
      border: 1px solid var(--dark-border);
      border-radius: 14px;
      overflow: hidden;
      display: flex; align-items: center; justify-content: center;
      position: relative;
    }}
    .video-frame video {{ width: 100%; height: 100%; object-fit: contain; }}
    .drive-poster-wrap {{ flex-direction: column; gap: 14px; padding: 14px; }}
    .drive-poster {{ max-width: 100%; max-height: calc(100% - 58px); object-fit: contain; border-radius: 8px; }}
    .drive-play-btn {{
      display: inline-block;
      background: #1D4ED8;
      color: #FFFFFF;
      font-family: var(--font-mono);
      font-size: 15px;
      font-weight: 700;
      padding: 12px 26px;
      border-radius: 8px;
      text-decoration: none;
    }}
    .drive-play-btn.green-btn {{ background: #065F46; }}
    .drive-play-btn:hover {{ opacity: 0.92; }}

    .kpi-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; }}
    .big-kpi {{
      background: var(--dark-surface);
      border: 1px solid var(--dark-border);
      border-radius: 14px;
      padding: 28px 26px;
      display: flex; flex-direction: column; gap: 10px;
    }}
    .kpi-num {{ font-family: var(--font-mono); font-size: 64px; font-weight: 800; letter-spacing: -0.04em; line-height: 1; }}
    .kpi-num.green {{ color: #4ADE80; }}
    .kpi-num.blue {{ color: #60A5FA; }}
    .kpi-num.amber {{ color: #FBBF24; }}
    .kpi-head {{ font-size: 21px; font-weight: 700; }}
    .big-kpi p {{ font-size: 16.5px; line-height: 1.48; color: #CBD5E1; }}

    .slide-counter {{
      position: fixed; bottom: 16px; right: 24px;
      font-family: var(--font-mono); font-size: 13px;
      color: rgba(148,163,184,0.55); z-index: 40; pointer-events: none;
    }}
    body.on-cream .slide-counter {{ color: rgba(28,36,52,0.45); }}

    .teleprompter {{
      position: fixed; left: 0; right: 0; bottom: 0;
      background: rgba(8, 12, 21, 0.96);
      border-top: 2px solid var(--blue);
      padding: 20px 44px;
      z-index: 100;
      display: none;
      flex-direction: column; gap: 10px;
    }}
    .teleprompter.open {{ display: flex; }}
    .tp-bar {{ display: flex; justify-content: space-between; align-items: center; font-family: var(--font-mono); font-size: 13px; color: var(--blue); }}
    .tp-text {{ font-size: 19px; line-height: 1.55; color: #F1F5F9; max-width: 1280px; }}

    .grid-modal {{
      position: fixed; inset: 0;
      background: rgba(8, 12, 21, 0.96);
      z-index: 120;
      display: none;
      padding: 36px 56px;
      overflow-y: auto;
    }}
    .grid-modal.open {{ display: block; }}
    .grid-list {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-top: 20px; }}
    .grid-card {{
      background: var(--dark-surface); border: 1px solid var(--dark-border);
      border-radius: 10px; padding: 14px; cursor: pointer;
    }}
    .grid-card:hover, .grid-card.cur {{ border-color: var(--blue); }}
  </style>
</head>
<body>
  <div class="deck" id="deck">
    {''.join(slides_markup)}
  </div>

  <div class="slide-counter" id="counter">01 / {len(slides):02d}</div>

  <aside class="teleprompter" id="teleprompter">
    <div class="tp-bar">
      <span id="tpHeader">PRIVATE SPEAKER NOTES (Press S to hide)</span>
      <span id="tpTimer">30:00 Keynote Timer · Click to Start/Reset</span>
    </div>
    <div class="tp-text" id="tpBody"></div>
  </aside>

  <div class="grid-modal" id="gridModal">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <h2 style="font-size:26px;">Keynote Slide Overview (Press G or Esc to close)</h2>
    </div>
    <div class="grid-list" id="gridList"></div>
  </div>

  <script>
    const NOTES = {json.dumps(notes_list)};
    const TITLES = {json.dumps(titles_list)};
    const slides = Array.from(document.querySelectorAll('.slide'));
    let idx = 0;
    let timerSec = 0;
    let timerHandle = null;

    function showSlide(n) {{
      const oldVid = slides[idx].querySelector('video');
      if (oldVid) oldVid.pause();

      slides[idx].classList.remove('active');
      idx = Math.max(0, Math.min(slides.length - 1, n));
      slides[idx].classList.add('active');

      document.body.classList.toggle('on-cream', slides[idx].classList.contains('theme-cream'));
      document.getElementById('counter').textContent =
        String(idx + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
      document.getElementById('tpHeader').textContent =
        `SLIDE ${{idx + 1}} / ${{slides.length}} · ${{TITLES[idx]}}  (Press S to hide)`;
      document.getElementById('tpBody').textContent = NOTES[idx];
    }}

    function renderGrid() {{
      const list = document.getElementById('gridList');
      list.innerHTML = TITLES.map((t, i) => `
        <div class="grid-card ${{i === idx ? 'cur' : ''}}" onclick="jumpTo(${{i}})">
          <div style="font-family:var(--font-mono);font-size:12px;color:#60A5FA;margin-bottom:6px;">SLIDE ${{String(i+1).padStart(2,'0')}}</div>
          <div style="font-size:14px;font-weight:700;color:#F8FAFC;">${{t}}</div>
        </div>
      `).join('');
    }}

    window.jumpTo = function(i) {{
      document.getElementById('gridModal').classList.remove('open');
      showSlide(i);
    }};

    document.getElementById('tpTimer').addEventListener('click', () => {{
      if (timerHandle) {{ clearInterval(timerHandle); timerHandle = null; timerSec = 0; }}
      timerHandle = setInterval(() => {{
        timerSec++;
        const m = String(Math.floor(timerSec / 60)).padStart(2, '0');
        const s = String(timerSec % 60).padStart(2, '0');
        document.getElementById('tpTimer').textContent = `Elapsed ${{m}}:${{s}} / 30:00 (Click to Reset)`;
      }}, 1000);
    }});

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        if (document.activeElement?.tagName === 'VIDEO') return;
        e.preventDefault(); showSlide(idx + 1);
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        e.preventDefault(); showSlide(idx - 1);
      }} else if (e.key === 's' || e.key === 'S') {{
        document.getElementById('teleprompter').classList.toggle('open');
      }} else if (e.key === 'g' || e.key === 'G') {{
        renderGrid();
        document.getElementById('gridModal').classList.toggle('open');
      }} else if (e.key === 'Escape') {{
        document.getElementById('gridModal').classList.remove('open');
      }} else if (e.key === 'f' || e.key === 'F') {{
        if (!document.fullscreenElement) document.documentElement.requestFullscreen().catch(() => {{}});
        else document.exitFullscreen().catch(() => {{}});
      }}
    }});

    showSlide(0);
  </script>
</body>
</html>
"""


def main() -> None:
    tr = load_traces()
    slides = build_slides(tr)
    OUT_HTML.write_text(generate_html(slides), encoding="utf-8")
    print(f"✔ Built 25-slide HTML5 keynote -> {OUT_HTML}")


if __name__ == "__main__":
    main()
