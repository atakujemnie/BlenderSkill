# Vegetation Runtime Preparation

## Boundary

Generated authoring vegetation can be intentionally dense. Runtime vegetation must satisfy engine budgets.

```text
VEGETATION_GENERATION_GATE PASS
-> semantic separation
-> runtime budget plan
-> LOD/card/impostor strategy
-> material/atlas strategy
-> wind attributes
-> collision policy
-> existing UV/bake/export/package gates
```

## Required metadata

- generator provenance and seed;
- authoring triangle count;
- semantic parts;
- material slots;
- leaf count/leaf geometry class;
- usage class: `HERO`, `MID`, `BACKGROUND`;
- target LOD budgets.

## Defaults in v0.13 executor

Defaults are initial policy, not universal engine truth:

| Usage | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---:|---:|---:|---:|
| HERO | 60k | 30k | 12k | 2.5k |
| MID | 30k | 14k | 5k | 1.2k |
| BACKGROUND | 12k | 5k | 1.8k | 0.5k |

Project profile may override them.

## Materials

Prefer semantic/shared material families rather than one unique material per plant. Vegetation draw-call budget is often limited by material fragmentation before raw triangle count.

## Executor

`executors/vegetation_runtime_prep.py` produces/validates a compact budget plan; actual decimation/card generation remains Blender-side implementation.
