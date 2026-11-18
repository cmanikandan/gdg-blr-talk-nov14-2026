"""
Legacy Procedural UPI / Merchant Settlement Monolith (v1 — Pre-Modernization Baseline).

Represents a typical 10-year-old enterprise banking/payments settlement batch engine:
  - O(N^2) linear deduplication scan across all seen UTRs
  - Repeated per-row dictionary lookups & procedural state mutation
  - Exact business invariants buried across undocumented magic thresholds:
      * Duplicate UTRs must be ignored idempotently (first occurrence wins)
      * REVERSAL entries subtract gross amount from merchant ledger and carry 0 MDR / 0 GST
      * UPI payments <= 200,000 paise (INR 2,000) have 0% MDR (RBI zero-MDR mandate)
      * UPI payments > 200,000 paise & CARD/NETBANKING have tier-based MDR:
          - ENTERPRISE: 0.45% (45 bps), STANDARD: 0.85% (85 bps)
          - High-value RBI compliance flag if gross_paise >= 5,000,000 (INR 50,000)
      * GST is strictly 18% of MDR fee, rounded half-up to nearest integer paise
      * Net payout = gross_paise - mdr_paise - gst_paise

Used as the real input to our Gemini 4 Code Modernization demo (1M Context + Long Decode +
Antigravity `/teamwork` unmodified golden test falsifier pattern).
"""

from __future__ import annotations

import hashlib
import json
import random
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List


def _round_half_up_paise(val: Decimal) -> int:
    return int(val.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def legacy_settle_batch(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Slow, legacy O(N^2) procedural settlement engine — ground-truth business semantics."""
    seen_utrs: List[str] = []  # Legacy O(N^2) linear list scan!
    merchant_totals: Dict[str, Dict[str, int]] = {}
    duplicate_count = 0
    rbi_flagged_utrs: List[str] = []

    for rec in records:
        utr = rec["utr"]
        # Legacy O(N) linear membership check per transaction -> O(N^2) total
        is_dup = False
        for old_utr in seen_utrs:
            if old_utr == utr:
                is_dup = True
                break
        if is_dup:
            duplicate_count += 1
            continue
        seen_utrs.append(utr)

        mid = rec["merchant_id"]
        if mid not in merchant_totals:
            merchant_totals[mid] = {
                "txn_count": 0,
                "gross_paise": 0,
                "mdr_paise": 0,
                "gst_paise": 0,
                "net_payout_paise": 0,
            }

        gross = int(rec["amount_paise"])
        tx_type = rec["tx_type"]
        rail = rec["rail"]
        tier = rec["merchant_tier"]

        if tx_type == "REVERSAL":
            merchant_totals[mid]["txn_count"] += 1
            merchant_totals[mid]["gross_paise"] -= gross
            merchant_totals[mid]["net_payout_paise"] -= gross
            continue

        if gross >= 5_000_000:
            rbi_flagged_utrs.append(utr)

        if rail == "UPI" and gross <= 200_000:
            mdr = 0
        else:
            bps = Decimal("45") if tier == "ENTERPRISE" else Decimal("85")
            mdr = _round_half_up_paise((Decimal(gross) * bps) / Decimal("10000"))

        gst = _round_half_up_paise((Decimal(mdr) * Decimal("18")) / Decimal("100"))
        net = gross - mdr - gst

        merchant_totals[mid]["txn_count"] += 1
        merchant_totals[mid]["gross_paise"] += gross
        merchant_totals[mid]["mdr_paise"] += mdr
        merchant_totals[mid]["gst_paise"] += gst
        merchant_totals[mid]["net_payout_paise"] += net

    # Canonical deterministic digest for bit-exact conformance verification
    canonical = json.dumps(
        {
            "merchants": dict(sorted(merchant_totals.items())),
            "duplicate_count": duplicate_count,
            "rbi_flagged_utrs": sorted(rbi_flagged_utrs),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return {
        "processed_unique": len(seen_utrs),
        "duplicate_count": duplicate_count,
        "rbi_flagged_count": len(rbi_flagged_utrs),
        "merchant_count": len(merchant_totals),
        "total_net_payout_paise": sum(m["net_payout_paise"] for m in merchant_totals.values()),
        "total_mdr_paise": sum(m["mdr_paise"] for m in merchant_totals.values()),
        "total_gst_paise": sum(m["gst_paise"] for m in merchant_totals.values()),
        "sha256_parity_digest": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    }


def generate_golden_upi_batch(n: int = 8000, seed: int = 20261114) -> List[Dict[str, Any]]:
    """Generates a deterministic Indian UPI/Card/NetBanking settlement batch with duplicates & reversals."""
    rng = random.Random(seed)
    merchants = [f"MRC-BLR-{i:03d}" for i in range(1, 51)]
    rails = ["UPI", "UPI", "UPI", "CARD", "NETBANKING"]
    records: List[Dict[str, Any]] = []
    utr_pool: List[str] = []

    for i in range(n):
        if utr_pool and i % 17 == 0:
            # Inject duplicate UTR for idempotency testing
            utr = utr_pool[i % len(utr_pool)]
        else:
            utr = f"UTR2026BLR{i:07d}"
            utr_pool.append(utr)

        rail = rails[i % len(rails)]
        tier = "ENTERPRISE" if i % 4 == 0 else "STANDARD"
        tx_type = "REVERSAL" if i % 29 == 0 else "CAPTURE"
        if i % 43 == 0:
            amount_paise = rng.randint(5_000_000, 12_000_000)  # RBI high-value
        elif rail == "UPI" and i % 2 == 0:
            amount_paise = rng.randint(10_000, 199_900)  # Zero-MDR UPI tier
        else:
            amount_paise = rng.randint(205_000, 1_500_000)

        records.append(
            {
                "utr": utr,
                "merchant_id": merchants[i % len(merchants)],
                "amount_paise": amount_paise,
                "tx_type": tx_type,
                "rail": rail,
                "merchant_tier": tier,
            }
        )
    return records
