"""Index multi-view reference evidence by component and feature without resending full sheets."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

EXECUTOR_ID = "REFERENCE_EVIDENCE_REGISTRY"
EXECUTOR_VERSION = "0.1.0"
AUTHORITIES = {"PRIMARY", "SECONDARY", "INSPIRATION"}
VIEWS = {"FRONT", "REAR", "LEFT", "RIGHT", "SIDE", "TOP", "BOTTOM", "PERSPECTIVE", "DETAIL"}


def validate(registry: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    entries = list(registry.get("evidence", []) or [])
    ids: set[str] = set()
    for raw in entries:
        if not isinstance(raw, Mapping):
            blockers.append({"reason": "EVIDENCE_RECORD_INVALID"})
            continue
        item = dict(raw)
        evidence_id = str(item.get("evidence_id") or "")
        if not evidence_id:
            blockers.append({"reason": "EVIDENCE_ID_REQUIRED"})
        elif evidence_id in ids:
            blockers.append({"reason": "DUPLICATE_EVIDENCE_ID", "evidence_id": evidence_id})
        ids.add(evidence_id)
        if not str(item.get("reference_id") or ""):
            blockers.append({"reason": "REFERENCE_ID_REQUIRED", "evidence_id": evidence_id})
        if not str(item.get("component_id") or ""):
            blockers.append({"reason": "COMPONENT_ID_REQUIRED", "evidence_id": evidence_id})
        authority = str(item.get("authority", "PRIMARY")).upper()
        if authority not in AUTHORITIES:
            blockers.append({"reason": "REFERENCE_AUTHORITY_INVALID", "evidence_id": evidence_id})
        view = str(item.get("view", "DETAIL")).upper()
        if view not in VIEWS:
            blockers.append({"reason": "REFERENCE_VIEW_INVALID", "evidence_id": evidence_id, "view": view})
        roi = item.get("roi")
        if roi is not None:
            if not isinstance(roi, (list, tuple)) or len(roi) != 4:
                blockers.append({"reason": "ROI_XYXY_REQUIRED", "evidence_id": evidence_id})
            else:
                try:
                    x1, y1, x2, y2 = (float(v) for v in roi)
                    if x2 <= x1 or y2 <= y1:
                        blockers.append({"reason": "ROI_NOT_POSITIVE", "evidence_id": evidence_id})
                except (TypeError, ValueError):
                    blockers.append({"reason": "ROI_NUMERIC_REQUIRED", "evidence_id": evidence_id})
        if not item.get("artifact_id") and roi is not None:
            blockers.append({"reason": "ROI_ARTIFACT_REQUIRED", "evidence_id": evidence_id})
    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "evidence_count": len(entries),
        "blockers": blockers,
    }


def query(
    registry: Mapping[str, Any],
    *,
    component_id: str,
    feature_ids: list[str] | None = None,
    views: list[str] | None = None,
    include_inspiration: bool = False,
) -> dict[str, Any]:
    verdict = validate(registry)
    if verdict["status"] != "PASS":
        return verdict
    wanted_features = {str(x) for x in (feature_ids or [])}
    wanted_views = {str(x).upper() for x in (views or [])}
    matches: list[dict[str, Any]] = []
    for raw in registry.get("evidence", []) or []:
        item = dict(raw)
        if str(item.get("component_id")) != str(component_id):
            continue
        if not include_inspiration and str(item.get("authority", "PRIMARY")).upper() == "INSPIRATION":
            continue
        if wanted_views and str(item.get("view", "DETAIL")).upper() not in wanted_views:
            continue
        item_features = {str(x) for x in item.get("feature_ids", []) or []}
        if wanted_features and not (wanted_features & item_features):
            continue
        matches.append(
            {
                key: item.get(key)
                for key in (
                    "evidence_id",
                    "reference_id",
                    "component_id",
                    "view",
                    "authority",
                    "feature_ids",
                    "roi",
                    "artifact_id",
                    "registration_id",
                )
                if item.get(key) is not None
            }
        )
    authority_rank = {"PRIMARY": 0, "SECONDARY": 1, "INSPIRATION": 2}
    matches.sort(key=lambda item: (authority_rank.get(str(item.get("authority", "PRIMARY")).upper(), 9), str(item.get("view")), str(item.get("evidence_id"))))
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "component_id": component_id,
        "evidence": matches,
        "evidence_count": len(matches),
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "query", "validate"]
