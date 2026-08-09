# Location Asset Manifest

## Purpose

Prevent missing expensive/focal assets from disappearing behind a populated scene.

## State model

```text
MISSING -> PROXY -> BUILDING -> BUILT_UNVERIFIED -> ACCEPTED -> INSTANCED
                     \-> FAIL/BLOCKED
```

`PROXY` is blockout evidence only.

## Required fields

```yaml
asset_id: BAR_MAIN
required: true
tier: HERO
state: ACCEPTED
source_refs: []
asset_contract: ...
instance_targets: []
```

## Final policy

- required HERO final coverage = 100%;
- every required final asset must be `ACCEPTED` or `INSTANCED`;
- any final `PROXY` fails;
- optional BACKGROUND content cannot compensate for missing HERO/MID requirements.

Canonical executor: `executors/location_asset_manifest.py`.
