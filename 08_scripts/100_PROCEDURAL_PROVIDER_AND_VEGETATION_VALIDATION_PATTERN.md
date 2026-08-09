# Procedural Provider and Vegetation Validation Pattern

## Adapter/decision split

Blender-side adapters collect facts and execute the actual generator. Pure-Python executors decide whether the evidence satisfies the contract.

```text
Blender adapter
-> provider discovery + minimal probe artifact
-> PROCEDURAL_GENERATOR_PROVIDER

Blender/GN surface sampler
-> candidate points + masks/slope values
-> VEGETATION_SCATTER

Generator
-> semantic geometry + metadata
-> botanical/reproduction evidence
-> VEGETATION_GENERATION_GATE

Planter/soil measurement adapter
-> interior/rootball compact metrics
-> PLANTER_VEGETATION_COMPOSITION
```

## Probe fixture

Never probe a third-party operator on the production asset. Create a disposable collection/scene, execute the smallest representative request, inspect output and remove all created data.

## Negative controls

Required examples:
- provider beyond documented Blender max -> BLOCKED;
- missing seed -> vegetation FAIL;
- fixed seed produces two different signatures -> FAIL;
- excluded/high-slope scatter candidate selected -> test failure;
- rootball outside usable planter soil -> FAIL;
- LOD budgets increase at a lower-detail level -> FAIL.

## CI

`tools/test_v013_procedural_vegetation.py` covers the pure decision layer without requiring Blender or third-party add-ons.
