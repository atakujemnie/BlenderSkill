from __future__ import annotations

"""Resolve reusable design-system resources into asset-scoped bindings."""

from copy import deepcopy
from typing import Any, Mapping

EXECUTOR_ID = "DESIGN_BINDING_RESOLVER"
EXECUTOR_VERSION = "0.1.0"
BINDING_MODES = {"INHERITED", "OVERRIDDEN", "CUSTOM"}


def _catalog(resources: Any) -> dict[str, dict[str, Any]]:
    if isinstance(resources, Mapping):
        return {str(k): dict(v) for k, v in resources.items() if isinstance(v, Mapping)}
    out: dict[str, dict[str, Any]] = {}
    for raw in list(resources or []):
        if not isinstance(raw, Mapping):
            continue
        item = dict(raw)
        resource_id = str(item.get("resource_id") or item.get("id") or "")
        if resource_id:
            out[resource_id] = item
    return out


def resolve(spec: Mapping[str, Any]) -> dict[str, Any]:
    resources = _catalog(spec.get("resources", {}))
    bindings = spec.get("bindings", {})
    if not isinstance(bindings, Mapping):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "BINDINGS_MAPPING_REQUIRED"}],
        }

    resolved: dict[str, dict[str, Any]] = {}
    blockers: list[dict[str, Any]] = []
    deviations: list[dict[str, Any]] = []

    for binding_id, raw in sorted(bindings.items()):
        if not isinstance(raw, Mapping):
            blockers.append({"reason": "BINDING_INVALID", "binding_id": str(binding_id)})
            continue
        binding = dict(raw)
        mode = str(binding.get("mode", "INHERITED")).upper()
        if mode not in BINDING_MODES:
            blockers.append({"reason": "BINDING_MODE_INVALID", "binding_id": str(binding_id), "mode": mode})
            continue

        resource_id = str(binding.get("resource_id") or "")
        resource = resources.get(resource_id)
        if mode in {"INHERITED", "OVERRIDDEN"} and resource is None:
            blockers.append(
                {"reason": "DESIGN_RESOURCE_MISSING", "binding_id": str(binding_id), "resource_id": resource_id}
            )
            continue

        if mode == "CUSTOM":
            custom = binding.get("custom")
            if not isinstance(custom, Mapping):
                blockers.append({"reason": "CUSTOM_BINDING_PAYLOAD_REQUIRED", "binding_id": str(binding_id)})
                continue
            resolved[str(binding_id)] = {
                "binding_id": str(binding_id),
                "mode": mode,
                "resource_id": None,
                "resolved": deepcopy(dict(custom)),
                "locked": False,
            }
            deviations.append({"binding_id": str(binding_id), "kind": "CUSTOM_RESOURCE"})
            continue

        assert resource is not None
        payload = deepcopy(resource)
        locked = bool(resource.get("locked", False) or binding.get("locked", False))
        requested_version = binding.get("version")
        actual_version = resource.get("version")
        if requested_version is not None and str(requested_version) != str(actual_version):
            blockers.append(
                {
                    "reason": "DESIGN_RESOURCE_VERSION_MISMATCH",
                    "binding_id": str(binding_id),
                    "resource_id": resource_id,
                    "requested": requested_version,
                    "actual": actual_version,
                }
            )
            continue

        override = binding.get("override", {})
        if mode == "OVERRIDDEN":
            if not isinstance(override, Mapping) or not override:
                blockers.append({"reason": "OVERRIDE_PAYLOAD_REQUIRED", "binding_id": str(binding_id)})
                continue
            if locked and not binding.get("authority_record_id"):
                blockers.append(
                    {"reason": "LOCKED_RESOURCE_OVERRIDE_REQUIRES_AUTHORITY", "binding_id": str(binding_id)}
                )
                continue
            payload.update(deepcopy(dict(override)))
            deviations.append(
                {
                    "binding_id": str(binding_id),
                    "kind": "OVERRIDE",
                    "authority_record_id": binding.get("authority_record_id"),
                }
            )

        resolved[str(binding_id)] = {
            "binding_id": str(binding_id),
            "mode": mode,
            "resource_id": resource_id,
            "resource_type": resource.get("type"),
            "version": actual_version,
            "resolved": payload,
            "locked": locked,
        }

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "resolved_bindings": resolved,
        "deviations": deviations,
        "blockers": blockers,
    }


__all__ = ["BINDING_MODES", "EXECUTOR_ID", "EXECUTOR_VERSION", "resolve"]
