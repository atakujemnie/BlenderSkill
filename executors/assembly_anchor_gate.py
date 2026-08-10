from __future__ import annotations

"""Validate component assembly relations from measured anchor transforms.

This is the deterministic assembly layer above component-local geometry. Blender
adapters measure world-space anchor transforms; this pure-Python gate decides
whether the assembly satisfies the external state contract.
"""

from math import sqrt
from typing import Any, Mapping

EXECUTOR_ID = "ASSEMBLY_ANCHOR_GATE"
EXECUTOR_VERSION = "0.1.1"
RELATION_TYPES = {"COINCIDENT", "OFFSET", "ALIGNED_AXIS", "CLEARANCE"}


def _vec(value: Any, *, size: int = 3) -> tuple[float, ...] | None:
    if not isinstance(value, (list, tuple)) or len(value) != size:
        return None
    try:
        return tuple(float(x) for x in value)
    except (TypeError, ValueError):
        return None


def _distance(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b, strict=True)))


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    measurements = report.get("anchors", {})
    if not isinstance(measurements, Mapping):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "ANCHOR_MEASUREMENTS_MAPPING_REQUIRED"}],
        }

    relation_results: list[dict[str, Any]] = []
    blockers: list[dict[str, Any]] = []
    for raw in list(report.get("relations", []) or []):
        if not isinstance(raw, Mapping):
            blockers.append({"reason": "ASSEMBLY_RELATION_INVALID_RECORD"})
            continue
        relation = dict(raw)
        relation_id = str(relation.get("id") or relation.get("relation_id") or "UNKNOWN")
        rtype = str(relation.get("type") or relation.get("relation_type") or "").upper()
        importance = str(relation.get("importance", "MUST")).upper()
        local_blockers: list[dict[str, Any]] = []
        if rtype not in RELATION_TYPES:
            local_blockers.append({"reason": "ANCHOR_RELATION_TYPE_INVALID", "relation_type": rtype})

        a_id = str(relation.get("a") or "")
        b_id = str(relation.get("b") or "")
        a_raw = measurements.get(a_id)
        b_raw = measurements.get(b_id)
        if not isinstance(a_raw, Mapping) or not isinstance(b_raw, Mapping):
            local_blockers.append({"reason": "ANCHOR_MEASUREMENT_MISSING", "a": a_id, "b": b_id})
            relation_results.append(
                {"relation_id": relation_id, "relation_type": rtype, "status": "FAIL", "blockers": local_blockers}
            )
            if importance == "MUST":
                blockers.extend({"relation_id": relation_id, **item} for item in local_blockers)
            continue

        a_pos = _vec(a_raw.get("position_mm"))
        b_pos = _vec(b_raw.get("position_mm"))
        if a_pos is None or b_pos is None:
            local_blockers.append({"reason": "ANCHOR_POSITION_INVALID"})
        else:
            distance = _distance(a_pos, b_pos)
            if rtype == "COINCIDENT":
                tolerance = float(relation.get("tolerance_mm", 0.5))
                if distance > tolerance:
                    local_blockers.append(
                        {"reason": "COINCIDENT_TOLERANCE_EXCEEDED", "actual_mm": distance, "maximum_mm": tolerance}
                    )
            elif rtype == "OFFSET":
                expected = _vec(relation.get("offset_mm"))
                if expected is None:
                    local_blockers.append({"reason": "OFFSET_VECTOR_REQUIRED"})
                else:
                    actual = tuple(b - a for a, b in zip(a_pos, b_pos, strict=True))
                    error = _distance(actual, expected)
                    tolerance = float(relation.get("tolerance_mm", 0.5))
                    if error > tolerance:
                        local_blockers.append(
                            {"reason": "OFFSET_TOLERANCE_EXCEEDED", "actual_error_mm": error, "maximum_mm": tolerance}
                        )
            elif rtype == "CLEARANCE":
                minimum = float(relation.get("min_clearance_mm", 0.1))
                maximum = relation.get("max_clearance_mm")
                if distance < minimum:
                    local_blockers.append(
                        {"reason": "CLEARANCE_BELOW_MINIMUM", "actual_mm": distance, "minimum_mm": minimum}
                    )
                if maximum is not None and distance > float(maximum):
                    local_blockers.append(
                        {"reason": "CLEARANCE_ABOVE_MAXIMUM", "actual_mm": distance, "maximum_mm": float(maximum)}
                    )

        if rtype == "ALIGNED_AXIS":
            axis = str(relation.get("axis", "Z")).upper()
            a_axis = _vec(a_raw.get("axes", {}).get(axis) if isinstance(a_raw.get("axes"), Mapping) else None)
            b_axis = _vec(b_raw.get("axes", {}).get(axis) if isinstance(b_raw.get("axes"), Mapping) else None)
            if a_axis is None or b_axis is None:
                local_blockers.append({"reason": "ANCHOR_AXIS_MEASUREMENT_REQUIRED", "axis": axis})
            else:
                dot = sum(x * y for x, y in zip(a_axis, b_axis, strict=True))
                tolerance = float(relation.get("min_abs_dot", 0.999))
                if abs(dot) < tolerance:
                    local_blockers.append(
                        {"reason": "AXIS_ALIGNMENT_FAILED", "axis": axis, "actual_abs_dot": abs(dot), "minimum": tolerance}
                    )

        status = "PASS" if not local_blockers else "FAIL"
        relation_results.append(
            {"relation_id": relation_id, "relation_type": rtype, "status": status, "blockers": local_blockers}
        )
        if status == "FAIL" and importance == "MUST":
            blockers.extend({"relation_id": relation_id, **item} for item in local_blockers)

    if not relation_results and not bool(report.get("allow_empty", False)):
        blockers.append({"reason": "ANCHOR_RELATION_CONTRACT_REQUIRED"})

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "provenance_id": report.get("provenance_id") or f"assembly_anchor:{report.get('assembly_revision', 'UNKNOWN')}",
        "assembly_revision": report.get("assembly_revision"),
        "relations": relation_results,
        "blockers": blockers,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "RELATION_TYPES", "evaluate"]
