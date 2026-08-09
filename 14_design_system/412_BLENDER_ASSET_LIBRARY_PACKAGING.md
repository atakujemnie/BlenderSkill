# Blender Asset Library Packaging

## Output

Each mature location design system may own one canonical authoring library:

```text
<design-system>/<LOCATION>_ASSET_LIBRARY.blend
```

The `.blend` is an executable resource cache, not the semantic source of truth. `design_system.json`, `asset_library_manifest.json` and resource provenance remain authoritative.

## Eligible datablocks

- approved Materials;
- reusable Objects/Collections;
- Geometry Node groups;
- shader node groups;
- reusable profile Curves;
- decal carriers/templates.

## API-first rules

Agent operations must be scriptable through Blender Python. Prefer direct datablock access and `bpy.data.libraries.load(...)` for library ingestion over UI-only Asset Browser interaction.

When creating/updating the library:

```text
open/construct isolated design-system library scene
-> add only approved canonical datablocks
-> use stable names matching semantic resource IDs
-> mark reusable datablocks as assets when supported by the runtime
-> assign catalog/category metadata when available
-> save canonical .blend
-> reopen/readback
-> compare asset_library_manifest.json with actual datablocks
```

## Append/link policy

- stable reusable source may be linked/appended for authoring;
- destructive asset-specific edits require a local copy;
- local copy preserves `source_component_id` or equivalent provenance;
- future generic improvements should be promoted back to the canonical component instead of replicated asset by asset.

## Do not package

Do not put whole finished unrelated production assets into the design-system library merely because they use the same style. Package reusable resources/components, not the entire project.

## Runtime boundary

The design-system `.blend` is an authoring dependency. Game runtime export still follows existing glTF/material/runtime contracts.
