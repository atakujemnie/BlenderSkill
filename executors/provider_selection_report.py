from __future__ import annotations

"""Build an auditable provider-selection report without hiding rejected providers."""

from typing import Any, Mapping

EXECUTOR_ID = "PROVIDER_SELECTION_REPORT"
EXECUTOR_VERSION = "0.17.0"

VEGETATION_DOMAINS = {"TREE", "WOODY_PLANT", "GRASS", "GROUNDCOVER", "VINE", "SURFACE_GROWTH"}


def _broadly_relevant(provider: Mapping[str, Any], requested_domains: set[str]) -> bool:
    domains = {str(x) for x in provider.get("domains", []) or []}
    kind = str(provider.get("source_kind") or "")
    if domains & requested_domains:
        return True
    if requested_domains & VEGETATION_DOMAINS:
        return bool(domains & VEGETATION_DOMAINS) or "GENERIC_PROCEDURAL" in domains or kind == "READY_ASSET_SOURCE"
    return kind in {"READY_ASSET_SOURCE", "PROCEDURAL_GENERATOR", "EXTERNAL_GENERATOR", "BUILTIN_BACKEND"}


def build_report(
    inventory: Mapping[str, Any],
    *,
    requested_domains: list[str],
    selected_provider_id: str | None = None,
    expected_provider_gate_status: str = "PASS",
    eligibility: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    requested = {str(x) for x in requested_domains}
    eligibility = eligibility or {}
    candidates: list[dict[str, Any]] = []

    for provider in inventory.get("providers", []) or []:
        if not _broadly_relevant(provider, requested):
            continue
        provider_id = str(provider.get("provider_id"))
        domains = {str(x) for x in provider.get("domains", []) or []}
        exact_domain = bool(domains & requested)
        generic_domain = "GENERIC_PROCEDURAL" in domains
        state = dict(eligibility.get(provider_id) or {})
        probe_status = str(state.get("runtime_probe_status") or provider.get("runtime_probe_status") or "PROBE_REQUIRED")

        if state.get("status"):
            decision = str(state["status"])
            reason = state.get("reason")
        elif exact_domain:
            decision = "ELIGIBLE" if probe_status == "PASS" else "PROBE_REQUIRED"
            reason = None if probe_status == "PASS" else "RUNTIME_CAPABILITY_PROBE_REQUIRED"
        elif generic_domain:
            decision = "ELIGIBLE_GENERIC" if probe_status == "PASS" else "PROBE_REQUIRED"
            reason = "GENERIC_BACKEND" if probe_status == "PASS" else "RUNTIME_CAPABILITY_PROBE_REQUIRED"
        else:
            decision = "REJECTED"
            reason = "REQUESTED_DOMAIN_MISMATCH"

        candidates.append({
            "provider_id": provider_id,
            "display_name": provider.get("display_name"),
            "version": provider.get("version"),
            "source_kind": provider.get("source_kind"),
            "domains": sorted(domains),
            "enabled": bool(provider.get("enabled", False)),
            "runtime_probe_status": probe_status,
            "decision": decision,
            "reason": reason,
            "selected": provider_id == selected_provider_id,
        })

    blockers: list[dict[str, Any]] = []
    if expected_provider_gate_status != "PASS":
        blockers.append({"reason": "EXPECTED_PROVIDER_DISCOVERY_UNRESOLVED"})
    if selected_provider_id and not any(x["provider_id"] == selected_provider_id for x in candidates):
        blockers.append({"reason": "SELECTED_PROVIDER_NOT_IN_RELEVANT_INVENTORY", "provider_id": selected_provider_id})
    if selected_provider_id:
        selected = next((x for x in candidates if x["provider_id"] == selected_provider_id), None)
        if selected and selected["decision"] not in {"ELIGIBLE", "ELIGIBLE_GENERIC"}:
            blockers.append({"reason": "SELECTED_PROVIDER_NOT_ELIGIBLE", "provider_id": selected_provider_id, "decision": selected["decision"]})

    buckets: dict[str, list[dict[str, Any]]] = {}
    for provider in inventory.get("providers", []) or []:
        buckets.setdefault(str(provider.get("source_kind")), []).append(provider)

    return {
        "status": "PASS" if not blockers else "BLOCKED",
        "validator_id": EXECUTOR_ID,
        "requested_domains": sorted(requested),
        "inventory_summary": dict(inventory.get("summary") or {}),
        "ready_asset_sources": [x.get("provider_id") for x in buckets.get("READY_ASSET_SOURCE", [])],
        "procedural_generators": [x.get("provider_id") for x in buckets.get("PROCEDURAL_GENERATOR", [])],
        "external_generators": [x.get("provider_id") for x in buckets.get("EXTERNAL_GENERATOR", [])],
        "utilities": [x.get("provider_id") for x in buckets.get("UTILITY", [])],
        "builtin_backends": [x.get("provider_id") for x in buckets.get("BUILTIN_BACKEND", [])],
        "candidates": candidates,
        "selected_provider_id": selected_provider_id,
        "blockers": blockers,
    }
