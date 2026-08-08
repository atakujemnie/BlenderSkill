# Final Validation

Final Validation must prove the requested completion level, not only that the Blender scene renders.

Use `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md` and finish with `05_execution/63_REFERENCE_TO_RUNTIME_COMPLETENESS_REPORT.md`.

## Visual / reconstruction

- [ ] silhouette matches
- [ ] proportions within tolerance
- [ ] all MUST features visible
- [ ] no invented major details
- [ ] no missing characteristic recess/groove/cut
- [ ] material regions match design
- [ ] asymmetry preserved where required
- [ ] floating/additive features are actually visible and not hidden by host geometry
- [ ] lighting/material readability did not force unauthorized geometry changes

## Mesh

- [ ] every mesh has declared topology intent
- [ ] `MESH_VALIDATE` or equivalent contract-aware audit passes
- [ ] no unintended duplicate geometry
- [ ] boundary/non-manifold state matches topology intent
- [ ] face normals correct
- [ ] no accidental zero-area geometry
- [ ] no loose vertices/edges
- [ ] no uncontrolled shading artifacts
- [ ] triangle count documented

## Modifiers / generated code

- [ ] stack intentional
- [ ] no disabled forgotten modifiers
- [ ] no accidental duplicate modifiers
- [ ] apply state follows pipeline
- [ ] reusable builder modules have no destructive import-time side effects
- [ ] generated code is persisted as an artifact, not dependent on conversation reconstruction

## UV / material authoring

- [ ] UV layers named
- [ ] overlap intentional
- [ ] texel density acceptable
- [ ] material slots within budget
- [ ] supplied authoritative branding source used where required
- [ ] material breakup follows material/manufacturing logic rather than uniform generic noise
- [ ] dark/civic materials are checked for sterile-uniform and over-grunged failure modes

## Bake / runtime texture gate

Required for Level C when runtime textures are part of the contract:

- [ ] every Blender-only procedural effect has runtime disposition
- [ ] required BaseColor exists
- [ ] required Normal exists
- [ ] required ORM/packed map exists
- [ ] required Emissive exists
- [ ] padding/mip safety passes
- [ ] tangent/normal transfer is correct
- [ ] packed channels match Engine Profile
- [ ] exported runtime material actually references produced textures

Use `04_game_ready/50_GAME_READY_BAKE_GATE.md`.

A separate high-poly mesh is required only for transfers that actually need a high-detail source.

## Emissive

If emissive features exist:

- [ ] emitter geometry/mask is correct
- [ ] emitter visibility passes
- [ ] intended hue survives Blender lookdev
- [ ] exported emissive data survives
- [ ] runtime bloom/exposure/tone-mapping responsibility is documented
- [ ] final runtime glow is PASS or explicitly `UNVERIFIED`

Use `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md`.

## Scene

- [ ] naming clean
- [ ] no Cube.001 style leftovers
- [ ] unrelated scene objects cannot contaminate QA renders
- [ ] helper objects hidden/removed according to policy
- [ ] collection structure clean
- [ ] pivot correct
- [ ] transforms correct
- [ ] project root/path source is stable even for unsaved `.blend` sessions

## Game-ready

- [ ] LOD budgets correct
- [ ] collision correct
- [ ] instancing/reuse considered
- [ ] runtime bounds correct
- [ ] export tested
- [ ] exported decal/material/texture references validated
- [ ] protected reconstruction features survive optimization

## Pipeline integration — Level D only

- [ ] stable project asset ID
- [ ] no unintended overwrite/name collision
- [ ] asset catalog/registry entry written
- [ ] LOD/collision/texture associations correct
- [ ] catalog entry read back successfully
- [ ] importer/instantiation smoke test passes when available

Use `09_engine/93_ASSET_CATALOG_INTEGRATION_PROTOCOL.md`.

## Deliverables

Depending on target level:

- [ ] source `.blend`
- [ ] build/code artifacts required for reproducibility
- [ ] runtime mesh export
- [ ] textures
- [ ] collision
- [ ] validation report
- [ ] completeness report
- [ ] catalog/registry integration record when Level D is required

## Final claim

Before saying `DONE`:
1. run `ASSET_COMPLETION`;
2. emit highest passed completion level;
3. list blockers/deferred items;
4. only use unconditional `DONE` if `TARGET_COMPLETION_LEVEL` passes.

Example:

```text
MODELING_COMPLETE: PASS
GAME_READY_COMPLETE: FAIL — PBR_BAKE_NOT_DONE
PIPELINE_INTEGRATED: NOT_REQUIRED
```

This is not a fully game-ready asset yet, even if the Blender model and glTF mesh look correct.
