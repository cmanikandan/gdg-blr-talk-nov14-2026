#!/usr/bin/env python3
"""
Seeds real queryable multi-cloud datasets for the DevFest Keynote ADK 2.0 + Data Cloud demo:
  1. monsoonpay/data/spanner_omni_commits.db   -> Operational Spanner Omni commits (GCP asia-south1 + AWS ap-south-1)
  2. monsoonpay/data/aws_s3_iceberg_envoy.parquet -> 40,000 AWS S3 Apache Iceberg/Parquet Envoy edge telemetry rows
  3. monsoonpay/data/knowledge_catalog.json    -> Semantic layer mapping verified joins & SLAs
"""

from __future__ import annotations

import json
import os
import random
import sqlite3
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

DATA_DIR = Path(__file__).resolve().parent / "data"


def seed_all(seed: int = 20261114) -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)

    # 1. SQLite representing Spanner Omni operational table (GCP + AWS active-active)
    db_path = DATA_DIR / "spanner_omni_commits.db"
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE checkout_commits (
            commit_id TEXT PRIMARY KEY,
            trace_span_id TEXT NOT NULL,
            cloud_region TEXT NOT NULL,
            merchant_tier TEXT NOT NULL,
            commit_latency_ms REAL NOT NULL,
            truetime_drift_ms REAL NOT NULL,
            status TEXT NOT NULL,
            ts_epoch INTEGER NOT NULL
        )
        """
    )

    commit_rows = []
    span_ids = []
    base_ts = 1794900000

    for i in range(10_000):
        span_id = f"tr-{i:06d}"
        span_ids.append(span_id)
        is_aws = (i % 2 == 1)
        region = "aws:ap-south-1" if is_aws else "gcp:asia-south1"
        tier = "ENTERPRISE" if i % 5 == 0 else "STANDARD"
        drift = round(rng.uniform(2.1, 3.4), 2)

        # Inject authentic cross-cloud Envoy retry burst in AWS ap-south-1 for the last 1,200 spans
        if is_aws and i >= 8800:
            latency = round(rng.uniform(285.0, 445.0), 1)
            status = "RETRY_DEGRADED" if latency > 350 else "OK_SLOW"
        else:
            latency = round(rng.uniform(7.5, 16.2), 1)
            status = "OK"

        commit_rows.append(
            (f"cm-{i:06d}", span_id, region, tier, latency, drift, status, base_ts + i)
        )

    cur.executemany(
        "INSERT INTO checkout_commits VALUES (?, ?, ?, ?, ?, ?, ?, ?)", commit_rows
    )
    cur.execute("CREATE INDEX idx_trace_span ON checkout_commits(trace_span_id)")
    conn.commit()
    conn.close()

    # 2. Apache Parquet (Iceberg table layout) representing AWS S3 Envoy edge telemetry (40,000 rows)
    parquet_path = DATA_DIR / "aws_s3_iceberg_envoy.parquet"
    trace_col = []
    edge_region_col = []
    envoy_pool_used_col = []
    envoy_pool_limit_col = []
    retry_count_col = []
    http_status_col = []

    for j in range(40_000):
        idx = j % 10_000
        span_id = span_ids[idx]
        is_burst = (idx % 2 == 1) and (idx >= 8800)
        trace_col.append(span_id)
        edge_region_col.append("aws:ap-south-1" if idx % 2 == 1 else "gcp:asia-south1")
        if is_burst:
            envoy_pool_used_col.append(rng.randint(60, 64))
            envoy_pool_limit_col.append(64)
            retry_count_col.append(rng.randint(4, 11))
            http_status_col.append(503 if j % 3 == 0 else 200)
        else:
            envoy_pool_used_col.append(rng.randint(8, 28))
            envoy_pool_limit_col.append(64)
            retry_count_col.append(0)
            http_status_col.append(200)

    table = pa.table(
        {
            "trace_span_id": trace_col,
            "edge_region": edge_region_col,
            "envoy_pending_requests": envoy_pool_used_col,
            "envoy_pool_limit": envoy_pool_limit_col,
            "synchronous_retries": retry_count_col,
            "http_status": http_status_col,
        }
    )
    pq.write_table(table, parquet_path, compression="snappy")

    # 3. Knowledge Catalog Semantic Contract
    catalog = {
        "catalog": "Google Cloud Knowledge Catalog (Universal Context Engine)",
        "domain": "monsoonpay_multicloud_checkout",
        "verified_entities": [
            {
                "entity": "spanner_omni.checkout_commits",
                "engine": "Spanner Omni (GA — GCP asia-south1 + AWS ap-south-1)",
                "local_uri": str(db_path),
                "primary_join_key": "trace_span_id",
            },
            {
                "entity": "lakehouse_iceberg.aws_s3_envoy_retries",
                "engine": "Cross-Cloud Apache Iceberg / BigQuery Omni (Zero-Copy AWS S3)",
                "local_uri": str(parquet_path),
                "primary_join_key": "trace_span_id",
            },
        ],
        "verified_join": "checkout_commits.trace_span_id = aws_s3_envoy_retries.trace_span_id",
        "slos": {"checkout_p99_ms": 25.0, "truetime_max_drift_ms": 7.0},
    }
    catalog_path = DATA_DIR / "knowledge_catalog.json"
    catalog_path.write_text(json.dumps(catalog, indent=2), encoding="utf-8")

    return {
        "spanner_rows": len(commit_rows),
        "iceberg_rows": len(trace_col),
        "db_bytes": db_path.stat().st_size,
        "parquet_bytes": parquet_path.stat().st_size,
    }


if __name__ == "__main__":
    stats = seed_all()
    print("Seeded real MonsoonPay multi-cloud data:", json.dumps(stats, indent=2))
