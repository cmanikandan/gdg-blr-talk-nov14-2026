# The Periodic Table of Agents: Building with Gemini 4 and Antigravity

> **DevFest Bengaluru 2026 Opening Keynote**  
> **Speaker:** Manikandan (Mani), Principal Architect, Google Cloud  
> **Core Mental Model:** *Plan big, execute fast, decide small, and review everything.*

Every slide, O'Reilly Head First visual, live Gemini 4 / Decisions API / Gemini 3.8 HD Audio demo, real **Google ADK 2.14.1** workflow graph, and zero-copy **Spanner Omni × AWS S3 Apache Iceberg** telemetry pipeline in this repository runs end-to-end with zero mocked numbers.

---

## Live Measured Highlights (Captured Against Production Gemini APIs)

### 1. Head-to-Head Control Plane Race: `gemini-decision-1` vs. `gemini-3.8-flash` vs. `gemini-4-hydrogen`

| Benchmark | Model | Latency | Billed Output Tokens | Cost / 1M Calls | Speedup / Savings |
| :--- | :--- | ---: | ---: | ---: | :--- |
| **8-Question Control Plane** *(Live)* | **`gemini-decision-1`** | **273 ms** | **0** | **$81** | **Baseline ($0 output)** |
| **8-Question Control Plane** *(Live)* | `gemini-3.8-flash` *(budget=0)* | 2,475 ms | 116 | $394 | 9.1x slower · 4.9x costlier |
| **8-Question Control Plane** *(Live)* | `gemini-4-hydrogen` *(low)* | 3,826 ms | 549 | $4,772 | 14.0x slower · 59.1x costlier |
| **50 Simultaneous Compliance Checks** *(Live)* | **`gemini-decision-1`** | **2,718 ms** | **0** | **$270** | **Baseline ($0 output)** |
| **50 Simultaneous Compliance Checks** *(Live)* | `gemini-3.8-flash` *(budget=0)* | 5,808 ms | 754 | $2,291 | 2.1x slower · 8.5x costlier |
| **50 Simultaneous Compliance Checks** *(Live)* | `gemini-4-hydrogen` *(low)* | 7,758 ms | 1,736 | $15,150 | 2.9x slower · **56.2x costlier** |
| **100-Question Scaling** *(Google Nov 2026)* | **`gemini-decision-1`** | **359 ms** | **0** | — | **20x vs Flash (7.2s) · 24x vs Hydrogen (8.6s)** |

### 2. MonsoonPay Live Engineering Loop Outcomes
- **Demo 1 (Plan Big + Execute Fast):** Live `gemini-4-carbon` architected the fix and flagged subtle circuit-breaker risks; 3 parallel `gemini-4-hydrogen` workers executed inside isolated `git worktree add --detach` sandboxes (**`2.37x` parallel speedup**, `0` merge conflicts).
- **Demo 3 (Voice Check-In + ADK 2.14.1 + Zero-Copy Multicloud):** Real `google.adk.Workflow` DAG ran in **`482 ms`** total—calling live `gemini-decision-1`, resolving Knowledge Catalog semantics, joining **40,000 rows** across Spanner Omni SQLite + AWS S3 Apache Iceberg Parquet in **`116.7 ms`** via DuckDB (`aws:ap-south-1` `p99=431.8ms`, `18,006` sync retries vs `gcp:asia-south1` `p99=16.1ms`, TrueTime drift `2.75ms`), and pausing natively at `@node(require_confirmation=True)` — narrated by real **Gemini 3.8 HD audio** (`gemini-3.8-flash-tts`).
- **Demo 4 (Review Everything):** Deterministic 500-request burst benchmark verified **`-97.1%` checkout p99 drop** (`478.55 ms -> 13.95 ms`) with **9/9 `pytest` passing** — yet live `gemini-4-carbon` adversarial review still threw **`CHANGES_REQUESTED`**, catching **5 subtle security and concurrency edge cases** pre-merge.

---

## Repository Map

```text
├── monsoonpay/                       # Real production reference app
│   ├── seed_multicloud_data.py       # Seeds 10k Spanner Omni SQLite + 40k S3 Iceberg Parquet rows
│   ├── circuit_breaker.py            # Spanner Omni Software TrueTime bounded stale-read breaker
│   ├── decisions_gate.py             # Real REST client for POST /v1beta/decisions (text + multimodal)
│   └── adk_workflow.py               # Real Google ADK 2.14.1 Workflow DAG + DuckDB + HITL pause
├── tests/
│   └── test_monsoonpay.py            # 9 automated pytest verification tests
├── demos/
│   ├── demo1_antigravity_swarm.py    # Live Carbon architect + 3 parallel Hydrogen git-worktree workers
│   ├── demo2_decisions_arena.py      # 4 events + Live Flash/Hydrogen race (8Q & 50Q) + Multimodal
│   ├── demo3_voice_adk_multicloud.py # Real ADK 2.14.1 + DuckDB + Gemini 3.8 HD Audio (+ --live-mic)
│   ├── demo4_review_shipped_pr.py    # SLA burst benchmark + pytest + Live Carbon adversarial review
│   ├── stage_workbench.py            # FastAPI live/replay stage server (http://127.0.0.1:8765)
│   ├── studio.html                   # 1920x1080 cinema workbench UI driven by real JSON traces
│   ├── record_demos.mjs              # 1080p 30fps CDP + FFmpeg MP4 & Gemini 3.8 audio muxer
│   └── traces/                       # Real captured API traces + mastered Gemini 3.8 HD WAV tracks
├── assets/
│   ├── infographics/                 # 8 O'Reilly Head First 16:9 visual posters (01..08)
│   └── videos/                       # 4 embedded 1080p 30fps H.264 MP4s + PNG posters
├── presentation/
│   ├── keynote_deck.html             # Self-contained 22-slide HTML5 keynote (F, S, G shortcuts)
│   ├── build_html_keynote.py         # Builds keynote_deck.html from live traces
│   ├── build_google_slides.py        # Builds 22-slide Google Slides deck + PDF/PPTX export
│   ├── Periodic_Table_of_Agents_DevFest_Keynote.pdf
│   ├── Periodic_Table_of_Agents_DevFest_Keynote.pptx
│   └── google_slides_metadata.json   # Live Google Slides & Drive video URLs
└── SPEAKER_RUN_OF_SHOW.md            # Minute-by-minute 30:00 stage playbook
```

---

## Quickstart

### 1. Install Dependencies & Run Tests
```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python monsoonpay/seed_multicloud_data.py
.venv/bin/pytest -v
```

### 2. Present the 22-Slide Keynote Deck (Offline-Safe, Embedded 1080p 30fps Videos + Audio)
Open [`presentation/keynote_deck.html`](presentation/keynote_deck.html) in Chrome/Edge:
- **`ArrowRight` / `Space`** — Next slide
- **`F`** — Fullscreen auditorium mode
- **`S`** — Private Speaker Teleprompter & 30:00 keynote timer
- **`G`** — 22-slide jump grid

### 3. Run Live Demos or Launch the Stage Workbench
Never hardcode API keys—export `GEMINI_API_KEY` transiently in your shell:
```bash
export GEMINI_API_KEY="<your-gemini-api-key>"

# Run individual live demos (writes fresh traces to demos/traces/)
.venv/bin/python demos/demo1_antigravity_swarm.py
.venv/bin/python demos/demo2_decisions_arena.py
.venv/bin/python demos/demo3_voice_adk_multicloud.py       # add --live-mic on stage laptop for live WebSocket
.venv/bin/python demos/demo4_review_shipped_pr.py

# Or launch the interactive Stage Workbench (Live API + Instant Trace Replay)
.venv/bin/python demos/stage_workbench.py
# Open http://127.0.0.1:8765
```