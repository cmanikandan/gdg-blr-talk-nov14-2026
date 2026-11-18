#!/usr/bin/env python3
"""
DEMO 3 — Real Google ADK 2.14.1 Workflow + Zero-Copy Spanner Omni x BigQuery Apache Iceberg Join + Gemini 3.8 HD Audio.

Runs LIVE against:
  - Google ADK 2.14.1 (`Workflow`, `@node`, `Edge`, `RetryConfig`, `require_confirmation=True`)
  - Live `gemini-decision-1` inside ADK `decision_gate_node`
  - Real DuckDB zero-copy federated SQL join (10,000 Spanner Omni commits x 40,000 BigQuery Borderless Iceberg logs)
  - Live `gemini-3.8-flash-tts` synthesizing studio-grade HD voice tracks for the voice check-in & recorded MP4 video!
  - Optional `--live-mic` flag: real `gemini-3.8-live-extended-thinking` WebSocket (`BidiGenerateContent`) for stage laptop use!
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
import wave
from pathlib import Path
from typing import Any, Dict, List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from demos._common import AUDIO_DIR, get_api_key, get_genai_client, save_trace
from monsoonpay.adk_workflow import run_adk_triage

console = Console()

ALERT_INCIDENT = (
    "Hey Gemini — I closed my laptop 12 minutes ago after launching the Antigravity remote swarm. "
    "Check our Spanner Omni checkout commits against BigQuery Borderless Apache Iceberg Envoy logs in asia-south2, "
    "confirm the root cause, and tell me if Pull Request #1 is ready for my approval."
)


def _save_audio_as_wav(raw_bytes: bytes, mime_type: str, out_wav: Path) -> float:
    """Writes valid RIFF WAV (handles both direct audio/wav and raw audio/L16 PCM 24kHz) and returns duration in seconds."""
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    if raw_bytes[:4] == b"RIFF":
        out_wav.write_bytes(raw_bytes)
    else:
        # Parse sample rate from mime_type if present (default 24000 Hz 16-bit mono PCM)
        rate = 24000
        for token in (mime_type or "").split(";"):
            token = token.strip()
            if token.startswith("rate="):
                try:
                    rate = int(token.split("=", 1)[1])
                except ValueError:
                    pass
        with wave.open(str(out_wav), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(rate)
            wf.writeframes(raw_bytes)

    with wave.open(str(out_wav), "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return round(frames / float(rate), 2)


def synthesize_gemini38_voice(
    client: Any,
    text: str,
    voice_name: str,
    out_wav: Path,
) -> Dict[str, Any]:
    """Calls LIVE `gemini-3.8-flash-tts` to synthesize studio-quality Gemini 3.8 HD voice audio."""
    from google.genai import types

    t0 = time.perf_counter()
    resp = client.models.generate_content(
        model="gemini-3.8-flash-tts",
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice_name)
                )
            ),
        ),
    )
    elapsed_ms = int((time.perf_counter() - t0) * 1000)

    audio_bytes = b""
    mime_type = "audio/wav"
    for cand in getattr(resp, "candidates", []) or []:
        for part in getattr(getattr(cand, "content", None), "parts", []) or []:
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                audio_bytes = inline.data
                mime_type = getattr(inline, "mime_type", "audio/wav") or "audio/wav"
                break

    if not audio_bytes:
        raise RuntimeError(f"gemini-3.8-flash-tts returned no audio bytes for voice={voice_name}")

    duration_s = _save_audio_as_wav(audio_bytes, mime_type, out_wav)
    return {
        "model": "gemini-3.8-flash-tts",
        "voice": voice_name,
        "mime_type": mime_type,
        "wav_path": str(out_wav),
        "wav_relpath": str(out_wav.relative_to(Path(__file__).resolve().parents[1])),
        "duration_sec": duration_s,
        "synthesis_latency_ms": elapsed_ms,
        "transcript": text,
    }


async def run_live_websocket_session() -> None:
    """
    Real bidirectional `gemini-3.8-live-extended-thinking` WebSocket client for Mani's stage laptop
    (outside sandbox proxies that restrict outbound wss:// upgrades).
    """
    import websockets

    api_key = get_api_key()
    ws_url = (
        "wss://generativelanguage.googleapis.com/ws/"
        "google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent"
        f"?key={api_key}"
    )
    console.print("[bold cyan]Connecting to live Gemini 3.8 Live Extended Thinking WebSocket...[/bold cyan]")
    async with websockets.connect(ws_url, max_size=None) as ws:
        setup_msg = {
            "setup": {
                "model": "models/gemini-3.8-live-extended-thinking",
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                    "speechConfig": {
                        "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Puck"}}
                    },
                },
                "systemInstruction": {
                    "parts": [
                        {
                            "text": (
                                "You are Mani's live DevFest Bengaluru 2026 keynote co-pilot. "
                                "Acknowledge immediately while running MonsoonPay ADK 2.0 multicloud tools asynchronously."
                            )
                        }
                    ]
                },
            }
        }
        await ws.send(json.dumps(setup_msg))
        setup_ack = await ws.recv()
        console.print(f"[green]✔ Live WebSocket Connected![/green] {str(setup_ack)[:140]}")
        await ws.send(
            json.dumps(
                {
                    "clientContent": {
                        "turns": [{"role": "user", "parts": [{"text": ALERT_INCIDENT}]}],
                        "turnComplete": True,
                    }
                }
            )
        )
        for _ in range(8):
            chunk = await asyncio.wait_for(ws.recv(), timeout=15.0)
            console.print(f"[dim]Received frame ({len(chunk)} bytes)[/dim]")


async def run_demo3(skip_tts: bool = False) -> Dict[str, Any]:
    console.print(
        Panel.fit(
            "[bold green]DEMO 3 · REAL GOOGLE ADK 2.14.1 + ZERO-COPY SPANNER x BIGQUERY ICEBERG[/bold green]\n"
            "Google ADK 2.0 Workflow DAG + DuckDB (Spanner Omni x BigQuery Borderless Iceberg) + HITL Pause + Gemini 3.8 HD Voice",
            border_style="green",
        )
    )

    # 1. Execute REAL Google ADK 2.14.1 Workflow (live `gemini-decision-1` + DuckDB 40,000-row join + HITL pause)
    console.print("[bold yellow]▶ Phase 1:[/bold yellow] Executing REAL `google.adk.Workflow` DAG (`monsoonpay_agentic_triage`)...")
    t0 = time.perf_counter()
    adk_trace = await run_adk_triage(ALERT_INCIDENT)
    adk_total_ms = int((time.perf_counter() - t0) * 1000)

    tbl = Table(title=f"Real Google ADK 2.14.1 Workflow Trace ({adk_total_ms} ms total)")
    tbl.add_column("Step", justify="right", style="dim")
    tbl.add_column("ADK Node Path", style="cyan bold")
    tbl.add_column("Route / Gate", style="magenta")
    tbl.add_column("Key Output")
    for idx, step in enumerate(adk_trace, start=1):
        out = step.get("output") or {}
        if step.get("hitl_pause"):
            summary = step.get("hitl_prompt") or "HITL pause"
        elif isinstance(out, dict):
            if "verdict" in out:
                summary = f"{out['verdict']} ({out['latency_ms']}ms, out_tok={out['output_tokens']})"
            elif "rows_correlated" in out:
                summary = f"{out['rows_correlated']:,} rows joined in {out['query_latency_ms']}ms -> {out['root_cause'][:72]}..."
            elif "p99_reduction_pct" in out:
                summary = f"p99 {out['before_patch_p99_ms']}ms -> {out['after_patch_p99_ms']}ms (-{out['p99_reduction_pct']}%)"
            elif "catalog" in out:
                summary = f"{out['catalog']} ({out['sql_accuracy_lift']} SQL lift, -{out['prompt_token_reduction_pct']}% tokens)"
            else:
                summary = json.dumps(out)[:80]
        else:
            summary = str(out)[:80]
        tbl.add_row(str(idx), step["node_path"], str(step.get("route") or ("HITL_PAUSE" if step["hitl_pause"] else "next")), summary)
    console.print(tbl)

    # Extract exact verified numbers from the real ADK execution to feed into Gemini 3.8 voice synthesis!
    sql_node = next(s["output"] for s in adk_trace if "lakehouse_mcp_sql_node" in s["node_path"])
    swarm_node = next(s["output"] for s in adk_trace if "swarm_status_node" in s["node_path"])
    hotspot = sql_node["regional_breakdown"][0]

    voice_turns: List[Dict[str, Any]] = []
    if not skip_tts:
        client = get_genai_client()
        console.print("\n[bold yellow]▶ Phase 2:[/bold yellow] Synthesizing REAL Gemini 3.8 HD Voice Tracks (`gemini-3.8-flash-tts`)...")

        turn_scripts = [
            (
                "turn1_mani_checkin.wav",
                "Orus",
                "Mani (Principal Architect, Google Cloud)",
                "Hey Gemini, my laptop's been closed ten minutes. Did our remote swarm isolate the Delhi checkout spike, and is PR one ready?",
            ),
            (
                "turn2_gemini_ack.wav",
                "Puck",
                "Gemini 3.8 Live (Immediate Track)",
                "On it, Mani! Your remote Antigravity VM is still running. I'm firing ADK 2.0 right now to join Spanner Omni with your BigQuery Iceberg Envoy logs.",
            ),
            (
                "turn3_gemini_report.wav",
                "Puck",
                "Gemini 3.8 Live (ADK Tool Result)",
                (
                    f"Done! Zero-copy SQL joined {sql_node['rows_correlated']:,} events in {int(round(sql_node['query_latency_ms']))} milliseconds. "
                    f"Spanner Omni TrueTime is rock solid at {hotspot['avg_truetime_drift_ms']} milliseconds drift. "
                    f"The culprit is Delhi asia-south2's 64-slot Cloud Run Envoy pool triggering {hotspot['total_sync_retries']:,} retries and a {int(round(hotspot['p99_commit_ms']))} millisecond spike. "
                    f"Your remote swarm patch cuts p99 to {int(round(swarm_node['after_patch_p99_ms']))} milliseconds, and ADK 2.0 is paused at your confirmation gate for PR one."
                ),
            ),
        ]

        for filename, voice_name, speaker_label, script in turn_scripts:
            res = synthesize_gemini38_voice(client, script, voice_name, AUDIO_DIR / filename)
            res["speaker"] = speaker_label
            voice_turns.append(res)
            console.print(
                f"  [green]✔ {filename}[/green] (voice={voice_name}, dur={res['duration_sec']}s, synth={res['synthesis_latency_ms']}ms)"
            )

    trace = {
        "demo": "demo3_voice_adk_multicloud",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "live_api": True,
        "adk_version": "2.14.1",
        "alert_incident": ALERT_INCIDENT,
        "adk_total_ms": adk_total_ms,
        "adk_trace": adk_trace,
        "lakehouse_finding": sql_node,
        "multicloud_finding": sql_node,
        "swarm_summary": swarm_node,
        "voice_turns": voice_turns,
    }
    out = save_trace("demo3_trace.json", trace)
    console.print(f"[dim]Trace saved -> {out}[/dim]")
    return trace


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DevFest 2026 Demo 3 — Gemini 3.8 Voice + ADK 2.0 + Multicloud")
    parser.add_argument("--live-mic", action="store_true", help="Connect to real Gemini 3.8 Live WebSocket (stage laptop)")
    parser.add_argument("--skip-tts", action="store_true", help="Skip TTS synthesis and run ADK workflow only")
    args = parser.parse_args()

    if args.live_mic:
        asyncio.run(run_live_websocket_session())
    else:
        asyncio.run(run_demo3(skip_tts=args.skip_tts))
