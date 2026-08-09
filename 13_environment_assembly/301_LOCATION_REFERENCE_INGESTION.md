# Location Reference Ingestion

## Goal

Turn a mixed folder of hero concepts, technical sheets and asset cards into a property-level authority map before building a complete location.

## Source classes

- `LOCATION_HERO` — global composition, focal hierarchy, density, mood and visible relationships;
- `ARCHITECTURAL_SHEET` — grid, dimensions, openings, wall/floor/ceiling systems;
- `ASSET_CARD` — individual object geometry, dimensions, materials and local pivots;
- `DESIGN_SYSTEM_SOURCE` — material, lighting, branding and reusable language;
- `DETAIL_REFERENCE` — local junction/finish evidence.

## Required output

```yaml
location_reference_registry:
  revision: ...
  sources: []
  authorities:
    footprint: ...
    wall_height: ...
    major_openings: ...
    hero_composition: ...
    focal_assets: ...
    material_language: ...
    lighting_language: ...
  conflicts: []
  unresolved: []
```

A hero render does not own printed dimensions. An asset card does not own room placement unless explicit.
