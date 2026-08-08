# Mesh Validation Snippets

## Negative scale

```python
bad = []
for obj in bpy.context.scene.objects:
    if obj.type == "MESH":
        if any(s < 0 for s in obj.scale):
            bad.append(obj.name)
print("Negative scale:", bad)
```

## Zero scale

```python
bad = []
for obj in bpy.context.scene.objects:
    if any(abs(s) < 1e-8 for s in obj.scale):
        bad.append(obj.name)
print("Zero scale:", bad)
```

## Duplicate final names heuristic

```python
import re
suspicious = [
    o.name for o in bpy.data.objects
    if re.search(r"\.\d{3}$", o.name)
]
print("Suffix names:", suspicious)
```

## BMesh manifold audit

```python
import bpy, bmesh

def mesh_report(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    try:
        non_manifold_edges = [e for e in bm.edges if not e.is_manifold]
        boundary_edges = [e for e in bm.edges if e.is_boundary]
        return {
            "verts": len(bm.verts),
            "edges": len(bm.edges),
            "faces": len(bm.faces),
            "non_manifold_edges": len(non_manifold_edges),
            "boundary_edges": len(boundary_edges),
        }
    finally:
        bm.free()
```

Uwaga:
otwarte siatki mogą mieć poprawne boundary edges.
Walidator nie powinien oznaczać każdego boundary jako błąd bez znajomości kontraktu.
