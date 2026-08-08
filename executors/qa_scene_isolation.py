from __future__ import annotations

"""Non-destructive render-isolation helper for Blender QA.

Prevents unrelated scene objects from contaminating QA renders while
restoring their exact hide_render state afterward.
"""

from contextlib import contextmanager
from typing import Iterable, Iterator

import bpy


def object_names_from_collections(collection_names: Iterable[str]) -> set[str]:
    keep: set[str] = set()
    for name in collection_names:
        col = bpy.data.collections.get(name)
        if col is not None:
            keep.update(obj.name for obj in col.all_objects)
    return keep


@contextmanager
def render_isolation(
    *,
    keep_object_names: Iterable[str] = (),
    keep_collection_names: Iterable[str] = (),
    scene=None,
) -> Iterator[dict]:
    """Temporarily hide every non-kept scene object from renders.

    The helper only changes ``hide_render`` and restores all saved values in
    ``finally``. It never deletes unrelated objects.
    """
    scene = scene or bpy.context.scene
    keep = set(keep_object_names)
    keep.update(object_names_from_collections(keep_collection_names))

    saved: dict[str, bool] = {}
    changed = 0
    for obj in scene.objects:
        if obj.name in keep:
            continue
        saved[obj.name] = bool(obj.hide_render)
        if not obj.hide_render:
            obj.hide_render = True
            changed += 1

    report = {
        "status": "ACTIVE",
        "kept_objects": len(keep),
        "objects_state_saved": len(saved),
        "objects_hidden_for_render": changed,
    }

    try:
        yield report
    finally:
        restored = 0
        for name, state in saved.items():
            obj = bpy.data.objects.get(name)
            if obj is not None:
                obj.hide_render = state
                restored += 1
        report["status"] = "RESTORED"
        report["objects_restored"] = restored
