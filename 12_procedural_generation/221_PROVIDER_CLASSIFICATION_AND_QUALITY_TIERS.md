# Provider Classification and Quality Tiers

## Separation

Runtime compatibility and visual suitability are independent.

```text
runtime_status: PASS
quality_tier: A | B | C | D | UNRATED
```

A provider may execute correctly and still be unsuitable for hero assets.

## Provider classes

- `GENERATOR_BACKEND` — Geometry Nodes, Sapling, Sverchok-like procedural systems;
- `ASSET_LIBRARY` — curated reusable vegetation/material/prop sources;
- `MATERIAL_LIBRARY` — reusable PBR families;
- `SCATTER_BACKEND` — placement/distribution systems;
- `SOURCE_REFERENCE` — algorithm/reference only, never runtime dependency.

## Quality tiers

- `A` — hero/close-up production quality;
- `B` — normal gameplay / mid-distance production quality;
- `C` — background, blockout or stylized fallback;
- `D` — diagnostic only;
- `UNRATED` — probe required before production selection.

Quality rating records evidence such as source resolution, material completeness, silhouette richness, variant depth, botanical plausibility and close-up review.

## Selection law

For a requested usage class choose the highest-quality compatible provider that satisfies license/runtime constraints. Built-in procedural generation is not automatically preferred merely because it is available.
