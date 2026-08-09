from __future__ import annotations

"""Compact visual/composition gate for planted assemblies."""

from typing import Any, Mapping

EXECUTOR_ID = "PLANTING_COMPOSITION_QUALITY"
EXECUTOR_VERSION = "0.14.0"


def evaluate(spec: Mapping[str, Any], metrics: Mapping[str, Any]) -> dict[str, Any]:
    blockers = []
    warnings = []

    soil = float(metrics.get("exposed_soil_ratio", 0.0))
    soil_range = spec.get("exposed_soil_range", [0.0, 1.0])
    if soil < float(soil_range[0]) or soil > float(soil_range[1]):
        blockers.append({"reason": "EXPOSED_SOIL_OUT_OF_RANGE", "actual": soil, "range": soil_range})

    layers_required = set(str(x).upper() for x in spec.get("required_height_layers", []) or [])
    layers_found = set(str(x).upper() for x in metrics.get("height_layers_present", []) or [])
    missing_layers = sorted(layers_required - layers_found)
    if missing_layers:
        blockers.append({"reason": "HEIGHT_LAYER_MISSING", "layers": missing_layers})

    mass_min = int(spec.get("min_major_masses", 1))
    mass_max = int(spec.get("max_major_masses", 999))
    masses = int(metrics.get("major_mass_count", 0))
    if masses < mass_min or masses > mass_max:
        blockers.append({"reason": "MAJOR_MASS_COUNT_OUT_OF_RANGE", "actual": masses, "range": [mass_min, mass_max]})

    periodicity = float(metrics.get("placement_periodicity_score", 0.0))
    max_periodicity = float(spec.get("max_periodicity_score", 0.35))
    if periodicity > max_periodicity:
        blockers.append({"reason": "PLACEMENT_TOO_PERIODIC", "actual": periodicity, "maximum": max_periodicity})

    clone = float(metrics.get("visible_clone_score", 0.0))
    max_clone = float(spec.get("max_visible_clone_score", 0.35))
    if clone > max_clone:
        blockers.append({"reason": "VISIBLE_CLONE_REPETITION", "actual": clone, "maximum": max_clone})

    coverage = float(metrics.get("vegetation_coverage_ratio", 0.0))
    min_coverage = float(spec.get("min_vegetation_coverage_ratio", 0.0))
    if coverage < min_coverage:
        blockers.append({"reason": "VEGETATION_COVERAGE_TOO_LOW", "actual": coverage, "minimum": min_coverage})

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "blockers": blockers,
        "warnings": warnings,
        "metrics": {
            "exposed_soil_ratio": soil,
            "major_mass_count": masses,
            "placement_periodicity_score": periodicity,
            "visible_clone_score": clone,
            "vegetation_coverage_ratio": coverage,
        },
    }
