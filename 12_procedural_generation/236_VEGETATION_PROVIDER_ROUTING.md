# Vegetation Provider Routing

Version: 0.18.0
Status: EXECUTOR_READY
Executor: `executors/provider_orchestrator.py`

## Source hierarchy

```text
approved project/Asset Library vegetation
→ specialized generator matching requested plant domain
→ eligible general procedural backend
→ custom/native generator fallback
```

The hierarchy is evaluated only after non-executing discovery, registry classification, expected-provider gate and capability evidence.

## Domain routing

- `TREE`, `WOODY_PLANT` → ready asset source, then Sapling/other specialized tree provider if probe and quality permit.
- `VINE`, `SURFACE_GROWTH` → ready asset source, then IvyGen/other specialized surface-growth provider if probe and quality permit.
- `GRASS`, `GROUNDCOVER`, ornamental broadleaf → ready asset source; when no specialized provider exists evaluate Geometry Nodes/Sverchok/general procedural backends.
- `TERRAIN` → ANT Landscape or another terrain provider; terrain capability must not be mislabeled as vegetation capability.

A provider that passes its runtime probe but does not support the requested domain is explicitly rejected. Example: Sapling for `GRASS` = `probe PASS`, `domain MISMATCH`, `selection REJECTED`.

## Reporting law

Absence of a ready vegetation Asset Library does not mean absence of procedural providers. Report ready assets, specialized generators, generic procedural backends, external generators and rejected candidates separately.

## Quality

Provider runtime capability is not visual-quality suitability. A technically executable provider still passes through usage-class quality evidence (`HERO`, `MID`, `BACKGROUND`, `BLOCKOUT`) before final selection when a quality contract is required.

## Custom fallback gate

Custom/native vegetation generation is legal only when:

- discovery is complete;
- expected-provider gate is PASS when applicable;
- stronger relevant candidates were evaluated;
- rejection/block reasons are present;
- no stronger candidate remains `ELIGIBLE` or `ELIGIBLE_GENERIC`.

If an eligible provider remains, custom fallback returns `BLOCKED`.
