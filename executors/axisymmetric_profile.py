from __future__ import annotations

"""Candidate reusable executor for AXISYMMETRIC_PROFILE.

Blender runtime dependency: bmesh + mathutils.
The module intentionally contains no bpy.ops calls.
"""

import math
from typing import Iterable, Sequence

import bmesh
from mathutils import Vector


def _validate_profile(profile: Sequence[Sequence[float]]) -> None:
    if len(profile) < 2:
        raise ValueError("profile requires at least two [radius, axis] points")
    for i, p in enumerate(profile):
        if len(p) != 2:
            raise ValueError(f"profile[{i}] must contain [radius, axis_position]")
        if float(p[0]) < 0.0:
            raise ValueError(f"profile[{i}] radius must be >= 0")


def revolve_profile(
    bm: bmesh.types.BMesh,
    profile: Sequence[Sequence[float]],
    *,
    segments: int = 32,
    unit_scale: float = 0.001,
    closed_profile: bool = False,
    cap_bottom: bool = False,
    cap_top: bool = False,
    material_index: int = 0,
    uv_layer=None,
):
    """Revolve a [radius, Z] profile around Z.

    Returns a compact report and leaves geometry in ``bm``.
    ``unit_scale`` converts profile units to Blender units; for millimetres
    use 0.001.
    """
    _validate_profile(profile)
    if segments < 3:
        raise ValueError("segments must be >= 3")
    if closed_profile and (cap_bottom or cap_top):
        raise ValueError("closed_profile cannot be combined with end caps")

    if uv_layer is None:
        uv_layer = bm.loops.layers.uv.verify()

    pts = [(float(r), float(z)) for r, z in profile]
    rings = []
    for r, z in pts:
        if abs(r) < 1e-12:
            rings.append([bm.verts.new((0.0, 0.0, z * unit_scale))])
            continue
        ring = []
        for s in range(segments):
            a = 2.0 * math.pi * s / segments
            ring.append(
                bm.verts.new(
                    (
                        r * math.cos(a) * unit_scale,
                        r * math.sin(a) * unit_scale,
                        z * unit_scale,
                    )
                )
            )
        rings.append(ring)

    arc = [0.0]
    for i in range(1, len(pts)):
        arc.append(arc[-1] + (Vector(pts[i]) - Vector(pts[i - 1])).length)
    profile_length = arc[-1] or 1.0

    def uv(side: float, pidx: int):
        return (side / segments, arc[pidx] / profile_length)

    pair_count = len(rings) if closed_profile else len(rings) - 1
    created_faces = []
    for i in range(pair_count):
        j = (i + 1) % len(rings)
        lo, hi = rings[i], rings[j]
        for s in range(segments):
            t = (s + 1) % segments
            if len(lo) == 1:
                face = bm.faces.new((lo[0], hi[s], hi[t]))
                coords = (uv(s + 0.5, i), uv(s, j), uv(s + 1, j))
            elif len(hi) == 1:
                face = bm.faces.new((lo[s], lo[t], hi[0]))
                coords = (uv(s, i), uv(s + 1, i), uv(s + 0.5, j))
            else:
                face = bm.faces.new((lo[s], lo[t], hi[t], hi[s]))
                coords = (uv(s, i), uv(s + 1, i), uv(s + 1, j), uv(s, j))
            face.material_index = material_index
            for loop, coord in zip(face.loops, coords):
                loop[uv_layer].uv = coord
            created_faces.append(face)

    def cap(ring, reverse: bool):
        if len(ring) <= 1:
            return None
        verts = list(reversed(ring)) if reverse else list(ring)
        face = bm.faces.new(verts)
        face.material_index = material_index
        max_r = max(math.hypot(v.co.x, v.co.y) for v in verts) or 1.0
        for loop in face.loops:
            co = loop.vert.co
            loop[uv_layer].uv = (0.5 + co.x / (2.0 * max_r), 0.5 + co.y / (2.0 * max_r))
        created_faces.append(face)
        return face

    if cap_bottom:
        cap(rings[0], reverse=False)
    if cap_top:
        cap(rings[-1], reverse=True)

    return {
        "status": "PASS",
        "segments": segments,
        "profile_points": len(profile),
        "created_vertices": sum(len(r) for r in rings),
        "created_faces": len(created_faces),
        "radius_min": min(r for r, _ in pts),
        "radius_max": max(r for r, _ in pts),
        "axis_min": min(z for _, z in pts),
        "axis_max": max(z for _, z in pts),
        "closed_profile": bool(closed_profile),
    }


def estimate_side_triangles(profile_points: int, segments: int, *, closed_profile: bool = False) -> int:
    """Fast budget estimate for quad side walls, excluding special pole/cap cases."""
    pairs = profile_points if closed_profile else max(0, profile_points - 1)
    return pairs * segments * 2
