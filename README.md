# 🧪 The Periodic Table of Agents: Building with Gemini 4 & Antigravity

> **DevFest 2026 Keynote** · **Manikandan (Mani)**, Principal Architect, Google Cloud  
> *Plan Big · Execute Fast · Decide Small · Review Everything*

Six months ago, an AI coding agent was a smart pair programmer waiting for you to hit `Tab`. Today, a single session **plans with Carbon**, **builds in parallel with Hydrogen**, **routes in 150ms with Decision-1**, **checks in by voice with Gemini 3.8 Live**, **queries multicloud data zero-copy via ADK 2.0 + Spanner Omni & Iceberg**, and keeps shipping in the cloud long after you close your laptop.

---

## 📂 Repository Contents

| Path | Description |
| :--- | :--- |
| [`SPEAKER_RUN_OF_SHOW.md`](SPEAKER_RUN_OF_SHOW.md) | Complete 30-minute minute-by-minute keynote script, jokes, stage cues & pacing guide |
| [`presentation/keynote_deck.html`](presentation/keynote_deck.html) | **Interactive Offline HTML5 Keynote Deck** (17 slides, embedded 1080p MP4 videos, `S` speaker notes drawer, `F` fullscreen, 30:00 stage timer) |
| [`presentation/Periodic_Table_of_Agents_DevFest_Keynote.pptx`](presentation/Periodic_Table_of_Agents_DevFest_Keynote.pptx) | Exported PowerPoint backup of the 17-slide Google Slides deck |
| [`presentation/Periodic_Table_of_Agents_DevFest_Keynote.pdf`](presentation/Periodic_Table_of_Agents_DevFest_Keynote.pdf) | Exported PDF slide deck |
| [`assets/infographics/`](assets/infographics/) | **7 Custom O'Reilly "Head First" Style 16:9 Technical Infographics** |
| [`assets/videos/`](assets/videos/) | **4 Pre-Recorded 1080p HD Demo Videos (`.mp4`) + Poster Frames (`.png`)** |
| [`demos/live_demo_studio.html`](demos/live_demo_studio.html) | **Interactive Browser Mission Control Console** for all 4 stage demos + live Web Speech voice synthesis |
| [`demos/omnipulse_decisions_router.py`](demos/omnipulse_decisions_router.py) | **Demo 2 CLI:** `gemini-decision-1` evaluating 8 parallel questions (`noul`, `choice`, `score`) in ~167ms (`$0` output tokens) |
| [`demos/omnipulse_adk2_multicloud_agent.py`](demos/omnipulse_adk2_multicloud_agent.py) | **Demo 3A CLI:** Google ADK 2.0 `BaseNode` Workflow Graph + Knowledge Catalog, Spanner Omni (GA), Cross-Cloud Iceberg & AlloyDB Express MCP |
| [`demos/omnipulse_live38_voice_checkin.py`](demos/omnipulse_live38_voice_checkin.py) | **Demo 3B CLI:** `gemini-3.8-live-extended-thinking` parallel voice turn-taking + async background tool orchestration |

---

## ⚡ Quickstart: Run the Demos Locally

```bash
# 1. Run automated verification tests
python3 -m unittest demos/test_omnipulse.py -v

# 2. Demo 2: Gemini Decisions API (8 simultaneous guardrails & routes in ~167ms, $0 output tokens)
#    (Add --live with GEMINI_API_KEY exported to hit live Google AI Studio v1beta endpoint)
python3 demos/omnipulse_decisions_router.py

# 3. Demo 3A: Google ADK 2.0 Deterministic BaseNode Graph + Multicloud Data Agent Kit (MCP)
python3 demos/omnipulse_adk2_multicloud_agent.py

# 4. Demo 3B: Mid-Talk Voice Check-In (Gemini 3.8 Live Extended Thinking)
python3 demos/omnipulse_live38_voice_checkin.py
```

To open the interactive browser keynote deck or demo console:
- Open `presentation/keynote_deck.html` in Chrome/Edge/Safari (`←`/`→` navigate, `S` speaker notes, `F` fullscreen).
- Open `demos/live_demo_studio.html` (`1`–`4` switch live scenes, `Space` replays, `🔊 Speak Audio` triggers live speech).

---

## 🧠 The 4-Rule Mental Model

1. **Plan Big (`gemini-4-carbon` & `gemini-4-argon`):** Spend frontier 1M-context reasoning tokens upfront on system boundaries, contracts, and security invariants.
2. **Execute Fast (`gemini-4-hydrogen` + Antigravity `/swarm`):** Fan out parallel workers across isolated git worktrees and `<2s` AlloyDB Express sandboxes—Orchestrator saves **24% quota** and finishes **19% faster**.
3. **Decide Small (`gemini-decision-1`):** Replace slow token-decoding routers with single-pass calibrated probabilities (**150–250ms**, up to **1,000 questions**, **$0.10/1M in · $0.00 out**).
4. **Review Everything (`Verifier` + `Artifacts` + `PR`):** Pair adversarial verification agents with structured human PR sign-off grounded on **Google ADK 2.0** and the **Agentic Data Cloud** (**Spanner Omni**, **Borderless Iceberg**, **Knowledge Catalog**).