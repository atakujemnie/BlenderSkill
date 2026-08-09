# Shape, Edge, Seam and Detail Language

## Why this exists

Shared materials alone do not create a coherent product family. Assets must also share recurring form logic.

## Shape language

Record preferred and forbidden tendencies, for example:

```yaml
shape_language:
  families:
    ASTERA_CIVIC_HARDSURFACE:
      preferred:
        - broad planar surfaces
        - controlled faceted/chamfered transitions
        - modular service segmentation
        - visible mechanical part boundaries
      avoid:
        - capsule_everything
        - decorative_freeform_without_function
        - excessive_global_bevel
```

## Edge families

Stable edge-family IDs define ranges/roles rather than one radius for every object:

```yaml
edge_language:
  families:
    EDGE_ASTERA_OUTER_A:
      role: main exposed housing
      radius_mm: [12, 24]
    EDGE_ASTERA_PANEL_A:
      role: service panel
      radius_mm: [3, 8]
```

## Seam/gap language

Define recurring:
- panel gaps;
- shadow gaps;
- trim widths;
- service seams;
- recess depth families;
- junction types.

The Assembly Relation Contract still validates physical correctness per asset; the design system defines stylistic families.

## Detail language

Record repeated mezo-detail density and vocabulary:
- fastener families;
- panel-line rhythm;
- vent/perforation grammar;
- indicator strips;
- handle/port framing;
- service segmentation.

## Conformance

A new asset may introduce a source-required exception, but a generic family asset should not invent a foreign edge/seam vocabulary when a canonical family exists.
