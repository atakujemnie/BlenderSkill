from __future__ import annotations

"""Aggregate proof-bearing appearance-fidelity records with v0.11 owner closure."""

from collections.abc import Mapping
from typing import Any

EXECUTOR_ID = "APPEARANCE_FIDELITY_GATE"
EXECUTOR_VERSION = "0.2.0"
PASS = "PASS"
NOT_REQUIRED = "NOT_REQUIRED"
LEVELS = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}
ALLOWED_EVIDENCE = {
    "part_boundaries": {"PART_BOUNDARY_VALIDATION", "REGISTERED_OVERLAY", "FEATURE_ROI", "LOCAL_FEATURE_ROI"},
    "trim_paths": {"TRIM_PATH_VALIDATION", "REGISTERED_OVERLAY", "FEATURE_ROI", "LOCAL_FEATURE_ROI", "LANDMARK_PROJECTION"},
    "junctions": {"JUNCTION_VALIDATION", "FEATURE_ROI", "LOCAL_FEATURE_ROI", "LAYER_STACK", "REGISTERED_OVERLAY"},
    "edge_families": {"EDGE_FAMILY_VALIDATION", "FEATURE_ROI", "LOCAL_FEATURE_ROI", "REGISTERED_OVERLAY", "NUMERIC_MEASUREMENT"},
    "material_regions": {"MATERIAL_APPEARANCE_VALIDATION", "MATERIAL_SEGMENTATION", "REGISTERED_OVERLAY", "LOCAL_FEATURE_ROI"},
    "emissive_regions": {"EMISSIVE_REGION_VALIDATION", "FEATURE_ROI", "LOCAL_FEATURE_ROI", "MATERIAL_APPEARANCE_VALIDATION"},
    "branding": {"BRANDING_VALIDATION", "FEATURE_ROI", "LOCAL_FEATURE_ROI", "REGISTERED_OVERLAY"},
    "detail_coverage": {"DETAIL_COVERAGE"},
    "final_views": {"REGISTERED_OVERLAY", "SILHOUETTE_DIFF", "FEATURE_ROI"},
}
REFERENCE_DERIVED_KINDS = {
    "PART_BOUNDARY_VALIDATION",
    "TRIM_PATH_VALIDATION",
    "JUNCTION_VALIDATION",
    "EDGE_FAMILY_VALIDATION",
    "MATERIAL_APPEARANCE_VALIDATION",
    "MATERIAL_SEGMENTATION",
    "EMISSIVE_REGION_VALIDATION",
    "BRANDING_VALIDATION",
    "DETAIL_COVERAGE",
    "REGISTERED_OVERLAY",
    "SILHOUETTE_DIFF",
    "FEATURE_ROI",
    "LOCAL_FEATURE_ROI",
    "LANDMARK_PROJECTION",
}
PROJECTED_KINDS = {
    "REGISTERED_OVERLAY",
    "SILHOUETTE_DIFF",
    "FEATURE_ROI",
    "LOCAL_FEATURE_ROI",
    "LANDMARK_PROJECTION",
    "PART_BOUNDARY_VALIDATION",
    "TRIM_PATH_VALIDATION",
    "JUNCTION_VALIDATION",
}
CANONICAL_VALIDATORS = {
    "APPEARANCE_REFERENCE_VALIDATE",
    "REFERENCE_OVERLAY_VALIDATE",
    "LAYER_STACK_VALIDATE",
    "REFERENCE_MEASURE",
    "APPEARANCE_FIDELITY_GATE",
    "APPEARANCE_OWNER_COVERAGE",
}


def _status(value: Any) -> str:
    if isinstance(value, str):
        return value.upper()
    if isinstance(value, Mapping):
        return str(value.get("status", "UNVERIFIED")).upper()
    return "UNVERIFIED"


def _proof_blocker(owner: str, value: Any, proof_class: str, *, strict: bool) -> dict[str, str] | None:
    st = _status(value)
    if st == NOT_REQUIRED:
        return None
    if st != PASS:
        return {"owner": owner, "status": st, "reason": "required_appearance_owner_not_passed"}
    if not strict:
        return None
    if not isinstance(value, Mapping):
        return {"owner": owner, "status": "UNVERIFIED", "reason": "pass_without_evidence_record"}
    kind = str(value.get("evidence_kind", "")).upper()
    if kind not in ALLOWED_EVIDENCE[proof_class]:
        return {
            "owner": owner,
            "status": "UNVERIFIED",
            "reason": f"invalid_or_missing_evidence_kind:{kind or 'NONE'}",
        }
    provenance = str(value.get("provenance_id") or value.get("artifact_id") or "").strip()
    if not provenance:
        return {"owner": owner, "status": "UNVERIFIED", "reason": "missing_provenance_id"}
    validator = str(value.get("validator_id", "")).upper()
    if validator not in CANONICAL_VALIDATORS:
        return {
            "owner": owner,
            "status": "UNVERIFIED",
            "reason": f"noncanonical_or_missing_validator:{validator or 'NONE'}",
        }
    if kind in REFERENCE_DERIVED_KINDS and not (
        value.get("source_reference_ids") or value.get("source_reference_id")
    ):
        return {"owner": owner, "status": "UNVERIFIED", "reason": "missing_source_reference"}
    if kind in PROJECTED_KINDS and not value.get("registration_id"):
        return {"owner": owner, "status": "UNVERIFIED", "reason": "missing_registration_id"}
    return None


def _coverage_blocker(value: Any, *, strict: bool, require_complete: bool) -> dict[str, str] | None:
    blocker = _proof_blocker("detail_coverage", value, "detail_coverage", strict=strict)
    if blocker:
        return blocker
    if not isinstance(value, Mapping):
        return None
    missing = int(value.get("must_missing", 0) or 0)
    coverage = float(value.get("weighted_coverage", 1.0) or 0.0)
    if require_complete and missing != 0:
        return {
            "owner": "detail_coverage",
            "status": "FAIL",
            "reason": f"missing_must_features:{missing}",
        }
    if require_complete and coverage < 0.999999:
        return {
            "owner": "detail_coverage",
            "status": "FAIL",
            "reason": f"must_coverage_incomplete:{coverage:.6f}",
        }
    return None


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    target = str(report.get("target_fidelity", "L4")).upper()
    if target not in LEVELS:
        raise ValueError("target_fidelity must be L0..L5")
    strict = bool(report.get("strict_evidence", True))
    blockers: list[dict[str, str]] = []
    if LEVELS[target] < 4:
        return {
            "status": NOT_REQUIRED,
            "target_fidelity": target,
            "strict_evidence": strict,
            "blockers": [],
            "can_advance_to_recon_fidelity": True,
        }
    coverage = report.get("appearance_owner_coverage")
    if strict:
        if not isinstance(coverage, Mapping):
            blockers.append(
                {
                    "owner": "appearance_owner_coverage",
                    "status": "UNVERIFIED",
                    "reason": "canonical_owner_coverage_record_required",
                }
            )
        else:
            if str(coverage.get("validator_id", "")).upper() != "APPEARANCE_OWNER_COVERAGE":
                blockers.append(
                    {
                        "owner": "appearance_owner_coverage",
                        "status": "UNVERIFIED",
                        "reason": "canonical_owner_coverage_validator_required",
                    }
                )
            if str(coverage.get("status", "")).upper() != PASS:
                blockers.append(
                    {
                        "owner": "appearance_owner_coverage",
                        "status": str(coverage.get("status", "UNVERIFIED")).upper(),
                        "reason": "must_owner_inventory_not_closed",
                    }
                )
            missing = coverage.get("missing_must", []) or []
            if (missing if isinstance(missing, int) else len(missing)) != 0:
                blockers.append(
                    {
                        "owner": "appearance_owner_coverage",
                        "status": "FAIL",
                        "reason": "missing_must_owners",
                    }
                )
    required = [
        ("part_boundaries", "part_boundaries"),
        ("trim_paths", "trim_paths"),
        ("junctions", "junctions"),
        ("edge_families", "edge_families"),
        ("material_regions", "material_regions"),
        ("final_views", "final_views"),
    ]
    if report.get("emissive_regions") is not None:
        required.append(("emissive_regions", "emissive_regions"))
    if report.get("branding") is not None:
        required.append(("branding", "branding"))
    for owner, proof_class in required:
        blocker = _proof_blocker(owner, report.get(owner), proof_class, strict=strict)
        if blocker:
            blockers.append(blocker)
    if LEVELS[target] >= 5:
        blocker = _coverage_blocker(report.get("detail_coverage"), strict=strict, require_complete=True)
        if blocker:
            blockers.append(blocker)
    for item in list(report.get("must_owners", [])):
        owner_id = str(item.get("id", "UNKNOWN")) if isinstance(item, Mapping) else "UNKNOWN"
        st = _status(item)
        if st not in {PASS, NOT_REQUIRED}:
            blockers.append(
                {
                    "owner": f"must_owner:{owner_id}",
                    "status": st,
                    "reason": "MUST_appearance_owner_not_passed",
                }
            )
    score = report.get("reference_fidelity_score")
    benchmark_threshold = report.get("benchmark_score_threshold")
    if benchmark_threshold is not None and score is not None and float(score) < float(benchmark_threshold):
        blockers.append(
            {
                "owner": "benchmark_score",
                "status": "FAIL",
                "reason": f"score_{float(score):.2f}_below_{float(benchmark_threshold):.2f}",
            }
        )
    return {
        "status": PASS if not blockers else "FAIL",
        "target_fidelity": target,
        "strict_evidence": strict,
        "reference_fidelity_score": score,
        "blockers": blockers,
        "can_advance_to_recon_fidelity": not blockers,
    }
