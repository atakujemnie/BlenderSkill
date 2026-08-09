# Reusable Component, Profile and Node-Group Library

## Purpose

Repeated product language should be physically reused where appropriate, not reconstructed as lookalikes on every asset.

## Candidate reusable classes

- utility/power/payment panels;
- service hatches and fasteners;
- recessed LED modules/diffusers;
- feet/plinth interfaces;
- trim/extrusion profiles;
- handles, hinges and standardized access hardware;
- planter/bench/lamp civic submodules;
- Geometry Nodes groups;
- material node groups;
- decal carriers;
- profile curves.

## Component record

```yaml
component_id: CMP_ASTERA_UTILITY_PANEL_A
source_blend: LAFAR_ASSET_LIBRARY.blend
asset_name: ACS_UtilityPanel_A
role: civic_utility_panel
interface:
  mount_plane: BACK
  nominal_size_mm: [100, 45, 120]
allowed_variants:
  - power_only
  - power_and_id
usage:
  - bench
  - kiosk
  - terminal
```

## Reuse vs copy

Use linked/asset-library source during authoring when stable. Make local only when asset-specific destructive modification is required. Even then preserve `source_component_id` metadata.

## Do not over-generalize

A component becomes canonical because its form/interface is intentionally shared, not merely because two objects happen to look similar.

## Blender ownership

Approved reusable Blender datablocks are packaged by `DESIGN_SYSTEM_ASSET_LIBRARY_BUILD` into the canonical location `.blend` library and registered in `asset_library_manifest.json`.
