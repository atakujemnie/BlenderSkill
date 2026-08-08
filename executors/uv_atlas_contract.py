from __future__ import annotations

"""Reusable helpers for semantic UV atlas ownership across bake source and LODs."""

import re
from typing import Mapping, Sequence

_SUFFIX = re.compile(r"\.\d{3}$")


def set_part_id(obj, part_id: str, *, property_name: str = "_bs_part_id") -> str:
    if not part_id:
        raise ValueError("part_id must be non-empty")
    obj[property_name] = str(part_id)
    return str(part_id)


def get_part_id(
    obj,
    *,
    property_name: str = "_bs_part_id",
    allow_name_fallback: bool = False,
) -> str:
    value = obj.get(property_name)
    if value:
        return str(value)
    if allow_name_fallback:
        return _SUFFIX.sub("", obj.name)
    raise KeyError(f"missing semantic part id on {obj.name}")


def validate_rects(rects: Mapping[str, Sequence[float]], *, allow_overlap=()) -> dict:
    allowed = {frozenset(pair) for pair in allow_overlap}
    normalized = {}
    reasons = []

    for part_id, rect in rects.items():
        if len(rect) != 4:
            reasons.append(f"INVALID_RECT:{part_id}")
            continue
        u0, v0, u1, v1 = map(float, rect)
        if not (0.0 <= u0 < u1 <= 1.0 and 0.0 <= v0 < v1 <= 1.0):
            reasons.append(f"RECT_OUT_OF_BOUNDS:{part_id}")
            continue
        normalized[str(part_id)] = (u0, v0, u1, v1)

    ids = list(normalized)
    overlaps = []
    for i, a in enumerate(ids):
        au0, av0, au1, av1 = normalized[a]
        for b in ids[i + 1 :]:
            bu0, bv0, bu1, bv1 = normalized[b]
            intersects = max(au0, bu0) < min(au1, bu1) and max(av0, bv0) < min(av1, bv1)
            if intersects and frozenset((a, b)) not in allowed:
                overlaps.append((a, b))
                reasons.append(f"UNDECLARED_RECT_OVERLAP:{a}:{b}")

    return {
        "status": "FAIL" if reasons else "PASS",
        "rect_count": len(normalized),
        "overlaps": overlaps,
        "reasons": reasons,
    }


def remap_existing_uv_to_rect(
    obj,
    rect,
    *,
    gutter: float = 0.0,
    uv_layer_name: str | None = None,
) -> dict:
    """Normalize existing UV bounds into a declared rectangle.

    This is a compatibility helper, not a substitute for semantic parametric UV
    generation. Use only when min/max remapping is valid for the part class.
    """
    if obj.type != "MESH":
        raise TypeError(f"{obj.name} is not MESH")
    layer = (
        obj.data.uv_layers.get(uv_layer_name)
        if uv_layer_name
        else obj.data.uv_layers.active
    )
    if layer is None:
        raise RuntimeError(f"NO_UV_LAYER:{obj.name}")

    u0, v0, u1, v1 = map(float, rect)
    u0 += gutter
    v0 += gutter
    u1 -= gutter
    v1 -= gutter
    if not (0.0 <= u0 < u1 <= 1.0 and 0.0 <= v0 < v1 <= 1.0):
        raise ValueError("gutter collapses or invalidates atlas rectangle")

    data = layer.data
    if not data:
        raise RuntimeError(f"EMPTY_UV_LAYER:{obj.name}")
    us = [float(loop.uv.x) for loop in data]
    vs = [float(loop.uv.y) for loop in data]
    src_u0, src_u1 = min(us), max(us)
    src_v0, src_v1 = min(vs), max(vs)
    du = src_u1 - src_u0
    dv = src_v1 - src_v0
    if du <= 1e-12 or dv <= 1e-12:
        raise RuntimeError(f"DEGENERATE_UV_BOUNDS:{obj.name}")

    for loop in data:
        loop.uv.x = u0 + (float(loop.uv.x) - src_u0) / du * (u1 - u0)
        loop.uv.y = v0 + (float(loop.uv.y) - src_v0) / dv * (v1 - v0)

    return {
        "status": "PASS",
        "object": obj.name,
        "rect": [u0, v0, u1, v1],
        "loops": len(data),
    }


def apply_contract(
    objects,
    rects: Mapping[str, Sequence[float]],
    *,
    property_name: str = "_bs_part_id",
    gutter: float = 0.0,
    allow_name_fallback: bool = False,
) -> dict:
    validation = validate_rects(rects)
    if validation["status"] != "PASS":
        return validation

    reports = []
    missing = []
    fallbacks = []

    for obj in objects:
        try:
            part_id = get_part_id(
                obj,
                property_name=property_name,
                allow_name_fallback=allow_name_fallback,
            )
        except KeyError:
            missing.append(obj.name)
            continue
        if part_id not in rects:
            missing.append(part_id)
            continue
        if obj.get(property_name) is None:
            fallbacks.append({"object": obj.name, "part_id": part_id})
        reports.append(remap_existing_uv_to_rect(obj, rects[part_id], gutter=gutter))

    return {
        "status": "FAIL" if missing else "PASS",
        "objects": len(reports),
        "missing": missing,
        "name_fallbacks": fallbacks,
        "reports": reports,
    }
