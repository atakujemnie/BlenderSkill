# Design System Inheritance and Overrides

## Hierarchy

```text
UNIVERSE
-> LOCATION
-> ORGANIZATION / FACTION / BRAND
-> ASSET FAMILY
-> ASSET
```

Example:

```text
RPG
-> LAFAR
-> ASTERA_CIVIC_SYSTEMS
-> STREET_FURNITURE
-> STREET_BENCH
```

## Resolution

Higher layers establish defaults. Lower layers may override only where permitted.

Typical split:
- Location: climate response, city palette, environmental materials, wetness/maintenance baseline.
- Organization: brand palette, logo, civic-blue emissive, industrial form language, recurring components.
- Family: dimensions/rules shared by benches, planters, lamps, kiosks etc.
- Asset: source-specific exceptions and dimensions.

## Locked tokens

Identity-critical paths can be locked, for example:

```text
branding.primary_symbol
lighting.families.ASTERA_CIVIC_BLUE.color
material_families.MAT_ASTERA_GRAPHITE_COMPOSITE_A.identity
```

An asset cannot silently override a locked token. It must either reuse it or receive an explicit design-system revision/waiver.

## Merge semantics

- dictionaries deep-merge;
- scalar/list values replace at the lower layer;
- provenance is retained per resolved leaf path;
- scope order may not move backward;
- conflicting locked values fail resolution.

Canonical pure-Python resolver: `executors/design_system_inheritance.py`.
