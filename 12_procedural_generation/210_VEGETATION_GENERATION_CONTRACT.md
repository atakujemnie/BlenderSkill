# Vegetation Generation Contract

## Separation

```text
PlantSpec
-> provider selection
-> generated authoring geometry
-> botanical validation
-> deterministic reproduction proof
-> VEGETATION_GENERATION_GATE
-> runtime prep
```

Generation and runtime preparation are separate gates.

## PlantSpec minimum

```yaml
form_class: TREE | SHRUB | HERBACEOUS | GRASS | ROSETTE | REED | VINE | GROUND_COVER | ALIEN_BRANCHING
height_m: ...
crown_radius_m: ...
stem_radius_m: ...
branching_orders: ...
internode_length_m: ...
phyllotaxis_deg: ...
apical_dominance: 0..1
crown_density: 0..1
tropism: [x,y,z]
age_class: ...
season: ...
seed: integer
```

Alien flora may use non-terrestrial values but still requires a coherent declared grammar.

## Output contract

Generated authoring output records:
- stable semantic parts;
- bounds and contact/root datum;
- geometry signature;
- generator/provider provenance;
- seed and parameter hash;
- authoring triangle count;
- material region inventory.

## Semantic parts

Use the narrowest sensible set:
- `stem` / `trunk`;
- `branches`;
- `leaves`;
- `flowers`;
- `fruit`;
- `roots_visible`;
- `support_or_stake` when authored.

Do not merge everything before runtime decisions are made.

## Acceptance

`executors/vegetation_generation_gate.py` requires provider proof, botanical grammar proof, nonempty semantic geometry and a fixed-seed reproduction probe.
