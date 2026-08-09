from __future__ import annotations

"""Explicit capability-probe dispatcher.

This module is deliberately separate from discovery. Calling run_probe() is an
explicit execution decision and may import provider-specific probe adapters.
"""

from importlib import import_module
from typing import Any, Mapping

from executors.provider_registry import get_provider

EXECUTOR_ID = "PROVIDER_CAPABILITY_PROBE"
EXECUTOR_VERSION = "0.18.0"

_ADAPTERS = {
    "geometry_nodes": "executors.provider_probes.geometry_nodes",
}


def run_probe(provider: Mapping[str, Any]) -> dict[str, Any]:
    provider_id = str(provider.get("provider_id") or "")
    definition = get_provider(provider_id)
    if not definition:
        return {"provider_id": provider_id, "probe_state": "BLOCKED", "cleanup_state": "NOT_APPLICABLE", "side_effects_detected": False, "capabilities": [], "warnings": [], "blockers": [{"reason": "UNCLASSIFIED_PROVIDER"}]}
    if not bool(provider.get("enabled", False)) and definition.get("source_kind") not in {"BUILTIN_BACKEND", "READY_ASSET_SOURCE"}:
        return {"provider_id": provider_id, "probe_state": "DISABLED", "cleanup_state": "NOT_APPLICABLE", "side_effects_detected": False, "capabilities": [], "warnings": [], "blockers": [{"reason": "PROVIDER_DISABLED"}]}
    probe_type = str(definition.get("probe_type") or "")
    module_path = _ADAPTERS.get(probe_type)
    if not module_path:
        return {"provider_id": provider_id, "probe_state": "PROBE_REQUIRED", "cleanup_state": "NOT_APPLICABLE", "side_effects_detected": False, "capabilities": [], "warnings": [{"reason": "PROBE_ADAPTER_NOT_IMPLEMENTED", "probe_type": probe_type}], "blockers": []}
    adapter = import_module(module_path)
    return adapter.run(dict(provider))


def run_inventory_probes(inventory: Mapping[str, Any], provider_ids: list[str] | None = None) -> dict[str, Any]:
    wanted = set(provider_ids or [])
    results = []
    for provider in inventory.get("providers", []) or []:
        provider_id = str(provider.get("provider_id") or "")
        if wanted and provider_id not in wanted:
            continue
        if str(provider.get("runtime_probe_status") or provider.get("probe_state") or "PROBE_REQUIRED") == "NOT_APPLICABLE":
            continue
        results.append(run_probe(provider))
    return {"status": "PASS" if all(r.get("probe_state") in {"PASS", "PROBE_REQUIRED", "DISABLED"} for r in results) else "FAIL", "validator_id": EXECUTOR_ID, "results": results}
