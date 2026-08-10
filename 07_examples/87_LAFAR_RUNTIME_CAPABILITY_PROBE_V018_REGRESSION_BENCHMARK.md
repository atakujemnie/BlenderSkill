# Benchmark 87 — Lafar Runtime Capability Probe v0.18

Version: 0.18.0
Status: RELEASE REGRESSION BENCHMARK

## Goal

Prove that provider selection for a Lafar procedural vegetation task is based on real runtime evidence rather than declared installation metadata.

## Primary scenario

```text
REAL BLENDER 5.1.x
→ runtime discovery
→ canonical provider registry normalization
→ expected provider gate
→ real Geometry Nodes capability probe
→ requested domain = GRASS
→ domain suitability
→ quality suitability
→ provider selection report
→ minimal generated output
→ geometry validation
→ cleanup validation
```

Required primary evidence: Geometry Nodes is `PROBE_REQUIRED` after discovery, changes to `PASS` only after real evaluation, output geometry is valid, and probe cleanup leaves no object/mesh/node-group delta.

## Negative controls

### NC-1 — discovery execution
`blender_addon_inventory.py` must not import provider modules or execute provider operators.

### NC-2 — built-in capability assumption
`builtin_geometry_nodes` discovered without probe must not be `PASS`.

### NC-3 — canonical probe state
`PROBE_REQUIRED` is valid across provider executors.

### NC-4 — unknown classification
An unknown add-on remains `UNKNOWN` and is not coerced to `UTILITY`.

### NC-5 — expected-provider mismatch
Missing expected provider produces `DISCOVERY_MISMATCH` and blocks the pipeline.

### NC-6 — wrong vegetation domain
Sapling with `probe=PASS` and requested `GRASS` produces `domain=MISMATCH`, `selection=REJECTED`.

### NC-7 — dirty probe
Any remaining object, mesh, curve or node group produces `cleanup=FAIL`; probe cannot remain `PASS`.

### NC-8 — insufficient quality
A provider below the required quality tier remains visible and receives `QUALITY_REJECTED`.

### NC-9 — illegal custom fallback
Custom/native fallback while an eligible stronger provider exists produces `BLOCKED`.

## Pass condition

All unit/integration/regression tests pass and the required Blender runtime suite passes in a pinned 5.1.x binary under factory-startup background mode with auto-execution disabled.
