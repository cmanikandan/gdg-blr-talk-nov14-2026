#!/usr/bin/env python3
"""Unit tests verifying the OmniPulse Decisions Router & ADK 2.0 Multicloud Workflow Graph."""

import unittest
from demos.omnipulse_decisions_router import SAMPLE_EVENTS, evaluate_policy_gate
from demos.omnipulse_adk2_multicloud_agent import ADK2WorkflowGraph


class TestOmniPulseAgentArchitecture(unittest.TestCase):
    def test_prompt_injection_quarantined_fast(self) -> None:
        ev = SAMPLE_EVENTS[0]
        decision = evaluate_policy_gate(ev["simulated_scores"])
        self.assertEqual(decision.verdict, "BLOCK_QUARANTINE_INJECTION")
        self.assertEqual(decision.route_node, "security_quarantine_sink")
        self.assertLess(decision.latency_ms, 250)

    def test_secret_leak_redacted(self) -> None:
        ev = SAMPLE_EVENTS[1]
        decision = evaluate_policy_gate(ev["simulated_scores"])
        self.assertEqual(decision.verdict, "REDACT_AND_ROTATE_SECRET")

    def test_everyday_task_routes_to_hydrogen(self) -> None:
        ev = SAMPLE_EVENTS[2]
        decision = evaluate_policy_gate(ev["simulated_scores"])
        self.assertEqual(decision.selected_model, "gemini-4-hydrogen")
        self.assertEqual(decision.verdict, "FAST_LANE_HYDROGEN_WORKER")

    def test_multicloud_outage_routes_to_carbon_and_spanner_omni_mcp(self) -> None:
        ev = SAMPLE_EVENTS[3]
        decision = evaluate_policy_gate(ev["simulated_scores"])
        self.assertEqual(decision.selected_model, "gemini-4-carbon")
        self.assertEqual(decision.mcp_toolset, "spanner_omni_plus_iceberg")
        self.assertEqual(decision.verdict, "DISPATCH_ORCHESTRATOR_CARBON_SWARM")

    def test_adk2_graph_executes_and_pauses_at_hitl_review(self) -> None:
        graph = ADK2WorkflowGraph()
        events = graph.run("Cross-cloud Spanner Omni + AWS S3 Iceberg p99 spike")
        self.assertEqual(len(events), 4)
        self.assertEqual(events[0].node_id, "decision_router_node")
        self.assertEqual(events[1].node_id, "knowledge_catalog_grounding")
        self.assertEqual(events[2].node_id, "data_agent_kit_mcp")
        self.assertEqual(events[3].node_id, "orchestrator_carbon_hydrogen")
        self.assertIsNotNone(events[3].requested_input)


if __name__ == "__main__":
    unittest.main(verbosity=2)
