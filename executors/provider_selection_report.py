from __future__ import annotations

"""Build an auditable provider-selection report without hiding rejected providers."""

from typing import Any, Mapping

EXECUTOR_ID = "PROVIDER_SELECTION_REPORT"
EXECUTOR_VERSION = "0.18.0"

VEGETATION_DOMAINS = {"TREE", "WOODY_PLANT", "GRASS", "GROUNDCOVER", "VINE", "SURFACE_GROWTH"}


def _broadly_relevant(provider: Mapping[str, Any], requested_domains: set[str]) -> bool:
    domains = {str(x) for x in provider.get("domains", []) or []}
    kind = str(provider.get("source_kind") or "")
    if domains & requested_domains:
        return True
    if requested_domains & VEGETATION_DOMAINS:
        return bool(domains & VEGETATION_DOMAINS) or "GENERIC_PROCEDURAL" in domains or kind == "READY_ASSET_SOURCE"
    return kind in {"READY_ASSET_SOURCE", "PROCEDURAL_GENERATOR", "EXTERNAL_GENERATOR", "BUILTIN_BACKEND", "UNKNOWN"}


def build_report(
    inventory: Mapping[str, Any],
    *,
    requested_domains: list[str],
    selected_provider_id: str | None = None,
    expected_provider_gate_status: str = "PASS",
    eligibility: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    requested = {str(x).upper() for x in requested_domains}
    eligibility = eligibility or {}
    candidates: list[dict[str, Any]] = []

    for provider in inventory.get("providers", []) or []:
        if not _broadly_relevant(provider, requested):
            continue
        provider_id = str(provider.get("provider_id"))
        domains = {str(x).upper() for x in provider.get("domains", []) or []}
        exact_domain = bool(domains & requested)
        generic_domain = "GENERIC_PROCEDURAL" in domains
        state = dict(eligibility.get(provider_id) or {})
        probe_state = str(state.get("probe_state") or state.get("runtime_probe_status") or provider.get("probe_state") or provider.get("runtime_probe_status") or "PROBE_REQUIRED")
        quality_state = str(state.get("quality_state") or "UNRATED")
        compatibility_state = str(state.get("compatibility_state") or "UNKNOWN")
        license_state = str(state.get("license_state") or "UNKNOWN")

        if exact_domain:
            domain_state = "MATCH"
        elif generic_domain:
            domain_state = "GENERIC_MATCH"
        elif domains:
            domain_state = "MISMATCH"
        else:
            domain_state = "UNKNOWN"

        reasons: list[str] = []
        if str(provider.get("source_kind")) == "UNKNOWN":
            decision = "BLOCKED"
            reasons.append("UNCLASSIFIED_PROVIDER")
        elif domain_state == "MISMATCH":
            decision = "REJECTED"
            reasons.append("REQUESTED_DOMAIN_MISMATCH")
        elif probe_state != "PASS" and str(provider.get("source_kind")) != "READY_ASSET_SOURCE":
            decision = "BLOCKED"
            reasons.append("RUNTIME_CAPABILITY_PROBE_REQUIRED" if probe_state == "PROBE_REQUIRED" else f"PROBE_{probe_state}")
        elif quality_state == "REJECTED":
            decision = "REJECTED"
            reasons.append("QUALITY_REJECTED")
        elif domain_state == "MATCH":
            decision = "ELIGIBLE"
        elif domain_state == "GENERIC_MATCH":
            decision = "ELIGIBLE_GENERIC"
            reasons.append("GENERIC_BACKEND")
        else:
            decision = "BLOCKED"
            reasons.append("DOMAIN_CLASSIFICATION_REQUIRED")

        if provider_id == selected_provider_id and decision in {"ELIGIBLE", "ELIGIBLE_GENERIC"}:
            selection_state = "SELECTED"
        else:
            selection_state = decision

        candidates.append({
            "provider_id": provider_id,
            "display_name": provider.get("display_name"),
            "version": provider.get("version"),
            "source_kind": provider.get("source_kind"),
            "domains": sorted(domains),
            "enabled": bool(provider.get("enabled", False)),
            "discovery_state": provider.get("discovery_state") or ("DISCOVERED" if provider.get("discovered", True) else "NOT_DISCOVERED"),
            "probe_state": probe_state,
            "domain_state": domain_state,
            "compatibility_state": compatibility_state,
            "license_state": license_state,
            "quality_state": quality_state,
            "selection_state": selection_state,
            "reason": reasons,
            "selected": provider_id == selected_provider_id,
        })

    blockers: list[dict[str, Any]] = []
    if expected_provider_gate_status != "PASS":
        blockers.append({"reason": "EXPECTED_PROVIDER_DISCOVERY_UNRESOLVED"})
    if selected_provider_id:
        selected = next((x for x in candidates if x["provider_id"] == selected_provider_id), None)
        if not selected:
            blockers.append({"reason": "SELECTED_PROVIDER_NOT_IN_RELEVANT_INVENTORY", "provider_id": selected_provider_id})
        elif selected["selection_state"] != "SELECTED":
            blockers.append({"reason": "SELECTED_PROVIDER_NOT_ELIGIBLE", "provider_id": selected_provider_id, "decision": selected["selection_state"]})

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
        "unknown": [x.get("provider_id") for x in buckets.get("UNKNOWN", [])],
        "candidates": candidates,
        "selected_provider_id": selected_provider_id,
        "blockers": blockers,
    }
