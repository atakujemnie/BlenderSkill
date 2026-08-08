from __future__ import annotations

"""Blender image datablock/cache coherence helpers.

Candidate executor. Scene/image mutation is explicit; importing this module does
not reload or modify anything.
"""

from pathlib import Path
from typing import Optional

import bpy


def canonical_path(path) -> str:
    return str(Path(path).expanduser().resolve())


def image_absolute_path(image) -> Optional[str]:
    if image is None or not getattr(image, "filepath", ""):
        return None
    try:
        return canonical_path(bpy.path.abspath(image.filepath))
    except Exception:
        return canonical_path(image.filepath)


def find_external_image(path):
    """Find an existing Blender image by canonical external filepath."""
    target = canonical_path(path)
    for image in bpy.data.images:
        if image.source != "FILE":
            continue
        current = image_absolute_path(image)
        if current == target:
            return image
    return None


def load_disk_authoritative(
    path,
    *,
    image_name: str | None = None,
    colorspace: str | None = None,
    reload_existing: bool = True,
) -> tuple[object, dict]:
    """Load/synchronize an external texture whose disk file is authoritative.

    This function must not be used when unsaved in-memory pixels are the source
    of truth. Call only after the bake/image has been saved and accepted.
    """
    target = canonical_path(path)
    if not Path(target).is_file():
        raise FileNotFoundError(target)

    image = find_external_image(target)
    action = "REUSE"

    if image is None and image_name:
        candidate = bpy.data.images.get(image_name)
        if candidate is not None and candidate.source == "FILE":
            image = candidate

    if image is None:
        image = bpy.data.images.load(target, check_existing=False)
        action = "LOAD"
    else:
        image.filepath = target
        if reload_existing:
            image.reload()
            action = "RELOAD"

    if image_name:
        image.name = image_name
    if colorspace:
        image.colorspace_settings.name = colorspace

    image.update()
    width, height = int(image.size[0]), int(image.size[1])
    if width <= 0 or height <= 0:
        raise RuntimeError(f"IMAGE_LOAD_EMPTY: {target}")

    resolved = image_absolute_path(image)
    if resolved != target:
        raise RuntimeError(
            f"IMAGE_PATH_MISMATCH: expected={target!r} actual={resolved!r}"
        )

    report = {
        "status": "PASS",
        "action": action,
        "image": image.name,
        "path": target,
        "size": [width, height],
        "colorspace": image.colorspace_settings.name,
        "source": image.source,
    }
    return image, report


def binding_report(material, expected_images: dict[str, object]) -> dict:
    """Compactly verify named image texture nodes use expected datablocks."""
    if material is None or material.node_tree is None:
        return {
            "status": "FAIL",
            "reason": "MATERIAL_HAS_NO_NODE_TREE",
        }

    failures = []
    bound = {}
    for node_name, expected in expected_images.items():
        node = material.node_tree.nodes.get(node_name)
        if node is None or node.type != "TEX_IMAGE":
            failures.append({"node": node_name, "reason": "NODE_MISSING"})
            continue
        actual = node.image
        bound[node_name] = actual.name if actual else None
        if actual is not expected:
            failures.append({"node": node_name, "reason": "WRONG_IMAGE"})

    return {
        "status": "FAIL" if failures else "PASS",
        "material": material.name,
        "bound": bound,
        "failures": failures,
    }
