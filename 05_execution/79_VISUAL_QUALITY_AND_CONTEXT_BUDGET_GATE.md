# Visual Quality and Context Budget Gate

## Purpose

A technically valid asset can still be visually below production quality or consume excessive agent context. v0.14 treats both as explicit completion constraints.

## Visual stage barrier

Before expensive runtime work (LOD/bake/export/catalog/engine integration), require an early visual-quality decision for final assets.

For vegetation/planters this includes:
- source-asset quality tier suitable for usage class;
- planting composition grammar PASS;
- reference composition fidelity PASS when reference-driven;
- location material library resolved;
- material-language consistency reviewed;
- no obvious procedural periodicity/sterility blockers.

If the asset will be rebuilt visually, runtime finishing is blocked.

## Context budget

Default v0.14 benchmark targets:
- total agent context for the Lafar three-planter regression: <= 30k tokens;
- stretch target: <= 20k tokens;
- no full-source echo after a script is persisted;
- default diagnostics: SUMMARY;
- unchanged sources are not reread without a specific missing fact;
- reusable executor search is mandatory before generating non-trivial per-asset infrastructure.

## Reusable-executor law

Before creating a new project-local script, classify it:

```text
asset-specific data/spec
-> project file allowed

reusable generator/validator/material resolver/provider probe
-> BlenderSkill executor/tool first
```

A repeated local helper is technical debt and should be promoted to the canonical library.

## Reporting

Return compact metrics:
- `visual_quality_status`;
- failing quality owners/ROIs;
- `context_tokens_estimated` or available tool usage metric;
- scripts/files generated this run;
- reusable-executor misses;
- runtime stage authorization.
