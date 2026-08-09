from __future__ import annotations

"""Provider compatibility/capability gate for procedural generators.

Pure Python by design. Blender-specific adapters may discover operators/modules and
feed a compact probe artifact to this executor.
"""

from typing import Any, Mapping

EXECUTOR_ID = "PROCEDURAL_GENERATOR_PROVIDER"
EXECUTOR_VERSION = "0.1.0"

EXECUTION_TYPES = {"DIRECT_PYTHON", "BPY_OPERATOR", "GEOMETRY_NODES", "EXTERNAL_PROCESS", "SOURCE_ONLY"}
PROBE_STATES = {"PASS", "FAIL", "UNAVAILABLE", "UNTESTED"}


def _version(value: Any) -> tuple[int, ...]:
    if isinstance(value, (tuple, list)):
        return tuple(int(x) for x in value)
    text = str(value or "0")
    out = []
    for part in text.split("."):
        digits = "".join(ch for ch in part if ch.isdigit())
        if not digits:
            break
        out.append(int(digits))
    return tuple(out or [0])


def _cmp_pad(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    n = max(len(a), len(b))
    return a + (0,) * (n - len(a)), b + (0,) * (n - len(b))


def _lt(a: tuple[int, ...], b: tuple[int, ...]) -> bool:
    aa, bb = _cmp_pad(a, b)
    return aa < bb


def _gt(a: tuple[int, ...], b: tuple[int, ...]) -> bool:
    aa, bb = _cmp_pad(a, b)
    return aa > bb


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

    license_id = str(provider.get("license", "")).strip()
    if require_known_license and not license_id:
        blockers.append({"reason": "LICENSE_REQUIRED"})

    runtime_blender = _version(runtime.get("blender_version"))
    min_blender = _version(provider.get("blender_min", "0"))
    max_value = provider.get("blender_max")
    max_blender = _version(max_value) if max_value else None
    if _lt(runtime_blender, min_blender):
        blockers.append({"reason": "BLENDER_VERSION_TOO_OLD", "runtime": runtime_blender, "minimum": min_blender})
    if max_blender and _gt(runtime_blender, max_blender):
        blockers.append({"reason": "BLENDER_VERSION_TOO_NEW", "runtime": runtime_blender, "maximum": max_blender})

    if execution_type == "SOURCE_ONLY":
        return {
            "status": "SOURCE_ONLY" if not blockers else "BLOCKED",
            "provider_id": provider_id,
            "can_execute": False,
            "blockers": blockers,
            "warnings": warnings,
        }

    if require_determinism and not bool(provider.get("supports_seed", False)):
        blockers.append({"reason": "DETERMINISTIC_SEED_REQUIRED"})

    if bool(provider.get("requires_ui_context", False)) and bool(runtime.get("background", False)):
        blockers.append({"reason": "UI_CONTEXT_REQUIRED_IN_BACKGROUND"})

    probe = dict(provider.get("probe") or {})
    probe_state = str(probe.get("status", "UNTESTED")).upper()
    if probe_state not in PROBE_STATES:
        blockers.append({"reason": "INVALID_PROBE_STATE", "value": probe_state})
    if bool(provider.get("probe_required", True)):
        if probe_state == "UNTESTED":
            blockers.append({"reason": "CAPABILITY_PROBE_REQUIRED"})
        elif probe_state != "PASS":
            blockers.append({"reason": "CAPABILITY_PROBE_FAILED", "probe_status": probe_state})

    if probe_state == "PASS":
        required_caps = set(str(x) for x in provider.get("required_capabilities", []) or [])
        found_caps = set(str(x) for x in probe.get("capabilities", []) or [])
        missing = sorted(required_caps - found_caps)
        if missing:
            blockers.append({"reason": "REQUIRED_CAPABILITY_MISSING", "capabilities": missing})

    status = "PASS" if not blockers else "BLOCKED"
    return {
        "status": status,
        "provider_id": provider_id,
        "provider_version": provider.get("provider_version"),
        "execution_type": execution_type,
        "can_execute": status == "PASS",
        "blockers": blockers,
        "warnings": warnings,
    }
