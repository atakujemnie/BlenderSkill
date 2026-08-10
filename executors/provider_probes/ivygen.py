from __future__ import annotations

from typing import Any

from executors.provider_probes._shared import blender_version, provider_version, remove_new_ids, resolve_operator, result, snapshot_ids


def run(provider: dict[str, Any]) -> dict[str, Any]:
    try:
        import bpy  # type: ignore
    except Exception as exc:
        return result("ivygen", "BLOCKED", blockers=[{"reason": "BLENDER_RUNTIME_REQUIRED", "error": str(exc)}])
    operator = resolve_operator(bpy, "curve.ivy_gen") or resolve_operator(bpy, "curve.ivygen")
    if operator is None:
        return result("ivygen", "BLOCKED", blender_version=blender_version(bpy), provider_version=provider_version(provider), blockers=[{"reason": "EXPECTED_API_NOT_AVAILABLE", "apis": ["bpy.ops.curve.ivy_gen", "bpy.ops.curve.ivygen"]}])
    before = snapshot_ids(bpy)
    blockers: list[dict[str, Any]] = []
    state = "BLOCKED"
    source_mesh = source_object = None
    try:
        source_mesh = bpy.data.meshes.new("__BLENDERSKILL_IVY_SOURCE__")
        source_mesh.from_pydata([(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)], [], [(0, 1, 2, 3)])
        source_object = bpy.data.objects.new("__BLENDERSKILL_IVY_SOURCE__", source_mesh)
        bpy.context.scene.collection.objects.link(source_object)
        bpy.context.view_layer.objects.active = source_object
        source_object.select_set(True)
        try:
            operator()
            created = [o for o in bpy.data.objects if o.name not in before[0] and o != source_object]
            state = "PASS" if created else "FAIL"
            if not created:
                blockers.append({"reason": "EXPECTED_IVY_OUTPUT_MISSING"})
        except RuntimeError as exc:
            blockers.append({"reason": "UI_CONTEXT_REQUIRED", "error": str(exc)})
    except Exception as exc:
        state = "FAIL"
        blockers.append({"reason": "IVYGEN_PROBE_EXCEPTION", "error": str(exc)})
    clean = remove_new_ids(bpy, before)
    if not clean:
        state = "FAIL"
        blockers.append({"reason": "PROBE_CLEANUP_FAILED"})
    return result("ivygen", state, capabilities=["VINE", "SURFACE_GROWTH"] if state == "PASS" else [], cleanup_state="PASS" if clean else "FAIL", side_effects_detected=not clean, blockers=blockers, blender_version=blender_version(bpy), provider_version=provider_version(provider))
