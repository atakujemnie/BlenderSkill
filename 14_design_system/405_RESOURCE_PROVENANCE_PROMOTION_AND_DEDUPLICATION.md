# Resource Provenance, Promotion and Deduplication

## Problem

Without canonical ownership, every asset tends to create another logo PNG, another graphite texture, another blue LED material and another service panel. Visual drift and token/tool cost grow with every object.

## Promotion route

```text
asset/local/reference resource
-> identify reusable semantic role
-> verify ownership/license/provenance
-> hash content
-> compare design-system registry
-> reuse identical existing resource OR promote new canonical resource
-> assign stable resource ID
-> update design-system manifest/library manifest
-> future assets reference canonical ID/path
```

## Categories

- `MATERIAL` / `TEXTURE`;
- `BRANDING`;
- `DECAL`;
- `COMPONENT`;
- `PROFILE`;
- `NODEGROUP`;
- `REFERENCE`.

## Hash rules

- identical content under a different asset-local name should normally deduplicate;
- one semantic `resource_id` may not silently point to two different hashes;
- replacing content under an existing stable ID is a design-system version change;
- original source paths remain in provenance even after copying into canonical ownership.

## Non-destructive migration

Promotion copies/registers; it does not delete the original source asset. Source deletion is a separate cleanup decision after dependency audit.

Canonical executor: `executors/design_system_resource_registry.py`.
