from __future__ import annotations

"""Canonical provider decision pipeline for procedural/environment tasks."""

from typing import Any, Mapping

from executors.expected_provider_gate import evaluate as evaluate_expected
from executors.provider_probe_runner import run_inventory_probes
from executors.provider_selection_report import build_report

EXECUTOR_ID = "PROVIDER_DECISION_PIPELINE"
EXECUTOR_VERSION = "0.18.0"


def evaluate(
    inventory: Mapping[str, Any],
    *,
    requested_domains: list[str],
    expected_providers: list[Mapping[str, Any]] | None = None,
    selected_provider_id: str | None = None,
    run_probes: bool = False,
    probe_provider_ids: list[str] | None = None,
    quality: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    expected = evaluate_expected(list(expected_providers or []), inventory)
    if expected["status"] != "PASS":
        return {
            "status": "BLOCKED",
            "validator_id": EXECUTOR_ID,
            "stage": "EXPECTED_PROVIDER_GATE",
            "expected_provider_gate": expected,
            "blockers": list(expected.get("blockers") or []),
        }

    eligibility: dict[str, dict[str, Any]] = {str(k): dict(v) for k, v in (quality or {}).items()}
    probes = {"status": "SKIPPED", "results": []}
    if run_probes:
        probes = run_inventory_probes(inventory, provider_ids=probe_provider_ids)
        for result in probes.get("results", []) or []:
            provider_id = str(result.get("provider_id") or "")
            eligibility.setdefault(provider_id, {})["probe_state"] = result.get("probe_state")

    report = build_report(
        inventory,
        requested_domains=requested_domains,
        selected_provider_id=selected_provider_id,
        expected_provider_gate_status=expected["status"],
        eligibility=eligibility,
    )
    return {
        "status": report["status"],
        "validator_id": EXECUTOR_ID,
        "stage": "PROVIDER_SELECTION",
        "expected_provider_gate": expected,
        "capability_probes": probes,
        "selection_report": report,
        "blockers": list(report.get("blockers") or []),
    }
