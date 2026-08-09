from __future__ import annotations

"""Pure-Python structural validator for procedural plant specifications."""

from math import sqrt
from typing import Any, Mapping

EXECUTOR_ID = "VEGETATION_BOTANICAL_GRAMMAR"
EXECUTOR_VERSION = "0.1.0"
FORM_CLASSES = {"TREE", "SHRUB", "HERBACEOUS", "GRASS", "ROSETTE", "REED", "VINE", "GROUND_COVER", "ALIEN_BRANCHING"}
AGE_CLASSES = {"SEEDLING", "JUVENILE", "MATURE", "OLD"}
SEASONS = {"DORMANT", "SPRING", "SUMMER", "AUTUMN", "EVERGREEN", "ALIEN_CYCLE"}


def _positive(spec: Mapping[str, Any], key: str, blockers: list[dict[str, Any]], *, allow_zero: bool = False) -> float:
    try: value = float(spec.get(key))
    except (TypeError, ValueError): blockers.append({"reason": "NUMERIC_FIELD_REQUIRED", "field": key}); return 0.0
    if value < 0 or (value == 0 and not allow_zero): blockers.append({"reason": "POSITIVE_VALUE_REQUIRED", "field": key, "value": value})
    return value


def evaluate(spec: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []; warnings: list[dict[str, Any]] = []
    form = str(spec.get("form_class", "")).upper()
    if form not in FORM_CLASSES: blockers.append({"reason": "INVALID_FORM_CLASS", "value": form})
    height = _positive(spec, "height_m", blockers)
    crown_radius = _positive(spec, "crown_radius_m", blockers, allow_zero=form in {"GRASS", "REED", "VINE"})
    stem_radius = _positive(spec, "stem_radius_m", blockers)
    seed = spec.get("seed")
    if not isinstance(seed, int): blockers.append({"reason": "INTEGER_SEED_REQUIRED"})
    orders = int(spec.get("branching_orders", 0) or 0)
    if not 0 <= orders <= 8: blockers.append({"reason": "BRANCHING_ORDERS_OUT_OF_RANGE", "value": orders})
    angle = float(spec.get("phyllotaxis_deg", 137.5))
    if not 0.0 <= angle < 360.0: blockers.append({"reason": "PHYLLOTAXIS_OUT_OF_RANGE", "value": angle})
    internode = float(spec.get("internode_length_m", 0.0) or 0.0)
    if form not in {"ROSETTE", "GROUND_COVER"} and internode <= 0: blockers.append({"reason": "INTERNODE_LENGTH_REQUIRED", "value": internode})
    apical = float(spec.get("apical_dominance", 0.5)); crown_density = float(spec.get("crown_density", 0.5))
    for key, value in (("apical_dominance", apical), ("crown_density", crown_density)):
        if not 0.0 <= value <= 1.0: blockers.append({"reason": "NORMALIZED_FIELD_OUT_OF_RANGE", "field": key, "value": value})
    tropism = spec.get("tropism", [0.0, 0.0, 1.0])
    if not isinstance(tropism, (list, tuple)) or len(tropism) != 3: blockers.append({"reason": "TROPISM_VECTOR_REQUIRED"}); tropism_norm = 0.0
    else:
        tropism_norm = sqrt(sum(float(x) ** 2 for x in tropism))
        if tropism_norm == 0: warnings.append({"reason": "ZERO_TROPISM_VECTOR"})
    age = str(spec.get("age_class", "MATURE")).upper()
    if age not in AGE_CLASSES: blockers.append({"reason": "INVALID_AGE_CLASS", "value": age})
    season = str(spec.get("season", "EVERGREEN")).upper()
    if season not in SEASONS: blockers.append({"reason": "INVALID_SEASON", "value": season})
    if crown_radius > height * 1.5 and form not in {"GROUND_COVER", "VINE"}: warnings.append({"reason": "EXTREME_CROWN_TO_HEIGHT_RATIO", "ratio": crown_radius / max(height, 1e-9)})
    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID, "form_class": form, "seed": seed, "derived": {"height_m": height, "crown_diameter_m": crown_radius * 2.0, "stem_diameter_m": stem_radius * 2.0, "tropism_norm": tropism_norm}, "blockers": blockers, "warnings": warnings}
