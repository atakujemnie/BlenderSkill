from __future__ import annotations

"""Hard reconstruction-fidelity transition gate.

Prevents runtime/LOD/export work from hiding unresolved reconstruction failures.
The caller supplies compact validator reports; this executor only aggregates
ownership/severity and decides whether R12+ may begin.
"""

from typing import Any, Mapping

EXECUTOR_ID = "RECON_FIDELITY_GATE"
EXECUTOR_VERSION = "0.1.0"

LEVELS = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}


def _status(item: Any) -> str:
    if isinstance(item, str):
        return item.upper()
    if isinstance(item, Mapping):
        return str(item.get("status", "UNVERIFIED")).upper()
    return "UNVERIFIED"


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    target = str(report.get("target_fidelity", "L3")).upper()
    achieved = str(report.get("achieved_fidelity", "L0")).upper()
    if target not in LEVELS or achieved not in LEVELS:
        raise ValueError("fidelity level must be L0..L5")

    blockers: list[dict[str, str]] = []

    required_single = {
        "hard_dimensions": report.get("hard_dimensions"),
        "landmarks_d0_d1": report.get("landmarks_d0_d1"),
        "material_segmentation": report.get("material_segmentation") if LEVELS[target] >= 4 else {"status": "PASS"},
    }
    for owner, value in required_single.items():
        st = _status(value)
        if st != "PASS":
            blockers.append({"owner": owner, "status": st, "reason": "required_gate_not_passed"})

    canonical = dict(report.get("canonical_views", {}))
    required_views = list(report.get("required_views", ["FRONT", "SIDE", "TOP", "REAR", "BOTTOM"]))
    for view in required_views:
        st = _status(canonical.get(view))
        if st != "PASS":
            blockers.append({"owner": f"view:{view}", "status": st, "reason": "canonical_view_not_passed"})

    for feature in list(report.get("must_features", [])):
        fid = str(feature.get("id", "UNKNOWN"))
        st = _status(feature)
        if st != "PASS":
            blockers.append({"owner": f"feature:{fid}", "status": st, "reason": "MUST_feature_not_passed"})

    for dev in list(report.get("deviations", [])):
        severity = str(dev.get("severity", "SOFT")).upper()
        st = str(dev.get("status", "OPEN")).upper()
        if severity in {"HARD", "MUST", "CANONICAL"} and st not in {"RESOLVED", "ACCEPTED_BY_AUTHORITY"}:
            blockers.append({"owner": f"deviation:{dev.get('id','UNKNOWN')}", "status": st, "reason": "unresolved_hard_deviation"})

    if LEVELS[achieved] < LEVELS[target]:
        blockers.append({"owner": "fidelity_level", "status": achieved, "reason": f"target_{target}_not_reached"})

    return {
        "status": "PASS" if not blockers else "FAIL",
        "target_fidelity": target,
        "achieved_fidelity": achieved,
        "blockers": blockers,
        "can_advance_to_runtime": not blockers,
        "next_state": "R12_TOPOLOGY_RUNTIME" if not blockers else "BACKTRACK_TO_EARLIEST_FIDELITY_OWNER",
    }
