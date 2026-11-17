"""Shared helpers for live DevFest 2026 keynote demos (never hardcodes API keys)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
TRACES_DIR = REPO_ROOT / "demos" / "traces"
AUDIO_DIR = TRACES_DIR / "audio"


def sanitize_proxy_env() -> None:
    """Strip IPv6 bracket entries like `[::1]` from NO_PROXY that break httpx==0.28 URL parsing."""
    for var in ("NO_PROXY", "no_proxy"):
        raw = os.environ.get(var, "")
        if not raw:
            continue
        cleaned = [part.strip() for part in raw.split(",") if part.strip() and ":" not in part]
        if cleaned:
            os.environ[var] = ",".join(cleaned)


def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Export GEMINI_API_KEY before running live demos."
        )
    return key


def get_genai_client():
    """Returns an initialized google.genai.Client using GEMINI_API_KEY from environment."""
    sanitize_proxy_env()
    from google import genai

    return genai.Client(api_key=get_api_key())


def save_trace(filename: str, payload: dict[str, Any]) -> Path:
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = TRACES_DIR / filename
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out_path
