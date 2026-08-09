# Location Build Order and Stage Barriers

## Stages

```text
REFERENCE
DESIGN_SYSTEM
ARCHITECTURE
HERO_ANCHORS
FIXED_ASSETS
FURNITURE
LIGHTING_VEGETATION_PROPS
FINAL_FIDELITY
RUNTIME
```

A stage may use explicit proxies for planning, but only PASS from prior stages unlocks final evidence downstream.

Examples:
- failed architecture -> no final furniture acceptance;
- missing HERO bar -> no final dining population acceptance;
- failed clearance -> no final fidelity completion;
- failed reference composition -> no runtime finishing claim.

Canonical executor: `executors/location_stage_barrier.py`.
