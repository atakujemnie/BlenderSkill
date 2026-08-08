from __future__ import annotations

"""Hard proof-bearing reconstruction-fidelity transition gate.

v0.10 hardening:
- L4/L5 reconstruction requires APPEARANCE_FIDELITY_GATE proof;
- strict proof records name canonical validator IDs;
- reference-derived/projected evidence must link to source/registration;
- downstream runtime success cannot compensate for appearance failure.
"""

from typing import Any, Mapping

EXECUTOR_ID = "RECON_FIDELITY_GATE"
EXECUTOR_VERSION = "0.3.0"

LEVELS = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}

ALLOWED_EVIDENCE = {
    "hard_dimensions": {"NUMERIC_MEASUREMENT", "EXPORT_ROUNDTRIP_MEASUREMENT"},
    "landmarks_d0_d1": {"LANDMARK_PROJECTION", "NUMERIC_MEASUREMENT"},
    "material_segmentation": {"MATERIAL_SEGMENTATION", "REGISTERED_OVERLAY"},
    "canonical_view": {"REGISTERED_OVERLAY", "SILHOUETTE_DIFF"},
    "must_feature": {
        "FEATURE_ROI",
        "LAYER_STACK",
        "RAY_VISIBILITY",
        "NUMERIC_MEASUREMENT",
        "REGISTERED_OVERLAY",
        "SILHOUETTE_DIFF",
        "LANDMARK_PROJECTION",
        "PART_BOUNDARY_VALIDATION",
        "TRIM_PATH_VALIDATION",
        "JUNCTION_VALIDATION",
        "EDGE_FAMILY_VALIDATION",
        "MATERIAL_APPEARANCE_VALIDATION",
        "EMISSIVE_REGION_VALIDATION",
        "DETAIL_COVERAGE",
    },
    "appearance_fidelity": {"APPEARANCE_FIDELITY_GATE"},
}

ALLOWED_VALIDATORS = {
    "hard_dimensions": {"REFERENCE_MEASURE", "EXPORT_ROUNDTRIP_VALIDATE"},
    "landmarks_d0_d1": {"REFERENCE_MEASURE", "REFERENCE_OVERLAY_VALIDATE", "APPEARANCE_REFERENCE_VALIDATE"},
    "material_segmentation": {"REFERENCE_OVERLAY_VALIDATE", "APPEARANCE_REFERENCE_VALIDATE"},
    "canonical_view": {"REFERENCE_OVERLAY_VALIDATE"},
    "must_feature": {
        "REFERENCE_OVERLAY_VALIDATE",
        "APPEARANCE_REFERENCE_VALIDATE",
        "LAYER_STACK_VALIDATE",
        "REFERENCE_MEASURE",
    },
    "appearance_fidelity": {"APPEARANCE_FIDELITY_GATE"},
}

REFERENCE_PROOF_CLASSES = {
    "hard_dimensions",
    "landmarks_d0_d1",
    "material_segmentation",
    "canonical_view",
    "must_feature",
}

PROJECTED_EVIDENCE = {
    "REGISTERED_OVERLAY",
    "SILHOUETTE_DIFF",
    "FEATURE_ROI",
    "LANDMARK_PROJECTION",
    "PART_BOUNDARY_VALIDATION",
    "TRIM_PATH_VALIDATION",
    "JUNCTION_VALIDATION",
}


def _status(item: Any) -> str:
    if isinstance(item, str):
        return item.upper()
    if isinstance(item, Mapping):
        return str(item.get("status", "UNVERIFIED")).upper()
    return "UNVERIFIED"


def _proof_blocker(
    owner: str,
    value: Any,
    *,
    proof_class: str,
    strict_evidence: bool,
) -> dict[str, str] | None:
    st = _status(value)
    if st != "PASS":
        return {"owner": owner, "status": st, "reason": "required_gate_not_passed"}

    if not strict_evidence:
        return None

    if not isinstance(value, Mapping):
        return {"owner": owner, "status": "UNVERIFIED", "reason": "pass_without_evidence_record"}

    evidence_kind = str(value.get("evidence_kind", "")).upper()
    allowed = ALLOWED_EVIDENCE[proof_class]
    if evidence_kind not in allowed:
        return {
            "owner": owner,
            "status": "UNVERIFIED",
            "reason": f"invalid_or_missing_evidence_kind:{evidence_kind or 'NONE'}",
        }

    provenance_id = str(
        value.get("provenance_id")
        or value.get("registration_id")
        or value.get("artifact_id")
        or ""
    ).strip()
    if not provenance_id:
        return {"owner": owner, "status": "UNVERIFIED", "reason": "missing_provenance_id"}

    validator = str(value.get("validator_id", "")).upper()
    if validator not in ALLOWED_VALIDATORS[proof_class]:
        return {
            "owner": owner,
            "status": "UNVERIFIED",
            "reason": f"invalid_or_missing_validator:{validator or 'NONE'}",
        }

    if proof_class in REFERENCE_PROOF_CLASSES:
        refs = value.get("source_reference_ids") or value.get("source_reference_id")
        if not refs:
            return {"owner": owner, "status": "UNVERIFIED", "reason": "missing_source_reference"}

    if evidence_kind in PROJECTED_EVIDENCE and not value.get("registration_id"):
        return {"owner": owner, "status": "UNVERIFIED", "reason": "missing_registration_id"}

    return None


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    target = str(report.get("target_fidelity", "L3")).upper()
    achieved = str(report.get("achieved_fidelity", "L0")).upper()
    strict_evidence = bool(report.get("strict_evidence", True))

    if target not in LEVELS or achieved not in LEVELS:
        raise ValueError("fidelity level must be L0..L5")

    blockers: list[dict[str, str]] = []

    required_single = [
        ("hard_dimensions", report.get("hard_dimensions"), "hard_dimensions"),
        ("landmarks_d0_d1", report.get("landmarks_d0_d1"), "landmarks_d0_d1"),
    ]
    if LEVELS[target] >= 4:
        required_single.extend([
            ("material_segmentation", report.get("material_segmentation"), "material_segmentation"),
            ("appearance_fidelity", report.get("appearance_fidelity"), "appearance_fidelity"),
        ])

    for owner, value, proof_class in required_single:
        blocker = _proof_blocker(
            owner,
            value,
            proof_class=proof_class,
            strict_evidence=strict_evidence,
        )
        if blocker:
            blockers.append(blocker)

    canonical = dict(report.get("canonical_views", {}))
    required_views = list(report.get("required_views", ["FRONT", "SIDE", "TOP", "REAR", "BOTTOM"]))
    for view in required_views:
        blocker = _proof_blocker(
            f"view:{view}",
            canonical.get(view),
            proof_class="canonical_view",
            strict_evidence=strict_evidence,
        )
        if blocker:
            blocker["reason"] = (
                "canonical_view_not_passed"
                if blocker["reason"] == "required_gate_not_passed"
                else blocker["reason"]
            )
            blockers.append(blocker)

    for feature in list(report.get("must_features", [])):
        fid = str(feature.get("id", "UNKNOWN"))
        blocker = _proof_blocker(
            f"feature:{fid}",
            feature,
            proof_class="must_feature",
            strict_evidence=strict_evidence,
        )
        if blocker:
            blocker["reason"] = (
                "MUST_feature_not_passed"
                if blocker["reason"] == "required_gate_not_passed"
                else blocker["reason"]
            )
            blockers.append(blocker)

    for dev in list(report.get("deviations", [])):
        severity = str(dev.get("severity", "SOFT")).upper()
        st = str(dev.get("status", "OPEN")).upper()
        if severity not in {"HARD", "MUST", "CANONICAL"}:
            continue

        owner = f"deviation:{dev.get('id', 'UNKNOWN')}"
        if st not in {"RESOLVED", "ACCEPTED_BY_AUTHORITY"}:
            blockers.append({"owner": owner, "status": st, "reason": "unresolved_hard_deviation"})
            continue

        if strict_evidence and st == "ACCEPTED_BY_AUTHORITY":
            authority_source = str(dev.get("authority_source", "")).strip()
            authority_record = str(dev.get("authority_record_id", "")).strip()
            if not authority_source or not authority_record:
                blockers.append({
                    "owner": owner,
                    "status": "UNVERIFIED",
                    "reason": "authority_acceptance_without_record",
                })

        if strict_evidence and st == "RESOLVED":
            resolution_record = str(
                dev.get("resolution_record_id")
                or dev.get("provenance_id")
                or ""
            ).strip()
            if not resolution_record:
                blockers.append({
                    "owner": owner,
                    "status": "UNVERIFIED",
                    "reason": "resolved_deviation_without_evidence",
                })

    if LEVELS[achieved] < LEVELS[target]:
        blockers.append({
            "owner": "fidelity_level",
            "status": achieved,
            "reason": f"target_{target}_not_reached",
        })

    return {
        "status": "PASS" if not blockers else "FAIL",
        "strict_evidence": strict_evidence,
        "target_fidelity": target,
        "achieved_fidelity": achieved,
        "blockers": blockers,
        "can_advance_to_runtime": not blockers,
        "next_state": "R12_TOPOLOGY_RUNTIME" if not blockers else "BACKTRACK_TO_EARLIEST_FIDELITY_OWNER",
    }
