# Speaker Run of Show — The Periodic Table of Agents (30:00)

**Event:** DevFest Bengaluru 2026 — Opening Keynote  
**Speaker:** Manikandan (Mani), Principal Architect, Google Cloud  
**Deck:** 22 Slides (`presentation/keynote_deck.html` & Google Slides v2)  
**Golden Rule:** *"Plan big, execute fast, decide small, and review everything."*

---

## Pre-Stage 5-Minute Checklist

1. **Audio Check (CRITICAL for Slide 17 / Demo 3):** Confirm HDMI/USB-C audio is routed to auditorium speakers and unmuted. Demo 3 (`demo3_live38_voice_multicloud_adk.mp4`) contains **real studio-mastered Gemini 3.8 HD voice audio** (`Orus` & `Puck`) synced to the live ADK 2.14.1 workflow trace.
2. **Presentation Mode:**
   - **Option A (Recommended — Zero Wi-Fi Risk, Inline 1080p 30fps Video + Audio):** Open `presentation/keynote_deck.html` in Chrome/Edge, press **`F`** for fullscreen. Press **`S`** on a mirrored/secondary screen for private speaker notes + 30:00 timer; **`G`** for slide overview.
   - **Option B (Google Slides):** Open the Google Slides URL from `presentation/google_slides_metadata.json` in Presenter View (private speaker notes included on all 22 slides; clickable HD Google Drive video links on Slides 05, 12, 17, 19).
   - **Option C (Live Stage Workbench):** Run `.venv/bin/python demos/stage_workbench.py` with `export GEMINI_API_KEY=...` and open `http://127.0.0.1:8765` to fire live API calls on stage or replay traces instantaneously.
3. **Physical Prop:** Wear your shiny new Google Cloud badge prominently for Slide 02!

---

## Minute-by-Minute Keynote Playbook

| Time | Slide | Title / Beat | Stage Direction & Key Lines |
| :--- | :---: | :--- | :--- |
| **00:00–01:00** | **01** | **The Periodic Table of Agents** | High-energy walk-on. Hook the room immediately: *"Six months ago, an AI coding agent was a smart pair programmer. Today, a single session plans with one model, builds in parallel with another, decides with zero output tokens, and keeps shipping long after you close your laptop."* |
| **01:00–02:15** | **02** | **Fresh Badge (Head First)** | **BADGE JOKE!** Hold up your physical badge: *"Full disclosure before we talk distributed systems—I am SO new to Google Cloud that my badge is still warm from the printer. I literally used Gemini 4 Hydrogen this morning just to find the micro-kitchen! The upside? Zero corporate slideware today—everything you'll see I had to build, break, and verify myself."* |
| **02:15–03:30** | **03** | **Six-Month Shift (Head First)** | Pause 3 seconds so the room laughs at the contrast. Point out the single-model bottleneck on the left vs. multi-model cloud execution on the right. |
| **03:30–04:30** | **04** | **No Slideware Promises** | Introduce **MonsoonPay** (cross-cloud checkout on Spanner Omni across GCP & AWS, Envoy logs in AWS S3 Apache Iceberg). Make the live contract: Act I kick off & close laptop; Act II voice check-in mid-talk; Act III review shipped PR before wrap. |
| **04:30–06:30** | **05** | **DEMO 01 · Minute 1 Kickoff** | **Play 1080p MP4 (13.5s) or Live Workbench.** Narrate 3 real facts: (1) Live `gemini-4-carbon` didn't just paraphrase—it flagged a `HALF_OPEN` probe flaw & benchmark blind spot; (2) 3 parallel `gemini-4-hydrogen` workers ran inside isolated `git worktree add --detach` sandboxes (`2.37x` speedup, `0` conflicts); (3) We launch `agy --remote-agent` — **mime closing the laptop lid!** |
| **06:30–08:00** | **06** | **Periodic Table (Head First)** | Unpack the five elements: `[H] 1` Hydrogen (abundant sub-second fuel), `[C] 6` Carbon (diamond-strength architect & verifier), `[Ar] 18` Argon (inert enterprise workhorse), `[Dc]` Decisions (`$0` output-token router), `[Lv]` Gemini 3.8 Live (voice that reasons while speaking). |
| **08:00–09:30** | **07** | **Gemini 4 Model Matrix** | Principal Architect selection guide: highlight Hydrogen's **4 thinking tiers (`low`/`medium`/`high`/`xhigh`)** at flat `$1.50/$7.50` across 1M tokens (hitting 54 AA Index at `xhigh`, 2.5x faster than 3.8 Flash) vs Carbon's **0% Gray Swan IPI** & **#1 CursorBench 4.0**. |
| **09:30–11:00** | **08** | **Inside Google Antigravity** | Walk Orchestrator -> `/swarm` isolated git worktrees -> Cloud Remote Agents. Emphasize why worktree isolation kills merge-conflict thrashing. |
| **11:00–12:15** | **09** | **Stop Using an LLM as an `if`** | Pivot to **your production apps**. Call out the #1 mistake teams make in 2026: burning 2–8 seconds and hundreds of autoregressive JSON output tokens on prompt-injection checks and model routing before real work even starts. |
| **12:15–13:30** | **10** | **Decisions API (Head First)** | Explain the prism: `POST /v1beta/decisions` (`gemini-decision-1`) evaluates up to **1,000 independent `noul`, `choice`, and `score` questions** over text/images/audio/PDF in **ONE forward pass**—**zero output tokens**, `$0.10/1M` input! |
| **13:30–15:15** | **11** | **Decision-1 vs Flash vs Hydrogen** | **MONEY SLIDE (pause for photos!).** Deliver our **live measured stats**: on an 8-question production control plane, `gemini-decision-1` ran in **273ms** with **0 output tokens (`$81/1M`)** — **9.1x faster** than `gemini-3.8-flash` (`2,475ms`) and **14.0x faster & 59.1x cheaper** than `gemini-4-hydrogen` (`3,826ms`, `$4,772/1M`)! On **50 simultaneous compliance checks**, Decision-1 is **8.5x cheaper than Flash** and **56.2x cheaper than Hydrogen** (`$270` vs `$15,150` per 1M calls). On Google's published 100-Q scaling benchmark: **359ms vs 7.2s Flash (20x) & 8.6s Hydrogen (24x)**. |
| **15:15–17:15** | **12** | **DEMO 02 · Decisions Arena** | **Play 1080p MP4 (15s).** Point out Round A catching Indirect Prompt Injection (`0.99`), leaked AWS/Stripe keys (`0.97`), routing CSS to Hydrogen, and routing multicloud outage to Carbon—plus Round B's bar race and Round C scoring our own Head First infographic JPEG in ONE pass! |
| **17:15–18:30** | **13** | **Gemini 3.8 Live (Head First)** | Mid-talk check-in! Explain Dual-Track Voice: conversational speech stays live and responsive in **97 languages** (plus Live Avatar GA & SynthID) while asynchronous ADK 2.0 tools execute in the background. |
| **18:30–20:00** | **14** | **Google ADK 2.0 Runtime** | Walk the real Python code from `monsoonpay/adk_workflow.py` (`google-adk==2.14.1`): `@node`, conditional `Edge(..., route=...)`, `RetryConfig(max_attempts=3)`, and **`require_confirmation=True`** for durable HITL checkpoints. Mention 5 languages (Python/Go/TS/Java/C#), MCP, and A2A. |
| **20:00–21:30** | **15** | **Agentic Data Cloud (Head First)** | Enterprise agents need enterprise data—and real enterprises are multicloud. Walk the temple roof (`Knowledge Catalog + 50+ Managed MCP Servers`) down to the 4 pillars. |
| **21:30–22:45** | **16** | **Multicloud Data Blueprint** | Crisp 4-pillar callout: **Spanner Omni GA** (Software TrueTime on GCP/AWS/Azure/OCI/K8s), **Borderless Iceberg & BQ Omni** (zero-copy over AWS S3 & Azure Blob federating Glue/Unity/Horizon), **AlloyDB Express** (`<2s` boot, scale-to-zero, 10B ScaNN vectors), **Knowledge Catalog** (`4x` SQL accuracy, `-75%` tokens). |
| **22:45–24:45** | **17** | **DEMO 03 · Voice + ADK + Multicloud** | **UNMUTE SPEAKERS! Play 1080p MP4 (44.9s with REAL Gemini 3.8 HD Audio!).** Let the auditorium HEAR Mani ask and Gemini 3.8 reply live while real ADK 2.14.1 (`482ms`) runs a zero-copy DuckDB join over **40,000 rows in 116.7ms**, isolates AWS Mumbai's 64-slot Envoy retry storm (`18,006` retries, `431.8ms` p99) while TrueTime stays rock-solid (`2.75ms`), and pauses cleanly at `hitl_pr_approval_node`! |
| **24:45–26:00** | **18** | **Four 2026 Force Multipliers** | Rapid 60-second Principal Architect radar: **8th-Gen TPUs (8t/8i, 16B+ tok/min)**, **Oracle AI Database@Google Cloud**, **Nano Banana 2.1 + Omni 1.2 + `/generative_ui`**, and **AlphaProof Code** (formal Lean proofs). |
| **26:00–27:45** | **19** | **DEMO 04 · Review Everything** | **Play 1080p MP4 (13.5s).** Deliver the climax punchline: *"Look—p99 dropped 97.1% (`478.55ms -> 13.95ms`), all 9 pytest tests passed. A naive team merges right here. Watch what happened when we pointed live `gemini-4-carbon` at our own PR: **Carbon threw `CHANGES_REQUESTED`**—catching 5 subtle security & concurrency bugs (unused `autonomy_readiness`, low-res multimodal IPI, NaN/negative TrueTime bound, HALF_OPEN race)! Frontier AI doesn't replace architects—it gives you an adversarial co-reviewer!"* |
| **27:45–28:30** | **20** | **Verified Production Impact** | Anchor the three live numbers: **`-97.1%`** p99 latency · **`56.2x`** cheaper control plane · **`5`** subtle bugs caught pre-merge. |
| **28:30–29:15** | **21** | **Mental Model Poster (Head First)** | *"Phones up—take this poster back to your engineering team on Monday."* Read all four quadrants with punch. |
| **29:15–30:00** | **22** | **Closing & Repo CTA** | Point to `github.com/cmanikandan/gdg-blr-talk-nov14-2026`. Close with the badge callback: *"Thank you DevFest Bengaluru—and if anyone knows where the best filter coffee is at Google Bengaluru, come find the Principal Architect with the brand-new badge!"* |
