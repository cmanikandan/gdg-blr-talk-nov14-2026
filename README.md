# The Periodic Table of Agents: Building with Gemini 4 and Antigravity

> **DevFest Bengaluru 2026 Opening Keynote**  
> **Speaker:** Mani, Principal Architect, Google Cloud — [linkedin.com/in/cmanikandan](https://www.linkedin.com/in/cmanikandan)  
> **Core Mental Model:** *Plan big, execute fast, decide small, and review everything.*

Every slide, architecture diagram, live Gemini 4 (`Carbon`, `Argon`, `Hydrogen`), Gemini Decisions API (`gemini-decision-1`), Gemini 3.8 Live & Voice AI showcase, real **Google ADK 2.14.1** workflow graph, and zero-copy **Spanner Omni × BigQuery Borderless Apache Iceberg** telemetry pipeline in this repository runs end-to-end on Google Cloud architecture with live measured numbers.

---

## Live Measured Highlights (Captured Against Production Gemini APIs)

### 1. Head-to-Head Control Plane Race: `gemini-decision-1` vs. `gemini-3.8-flash` vs. `gemini-4-hydrogen`

- **Use Case:** MonsoonPay incoming SEV-1 payment alert gated on **8 real-time security & routing rules** OR **50 simultaneous RBI / PCI-DSS / SOC-2 compliance checks** before invoking an agent.
- **Methodology:** Identical alert payload evaluated live on the Gemini API — `gemini-decision-1` via `POST /v1beta/decisions` (1 forward pass, **0 output tokens**) vs. `gemini-3.8-flash` (`thinking_budget=0`) and `gemini-4-hydrogen` (`thinking_level=low`) returning strict JSON via `generateContent`. Costs calculated from exact API `usage_metadata` at Nov 2026 list prices.

| Benchmark | Model | Latency | Billed Output Tokens | Cost / 1M Calls | Speedup / Savings |
| :--- | :--- | ---: | ---: | ---: | :--- |
| **8-Question Guardrail Gate** *(Live)* | **`gemini-decision-1`** | **290 ms** | **0** | **$80.50** | **Baseline ($0 output)** |
| **8-Question Guardrail Gate** *(Live)* | `gemini-3.8-flash` *(budget=0)* | 2,921 ms | 111 | $381.90 | 10.1x slower · 4.7x costlier |
| **8-Question Guardrail Gate** *(Live)* | `gemini-4-hydrogen` *(low)* | 7,817 ms | 733 | $6,159.00 | 27.0x slower · 76.5x costlier |
| **50 Simultaneous RBI/PCI Checks** *(Live)* | **`gemini-decision-1`** | **270 ms** | **0** | **$270.70** | **Baseline ($0 output)** |
| **50 Simultaneous RBI/PCI Checks** *(Live)* | `gemini-3.8-flash` *(budget=0)* | 5,479 ms | 755 | $2,296.70 | **20.3x slower · 8.5x costlier** |
| **50 Simultaneous RBI/PCI Checks** *(Live)* | `gemini-4-hydrogen` *(low)* | 7,693 ms | 1,641 | $14,457.00 | **28.5x slower · 53.4x costlier** |
| **100-Question Scaling** *(Google Nov 2026)* | **`gemini-decision-1`** | **359 ms** | **0** | — | **20.1x vs Flash (7.2s) · 24.0x vs Hydrogen (8.6s)** |

### 2. Six Live Engineering & Voice AI Demos

1. **Demo 01 — Plan Big + Execute Fast (`demos/demo1_antigravity_swarm.py`):** Live `gemini-4-carbon` planned the Google Cloud `asia-south2` (Delhi) Cloud Run / Envoy recovery (`12.3s`) and caught subtle probe edge cases; 3 parallel `gemini-4-hydrogen` workers executed inside isolated `git worktree add --detach` sandboxes (`24.30s` wall vs. `43.25s` sequential → **`1.78x` speedup**, `0` merge conflicts), handing off to an Antigravity Remote Agent VM (`agy --remote-agent`).
2. **Demo 02 — Enterprise Code Modernization (`demos/demo5_code_modernization.py`):** Live `gemini-4-carbon` extracted 5 hidden RBI/GST/idempotency invariants from a legacy `O(N²)` Indian UPI settlement monolith (`358.4 ms`), live **`gemini-4-argon`** synthesized a clean 87-line `O(N)` engine on Attempt 1 (`11.1s`), and our locked unmodified golden conformance falsifier proved **`94.3x` faster (`358.4 ms → 3.80 ms`, `-98.94%`)**, **100% bit-exact SHA-256 parity**, **`0.00 INR` drift** on 8,000 transactions (`INR 56,232,066.19` net payout), and `6/6` adversarial edge cases passing.
3. **Demo 03 — Gemini Decisions API Arena (`demos/demo2_decisions_arena.py`):** Live 4-event security & routing control plane (`0` output tokens), live 8Q & 50Q race against `gemini-3.8-flash` & `gemini-4-hydrogen`, plus single-pass multimodal scoring of `assets/diagrams/07_gcp_data_cloud.jpg` (`illustrated_architecture_diagram`, clarity `2.52/3.0`).
4. **Demo 04A & 04B — Real Voice AI Recordings (Google Drive):**
   - **4A (`Gemini 3.8 Live Extended Thinking`):** Live 1 FPS camera + 16kHz voice flight cancellation rebooking (`PNR LH8942X`) executing `NON_BLOCKING` BigQuery & Firestore SQL + EU261 compensation with zero dead air — [Watch on Google Drive](https://drive.google.com/file/d/1KkvhldhlXGUEYQMLs28EMQXsSeAbZRZO/view).
   - **4B (`Gemini VoiceAI — Indian PSTN Integration`):** Real multilingual Indian PSTN/VoLTE call (EN, HI, TA, KN, TE, Hinglish) into Cloud Load Balancing + Cloud Armor → Cloud Run Gen2 (`asia-south1`) → Firestore, comparing Direct Speech-to-Speech vs. Cascading Listen-Think-Speak — [Watch on Google Drive](https://drive.google.com/file/d/1kv3NheXiAbhIBhYuBDUMRBCa054gIE9M/view).
5. **Demo 05 — Google ADK 2.14.1 + Zero-Copy Data Cloud (`demos/demo3_voice_adk_multicloud.py`):** Real `google.adk.Workflow` DAG calls live `gemini-decision-1`, resolves Knowledge Catalog semantic join paths, executes a zero-copy DuckDB join over **40,000 Spanner Omni × BigQuery Apache Iceberg Parquet rows in `162.4 ms`** (isolating `gcp:asia-south2` `p99=431.8ms` / `18,006` Envoy retries vs. healthy `gcp:asia-south1` `p99=16.1ms`, Software TrueTime drift `2.75ms`), and pauses natively at `@node(require_confirmation=True)` — narrated with real **Gemini 3.8 HD Audio**.
6. **Demo 06 — Review Everything (`demos/demo4_review_shipped_pr.py`):** Deterministic 500-request burst benchmark verified **`-97.1%` checkout p99 drop** (`478.55 ms → 13.95 ms`) with **10/10 `pytest` passing** — yet live `gemini-4-carbon` adversarial code review returned **`CHANGES_REQUESTED`**, catching **4 subtle pre-merge security and concurrency findings**.

---

## Repository Map

```text
├── monsoonpay/                       # 100% Google Cloud-native reference platform
│   ├── seed_multicloud_data.py       # Seeds 10k Spanner Omni SQLite + 40k BigQuery Iceberg Parquet rows
│   ├── circuit_breaker.py            # Spanner Omni Software TrueTime bounded stale-read circuit breaker
│   ├── decisions_gate.py             # Real REST client for POST /v1beta/decisions (text + multimodal)
│   ├── adk_workflow.py               # Real Google ADK 2.14.1 Workflow DAG + DuckDB + native HITL pause
│   └── legacy_settlement.py          # Legacy O(N²) Indian UPI settlement monolith + golden conformance falsifier
├── tests/
│   └── test_monsoonpay.py            # 10 automated pytest verification tests
├── demos/
│   ├── demo1_antigravity_swarm.py    # Live Carbon architect + 3 parallel Hydrogen git-worktree workers
│   ├── demo2_decisions_arena.py      # 4 events + Live 8Q/50Q Flash/Hydrogen race + Multimodal check
│   ├── demo3_voice_adk_multicloud.py # Real ADK 2.14.1 + DuckDB + Gemini 3.8 HD Audio (+ --live-mic)
│   ├── demo4_review_shipped_pr.py    # SLA burst benchmark + pytest + Live Carbon adversarial PR review
│   ├── demo5_code_modernization.py   # Live Carbon invariant extraction + Argon O(N) synthesis + Golden Falsifier
│   ├── reset_environment.py          # Clean reset utility (git worktrees, code, Spanner/Iceberg DB, optional traces)
│   ├── stage_workbench.py            # FastAPI Stage Command Center (SSE live streaming + Reset API on :8765)
│   ├── studio.html                   # Interactive Web UI + 1920x1080 cinema recorder (`?record=1`)
│   ├── record_demos.mjs              # 1080p 30fps CDP + FFmpeg MP4 & Gemini 3.8 audio muxer
│   └── traces/                       # Real captured API traces + mastered Gemini 3.8 HD WAV tracks
├── assets/
│   ├── diagrams/                     # 8 clean 16:9 architecture diagrams (01..08)
│   └── videos/                       # 5 embedded 1080p 30fps H.264 MP4s + 7 crisp PNG posters
├── presentation/
│   ├── keynote_deck.html             # Self-contained 25-slide HTML5 keynote (F, S, G shortcuts)
│   ├── build_html_keynote.py         # Builds keynote_deck.html dynamically from live traces
│   ├── build_google_slides.py        # Builds 25-slide Google Slides v3 deck + PDF/PPTX export
│   ├── Periodic_Table_of_Agents_DevFest_Keynote.pdf
│   ├── Periodic_Table_of_Agents_DevFest_Keynote.pptx
│   └── google_slides_metadata.json   # Live Google Slides v3 & Drive video URLs
└── SPEAKER_RUN_OF_SHOW.md            # 30-minute stage playbook for all 25 slides
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

### 2. Launch the Interactive Stage Command Center Web UI (Recommended — No CLI on Stage!)
Export `GEMINI_API_KEY` transiently in your shell and launch the Web UI on your laptop:
```bash
export GEMINI_API_KEY="<your-gemini-api-key>"
.venv/bin/python demos/stage_workbench.py --open
# Opens http://127.0.0.1:8765 automatically
```
Inside the Web UI:
- **6 Keynote Tabs (`1`–`6`)**: `/swarm Outage`, `Code Modernize`, `Decisions Arena`, `ADK + Lakehouse`, `Carbon PR Audit`, and `Voice AI Live` (1-click Google Drive launch for Demos 4A & 4B).
- **`⚡ Run LIVE`**: Executes real Gemini APIs with a live visual phase stepper & event stream — then renders fresh live results directly on the visual stage.
- **`▶ Replay` (`R`)**: Instant zero-Wi-Fi animated replay from the latest verified trace (including synchronized Gemini 3.8 HD audio with **`🔊 Audio ON/OFF`** on Tab 4).
- **`? Behind the Scenes` (`B`)**: Plain-English 4-card breakdown explaining what executes live vs. local fixtures and the exact stage takeaway for every demo.
- **`Auto-Reset` toggle + `⟲ Reset ▾` menu**: Automatically prunes stale git worktrees, verifies clean `monsoonpay/` code, and re-seeds Spanner Omni (`10k` rows) + BigQuery Iceberg (`40k` rows) after every live demo — or trigger **Reset Code & Backend** / **Full Factory Reset (+ Traces & Pytest)** anytime with one click.

### 3. Clean Reset via CLI (Optional)
```bash
# Quick reset: prune git worktrees, restore clean monsoonpay/ code, re-seed 10k Spanner + 40k Iceberg
.venv/bin/python demos/reset_environment.py

# Full Factory Reset: also restore committed baseline traces & audio + run 10/10 pytest
.venv/bin/python demos/reset_environment.py --restore-traces --verify-tests
```

### 4. Present the 25-Slide Keynote Deck (Offline-Safe, Embedded 1080p 30fps Videos + Audio)
Open [`presentation/keynote_deck.html`](presentation/keynote_deck.html) in Chrome/Edge:
- **`ArrowRight` / `Space`** — Next slide
- **`F`** — Fullscreen auditorium mode
- **`S`** — Private Speaker Teleprompter & 30:00 keynote timer
- **`G`** — 25-slide jump grid