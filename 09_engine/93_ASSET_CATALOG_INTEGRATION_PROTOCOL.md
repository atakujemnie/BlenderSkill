# Asset Catalog Integration Protocol

## Purpose

Exporting a mesh file is not the same as integrating an asset into a production project.

This protocol defines the final `PIPELINE_INTEGRATED` step for projects that maintain an asset catalog, importer registry, content database, manifest or equivalent system.

The exact catalog format is project-specific and must come from the active Project Asset Pipeline Profile.

---

# Preconditions

Before catalog integration:
- `GAME_READY_COMPLETE` passes;
- runtime files exist;
- stable asset ID exists;
- destination namespace/path is known;
- active Project Asset Pipeline Profile describes the catalog/import mechanism;
- agent has write capability for the catalog, or reports a blocker.

Do not invent a catalog schema.

---

# Discovery

Before writing:
1. search for an existing asset with the same semantic role/name/ID;
2. identify whether this is a replacement, version, variant or new asset;
3. inspect the smallest relevant catalog entry/example;
4. determine required files/fields;
5. persist the resolved integration contract.

Do not overwrite an existing production asset because a generated object happens to have a similar name.

---

# Minimal integration record

Project-specific fields may differ, but the semantic record should cover:

```yaml
asset_catalog_entry:
  asset_id: ACS-BOL-140
  source_blend: path/to/source.blend
  runtime_meshes:
    LOD0: path/to/mesh0
    LOD1: path/to/mesh1
    LOD2: path/to/mesh2
    LOD3: path/to/mesh3
  collision: path/to/collision
  textures:
    basecolor: path/to/basecolor
    normal: path/to/normal
    orm: path/to/orm
    emissive: path/to/emissive
  material_profile: ACS_CIVIC_DARK_EMISSIVE
  pivot_policy: BASE_CENTER
  bounds_mm: [210, 210, 1050]
  status: ACTIVE
```

Only fields actually supported by the project should be written.

---

# Existing asset conflict

If an existing catalog item is found:

Classify:
- `SAME_ASSET_UPDATE`;
- `NEW_VARIANT`;
- `LEGACY_ASSET_REPLACEMENT`;
- `NAME_COLLISION_UNRELATED`.

A replacement requires explicit project policy or user instruction.

If the current project already has a generic road bollard and the new reconstruction is a branded Astera bollard, do not silently overwrite the generic asset. Register as a distinct asset or follow the replacement policy.

---

# Validation after registration

After writing the catalog/import record:
- read it back;
- verify all referenced paths exist;
- verify expected LOD/collision associations;
- verify material/texture references;
- verify asset ID uniqueness;
- run importer/instantiation smoke test if the current toolchain supports it.

A successful file write without readback is not sufficient.

---

# Missing capability

If the agent can create/export files but cannot modify the project's catalog:

```yaml
pipeline_integration:
  status: BLOCKED
  reason: CATALOG_WRITE_CAPABILITY_MISSING
  prepared_files: true
  proposed_asset_id: ACS-BOL-140
```

This can still satisfy `GAME_READY_COMPLETE`, but not `PIPELINE_INTEGRATED` when Level D is required.

---

# Idempotency

Re-running integration must not create:
- duplicate asset IDs;
- duplicate manifest entries;
- `.001`-style catalog variants;
- multiple references to the same LOD file.

Prefer update-by-stable-ID.

---

# Rollback

Before changing an existing catalog entry:
- capture the old record;
- record affected asset ID;
- write transactionally where possible;
- restore the previous record if verification fails.

---

# Boundary with engine adapter

This protocol describes **project registration**.
`09_engine/91_ENGINE_ADAPTER_PROTOCOL.md` describes runtime format/import behavior.

Both may be required for Level D.
