"""
Gemini Decisions API (`gemini-decision-1`) Single-Pass Guardrail & ADK 2.0 Router.

Evaluates calibrated `noul`, `choice`, and `score` outputs from a single 150-250ms
forward pass ($0.10/1M input tokens, $0.00 output tokens) before dispatching to
Hydrogen, Argon, or Carbon nodes inside the Google ADK 2.0 workflow graph.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class DecisionAnswer:
    noul: float = 0.0
    choice: str = ""
    score: float = 0.0


@dataclass(frozen=True)
class DecisionsPayload:
    answers: Dict[str, DecisionAnswer]
    latency_ms: int = 167


@dataclass(frozen=True)
class GateVerdict:
    allowed: bool
    action: str
    target_model: Optional[str]
    adk2_entry_node: str
    require_hitl_approval: bool
    latency_ms: int


@dataclass(frozen=True)
class QuarantineVerdict(GateVerdict):
    def __init__(self, reason: str, latency_ms: int = 162) -> None:
        super().__init__(
            allowed=False,
            action=f"QUARANTINE:{reason}",
            target_model=None,
            adk2_entry_node="security_quarantine_sink",
            require_hitl_approval=True,
            latency_ms=latency_ms,
        )


MODEL_MAP = {
    "hydrogen": "gemini-4-hydrogen",
    "argon": "gemini-4-argon",
    "carbon": "gemini-4-carbon",
}


def route_to_adk2_graph(
    model: str,
    require_hitl: bool = False,
    latency_ms: int = 167,
) -> GateVerdict:
    resolved_model = MODEL_MAP.get(model, model)
    if resolved_model == "gemini-4-carbon":
        entry_node = "orchestrator_carbon_multicloud_swarm"
    elif resolved_model == "gemini-4-argon":
        entry_node = "argon_service_refactor_node"
    else:
        resolved_model = "gemini-4-hydrogen"
        entry_node = "hydrogen_fast_worker_node"

    return GateVerdict(
        allowed=True,
        action="DISPATCH_ADK2_WORKFLOW",
        target_model=resolved_model,
        adk2_entry_node=entry_node,
        require_hitl_approval=require_hitl,
        latency_ms=latency_ms,
    )


def evaluate_decisions_gate(decision: DecisionsPayload) -> GateVerdict:
    """Enforces deterministic probability thresholds over `gemini-decision-1` scores."""
    inj = decision.answers.get("prompt_injection_attempt", DecisionAnswer())
    if inj.noul >= 0.70:
        return QuarantineVerdict(reason="adversarial_input", latency_ms=decision.latency_ms)

    leak = decision.answers.get("contains_live_credentials", DecisionAnswer())
    if leak.noul >= 0.65:
        return QuarantineVerdict(reason="credential_exposure", latency_ms=decision.latency_ms)

    hitl = decision.answers.get("production_blast_radius", DecisionAnswer()).score >= 70.0
    choice = decision.answers.get("target_element", DecisionAnswer(choice="hydrogen")).choice
    return route_to_adk2_graph(
        model=choice,
        require_hitl=hitl,
        latency_ms=decision.latency_ms,
    )
