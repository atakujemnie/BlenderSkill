# Game Asset Contract

Każdy asset przed finalizacją powinien posiadać kontrakt runtime.

## Completion target

Declare during CONTRACT/PLAN:

```yaml
target_completion_level: GAME_READY_COMPLETE
```

Allowed values:
- `RECONSTRUCTION_COMPLETE`;
- `MODELING_COMPLETE`;
- `GAME_READY_COMPLETE`;
- `PIPELINE_INTEGRATED`.

Use `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md`.

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
- procedural authoring effects:
- runtime disposition per procedural effect (`BAKE` / `RECREATE_IN_ENGINE` / `EXPORT_NATIVELY_VERIFIED` / `REMOVE_BY_DESIGN`):

## Texture / bake contract
- bake required:
- BaseColor output:
- Normal output:
- ORM / packed channels:
- Emissive output:
- alpha/masks:
- padding/mip policy:
- high-to-low source required for which channels/features:
- runtime material binding validator:

A separate high-poly source is not required for every procedural-to-texture bake. Declare it only where geometry-detail transfer requires it.

Use `04_game_ready/50_GAME_READY_BAKE_GATE.md`.

## Emissive contract
- emitter feature IDs:
- geometry/mask authoring owner:
- Blender lookdev strength:
- exported emissive data:
- runtime bloom responsibility:
- runtime exposure/tone-mapping responsibility:
- actual scene-light contribution required:

Do not merge `emissive authoring PASS` with `runtime glow PASS`.
Use `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md`.

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
- post-export material/texture reference validation:

## Project integration
- stable asset ID:
- destination namespace/path:
- catalog/registry required:
- catalog write capability:
- existing-asset conflict policy:
- importer/instantiation smoke test:

Use `09_engine/93_ASSET_CATALOG_INTEGRATION_PROTOCOL.md` when Level D is requested.

## Edytowalność

Źródłowy `.blend` nie powinien być tym samym, czym finalna "spłaszczona" wersja export.
Zachowaj authoring source.

## Completion rule

Successful glTF/mesh export alone does not prove `GAME_READY_COMPLETE`.

Before final claim run:
- mesh validation;
- bake/runtime material gate;
- emissive handoff gate if applicable;
- export validation;
- completion-level evaluation;
- catalog integration when Level D is required.
