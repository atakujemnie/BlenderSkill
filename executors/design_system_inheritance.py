from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable, Mapping

EXECUTOR_ID = "DESIGN_SYSTEM_INHERITANCE_RESOLVE"
EXECUTOR_VERSION = "0.16.0"
SCOPE_ORDER = {"UNIVERSE": 0, "LOCATION": 1, "ORGANIZATION": 2, "FAMILY": 3, "ASSET": 4}


def _flatten_paths(value: Any, prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    if isinstance(value, Mapping):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(item, Mapping):
                out.update(_flatten_paths(item, path))
            else:
                out[path] = item
    else:
        out[prefix] = value
    return out


def _deep_merge(base: dict[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    out = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, Mapping) and isinstance(out.get(key), Mapping):
            out[key] = _deep_merge(dict(out[key]), value)
        else:
            out[key] = deepcopy(value)
    return out


def resolve(layers: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    layer_list = list(layers)
    if not layer_list:
        return {"validator_id": EXECUTOR_ID, "status": "FAIL", "blockers": [{"reason": "NO_LAYERS"}]}

    resolved: dict[str, Any] = {}
    provenance: dict[str, str] = {}
    locked: dict[str, str] = {}
    previous_scope = -1

    for index, layer in enumerate(layer_list):
        layer_id = str(layer.get("id") or f"layer_{index}")
        scope = str(layer.get("scope") or "").upper()
        if scope not in SCOPE_ORDER:
            blockers.append({"reason": "INVALID_SCOPE", "layer_id": layer_id, "scope": scope})
            continue
        order = SCOPE_ORDER[scope]
        if order < previous_scope:
            blockers.append({"reason": "SCOPE_ORDER_REGRESSION", "layer_id": layer_id, "scope": scope})
        previous_scope = max(previous_scope, order)

        payload = layer.get("values")
        if not isinstance(payload, Mapping):
            blockers.append({"reason": "LAYER_VALUES_INVALID", "layer_id": layer_id})
            continue

        flat = _flatten_paths(payload)
        current_flat = _flatten_paths(resolved)
        for path, value in flat.items():
            if path in locked and path in current_flat and current_flat[path] != value:
                blockers.append({
                    "reason": "LOCKED_TOKEN_OVERRIDE",
                    "path": path,
                    "locked_by": locked[path],
                    "attempted_by": layer_id,
                })

        if not any(b.get("attempted_by") == layer_id for b in blockers):
            resolved = _deep_merge(resolved, payload)
            for path in flat:
                provenance[path] = layer_id

        for path in layer.get("locked_paths", []) or []:
            locked[str(path)] = layer_id

    return {
        "validator_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "status": "PASS" if not blockers else "FAIL",
        "resolved": resolved,
        "provenance": provenance,
        "locked_paths": locked,
        "layers": [str(layer.get("id") or f"layer_{i}") for i, layer in enumerate(layer_list)],
        "blockers": blockers,
    }
