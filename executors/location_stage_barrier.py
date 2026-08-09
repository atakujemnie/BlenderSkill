from __future__ import annotations

from typing import Any

STAGES = [
    "REFERENCE",
    "DESIGN_SYSTEM",
    "ARCHITECTURE",
    "HERO_ANCHORS",
    "FIXED_ASSETS",
    "FURNITURE",
    "LIGHTING_VEGETATION_PROPS",
    "FINAL_FIDELITY",
    "RUNTIME",
]


def evaluate_stage_barrier(stage_status: dict[str, Any], target_stage: str) -> dict[str, Any]:
    if target_stage not in STAGES:
        return {"validator_id": "LOCATION_STAGE_BARRIER", "status": "FAIL", "blockers": [{"code": "UNKNOWN_STAGE", "stage": target_stage}]}
    target_idx = STAGES.index(target_stage)
    blockers = []
    for stage in STAGES[:target_idx]:
        if stage_status.get(stage) != "PASS":
            blockers.append({"code": "PREVIOUS_STAGE_NOT_PASS", "stage": stage, "value": stage_status.get(stage)})
    return {"validator_id": "LOCATION_STAGE_BARRIER", "status": "PASS" if not blockers else "FAIL", "target_stage": target_stage, "blockers": blockers}
