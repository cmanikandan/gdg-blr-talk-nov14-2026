#!/usr/bin/env python3
"""
DevFest Bengaluru 2026 Keynote — Interactive Web Stage Command Center (`demos/stage_workbench.py`).

Serves `demos/studio.html` at http://127.0.0.1:8765 with:
  - One-click LIVE execution with real-time Server-Sent Events (SSE) progress streaming
    (`/api/stream/demo1`..`demo5`) — zero command-line showcasing required on stage!
  - Instant zero-Wi-Fi Trace Replay (`GET /api/traces`) + synchronized Gemini 3.8 HD WAV audio
  - One-click Clean Code & Backend Reset (`POST /api/reset`) + optional automatic post-demo reset
    (`?auto_reset=1`), resetting git worktrees, core code files, Spanner Omni SQLite (10k rows),
    and BigQuery Borderless Iceberg Parquet (40k rows).
  - Live environment health telemetry (`GET /api/status`).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
import webbrowser
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Optional, Tuple

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from demos.reset_environment import get_environment_status, reset_environment

TRACES_DIR = REPO_ROOT / "demos" / "traces"

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
BOX_ONLY_RE = re.compile(r"^[\s╭╮╰╯─━│┃┏┓┗┛┡┩╇╈┼├┤┬┴═║╔╗╚╝]+$")

DEMO_REGISTRY: Dict[str, Dict[str, Any]] = {
    "demo1": {
        "script": "demo1_antigravity_swarm.py",
        "trace": "demo1_trace.json",
        "title": "Gemini 4 Neon Plans + 3 Parallel Hydrogen Builders",
        "steps": [
            "Step 1: Gemini 4 Neon Plans the Fix",
            "Step 2: 3 Hydrogen Workers Build in Parallel",
            "Step 3: Automated Tests & Cloud Handoff",
        ],
        "phase_markers": [
            ("Phase 1:", 0),
            ("Phase 2:", 1),
            ("Live Antigravity", 2),
            ("Trace saved", 2),
        ],
    },
    "demo5": {
        "script": "demo5_code_modernization.py",
        "trace": "demo5_trace.json",
        "title": "Gemini 4 Neon Rewrites Legacy UPI Engine (0.00 INR Error)",
        "steps": [
            "Step 1: Measure Slow Legacy Code",
            "Step 2: Neon Discovers 5 Hidden RBI Rules",
            "Step 3: Neon Rewrites & Proves 0.00 INR Error",
        ],
        "phase_markers": [
            ("Phase 1:", 0),
            ("Phase 2:", 1),
            ("Phase 3:", 2),
            ("Trace saved", 2),
        ],
    },
    "demo2": {
        "script": "demo2_decisions_arena.py",
        "trace": "demo2_trace.json",
        "title": "Instant Security & Compliance Guardrails ($0 Output Cost)",
        "steps": [
            "Round A: 4 Live Events x 8 Instant Security Checks",
            "Round B: Live Speed & Cost Race vs Flash & Hydrogen",
            "Round C: Instant Architecture Diagram Check",
        ],
        "phase_markers": [
            ("Round A:", 0),
            ("Round B1", 1),
            ("Round C:", 2),
            ("Trace saved", 2),
        ],
    },
    "demo3": {
        "script": "demo3_voice_adk_multicloud.py",
        "trace": "demo3_trace.json",
        "title": "Voice Check-In + Automated Workflow + Unified Cloud Data",
        "steps": [
            "Step 1: Google ADK 2.0 + Zero-Copy Cloud Data Join",
            "Step 2: Generate Gemini 3.8 HD Voice Response",
            "Step 3: Pause at Human Approval Gate",
        ],
        "phase_markers": [
            ("Phase 1:", 0),
            ("Phase 2:", 1),
            ("Trace saved", 2),
        ],
    },
    "demo4": {
        "script": "demo4_review_shipped_pr.py",
        "trace": "demo4_trace.json",
        "title": "Review Everything: Load Test + Gemini 4 Neon Cyber Audit",
        "steps": [
            "Step 1: 500-User Flash-Sale Load Test",
            "Step 2: Run Automated Test Suite (10 Tests)",
            "Step 3: Live Gemini 4 Neon Security Review",
        ],
        "phase_markers": [
            ("500-Request Burst", 0),
            ("pytest suite", 1),
            ("Independent Security Review", 2),
            ("Trace saved", 2),
        ],
    },
}

app = FastAPI(title="The Periodic Table of Agents — Interactive Stage Command Center")

_RUN_LOCK = asyncio.Lock()
_LAST_RESET_INFO: Optional[Dict[str, Any]] = None
_LAST_RUN_INFO: Optional[Dict[str, Any]] = None


@app.middleware("http")
async def add_no_cache_headers(request: Request, call_next):
    response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith(("/api/", "/traces/")):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return response


app.mount("/assets", StaticFiles(directory=str(REPO_ROOT / "assets")), name="assets")
if TRACES_DIR.exists():
    app.mount("/traces", StaticFiles(directory=str(TRACES_DIR)), name="traces")


class ResetRequest(BaseModel):
    reset_code: bool = True
    restore_traces: bool = False
    verify_tests: bool = False


def _load_all_traces() -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for idx in ("demo1", "demo2", "demo3", "demo4", "demo5"):
        p = TRACES_DIR / f"{idx}_trace.json"
        if p.exists():
            try:
                out[idx] = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
    return out


def _sse_pack(event: str, data: Dict[str, Any]) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def _clean_log_line(raw: str) -> str:
    clean = ANSI_RE.sub("", raw).strip()
    if not clean or BOX_ONLY_RE.match(clean):
        return ""
    # Strip decorative outer box pipes from Rich tables/panels while keeping content readable
    clean = clean.strip("│┃").strip()
    if not clean or BOX_ONLY_RE.match(clean):
        return ""
    return clean


@app.get("/")
def serve_studio():
    return FileResponse(REPO_ROOT / "demos" / "studio.html")


@app.get("/api/status")
def api_status():
    st = get_environment_status()
    return JSONResponse(
        {
            **st,
            "busy": _RUN_LOCK.locked(),
            "last_reset": _LAST_RESET_INFO,
            "last_run": _LAST_RUN_INFO,
        }
    )


@app.get("/api/traces")
def get_all_traces():
    st = get_environment_status()
    return JSONResponse(
        {
            "live_key_configured": st["live_key_configured"],
            "status": st,
            "traces": _load_all_traces(),
            "audio_bust": int(time.time()),
        }
    )


@app.post("/api/reset")
async def api_reset(payload: ResetRequest = ResetRequest()):
    global _LAST_RESET_INFO
    if _RUN_LOCK.locked():
        raise HTTPException(status_code=409, detail="A live demo is currently executing. Please wait.")
    async with _RUN_LOCK:
        res = await asyncio.to_thread(
            reset_environment,
            reset_code=payload.reset_code,
            restore_traces=payload.restore_traces,
            verify_tests=payload.verify_tests,
        )
        _LAST_RESET_INFO = {
            "timestamp_utc": res["timestamp_utc"],
            "elapsed_ms": res["elapsed_ms"],
            "restore_traces": res["restore_traces"],
            "actions": res["actions"],
        }
        if payload.restore_traces:
            res["traces"] = _load_all_traces()
            res["audio_bust"] = int(time.time())
        return JSONResponse(res)


@app.get("/api/stream/{demo_id}")
async def stream_live_demo(
    demo_id: str,
    auto_reset: int = Query(default=1, ge=0, le=1),
):
    """Streams live demo progress over Server-Sent Events (SSE) and optionally resets backend cleanly afterward."""
    if demo_id not in DEMO_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Unknown demo: {demo_id}")
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(
            status_code=400,
            detail="GEMINI_API_KEY is not exported in this shell. Export it before starting stage_workbench.py.",
        )

    meta = DEMO_REGISTRY[demo_id]
    steps = list(meta["steps"])
    if auto_reset:
        steps.append("Auto-Reset: Prune Worktrees & Re-Seed Backend")

    async def event_generator() -> AsyncIterator[str]:
        global _LAST_RESET_INFO, _LAST_RUN_INFO

        if _RUN_LOCK.locked():
            yield _sse_pack("error", {"message": "Another live demo or reset is already running."})
            return

        async with _RUN_LOCK:
            t0 = time.perf_counter()
            yield _sse_pack(
                "start",
                {
                    "demo_id": demo_id,
                    "title": meta["title"],
                    "steps": steps,
                    "auto_reset": bool(auto_reset),
                },
            )
            yield _sse_pack("phase", {"step_index": 0, "label": steps[0]})

            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"
            env["NO_COLOR"] = "1"
            env["TERM"] = "dumb"
            env["COLUMNS"] = "140"

            script_path = REPO_ROOT / "demos" / meta["script"]
            proc = await asyncio.create_subprocess_exec(
                sys.executable,
                "-u",
                str(script_path),
                cwd=str(REPO_ROOT),
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )

            current_step = 0
            tail_lines: List[str] = []

            assert proc.stdout is not None
            try:
                while True:
                    raw_line = await proc.stdout.readline()
                    if not raw_line:
                        break
                    decoded = raw_line.decode("utf-8", errors="replace")
                    cleaned = _clean_log_line(decoded)
                    if not cleaned:
                        continue
                    tail_lines.append(cleaned)
                    if len(tail_lines) > 25:
                        tail_lines.pop(0)

                    # Detect phase progression from script output
                    for marker, target_idx in meta["phase_markers"]:
                        if marker in cleaned and target_idx > current_step:
                            current_step = target_idx
                            yield _sse_pack(
                                "phase",
                                {"step_index": current_step, "label": steps[current_step]},
                            )

                    yield _sse_pack(
                        "log",
                        {
                            "line": cleaned,
                            "elapsed_ms": int((time.perf_counter() - t0) * 1000),
                        },
                    )
            except asyncio.CancelledError:
                proc.terminate()
                try:
                    await asyncio.wait_for(proc.wait(), timeout=3.0)
                except asyncio.TimeoutError:
                    proc.kill()
                # Always prune any interrupted worktree cleanly on cancel
                await asyncio.to_thread(
                    reset_environment, reset_code=False, restore_traces=False, verify_tests=False
                )
                raise

            returncode = await proc.wait()
            elapsed_ms = int((time.perf_counter() - t0) * 1000)

            if returncode != 0:
                err_tail = " | ".join(tail_lines[-5:]) or f"Process exited with code {returncode}"
                # Still clean up any stray worktrees on error
                await asyncio.to_thread(
                    reset_environment, reset_code=False, restore_traces=False, verify_tests=False
                )
                yield _sse_pack(
                    "error",
                    {
                        "message": err_tail[-500:],
                        "returncode": returncode,
                        "status": get_environment_status(),
                    },
                )
                return

            trace_path = TRACES_DIR / meta["trace"]
            trace_data = json.loads(trace_path.read_text(encoding="utf-8"))
            audio_bust = int(time.time())
            yield _sse_pack(
                "trace",
                {
                    "demo_id": demo_id,
                    "trace": trace_data,
                    "audio_bust": audio_bust,
                },
            )

            reset_res = None
            if auto_reset:
                reset_step_idx = len(steps) - 1
                yield _sse_pack(
                    "phase",
                    {"step_index": reset_step_idx, "label": steps[reset_step_idx]},
                )
                reset_res = await asyncio.to_thread(
                    reset_environment,
                    reset_code=True,
                    restore_traces=False,
                    verify_tests=False,
                )
                _LAST_RESET_INFO = {
                    "timestamp_utc": reset_res["timestamp_utc"],
                    "elapsed_ms": reset_res["elapsed_ms"],
                    "restore_traces": False,
                    "actions": reset_res["actions"],
                }
                yield _sse_pack("reset", reset_res)

            final_status = reset_res["status"] if reset_res else get_environment_status()
            _LAST_RUN_INFO = {
                "demo_id": demo_id,
                "elapsed_ms": elapsed_ms,
                "auto_reset": bool(auto_reset),
                "completed_utc": final_status["checked_at_utc"],
            }
            yield _sse_pack(
                "done",
                {
                    "ok": True,
                    "demo_id": demo_id,
                    "elapsed_ms": elapsed_ms,
                    "auto_reset": bool(auto_reset),
                    "status": final_status,
                },
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/api/run/{demo_id}")
async def run_live_demo(demo_id: str, auto_reset: int = Query(default=1, ge=0, le=1)):
    """Synchronous JSON fallback endpoint to run a live demo (kept for backwards compatibility)."""
    if demo_id not in DEMO_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Unknown demo: {demo_id}")
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(status_code=400, detail="Export GEMINI_API_KEY to execute live demos.")

    meta = DEMO_REGISTRY[demo_id]
    async with _RUN_LOCK:
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            str(REPO_ROOT / "demos" / meta["script"]),
            cwd=str(REPO_ROOT),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise HTTPException(status_code=500, detail=stderr.decode("utf-8", errors="replace")[-800:])
        trace_data = json.loads((TRACES_DIR / meta["trace"]).read_text(encoding="utf-8"))
        if auto_reset:
            await asyncio.to_thread(
                reset_environment, reset_code=True, restore_traces=False, verify_tests=False
            )
        return JSONResponse(trace_data)


def main() -> None:
    import uvicorn

    parser = argparse.ArgumentParser(
        description="Launch The Periodic Table of Agents Interactive Stage Web UI."
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765, help="Bind port (default: 8765)")
    parser.add_argument("--open", action="store_true", help="Automatically open default browser")
    parser.add_argument(
        "--reset-on-start",
        action="store_true",
        help="Run clean backend/worktree reset before starting the server",
    )
    args = parser.parse_args()

    if args.reset_on_start:
        r = reset_environment(reset_code=True, restore_traces=False, verify_tests=False)
        print(f"✔ Pre-flight reset clean in {r['elapsed_ms']} ms")

    st = get_environment_status()
    url = f"http://{args.host}:{args.port}"
    print("\n" + "=" * 74)
    print("  THE PERIODIC TABLE OF AGENTS — INTERACTIVE STAGE COMMAND CENTER")
    print("=" * 74)
    print(f"  Web UI URL   : {url}")
    print(
        f"  Gemini API   : {'LIVE READY (GEMINI_API_KEY detected)' if st['live_key_configured'] else 'REPLAY MODE (export GEMINI_API_KEY for live API calls)'}"
    )
    print(
        f"  Backend Data : Spanner Omni {st['spanner_rows']:,} rows · BigQuery Iceberg {st['iceberg_rows']:,} rows · Clean={st['backend_clean']}"
    )
    print("=" * 74 + "\n")

    if args.open:
        webbrowser.open(url)

    uvicorn.run("demos.stage_workbench:app", host=args.host, port=args.port, reload=False)


if __name__ == "__main__":
    main()
