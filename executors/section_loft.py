from __future__ import annotations

"""Deterministic multi-section loft helper for hard-surface reconstruction.

Pure geometry/spec functions work without Blender. Blender scene mutation is an
explicit optional entry point.
"""

from math import cos, pi, sin
from typing import Any, Mapping

EXECUTOR_ID = "SECTION_LOFT_HARD_SURFACE"
EXECUTOR_VERSION = "0.1.0"

SUPPORTED_MODES = {"RECTANGLE", "CHAMFERED_RECTANGLE", "ROUNDED_RECTANGLE", "EXPLICIT"}
SUPPORTED_AXES = {"X", "Y", "Z"}


def _f(value: Any) -> float:
    return float(value)


def _rounded_rect(width: float, depth: float, radius: float, segments: int) -> list[tuple[float, float]]:
    if width <= 0 or depth <= 0:
        raise ValueError("SECTION_SIZE_NONPOSITIVE")
    max_r = min(width, depth) * 0.5
    if not (0 <= radius < max_r + 1e-9):
        raise ValueError("SECTION_RADIUS_INVALID")
    if segments < 1:
        raise ValueError("SECTION_CORNER_SEGMENTS_INVALID")
    hx, hy = width * 0.5, depth * 0.5
    if radius <= 1e-9:
        return [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]
    centers = [
        (hx - radius, -hy + radius, -pi / 2, 0),
        (hx - radius, hy - radius, 0, pi / 2),
        (-hx + radius, hy - radius, pi / 2, pi),
        (-hx + radius, -hy + radius, pi, 3 * pi / 2),
    ]
    pts: list[tuple[float, float]] = []
    for cx, cy, a0, a1 in centers:
        for i in range(segments + 1):
            if pts and i == 0:
                continue
            t = i / segments
            a = a0 + (a1 - a0) * t
            pts.append((cx + radius * cos(a), cy + radius * sin(a)))
    return pts


def _chamfered_rect(width: float, depth: float, chamfer: float) -> list[tuple[float, float]]:
    if width <= 0 or depth <= 0:
        raise ValueError("SECTION_SIZE_NONPOSITIVE")
    hx, hy = width * 0.5, depth * 0.5
    if not (0 <= chamfer < min(hx, hy) + 1e-9):
        raise ValueError("SECTION_CHAMFER_INVALID")
    if chamfer <= 1e-9:
        return [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]
    c = chamfer
    return [
        (-hx + c, -hy), (hx - c, -hy), (hx, -hy + c), (hx, hy - c),
        (hx - c, hy), (-hx + c, hy), (-hx, hy - c), (-hx, -hy + c),
    ]


def section_points(section: Mapping[str, Any]) -> list[tuple[float, float]]:
    mode = str(section.get("profile_mode", "RECTANGLE")).upper()
    if mode not in SUPPORTED_MODES:
        raise ValueError(f"SECTION_MODE_UNSUPPORTED:{mode}")
    if mode == "EXPLICIT":
        pts = [(float(p[0]), float(p[1])) for p in section.get("points_xy", [])]
        if len(pts) < 3:
            raise ValueError("SECTION_EXPLICIT_TOO_FEW_POINTS")
        return pts
    width = _f(section["width"])
    depth = _f(section["depth"])
    if mode == "RECTANGLE":
        return _rounded_rect(width, depth, 0.0, 1)
    if mode == "CHAMFERED_RECTANGLE":
        return _chamfered_rect(width, depth, _f(section.get("chamfer", 0.0)))
    return _rounded_rect(
        width,
        depth,
        _f(section.get("radius", 0.0)),
        int(section.get("segments_per_corner", 2)),
    )


def normalize_spec(spec: Mapping[str, Any]) -> dict[str, Any]:
    axis = str(spec.get("axis", "Z")).upper()
    if axis not in SUPPORTED_AXES:
        raise ValueError(f"LOFT_AXIS_INVALID:{axis}")
    raw_sections = [dict(s) for s in spec.get("sections", [])]
    if len(raw_sections) < 2:
        raise ValueError("LOFT_REQUIRES_AT_LEAST_TWO_SECTIONS")

    sections = []
    previous = None
    sample_count = None
    for index, section in enumerate(raw_sections):
        section_id = str(section.get("id", f"S{index}"))
        pos = float(section.get("axis_pos", section.get("axis_pos_mm", 0.0)))
        if previous is not None and pos <= previous:
            raise ValueError("LOFT_SECTION_ORDER_NOT_MONOTONIC")
        previous = pos
        points = section_points(section)
        if sample_count is None:
            sample_count = len(points)
        elif len(points) != sample_count:
            raise ValueError("LOFT_SECTION_SAMPLE_COUNT_MISMATCH")
        sections.append({"id": section_id, "axis_pos": pos, "points": points, "source": section})

    return {
        "axis": axis,
        "sections": sections,
        "sample_count": int(sample_count or 0),
        "cap_start": bool(spec.get("cap_start", True)),
        "cap_end": bool(spec.get("cap_end", True)),
    }


def _to_xyz(axis: str, u: float, v: float, p: float) -> tuple[float, float, float]:
    if axis == "Z":
        return (u, v, p)
    if axis == "Y":
        return (u, p, v)
    return (p, u, v)


def generate_mesh_data(spec: Mapping[str, Any]) -> dict[str, Any]:
    norm = normalize_spec(spec)
    axis = norm["axis"]
    sections = norm["sections"]
    n = norm["sample_count"]

    vertices: list[tuple[float, float, float]] = []
    for section in sections:
        vertices.extend(_to_xyz(axis, u, v, section["axis_pos"]) for u, v in section["points"])

    faces: list[tuple[int, ...]] = []
    for s in range(len(sections) - 1):
        a0 = s * n
        b0 = (s + 1) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))

    if norm["cap_start"]:
        faces.append(tuple(reversed(range(0, n))))
    if norm["cap_end"]:
        start = (len(sections) - 1) * n
        faces.append(tuple(start + i for i in range(n)))

    return {
        "status": "PASS",
        "axis": axis,
        "section_count": len(sections),
        "sample_count": n,
        "vertex_count": len(vertices),
        "face_count": len(faces),
        "section_ids": [s["id"] for s in sections],
        "section_positions": [s["axis_pos"] for s in sections],
        "vertices": vertices,
        "faces": faces,
    }


def compact_report(spec: Mapping[str, Any]) -> dict[str, Any]:
    data = generate_mesh_data(spec)
    return {k: v for k, v in data.items() if k not in {"vertices", "faces"}}


def create_blender_mesh(spec: Mapping[str, Any], *, object_name: str, collection=None):
    """Create one mesh object in Blender from a validated loft spec."""
    import bpy

    data = generate_mesh_data(spec)
    mesh = bpy.data.meshes.new(f"{object_name}_MESH")
    mesh.from_pydata(data["vertices"], [], data["faces"])
    mesh.update()
    obj = bpy.data.objects.new(object_name, mesh)
    target = collection or bpy.context.collection
    target.objects.link(obj)
    obj["semantic_skill"] = EXECUTOR_ID
    obj["loft_section_count"] = data["section_count"]
    return obj
