from __future__ import annotations

"""Pure-Python validator for glTF JSON package contracts."""

import json
from pathlib import Path
from typing import Iterable


def validate_gltf_package(
    path,
    *,
    expected_nodes: Iterable[str] = (),
    expected_materials: Iterable[str] = (),
    expected_images: Iterable[str] = (),
) -> dict:
    p = Path(path)
    if not p.exists():
        return {"status": "FAIL", "reasons": ["FILE_NOT_FOUND"], "path": str(p)}

    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "status": "FAIL",
            "reasons": ["INVALID_GLTF_JSON"],
            "error": str(exc),
            "path": str(p),
        }

    nodes = {str(n.get("name", "")) for n in doc.get("nodes", [])}
    materials = {str(m.get("name", "")) for m in doc.get("materials", [])}
    images = {str(i.get("uri", "")) for i in doc.get("images", [])}

    exp_nodes = {str(x) for x in expected_nodes}
    exp_mats = {str(x) for x in expected_materials}
    exp_images = {str(x) for x in expected_images}

    missing_nodes = sorted(exp_nodes - nodes)
    missing_materials = sorted(exp_mats - materials)
    missing_images = sorted(exp_images - images)

    reasons = []
    if missing_nodes:
        reasons.append("MISSING_NODES")
    if missing_materials:
        reasons.append("MISSING_MATERIALS")
    if missing_images:
        reasons.append("MISSING_IMAGES")

    return {
        "status": "FAIL" if reasons else "PASS",
        "path": str(p),
        "node_count": len(nodes),
        "material_count": len(materials),
        "image_count": len(images),
        "missing_nodes": missing_nodes,
        "missing_materials": missing_materials,
        "missing_images": missing_images,
        "nodes": sorted(nodes),
        "materials": sorted(materials),
        "images": sorted(images),
        "reasons": reasons,
    }


def expected_lod_nodes(prefix: str, lod_count: int) -> list[str]:
    if lod_count < 1:
        raise ValueError("lod_count must be >= 1")
    return [f"{prefix}_LOD{i}" for i in range(lod_count)]
