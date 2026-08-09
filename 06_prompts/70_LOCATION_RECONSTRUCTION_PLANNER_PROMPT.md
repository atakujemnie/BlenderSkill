# Location Reconstruction Planner Prompt v0.15

Use this prompt when the user asks to build a complete room, building interior, exterior block, street, plaza or other authored location from multiple references/assets.

## Required planning output before final geometry population

1. Resolve `location_id` and project profile.
2. Ingest all location-level references and classify authority.
3. Resolve/create the Location Design System and persistent material library.
4. Build Location Scene Graph.
5. Build exhaustive Location Asset Manifest with HERO/MID/BACKGROUND tier and `MISSING/PROXY/...` state.
6. Define zones and circulation paths.
7. Define architectural raster/envelope and module interfaces.
8. Define HERO anchors and spatial relations.
9. Define stage barriers and QA cameras.
10. Only then execute architecture and assets in dependency order.

## Forbidden shortcuts

- empty room + repeated generic chairs -> claim restaurant complete;
- use one proxy mesh as a final accepted asset;
- random furniture scatter for authored interior;
- skip bar/backbar/hero anchors because they are expensive;
- invent per-asset materials when a location design system exists;
- let a nice render override penetrations/clearance failures;
- start runtime optimization before final location fidelity.

## Required compact status

```yaml
location_build:
  location_id: ...
  stage: ...
  scene_graph: PASS|FAIL
  design_system: PASS|FAIL
  asset_coverage: ...
  hero_coverage: ...
  proxies: ...
  spatial_relations: PASS|FAIL
  clearance: PASS|FAIL
  reference_fidelity: PASS|FAIL
  completeness: PASS|FAIL
  blockers: []
```
