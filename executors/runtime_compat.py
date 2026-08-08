from __future__ import annotations

"""Compact Blender runtime capability/compatibility helpers.

Designed for Blender-agent preflight. No bpy.ops calls and no scene mutation
except the explicit choose_render_engine() helper.
"""

import os
from typing import Iterable, Optional, Sequence

import bpy


def blender_version() -> tuple[int, int, int]:
    return tuple(int(v) for v in bpy.app.version[:3])


def available_render_engines(scene=None) -> list[str]:
    scene = scene or bpy.context.scene
    prop = scene.render.bl_rna.properties.get("engine")
    if prop is None:
        return []
    return list(prop.enum_items.keys())


def choose_render_engine(
    scene=None,
    preferred: Sequence[str] = ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"),
) -> dict:
    scene = scene or bpy.context.scene
    available = available_render_engines(scene)
    selected = next((name for name in preferred if name in available), None)
    if selected is None:
        return {
            "status": "FAIL",
            "reason": "NO_PREFERRED_RENDER_ENGINE_AVAILABLE",
            "available": available,
        }
    scene.render.engine = selected
    return {"status": "PASS", "selected": selected, "available": available}


def mesh_shading_capabilities(mesh=None) -> dict:
    return {
        "mesh_use_auto_smooth": bool(mesh is not None and hasattr(mesh, "use_auto_smooth")),
        "edge_sharp_flag": True,
    }


def material_node_capabilities(material=None) -> dict:
    return {
        "material_has_node_tree": bool(material is not None and material.node_tree is not None),
        "material_has_use_nodes": bool(material is not None and hasattr(material, "use_nodes")),
    }


def resolve_project_root(
    *,
    explicit_root: Optional[str] = None,
    script_file: Optional[str] = None,
    blend_path: Optional[str] = None,
    markers: Sequence[str] = (".git", "GameAssets"),
    max_parents: int = 10,
) -> dict:
    """Resolve a stable project root without trusting an unsaved blend path.

    Candidate precedence:
      explicit_root > script_file directory > blend_path directory > cwd
    A candidate is accepted when it or one of its parents contains at least
    one configured marker.
    """
    candidates: list[tuple[str, str]] = []
    if explicit_root:
        candidates.append(("EXPLICIT", explicit_root))
    if script_file:
        candidates.append(("SCRIPT_FILE", os.path.dirname(os.path.abspath(script_file))))
    if blend_path:
        candidates.append(("BLEND_FILE", os.path.dirname(os.path.abspath(blend_path))))
    elif bpy.data.filepath:
        candidates.append(("BLEND_FILE", os.path.dirname(os.path.abspath(bpy.data.filepath))))
    candidates.append(("CWD", os.getcwd()))

    checked = []
    for source, start in candidates:
        probe = os.path.abspath(start)
        for _ in range(max_parents + 1):
            found = [m for m in markers if os.path.exists(os.path.join(probe, m))]
            checked.append((source, probe, found))
            if found:
                return {
                    "status": "PASS",
                    "root": probe,
                    "source": source,
                    "markers": found,
                    "blend_saved": bool(bpy.data.filepath),
                }
            parent = os.path.dirname(probe)
            if parent == probe:
                break
            probe = parent

    return {
        "status": "FAIL",
        "reason": "PROJECT_ROOT_MARKER_NOT_FOUND",
        "blend_saved": bool(bpy.data.filepath),
        "checked_candidates": len(checked),
    }


def discover_runtime(scene=None) -> dict:
    scene = scene or bpy.context.scene
    return {
        "status": "PASS",
        "blender_version": blender_version(),
        "render_engines": available_render_engines(scene),
        "blend_saved": bool(bpy.data.filepath),
        "blend_path": bpy.data.filepath or None,
        "gltf_export_operator_present": bool(
            hasattr(bpy.ops, "export_scene") and hasattr(bpy.ops.export_scene, "gltf")
        ),
    }
