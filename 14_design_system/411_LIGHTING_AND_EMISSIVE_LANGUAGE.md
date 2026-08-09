# Lighting and Emissive Language

## Purpose

Integrated lights and environmental lighting communicate system identity and function. They must use shared roles rather than arbitrary per-asset glow.

## Family record

```yaml
lighting:
  families:
    LIGHT_ASTERA_CIVIC_BLUE_A:
      role:
        - status
        - orientation
        - safety
      color_linear: [0.06, 0.45, 1.0]
      intensity_class: LOW
      preferred_placement:
        - recessed_strip
        - underside
        - edge_guidance
      forbidden:
        - large_decorative_glowing_surface
        - exposed_neon_tube_as_structure
```

## Separation of concerns

Design system owns semantic family and visual range.

Asset owns exact fixture geometry/placement required by its reference.

Runtime owns bloom/exposure response.

## Environmental lighting

Location-level ambient/task/accent families may also live here. v0.15 `LOCATION_MATERIAL_LIGHTING_LANGUAGE` consumes these resolved families during full-location art direction.

## Conformance

A new asset with a different accent color/intensity hierarchy requires an explicit family override or design-system update. It cannot silently introduce another "almost Astera blue".
