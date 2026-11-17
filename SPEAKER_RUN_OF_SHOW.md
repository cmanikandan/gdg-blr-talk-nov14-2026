# 🎤 30-Minute DevFest Keynote Run-of-Show & Speaker Script

**Title:** *The Periodic Table of Agents: Building with Gemini 4 & Antigravity*  
**Speaker:** Manikandan (Mani) — Principal Architect, Google Cloud  
**Duration:** 30:00 (High-energy, live-build & demo-driven)  
**Core Takeaway:** *"Plan big, execute fast, decide small, and review everything."*

---

## 🛠️ Pre-Stage Checklist (5 Minutes Before Walk-On)

1. **Tab 1 — Keynote Deck (Choose Either!):**
   - **Google Slides Deck:** [Open in Google Slides](https://docs.google.com/presentation/d/18YBK6Fdc-_WCEs6_DtVW28ZwuHNMAZTFcIrqRDw7LGg/edit)
   - **Offline HTML5 Stage Deck (with embedded 1080p MP4 autoplay + `S` Teleprompter + 30:00 Timer):** Open `presentation/keynote_deck.html` in Chrome and press `F` for Fullscreen!
2. **Tab 2 — Interactive Live Demo Console:**
   - Open `demos/live_demo_studio.html` (keys `1`, `2`, `3`, `4` jump instantly to each demo; `Space` replays; `🔊 Speak Audio` speaks the Gemini 3.8 Live response out loud!).
3. **Tab 3 — Real Shipped GitHub Pull Request #1:**
   - Open `https://github.com/cmanikandan/gdg-blr-talk-nov14-2026/pull/1` ready for the Minute-26 Finale!
4. **Terminal Window (Optional Live CLI):**
   - `cd gdg-blr-talk-nov14-2026` ready to run `python3 demos/omnipulse_decisions_router.py`, `python3 demos/omnipulse_adk2_multicloud_agent.py`, and `python3 demos/omnipulse_live38_voice_checkin.py`.

---

## ⏱️ Minute-by-Minute High-Energy Stage Arc

### Act I: The Hook, The Fresh Badge & Minute-One Kickoff (`00:00 – 05:00`)

- **`00:00 – 01:00` | Slide 1 — High-Voltage Walk-On**
  - *"Good morning DevFest!! Quick show of hands—how many of you paired with an AI coding agent this week? Keep your hands up if you closed your laptop, hopped into Bengaluru traffic, checked on your build by voice, and came back to a verified Pull Request with 14 passing tests and zero regressions! Today—zero slideware promises. In minute two we kick off a real multi-cloud build, check on it by voice mid-talk, and review the shipped PR before the clock hits zero!"*
- **`01:00 – 02:15` | Slide 2 — The Fresh Badge Wise-Crack & The 6-Month Shift (`01_hf_badge_shift.jpg`)**
  - **Hold up your badge / grin:** *"Quick confession before we touch live code on stage: I'm a Principal Architect at Google Cloud, and I am SO new to Google that I literally just got my badge! Seriously—the lamination is still warm, my badge photo still has optimism in its eyes, and yesterday I had to prompt Gemini 4 Hydrogen just to find the micro-kitchen! Which is great news for live demos, because if anything explodes on stage today, HR hasn't even replicated my manager hierarchy into Spanner yet!"*
  - **Pivot to the Shift:** *"Six months ago, an AI coding agent was a smart pair programmer chained to one giant model and your open laptop. Today, a single session plans with one model, builds in parallel with another, and keeps shipping in the cloud long after you close your lid."*
- **`02:15 – 05:00` | Slide 3 — ⚡ DEMO 1: Kick Off `/swarm` on Remote Agents & Close the Laptop!**
  - Run/play **Demo 1** (`demo1_antigravity_swarm_kickoff.mp4` or Tab `01` in `live_demo_studio.html`):
  - Show `agy --remote-agent` attaching to `cmanikandan/gdg-blr-talk-nov14-2026` inside an isolated Google-managed VM.
  - Select `Orchestrator (Carbon)` and fire `/swarm` to build **OmniPulse** (Decisions API router + ADK 2.0 workflow + Spanner Omni/Iceberg MCP + `pytest` suite).
  - Point out `Carbon` writing `plan.md`, assigning non-overlapping files to 3 `Hydrogen` workers, and then **dramatically close the terminal / half-drop the laptop lid**: *"Laptop session disconnected—cloud VM still sprinting. Let's look under the hood while it builds!"*

---

### Act II: The Periodic Table of Agents & Antigravity (`05:00 – 12:30`)

- **`05:00 – 07:00` | Slide 4 — Escaping the One-Model Trap (`02_hf_periodic_table.jpg`)**
  - Walk through the **Head First Periodic Table**: `[H] Hydrogen (#1)`, `[C] Carbon (#6)`, `[Ar] Argon (#18)`, `[Dc] Decision-1`, and `[Lv] Live 3.8`.
  - Punchline from the *Geek Bits* corner box: *"Stop paying Carbon latency and quota to rename a CSS variable—and stop asking a lightweight model to audit distributed transaction locks!"*
- **`07:00 – 09:00` | Slide 5 — Deep-Horizon Architects: `Carbon` & `Argon`**
  - **Argon (`gemini-4-argon`):** Noble, non-reactive daily workhorse for 80% of complex software & enterprise knowledge work (`$2/$10` per 1M intro, 1M context).
  - **Carbon (`gemini-4-carbon`):** Frontier intelligence—#1 on CursorBench 4.0, WANDR & AutomationBench at >2x lower task cost; 94% bug-fix resolution across 14,000-test codebases with zero regressions; **0% indirect prompt injection** on Gray Swan IPI.
- **`09:00 – 10:30` | Slide 6 — High-Velocity Fuel: `Hydrogen` (`gemini-4-hydrogen`)**
  - Adapted from Carbon (`$1.50/$7.50` flat across 1M context).
  - **The Plot Twist:** At its default `high` thinking level, Hydrogen hits **51 on the Artificial Analysis Intelligence Index** (edging past Argon's 50, and reaching **54** at `xhigh`!), runs **2.5x faster** than 3.8 Flash, triples Terminal-Bench 4.1 (57%), scores **43/43** on PlotlyDataAnalyticsBench, and batches parallel file reads natively.
- **`10:30 – 12:30` | Slide 7 — Inside Google Antigravity (`03_hf_antigravity_architecture.jpg`)**
  - **Orchestrator:** Automatically swaps Carbon (Coordinator) + Hydrogen (Workers) mid-session → **24% less quota & 19% faster** on Terminal-Bench 4.0!
  - **`/swarm` vs `/teamwork` vs `/boost`:** Live shared message board, isolated git worktrees (zero merge conflicts!), and an **Adversarial Verifier** challenging every diff.
  - **Remote Agents:** Ephemeral cloud VM + `agy-plugin-proxy` OAuth handle injection (`gh`, `gdrive`, `gslides`).

---

### Act III: Production Apps — Decisions API, ADK 2.0 & Voice Check-In (`12:30 – 20:30`)

- **`12:30 – 14:00` | Slide 8 — Decide Small: Gemini Decisions API (`04_hf_decisions_api.jpg`)**
  - Introduce `gemini-decision-1`: **Zero token-by-token decoding!**
  - One forward pass scores up to **1,000 bounded questions** (`noul` yes/no, `choice` 2–255 options, `score` ordered rubric) across multimodal inputs in **150–250ms E2E** at **$0.10 / 1M input tokens and $0.00 output tokens!**
- **`14:00 – 16:15` | Slide 9 — ⚡ DEMO 2: 32 Guardrails & Routes in 167ms**
  - Run `python3 demos/omnipulse_decisions_router.py` or play **Demo 2** (`demo2_decisions_api_167ms.mp4`):
  - Show the live latency race: **167ms** vs **2,380ms** generative JSON router (**13.9x faster**).
  - Highlight how 1 pass quarantines prompt injection (`0.99`), redacts a leaked `AKIA...` AWS key (`0.98`), sends UI tweaks to Hydrogen (`0.94`), and routes a multi-cloud p99 spike to Carbon + Spanner Omni MCP (`0.95`).
- **`16:15 – 18:00` | Slide 10 — Google ADK 2.0 + Gemini 3.8 Live (`05_hf_adk2_and_live38.jpg`)**
  - **Google ADK 2.0 (`Python`, `TS`, `Go` GA):** From 1.x agent trees to the deterministic **`Workflow Runtime` (`BaseNode` graphs)**—typed `routes`, `isolationScope` prompt sandboxing, native `RetryConfig`, `requestedInput` HITL pauses, MCP & A2A.
  - **Gemini 3.8 Live Extended Thinking:** #1 Speech-to-Speech Quality (82.6)—**reasons WHILE speaking** across 97 languages with async background tools and SynthID watermarking!
- **`18:00 – 20:30` | Slide 11 — ⚡ DEMO 3: Mid-Talk Voice Check-In + Multicloud ADK Graph!**
  - Tap **Speak Audio** in Tab `03` of `live_demo_studio.html` (or run `python3 demos/omnipulse_live38_voice_checkin.py` / play `demo3_live38_voice_multicloud_adk.mp4`):
  - Ask by voice: *"Hey Antigravity! My laptop's been closed since minute two—how's our `/swarm` build, and did Spanner Omni pass the cross-cloud check?"*
  - Watch Track 1 speak at **190ms** (*"Let me check your remote swarm board while we talk..."*) while Track 2 runs the ADK 2.0 `BaseNode` graph across `KnowledgeCatalog` → `SpannerOmniMCP` → `IcebergLakehouse`, confirming p99 dropped **390ms → 13.4ms** and **PR #1** is ready!

---

### Act IV: The Agentic Data Cloud, Bonus Firepower & Shipped PR Finale (`20:30 – 30:00`)

- **`20:30 – 22:30` | Slide 12 — Google's Agentic Data Cloud & Multicloud (`06_hf_agentic_data_cloud.jpg`)**
  - **Spanner Omni (GA):** Untethered Spanner! Runs across **GCP, AWS, Azure, OCI, K8s & Laptop Docker** using **Software TrueTime** + SQL + Graph + Vector + Columnar Engine (200x scan speedup, 2M+ downloads).
  - **Borderless Apache Iceberg Lakehouse & BigQuery Omni:** Zero-copy queries over AWS S3 & Azure Blob via Cross-Cloud Interconnect, federating AWS Glue, Unity Catalog & Snowflake Horizon + **BigQuery Graph (GA)**.
- **`22:30 – 24:15` | Slide 13 — AlloyDB Express, Knowledge Catalog & Data Agent Kit**
  - **AlloyDB Express:** `<2s` database boot for coding agents' disposable branches, scale-to-zero (`$0` idle), 10B ScaNN vectors, 3M+ QPS isolation.
  - **Knowledge Catalog + Data Agent Kit (MCP):** Resolves joins *before* SQL generation → **4x higher accuracy, 33% lower latency, 75% fewer tokens**.
- **`24:15 – 25:45` | Slide 14 — Silicon to Formal Proofs ("Wait, There's More!")**
  - **8th-Gen TPUs (`TPU 8t` & `TPU 8i`)** powering **16B+ tokens/min**; **Oracle AI Database@Google Cloud**; **Nano Banana 2.1 + `/generative_ui`**; and **AlphaProof Code** proving Signal's cryptography in Lean in weeks!
- **`25:45 – 28:00` | Slide 15 — ⚡ DEMO 4 FINALE: Review Everything & Ship Pull Request #1!**
  - Play **Demo 4** (`demo4_review_shipped_pr.mp4`) AND tab over to the real **GitHub PR #1** (`https://github.com/cmanikandan/gdg-blr-talk-nov14-2026/pull/1`)!
  - Highlight the surgical diff, 14/14 passing unit tests, 0% prompt injection audit, and click Approve: *"Autonomy proposes; architects verify!"*
- **`28:00 – 29:15` | Slide 16 — The Agentic Architect Cheat Sheet (`07_hf_mental_model_blueprint.jpg`)**
  - Pause 5 seconds for audience photos! Recap: **1. Plan Big · 2. Execute Fast · 3. Decide Small · 4. Review Everything.**
- **`29:15 – 30:00` | Slide 17 — Big Closing & Badge Callback**
  - *"Every slide, Head First infographic, ADK 2.0 + Decisions API script, video, and PR #1 is waiting for you in the repo. My Google badge is only 48 hours old—so please star the repo so they let me keep it on Monday! Thank you DevFest!!"*
