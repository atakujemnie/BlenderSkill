# Game Asset Contract

Każdy asset przed finalizacją powinien posiadać kontrakt runtime.

## Geometry
- target triangles:
- max triangles:
- LOD count:
- deformation:
- backface assumptions:
- hidden geometry policy:
- per-object topology intent:

### Per-object topology intent

Każdy render/collision mesh deklaruje:

```text
CLOSED_SOLID
OPEN_ASSEMBLY_PART
SURFACE_DETAIL
COLLISION
```

Przykład:

```yaml
topology_contract:
  BOL_BasePlate: CLOSED_SOLID
  BOL_MainBody: OPEN_ASSEMBLY_PART
  BOL_ServicePanel: SURFACE_DETAIL
  COL_ACS_Bollard: COLLISION
```

`OPEN_ASSEMBLY_PART` wymaga zapisania, co zamyka/zasłania otwarte boundary i dlaczego runtime/backface policy to dopuszcza.

Nie można używać `OPEN_ASSEMBLY_PART` jako automatycznego obejścia błędu non-manifold.

`SURFACE_DETAIL` wymaga testu widoczności oraz braku niepożądanego z-fighting/occlusion.

Finalny validator: semantic skill `MESH_VALIDATE`.

## Materials
- max material slots:
- shader model:
- transparency:
- alpha mode:
- emissive:
- normal map:
- texture resolution:
- compression target:

## Transform
- units:
- forward axis:
- up axis:
- pivot:
- applied transforms policy:

## Runtime
- static / movable:
- instanced:
- collision:
- occlusion:
- navmesh interaction:
- lightmap:
- shadow:
- animation:

## Export
- format:
- object root:
- naming:
- animation clips:
- external textures / embedded:
- validator:

## Edytowalność

Źródłowy `.blend` nie powinien być tym samym, czym finalna "spłaszczona" wersja export.
Zachowaj authoring source.
