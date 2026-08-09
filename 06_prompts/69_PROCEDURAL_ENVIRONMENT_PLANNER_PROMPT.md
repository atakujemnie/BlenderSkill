# Procedural Environment Planner Prompt

Use this prompt for vegetation/terrain/environment authoring requests.

## Required reasoning output

1. Split hard-surface/reference owners from procedural owners.
2. Declare target completion level and runtime usage class.
3. Build semantic specs before selecting a generator.
4. Discover/probe provider compatibility for active Blender 5.1.
5. Prefer built-in Geometry Nodes or committed generated Python when they satisfy the requirement.
6. Record seed, provider/version, parameters hash and expected semantic parts.
7. Generate one disposable candidate before production population.
8. Validate botanical structure and fixed-seed reproducibility.
9. For placement, declare masks/slope/spacing/exclusion before scatter.
10. For planters, validate rootball/soil/wall/stem composition.
11. Run vegetation runtime prep before existing UV/bake/export/runtime gates.

## Forbidden shortcuts

- provider documentation -> assume installed/working;
- random scatter without explicit seed/constraints;
- beautiful generated tree -> claim game ready;
- manually tweak a random output while claiming reproducibility;
- use paid asset pack without explicit local availability/license;
- full Infinigen/BlenderProc dependency when one extracted algorithm/contract is sufficient;
- use a version-blocked provider because its output quality is attractive.

## Preferred result format

```yaml
procedural_task:
  owner: ...
  provider: ...
  provider_probe: PASS|BLOCKED
  semantic_spec: ...
  seed: ...
  generation_gate: ...
  placement_gate: ...
  composition_gate: ...
  runtime_prep: ...
  blockers: []
```
