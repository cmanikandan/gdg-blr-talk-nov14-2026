#!/usr/bin/env python3
"""
Clean Code & Backend Reset Utility (`demos/reset_environment.py`).

Resets the MonsoonPay demo repository and local Google Cloud data plane back to a
pristine, reproducible keynote state — runnable either on-demand from the CLI, via the
Web UI "Reset Backend & Code" button, or automatically after each live demo finishes.

What it resets:
  1. Removes any leftover temporary git worktrees (`agy_swarm_wt_*`, `.worktrees/`, `.antigravity_swarm_out/`)
     and runs `git worktree prune`.
  2. Restores core MonsoonPay source & test files (`monsoonpay/*.py`, `tests/*.py`) to clean git HEAD
     when `reset_code=True`.
  3. Cleanly wipes and re-seeds the local Google Cloud data backend (`monsoonpay/data/`):
       - `spanner_omni_commits.db`        (10,000 Spanner Omni commits: asia-south1 + asia-south2)
       - `bigquery_iceberg_envoy.parquet` (40,000 BigQuery Borderless Apache Iceberg telemetry rows)
       - `knowledge_catalog.json`         (Knowledge Catalog semantic join contract)
  4. Optionally (`restore_traces=True` / `--restore-traces`), restores `demos/traces/*.json`
     and `demos/traces/audio/*.wav` back to the committed keynote baseline.
  5. Optionally (`verify_tests=True` / `--verify-tests`), runs `pytest -q` to confirm 10/10 passing.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import pyarrow.parquet as pq

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from monsoonpay.seed_multicloud_data import DATA_DIR, seed_all

TRACES_DIR = REPO_ROOT / "demos" / "traces"

CORE_CODE_PATHS = [
    "monsoonpay/circuit_breaker.py",
    "monsoonpay/decisions_gate.py",
    "monsoonpay/adk_workflow.py",
    "monsoonpay/legacy_settlement.py",
    "monsoonpay/seed_multicloud_data.py",
    "tests/test_monsoonpay.py",
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run_git(args: List[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def _list_extra_worktrees() -> List[Path]:
    """Returns any registered git worktree paths other than REPO_ROOT itself."""
    proc = _run_git(["worktree", "list", "--porcelain"])
    if proc.returncode != 0:
        return []
    repo_resolved = REPO_ROOT.resolve()
    extras: List[Path] = []
    for line in proc.stdout.splitlines():
        if line.startswith("worktree "):
            wt_path = Path(line[len("worktree ") :].strip())
            try:
                if wt_path.resolve() != repo_resolved:
                    extras.append(wt_path)
            except OSError:
                extras.append(wt_path)
    return extras


def _count_spanner_rows() -> int:
    db_path = DATA_DIR / "spanner_omni_commits.db"
    if not db_path.exists():
        return 0
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM checkout_commits")
        row = cur.fetchone()
        conn.close()
        return int(row[0]) if row else 0
    except sqlite3.Error:
        return 0


def _count_iceberg_rows() -> int:
    pq_path = DATA_DIR / "bigquery_iceberg_envoy.parquet"
    if not pq_path.exists():
        return 0
    try:
        meta = pq.read_metadata(pq_path)
        return int(meta.num_rows)
    except Exception:
        return 0


def _get_modified_code_files() -> List[str]:
    proc = _run_git(["status", "--porcelain", "--", *CORE_CODE_PATHS])
    if proc.returncode != 0:
        return []
    modified: List[str] = []
    for line in proc.stdout.splitlines():
        if line.strip():
            modified.append(line[3:].strip())
    return modified


def get_environment_status() -> Dict[str, Any]:
    """Inspects live backend health, git worktree hygiene, code cleanliness, and available traces."""
    spanner_rows = _count_spanner_rows()
    iceberg_rows = _count_iceberg_rows()
    catalog_ready = (DATA_DIR / "knowledge_catalog.json").exists()
    extra_worktrees = _list_extra_worktrees()
    leftover_dirs = [
        p for p in (REPO_ROOT / ".worktrees", REPO_ROOT / ".antigravity_swarm_out") if p.exists()
    ]
    stale_worktree_count = len(extra_worktrees) + len(leftover_dirs)
    modified_code = _get_modified_code_files()

    traces_info: Dict[str, Any] = {}
    for demo_id in ("demo1", "demo2", "demo3", "demo4", "demo5"):
        p = TRACES_DIR / f"{demo_id}_trace.json"
        if p.exists():
            mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
            traces_info[demo_id] = {"exists": True, "updated_utc": mtime, "bytes": p.stat().st_size}
        else:
            traces_info[demo_id] = {"exists": False}

    backend_clean = (
        spanner_rows == 10_000
        and iceberg_rows == 40_000
        and catalog_ready
        and stale_worktree_count == 0
        and len(modified_code) == 0
    )

    return {
        "live_key_configured": bool(os.environ.get("GEMINI_API_KEY")),
        "backend_clean": backend_clean,
        "spanner_rows": spanner_rows,
        "iceberg_rows": iceberg_rows,
        "catalog_ready": catalog_ready,
        "stale_worktrees": stale_worktree_count,
        "modified_code_files": modified_code,
        "traces": traces_info,
        "checked_at_utc": _utc_now(),
    }


def reset_environment(
    *,
    reset_code: bool = True,
    restore_traces: bool = False,
    verify_tests: bool = False,
) -> Dict[str, Any]:
    """Cleanly resets git worktrees, core MonsoonPay source code, and the local Google Cloud data backend."""
    t0 = time.perf_counter()
    actions: List[str] = []

    # 1. Remove any stale git worktrees & leftover swarm scratch folders
    removed_wts = 0
    for wt_path in _list_extra_worktrees():
        _run_git(["worktree", "remove", "--force", str(wt_path)])
        if wt_path.exists():
            shutil.rmtree(wt_path, ignore_errors=True)
        removed_wts += 1

    for leftover in (REPO_ROOT / ".worktrees", REPO_ROOT / ".antigravity_swarm_out"):
        if leftover.exists():
            shutil.rmtree(leftover, ignore_errors=True)
            removed_wts += 1

    _run_git(["worktree", "prune"])
    actions.append(f"Pruned git worktrees ({removed_wts} stale removed)")

    # 2. Restore core MonsoonPay source code & tests to clean HEAD if modified
    if reset_code:
        existing_core = [p for p in CORE_CODE_PATHS if (REPO_ROOT / p).exists()]
        if existing_core:
            proc = _run_git(["checkout", "--", *existing_core])
            if proc.returncode == 0:
                actions.append(f"Verified & restored {len(existing_core)} core code/test files to HEAD")
            else:
                actions.append("Skipped git code restore (not in a git worktree)")

    # 3. Cleanly re-seed local Spanner Omni SQLite + BigQuery Iceberg Parquet + Knowledge Catalog
    seed_stats = seed_all(seed=20261114)
    actions.append(
        f"Re-seeded Spanner Omni ({seed_stats['spanner_rows']:,} rows) + "
        f"BigQuery Iceberg ({seed_stats['iceberg_rows']:,} rows) + Knowledge Catalog"
    )

    # 4. Optionally restore committed golden traces & audio tracks (Factory Reset)
    if restore_traces:
        proc = _run_git(["checkout", "--", "demos/traces"])
        if proc.returncode == 0:
            actions.append("Restored golden baseline traces & Gemini 3.8 HD audio from git HEAD")
        else:
            actions.append("Skipped baseline trace restore (git checkout unavailable)")

    # 5. Optional quick pytest verification
    pytest_summary = None
    if verify_tests:
        pt = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        last_lines = [ln.strip() for ln in pt.stdout.splitlines() if ln.strip()]
        pytest_summary = {
            "passed": pt.returncode == 0,
            "summary": last_lines[-1] if last_lines else f"exit={pt.returncode}",
        }
        actions.append(f"Pytest verification: {pytest_summary['summary']}")

    elapsed_ms = int((time.perf_counter() - t0) * 1000)
    status = get_environment_status()
    return {
        "ok": status["backend_clean"] and (pytest_summary["passed"] if pytest_summary else True),
        "elapsed_ms": elapsed_ms,
        "reset_code": reset_code,
        "restore_traces": restore_traces,
        "actions": actions,
        "pytest": pytest_summary,
        "status": status,
        "timestamp_utc": _utc_now(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reset MonsoonPay code, git worktrees, and local Google Cloud data backend."
    )
    parser.add_argument(
        "--skip-code",
        action="store_true",
        help="Re-seed backend & prune worktrees without running git checkout on monsoonpay/ or tests/.",
    )
    parser.add_argument(
        "--restore-traces",
        action="store_true",
        help="Full Factory Reset: also restore demos/traces/*.json and audio WAVs from git HEAD.",
    )
    parser.add_argument(
        "--verify-tests",
        action="store_true",
        help="Run pytest -q after resetting to verify all 10 tests pass.",
    )
    parser.add_argument(
        "--status-only",
        action="store_true",
        help="Print current backend & workspace health as JSON without modifying anything.",
    )
    args = parser.parse_args()

    if args.status_only:
        print(json.dumps(get_environment_status(), indent=2))
        return

    res = reset_environment(
        reset_code=not args.skip_code,
        restore_traces=args.restore_traces,
        verify_tests=args.verify_tests,
    )
    print(json.dumps(res, indent=2))
    if not res["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
