from __future__ import annotations

from typing import Any

from executors.provider_probes._shared import blender_version, provider_version, remove_new_ids, result, snapshot_ids


def run(provider: dict[str, Any]) -> dict[str, Any]:
    try:
        import bpy  # type: ignore
    except Exception as exc:
        return result("sverchok", "BLOCKED", blockers=[{"reason": "BLENDER_RUNTIME_REQUIRED", "error": str(exc)}])
    before = snapshot_ids(bpy)
    blockers: list[dict[str, Any]] = []
    state = "FAIL"
    tree = None
    try:
        tree = bpy.data.node_groups.new("__BLENDERSKILL_SVERCHOK_PROBE__", "SverchCustomTreeType")
        if tree.bl_idname == "SverchCustomTreeType":
            state = "PASS"
        else:
            blockers.append({"reason": "SVERCHOK_NODE_TREE_TYPE_MISMATCH"})
    except Exception as exc:
        state = "BLOCKED"
        blockers.append({"reason": "SVERCHOK_API_UNAVAILABLE", "error": str(exc)})
    clean = remove_new_ids(bpy, before)
    if not clean:
        state = "FAIL"
        blockers.append({"reason": "PROBE_CLEANUP_FAILED"})
    return result("sverchok", state, capabilities=["PARAMETRIC_GEOMETRY", "GENERIC_PROCEDURAL"] if state == "PASS" else [], cleanup_state="PASS" if clean else "FAIL", side_effects_detected=not clean, blockers=blockers, blender_version=blender_version(bpy), provider_version=provider_version(provider))
