from __future__ import annotations

"""Provider compatibility/capability gate using the v0.18 canonical protocol."""

from typing import Any, Mapping

from executors.provider_contracts import PROBE_STATES
from executors.version_constraints import satisfies

EXECUTOR_ID = "PROCEDURAL_GENERATOR_PROVIDER"
EXECUTOR_VERSION = "0.18.0"

EXECUTION_TYPES = {"DIRECT_PYTHON", "PYTHON_API", "ADDON_API", "BPY_OPERATOR", "GEOMETRY_NODES", "NODE_TREE", "BUILTIN_API", "EXTERNAL_API", "EXTERNAL_PROCESS", "ASSET_PROVIDER", "INTEGRATION", "UTILITY", "SOURCE_ONLY"}


def evaluate(provider: Mapping[str, Any], runtime: Mapping[str, Any], *, require_determinism: bool = True,
             require_known_license: bool = True) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    provider_id = str(provider.get("provider_id", "")).strip()
    execution_type = str(provider.get("execution_type", "")).upper()
    if not provider_id:
        blockers.append({"reason": "PROVIDER_ID_REQUIRED"})
    if execution_type not in EXECUTION_TYPES:
        blockers.append({"reason": "INVALID_EXECUTION_TYPE", "value": execution_type})

    license_id = str(provider.get("license_policy") or provider.get("license") or "").strip()
    if require_known_license and not license_id:
        blockers.append({"reason": "LICENSE_REQUIRED"})

    runtime_blender = str(runtime.get("blender_version") or "UNKNOWN")
    min_blender = str(provider.get("blender_min") or "").strip()
    max_blender = str(provider.get("blender_max") or "").strip()
    if min_blender and not satisfies(runtime_blender, f">={min_blender}"):
        blockers.append({"reason": "BLENDER_VERSION_TOO_OLD", "runtime": runtime_blender, "minimum": min_blender})
    if max_blender and not satisfies(runtime_blender, f"<={max_blender}"):
        blockers.append({"reason": "BLENDER_VERSION_TOO_NEW", "runtime": runtime_blender, "maximum": max_blender})

    if execution_type == "SOURCE_ONLY":
        return {"status": "SOURCE_ONLY" if not blockers else "BLOCKED", "validator_id": EXECUTOR_ID, "provider_id": provider_id, "can_execute": False, "blockers": blockers, "warnings": warnings}

    if require_determinism and not bool(provider.get("supports_seed", False)):
        warnings.append({"reason": "DETERMINISTIC_SEED_NOT_SUPPORTED"})

    if bool(provider.get("requires_ui_context", False)) and bool(runtime.get("background", False)):
        blockers.append({"reason": "UI_CONTEXT_REQUIRED_IN_BACKGROUND"})

    probe = dict(provider.get("probe") or {})
    probe_state = str(provider.get("probe_state") or provider.get("runtime_probe_status") or probe.get("probe_state") or probe.get("status") or "PROBE_REQUIRED").upper()
    if probe_state not in PROBE_STATES:
        blockers.append({"reason": "INVALID_PROBE_STATE", "value": probe_state})
    elif bool(provider.get("probe_required", True)):
        if probe_state == "PROBE_REQUIRED":
            blockers.append({"reason": "CAPABILITY_PROBE_REQUIRED"})
        elif probe_state != "PASS":
            blockers.append({"reason": "CAPABILITY_PROBE_FAILED", "probe_status": probe_state})

    if probe_state == "PASS":
        required_caps = {str(x) for x in provider.get("required_capabilities", []) or []}
        found_caps = {str(x) for x in probe.get("capabilities", []) or []}
        missing = sorted(required_caps - found_caps)
        if missing:
            blockers.append({"reason": "REQUIRED_CAPABILITY_MISSING", "capabilities": missing})

    status = "PASS" if not blockers else "BLOCKED"
    return {"status": status, "validator_id": EXECUTOR_ID, "provider_id": provider_id, "provider_version": provider.get("provider_version") or provider.get("version"), "execution_type": execution_type, "probe_state": probe_state, "can_execute": status == "PASS", "blockers": blockers, "warnings": warnings}
