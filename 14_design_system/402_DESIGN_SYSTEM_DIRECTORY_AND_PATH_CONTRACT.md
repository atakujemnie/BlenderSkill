# Design System Directory and Path Contract

## Source-side root

Default RPG/project convention:

```text
<repo>/Blender/DesignSystems/<location_id>/
```

This is a source-authoring location. It may contain Markdown, JSON, source textures, logos and `.blend` authoring libraries that should not be copied blindly into runtime packages.

## Required files

```text
LOCATION_DESIGN_SYSTEM.md
 design_system.json
 sources.json
 asset_library_manifest.json
```

## Standard directories

```text
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

## Runtime material boundary

The v0.14 runtime material library remains:

```text
<repo>/Assets/GameAssets/Materials/Locations/<location_id>/
```

`design_system.json.resource_paths.material_library` points to it.

The design-system source root may contain high-resolution/source material assets, while the runtime material library owns approved game-ready payloads.

## Find-or-create behavior

```text
known design_system_root
-> <root>/<location_id>
else known project_root
-> <project_root>/Blender/DesignSystems/<location_id>
else BLOCKED
```

If missing and creation is authorized, bootstrap canonical directories and schemas. Never create multiple sibling roots because of capitalization, spaces or spelling variants; normalize the stable `location_id` first.

## No silent relocation

Changing the design-system root is a migration. Update:
- `design_system.json`;
- project profile;
- dependent asset records;
- Blender Asset Library registration;
- runtime material link when affected.

Do not leave old and new roots both authoritative.

Canonical resolver: `executors/design_system_resolver.py`.
