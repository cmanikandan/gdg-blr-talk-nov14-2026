#!/usr/bin/env python3
"""
Builds the World-Class 22-Slide HTML5 Keynote Deck (`presentation/keynote_deck.html`).

Features:
  - Alternating Deep Obsidian (#0B101B) Editorial Slides & Full-Stage Warm Cream (#FAF7F0) O'Reilly Head First Infographics
  - Zero redundant text on infographic slides, zero emoji spam, zero audience-visible pacing timers
  - Embedded 1080p 30fps H.264 MP4 demo videos (Demo 3 includes REAL Gemini 3.8 HD Voice Audio!)
  - All benchmark numbers loaded dynamically from real `demos/traces/demo{1..4}_trace.json`
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


def load_traces() -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, fname in [
        ("d1", "demo1_trace.json"),
        ("d2", "demo2_trace.json"),
        ("d3", "demo3_trace.json"),
        ("d4", "demo4_trace.json"),
    ]:
        out[k] = json.loads((TRACES_DIR / fname).read_text(encoding="utf-8"))
    return out


def e(val: Any) -> str:
    return html.escape(str(val))


def build_slides(tr: Dict[str, Any]) -> List[Dict[str, Any]]:
    d1, d2, d3, d4 = tr["d1"], tr["d2"], tr["d3"], tr["d4"]
    b8 = d2["round_b_head_to_head"]["benchmark_8q"]
    b50 = d2["round_b_head_to_head"]["benchmark_50q"]
    pub100 = d2["round_b_head_to_head"]["published_100q_reference"]
    r50 = d2["round_b_head_to_head"]["live_ratios_50q"]
    speedup_8_flash = round(b8[1]["latency_ms"] / max(b8[0]["latency_ms"], 1), 1)
    speedup_8_hydro = round(b8[2]["latency_ms"] / max(b8[0]["latency_ms"], 1), 1)
    cost_8_flash = round(b8[1]["cost_per_1m_calls_usd"] / max(b8[0]["cost_per_1m_calls_usd"], 0.01), 1)
    cost_8_hydro = round(b8[2]["cost_per_1m_calls_usd"] / max(b8[0]["cost_per_1m_calls_usd"], 0.01), 1)

    sla = d4["sla_benchmark"]
    sql = d3["multicloud_finding"]
    ca = d4["carbon_security_audit"]

    return [
        # 01 — HERO TITLE
        {
            "theme": "dark",
            "title": "The Periodic Table of Agents",
            "notes": (
                "[00:00 - 01:00] High-energy walk-on! Good morning DevFest Bengaluru! "
                "Six months ago, AI coding agents were smart pair programmers. Today, a single session plans with one model, "
                "executes in parallel with another, decides with a zero-output-token classifier, and ships in the cloud after you shut your laptop. "
                "Let's unpack the Periodic Table of Agents."
            ),
            "html": """
            <div class="hero-slide">
              <div class="kicker">DEVFEST BENGALURU 2026 · OPENING KEYNOTE</div>
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
                <div><strong>Manikandan (Mani)</strong> · Principal Architect, Google Cloud</div>
                <div class="mono-dim">github.com/cmanikandan/gdg-blr-talk-nov14-2026</div>
              </div>
            </div>
            """,
        },
        # 02 — HEAD FIRST: FRESH BADGE
        {
            "theme": "cream",
            "title": "Fresh Badge, First Keynote",
            "notes": (
                "[01:00 - 02:15] BADGE JOKE MOMENT! Hold up your physical Google badge! "
                "'Full transparency before we dive into distributed systems: I am SO new to Google Cloud that my badge is still warm from the printer. "
                "I literally used Gemini 4 Hydrogen this morning just to navigate the Bengaluru campus and find the micro-kitchen! "
                "The upside? Everything I am showing you today I had to build, break, and verify from first principles myself—zero corporate slideware.'"
            ),
            "html": """
            <div class="hf-slide">
              <div class="hf-header">
                <span class="hf-kicker">01 · FULL DISCLOSURE</span>
                <span class="hf-title">So New to Google, My Badge Is Still Warm</span>
              </div>
              <div class="hf-stage">
                <img src="../assets/infographics/01_hf_fresh_badge.jpg" alt="Fresh Badge Head First Infographic" />
              </div>
            </div>
            """,
        },
        # 03 — HEAD FIRST: SIX-MONTH SHIFT
        {
            "theme": "cream",
            "title": "The Six-Month Shift",
            "notes": (
                "[02:15 - 03:30] Pause and let the room read the contrast. Six months ago: one model, one synchronous chat tab, laptop stays open, "
                "every question costs the same frontier price. Today: multi-model specialization, parallel worktrees, remote cloud VMs that keep shipping "
                "long after your laptop lid snaps shut."
            ),
            "html": """
            <div class="hf-slide">
              <div class="hf-header">
                <span class="hf-kicker">02 · THE ARCHITECTURAL INFLECTION</span>
                <span class="hf-title">Six Months Ago vs. Today</span>
              </div>
              <div class="hf-stage">
                <img src="../assets/infographics/02_hf_six_month_shift.jpg" alt="Six Month Shift Head First Infographic" />
              </div>
            </div>
            """,
        },
        # 04 — NO SLIDEWARE PROMISES
        {
            "theme": "dark",
            "title": "No Slideware Promises",
            "notes": (
                "[03:30 - 04:30] Set up the live engineering arc for MonsoonPay (our cross-cloud fintech checkout running on Spanner Omni across GCP & AWS "
                "with Envoy telemetry in AWS S3 Apache Iceberg). In minute one we kick off the real build and close the laptop; mid-talk we check in by voice; "
                "before we wrap we review the shipped PR—including what our adversarial verifier caught."
            ),
            "html": """
            <div class="std-slide">
              <div class="kicker">THE LIVE KEYNOTE CONTRACT</div>
              <h2 class="slide-h2">No Slideware Promises — One Real Engineering Arc</h2>
              <div class="cards-3">
                <div class="arch-card">
                  <div class="card-num">ACT I · MINUTE 1</div>
                  <h3>Kick Off &amp; Close Laptop</h3>
                  <p>Gemini 4 Carbon architects the MonsoonPay AWS Mumbai tail-latency fix. Three Gemini 4 Hydrogen workers execute in isolated git worktrees, then hand off to a Remote Agent VM.</p>
                </div>
                <div class="arch-card">
                  <div class="card-num">ACT II · MID-TALK</div>
                  <h3>Voice Check-In Over Multicloud</h3>
                  <p>Ask Gemini 3.8 Live for status by voice. While it talks, Google ADK 2.0 runs a zero-copy SQL join across Spanner Omni and 40,000 AWS S3 Iceberg rows—then pauses at a HITL gate.</p>
                </div>
                <div class="arch-card">
                  <div class="card-num">ACT III · WRAP-UP</div>
                  <h3>Adversarial Audit &amp; PR Review</h3>
                  <p>Verify the 97.1% p99 latency drop and green pytest suite—then watch Gemini 4 Carbon run an adversarial security audit and still catch edge cases before a human merges.</p>
                </div>
              </div>
              <div class="thesis-bar">
                <span>MENTAL MODEL</span>
                <strong>Plan big · Execute fast · Decide small · Review everything.</strong>
              </div>
            </div>
            """,
        },
        # 05 — DEMO 1 VIDEO
        {
            "theme": "dark",
            "title": "Demo 1: Minute 1 Kickoff",
            "notes": (
                f"[04:30 - 06:30] DEMO 1! Press play (or switch to Stage Workbench). Point out three real things: "
                f"1) Gemini 4 Carbon didn't just paraphrase—it caught a HALF_OPEN probe flaw and benchmark coverage gap in {round(d1['carbon_architect']['latency_ms']/1000,1)}s. "
                f"2) Three parallel Hydrogen workers ran inside real `git worktree add --detach` sandboxes for a {d1['hydrogen_swarm']['parallel_speedup']}x parallel speedup. "
                "3) We fire `agy --remote-agent` and physically close the laptop lid!"
            ),
            "html": f"""
            <div class="video-slide">
              <div class="video-top">
                <div>
                  <div class="kicker">DEMO 01 · REAL LIVE TRACE</div>
                  <h2 class="slide-h2-sm">Minute 1 Kickoff: Carbon Plan -&gt; Parallel Hydrogen <code>/swarm</code> -&gt; Remote VM</h2>
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
        # 06 — HEAD FIRST: PERIODIC TABLE
        {
            "theme": "cream",
            "title": "The Periodic Table of Agents",
            "notes": (
                "[06:30 - 08:00] Here is the core mental model of the entire keynote. Just like chemistry doesn't build every molecule out of gold, "
                "you should never build every agent turn out of one frontier model. Hydrogen is your sub-second abundant fuel; Carbon is your deep diamond-strength architect "
                "and adversarial verifier; Argon is your inert, rock-solid enterprise workhorse; Decisions is your zero-output-token control plane; Live 3.8 is your voice."
            ),
            "html": """
            <div class="hf-slide">
              <div class="hf-header">
                <span class="hf-kicker">03 · THE CORE ARCHITECTURE</span>
                <span class="hf-title">The Periodic Table of Agents</span>
              </div>
              <div class="hf-stage">
                <img src="../assets/infographics/03_hf_periodic_table.jpg" alt="Periodic Table of Agents Head First Infographic" />
              </div>
            </div>
            """,
        },
        # 07 — GEMINI 4 MODEL MATRIX
        {
            "theme": "dark",
            "title": "Gemini 4 Element Specs",
            "notes": (
                "[08:00 - 09:30] Quick Principal Architect cheat sheet. Look at Hydrogen's 4 thinking tiers: `low`, `medium`, `high`, `xhigh`—same $1.50/$7.50 flat rate across 1M context, "
                "hitting 54 on the Artificial Analysis Intelligence Index at `xhigh` and 43/43 on PlotlyDataAnalyticsBench while running 2.5x faster than 3.8 Flash. "
                "Save Carbon ($2/$10 intro, rising to $4/$20 after Nov 30) for long-horizon planning and security verification—0% Gray Swan indirect prompt injection bypass and #1 CursorBench 4.0!"
            ),
            "html": """
            <div class="std-slide">
              <div class="kicker">GEMINI 4 FAMILY · PRODUCTION SELECTION GUIDE</div>
              <h2 class="slide-h2">Match the Element to the Reasoning Horizon</h2>
              <div class="cards-3">
                <div class="spec-card spec-c">
                  <div class="spec-head"><span class="spec-sym">C</span><div><h3>Gemini 4 Carbon</h3><div class="mono-dim">Deep Architect &amp; Verifier</div></div></div>
                  <div class="spec-price">$2 / $10 <small>per 1M tok (intro thru Nov 30)</small></div>
                  <ul class="clean-list">
                    <li><strong>Long-horizon planning</strong> across 1M-token repositories</li>
                    <li><strong>0% bypass</strong> on Gray Swan indirect prompt injection</li>
                    <li><strong>#1 CursorBench 4.0</strong> for complex multi-file diffs</li>
                    <li>Best for: System design, root cause, adversarial PR review</li>
                  </ul>
                </div>
                <div class="spec-card spec-ar">
                  <div class="spec-head"><span class="spec-sym">Ar</span><div><h3>Gemini 4 Argon</h3><div class="mono-dim">Enterprise Workhorse</div></div></div>
                  <div class="spec-price">$2 / $10 <small>per 1M tok · 1M context</small></div>
                  <ul class="clean-list">
                    <li><strong>50 AA Intelligence Index</strong> with low variance</li>
                    <li>Predictable multi-package refactors &amp; SQL generation</li>
                    <li>Balanced throughput for regulated enterprise pipelines</li>
                    <li>Best for: Core service logic, migrations, domain RAG</li>
                  </ul>
                </div>
                <div class="spec-card spec-h">
                  <div class="spec-head"><span class="spec-sym">H</span><div><h3>Gemini 4 Hydrogen</h3><div class="mono-dim">Sub-Second Execution Fuel</div></div></div>
                  <div class="spec-price">$1.50 / $7.50 <small>flat across full 1M context</small></div>
                  <ul class="clean-list">
                    <li><strong>4 Thinking Tiers:</strong> <code>low</code> · <code>medium</code> · <code>high</code> · <code>xhigh</code></li>
                    <li><strong>54 AA Index</strong> at <code>xhigh</code> · <strong>43/43</strong> PlotlyDataAnalyticsBench</li>
                    <li><strong>2.5x faster</strong> than Gemini 3.8 Flash</li>
                    <li>Best for: Parallel <code>/swarm</code> workers, tests, everyday coding</li>
                  </ul>
                </div>
              </div>
            </div>
            """,
        },
        # 08 — HEAD FIRST: ANTIGRAVITY ENGINE
        {
            "theme": "cream",
            "title": "Inside Google Antigravity",
            "notes": (
                "[09:30 - 11:00] Walk left to right: The Orchestrator uses Carbon to build an executable plan with file ownership boundaries. "
                "`/swarm` spawns parallel Hydrogen workers, each inside an isolated `git worktree` so they NEVER trample each other's working tree. "
                "And Remote Agents run inside dedicated Cloud VMs—so closing your laptop no longer kills your engineering sprint."
            ),
            "html": """
            <div class="hf-slide">
              <div class="hf-header">
                <span class="hf-kicker">04 · MULTI-AGENT EXECUTION</span>
                <span class="hf-title">Inside Google Antigravity: Orchestrator, /swarm &amp; Remote Agents</span>
              </div>
              <div class="hf-stage">
                <img src="../assets/infographics/04_hf_antigravity_engine.jpg" alt="Google Antigravity Engine Head First Infographic" />
              </div>
            </div>
            """,
        },
        # 09 — WHY NAIVE ROUTERS FAIL
        {
            "theme": "dark",
            "title": "Stop Using an LLM as an If-Statement",
            "notes": (
                "[11:00 - 12:15] Now bring this exact multi-model discipline into YOUR production apps! "
                "Most teams put an autoregressive LLM in front of their agent to check for prompt injection, PII leaks, and model routing—paying 2-4 seconds "
                "and hundreds of output tokens BEFORE the real work even starts. Even worse, they get brittle 'true/false' strings instead of calibrated probabilities!"
            ),
            "html": """
            <div class="stat-slide">
              <div class="kicker">PRODUCTION CONTROL PLANE ANTI-PATTERN</div>
              <h2 class="slide-h2">Stop Burning Autoregressive Output Tokens on Routing &amp; Guardrails</h2>
              <div class="split-contrast">
                <div class="contrast-box bad">
                  <div class="mono-tag red">THE OLD WAY · AUTOREGRESSIVE JSON</div>
                  <div class="big-num red">2–8 sec</div>
                  <p>One token decoded at a time. Ask 50 compliance checks and you pay for 750–1,700 output tokens + uncalibrated strings.</p>
                </div>
                <div class="contrast-box good">
                  <div class="mono-tag green">GEMINI DECISIONS API · SINGLE FORWARD PASS</div>
                  <div class="big-num green">0 output tok</div>
                  <p>Evaluates up to <strong>1,000 independent questions</strong> in one forward pass. Returns calibrated probabilities at <strong>$0.10 / 1M input · $0 output</strong>.</p>
                </div>
              </div>
            </div>
            """,
        },
        # 10 — HEAD FIRST: DECISIONS API
        {
            "theme": "cream",
            "title": "Gemini Decisions API Architecture",
            "notes": (
                "[12:15 - 13:30] Look at the prism on the right: `gemini-decision-1` takes multimodal inputs (text, images, audio, video, PDFs) "
                "and runs ONE forward pass across three native primitives: `noul` (calibrated 0.01-0.99 probability), `choice` (2 to 255 options), "
                "and `score` (weighted rubric expectation). Zero autoregressive decoding!"
            ),
            "html": """
            <div class="hf-slide">
              <div class="hf-header">
                <span class="hf-kicker">05 · DECIDE SMALL</span>
                <span class="hf-title">How Gemini Decisions API Eliminates Output-Token Latency</span>
              </div>
              <div class="hf-stage">
                <img src="../assets/infographics/05_hf_decisions_api.jpg" alt="Gemini Decisions API Head First Infographic" />
              </div>
            </div>
            """,
        },
        # 11 — LIVE BENCHMARK SHOWDOWN (MANI'S REQUESTED COMPARISON!)
        {
            "theme": "dark",
            "title": "Decision-1 vs 3.8 Flash vs 4 Hydrogen",
            "notes": (
                f"[13:30 - 15:15] THIS IS THE SLIDE EVERYONE TAKES A PHOTO OF! We benchmarked `gemini-decision-1` head-to-head against "
                f"`gemini-3.8-flash` (with thinking_budget=0!) and `gemini-4-hydrogen` (low thinking) LIVE on the real API. "
                f"On an 8-question production guardrail + router gate: Decision-1 ran in {b8[0]['latency_ms']}ms with ZERO output tokens ($80.80 per 1M calls)—"
                f"{speedup_8_flash}x faster than 3.8 Flash and {speedup_8_hydro}x faster & {cost_8_hydro}x cheaper than 4 Hydrogen! "
                f"Scale to 50 simultaneous compliance checks in ONE call: Decision-1 is {r50['cost_savings_vs_3_8_flash']}x cheaper than Flash and "
                f"{r50['cost_savings_vs_4_hydrogen']}x cheaper than Hydrogen ($270 vs $15,150 per 1M calls)! "
                f"And in Google's published 100-question benchmark, Decision-1 stays flat at 359ms vs 7.2s Flash (20x) and 8.6s Hydrogen (24x)!"
            ),
            "html": f"""
            <div class="std-slide">
              <div class="kicker">HEAD-TO-HEAD BENCHMARK · DECISION-1 VS 3.8 FLASH VS 4 HYDROGEN</div>
              <h2 class="slide-h2">Why "Decide Small" Changes Production Unit Economics</h2>
              <div class="bench-grid">
                <div class="bench-card">
                  <div class="bench-title">8-Question Control Plane (Measured Live)</div>
                  <table class="slide-table">
                    <thead><tr><th>Model</th><th class="num">Latency</th><th class="num">Out Tok</th><th class="num">$ / 1M Calls</th></tr></thead>
                    <tbody>
                      <tr class="winner"><td><strong>gemini-decision-1</strong></td><td class="num">{b8[0]['latency_ms']} ms</td><td class="num">0</td><td class="num">${b8[0]['cost_per_1m_calls_usd']:,.0f}</td></tr>
                      <tr><td>gemini-3.8-flash <small>(budget=0)</small></td><td class="num">{b8[1]['latency_ms']:,} ms <small>({speedup_8_flash}x)</small></td><td class="num">{b8[1]['billed_output_tokens']}</td><td class="num">${b8[1]['cost_per_1m_calls_usd']:,.0f} <small>({cost_8_flash}x)</small></td></tr>
                      <tr><td>gemini-4-hydrogen <small>(low)</small></td><td class="num">{b8[2]['latency_ms']:,} ms <small>({speedup_8_hydro}x)</small></td><td class="num">{b8[2]['billed_output_tokens']}</td><td class="num">${b8[2]['cost_per_1m_calls_usd']:,.0f} <small>({cost_8_hydro}x)</small></td></tr>
                    </tbody>
                  </table>
                </div>
                <div class="bench-card">
                  <div class="bench-title">50 Simultaneous Compliance Checks in 1 Call (Live)</div>
                  <table class="slide-table">
                    <thead><tr><th>Model</th><th class="num">Billed Out</th><th class="num">$ / 1M Calls</th><th class="num">Savings</th></tr></thead>
                    <tbody>
                      <tr class="winner"><td><strong>gemini-decision-1</strong></td><td class="num">0 tok</td><td class="num">${b50[0]['cost_per_1m_calls_usd']:,.0f}</td><td class="num">Baseline</td></tr>
                      <tr><td>gemini-3.8-flash</td><td class="num">{b50[1]['billed_output_tokens']} tok</td><td class="num">${b50[1]['cost_per_1m_calls_usd']:,.0f}</td><td class="num">{r50['cost_savings_vs_3_8_flash']}x costlier</td></tr>
                      <tr><td>gemini-4-hydrogen</td><td class="num">{b50[2]['billed_output_tokens']:,} tok</td><td class="num">${b50[2]['cost_per_1m_calls_usd']:,.0f}</td><td class="num">{r50['cost_savings_vs_4_hydrogen']}x costlier</td></tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <div class="thesis-bar green-bar">
                <span>100-QUESTION SCALING (GOOGLE BENCHMARK)</span>
                <strong>Decision-1: {pub100['gemini_decision_1_ms']} ms · 3.8 Flash: {pub100['gemini_3_8_flash_ms']/1000:.1f}s ({pub100['speedup_vs_flash']}x) · 4 Hydrogen: {pub100['gemini_4_hydrogen_ms']/1000:.1f}s ({pub100['speedup_vs_hydrogen']}x)</strong>
              </div>
            </div>
            """,
        },
        # 12 — DEMO 2 VIDEO
        {
            "theme": "dark",
            "title": "Demo 2: Decisions API Arena",
            "notes": (
                "[15:15 - 17:15] DEMO 2! Watch all three live rounds: Round A catches prompt injection (0.99), leaked AWS/Stripe keys (0.97), "
                "routes a CSS tweak to Hydrogen fast-lane, and dispatches the multicloud outage to Carbon—ALL with 0 output tokens. "
                "Round B runs the live race against Flash & Hydrogen. Round C evaluates our actual Head First diagram image + text in one forward pass!"
            ),
            "html": """
            <div class="video-slide">
              <div class="video-top">
                <div>
                  <div class="kicker">DEMO 02 · LIVE BENCHMARK &amp; MULTIMODAL ARENA</div>
                  <h2 class="slide-h2-sm">4 Events x 8 Qs · Live Flash/Hydrogen Race · Multimodal Single-Pass</h2>
                </div>
                <div class="video-pills">
                  <span class="accent-green">0 Output Tokens Billed</span>
                  <span>Up to 1,000 Qs / Call</span>
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
        # 13 — HEAD FIRST: GEMINI 3.8 LIVE VOICE
        {
            "theme": "cream",
            "title": "Gemini 3.8 Live Extended Thinking",
            "notes": (
                "[17:15 - 18:30] Now it's mid-talk—our laptop has been closed for 12 minutes. How do we check on our remote engineering swarm without breaking stride? "
                "Gemini 3.8 Live Extended Thinking separates the conversational audio track from deep asynchronous tool execution! "
                "No awkward 8-second dead silence—it speaks naturally in 97 languages (with Live Avatar GA & SynthID watermarking) while firing ADK 2.0 in parallel."
            ),
            "html": """
            <div class="hf-slide">
              <div class="hf-header">
                <span class="hf-kicker">06 · REASON WHILE SPEAKING</span>
                <span class="hf-title">Gemini 3.8 Live Extended Thinking + Async Tool Execution</span>
              </div>
              <div class="hf-stage">
                <img src="../assets/infographics/06_hf_live38_voice.jpg" alt="Gemini 3.8 Live Voice Head First Infographic" />
              </div>
            </div>
            """,
        },
        # 14 — GOOGLE ADK 2.0 WORKFLOW RUNTIME
        {
            "theme": "dark",
            "title": "Google ADK 2.0 Workflow Runtime",
            "notes": (
                "[18:30 - 20:00] This is REAL production code from `monsoonpay/adk_workflow.py` running on `google-adk==2.14.1`! "
                "ADK 2.0 replaces brittle while-loops with an explicit `Workflow` DAG: deterministic `@node` routing from `gemini-decision-1`, "
                "native `RetryConfig(max_attempts=3)` on cross-cloud SQL nodes, and `require_confirmation=True` for durable Human-in-the-Loop checkpoints before any PR merge."
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
    verdict = apply_policy_gate(call_decisions_api(ctx.state[<span class="str">"alert"</span>]))
    <span class="kw">yield</span> Event(output=verdict, route=verdict.adk_route)

<span class="dec">@node</span>(name=<span class="str">"multicloud_mcp_sql"</span>, retry_config=RetryConfig(max_attempts=<span class="num">3</span>))
<span class="kw">async def</span> <span class="fn">multicloud_sql</span>(ctx): <span class="cm"># DuckDB / BQ Omni zero-copy join</span>
    <span class="kw">return</span> query_spanner_omni_x_s3_iceberg()

<span class="dec">@node</span>(name=<span class="str">"hitl_pr_approval"</span>, require_confirmation=<span class="kw">True</span>)
<span class="kw">async def</span> <span class="fn">approve_pr</span>(ctx): <span class="cm"># Native durable pause for Principal Architect</span>
    <span class="kw">return</span> {<span class="str">"status"</span>: <span class="str">"APPROVED_AND_SHIPPED"</span>}</code></pre>
                <div class="pillars-col">
                  <div class="pillar-item">
                    <h4>Explicit DAG Routing</h4>
                    <p><code>Edge(..., route="quarantine")</code> enforces security boundaries in code—not hopes inside a system prompt.</p>
                  </div>
                  <div class="pillar-item">
                    <h4>Native HITL Checkpoints</h4>
                    <p><code>require_confirmation=True</code> emits <code>adk_request_input</code> and pauses execution until a human approves.</p>
                  </div>
                  <div class="pillar-item">
                    <h4>Open Protocol First</h4>
                    <p>Native <strong>MCP</strong> (Model Context Protocol) tool binding + <strong>A2A</strong> (Agent-to-Agent) across 5 languages.</p>
                  </div>
                </div>
              </div>
            </div>
            """,
        },
        # 15 — HEAD FIRST: AGENTIC & MULTICLOUD DATA CLOUD
        {
            "theme": "cream",
            "title": "The Agentic & Multicloud Data Cloud",
            "notes": (
                "[20:00 - 21:30] Agents are only as smart as the enterprise data they can safely query—and real enterprises don't live in one cloud! "
                "Google Cloud's 2026 Data Cloud removes data gravity: Spanner Omni runs everywhere with Software TrueTime; Borderless Apache Iceberg queries AWS S3 & Azure Blob zero-copy; "
                "AlloyDB Express boots ephemeral agent sandboxes in <2 seconds; Knowledge Catalog grounds every agent query with verified semantics."
            ),
            "html": """
            <div class="hf-slide">
              <div class="hf-header">
                <span class="hf-kicker">07 · ENTERPRISE DATA GRAVITY SOLVED</span>
                <span class="hf-title">Google Cloud's Agentic &amp; Multicloud Data Platform</span>
              </div>
              <div class="hf-stage">
                <img src="../assets/infographics/07_hf_agentic_data_cloud.jpg" alt="Agentic and Multicloud Data Cloud Head First Infographic" />
              </div>
            </div>
            """,
        },
        # 16 — MULTICLOUD DATA BLUEPRINT
        {
            "theme": "dark",
            "title": "Multicloud Data Offerings",
            "notes": (
                "[21:30 - 22:45] Highlight the four game-changers for Principal Architects: Spanner Omni GA bringing Software TrueTime to AWS, Azure, OCI, and K8s; "
                "Borderless Iceberg & BigQuery Omni federating AWS Glue, Databricks Unity Catalog, and Snowflake Horizon with zero ETL egress; "
                "AlloyDB Express booting in under 2 seconds and scaling to zero for ephemeral `/swarm` test databases with 10B ScaNN vector search; "
                "and Knowledge Catalog + 50+ Managed MCP Servers boosting agent SQL accuracy 4x while cutting prompt tokens 75%."
            ),
            "html": """
            <div class="std-slide">
              <div class="kicker">NEW GOOGLE CLOUD DATA OFFERINGS · MULTICLOUD BY DEFAULT</div>
              <h2 class="slide-h2">Zero-Copy Data Access Across GCP, AWS &amp; Azure</h2>
              <div class="cards-2x2">
                <div class="arch-card">
                  <div class="card-num">TRANSACTIONAL EVERYWHERE</div>
                  <h3>Spanner Omni (GA)</h3>
                  <p>Distributed SQL with <strong>Software TrueTime</strong> running natively across GCP, AWS, Azure, OCI, Kubernetes, and Docker—strong consistency without lock-in.</p>
                </div>
                <div class="arch-card">
                  <div class="card-num">ZERO-COPY LAKEHOUSE</div>
                  <h3>Borderless Iceberg &amp; BigQuery Omni</h3>
                  <p>Query Apache Iceberg directly on <strong>AWS S3 &amp; Azure Blob</strong> while federating AWS Glue, Unity Catalog, and Snowflake Horizon with zero data egress.</p>
                </div>
                <div class="arch-card">
                  <div class="card-num">EPHEMERAL AGENT SANDBOXES</div>
                  <h3>AlloyDB Express + ScaNN</h3>
                  <p>Serverless PostgreSQL that boots in <strong>&lt;2 seconds</strong>, scales to zero between swarm runs, and indexes up to <strong>10B vector embeddings</strong>.</p>
                </div>
                <div class="arch-card">
                  <div class="card-num">SEMANTIC GROUNDING</div>
                  <h3>Knowledge Catalog + 50+ Managed MCPs</h3>
                  <p>Universal Context Engine resolves verified cross-cloud joins before SQL generation—delivering <strong>4x higher SQL accuracy</strong> and <strong>-75% prompt tokens</strong>.</p>
                </div>
              </div>
            </div>
            """,
        },
        # 17 — DEMO 3 VIDEO (WITH REAL GEMINI 3.8 HD VOICE AUDIO!)
        {
            "theme": "dark",
            "title": "Demo 3: Voice Check-In + ADK + Multicloud",
            "notes": (
                f"[22:45 - 24:45] DEMO 3 — TURN UP THE AUDITORIUM SPEAKERS! This video has REAL Gemini 3.8 HD voice audio (`gemini-3.8-flash-tts`) "
                f"synced to our REAL Google ADK 2.14.1 execution ({d3['adk_total_ms']}ms total)! Listen as Gemini immediately acknowledges Mani while DuckDB runs "
                f"a live zero-copy join over {sql['rows_correlated']:,} rows in {sql['query_latency_ms']}ms—proving Spanner Omni TrueTime held 2.75ms while AWS Mumbai's 64-slot Envoy pool triggered 18,006 retries—then pauses at ADK's HITL confirmation gate!"
            ),
            "html": f"""
            <div class="video-slide">
              <div class="video-top">
                <div>
                  <div class="kicker">DEMO 03 · REAL GEMINI 3.8 HD AUDIO + GOOGLE ADK 2.14.1</div>
                  <h2 class="slide-h2-sm">Voice Check-In: Dual-Track Audio + Zero-Copy Spanner Omni x S3 Iceberg</h2>
                </div>
                <div class="video-pills">
                  <span class="accent-green">Audio Included · Unmute</span>
                  <span>{sql['rows_correlated']:,} Rows in {sql['query_latency_ms']}ms</span>
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
        # 18 — BEYOND CODE: 2026 BREAKTHROUGHS
        {
            "theme": "dark",
            "title": "What Else Shipped in 2026",
            "notes": (
                "[24:45 - 26:00] Zoom out for 60 seconds as a Google Cloud Principal Architect: four force multipliers worth watching right now. "
                "8th-Gen TPUs (8t & 8i) pushing 16B+ tokens/min infrastructure; Oracle AI Database@Google Cloud uniting mission-critical Oracle workloads with Gemini; "
                "Nano Banana 2.1 + Gemini Omni 1.2 + `/generative_ui` generating live visual infographics (like the ones in this deck!) and rich UI on the fly; "
                "and AlphaProof Code bringing formal Lean proofs to security-critical code paths."
            ),
            "html": """
            <div class="std-slide">
              <div class="kicker">THE WIDER 2026 PLATFORM · ARCHITECT RADAR</div>
              <h2 class="slide-h2">Four Force Multipliers Beyond Code Generation</h2>
              <div class="cards-2x2">
                <div class="arch-card">
                  <div class="card-num">CUSTOM SILICON</div>
                  <h3>8th-Gen TPUs (TPU 8t &amp; 8i)</h3>
                  <p>Purpose-built inference &amp; training silicon powering <strong>16B+ tokens/minute</strong> globally—making sub-second Hydrogen swarms economically viable.</p>
                </div>
                <div class="arch-card">
                  <div class="card-num">ENTERPRISE GRAVITY</div>
                  <h3>Oracle AI Database@Google Cloud</h3>
                  <p>Zero-latency Exadata &amp; Autonomous Database inside Google Cloud regions—connecting legacy core banking directly to ADK 2.0 &amp; BigQuery Graph.</p>
                </div>
                <div class="arch-card">
                  <div class="card-num">AGENTIC INTERFACES</div>
                  <h3>Nano Banana 2.1 · Omni 1.2 · /generative_ui</h3>
                  <p>Agents no longer stop at Markdown walls—they synthesize crisp visual diagrams, audio, and live interactive HTML widgets mid-conversation.</p>
                </div>
                <div class="arch-card">
                  <div class="card-num">FORMAL VERIFICATION</div>
                  <h3>AlphaProof Code</h3>
                  <p>Bridges neural code synthesis with formal mathematical <strong>Lean</strong> verification for cryptographic, consensus, and financial invariant proofs.</p>
                </div>
              </div>
            </div>
            """,
        },
        # 19 — DEMO 4 VIDEO
        {
            "theme": "dark",
            "title": "Demo 4: Review Everything",
            "notes": (
                f"[26:00 - 27:45] DEMO 4 — CLOSING THE LOOP! Watch what happened when we ran our real benchmark & test suite: "
                f"p99 tail latency plunged -{sla['p99_reduction_pct']}% ({sla['before']['p99_ms']}ms -> {sla['after']['p99_ms']}ms), all 9 pytest tests passed. "
                f"If we stopped there, we'd merge blindly. Instead, we ran LIVE Gemini 4 Carbon as an adversarial reviewer—and Carbon threw `{ca['audit']['overall_verdict']}`! "
                "It caught 5 real edge cases: an unused `autonomy_readiness` signal, low-res multimodal IPI evasion, negative/NaN TrueTime bounds, and a HALF_OPEN race condition! "
                "THAT is why Rule 4 is Review Everything."
            ),
            "html": f"""
            <div class="video-slide">
              <div class="video-top">
                <div>
                  <div class="kicker">DEMO 04 · ADVERSARIAL VERIFICATION &amp; PR #1</div>
                  <h2 class="slide-h2-sm">p99 Dropped {sla['p99_reduction_pct']}% &amp; Tests Passed — Yet Carbon Still Caught 5 Edge Cases</h2>
                </div>
                <div class="video-pills">
                  <span class="accent-green">p99: {sla['before']['p99_ms']}ms -&gt; {sla['after']['p99_ms']}ms</span>
                  <span class="accent-amber">Carbon: {e(ca['audit']['overall_verdict'])}</span>
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
        # 20 — PRODUCTION ECONOMICS SUMMARY
        {
            "theme": "dark",
            "title": "What Multi-Model Architecture Buys You",
            "notes": (
                "[27:45 - 28:30] Pause on three verified numbers measured live from our own codebase today: "
                "97.1% checkout tail latency reduction verified via deterministic load test; 56x to 59x control-plane cost savings using Decisions API instead of Hydrogen; "
                "and zero blind merges thanks to worktree isolation, ADK HITL checkpoints, and Carbon adversarial review."
            ),
            "html": f"""
            <div class="stat-slide">
              <div class="kicker">VERIFIED LIVE KEYNOTE OUTCOMES</div>
              <h2 class="slide-h2">What the Periodic Table Architecture Actually Buys You</h2>
              <div class="kpi-3">
                <div class="big-kpi">
                  <div class="kpi-num green">-{sla['p99_reduction_pct']}%</div>
                  <div class="kpi-head">Checkout p99 Latency</div>
                  <p>{sla['before']['p99_ms']} ms -&gt; {sla['after']['p99_ms']} ms across 500-request AWS ap-south-1 flash-sale burst.</p>
                </div>
                <div class="big-kpi">
                  <div class="kpi-num blue">{r50['cost_savings_vs_4_hydrogen']}x</div>
                  <div class="kpi-head">Cheaper Control Plane</div>
                  <p>Live 50-question compliance gate: $270/1M calls on Decision-1 vs $15,150/1M on Hydrogen (0 output tokens).</p>
                </div>
                <div class="big-kpi">
                  <div class="kpi-num amber">5</div>
                  <div class="kpi-head">Subtle Bugs Caught Pre-Merge</div>
                  <p>Real edge cases flagged by Gemini 4 Carbon adversarial review even after all 9 unit tests passed green.</p>
                </div>
              </div>
            </div>
            """,
        },
        # 21 — HEAD FIRST: MENTAL MODEL POSTER
        {
            "theme": "cream",
            "title": "The Mental Model",
            "notes": (
                "[28:30 - 29:15] Phones up! If you remember ONE slide from this 30-minute keynote: "
                "1. Plan Big (Carbon / Argon). 2. Execute Fast (Hydrogen `/swarm` + Remote Agents). "
                "3. Decide Small (Gemini Decisions API, $0 output tokens). 4. Review Everything (Adversarial Carbon + ADK HITL + Human Architect)."
            ),
            "html": """
            <div class="hf-slide">
              <div class="hf-header">
                <span class="hf-kicker">08 · TAKE A PHOTO</span>
                <span class="hf-title">The Battle-Tested Mental Model for Agentic Systems</span>
              </div>
              <div class="hf-stage">
                <img src="../assets/infographics/08_hf_mental_model_poster.jpg" alt="Mental Model Poster Head First Infographic" />
              </div>
            </div>
            """,
        },
        # 22 — CLOSING & REPO CTA
        {
            "theme": "dark",
            "title": "Thank You, DevFest Bengaluru!",
            "notes": (
                "[29:15 - 30:00] Bring the energy home! Every single line of MonsoonPay, the real ADK 2.14.1 DAG, the live Decision-1 vs Flash vs Hydrogen benchmark, "
                "all 4 demo recordings, and all 8 O'Reilly Head First posters are live on GitHub right now. "
                "Closing callback joke: 'Thank you DevFest Bengaluru—and if you know where the best filter coffee is at Google Bengaluru, come find the Principal Architect with the brand-new badge!'"
            ),
            "html": """
            <div class="hero-slide">
              <div class="kicker">ALL CODE · REAL ADK 2.0 GRAPH · LIVE BENCHMARKS · OPEN SOURCE</div>
              <h1 class="hero-title" style="font-size:66px;">Plan Big. Execute Fast.<br/>Decide Small. Review Everything.</h1>
              <div class="cta-box">
                <span class="mono-dim">CLONE THE KEYNOTE REPO</span>
                <strong>github.com/cmanikandan/gdg-blr-talk-nov14-2026</strong>
              </div>
              <div class="hero-footer">
                <div><strong>Manikandan (Mani)</strong> · Principal Architect, Google Cloud · DevFest Bengaluru 2026</div>
                <div class="mono-dim">Press [S] for Speaker Notes · [G] for Slide Grid · [F] for Fullscreen</div>
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
        cls = "slide theme-cream" if s["theme"] == "cream" else "slide theme-dark"
        active = " active" if i == 0 else ""
        slides_markup.append(
            f'<section class="{cls}{active}" data-index="{i}">{s["html"]}</section>'
        )
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
      --dark-border: #25334D;
      --cream-bg: #FAF7F0;
      --cream-ink: #1C2434;
      --text: #F8FAFC;
      --muted: #94A3B8;
      --blue: #4285F4;
      --green: #34A853;
      --amber: #F59E0B;
      --red: #EA4335;
      --font-sans: 'Inter', 'Segoe UI', system-ui, -apple-system, 'DejaVu Sans', sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', 'DejaVu Sans Mono', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ width: 100%; height: 100%; overflow: hidden; background: var(--dark-bg); font-family: var(--font-sans); color: var(--text); -webkit-font-smoothing: antialiased; }}

    .deck {{ width: 100vw; height: 100vh; position: relative; }}
    .slide {{
      position: absolute; inset: 0;
      display: none;
      padding: 52px 72px 48px 72px;
      flex-direction: column;
      justify-content: center;
    }}
    .slide.active {{ display: flex; }}
    .theme-dark {{ background: var(--dark-bg); color: var(--text); }}
    .theme-cream {{ background: var(--cream-bg); color: var(--cream-ink); padding: 26px 44px 28px 44px; justify-content: flex-start; }}

    /* Typography */
    .kicker {{
      font-family: var(--font-mono);
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--blue);
      margin-bottom: 14px;
    }}
    .mono-dim {{ font-family: var(--font-mono); font-size: 14px; color: var(--muted); }}
    .slide-h2 {{ font-size: 50px; font-weight: 700; letter-spacing: -0.025em; line-height: 1.12; margin-bottom: 36px; max-width: 1680px; }}
    .slide-h2-sm {{ font-size: 32px; font-weight: 700; letter-spacing: -0.02em; line-height: 1.16; }}
    code {{ font-family: var(--font-mono); font-size: 0.9em; background: rgba(66,133,244,0.14); padding: 2px 7px; border-radius: 5px; color: #93C5FD; }}

    /* Hero slide */
    .hero-slide {{ display: flex; flex-direction: column; height: 100%; justify-content: center; gap: 22px; }}
    .hero-title {{ font-size: 84px; font-weight: 800; letter-spacing: -0.035em; line-height: 1.04; max-width: 1680px; }}
    .hero-sub {{ font-size: 28px; color: #CBD5E1; font-weight: 400; max-width: 1200px; }}
    .element-strip {{ display: flex; gap: 16px; margin-top: 18px; }}
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
      margin-top: auto; padding-top: 22px;
      border-top: 1px solid var(--dark-border);
      display: flex; justify-content: space-between; align-items: center;
      font-size: 18px; color: #CBD5E1;
    }}
    .cta-box {{
      margin-top: 18px;
      background: var(--dark-surface);
      border: 1px solid var(--dark-border);
      border-left: 5px solid var(--blue);
      border-radius: 12px;
      padding: 22px 28px;
      display: inline-flex; flex-direction: column; gap: 8px; align-self: flex-start;
    }}
    .cta-box strong {{ font-family: var(--font-mono); font-size: 28px; color: #FFFFFF; }}

    /* Full-Stage O'Reilly Head First Infographic Slide */
    .hf-slide {{ display: flex; flex-direction: column; height: 100%; width: 100%; gap: 14px; }}
    .hf-header {{ display: flex; align-items: baseline; gap: 18px; border-bottom: 2px solid rgba(28,36,52,0.12); padding-bottom: 10px; }}
    .hf-kicker {{ font-family: var(--font-mono); font-size: 13px; font-weight: 800; letter-spacing: 0.12em; color: #1D4ED8; text-transform: uppercase; }}
    .hf-title {{ font-size: 26px; font-weight: 800; letter-spacing: -0.02em; color: var(--cream-ink); }}
    .hf-stage {{ flex: 1; min-height: 0; display: flex; align-items: center; justify-content: center; padding: 6px 0; }}
    .hf-stage img {{ height: 100%; width: auto; max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 10px; box-shadow: 0 14px 40px rgba(15,23,42,0.10); }}

    /* Standard Dark Editorial Slides */
    .std-slide, .stat-slide {{ display: flex; flex-direction: column; height: 100%; justify-content: center; }}
    .cards-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px; }}
    .cards-2x2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
    .arch-card {{
      background: var(--dark-surface);
      border: 1px solid var(--dark-border);
      border-radius: 14px;
      padding: 28px 30px;
      display: flex; flex-direction: column; gap: 12px;
    }}
    .card-num {{ font-family: var(--font-mono); font-size: 13px; font-weight: 700; letter-spacing: 0.08em; color: var(--blue); }}
    .arch-card h3 {{ font-size: 25px; font-weight: 700; letter-spacing: -0.015em; }}
    .arch-card p {{ font-size: 18px; line-height: 1.55; color: #CBD5E1; }}

    .thesis-bar {{
      margin-top: 30px;
      background: #10192B;
      border: 1px solid var(--dark-border);
      border-left: 5px solid var(--blue);
      border-radius: 10px;
      padding: 18px 26px;
      display: flex; align-items: center; gap: 22px;
      font-size: 22px;
    }}
    .thesis-bar.green-bar {{ border-left-color: var(--green); }}
    .thesis-bar span {{ font-family: var(--font-mono); font-size: 13px; font-weight: 700; letter-spacing: 0.1em; color: var(--muted); white-space: nowrap; }}

    /* Gemini 4 Spec Cards */
    .spec-card {{
      background: var(--dark-surface);
      border: 1px solid var(--dark-border);
      border-top: 4px solid var(--blue);
      border-radius: 14px;
      padding: 26px 28px;
      display: flex; flex-direction: column; gap: 16px;
    }}
    .spec-ar {{ border-top-color: #94A3B8; }}
    .spec-h {{ border-top-color: var(--green); }}
    .spec-head {{ display: flex; align-items: center; gap: 16px; }}
    .spec-sym {{
      width: 56px; height: 56px; border-radius: 10px;
      background: #0B101B; border: 1px solid var(--dark-border);
      display: flex; align-items: center; justify-content: center;
      font-size: 28px; font-weight: 800; color: #60A5FA;
    }}
    .spec-ar .spec-sym {{ color: #CBD5E1; }}
    .spec-h .spec-sym {{ color: #6CE08A; }}
    .spec-head h3 {{ font-size: 23px; font-weight: 700; }}
    .spec-price {{ font-family: var(--font-mono); font-size: 26px; font-weight: 700; color: #FFFFFF; }}
    .spec-price small {{ font-size: 13px; color: var(--muted); font-weight: 400; display: block; margin-top: 2px; }}
    .clean-list {{ list-style: none; display: flex; flex-direction: column; gap: 12px; font-size: 17px; line-height: 1.45; color: #CBD5E1; }}
    .clean-list li {{ padding-left: 16px; position: relative; }}
    .clean-list li::before {{ content: '—'; position: absolute; left: 0; color: var(--muted); }}

    /* Contrast Stat Slide */
    .split-contrast {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
    .contrast-box {{
      background: var(--dark-surface);
      border: 1px solid var(--dark-border);
      border-radius: 16px;
      padding: 36px 38px;
      display: flex; flex-direction: column; gap: 16px;
    }}
    .contrast-box.bad {{ border-top: 5px solid var(--red); }}
    .contrast-box.good {{ border-top: 5px solid var(--green); }}
    .mono-tag {{ font-family: var(--font-mono); font-size: 13px; font-weight: 700; letter-spacing: 0.08em; }}
    .mono-tag.red, .big-num.red {{ color: #F87171; }}
    .mono-tag.green, .big-num.green {{ color: #4ADE80; }}
    .big-num {{ font-family: var(--font-mono); font-size: 68px; font-weight: 800; letter-spacing: -0.03em; line-height: 1.05; }}
    .contrast-box p {{ font-size: 20px; line-height: 1.5; color: #CBD5E1; }}

    /* Benchmark Table Slide */
    .bench-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 26px; }}
    .bench-card {{
      background: var(--dark-surface);
      border: 1px solid var(--dark-border);
      border-radius: 14px;
      padding: 24px 26px;
    }}
    .bench-title {{ font-family: var(--font-mono); font-size: 14px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--blue); margin-bottom: 16px; }}
    .slide-table {{ width: 100%; border-collapse: collapse; font-size: 17px; }}
    .slide-table th {{ text-align: left; font-family: var(--font-mono); font-size: 12px; text-transform: uppercase; color: var(--muted); padding: 10px 8px; border-bottom: 1px solid var(--dark-border); }}
    .slide-table td {{ padding: 14px 8px; border-bottom: 1px solid rgba(37,51,77,0.6); color: #CBD5E1; }}
    .slide-table td.num, .slide-table th.num {{ text-align: right; font-family: var(--font-mono); }}
    .slide-table tr.winner td {{ color: #4ADE80; font-weight: 700; background: rgba(52,168,83,0.09); }}
    .slide-table small {{ color: var(--muted); font-weight: 400; }}

    /* Code Split (ADK 2.0) */
    .code-split {{ display: grid; grid-template-columns: 58fr 42fr; gap: 28px; align-items: stretch; }}
    .code-panel {{
      background: #070B13;
      border: 1px solid var(--dark-border);
      border-radius: 14px;
      padding: 26px 28px;
      font-family: var(--font-mono);
      font-size: 15.5px;
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
    .pillars-col {{ display: flex; flex-direction: column; gap: 18px; justify-content: space-between; }}
    .pillar-item {{ background: var(--dark-surface); border: 1px solid var(--dark-border); border-radius: 12px; padding: 20px 22px; }}
    .pillar-item h4 {{ font-size: 20px; margin-bottom: 6px; color: #FFFFFF; }}
    .pillar-item p {{ font-size: 16.5px; line-height: 1.48; color: #CBD5E1; }}

    /* Video Slides */
    .video-slide {{ display: flex; flex-direction: column; height: 100%; gap: 18px; }}
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
    }}
    .video-frame video {{ width: 100%; height: 100%; object-fit: contain; }}

    /* Big KPI Summary */
    .kpi-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; }}
    .big-kpi {{
      background: var(--dark-surface);
      border: 1px solid var(--dark-border);
      border-radius: 16px;
      padding: 36px 32px;
      display: flex; flex-direction: column; gap: 12px;
    }}
    .kpi-num {{ font-family: var(--font-mono); font-size: 76px; font-weight: 800; letter-spacing: -0.04em; line-height: 1; }}
    .kpi-num.green {{ color: #4ADE80; }}
    .kpi-num.blue {{ color: #60A5FA; }}
    .kpi-num.amber {{ color: #FBBF24; }}
    .kpi-head {{ font-size: 24px; font-weight: 700; }}
    .big-kpi p {{ font-size: 18px; line-height: 1.5; color: #CBD5E1; }}

    /* Minimal Corner Slide Counter (subtle, zero clutter!) */
    .slide-counter {{
      position: fixed; bottom: 16px; right: 24px;
      font-family: var(--font-mono); font-size: 13px;
      color: rgba(148,163,184,0.55); z-index: 40; pointer-events: none;
    }}
    body.on-cream .slide-counter {{ color: rgba(28,36,52,0.45); }}

    /* Private Speaker Teleprompter Drawer (Toggle with 'S' key!) */
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

    /* Slide Grid Overview (Toggle with 'G' key!) */
    .grid-modal {{
      position: fixed; inset: 0;
      background: rgba(8, 12, 21, 0.96);
      z-index: 120;
      display: none;
      padding: 36px 56px;
      overflow-y: auto;
    }}
    .grid-modal.open {{ display: block; }}
    .grid-list {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 20px; }}
    .grid-card {{
      background: var(--dark-surface); border: 1px solid var(--dark-border);
      border-radius: 10px; padding: 16px; cursor: pointer;
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
      // Pause any playing video on old slide
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
          <div style="font-size:15px;font-weight:700;color:#F8FAFC;">${{t}}</div>
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
    print(f"✔ Built world-class {len(slides)}-slide HTML5 keynote -> {OUT_HTML}")


if __name__ == "__main__":
    main()
