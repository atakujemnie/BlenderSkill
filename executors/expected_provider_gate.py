from __future__ import annotations

"""Verify user/project-declared installed providers against normalized discovery."""

from typing import Any, Mapping

EXECUTOR_ID = "EXPECTED_PROVIDER_GATE"
EXECUTOR_VERSION = "0.17.0"


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
            blockers.append({"reason": "DISCOVERY_MISMATCH", "provider_id": provider_id, "expected_version": item.get("version")})
            continue
        expected_version = str(item.get("version") or "").strip()
        found_version = str(found.get("version") or "UNKNOWN")
        if require_exact_version and expected_version and expected_version != found_version:
            blockers.append({
                "reason": "EXPECTED_PROVIDER_VERSION_MISMATCH",
                "provider_id": provider_id,
                "expected_version": expected_version,
                "found_version": found_version,
            })
            continue
        matched.append({
            "provider_id": provider_id,
            "expected_version": expected_version or None,
            "found_version": found_version,
            "enabled": bool(found.get("enabled", False)),
        })

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "matched": matched,
        "blockers": blockers,
    }
