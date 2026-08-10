# Real Blender Runtime Validation

Version: 0.18.0
Status: CURRENT CONTRACT

## Runtime requirement

Tests that claim Blender capability must execute inside a real pinned Blender 5.1.x binary. CPython mocks may test normalization and decision logic, but cannot provide runtime capability evidence.

Required command shape:

```text
blender --background --factory-startup --disable-autoexec --python tests/blender/run_suite.py
```

## Required release checks

1. runtime add-on discovery returns `PASS`;
2. built-in Geometry Nodes is discovered as `PROBE_REQUIRED` before probing;
3. the Geometry Nodes probe creates a disposable object, node tree and modifier;
4. evaluated output geometry satisfies the expected vertex/polygon contract;
5. temporary object, mesh and node group are removed;
6. before/after datablock snapshots are identical;
7. `cleanup_state=PASS` and `side_effects_detected=false`.

A probe that produces correct geometry but leaves persistent datablocks fails the runtime gate.
