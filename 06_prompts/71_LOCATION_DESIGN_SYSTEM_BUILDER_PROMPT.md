# Location Design System Builder Prompt

Use when the user asks to build/refresh a reusable design system for a location, organization/faction or asset family.

## Role

You are not building one prop. You are extracting and packaging reusable visual/product language so future Blender tasks stop reinventing the same materials, logos, components and style rules.

## Procedure

1. Resolve `location_id`, project root and optional organization/family scope.
2. Run `LOCATION_DESIGN_SYSTEM_RESOLVE` with `create_if_missing=true`.
3. Return/retain the canonical path immediately; do not create a second design-system root later.
4. Inventory authoritative references and accepted existing assets.
5. Separate reusable system rules from asset-specific dimensions.
6. Populate `LOCATION_DESIGN_SYSTEM.md` and `design_system.json`.
7. Promote canonical source resources with provenance/hash deduplication:
   - material/texture sources;
   - logos/symbols/wordmarks/icons;
   - decals;
   - reusable components/profiles/nodegroups.
8. Link the v0.14 runtime material library path.
9. Define shape/edge/seam/detail, lighting/emissive and weathering languages.
10. Create organization and asset-family overrides rather than duplicating the whole base system.
11. Build/update the Blender Asset Library `.blend` through Blender Python when reusable Blender datablocks exist.
12. Validate manifest final readiness and run `DESIGN_SYSTEM_CONFORMANCE_GATE` on at least one known accepted asset as a regression fixture.
13. Report exact reusable paths.

## Evidence discipline

Label rules as EXPLICIT / REPEATED / INFERRED / PROPOSED. Do not universalize a one-off modeling accident.

## Reuse discipline

Existing canonical resource wins over a visually similar new local resource unless the reference requires a true exception.

## Output contract

Compact final report:

```text
DESIGN_SYSTEM: READY | BOOTSTRAPPED | BLOCKED
location_id: ...
design_system_version: ...
MD: ...
manifest: ...
material_library: ...
branding: ...
components: ...
asset_library_blend: ...
new_promoted_resources: N
reused_resources: N
blockers: ...
```

Do not dump full manifests or generated scripts unless diagnostics require them.
