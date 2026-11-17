#!/usr/bin/env python3
"""
14-test verification suite for the OmniPulse Multi-Cloud Agent Mesh (PR #1).

Validates:
- `gemini-decision-1` adversarial injection & credential leak quarantine
- Calibrated routing across `gemini-4-hydrogen`, `gemini-4-argon`, and `gemini-4-carbon`
- Spanner Omni cross-cloud circuit breaker transitions & full-jitter backoff
- Software TrueTime bounded stale-read fallback (< 15ms uncertainty)
- End-to-end ADK 2.0 `BaseNode` multicloud workflow + HITL review checkpoint
"""

import unittest

from demos.omnipulse_adk2_multicloud_agent import ADK2WorkflowGraph
from omnipulse.decisions_gate import (
    DecisionAnswer,
    DecisionsPayload,
    QuarantineVerdict,
    evaluate_decisions_gate,
)
from omnipulse.spanner_omni_circuit_breaker import (
    MAX_ENVOY_PENDING_REQUESTS,
    RETRY_POLICY,
    TRUETIME_STALE_READ_FALLBACK_MS,
    CircuitState,
    EnvoyPoolExhaustedError,
    SpannerOmniCircuitBreaker,
)


class TestOmniPulseShippedPR(unittest.TestCase):
    # --- Decisions API Guardrails & Routing (6 tests) ---

    def test_01_quarantines_prompt_injection_under_250ms(self) -> None:
        payload = DecisionsPayload(
            answers={"prompt_injection_attempt": DecisionAnswer(noul=0.984)},
            latency_ms=162,
        )
        verdict = evaluate_decisions_gate(payload)
        self.assertIsInstance(verdict, QuarantineVerdict)
        self.assertFalse(verdict.allowed)
        self.assertEqual(verdict.action, "QUARANTINE:adversarial_input")
        self.assertEqual(verdict.adk2_entry_node, "security_quarantine_sink")
        self.assertLess(verdict.latency_ms, 250)

    def test_02_quarantines_live_credential_exposure(self) -> None:
        payload = DecisionsPayload(
            answers={
                "prompt_injection_attempt": DecisionAnswer(noul=0.02),
                "contains_live_credentials": DecisionAnswer(noul=0.96),
            },
            latency_ms=158,
        )
        verdict = evaluate_decisions_gate(payload)
        self.assertFalse(verdict.allowed)
        self.assertEqual(verdict.action, "QUARANTINE:credential_exposure")

    def test_03_routes_routine_task_to_hydrogen_fast_lane(self) -> None:
        payload = DecisionsPayload(
            answers={
                "prompt_injection_attempt": DecisionAnswer(noul=0.01),
                "target_element": DecisionAnswer(choice="hydrogen"),
                "production_blast_radius": DecisionAnswer(score=12.0),
            }
        )
        verdict = evaluate_decisions_gate(payload)
        self.assertTrue(verdict.allowed)
        self.assertEqual(verdict.target_model, "gemini-4-hydrogen")
        self.assertEqual(verdict.adk2_entry_node, "hydrogen_fast_worker_node")
        self.assertFalse(verdict.require_hitl_approval)

    def test_04_routes_service_refactor_to_argon_workhorse(self) -> None:
        payload = DecisionsPayload(
            answers={
                "target_element": DecisionAnswer(choice="argon"),
                "production_blast_radius": DecisionAnswer(score=44.0),
            }
        )
        verdict = evaluate_decisions_gate(payload)
        self.assertEqual(verdict.target_model, "gemini-4-argon")
        self.assertEqual(verdict.adk2_entry_node, "argon_service_refactor_node")

    def test_05_routes_multicloud_spike_to_carbon_with_hitl_gate(self) -> None:
        payload = DecisionsPayload(
            answers={
                "target_element": DecisionAnswer(choice="carbon"),
                "production_blast_radius": DecisionAnswer(score=92.0),
            }
        )
        verdict = evaluate_decisions_gate(payload)
        self.assertEqual(verdict.target_model, "gemini-4-carbon")
        self.assertEqual(verdict.adk2_entry_node, "orchestrator_carbon_multicloud_swarm")
        self.assertTrue(verdict.require_hitl_approval)

    def test_06_unknown_choice_defaults_safely_to_hydrogen(self) -> None:
        payload = DecisionsPayload(answers={"target_element": DecisionAnswer(choice="unknown")})
        verdict = evaluate_decisions_gate(payload)
        self.assertEqual(verdict.target_model, "gemini-4-hydrogen")

    # --- Spanner Omni Circuit Breaker & TrueTime Fallback (6 tests) ---

    def test_07_envoy_pool_capacity_tuned_to_512(self) -> None:
        self.assertEqual(MAX_ENVOY_PENDING_REQUESTS, 512)
        self.assertEqual(RETRY_POLICY, "jittered_exponential_circuit_breaker")
        self.assertEqual(TRUETIME_STALE_READ_FALLBACK_MS, 15)

    def test_08_healthy_leader_read_returns_13_4ms_p99(self) -> None:
        cb = SpannerOmniCircuitBreaker()
        res = cb.read_checkout_session("ord-9001", pending_requests=180, truetime_drift_ms=2.9)
        self.assertEqual(res.source, "spanner_omni_leader")
        self.assertAlmostEqual(res.latency_ms, 13.4)
        self.assertEqual(res.circuit_state, CircuitState.CLOSED)

    def test_09_opens_circuit_and_serves_local_truetime_replica_on_timeouts(self) -> None:
        cb = SpannerOmniCircuitBreaker(failure_threshold=2)

        def timeout_leader(_order_id: str) -> float:
            raise TimeoutError("cross-cloud transient S3 retry burst")

        first = cb.read_checkout_session("ord-1", pending_requests=210, leader_fn=timeout_leader)
        self.assertEqual(first.source, "spanner_omni_local_stale_replica")
        self.assertEqual(cb.state, CircuitState.CLOSED)

        second = cb.read_checkout_session("ord-2", pending_requests=220, leader_fn=timeout_leader)
        self.assertEqual(second.source, "spanner_omni_local_stale_replica")
        self.assertEqual(cb.state, CircuitState.OPEN)

        # Subsequent call short-circuits directly to local replica in 6.8ms without hitting leader
        third = cb.read_checkout_session("ord-3", pending_requests=200, leader_fn=timeout_leader)
        self.assertEqual(third.latency_ms, 6.8)
        self.assertEqual(third.circuit_state, CircuitState.OPEN)

    def test_10_half_open_probe_recovers_to_closed_when_leader_heals(self) -> None:
        cb = SpannerOmniCircuitBreaker(failure_threshold=1)
        cb.read_checkout_session(
            "ord-1",
            pending_requests=100,
            leader_fn=lambda _: (_ for _ in ()).throw(TimeoutError()),
        )
        self.assertEqual(cb.state, CircuitState.OPEN)
        cb.probe_half_open()
        self.assertEqual(cb.state, CircuitState.HALF_OPEN)
        healed = cb.read_checkout_session("ord-2", pending_requests=90, leader_fn=lambda _: 12.1)
        self.assertEqual(healed.source, "spanner_omni_leader")
        self.assertEqual(cb.state, CircuitState.CLOSED)

    def test_11_rejects_stale_fallback_if_truetime_drift_exceeds_15ms(self) -> None:
        cb = SpannerOmniCircuitBreaker(failure_threshold=1)
        with self.assertRaises(RuntimeError):
            cb.read_checkout_session(
                "ord-drift",
                pending_requests=120,
                truetime_drift_ms=19.5,
                leader_fn=lambda _: (_ for _ in ()).throw(TimeoutError()),
            )

    def test_12_raises_when_pending_requests_exceed_512_cap(self) -> None:
        cb = SpannerOmniCircuitBreaker()
        with self.assertRaises(EnvoyPoolExhaustedError):
            cb.read_checkout_session("ord-burst", pending_requests=513)

    # --- Backoff Jitter & End-to-End ADK 2.0 Graph Integration (2 tests) ---

    def test_13_jittered_exponential_backoff_stays_within_bounds(self) -> None:
        cb = SpannerOmniCircuitBreaker()
        for attempt in range(6):
            delay = cb.compute_backoff_ms(attempt, base_ms=12.0, cap_ms=120.0)
            self.assertGreaterEqual(delay, 6.0)
            self.assertLessEqual(delay, 120.0)

    def test_14_adk2_multicloud_graph_emits_hitl_pr_approval_request(self) -> None:
        graph = ADK2WorkflowGraph()
        events = graph.run("Investigate Spanner Omni + AWS S3 Iceberg checkout p99 spike")
        self.assertEqual(len(events), 4)
        self.assertIsNotNone(events[-1].requested_input)
        self.assertIn("PR", str(events[-1].requested_input))


if __name__ == "__main__":
    unittest.main(verbosity=2)
