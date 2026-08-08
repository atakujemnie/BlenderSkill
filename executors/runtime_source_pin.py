from __future__ import annotations

"""Validate that the project-embedded BlenderSkill runtime matches the canonical release."""

from typing import Any, Mapping

EXECUTOR_ID = "CANONICAL_SKILL_RUNTIME_PIN"
EXECUTOR_VERSION = "0.1.0"


def evaluate(runtime: Mapping[str, Any], expected: Mapping[str, Any]) -> dict[str, Any]:
    blockers = []
    for key in ("version", "commit"):
        got = str(runtime.get(key, "")).strip(); want = str(expected.get(key, "")).strip()
        if not want: blockers.append({"reason": f"EXPECTED_{key.upper()}_REQUIRED"})
        elif got != want: blockers.append({"reason": f"{key.upper()}_MISMATCH", "expected": want, "actual": got})
    source = str(runtime.get("source_path", "")).strip()
    if not source: blockers.append({"reason": "RUNTIME_SOURCE_PATH_REQUIRED"})
    duplicate_roots = list(runtime.get("active_duplicate_roots", []) or [])
    if duplicate_roots: blockers.append({"reason": "MULTIPLE_ACTIVE_SKILL_ROOTS_FORBIDDEN", "roots": duplicate_roots})
    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID, "runtime_version": runtime.get("version"), "runtime_commit": runtime.get("commit"), "source_path": source, "blockers": blockers}
