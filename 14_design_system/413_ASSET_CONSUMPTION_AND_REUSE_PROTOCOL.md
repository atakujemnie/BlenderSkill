# Asset Consumption and Reuse Protocol

## Preflight for any known-location asset

Before final appearance authoring:

```text
location_id / organization_id / family_id
-> LOCATION_DESIGN_SYSTEM_RESOLVE
-> load design_system.json
-> resolve inheritance layers
-> produce compact RESOLVED_DESIGN_CONTEXT
-> bind canonical materials/branding/components/form families
-> then construct/reconstruct asset
```

Do not load every source texture/reference into context. The compact resolved context should contain semantic IDs, paths and rules relevant to the current asset class.

## Resolved Design Context

Recommended payload:

```yaml
location: lafar
organization: astera_civic_systems
family: street_furniture
design_system_version: 3
materials:
  structural_dark: MAT_ASTERA_GRAPHITE_COMPOSITE_A
  trim_metal: MAT_ASTERA_BRUSHED_ALUMINIUM_A
branding:
  primary: BRAND_ASTERA_PRIMARY
components:
  utility_panel: CMP_ASTERA_UTILITY_PANEL_A
edge_family: EDGE_ASTERA_CIVIC_OUTER_A
lighting_family: LIGHT_ASTERA_CIVIC_BLUE_A
weathering_profile: WEATHER_LAFAR_MAINTAINED_WET_A
source_root: ...
asset_library_blend: ...
```

## Reference priority

The design system supplies shared language. Asset-specific authoritative technical drawings still own exact dimensions/assembly details for the asset.

Therefore:

```text
asset hard dimension/reference
> generic family proportion
```

but:

```text
canonical logo/material identity/locked brand color
> arbitrary asset-local approximation
```

## New reusable discovery

If the asset reveals a new repeated component/material/detail that belongs to the system:

```text
candidate
-> validate against reference
-> DESIGN_SYSTEM_RESOURCE_PROMOTE
-> update manifest/library
-> use canonical ID in current asset
```

## Output

Asset records should persist:
- design-system path;
- design-system version;
- resolved organization/family layers;
- canonical resource IDs used;
- waivers/exceptions;
- conformance result.
