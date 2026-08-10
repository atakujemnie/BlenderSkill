from __future__ import annotations

"""Canonical v0.18 provider decision pipeline.

The orchestrator preserves independent evidence dimensions instead of collapsing
provider discovery, capability, compatibility, domain, license and quality into
one opaque status.
"""

from typing import Any, Mapping

from executors.expected_provider_gate import evaluate as evaluate_expected
from executors.procedural_provider import evaluate as evaluate_compatibility
from executors.provider_probe_runner import run_inventory_probes
from executors.provider_quality import select as select_quality
from executors.provider_registry import get_provider
from executors.provider_selection_report import build_report

EXECUTOR_ID = "PROVIDER_DECISION_PIPELINE"
EXECUTOR_VERSION = "0.18.0"

_SOURCE_PRIORITY = {
    "READY_ASSET_SOURCE": 5,
    "PROCEDURAL_GENERATOR": 4,
    "BUILTIN_BACKEND": 3,
    "EXTERNAL_GENERATOR": 2,
    "UTILITY": 1,
    "UNKNOWN": 0,
}


def _merged_definition(provider: Mapping[str, Any], probe: Mapping[str, Any] | None) -> dict[str, Any]:
    provider_id = str(provider.get("provider_id") or "")
    definition = dict(get_provider(provider_id) or {})
    merged = {**definition, **dict(provider)}
    if probe:
        merged["probe"] = dict(probe)
        merged["probe_state"] = probe.get("probe_state")
    merged.setdefault("execution_type", definition.get("execution_type", "UTILITY"))
    merged.setdefault("license_policy", definition.get("license_policy"))
    merged.setdefault("supports_seed", definition.get("supports_seed", False))
    merged.setdefault("probe_required", str(merged.get("source_kind")) != "READY_ASSET_SOURCE")
    return merged


def _automatic_selection(report: Mapping[str, Any]) -> str | None:
    eligible = [item for item in report.get("candidates", []) or [] if item.get("selection_state") in {"ELIGIBLE", "ELIGIBLE_GENERIC"}]
    if not eligible:
        return None
    eligible.sort(
        key=lambda item: (
            1 if item.get("domain_state") == "MATCH" else 0,
            _SOURCE_PRIORITY.get(str(item.get("source_kind")), 0),
            str(item.get("provider_id")),
        ),
        reverse=True,
    )
    return str(eligible[0]["provider_id"])


def evaluate(
    inventory: Mapping[str, Any],
    *,
    requested_domains: list[str],
    expected_providers: list[Mapping[str, Any]] | None = None,
    selected_provider_id: str | None = None,
    run_probes: bool = False,
    probe_provider_ids: list[str] | None = None,
    quality: Mapping[str, Mapping[str, Any]] | None = None,
    usage_class: str = "MID",
    allow_custom_fallback: bool = False,
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

    probe_bundle = {"status": "SKIPPED", "results": []}
    if run_probes:
        probe_bundle = run_inventory_probes(inventory, provider_ids=probe_provider_ids)
    probe_by_id = {str(item.get("provider_id")): item for item in probe_bundle.get("results", []) or []}

    eligibility: dict[str, dict[str, Any]] = {}
    quality_input = quality or {}
    for provider in inventory.get("providers", []) or []:
        provider_id = str(provider.get("provider_id") or "")
        probe = probe_by_id.get(provider_id)
        merged = _merged_definition(provider, probe)
        probe_state = str((probe or {}).get("probe_state") or merged.get("probe_state") or merged.get("runtime_probe_status") or "PROBE_REQUIRED")
        state: dict[str, Any] = {"probe_state": probe_state}

        if not get_provider(provider_id):
            state.update({"compatibility_state": "UNKNOWN", "license_state": "UNKNOWN", "quality_state": "UNRATED"})
            eligibility[provider_id] = state
            continue

        compatibility = evaluate_compatibility(
            merged,
            {"blender_version": inventory.get("blender_version", "UNKNOWN"), "background": True},
            require_determinism=False,
            require_known_license=True,
        )
        state["compatibility_state"] = "PASS" if compatibility["status"] == "PASS" else "BLOCKED"
        state["license_state"] = "PASS" if merged.get("license_policy") else "BLOCKED"

        q = dict(quality_input.get(provider_id) or {})
        if q:
            quality_result = select_quality([{**merged, **q, "provider_id": provider_id, "probe_state": probe_state}], usage_class)
            state["quality_state"] = "PASS" if quality_result.get("selected_provider_id") == provider_id else "REJECTED"
        else:
            state["quality_state"] = "UNRATED"
        eligibility[provider_id] = state

    provisional = build_report(
        inventory,
        requested_domains=requested_domains,
        expected_provider_gate_status=expected["status"],
        eligibility=eligibility,
    )

    for candidate in provisional.get("candidates", []) or []:
        state = eligibility.get(str(candidate.get("provider_id")), {})
        if state.get("compatibility_state") == "BLOCKED" and candidate.get("selection_state") in {"ELIGIBLE", "ELIGIBLE_GENERIC"}:
            candidate["selection_state"] = "BLOCKED"
            candidate.setdefault("reason", []).append("BLENDER_VERSION_OR_PROVIDER_CONTRACT_BLOCKED")
        if state.get("license_state") == "BLOCKED" and candidate.get("selection_state") in {"ELIGIBLE", "ELIGIBLE_GENERIC"}:
            candidate["selection_state"] = "BLOCKED"
            candidate.setdefault("reason", []).append("LICENSE_POLICY_BLOCKED")

    auto_selected = _automatic_selection(provisional)
    chosen = selected_provider_id or auto_selected

    if selected_provider_id and selected_provider_id.startswith("custom"):
        stronger = [c for c in provisional.get("candidates", []) or [] if c.get("selection_state") in {"ELIGIBLE", "ELIGIBLE_GENERIC"}]
        if stronger or not allow_custom_fallback:
            return {
                "status": "BLOCKED",
                "validator_id": EXECUTOR_ID,
                "stage": "CUSTOM_FALLBACK_GATE",
                "expected_provider_gate": expected,
                "capability_probes": probe_bundle,
                "selection_report": provisional,
                "blockers": [{"reason": "CUSTOM_FALLBACK_BLOCKED", "eligible_provider_ids": [c.get("provider_id") for c in stronger]}],
            }

    report = build_report(
        inventory,
        requested_domains=requested_domains,
        selected_provider_id=chosen,
        expected_provider_gate_status=expected["status"],
        eligibility=eligibility,
    )
    return {
        "status": report["status"],
        "validator_id": EXECUTOR_ID,
        "stage": "PROVIDER_SELECTION",
        "expected_provider_gate": expected,
        "capability_probes": probe_bundle,
        "selection_report": report,
        "selected_provider_id": chosen,
        "blockers": list(report.get("blockers") or []),
    }
