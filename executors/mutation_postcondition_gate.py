from __future__ import annotations

"""Canonical postcondition gate for one authorized geometry mutation.

The executor evaluates compact before/after metrics captured by an asset-local
Blender adapter. It intentionally does not execute bpy itself so the acceptance
logic is deterministic and testable outside Blender.
"""

from typing import Any, Mapping

EXECUTOR_ID = "MUTATION_POSTCONDITION_GATE"
EXECUTOR_VERSION = "0.1.0"

BOOLEAN_KINDS = {"BOOLEAN_CUT", "BOOLEAN_DIFFERENCE", "BOOLEAN_UNION", "BOOLEAN_INTERSECT"}


def _num(mapping: Mapping[str, Any], key: str) -> float | None:
    value = mapping.get(key)
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _delta(before: Mapping[str, Any], after: Mapping[str, Any], key: str) -> float | None:
    a = _num(before, key)
    b = _num(after, key)
    if a is None or b is None:
        return None
    return b - a


def _status_ok(value: Any) -> bool:
    if isinstance(value, Mapping):
        return str(value.get("status", "")).upper() == "PASS"
    return str(value).upper() == "PASS"


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    operation_id = str(report.get("operation_id", "UNKNOWN"))
    kind = str(report.get("operation_kind", "GENERIC_MUTATION")).upper()
    before = dict(report.get("before", {}))
    after = dict(report.get("after", {}))
    exp = dict(report.get("expectations", {}))
    blockers: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []

    def check(name: str, ok: bool, **detail: Any) -> None:
        rec = {"check": name, "status": "PASS" if ok else "FAIL", **detail}
        checks.append(rec)
        if not ok:
            blockers.append({"reason": name, **detail})

    if not operation_id or operation_id == "UNKNOWN":
        check("OPERATION_ID_REQUIRED", False)

    if exp.get("object_created"):
        check("EXPECTED_OBJECT_CREATION",
              not bool(before.get("object_exists", False)) and bool(after.get("object_exists", False)),
              before_exists=bool(before.get("object_exists", False)),
              after_exists=bool(after.get("object_exists", False)))

    geometry_change_required = bool(exp.get("geometry_change_required", kind in BOOLEAN_KINDS))
    face_delta = _delta(before, after, "faces")
    vert_delta = _delta(before, after, "vertices")
    volume_delta = _delta(before, after, "volume_mm3")
    min_face = float(exp.get("min_abs_face_delta", 0.0))
    min_vert = float(exp.get("min_abs_vertex_delta", 0.0))
    min_vol = float(exp.get("min_abs_volume_delta_mm3", 0.0))

    if geometry_change_required:
        observed = False
        if face_delta is not None and abs(face_delta) > max(min_face, 0.0): observed = True
        if vert_delta is not None and abs(vert_delta) > max(min_vert, 0.0): observed = True
        if volume_delta is not None and abs(volume_delta) > max(min_vol, 0.0): observed = True
        before_sig = before.get("geometry_signature")
        after_sig = after.get("geometry_signature")
        if before_sig is not None and after_sig is not None and before_sig != after_sig: observed = True
        check("GEOMETRY_CHANGE_REQUIRED", observed, face_delta=face_delta,
              vertex_delta=vert_delta, volume_delta_mm3=volume_delta)

    if min_vol > 0.0:
        check("MIN_VOLUME_DELTA", volume_delta is not None and abs(volume_delta) >= min_vol,
              actual=None if volume_delta is None else abs(volume_delta), expected_min=min_vol)

    direction = str(exp.get("volume_direction", "ANY")).upper()
    if direction == "DECREASE":
        check("VOLUME_MUST_DECREASE", volume_delta is not None and volume_delta < 0.0, actual=volume_delta)
    elif direction == "INCREASE":
        check("VOLUME_MUST_INCREASE", volume_delta is not None and volume_delta > 0.0, actual=volume_delta)

    if exp.get("require_identity_transform") or kind == "TRANSFORM_APPLY":
        check("IDENTITY_TRANSFORM_REQUIRED", bool(after.get("matrix_identity", False)))
    if exp.get("require_depsgraph_update") or kind == "TRANSFORM_APPLY":
        check("DEPSGRAPH_UPDATE_REQUIRED", bool(after.get("depsgraph_updated", False)))
    if exp.get("require_positive_signed_volume"):
        signed = _num(after, "signed_volume_mm3")
        check("POSITIVE_SIGNED_VOLUME_REQUIRED", signed is not None and signed > 0.0, actual=signed)

    expected_modifier_absent = list(exp.get("modifier_absent", []))
    if expected_modifier_absent:
        remaining = set(str(x) for x in after.get("modifiers", []))
        for name in expected_modifier_absent:
            check("MODIFIER_MUST_BE_APPLIED", str(name) not in remaining, modifier=str(name))

    expected_cutter_absent = list(exp.get("cutter_absent", []))
    if expected_cutter_absent:
        remaining = set(str(x) for x in after.get("scene_objects", []))
        for name in expected_cutter_absent:
            check("CUTTER_MUST_BE_REMOVED", str(name) not in remaining, cutter=str(name))

    probe = exp.get("feature_probe")
    if probe is not None:
        check("FEATURE_PROBE_REQUIRED", _status_ok(probe),
              probe_status=(probe.get("status") if isinstance(probe, Mapping) else probe))

    if kind in BOOLEAN_KINDS:
        changed = any(c["check"] == "GEOMETRY_CHANGE_REQUIRED" and c["status"] == "PASS" for c in checks)
        check("BOOLEAN_NOT_A_NOOP", changed)

    if kind == "MATERIAL_ONLY":
        before_sig = before.get("geometry_signature")
        after_sig = after.get("geometry_signature")
        if before_sig is not None and after_sig is not None:
            check("MATERIAL_ONLY_GEOMETRY_STABLE", before_sig == after_sig)
        check("MATERIAL_RESPONSE_CHANGED", before.get("material_signature") != after.get("material_signature"))

    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID,
            "evidence_kind": "MUTATION_POSTCONDITION",
            "provenance_id": report.get("provenance_id") or f"mutation_postcondition:{operation_id}",
            "operation_id": operation_id, "operation_kind": kind,
            "checks": checks, "blockers": blockers}


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "evaluate"]
