from __future__ import annotations

"""Prevent a structural pass from being reported as a finished asset.

v0.21 allowed all component BUILD tasks to be APPROVED while the asset remained
at STRUCTURAL_GEOMETRY. v0.22 requires reference-feature inventory before serious
geometry, proves each later completion level, and requires a current independent
visual review for final approval.
"""

from typing import Any, Mapping

from executors.asset_state_runtime import ASSET_STAGES

EXECUTOR_ID = "ASSET_STAGE_COMPLETION_GATE"
EXECUTOR_VERSION = "0.22.0"

ACCEPTANCE_LEVELS = {
    "NONE": 0,
    "BLOCKOUT": 1,
    "STRUCTURAL": 2,
    "DETAILS": 3,
    "MATERIALS": 4,
    "GAME_READY": 5,
    "FIDELITY": 6,
    "FINAL": 7,
}
# The requirement applies when *leaving* a production stage. Entering
# STRUCTURAL_GEOMETRY must remain possible before structural tasks exist.
TARGET_REQUIREMENTS = {
    "DETAILS": "STRUCTURAL",
    "MATERIALS": "DETAILS",
    "GAME_READY": "MATERIALS",
    "FIDELITY_AUDIT": "GAME_READY",
    "APPROVED": "FIDELITY",
}


def acceptance_level_for_stage(stage: str) -> str:
    value = str(stage or "").upper()
    return {
        "BRIEF": "NONE",
        "REFERENCE_ANALYSIS": "NONE",
        "RECONSTRUCTION_MANIFEST": "NONE",
        "BLOCKOUT": "BLOCKOUT",
        "STRUCTURAL_GEOMETRY": "STRUCTURAL",
        "DETAILS": "DETAILS",
        "MATERIALS": "MATERIALS",
        "GAME_READY": "GAME_READY",
        "FIDELITY_AUDIT": "FIDELITY",
        "APPROVED": "FINAL",
    }.get(value, "NONE")


def _production_components(asset: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    components = {
        str(component_id): dict(component)
        for component_id, component in dict(asset.get("components", {}) or {}).items()
        if isinstance(component, Mapping)
    }
    out: dict[str, dict[str, Any]] = {}
    for component_id, component in components.items():
        shape_class = str(component.get("shape_class") or "").upper()
        children = [child_id for child_id, child in components.items() if str(child.get("parent") or "") == component_id]
        if shape_class == "ASSEMBLY" and children:
            continue
        out[component_id] = component
    return out


def _effective_level(component: Mapping[str, Any]) -> str:
    level = str(component.get("acceptance_level") or "").upper()
    if level in ACCEPTANCE_LEVELS:
        return level
    # v0.21 compatibility: ACCEPTED without a level represented a structural
    # geometry acceptance and must not be promoted beyond that implicitly.
    if str(component.get("state") or "").upper() == "ACCEPTED":
        return "STRUCTURAL"
    return "NONE"


def validate(
    asset: Mapping[str, Any],
    target_stage: str,
    *,
    fidelity_review: Mapping[str, Any] | None = None,
    scene_revision: int = 0,
    reference_revision: int = 0,
) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    target = str(target_stage or "").upper()
    current = str(asset.get("stage") or "").upper()
    if current not in ASSET_STAGES or target not in ASSET_STAGES:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "ASSET_STAGE_INVALID", "from": current, "to": target}],
        }
    if ASSET_STAGES.index(target) != ASSET_STAGES.index(current) + 1:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "NON_SEQUENTIAL_STAGE_ADVANCE", "from": current, "to": target}],
        }

    required_level = TARGET_REQUIREMENTS.get(target)
    components = _production_components(asset)
    incomplete: list[dict[str, Any]] = []
    if required_level:
        required_rank = ACCEPTANCE_LEVELS[required_level]
        for component_id, component in components.items():
            state = str(component.get("state") or "DECLARED").upper()
            actual_level = _effective_level(component)
            if state != "ACCEPTED" or ACCEPTANCE_LEVELS.get(actual_level, 0) < required_rank:
                incomplete.append(
                    {
                        "component_id": component_id,
                        "state": state,
                        "acceptance_level": actual_level,
                        "required_level": required_level,
                    }
                )
        if incomplete:
            blockers.append({"reason": "ASSET_STAGE_COMPONENTS_INCOMPLETE", "components": incomplete})

    # Feature inventory must exist before entering structural production, not
    # after details have already been lost.
    if bool(asset.get("enforce_feature_contracts", False)) and target in {
        "STRUCTURAL_GEOMETRY",
        "DETAILS",
        "MATERIALS",
        "GAME_READY",
        "FIDELITY_AUDIT",
        "APPROVED",
    }:
        missing_contract = [
            component_id
            for component_id, component in components.items()
            if not component.get("feature_contract")
        ]
        if missing_contract:
            blockers.append({"reason": "ASSET_FEATURE_CONTRACTS_INCOMPLETE", "component_ids": sorted(missing_contract)})

    if target == "APPROVED":
        review = dict(fidelity_review) if isinstance(fidelity_review, Mapping) else {}
        if str(review.get("status") or "").upper() != "PASS":
            blockers.append({"reason": "CURRENT_VISUAL_FIDELITY_REVIEW_REQUIRED"})
        else:
            if str(review.get("asset_id") or "") != str(asset.get("asset_id") or ""):
                blockers.append({"reason": "FIDELITY_REVIEW_ASSET_MISMATCH"})
            if int(review.get("asset_revision", 0)) != int(asset.get("revision", 0)):
                blockers.append(
                    {
                        "reason": "FIDELITY_REVIEW_ASSET_REVISION_STALE",
                        "expected": int(asset.get("revision", 0)),
                        "actual": int(review.get("asset_revision", 0)),
                    }
                )
            if int(review.get("scene_revision", 0)) != int(scene_revision):
                blockers.append({"reason": "FIDELITY_REVIEW_SCENE_REVISION_STALE"})
            if int(review.get("reference_revision", 0)) != int(reference_revision):
                blockers.append({"reason": "FIDELITY_REVIEW_REFERENCE_REVISION_STALE"})

    return {
        "status": "PASS" if not blockers else "BLOCKED",
        "validator_id": EXECUTOR_ID,
        "validator_version": EXECUTOR_VERSION,
        "asset_id": asset.get("asset_id"),
        "from_stage": current,
        "target_stage": target,
        "required_acceptance_level": required_level,
        "production_component_count": len(components),
        "blockers": blockers,
    }


__all__ = [
    "ACCEPTANCE_LEVELS",
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "TARGET_REQUIREMENTS",
    "acceptance_level_for_stage",
    "validate",
]
