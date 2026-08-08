# Feature-to-Modeling Strategy Map

## Cel

Każdy Shape Node / Feature ID powinien zostać przypisany do techniki **dopiero po sklasyfikowaniu formy**.

Canonical decision order v0.9:

```text
design role
-> Shape Graph node
-> shape class / mathematical representation
-> semantic skill
-> Blender implementation
```

Agent nie może wybrać techniki tylko dlatego, że zna operator.

## Shape representation classes

Primary classes:
- ENVELOPE
- PARAMETRIC_PRIMITIVE
- EXTRUDED_PROFILE
- REVOLVED_PROFILE
- PROFILE_SWEEP
- MULTI_SECTION_LOFT
- MULTI_SECTION_TRANSITION
- SUBD_FREEFORM
- BOOLEAN_RECESS
- PANEL_LINE
- LAYERED_ASSEMBLY
- HYBRID_ASSEMBLY

Canonical definitions są w `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md`.

## Implementation strategy classes

- PARAMETRIC_PRIMITIVE
- DIRECT_MESH
- BMESH_PROCEDURAL
- SECTION_LOFT_HARD_SURFACE
- EXTRUDED_PROFILE
- PROFILE_SWEEP
- AXISYMMETRIC_PROFILE
- BOOLEAN_RECESS
- BOOLEAN_UNION
- SOLIDIFY_SHELL
- BEVEL
- CURVE_PROFILE
- SUBD_TOPOLOGY_CONTROL
- ARRAY_INSTANCE
- RADIAL_REPEAT
- GEOMETRY_NODES
- FLOATING_DETAIL
- PANEL_LINE
- DECAL
- NORMAL_BAKE
- MATERIAL_ONLY

## Selection criteria

Uwzględnij:
- wpływ na silhouette;
- authoritative views;
- cross-section behavior;
- editability;
- precision;
- repeated use;
- shading/continuity;
- host/parent relation;
- runtime;
- risk of regression.

## Routing examples

### Osiowo symetryczny stacked profile

```text
REVOLVED_PROFILE
-> AXISYMMETRIC_PROFILE
```

### Base zmienia width + depth + corner plan po Z

```text
MULTI_SECTION_LOFT
-> SECTION_LOFT_HARD_SURFACE
```

### Shoulder łączący dwa zaakceptowane przekroje

```text
MULTI_SECTION_TRANSITION
-> SECTION_LOFT_HARD_SURFACE
```

### Głęboki panel

```text
BOOLEAN_RECESS
-> BOOLEAN_RECESS / DIRECT_MESH
```

### Wąski seam

```text
PANEL_LINE
-> HS_PANEL_LINE
```

### Smooth compound shell bez stabilnych section stations

```text
SUBD_FREEFORM
-> SUBD_TOPOLOGY_CONTROL
```

### Logo

```text
G5 SURFACE_DETAIL
-> DECAL
```

### Niebieski light strip

```text
G3 STRUCTURAL_FEATURE
-> separate geometry + emissive material
```

## Box-abuse rule

Jeżeli primary node:
- zmienia width wzdłuż osi;
- zmienia depth wzdłuż osi;
- ma zmienny corner/chamfer treatment;
- pokazuje continuous surface między stacjami;

to `PARAMETRIC_PRIMITIVE + BEVEL` nie może być default strategy.

Najpierw rozważ `MULTI_SECTION_LOFT` albo `SUBD_FREEFORM`.

## Leaf-skill rule

Skille detalu są downstream od zaakceptowanego hosta.

Przykłady:
- `HS_PANEL_LINE` nie naprawia błędnego primary shell;
- `BEVEL` nie naprawia złego base cross-section;
- `DECAL` nie jest budowany na panelu, który jeszcze FAIL;
- material finish nie kompensuje błędnej geometrii.

## Strategy switch

Po jednej poprawionej ponownej próbie tej samej strategii, jeżeli authoritative views nadal wskazują niezgodność 3D:
- re-inspect registration/parameters;
- re-open shape classification;
- zmień representation zamiast wykonywać nieskończone lokalne tweaki.
