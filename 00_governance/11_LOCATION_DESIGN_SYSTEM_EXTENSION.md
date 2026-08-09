# v0.16 Persistent Location Design System Extension

## Purpose

v0.15 introduced complete-location assembly and already required a thin Location Design System gate. v0.16 makes that design system a first-class persistent source of truth that can be built once, versioned, reused by future assets and validated for conformance.

The core change is:

```text
reference -> asset
```

becomes:

```text
location/corporation references
-> persistent Location Design System
-> resolved inheritance layer
-> asset family
-> asset reference reconstruction
-> Design System Conformance Gate
```

## Mandatory behavior

For any asset assigned to a known location:

```text
LOCATION_DESIGN_SYSTEM_RESOLVE
-> existing system found: reuse it
-> missing system: bootstrap canonical folder and manifest
-> populate/approve from available authoritative references before final appearance
-> return exact source path to the user/parent task
```

Do not silently invent a second local material/branding/component language inside an asset folder when an approved location system exists.

## Canonical ownership

The design system owns reusable visual language, not individual asset geometry.

It may own:
- location and organization design tokens;
- material families and texture sources;
- logos, symbols, wordmarks, signage icons and decals;
- reusable Blender components and node groups;
- trim/profile families;
- shape, edge, gap, seam and detail language;
- lighting/emissive language;
- weathering and environmental-response language;
- asset-family overrides;
- provenance and license metadata;
- the canonical Blender Asset Library path.

Individual assets own only asset-specific geometry, dimensions, reference exceptions and approved one-off additions.

## Hierarchy and inheritance

```text
UNIVERSE
-> LOCATION
-> ORGANIZATION / FACTION / BRAND
-> ASSET FAMILY
-> ASSET
```

Lower layers may override only unlocked tokens. Locked location/organization identity cannot be silently changed by an asset.

## Source layout

Default project pattern:

```text
<repo>/Blender/DesignSystems/<location_id>/
    LOCATION_DESIGN_SYSTEM.md
    design_system.json
    sources.json
    asset_library_manifest.json
    <LOCATION>_ASSET_LIBRARY.blend
    materials/
    branding/
    components/
    decals/
    profiles/
    nodegroups/
    references/
    previews/
    families/
    organizations/
```

The v0.14 runtime material library remains separate and linked from `design_system.json`:

```text
<repo>/Assets/GameAssets/Materials/Locations/<location_id>/
```

Source design-system files and runtime-ready material payloads must not be conflated.

## Final appearance lock

For a known location, strict L4/L5 or final location art direction requires:

```text
resolved design system READY
+ DESIGN_SYSTEM_CONFORMANCE_GATE PASS
```

before final appearance/runtime completion.

A technically valid asset that uses an unregistered one-off material, wrong logo variant, foreign edge family or incompatible lighting language remains visually unresolved.

## Promotion law

If an asset introduces a genuinely reusable new material/component/decal:

```text
asset-local candidate
-> source/provenance check
-> design-system promotion
-> canonical resource ID/path
-> subsequent assets reuse canonical resource
```

Do not leave repeated resources trapped in the first asset that introduced them.
