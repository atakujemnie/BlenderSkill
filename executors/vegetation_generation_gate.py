from __future__ import annotations

"""Aggregate authoring acceptance for generated vegetation before runtime prep."""

from typing import Any, Mapping

EXECUTOR_ID = "VEGETATION_GENERATION_GATE"; EXECUTOR_VERSION = "0.1.0"


def _pass(record: Mapping[str, Any] | None, validator: str | None = None) -> bool:
    if not isinstance(record, Mapping) or str(record.get("status", "")).upper() != "PASS": return False
    return not validator or str(record.get("validator_id", "")).upper() == validator.upper()


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    if not _pass(report.get("provider"), "PROCEDURAL_GENERATOR_PROVIDER"): blockers.append({"reason": "PROVIDER_GATE_REQUIRED"})
    if not _pass(report.get("botanical_grammar"), "VEGETATION_BOTANICAL_GRAMMAR"): blockers.append({"reason": "BOTANICAL_GRAMMAR_REQUIRED"})
    meta = dict(report.get("generation_metadata") or {})
    for key in ("generator", "generator_version", "seed", "parameters_hash", "geometry_signature"):
        if meta.get(key) is None or meta.get(key) == "": blockers.append({"reason": "GENERATION_METADATA_REQUIRED", "field": key})
    if not isinstance(meta.get("seed"), int): blockers.append({"reason": "INTEGER_SEED_REQUIRED"})
    semantic_parts = set(str(x) for x in meta.get("semantic_parts", []) or [])
    if not semantic_parts: blockers.append({"reason": "SEMANTIC_PARTS_REQUIRED"})
    if int(meta.get("generated_triangle_count", 0) or 0) <= 0: blockers.append({"reason": "NONEMPTY_GEOMETRY_REQUIRED"})
    reproduction = dict(report.get("reproduction_probe") or {})
    if str(reproduction.get("status", "")).upper() != "PASS": blockers.append({"reason": "REPRODUCTION_PROBE_REQUIRED"})
    elif reproduction.get("first_signature") != reproduction.get("second_signature"): blockers.append({"reason": "NONDETERMINISTIC_OUTPUT_FOR_FIXED_SEED"})
    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID, "provenance_id": report.get("provenance_id"), "blockers": blockers, "can_advance_to_runtime_prep": not blockers}
