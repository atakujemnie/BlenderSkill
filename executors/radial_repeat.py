from __future__ import annotations

"""Pure-Python radial repetition helpers for circular civic/hard-surface parts.

Useful for anchors, fasteners, vents and repeated radial details. Geometry
creation remains the caller's responsibility; this module provides stable
positions/orientations and containment validation.
"""

import math
from typing import Iterable


def radial_instances(
    *,
    count: int,
    radius: float,
    z: float = 0.0,
    phase_degrees: float = 0.0,
    face_outward: bool = True,
) -> list[dict]:
    if count < 1:
        raise ValueError("count must be >= 1")
    if radius < 0.0:
        raise ValueError("radius must be >= 0")

    phase = math.radians(phase_degrees)
    out = []
    for i in range(count):
        a = phase + 2.0 * math.pi * i / count
        out.append(
            {
                "index": i,
                "angle_radians": a,
                "position": (radius * math.cos(a), radius * math.sin(a), z),
                "rotation_z": a if face_outward else 0.0,
            }
        )
    return out


def validate_annulus_containment(
    *,
    center_radius: float,
    feature_outer_radius: float,
    annulus_inner_radius: float,
    annulus_outer_radius: float,
    margin: float = 0.0,
) -> dict:
    if feature_outer_radius < 0.0:
        raise ValueError("feature_outer_radius must be >= 0")
    if annulus_inner_radius < 0.0 or annulus_outer_radius < annulus_inner_radius:
        raise ValueError("invalid annulus radii")

    feature_min = center_radius - feature_outer_radius
    feature_max = center_radius + feature_outer_radius
    allowed_min = annulus_inner_radius + margin
    allowed_max = annulus_outer_radius - margin

    reasons = []
    if feature_min < allowed_min:
        reasons.append("FEATURE_CROSSES_INNER_ANNULUS_BOUNDARY")
    if feature_max > allowed_max:
        reasons.append("FEATURE_CROSSES_OUTER_ANNULUS_BOUNDARY")

    return {
        "status": "FAIL" if reasons else "PASS",
        "feature_radius_span": [feature_min, feature_max],
        "allowed_radius_span": [allowed_min, allowed_max],
        "reasons": reasons,
    }


def estimate_radial_detail_triangles(*, count: int, tris_per_instance: int) -> int:
    if count < 0 or tris_per_instance < 0:
        raise ValueError("counts must be non-negative")
    return count * tris_per_instance
