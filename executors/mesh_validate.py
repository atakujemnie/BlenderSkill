from __future__ import annotations

"""Candidate compact mesh validator for Blender asset agents.

No bpy.ops calls. Designed to return decision-grade summaries rather than
raw topology dumps.
"""

import math
from typing import Mapping

import bmesh


VALID_INTENTS = {"CLOSED_SOLID", "OPEN_ASSEMBLY_PART", "SURFACE_DETAIL", "COLLISION"}


def validate_mesh_object(obj, *, topology_intent: str, duplicate_digits: int = 6) -> dict:
    if obj.type != "MESH":
        raise TypeError(f"{obj.name} is not a MESH object")
    if topology_intent not in VALID_INTENTS:
        raise ValueError(f"topology_intent must be one of {sorted(VALID_INTENTS)}")

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    try:
        boundary_edges = sum(1 for e in bm.edges if e.is_boundary)
        non_manifold_edges = sum(1 for e in bm.edges if not e.is_manifold)
        loose_vertices = sum(1 for v in bm.verts if not v.link_edges)
        loose_edges = sum(1 for e in bm.edges if not e.link_faces)
        zero_area_faces = sum(1 for f in bm.faces if f.calc_area() <= 1e-12)

        seen = set()
        duplicate_vertices = 0
        for v in bm.verts:
            key = tuple(round(float(c), duplicate_digits) for c in v.co)
            if key in seen:
                duplicate_vertices += 1
            else:
                seen.add(key)

        tris = sum(max(0, len(f.verts) - 2) for f in bm.faces)
        reasons = []

        if topology_intent in {"CLOSED_SOLID", "COLLISION"}:
            if boundary_edges:
                reasons.append("CLOSED_MESH_HAS_BOUNDARY_EDGES")
            if non_manifold_edges:
                reasons.append("CLOSED_MESH_HAS_NON_MANIFOLD_EDGES")

        if loose_vertices:
            reasons.append("LOOSE_VERTICES")
        if loose_edges:
            reasons.append("LOOSE_EDGES")
        if zero_area_faces:
            reasons.append("ZERO_AREA_FACES")
        if duplicate_vertices:
            reasons.append("DUPLICATE_VERTEX_POSITIONS")

        return {
            "object": obj.name,
            "topology_intent": topology_intent,
            "status": "FAIL" if reasons else "PASS",
            "verts": len(bm.verts),
            "edges": len(bm.edges),
            "faces": len(bm.faces),
            "tris": tris,
            "boundary_edges": boundary_edges,
            "non_manifold_edges": non_manifold_edges,
            "loose_vertices": loose_vertices,
            "loose_edges": loose_edges,
            "duplicate_vertices": duplicate_vertices,
            "zero_area_faces": zero_area_faces,
            "uv_present": bool(obj.data.uv_layers),
            "material_slots": len(obj.data.materials),
            "reasons": reasons,
        }
    finally:
        bm.free()


def validate_collection(collection, topology_contract: Mapping[str, str]) -> dict:
    reports = []
    missing_contract = []
    total_tris = 0

    for obj in collection.objects:
        if obj.type != "MESH":
            continue
        intent = topology_contract.get(obj.name)
        if intent is None:
            missing_contract.append(obj.name)
            continue
        rep = validate_mesh_object(obj, topology_intent=intent)
        reports.append(rep)
        total_tris += rep["tris"]

    failed = [r["object"] for r in reports if r["status"] == "FAIL"]
    if missing_contract:
        failed.extend(missing_contract)

    return {
        "collection": collection.name,
        "status": "FAIL" if failed else "PASS",
        "objects_checked": len(reports),
        "total_tris": total_tris,
        "failed_objects": failed,
        "missing_topology_contract": missing_contract,
        "objects": reports,
    }
