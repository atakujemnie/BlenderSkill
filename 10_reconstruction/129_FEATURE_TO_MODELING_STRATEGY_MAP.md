# Feature-to-Modeling Strategy Map

Każdy Feature ID powinien zostać przypisany do techniki.

## Strategy classes

- PARAMETRIC_PRIMITIVE
- DIRECT_MESH
- BMESH_PROCEDURAL
- BOOLEAN_RECESS
- BOOLEAN_UNION
- SOLIDIFY_SHELL
- BEVEL
- CURVE_PROFILE
- ARRAY_INSTANCE
- GEOMETRY_NODES
- FLOATING_DETAIL
- DECAL
- NORMAL_BAKE
- MATERIAL_ONLY

## Selection criteria

Uwzględnij:
- wpływ na silhouette,
- editability,
- precision,
- repeated use,
- shading,
- runtime,
- risk of regression.

## Example

Głęboki panel:
`BOOLEAN_RECESS` lub `DIRECT_MESH`

Logo:
`DECAL`

Niebieski light strip:
separate geometry + emissive material.

## Rule

Agent nie może wybrać techniki tylko dlatego, że "zna operator".
Technika wynika z feature requirements.
