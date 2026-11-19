# The Periodic Table of Agents — Gemini 4 Neon Keynote

> **DevFest Bengaluru 2026 Keynote**  
> **Speaker:** Mani, Principal Architect, Google Cloud — [linkedin.com/in/cmanikandan](https://www.linkedin.com/in/cmanikandan)  
> **Core Mental Model:** *Plan big. Build fast. Decide instant. Ship safe.*

Every slide, bespoke architecture visual, live **Gemini 4 Neon** (`gemini-4-neon`) + **Gemini 4 Hydrogen** (`gemini-4-hydrogen`) + **Gemini Decisions API** (`gemini-decision-1`) + **Gemini 3.8 Live & Voice AI** showcase, real **Google ADK 2.14.1** workflow, and zero-copy **Spanner Omni × BigQuery Apache Iceberg** telemetry pipeline in this repository runs end-to-end on Google Cloud architecture with verified live measurements.

All Gemini 4 Neon launch benchmarks strictly cite the public announcement: [Introducing Gemini 4 Neon (blog.google)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/).

---

## Live Measured Highlights (Captured Against Production Gemini APIs)

### 1. Head-to-Head Control Plane Race: `gemini-decision-1` vs. `gemini-3.8-flash` vs. `gemini-4-hydrogen`

- **Use Case:** MonsoonPay incoming Delhi checkout incident gated on **8 real-time security & routing rules** OR **50 simultaneous RBI / PCI-DSS compliance rules** before invoking an agent.
- **Methodology:** Identical incident payload evaluated live on the Gemini API — `gemini-decision-1` via `POST /v1beta/decisions` (1 forward pass, **0 output tokens**) vs. `gemini-3.8-flash` (`thinking_budget=0`) and `gemini-4-hydrogen` (`thinking_level=low`) returning strict JSON via `generateContent`. Costs calculated from exact API `usage_metadata` at published pricing.

| Benchmark | Model | Latency | Billed Output Tokens | Cost / 1M Calls | Decisions Advantage |
| :--- | :--- | ---: | ---: | ---: | :--- |
| **8 Security & Routing Rules** *(Live)* | **`gemini-decision-1`** | **240 ms** | **0** | **$82.80** | **Baseline ($0 output)** |
| **8 Security & Routing Rules** *(Live)* | `gemini-3.8-flash` *(budget=0)* | 3,507 ms | 108 | $374.40 | 14.6× slower · 4.5× costlier |
| **8 Security & Routing Rules** *(Live)* | `gemini-4-hydrogen` *(low)* | 2,727 ms | 673 | $5,709.00 | 11.4× slower · 68.9× costlier |
| **50 Simultaneous RBI/PCI Rules** *(Live)* | **`gemini-decision-1`** | **283 ms** | **0** | **$270.70** | **Baseline ($0 output)** |
| **50 Simultaneous RBI/PCI Rules** *(Live)* | `gemini-3.8-flash` *(budget=0)* | 6,347 ms | 755 | $2,296.70 | **22.4× slower · 8.5× costlier** |
| **50 Simultaneous RBI/PCI Rules** *(Live)* | `gemini-4-hydrogen` *(low)* | 4,947 ms | 1,700 | $14,899.50 | **17.5× slower · 55.0× costlier** |
| **100-Rule Scaling** *(Google Pub.)* | **`gemini-decision-1`** | **359 ms** | **0** | — | **20.1× vs Flash (7.2s) · 24.0× vs Hydrogen (8.6s)** |

### 2. Six Live Engineering & Production Voice AI Demos

1. **Demo 1 — Parallel Swarm (`demos/demo1_antigravity_swarm.py`):** Live **`gemini-4-neon`** reads our Google Cloud Delhi (`asia-south2`) payment gateway code (`14.8s`), plans a 3-part fix, and spawns **3 parallel `gemini-4-hydrogen` builders** in isolated sandboxes (`10.8s` wall vs. `19.8s` sequential → **`1.83×` speedup**, `0` merge conflicts), handing off cleanly to a Cloud VM.
2. **Demo 2 — Legacy UPI Rewrite (`demos/demo5_code_modernization.py`):** Live **`gemini-4-neon`** reads a slow legacy Indian UPI settlement engine (`411.1 ms` on 8,000 payments), extracts all 5 hidden RBI & GST rounding rules (`7.1s`), writes a clean modern version on Attempt 1, and passes our locked verification suite **`100.5×` faster (`411.1 ms → 4.09 ms`)** with **`₹0.00` error** across **₹5.62 Cr**!
3. **Demo 3 — Instant Guardrails & 50-Rule Race (`demos/demo2_decisions_arena.py`):** Live `gemini-decision-1` blocks prompt attacks & leaked keys before any agent runs, routes UI tweaks to Hydrogen and outages to **Gemini 4 Neon**, wins the 50-rule race **`22.4×` faster than Flash** and **`55.0×` cheaper than Hydrogen**, and audits our Google Cloud architecture diagram in **`440 ms`** (`0` output tokens).
4. **Demo 4 — Voice Check-In + Zero-Copy Cloud Data (`demos/demo3_voice_adk_multicloud.py`):** Real **Google ADK 2.14.1** workflow (`google.adk.Workflow`) joins **40,000 Spanner Omni × BigQuery Apache Iceberg rows in `170 ms`** with zero copying, pinpoints Delhi's 64-slot queue, and pauses natively at a built-in Human Approval Gate — narrated with studio **Gemini 3.8 HD Audio**.
5. **Demo 5 — Neon Cyber Audit (`demos/demo4_review_shipped_pr.py`):** 500-user load test confirms **`-97.1%` checkout delay drop (`478.55 ms → 13.95 ms`)** and **10/10 `pytest` green** — yet an independent live **`gemini-4-neon`** cyber reviewer (`90.5%` SEC-bench Pro · `0.0%` IPI bypass) still catches a real human-approval gap (`APPROVE WITH NOTE`) before a human clicks Merge!
6. **Demo 6 — Embedded Production Voice AI Recordings (Slides 15 & 16 + Studio Tab 6):**
   - **Part A (`Gemini 3.8 Live Extended Thinking`):** 1 FPS live camera + voice boarding-pass flight rebooking running non-blocking BigQuery & Firestore updates with zero dead air — embedded directly inline inside Slide 15 & Studio Tab 6!
   - **Part B (`Indian Phone-Line Telephony on Google Cloud`):** Real Indian PSTN phone calls routed through Cloud Armor + Cloud Run Mumbai across 6 Indian languages (English, Hindi, Tamil, Kannada, Telugu, Hinglish) — embedded directly inline inside Slide 16 & Studio Tab 6!

---

## Repository Map

```text
├── monsoonpay/                       # 100% Google Cloud-native reference platform
│   ├── seed_multicloud_data.py       # Seeds 10k Spanner Omni SQLite + 40k BigQuery Iceberg Parquet rows
│   ├── circuit_breaker.py            # Spanner Omni TrueTime stale-read circuit breaker
│   ├── decisions_gate.py             # Real REST client for POST /v1beta/decisions (text + multimodal)
│   ├── adk_workflow.py               # Real Google ADK 2.14.1 Workflow + DuckDB + built-in HITL pause
│   └── legacy_settlement.py          # Legacy Indian UPI settlement monolith + exact verification harness
├── tests/
│   └── test_monsoonpay.py            # 10 automated pytest verification tests
├── demos/
│   ├── demo1_antigravity_swarm.py    # Live Neon orchestrator + 3 parallel Hydrogen sandbox builders
│   ├── demo2_decisions_arena.py      # 4 events + Live 8Q/50Q Flash/Hydrogen race + Diagram audit
│   ├── demo3_voice_adk_multicloud.py # Real ADK 2.14.1 + DuckDB + Gemini 3.8 HD Audio
│   ├── demo4_review_shipped_pr.py    # 500-user load test + 10/10 pytest + Live Neon cyber audit
│   ├── demo5_code_modernization.py   # Live Neon invariant extraction + rewrite + ₹0.00 proof
│   ├── reset_environment.py          # Clean reset utility (sandboxes, code, Spanner/Iceberg DB, tests)
│   ├── stage_workbench.py            # FastAPI Stage Studio backend (SSE live streaming + Reset API)
│   ├── studio.html                   # Uncluttered auditorium Stage Studio Web UI + cinema recorder
│   ├── record_demos.mjs              # 1080p 30fps CDP + FFmpeg MP4 & Gemini 3.8 audio muxer
│   └── traces/                       # Captured live API traces + mastered Gemini 3.8 HD WAV tracks
├── assets/
│   ├── diagrams/                     # Bespoke Obsidian + Neon hero & architecture visuals
│   └── videos/                       # All 7 embedded MP4 videos (5 live demos + 2 real Voice AI recordings)
├── presentation/
│   ├── keynote_deck.html             # Self-contained 18-slide HTML5 keynote (all 7 videos play inline!)
│   ├── build_html_keynote.py         # Builds keynote_deck.html dynamically from live traces
│   ├── build_google_slides.py        # Builds 18-slide Google Slides v4 deck + PDF + video-embedded PPTX
│   ├── Periodic_Table_of_Agents_DevFest_Keynote.pdf
│   ├── Periodic_Table_of_Agents_DevFest_Keynote.pptx  # Native embedded playable MP4s on all 7 video slides!
│   └── google_slides_metadata.json   # Live Google Slides v4 & Drive video URLs
└── SPEAKER_RUN_OF_SHOW.md            # Stage playbook for all 18 slides
```

---

## Quickstart (MacBook / Linux)

### 1. Clone, Install Dependencies & Verify Tests
```bash
git clone https://github.com/cmanikandan/gdg-blr-talk-nov14-2026.git
cd gdg-blr-talk-nov14-2026
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python monsoonpay/seed_multicloud_data.py
.venv/bin/pytest -v
```

### 2. Launch the Redesigned Stage Studio Web UI (No Terminal on Stage!)
Export `GEMINI_API_KEY` transiently in your shell and launch Stage Studio:
```bash
export GEMINI_API_KEY="<your-gemini-api-key>"
.venv/bin/python demos/stage_workbench.py --open
# Opens http://127.0.0.1:8765 automatically
```
Inside Stage Studio:
- **7 Spacious, Auditorium-Readable Views (`Overview` + Tabs `1`–`6`)**: Designed in plain English for both experienced engineers and newcomers, with a clean **`</> Technical Details & Code`** slide-over drawer tucked away until you want to dive deep.
- **`▶ Preview` (`P`)**: Smooth animated walkthrough from the latest verified live run (works even with zero conference Wi-Fi; includes synchronized Gemini 3.8 HD Audio on Tab 4).
- **`⚡ Run Live`**: Streams live Gemini 4 Neon, Hydrogen, Decisions API, and ADK 2.14.1 execution directly onto the stage UI.
- **Tab `6 · Live Videos`**: Plays both real Voice AI recordings (Flight Rebooking + Indian 6-Language Phone Calls) inline beside their architecture diagrams — zero Google Drive click-out!
- **`↺` Reset Popover**: One-click **Auto-Reset after each live run**, **Reset Code & Backend**, or **Full Factory Reset (+ Verify 10 Tests)**.

### 3. Present the 18-Slide Gemini 4 Neon Keynote (All 7 Videos Play Directly Inline!)
- **Option A — Browser HTML5 Keynote (Recommended, Works 100% Offline):** Open [`presentation/keynote_deck.html`](presentation/keynote_deck.html) in Chrome/Edge.
  - **`ArrowRight` / `Space`** — Next slide
  - **`F`** — Fullscreen auditorium mode
  - **`S`** — Private Speaker Teleprompter & timer
  - **`G`** — 18-slide overview grid
- **Option B — PowerPoint / Apple Keynote (Self-Contained Inline Videos):** Open [`presentation/Periodic_Table_of_Agents_DevFest_Keynote.pptx`](presentation/Periodic_Table_of_Agents_DevFest_Keynote.pptx) — all 7 MP4 videos (including Slides 15 & 16 Voice AI recordings) are embedded directly inside the slides.
- **Option C — Google Slides (v4):** Open the link in [`presentation/google_slides_metadata.json`](presentation/google_slides_metadata.json) for Presenter View with full speaker notes on all 18 slides.