from __future__ import annotations

from typing import Any

from executors.provider_probes._shared import blender_version, provider_version, remove_new_ids, resolve_operator, result, snapshot_ids


def run(provider: dict[str, Any]) -> dict[str, Any]:
    try:
        import bpy  # type: ignore
    except Exception as exc:
        return result("ant_landscape", "BLOCKED", blockers=[{"reason": "BLENDER_RUNTIME_REQUIRED", "error": str(exc)}])
    operator = resolve_operator(bpy, "mesh.landscape_add")
    if operator is None:
        return result("ant_landscape", "BLOCKED", blender_version=blender_version(bpy), provider_version=provider_version(provider), blockers=[{"reason": "EXPECTED_API_NOT_AVAILABLE", "api": "bpy.ops.mesh.landscape_add"}])
    before = snapshot_ids(bpy)
    blockers: list[dict[str, Any]] = []
    state = "FAIL"
    try:
        operator(subdivision_x=8, subdivision_y=8, mesh_size=2.0)
        created = [o for o in bpy.data.objects if o.name not in before[0]]
        if created and any(o.type == "MESH" and len(o.data.vertices) > 0 for o in created):
            state = "PASS"
        else:
            blockers.append({"reason": "EXPECTED_TERRAIN_OUTPUT_MISSING"})
    except RuntimeError as exc:
        state = "BLOCKED"
        blockers.append({"reason": "UI_CONTEXT_REQUIRED", "error": str(exc)})
    except Exception as exc:
        blockers.append({"reason": "ANT_LANDSCAPE_PROBE_EXCEPTION", "error": str(exc)})
    clean = remove_new_ids(bpy, before)
    if not clean:
        state = "FAIL"
        blockers.append({"reason": "PROBE_CLEANUP_FAILED"})
    return result("ant_landscape", state, capabilities=["TERRAIN"] if state == "PASS" else [], cleanup_state="PASS" if clean else "FAIL", side_effects_detected=not clean, blockers=blockers, blender_version=blender_version(bpy), provider_version=provider_version(provider))
