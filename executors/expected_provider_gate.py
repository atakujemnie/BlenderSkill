from __future__ import annotations

"""Verify expected providers against normalized discovery and version constraints."""

from typing import Any, Mapping

from executors.version_constraints import satisfies

EXECUTOR_ID = "EXPECTED_PROVIDER_GATE"
EXECUTOR_VERSION = "0.18.0"


def evaluate(expected: list[Mapping[str, Any]], inventory: Mapping[str, Any], *, require_exact_version: bool = False) -> dict[str, Any]:
    providers = {str(p.get("provider_id")): p for p in inventory.get("providers", []) or []}
    blockers: list[dict[str, Any]] = []
    matched: list[dict[str, Any]] = []

    for item in expected:
        provider_id = str(item.get("provider_id") or "").strip()
        if not provider_id:
            blockers.append({"reason": "EXPECTED_PROVIDER_ID_REQUIRED"})
            continue
        found = providers.get(provider_id)
        if not found:
            blockers.append({"reason": "DISCOVERY_MISMATCH", "provider_id": provider_id, "expected_version": item.get("version"), "version_constraint": item.get("version_constraint")})
            continue
        found_version = str(found.get("version") or "UNKNOWN")
        exact = str(item.get("version") or "").strip()
        constraint = str(item.get("version_constraint") or "").strip()
        if require_exact_version and exact:
            constraint = f"=={exact}"
        elif exact and not constraint:
            constraint = f"=={exact}"
        if constraint:
            try:
                ok = satisfies(found_version, constraint)
            except ValueError as exc:
                blockers.append({"reason": "INVALID_VERSION_CONSTRAINT", "provider_id": provider_id, "constraint": constraint, "error": str(exc)})
                continue
            if not ok:
                blockers.append({"reason": "EXPECTED_PROVIDER_VERSION_MISMATCH", "provider_id": provider_id, "version_constraint": constraint, "found_version": found_version})
                continue
        matched.append({"provider_id": provider_id, "version_constraint": constraint or None, "found_version": found_version, "enabled": bool(found.get("enabled", False))})

    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID, "matched": matched, "blockers": blockers}
