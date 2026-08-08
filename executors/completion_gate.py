from __future__ import annotations

"""Pure-Python completion gate for Blender asset agents.

The caller supplies compact check statuses. This module does not inspect a
scene; it prevents ambiguous 'DONE' reporting by evaluating explicit levels.

v0.7 hardening:
- `PIPELINE_INTEGRATED` cannot be closed by a bare Blender-side round-trip claim.

v0.8 hardening:
- `RECONSTRUCTION_COMPLETE` requires a proof-bearing reconstruction fidelity
  gate record;
- `GAME_READY_COMPLETE` requires runtime package validation, so a loadable glTF
  with missing primitive attributes or forbidden node transforms cannot pass.
"""

from collections.abc import Mapping
from typing import Sequence


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

ENGINE_RUNTIME_EVIDENCE_KINDS = {
    "ENGINE_PRODUCTION_LOADER",
    "ENGINE_REGRESSION_TEST",
    "ENGINE_INSTANTIATION",
}

TYPED_EVIDENCE_REQUIREMENTS = {
    "reconstruction_fidelity_gate": {"RECON_FIDELITY_GATE"},
    "runtime_package_validation": {"RUNTIME_PACKAGE_VALIDATE"},
}

DEFAULT_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "RECONSTRUCTION_COMPLETE": (
        "hard_dimensions",
        "canonical_silhouettes",
        "must_features",
        "multi_view_gate",
        "reconstruction_fidelity_gate",
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
        "runtime_package_validation",
        "export_validation",
        "runtime_emissive_data",
        "export_roundtrip_invariants",
    ),
    "PIPELINE_INTEGRATED": (
        "asset_catalog_registration",
        "runtime_import_or_instantiation",
    ),
}


def _status_and_evidence(value) -> tuple[str, str | None, str | None]:
    if isinstance(value, Mapping):
        status = str(value.get("status", NOT_EVALUATED))
        evidence = value.get("evidence_kind")
        provenance = (
            value.get("provenance_id")
            or value.get("artifact_id")
            or value.get("report_id")
        )
        return (
            status,
            str(evidence) if evidence is not None else None,
            str(provenance) if provenance is not None else None,
        )
    return str(value), None, None


def _requirement_passes(key: str, value) -> bool:
    status, evidence, provenance = _status_and_evidence(value)
    if status == NOT_REQUIRED:
        return True
    if status != PASS:
        return False

    if key == "runtime_import_or_instantiation":
        return evidence in ENGINE_RUNTIME_EVIDENCE_KINDS

    allowed = TYPED_EVIDENCE_REQUIREMENTS.get(key)
    if allowed is not None:
        return evidence in allowed and bool(provenance)

    return True


def _blocker(key: str, value) -> dict:
    status, evidence, provenance = _status_and_evidence(value)
    item = {"check": key, "status": status}

    if key == "runtime_import_or_instantiation":
        item["evidence_kind"] = evidence
        if status == PASS and evidence not in ENGINE_RUNTIME_EVIDENCE_KINDS:
            item["status"] = UNVERIFIED
            item["reason"] = "TARGET_ENGINE_EVIDENCE_REQUIRED"
        return item

    allowed = TYPED_EVIDENCE_REQUIREMENTS.get(key)
    if allowed is not None:
        item["evidence_kind"] = evidence
        item["provenance_id"] = provenance
        if status == PASS and (evidence not in allowed or not provenance):
            item["status"] = UNVERIFIED
            item["reason"] = "TYPED_PROOF_WITH_PROVENANCE_REQUIRED"

    return item


def evaluate_completion(
    checks: Mapping[str, object],
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
            if not _requirement_passes(key, value):
                failed.append(_blocker(key, value))

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
        "runtime_evidence_kinds": sorted(ENGINE_RUNTIME_EVIDENCE_KINDS),
        "typed_evidence_requirements": {
            key: sorted(value) for key, value in TYPED_EVIDENCE_REQUIREMENTS.items()
        },
    }
