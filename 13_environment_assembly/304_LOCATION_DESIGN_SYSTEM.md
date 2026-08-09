# Location Design System Contract

## Purpose

One location owns one persistent design language. Individual assets consume it instead of inventing local styles.

## Mandatory contract

```yaml
location_id: lafar_restaurant_01
unit_scale: 0.001
architectural_grid_mm: 1200
material_families:
  stone_dark: {...}
  graphite_metal: {...}
  warm_brass: {...}
  glass_smoked: {...}
edge_families:
  visible_micro_bevel_mm: [1,2]
lighting_families:
  warm_ambient_k: [2700,3000]
  technical_accent: cool_blue
branding:
  logo_family: ...
  signage_rules: ...
```

Also persist texture sources, trim families, emissive/glass policy, naming and reusable meshes. Reuse the v0.14 location material library path.

Any incompatible one-off asset material is a design-system violation unless explicitly waived.

Canonical executor: `executors/location_design_system_gate.py`.
