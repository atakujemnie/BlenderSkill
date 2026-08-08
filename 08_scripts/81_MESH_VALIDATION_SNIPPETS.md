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

## Topology intent rule

Otwarte siatki mogą mieć poprawne boundary edges, ale tylko wtedy, gdy kontrakt obiektu jawnie na to pozwala.

Każdy mesh przechodzący finalną walidację musi mieć topology intent:

```text
CLOSED_SOLID
OPEN_ASSEMBLY_PART
SURFACE_DETAIL
COLLISION
```

`CLOSED_SOLID` i domyślnie `COLLISION` wymagają:
- `boundary_edges == 0`;
- `non_manifold_edges == 0`;
- brak loose geometry;
- brak zero-area faces;
- brak nieuzasadnionych duplicate vertex positions.

`OPEN_ASSEMBLY_PART` może mieć boundary tylko wtedy, gdy boundary jest świadomie zakrywane/zamykane przez inny element assembly i taka polityka jest zapisana w Game Asset Contract.

`SURFACE_DETAIL` może być otwartą geometrią, ale wymaga osobnego testu widoczności/occlusion i z-fighting.

Walidator nie może powiedzieć ogólnie `all mesh checks pass`, jeśli boundary istnieją, a topology intent nie został określony.

## Canonical validator

Preferuj semantic skill `MESH_VALIDATE`:
- contract: `08_scripts/92_MESH_CONTRACT_VALIDATOR_PATTERN.md`;
- candidate executor: `executors/mesh_validate.py`.

Zwracaj compact report, nie listę wszystkich krawędzi/wierzchołków, chyba że DIAGNOSTIC wymaga konkretnego failing region.
