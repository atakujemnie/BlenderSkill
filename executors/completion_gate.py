from __future__ import annotations

"""Pure-Python completion gate for Blender asset agents.

The caller supplies compact check statuses. This module does not inspect a
scene; it prevents ambiguous 'DONE' reporting by evaluating explicit levels.
"""

from typing import Mapping, Sequence


PASS = "PASS"
FAIL = "FAIL"
NOT_REQUIRED = "NOT_REQUIRED"
NOT_EVALUATED = "NOT_EVALUATED"
UNVERIFIED = "UNVERIFIED"

LEVELS = (
    "RECONSTRUCTION_COMPLETE",
    "MODELING_COMPLETE",
    "GAME_READY_COMPLETE",
    "PIPELINE_INTEGRATED",
)

DEFAULT_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "RECONSTRUCTION_COMPLETE": (
        "hard_dimensions",
        "canonical_silhouettes",
        "must_features",
        "multi_view_gate",
    ),
    "MODELING_COMPLETE": (
        "mesh_validation",
        "uv_strategy",
        "material_segmentation",
        "pivot_transforms_naming",
        "authoring_source_saved",
    ),
    "GAME_READY_COMPLETE": (
        "lod_validation",
        "collision_validation",
        "bake_or_runtime_material_strategy",
        "export_validation",
        "runtime_emissive_data",
    ),
    "PIPELINE_INTEGRATED": (
        "asset_catalog_registration",
        "runtime_import_or_instantiation",
    ),
}


def _requirement_passes(value: str) -> bool:
    return value in {PASS, NOT_REQUIRED}


def evaluate_completion(
    checks: Mapping[str, str],
    *,
    target_level: str,
    requirements: Mapping[str, Sequence[str]] = DEFAULT_REQUIREMENTS,
) -> dict:
    if target_level not in LEVELS:
        raise ValueError(f"target_level must be one of {LEVELS}")

    level_results: dict[str, str] = {}
    missing_by_level: dict[str, list[dict]] = {}
    highest_passed = None

    target_index = LEVELS.index(target_level)
    previous_pass = True

    for idx, level in enumerate(LEVELS):
        if idx > target_index:
            level_results[level] = NOT_REQUIRED
            continue

        failed = []
        for key in requirements.get(level, ()):
            value = checks.get(key, NOT_EVALUATED)
            if not _requirement_passes(value):
                failed.append({"check": key, "status": value})

        if failed or not previous_pass:
            level_results[level] = FAIL
            missing_by_level[level] = failed
            previous_pass = False
        else:
            level_results[level] = PASS
            highest_passed = level

    target_status = level_results[target_level]
    blockers = []
    for level in LEVELS[: target_index + 1]:
        blockers.extend(missing_by_level.get(level, []))

    return {
        "status": target_status,
        "target_level": target_level,
        "highest_passed_level": highest_passed,
        "levels": level_results,
        "blockers": blockers,
        "can_claim_done": target_status == PASS,
    }
