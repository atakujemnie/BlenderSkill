from __future__ import annotations

"""Contract-aware mesh validator with v0.12 topology-risk classification."""

import math
from typing import Mapping

import bmesh

VALID_INTENTS = {"CLOSED_SOLID", "OPEN_ASSEMBLY_PART", "SURFACE_DETAIL", "COLLISION"}


def _project_face(face):
    n = face.normal
    axis = max(range(3), key=lambda i: abs(float(n[i])))
    pts = []
    for v in face.verts:
        co = v.co
        if axis == 0: pts.append((float(co.y), float(co.z)))
        elif axis == 1: pts.append((float(co.x), float(co.z)))
        else: pts.append((float(co.x), float(co.y)))
    return pts


def _concave(face, eps: float = 1e-10) -> bool:
    pts = _project_face(face)
    if len(pts) < 4:
        return False
    signs = set()
    n = len(pts)
    for i in range(n):
        ax, ay = pts[i - 1]
        bx, by = pts[i]
        cx, cy = pts[(i + 1) % n]
        cross = (bx - ax) * (cy - by) - (by - ay) * (cx - bx)
        if abs(cross) > eps:
            signs.add(1 if cross > 0 else -1)
    return len(signs) > 1


def _planarity_error(face) -> float:
    if len(face.verts) <= 3:
        return 0.0
    n = face.normal.normalized()
    p0 = face.verts[0].co
    return max(abs(float((v.co - p0).dot(n))) for v in face.verts)


def validate_mesh_object(obj, *, topology_intent: str, duplicate_digits: int = 6,
                         non_planar_ngon_tolerance: float = 1e-5,
                         reject_concave_ngons: bool = False,
                         max_ngon_vertices: int | None = None) -> dict:
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

        seen = set(); duplicate_vertices = 0
        for v in bm.verts:
            key = tuple(round(float(c), duplicate_digits) for c in v.co)
            if key in seen: duplicate_vertices += 1
            else: seen.add(key)

        ngons = [f for f in bm.faces if len(f.verts) > 4]
        ngons_gt6 = sum(1 for f in bm.faces if len(f.verts) > 6)
        non_planar_ngons = sum(1 for f in ngons if _planarity_error(f) > float(non_planar_ngon_tolerance))
        concave_ngons = sum(1 for f in ngons if _concave(f))
        oversized_ngons = 0 if max_ngon_vertices is None else sum(1 for f in ngons if len(f.verts) > max_ngon_vertices)

        tris = sum(max(0, len(f.verts) - 2) for f in bm.faces)
        closed = boundary_edges == 0 and non_manifold_edges == 0 and bool(bm.faces)
        signed_volume = None
        if closed:
            try:
                signed_volume = float(bm.calc_volume(signed=True))
            except Exception:
                signed_volume = None

        reasons = []
        warnings = []
        if topology_intent in {"CLOSED_SOLID", "COLLISION"}:
            if boundary_edges: reasons.append("CLOSED_MESH_HAS_BOUNDARY_EDGES")
            if non_manifold_edges: reasons.append("CLOSED_MESH_HAS_NON_MANIFOLD_EDGES")
            if signed_volume is not None and signed_volume < -1e-12:
                reasons.append("INVERTED_CLOSED_VOLUME")
        if loose_vertices: reasons.append("LOOSE_VERTICES")
        if loose_edges: reasons.append("LOOSE_EDGES")
        if zero_area_faces: reasons.append("ZERO_AREA_FACES")
        if duplicate_vertices: reasons.append("DUPLICATE_VERTEX_POSITIONS")
        if non_planar_ngons: reasons.append("NON_PLANAR_NGONS")
        if oversized_ngons: reasons.append("NGON_VERTEX_LIMIT_EXCEEDED")
        if concave_ngons:
            if reject_concave_ngons: reasons.append("CONCAVE_NGONS")
            else: warnings.append("CONCAVE_NGONS_REQUIRE_TRIANGULATION_REVIEW")
        if ngons_gt6:
            warnings.append("HIGH_ORDER_NGONS_PRESENT")

        return {
            "object": obj.name, "topology_intent": topology_intent,
            "status": "FAIL" if reasons else "PASS",
            "verts": len(bm.verts), "edges": len(bm.edges), "faces": len(bm.faces), "tris": tris,
            "boundary_edges": boundary_edges, "non_manifold_edges": non_manifold_edges,
            "loose_vertices": loose_vertices, "loose_edges": loose_edges,
            "duplicate_vertices": duplicate_vertices, "zero_area_faces": zero_area_faces,
            "ngons": len(ngons), "ngons_gt6": ngons_gt6,
            "non_planar_ngons": non_planar_ngons, "concave_ngons": concave_ngons,
            "signed_volume": signed_volume,
            "uv_present": bool(obj.data.uv_layers), "material_slots": len(obj.data.materials),
            "reasons": reasons, "warnings": warnings,
        }
    finally:
        bm.free()


def validate_collection(collection, topology_contract: Mapping[str, str]) -> dict:
    reports = []; missing_contract = []; total_tris = 0
    for obj in collection.objects:
        if obj.type != "MESH": continue
        intent = topology_contract.get(obj.name)
        if intent is None:
            missing_contract.append(obj.name); continue
        rep = validate_mesh_object(obj, topology_intent=intent)
        reports.append(rep); total_tris += rep["tris"]
    failed = [r["object"] for r in reports if r["status"] == "FAIL"]
    if missing_contract: failed.extend(missing_contract)
    return {"collection": collection.name, "status": "FAIL" if failed else "PASS",
            "objects_checked": len(reports), "total_tris": total_tris,
            "failed_objects": failed, "missing_topology_contract": missing_contract,
            "objects": reports}
