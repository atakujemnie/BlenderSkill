# Branding, Graphics and Signage Library

## Purpose

Branding must be loaded from canonical source assets, not regenerated from text or approximated per object.

## Canonical resource classes

```text
PRIMARY_LOGO
SYMBOL
WORDMARK
SUBBRAND_MARK
SIGNAGE_ICON
UTILITY_ICON
WARNING_MARK
DECAL_SHEET
TYPE_LAYOUT_REFERENCE
```

Recommended source formats preserve vector authority when available (`SVG`, source design files) plus approved raster/runtime derivatives.

## Branding record

```yaml
resource_id: BRAND_ASTERA_PRIMARY
role: PRIMARY_LOGO
source_path: branding/astera_primary.svg
runtime_derivatives:
  - branding/astera_primary_1024.png
allowed_colors:
  - neutral_light
  - neutral_dark
  - astera_blue
minimum_width_mm: 45
clear_space_ratio: 0.25
allowed_treatments:
  - decal
  - print
  - engraving
  - low_intensity_emissive
forbidden:
  - non_uniform_scale
  - arbitrary_recolor
  - redraw_from_text
```

## Consumption law

If `branding.applicable=true`, asset branding must reference registered resource IDs. A locally redrawn/retyped approximation is a conformance failure.

## Graphics consistency

Shared utility symbols, power icons, service marks and wayfinding glyphs belong here when they recur across assets. This prevents every bench, kiosk and terminal from receiving a different visual icon set.

## Promotion

A new approved graphic introduced by one asset should be promoted through `DESIGN_SYSTEM_RESOURCE_PROMOTE` before reuse elsewhere.
