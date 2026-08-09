from __future__ import annotations

from typing import Any

REQUIRED_KEYS = {
    "location_id",
    "unit_scale",
    "architectural_grid_mm",
    "material_families",
    "edge_families",
    "lighting_families",
    "branding",
}


def evaluate_location_design_system(spec: dict[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    missing = sorted(k for k in REQUIRED_KEYS if not spec.get(k))
    if missing:
        blockers.append({"code": "MISSING_REQUIRED_KEYS", "keys": missing})
    if spec.get("unit_scale") not in (0.001, "0.001", "1mm"):
        blockers.append({"code": "UNIT_SCALE_NOT_MM", "value": spec.get("unit_scale")})
    grid = spec.get("architectural_grid_mm")
    if not isinstance(grid, (int, float)) or grid <= 0:
        blockers.append({"code": "INVALID_ARCHITECTURAL_GRID", "value": grid})
    if not isinstance(spec.get("material_families"), dict) or not spec.get("material_families"):
        blockers.append({"code": "MATERIAL_LANGUAGE_EMPTY"})
    if not isinstance(spec.get("lighting_families"), dict) or not spec.get("lighting_families"):
        blockers.append({"code": "LIGHTING_LANGUAGE_EMPTY"})
    return {
        "validator_id": "LOCATION_DESIGN_SYSTEM_GATE",
        "status": "PASS" if not blockers else "FAIL",
        "blockers": blockers,
    }
