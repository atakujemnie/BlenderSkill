from __future__ import annotations

"""Acceptance gate for Geometry-Nodes-to-Python compilation artifacts."""

from typing import Any, Mapping

EXECUTOR_ID = "NODEGRAPH_TO_PYTHON"
EXECUTOR_VERSION = "0.1.0"


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    required = ["source_node_tree_id", "source_node_tree_hash", "compiler_provider_id", "compiler_provider_version", "blender_version", "generated_script_hash", "provenance_id"]
    for key in required:
        if not report.get(key): blockers.append({"reason": "FIELD_REQUIRED", "field": key})
    if str(report.get("compiler_probe_status", "")).upper() != "PASS": blockers.append({"reason": "COMPILER_PROVIDER_NOT_PROBED"})
    if str(report.get("roundtrip_probe_status", "")).upper() != "PASS": blockers.append({"reason": "GENERATED_SCRIPT_ROUNDTRIP_REQUIRED"})
    if bool(report.get("requires_runtime_compiler_dependency", False)) and not bool(report.get("runtime_dependency_approved", False)): blockers.append({"reason": "UNAPPROVED_RUNTIME_COMPILER_DEPENDENCY"})
    if report.get("source_node_tree_hash") == report.get("generated_script_hash"): blockers.append({"reason": "HASH_DOMAIN_COLLISION_OR_INVALID_PROVENANCE"})
    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID, "provenance_id": report.get("provenance_id"), "blockers": blockers, "runtime_independent": not bool(report.get("requires_runtime_compiler_dependency", False))}
