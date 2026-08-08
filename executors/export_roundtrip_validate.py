from __future__ import annotations

"""Blender-side invariant checks for already exported and re-imported meshes.

Candidate executor. The caller owns the scratch import and supplies expected
asset invariants; this module only measures/compares objects.
"""

from mathutils import Vector


def world_bounds(obj) -> tuple[Vector, Vector]:
    if obj.type != "MESH":
        raise TypeError(f"{obj.name} is not a mesh")
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    mins = Vector((min(v[i] for v in corners) for i in range(3)))
    maxs = Vector((max(v[i] for v in corners) for i in range(3)))
    return mins, maxs


def dimensions_mm(obj) -> list[float]:
    lo, hi = world_bounds(obj)
    return [float((hi[i] - lo[i]) * 1000.0) for i in range(3)]


def validate_object_invariants(
    obj,
    *,
    expected_dimensions_mm=None,
    dimension_tolerance_mm: float = 2.0,
    ground_axis: int | None = 2,
    expected_ground_mm: float = 0.0,
    ground_tolerance_mm: float = 2.0,
) -> dict:
    lo, hi = world_bounds(obj)
    dims = [float((hi[i] - lo[i]) * 1000.0) for i in range(3)]
    reasons = []
    dimension_errors = None

    if expected_dimensions_mm is not None:
        expected = [float(x) for x in expected_dimensions_mm]
        if len(expected) != 3:
            raise ValueError("expected_dimensions_mm must contain 3 values")
        dimension_errors = [round(dims[i] - expected[i], 6) for i in range(3)]
        if any(abs(e) > dimension_tolerance_mm for e in dimension_errors):
            reasons.append("HARD_DIMENSION_MISMATCH")

    ground_actual = None
    if ground_axis is not None:
        axis = int(ground_axis)
        if axis not in (0, 1, 2):
            raise ValueError("ground_axis must be 0, 1, 2 or None")
        ground_actual = float(lo[axis] * 1000.0)
        if abs(ground_actual - float(expected_ground_mm)) > ground_tolerance_mm:
            reasons.append("GROUND_DATUM_MISMATCH")

    return {
        "status": "FAIL" if reasons else "PASS",
        "object": obj.name,
        "dimensions_mm": [round(x, 6) for x in dims],
        "dimension_error_mm": dimension_errors,
        "ground_actual_mm": round(ground_actual, 6) if ground_actual is not None else None,
        "reasons": reasons,
    }


def validate_lod_family(
    objects,
    *,
    expected_dimensions_mm=None,
    dimension_tolerance_mm: float = 2.0,
    ground_axis: int | None = 2,
    expected_ground_mm: float = 0.0,
    ground_tolerance_mm: float = 2.0,
) -> dict:
    reports = [
        validate_object_invariants(
            obj,
            expected_dimensions_mm=expected_dimensions_mm,
            dimension_tolerance_mm=dimension_tolerance_mm,
            ground_axis=ground_axis,
            expected_ground_mm=expected_ground_mm,
            ground_tolerance_mm=ground_tolerance_mm,
        )
        for obj in objects
    ]
    return {
        "status": "FAIL" if any(r["status"] == "FAIL" for r in reports) else "PASS",
        "objects": reports,
        "count": len(reports),
    }
