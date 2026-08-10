from __future__ import annotations

"""Explicit capability-probe dispatcher.

Discovery and probing are intentionally separated. Only this explicit execution
layer may import provider-specific probe adapters.
"""

from importlib import import_module
from typing import Any, Mapping

from executors.provider_registry import get_provider

EXECUTOR_ID = "PROVIDER_CAPABILITY_PROBE"
EXECUTOR_VERSION = "0.18.0"

_ADAPTERS = {
    "geometry_nodes": "executors.provider_probes.geometry_nodes",
    "sapling": "executors.provider_probes.sapling",
    "ivygen": "executors.provider_probes.ivygen",
    "ant_landscape": "executors.provider_probes.ant_landscape",
    "sverchok": "executors.provider_probes.sverchok",
    "mpfb": "executors.provider_probes.mpfb",
    "geo_nodes_guide": "executors.provider_probes.geo_nodes_guide",
    "mcp": "executors.provider_probes.mcp",
    "meshy": "executors.provider_probes.meshy",
}


def _base(provider_id: str, state: str, reason: str | None = None, **extra: Any) -> dict[str, Any]:
    payload = {
        "provider_id": provider_id,
        "probe_state": state,
        "cleanup_state": "NOT_APPLICABLE",
        "side_effects_detected": False,
        "capabilities": [],
        "warnings": [],
        "blockers": ([{"reason": reason}] if reason else []),
    }
    payload.update(extra)
    return payload


def run_probe(provider: Mapping[str, Any]) -> dict[str, Any]:
    provider_id = str(provider.get("provider_id") or "")
    definition = get_provider(provider_id)
    if not definition:
        return _base(provider_id, "BLOCKED", "UNCLASSIFIED_PROVIDER")
    if not bool(provider.get("enabled", False)) and definition.get("source_kind") not in {"BUILTIN_BACKEND", "READY_ASSET_SOURCE"}:
        return _base(provider_id, "DISABLED", "PROVIDER_DISABLED")
    probe_type = str(definition.get("probe_type") or "")
    module_path = _ADAPTERS.get(probe_type)
    if not module_path:
        return _base(provider_id, "PROBE_REQUIRED", warnings=[{"reason": "PROBE_ADAPTER_NOT_IMPLEMENTED", "probe_type": probe_type}], blockers=[])
    adapter = import_module(module_path)
    result = adapter.run(dict(provider))
    if result.get("cleanup_state") == "FAIL" or result.get("side_effects_detected") is True:
        result["probe_state"] = "FAIL"
        result.setdefault("blockers", []).append({"reason": "PROBE_CLEANUP_FAILED"})
    return result


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
    states = {str(r.get("probe_state")) for r in results}
    status = "FAIL" if "FAIL" in states else ("BLOCKED" if "BLOCKED" in states else "PASS")
    return {"status": status, "validator_id": EXECUTOR_ID, "results": results}
