#!/usr/bin/env python3
"""
DevFest Bengaluru 2026 Keynote — Live & Replay Stage Workbench (`demos/stage_workbench.py`).

Serves `demos/studio.html` with:
  - Instant access to all 4 verified JSON traces (`demos/traces/demo{1..4}_trace.json`) + real Gemini 3.8 HD WAV audio
  - Live execution endpoints (`/api/run/demo1`..`demo4`) when `GEMINI_API_KEY` is exported on Mani's stage laptop
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

REPO_ROOT = Path(__file__).resolve().parents[1]
TRACES_DIR = REPO_ROOT / "demos" / "traces"

app = FastAPI(title="The Periodic Table of Agents — Keynote Demo Workbench")

app.mount("/assets", StaticFiles(directory=str(REPO_ROOT / "assets")), name="assets")
if TRACES_DIR.exists():
    app.mount("/traces", StaticFiles(directory=str(TRACES_DIR)), name="traces")


@app.get("/")
def serve_studio():
    return FileResponse(REPO_ROOT / "demos" / "studio.html")


@app.get("/api/traces")
def get_all_traces():
    out = {}
    for idx, name in [
        ("demo1", "demo1_trace.json"),
        ("demo2", "demo2_trace.json"),
        ("demo3", "demo3_trace.json"),
        ("demo4", "demo4_trace.json"),
        ("demo5", "demo5_trace.json"),
    ]:
        p = TRACES_DIR / name
        if p.exists():
            out[idx] = json.loads(p.read_text(encoding="utf-8"))
    return JSONResponse({"live_key_configured": bool(os.environ.get("GEMINI_API_KEY")), "traces": out})


@app.post("/api/run/{demo_id}")
async def run_live_demo(demo_id: str):
    script_map = {
        "demo1": ("demo1_antigravity_swarm.py", "demo1_trace.json"),
        "demo2": ("demo2_decisions_arena.py", "demo2_trace.json"),
        "demo3": ("demo3_voice_adk_multicloud.py", "demo3_trace.json"),
        "demo4": ("demo4_review_shipped_pr.py", "demo4_trace.json"),
        "demo5": ("demo5_code_modernization.py", "demo5_trace.json"),
    }
    if demo_id not in script_map:
        raise HTTPException(status_code=404, detail=f"Unknown demo: {demo_id}")
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(status_code=400, detail="Export GEMINI_API_KEY to execute live demos.")

    script_name, trace_name = script_map[demo_id]
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        str(REPO_ROOT / "demos" / script_name),
        cwd=str(REPO_ROOT),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise HTTPException(status_code=500, detail=stderr.decode("utf-8", errors="replace")[-800:])
    trace_path = TRACES_DIR / trace_name
    return JSONResponse(json.loads(trace_path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("demos.stage_workbench:app", host="127.0.0.1", port=8765, reload=False)
