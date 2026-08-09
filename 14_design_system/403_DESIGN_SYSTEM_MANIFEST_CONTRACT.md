# Design System Manifest Contract

`design_system.json` is the machine-readable source of truth. `LOCATION_DESIGN_SYSTEM.md` explains intent and evidence; the JSON drives resolution and validation.

## Required top-level domains

```json
{
  "schema_version": "1.0",
  "location_id": "lafar",
  "design_system_version": 1,
  "status": "READY",
  "extends": null,
  "locked_tokens": [],
  "design_tokens": {},
  "shape_language": {},
  "edge_language": {},
  "detail_language": {},
  "material_families": {},
  "branding": {},
  "component_families": {},
  "lighting": {},
  "weathering": {},
  "resource_paths": {}
}
```

## Recommended resource IDs

Use stable semantic IDs rather than filenames:

```text
MAT_ASTERA_GRAPHITE_COMPOSITE_A
MAT_ASTERA_BRUSHED_ALUMINIUM_A
BRAND_ASTERA_PRIMARY
BRAND_ASTERA_SYMBOL
CMP_ASTERA_UTILITY_PANEL_A
CMP_ASTERA_LED_RECESSED_A
EDGE_ASTERA_CIVIC_OUTER_A
WEATHER_LAFAR_MAINTAINED_WET_A
LIGHT_ASTERA_CIVIC_BLUE_A
```

A filename may change without changing the semantic resource ID.

## Provenance

Rules and resources should carry:
- source reference(s);
- evidence type;
- confidence where inferred;
- authoring/version origin;
- license/ownership for imported resources.

## Final readiness

`status=READY|APPROVED` is not sufficient by itself. The final validator requires populated design-token, shape, edge, material, lighting and weathering domains, plus branding assets when branding is applicable.

Canonical validator: `executors/design_system_manifest.py`.
