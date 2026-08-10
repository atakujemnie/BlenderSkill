from __future__ import annotations

"""Turn reference-evidence metadata into worker-consumable local attachment descriptors."""

from pathlib import Path
from typing import Any, Mapping

EXECUTOR_ID = "REFERENCE_EVIDENCE_MATERIALIZER"
EXECUTOR_VERSION = "0.21.0"


def _safe_path(path: str, *, allowed_root: str | Path | None) -> str:
    resolved = Path(path).expanduser().resolve()
    if allowed_root is not None:
        root = Path(allowed_root).expanduser().resolve()
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise ValueError("REFERENCE_ARTIFACT_OUTSIDE_ALLOWED_ROOT") from exc
    if not resolved.is_file():
        raise ValueError("REFERENCE_ARTIFACT_FILE_NOT_FOUND")
    return str(resolved)


def materialize(
    evidence: list[Mapping[str, Any]],
    artifact_catalog: Mapping[str, Mapping[str, Any]],
    *,
    allowed_root: str | Path | None = None,
) -> dict[str, Any]:
    attachments: list[dict[str, Any]] = []
    blockers: list[dict[str, Any]] = []
    for raw in evidence:
        item = dict(raw)
        artifact_id = str(item.get("artifact_id") or "")
        descriptor = artifact_catalog.get(artifact_id)
        if not isinstance(descriptor, Mapping):
            blockers.append({"reason": "REFERENCE_ARTIFACT_DESCRIPTOR_MISSING", "artifact_id": artifact_id})
            continue
        path = str(descriptor.get("path") or "")
        try:
            resolved_path = _safe_path(path, allowed_root=allowed_root)
        except ValueError as exc:
            blockers.append({"reason": str(exc), "artifact_id": artifact_id})
            continue
        roi = item.get("roi")
        if roi is not None:
            if not isinstance(roi, (list, tuple)) or len(roi) != 4:
                blockers.append({"reason": "REFERENCE_ROI_XYXY_REQUIRED", "evidence_id": item.get("evidence_id")})
                continue
            roi = [float(value) for value in roi]
        attachments.append(
            {
                "evidence_id": item.get("evidence_id"),
                "artifact_id": artifact_id,
                "path": resolved_path,
                "media_type": descriptor.get("media_type", "image/png"),
                "roi": roi,
                "view": item.get("view"),
                "authority": item.get("authority"),
                "feature_ids": list(item.get("feature_ids", []) or []),
            }
        )
    return {
        "status": "PASS" if not blockers else "FAIL",
        "executor_id": EXECUTOR_ID,
        "attachment_count": len(attachments),
        "attachments": attachments,
        "blockers": blockers,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "materialize"]
