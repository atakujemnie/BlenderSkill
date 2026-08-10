from __future__ import annotations

"""Validate an independent multi-view visual review against MUST features.

The gate deliberately does not pretend that a numeric global similarity score is
sufficient. A multimodal reviewer must bind its verdict to the exact asset/scene
revision and report every reference-critical MUST feature separately. Newly
noticed reference features that are absent from the Feature Contract are blockers
rather than being silently ignored.
"""

from typing import Any, Mapping

EXECUTOR_ID = "VISUAL_FIDELITY_REVIEW_GATE"
EXECUTOR_VERSION = "0.22.0"
ALLOWED_STATUSES = {"PASS", "FAIL", "BLOCKED", "NOT_VISIBLE"}


def _features(asset: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for component_id, raw_component in dict(asset.get("components", {}) or {}).items():
        if not isinstance(raw_component, Mapping):
            continue
        contract = raw_component.get("feature_contract")
        if isinstance(contract, Mapping):
            raw_features = contract.get("features", contract)
        else:
            raw_features = contract
        records: list[dict[str, Any]] = []
        if isinstance(raw_features, Mapping):
            records = [
                {"feature_id": str(feature_id), **dict(raw)}
                for feature_id, raw in raw_features.items()
                if isinstance(raw, Mapping)
            ]
        elif isinstance(raw_features, list):
            records = [dict(item) for item in raw_features if isinstance(item, Mapping)]
        for record in records:
            feature_id = str(record.get("feature_id") or record.get("id") or "")
            if not feature_id:
                continue
            out[feature_id] = {"component_id": str(component_id), **record, "feature_id": feature_id}
    return out


def validate(
    asset: Mapping[str, Any],
    review: Mapping[str, Any],
    *,
    scene_revision: int,
    reference_revision: int,
) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    asset_id = str(asset.get("asset_id") or "")
    revision = int(asset.get("revision", 0))

    if str(review.get("asset_id") or "") != asset_id:
        blockers.append({"reason": "FIDELITY_REVIEW_ASSET_MISMATCH"})
    if int(review.get("asset_revision", 0)) != revision:
        blockers.append(
            {
                "reason": "FIDELITY_REVIEW_ASSET_REVISION_STALE",
                "expected": revision,
                "actual": int(review.get("asset_revision", 0)),
            }
        )
    if int(review.get("scene_revision", 0)) != int(scene_revision):
        blockers.append(
            {
                "reason": "FIDELITY_REVIEW_SCENE_REVISION_STALE",
                "expected": int(scene_revision),
                "actual": int(review.get("scene_revision", 0)),
            }
        )
    if int(review.get("reference_revision", 0)) != int(reference_revision):
        blockers.append(
            {
                "reason": "FIDELITY_REVIEW_REFERENCE_REVISION_STALE",
                "expected": int(reference_revision),
                "actual": int(review.get("reference_revision", 0)),
            }
        )

    reviewer_id = str(review.get("reviewer_id") or "")
    worker_id = str(review.get("worker_id") or "")
    reviewer_role = str(review.get("reviewer_role") or "").upper()
    if not reviewer_id:
        blockers.append({"reason": "FIDELITY_REVIEWER_ID_REQUIRED"})
    if reviewer_role != "INDEPENDENT_VISUAL_REVIEWER":
        blockers.append({"reason": "INDEPENDENT_VISUAL_REVIEWER_REQUIRED", "actual": reviewer_role})
    if worker_id and reviewer_id == worker_id:
        blockers.append({"reason": "VISUAL_REVIEWER_MUST_DIFFER_FROM_WORKER", "reviewer_id": reviewer_id})

    qa_views = [dict(item) for item in list(review.get("qa_views", []) or []) if isinstance(item, Mapping)]
    if not qa_views:
        blockers.append({"reason": "QA_VIEWS_REQUIRED"})
    qa_view_ids = {str(item.get("view_id") or item.get("view") or "") for item in qa_views if item.get("view_id") or item.get("view")}
    for view in qa_views:
        if not str(view.get("render_artifact_id") or ""):
            blockers.append({"reason": "QA_RENDER_ARTIFACT_REQUIRED", "view": view.get("view_id") or view.get("view")})
        evidence = [str(value) for value in list(view.get("reference_evidence_ids", []) or []) if str(value)]
        if not evidence:
            blockers.append({"reason": "QA_REFERENCE_EVIDENCE_REQUIRED", "view": view.get("view_id") or view.get("view")})

    contract_features = _features(asset)
    must_features = {
        feature_id: feature
        for feature_id, feature in contract_features.items()
        if str(feature.get("priority", "MUST")).upper() == "MUST"
        and bool(feature.get("visual_required", True))
    }

    reviewed: dict[str, dict[str, Any]] = {}
    for raw in list(review.get("feature_reviews", []) or []):
        if not isinstance(raw, Mapping):
            continue
        item = dict(raw)
        feature_id = str(item.get("feature_id") or "")
        status = str(item.get("status") or "").upper()
        if not feature_id:
            blockers.append({"reason": "VISUAL_FEATURE_REVIEW_ID_REQUIRED"})
            continue
        if status not in ALLOWED_STATUSES:
            blockers.append({"reason": "VISUAL_FEATURE_REVIEW_STATUS_INVALID", "feature_id": feature_id, "status": status})
            continue
        if feature_id in reviewed:
            blockers.append({"reason": "VISUAL_FEATURE_REVIEW_DUPLICATE", "feature_id": feature_id})
            continue
        reviewed[feature_id] = item

    missing = sorted(set(must_features) - set(reviewed))
    if missing:
        blockers.append({"reason": "MUST_VISUAL_FEATURES_NOT_REVIEWED", "feature_ids": missing})

    for feature_id, feature in must_features.items():
        item = reviewed.get(feature_id)
        if not item:
            continue
        status = str(item.get("status") or "").upper()
        if status != "PASS":
            blockers.append(
                {
                    "reason": "MUST_VISUAL_FEATURE_FAILED",
                    "feature_id": feature_id,
                    "status": status,
                    "notes": item.get("notes"),
                }
            )
        required_views = {str(value) for value in list(feature.get("qa_views", []) or []) if str(value)}
        reviewed_views = {str(value) for value in list(item.get("view_ids", []) or []) if str(value)}
        if required_views and not (required_views & reviewed_views):
            blockers.append(
                {
                    "reason": "MUST_VISUAL_FEATURE_QA_VIEW_MISSING",
                    "feature_id": feature_id,
                    "required_any": sorted(required_views),
                    "reviewed": sorted(reviewed_views),
                }
            )
        if reviewed_views - qa_view_ids:
            blockers.append(
                {
                    "reason": "VISUAL_FEATURE_REFERENCES_UNKNOWN_QA_VIEW",
                    "feature_id": feature_id,
                    "view_ids": sorted(reviewed_views - qa_view_ids),
                }
            )

    discovered = [dict(item) for item in list(review.get("discovered_unmapped_features", []) or []) if isinstance(item, Mapping)]
    if discovered:
        blockers.append(
            {
                "reason": "UNMAPPED_REFERENCE_FEATURES_DISCOVERED",
                "features": discovered,
            }
        )

    global_score = review.get("global_similarity_score")
    threshold = float(review.get("minimum_global_similarity_score", 0.0))
    if global_score is not None:
        try:
            score = float(global_score)
        except (TypeError, ValueError):
            blockers.append({"reason": "GLOBAL_SIMILARITY_SCORE_INVALID"})
        else:
            if score < threshold:
                blockers.append(
                    {
                        "reason": "GLOBAL_SIMILARITY_SCORE_TOO_LOW",
                        "minimum": threshold,
                        "actual": score,
                    }
                )
            warnings.append({"reason": "GLOBAL_SCORE_IS_SECONDARY_TO_MUST_FEATURES", "score": score})

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "validator_version": EXECUTOR_VERSION,
        "asset_id": asset_id,
        "asset_revision": revision,
        "scene_revision": int(scene_revision),
        "reference_revision": int(reference_revision),
        "reviewer_id": reviewer_id,
        "must_visual_feature_count": len(must_features),
        "reviewed_feature_count": len(reviewed),
        "qa_view_count": len(qa_views),
        "blockers": blockers,
        "warnings": warnings,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "validate"]
