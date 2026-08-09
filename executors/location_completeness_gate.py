from __future__ import annotations

from typing import Any

REQUIRED_GATES = [
    "scene_graph",
    "design_system",
    "asset_manifest",
    "architecture",
    "spatial_relations",
    "clearance",
    "reference_fidelity",
]


def evaluate_location_completeness(evidence: dict[str, Any], *, final: bool = True) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    for gate in REQUIRED_GATES:
        value = evidence.get(gate)
        status = value.get("status") if isinstance(value, dict) else value
        if status != "PASS":
            blockers.append({"code": "REQUIRED_GATE_NOT_PASS", "gate": gate, "status": status})
    proxies = int(evidence.get("proxy_count", 0))
    missing_hero = int(evidence.get("missing_hero_count", 0))
    penetrations = int(evidence.get("unintended_penetration_count", 0))
    blocked_paths = int(evidence.get("blocked_required_path_count", 0))
    if final and proxies:
        blockers.append({"code": "PROXY_PRESENT", "count": proxies})
    if missing_hero:
        blockers.append({"code": "MISSING_HERO_ASSET", "count": missing_hero})
    if penetrations:
        blockers.append({"code": "UNINTENDED_INTERPENETRATION", "count": penetrations})
    if blocked_paths:
        blockers.append({"code": "BLOCKED_REQUIRED_CIRCULATION", "count": blocked_paths})
    return {
        "validator_id": "LOCATION_COMPLETENESS_GATE",
        "status": "PASS" if not blockers else "FAIL",
        "blockers": blockers,
    }
