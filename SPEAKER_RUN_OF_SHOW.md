# Speaker Run of Show — The Periodic Table of Agents (Gemini 4 Neon Edition)

**Event:** DevFest Bengaluru 2026 Keynote  
**Speaker:** Mani, Principal Architect, Google Cloud ([linkedin.com/in/cmanikandan](https://www.linkedin.com/in/cmanikandan))  
**Deck:** 18 Slides — [`presentation/keynote_deck.html`](presentation/keynote_deck.html), [`presentation/Periodic_Table_of_Agents_DevFest_Keynote.pptx`](presentation/Periodic_Table_of_Agents_DevFest_Keynote.pptx), and Google Slides v4  
**Golden Rule:** *"Plan big. Build fast. Decide instant. Ship safe."*

---

## Pre-Stage 5-Minute Checklist

1. **Audio Check (Important for Slides 14, 15, and 16):** Confirm HDMI/USB-C audio is routed to auditorium speakers and unmuted.
   - **Slide 14 (Demo 4):** Studio-mastered **Gemini 3.8 HD Audio** synced to the live Google ADK 2.14.1 workflow trace.
   - **Slide 15 (Voice AI Part A):** Real 2:40 Gemini 3.8 Live Extended Thinking camera + voice flight rebooking recording — **plays directly inline** right beside the architecture diagram (zero Drive click-out!).
   - **Slide 16 (Voice AI Part B):** Real 3:03 Indian PSTN 6-language telephony recording on Cloud Run Mumbai — **plays directly inline** right beside the architecture diagram!
2. **Choose Your Presentation Surface:**
   - **Option A — Browser HTML5 Keynote (Recommended, Zero Wi-Fi Risk):** Open [`presentation/keynote_deck.html`](presentation/keynote_deck.html) in Chrome/Edge, press **`F`** for fullscreen, **`S`** for private speaker teleprompter + timer, and **`G`** for the 18-slide jump grid. Every single demo and both Voice AI videos play inline!
   - **Option B — PowerPoint / Apple Keynote:** Open [`presentation/Periodic_Table_of_Agents_DevFest_Keynote.pptx`](presentation/Periodic_Table_of_Agents_DevFest_Keynote.pptx) — all 7 real MP4 videos are embedded natively inside the file!
   - **Option C — Live Stage Studio Web UI:** Export `GEMINI_API_KEY` transiently and run `.venv/bin/python demos/stage_workbench.py --open` (`http://127.0.0.1:8765`). Switch tabs (`Overview` + `1`–`6`), click **`▶ Preview`** for instant animation or **`⚡ Run Live`** to call production Gemini 4 Neon / Hydrogen / Decisions APIs live on stage.
3. **Physical Prop:** Wear your fresh Google Cloud badge visibly for Slide 02!

---

## 18-Slide Keynote Playbook (~30–35 Minutes)

| Time | Slide | Beat | Stage Direction & Key Lines |
| :--- | :---: | :--- | :--- |
| **00:00–01:00** | **01** | **The Periodic Table of Agents** | High-energy walk-on. *"Today is an electric moment to build with Gemini. Just days ago Google launched Gemini 4 Neon — frontier intelligence built for speed. One simple mental model, 6 live demos, zero fluff — whether you wrote your first API call yesterday or run banking systems at scale."* |
| **01:00–02:00** | **02** | **Fresh Badge Icebreaker** | **HOLD UP BADGE!** *"Full disclosure: I am so new to Google Cloud that my badge is literally still warm from the printer — I asked Gemini 4 Hydrogen how to find the micro-kitchen this morning! The upside: I built, broke, and live-tested every single demo myself."* |
| **02:00–03:15** | **03** | **Introducing Gemini 4 Neon** | **PAUSE 3 SECONDS** for the glowing neon glass tube hero! Call out the 4 headlines: **`$3 / $15` per 1M**, **1M-token context**, **95% off cached input (`$0.15/1M`)**, and **4 thinking tiers (`low`/`medium`/`high`/`xhigh`)**. |
| **03:15–04:45** | **04** | **The Periodic Table of Gemini Agents** | Simple element shorthand for beginners and pros alike: **Hydrogen** (fast everyday work), glowing **Neon** (fast frontier orchestrator), **Carbon** (deepest research), **Argon** (enterprise stability), plus **Decisions API** (`$0` output) and **Gemini 3.8 Live** (voice that thinks while speaking). |
| **04:45–06:30** | **05** | **Public Gemini 4 Neon Benchmarks** | Point to public `blog.google` numbers: **`#1` Artificial Analysis Coding Agent Index (`58.6`)**, **`39.0%` SWE-sweep in Antigravity (`3×` over `12.8%` standalone!)**, **`90.5%` SEC-bench Pro + `0.0%` IPI bypass + `99.2%` honesty**, and Glean's quote: *"Matched or exceeded Carbon at `3×` speed & `60%` cost."* |
| **06:30–08:15** | **06** | **One Simple Mental Model + MonsoonPay Story** | Set the real-world hook: a Diwali flash sale slows Delhi UPI checkouts past `470 ms` while an aging settlement engine struggles. Walk the 4 plain-English habits: **01 Plan Big (Neon)** · **02 Build Fast (3× Hydrogen Swarm)** · **03 Decide Instant (Decisions API)** · **04 Ship Safe (Neon Cyber + Human)**. |
| **08:15–09:45** | **07** | **Google Antigravity Architecture** | Explain WHY Neon hits `39.0%` SWE-sweep (`3×` standalone): Neon acts as the calm senior orchestrator, fanning coding work out to 3 parallel Hydrogen builders in isolated sandboxes with zero merge conflicts, then handing off to a Remote Cloud VM. |
| **09:45–11:45** | **08** | **LIVE DEMO 1 · Parallel Swarm** | **Play inline video or trigger Stage Studio Tab 1 (`⚡ Run Live`).** Live `gemini-4-neon` plans the fix (`14.8s`); 3 parallel `gemini-4-hydrogen` builders finish in **`10.8s` vs `19.8s` sequential (`1.83×` faster, `0` conflicts)** and hand off to a Cloud VM. |
| **11:45–13:15** | **09** | **Why Legacy Rewrites Finally Work** | Plain-English contrast for enterprise builders: small windows missed hidden RBI rules 600 lines away; short outputs truncated mid-file. Today **1M Context + Complete Rewrite + Locked Exact Fingerprint** proves **`₹0.00` drift** before shipping. |
| **13:15–15:15** | **10** | **LIVE DEMO 2 · Legacy UPI Rewrite** | **Play inline video or Stage Studio Tab 2.** Live `gemini-4-neon` reads our slow UPI settlement engine (`411.1 ms` across 8,000 Indian payments), uncovers all 5 hidden RBI/GST rules, rewrites it cleanly on Attempt 1 → **`4.09 ms` (`100.5×` faster!)** and **`₹0.00` error across `₹5.62 Cr`**! |
| **15:15–17:15** | **11** | **Decisions API: How We Measured Live** | **PHOTO SLIDE!** Walk the exact live methodology: same Delhi outage sent to all 3 live APIs asking 8 rules and 50 RBI/PCI rules in one call. Highlight **50 Rules Live**: Decisions **`283 ms` (`$271/1M`, `0` output tokens)** vs 3.8 Flash **`6.3s` (`22.4×` slower)** vs 4 Hydrogen **`4.9s` (`$14,900/1M` = `55.0×` costlier!)**. |
| **17:15–19:00** | **12** | **LIVE DEMO 3 · Instant Guardrails & Race** | **Play inline video or Stage Studio Tab 3.** Shows prompt attacks and leaked keys blocked instantly, CSS tweaks routed to Hydrogen, outages routed to **Neon**, live 50-rule race bars, and our architecture diagram audited for leaked secrets in **`440 ms` (`$0` output)**. |
| **19:00–20:30** | **13** | **Zero-Copy Data + Human Approval** | Show the Google Cloud data layer: **Spanner Omni + BigQuery Apache Iceberg** joined live by **Google ADK 2.0 + Knowledge Catalog** (zero ETL copies!) pausing cleanly at a **Built-In Human Approval Gate**. |
| **20:30–22:30** | **14** | **LIVE DEMO 4 · Voice Check-In + Data** | **UNMUTE SPEAKERS!** Play inline video or Stage Studio Tab 4. *"I closed my laptop 10 minutes ago and check in by voice."* Real Gemini 3.8 HD Audio + live ADK 2.14.1 joining **40,000 rows in `170 ms`**, isolating Delhi's 64-slot queue, and pausing for Mani's sign-off. |
| **22:30–25:30** | **15** | **VOICE AI (A) · Live Camera + Flight Rebooking** | **EMBEDDED INLINE VIDEO!** Point to the **Left Architecture Card** (1 FPS live camera + voice → Gemini 3.8 Live dual-track brain → non-blocking BigQuery & Firestore), then hit **Play** directly on the **Right Video** — zero dead air while rebooking flight `LH8942X` & EU261! |
| **25:30–28:30** | **16** | **VOICE AI (B) · Real Indian Phone Calls** | **EMBEDDED INLINE VIDEO!** Point to the **Left Architecture Card** (Indian phone line → Cloud Armor + Load Balancing + Cloud Run Mumbai → Direct S2S or Cascaded STT+TTS → Firestore), then hit **Play** on the **Right Video** across English, Hindi, Tamil, Kannada, Telugu & Hinglish! |
| **28:30–30:30** | **17** | **LIVE DEMO 5 · Neon Cyber Defense Audit** | **Play inline video or Stage Studio Tab 5.** Climax punchline: *"500-user load test proved **`-97.1%` delay drop (`478.55ms → 13.95ms`)** and **10/10 tests green**. Yet an independent **`gemini-4-neon`** cyber reviewer (`90.5%` SEC-bench Pro · `0.0%` IPI) STILL caught a missing human-approval safeguard before merge. AI writes and audits — humans own the Merge button!"* |
| **30:30–31:30** | **18** | **Closing — Start Building Today** | Recap the 4 Monday-morning habits (**Neon · Hydrogen · Decisions API · Humans**), point to LinkedIn (`/in/cmanikandan`) & GitHub repo, and close with the warm-badge callback: *"Come say hi — look for the Principal Architect with the brand-new badge!"* |
