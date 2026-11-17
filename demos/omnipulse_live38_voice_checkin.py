#!/usr/bin/env python3
"""
Demo 3B: Mid-Talk Voice Check-In with Gemini 3.8 Live Extended Thinking
Talk: The Periodic Table of Agents: Building with Gemini 4 and Antigravity
Speaker: Mani (Principal Architect, Google Cloud)

Demonstrates how `gemini-3.8-live-extended-thinking` reasons WHILE speaking:
  - Immediate low-latency verbal turn-taking ("Let me check your remote swarm board...")
  - Parallel asynchronous tool execution against Antigravity Remote Agent & Spanner Omni MCP
  - Built-in SynthID imperceptible audio watermarking
"""

from __future__ import annotations

import asyncio
from typing import Dict, Any


LIVE_API_CONFIG_SNIPPET = """
# Production Google GenAI SDK (`google-genai>=2.34.0`) Live Session Setup:
from google import genai
from google.genai import types

client = genai.Client()
config = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_budget=2048),
    tools=[get_antigravity_swarm_status, query_spanner_omni_health],
)
async with client.aio.live.connect(
    model="gemini-3.8-live-extended-thinking", config=config
) as session:
    await session.send_realtime_input(audio=mic_pcm_chunk)
"""


async def check_swarm_board() -> Dict[str, Any]:
    await asyncio.sleep(0.15)
    return {
        "remote_vm": "agy-remote-vm-blr-01 (Active — Laptop Disconnected 16m ago)",
        "orchestrator": "Orchestrator (Carbon) -> 3 Hydrogen Workers (-24% quota, +19% speed)",
        "workers": {
            "worker-decisions": "DONE (8-question gate calibrated)",
            "worker-adk-graph": "DONE (BaseNode graph + MCP wired)",
            "worker-mcp-data": "DONE (Spanner Omni + S3 Iceberg zero-copy verified)",
            "verifier-cyber": "PASS (14/14 pytest green, 0 regressions, 0% IPI)",
        },
        "pull_request": "PR #1 Ready for Human Review",
    }


async def check_spanner_omni_mesh() -> Dict[str, Any]:
    await asyncio.sleep(0.18)
    return {
        "mesh_nodes": ["gcp:asia-south1", "aws:ap-south-1", "docker:blr-stage-laptop"],
        "truetime_drift_ms": 2.9,
        "p99_after_patch_ms": 13.4,
    }


async def run_parallel_voice_turn() -> None:
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    print(f"\n{BOLD}{CYAN}🎙️  [MANI — LIVE STAGE MIC]{RESET}")
    print('   "Hey Antigravity! My laptop has been closed since minute two—how is our /swarm build')
    print('    looking, and did Spanner Omni pass the cross-cloud latency check?"\n')

    # Track 1: Immediate natural voice stream starts at ~190ms while Track 2 tools run concurrently!
    print(f"{BOLD}{GREEN}🔊 [GEMINI 3.8 LIVE EXTENDED THINKING — AUDIO STREAM @ 190ms | SynthID Watermarked]{RESET}")
    print('   "Hey Mani! Let me check your remote swarm board and ping the Spanner Omni mesh right now..."')

    print(f"\n{YELLOW}🧠 [PARALLEL EXTENDED THINKING + ASYNC TOOL CALLS IN BACKGROUND]{RESET}")
    swarm_task = asyncio.create_task(check_swarm_board())
    mesh_task = asyncio.create_task(check_spanner_omni_mesh())
    swarm_res, mesh_res = await asyncio.gather(swarm_task, mesh_task)

    print(f"   {DIM}├─ async tool `get_antigravity_swarm_status()` -> {swarm_res['pull_request']}{RESET}")
    print(f"   {DIM}└─ async tool `query_spanner_omni_health()`    -> p99={mesh_res['p99_after_patch_ms']}ms across {mesh_res['mesh_nodes']}{RESET}\n")

    print(f"{BOLD}{GREEN}🔊 [GEMINI 3.8 LIVE — CONTINUOUS SPOKEN SYNTHESIS (ZERO DEAD AIR)]{RESET}")
    print(
        '   "Good news—your Remote Agent VM never missed a beat! Carbon finished the architecture,\n'
        '    all three Hydrogen workers and the adversarial cyber verifier passed 14 out of 14 tests\n'
        '    using 24% less quota, and Spanner Omni p99 checkout latency dropped from 390ms back down\n'
        '    to 13.4ms across GCP and AWS. Pull Request #1 is queued up whenever you are ready to review!"\n'
    )


if __name__ == "__main__":
    asyncio.run(run_parallel_voice_turn())
