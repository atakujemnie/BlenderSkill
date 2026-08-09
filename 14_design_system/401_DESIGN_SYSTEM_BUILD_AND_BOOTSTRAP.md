# Design System Build and Bootstrap

## Intent

Use when the user asks to create a reusable visual/design system for a location, district, corporation/faction or asset family instead of immediately building another isolated asset.

## Inputs

At minimum:
- `location_id`;
- project/source root;
- available canonical references;
- known accepted assets or material/branding sources when they exist.

Optional:
- `organization_id` / faction / brand;
- parent design system;
- asset-family references;
- existing runtime material library;
- existing Blender Asset Library.

## Build sequence

```text
resolve canonical path
-> if absent: bootstrap folder + MD + JSON + registries
-> inventory references and accepted existing assets
-> classify evidence by domain
-> extract stable cross-asset rules, not one-off geometry
-> build design tokens
-> build shape/edge/detail language
-> build material families and source texture registry
-> build branding/graphics registry
-> identify reusable components/profiles/nodegroups
-> define lighting/emissive and weathering language
-> create family/organization overrides
-> package approved Blender resources
-> validate final manifest
-> return canonical paths
```

## Evidence rule

A design system is not invented from aesthetic prose alone if stronger source evidence exists.

Classify every promoted rule as:
- `EXPLICIT` — dimensions/specification/source file;
- `REPEATED` — observed consistently across multiple accepted assets/references;
- `INFERRED` — plausible shared rule with provenance and confidence;
- `PROPOSED` — new design decision requiring explicit design-system ownership.

Do not promote a one-off accident from a single asset into a universal rule without evidence.

## Existing-assets mining

Accepted assets may be mined for repeated:
- material IDs/textures;
- edge radii/chamfers;
- trim profiles;
- LED treatment;
- panel gaps/seams;
- branding placement;
- utility modules;
- fasteners;
- decals/signage;
- weathering intensity.

The source asset remains valid evidence, but promoted resources receive canonical design-system IDs and paths.

## Bootstrap vs Ready

`BOOTSTRAPPED` means folder/schema exists. It is not design approval.

`READY` requires relevant domains to be populated from evidence and pass `LOCATION_DESIGN_SYSTEM_MANIFEST final=True`.

## Required user-facing result

Always report exact paths:

```text
Design system MD: <...>/LOCATION_DESIGN_SYSTEM.md
Manifest: <...>/design_system.json
Materials: <runtime/material/path>
Branding: <...>/branding
Components: <...>/components
Blender Asset Library: <...>/<LOCATION>_ASSET_LIBRARY.blend
```

Those paths become reusable inputs for future prompts.
