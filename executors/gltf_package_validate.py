from __future__ import annotations

"""Pure-Python validator for glTF JSON package contracts.

Besides package naming/readback, v0.8 can validate primitive attributes and
node transform policy. This closes two silent runtime classes observed in the
Lafar Wayfinding Pylon benchmark: a package that loads with no ``TEXCOORD_0``
and a loader/test that measures local vertices while silently ignoring node
TRS.
"""

import json
from pathlib import Path
from typing import Iterable


IDENTITY_MATRIX = [
    1.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 1.0,
]


def _near(a, b, tol: float = 1e-6) -> bool:
    return abs(float(a) - float(b)) <= tol


def _sequence_near(value, expected, tol: float = 1e-6) -> bool:
    if len(value) != len(expected):
        return False
    return all(_near(a, b, tol) for a, b in zip(value, expected))


def _node_has_identity_transform(node: dict, tol: float = 1e-6) -> bool:
    if "matrix" in node and not _sequence_near(node["matrix"], IDENTITY_MATRIX, tol):
        return False
    if "translation" in node and not _sequence_near(node["translation"], [0.0, 0.0, 0.0], tol):
        return False
    if "rotation" in node and not _sequence_near(node["rotation"], [0.0, 0.0, 0.0, 1.0], tol):
        return False
    if "scale" in node and not _sequence_near(node["scale"], [1.0, 1.0, 1.0], tol):
        return False
    return True


def validate_gltf_package(
    path,
    *,
    expected_nodes: Iterable[str] = (),
    expected_materials: Iterable[str] = (),
    expected_images: Iterable[str] = (),
    required_attributes: Iterable[str] = (),
    attribute_nodes: Iterable[str] = (),
    identity_trs_nodes: Iterable[str] = (),
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

    node_list = list(doc.get("nodes", []))
    node_by_name = {str(n.get("name", "")): n for n in node_list}
    nodes = set(node_by_name)
    materials = {str(m.get("name", "")) for m in doc.get("materials", [])}
    images = {str(i.get("uri", "")) for i in doc.get("images", [])}

    exp_nodes = {str(x) for x in expected_nodes}
    exp_mats = {str(x) for x in expected_materials}
    exp_images = {str(x) for x in expected_images}
    req_attrs = {str(x) for x in required_attributes}
    attr_nodes = {str(x) for x in attribute_nodes}
    identity_nodes = {str(x) for x in identity_trs_nodes}

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

    # Primitive-attribute validation. If caller requests attributes but does
    # not specify a node subset, validate expected nodes when present, else all
    # mesh-bearing nodes.
    missing_attributes: list[dict] = []
    if req_attrs:
        target_names = attr_nodes or exp_nodes
        if not target_names:
            target_names = {
                name for name, node in node_by_name.items() if "mesh" in node
            }

        meshes = list(doc.get("meshes", []))
        for node_name in sorted(target_names):
            node = node_by_name.get(node_name)
            if node is None:
                continue
            mesh_index = node.get("mesh")
            if mesh_index is None or not (0 <= int(mesh_index) < len(meshes)):
                missing_attributes.append(
                    {
                        "node": node_name,
                        "primitive": None,
                        "missing": sorted(req_attrs),
                        "reason": "NODE_HAS_NO_VALID_MESH",
                    }
                )
                continue

            primitives = list(meshes[int(mesh_index)].get("primitives", []))
            if not primitives:
                missing_attributes.append(
                    {
                        "node": node_name,
                        "primitive": None,
                        "missing": sorted(req_attrs),
                        "reason": "MESH_HAS_NO_PRIMITIVES",
                    }
                )
                continue

            for primitive_index, primitive in enumerate(primitives):
                attrs = {str(k) for k in dict(primitive.get("attributes", {}))}
                missing = sorted(req_attrs - attrs)
                if missing:
                    missing_attributes.append(
                        {
                            "node": node_name,
                            "primitive": primitive_index,
                            "missing": missing,
                            "reason": "MISSING_PRIMITIVE_ATTRIBUTES",
                        }
                    )

    if missing_attributes:
        reasons.append("MISSING_PRIMITIVE_ATTRIBUTES")

    non_identity_nodes: list[dict] = []
    for node_name in sorted(identity_nodes):
        node = node_by_name.get(node_name)
        if node is None:
            continue
        if not _node_has_identity_transform(node):
            non_identity_nodes.append(
                {
                    "node": node_name,
                    "translation": node.get("translation"),
                    "rotation": node.get("rotation"),
                    "scale": node.get("scale"),
                    "matrix": node.get("matrix"),
                }
            )

    if non_identity_nodes:
        reasons.append("NON_IDENTITY_NODE_TRANSFORM")

    return {
        "status": "FAIL" if reasons else "PASS",
        "path": str(p),
        "node_count": len(nodes),
        "material_count": len(materials),
        "image_count": len(images),
        "missing_nodes": missing_nodes,
        "missing_materials": missing_materials,
        "missing_images": missing_images,
        "required_attributes": sorted(req_attrs),
        "missing_attributes": missing_attributes,
        "identity_trs_nodes": sorted(identity_nodes),
        "non_identity_nodes": non_identity_nodes,
        "nodes": sorted(nodes),
        "materials": sorted(materials),
        "images": sorted(images),
        "reasons": reasons,
    }


def expected_lod_nodes(prefix: str, lod_count: int) -> list[str]:
    if lod_count < 1:
        raise ValueError("lod_count must be >= 1")
    return [f"{prefix}_LOD{i}" for i in range(lod_count)]
