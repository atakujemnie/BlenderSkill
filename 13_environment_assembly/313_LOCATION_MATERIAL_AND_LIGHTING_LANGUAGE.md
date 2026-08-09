# Location Material and Lighting Language

## v0.16 source

Consume the resolved persistent design system from `14_design_system/`, not ad-hoc per-location shader/light guesses.

## Materials

Use resolved canonical material IDs and the v0.14 persistent runtime material library. Reuse approved structural, architectural, vegetation and organization-specific families. One-off neutral placeholders are blockout-only.

A repeated material discovered during assembly should be promoted back to the design system rather than copied into multiple asset folders.

## Lighting

Use resolved lighting/emissive families where defined, while preserving reference-specific fixture placement.

Separate:
- ambient/architectural light;
- task lights;
- table lights;
- integrated furniture/bar/civic LEDs;
- technical/cool accents when canonical.

Light placement follows architecture/HERO anchors. Do not use flat general illumination as a substitute for the reference lighting hierarchy.

## Weathering continuity

Location art direction also consumes the resolved weathering/environment-response profile so dirt, wetness and maintenance state remain coherent across assets.

Final art-direction PASS requires family coverage, visible hierarchy and `DESIGN_SYSTEM_CONFORMANCE_GATE` where applicable, not only correctly named material/light datablocks.
