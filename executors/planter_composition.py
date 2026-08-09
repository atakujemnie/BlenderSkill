from __future__ import annotations

"""Planter/container fit and plant-root anchoring validator."""

import math
from typing import Any, Mapping

EXECUTOR_ID = "PLANTER_VEGETATION_COMPOSITION"; EXECUTOR_VERSION = "0.1.0"


def _inside(container: Mapping[str, Any], x: float, y: float, radius: float, clearance: float) -> bool:
    shape = str(container.get("shape", "RECT")).upper()
    if shape == "CIRCLE":
        usable = float(container.get("inner_radius_m", 0.0)) - clearance - radius
        return usable >= 0 and math.hypot(x, y) <= usable
    if shape == "RECT":
        hx = float(container.get("inner_half_x_m", 0.0)) - clearance - radius; hy = float(container.get("inner_half_y_m", 0.0)) - clearance - radius
        return hx >= 0 and hy >= 0 and abs(x) <= hx and abs(y) <= hy
    return False


def evaluate(spec: Mapping[str, Any]) -> dict[str, Any]:
    container = dict(spec.get("container") or {}); plants = [dict(x) for x in spec.get("plants", []) or []]; blockers: list[dict[str, Any]] = []; warnings: list[dict[str, Any]] = []
    shape = str(container.get("shape", "")).upper()
    if shape not in {"CIRCLE", "RECT"}: blockers.append({"reason": "INVALID_CONTAINER_SHAPE", "value": shape})
    soil_depth = float(container.get("soil_depth_m", 0.0) or 0.0)
    if soil_depth <= 0: blockers.append({"reason": "SOIL_DEPTH_REQUIRED"})
    wall_clearance = max(0.0, float(spec.get("wall_clearance_m", 0.02) or 0.0))
    for plant in plants:
        pid = str(plant.get("id", ""))
        if not pid: blockers.append({"reason": "PLANT_ID_REQUIRED"}); continue
        x, y = float(plant.get("x", 0.0)), float(plant.get("y", 0.0)); root_r = float(plant.get("rootball_radius_m", 0.0) or 0.0); root_d = float(plant.get("rootball_depth_m", 0.0) or 0.0); stem_r = float(plant.get("stem_radius_m", 0.0) or 0.0)
        if root_r <= 0 or root_d <= 0: blockers.append({"reason": "ROOTBALL_DIMENSIONS_REQUIRED", "plant": pid}); continue
        if root_d > soil_depth: blockers.append({"reason": "ROOTBALL_TOO_DEEP", "plant": pid, "rootball_depth_m": root_d, "soil_depth_m": soil_depth})
        if not _inside(container, x, y, root_r, wall_clearance): blockers.append({"reason": "ROOTBALL_OUTSIDE_USABLE_SOIL", "plant": pid})
        if not _inside(container, x, y, stem_r, wall_clearance): blockers.append({"reason": "STEM_WALL_COLLISION", "plant": pid})
    min_stem_spacing = max(0.0, float(spec.get("min_stem_spacing_m", 0.0) or 0.0))
    for i, a in enumerate(plants):
        for b in plants[i + 1:]:
            d = math.hypot(float(a.get("x", 0.0)) - float(b.get("x", 0.0)), float(a.get("y", 0.0)) - float(b.get("y", 0.0)))
            if min_stem_spacing and d < min_stem_spacing: blockers.append({"reason": "STEM_SPACING_VIOLATION", "plants": [a.get("id"), b.get("id")], "distance_m": d})
            if d < float(a.get("rootball_radius_m", 0.0)) + float(b.get("rootball_radius_m", 0.0)): warnings.append({"reason": "ROOTBALL_OVERLAP", "plants": [a.get("id"), b.get("id")], "distance_m": d})
    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID, "plant_count": len(plants), "blockers": blockers, "warnings": warnings}
