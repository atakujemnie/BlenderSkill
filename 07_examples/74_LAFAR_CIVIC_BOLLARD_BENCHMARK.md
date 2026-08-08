# Benchmark — Lafar Civic Bollard

## Status

Real end-to-end agent run used as a BlenderSkill v0.5 regression benchmark.

Asset:
- Lafar Civic Bollard;
- Astera Civic Systems;
- technical concept sheet with hero/front/side/top/rear/bottom/detail views;
- game-ready hard-surface civic prop.

This benchmark exists to measure **quality and efficiency**, not just whether an asset file can be produced.

---

# Baseline run

Approximate language-model usage:

```text
~60k tokens total
```

Human visual evaluation of the final Blender result:

```text
9 / 10
```

Primary remaining visual weakness noted by the reviewer:
- surface/material reads too clean and uniform compared with the reference;
- final neon/bloom appearance still depends partly on runtime engine/post-processing.

---

# Final geometric/runtime outputs from baseline

```yaml
asset:
  bounds_mm: [210, 210, 1050]
  origin: BASE_CENTER
  rotation: [0, 0, 0]
  scale: [1, 1, 1]

lods:
  LOD0_tris: 2716
  LOD1_tris: 1152
  LOD2_tris: 480
  LOD3_tris: 128
  collision_tris: 88

mesh_summary:
  duplicate_vertices: 0
  loose_vertices: 0
  edges_over_2_faces: 0
  uv_present: true
```

Major locked dimensions:
- overall height = 1050 mm;
- main body diameter = 140 mm;
- base diameter = 210 mm;
- measured service collar ≈ 178.9 mm diameter.

---

# Source-authority behavior

The run correctly used:

```text
explicit numeric dimensions
> orthographic technical views
> detail views
> perspective hero
> approximate prose ranges
```

The technical sheet's front/side projections were measured separately by axis because the sheet showed approximately 13% vertical anisotropy relative to horizontal scale.

This is a positive benchmark behavior.

---

# Real defects caught by QA

The run found multiple problems that survived an initial visual "looks good" impression:

1. loose vertices in the rear service panel;
2. duplicated vertices in the light diffuser;
3. assembly width of 211 mm instead of required 210 mm;
4. anchor/bolt recess geometry extending outside the available flange annulus;
5. base accent emitter present in data but hidden behind the host wall and therefore invisible;
6. decal plates lost during LOD/export because importing the builder triggered destructive top-level `build()` side effects;
7. graphite material rendered too bright under the initial QA lighting setup.

Positive benchmark criterion:

> The agent must diagnose these classes with measurable evidence rather than repeatedly adjusting values by eye.

---

# Questionable baseline decision to prevent in v0.5+

The rear service panel was increased from 0.6 mm to 1.2 mm proud because it was difficult to read in flat lighting.

That is not a safe general reconstruction rule.

v0.5 requirement:
- first separate lighting/material readability from geometric evidence;
- use neutral/matcap/edge evidence;
- change geometric depth only if reference evidence permits the change.

A feature must not become physically larger merely to compensate for a poor QA light rig.

---

# Baseline incompleteness

Despite successful modeling, LOD generation and export, the run explicitly did **not** finish:
- BaseColor/Normal/ORM/Emissive runtime texture bake;
- small details intended for normal-map representation;
- full underside reconstruction from the bottom-view reference;
- project AssetCatalog integration.

Therefore the correct completion classification is not unconditional `DONE`.

Expected v0.5 classification:

```text
RECONSTRUCTION_COMPLETE: PASS
MODELING_COMPLETE: PASS
GAME_READY_COMPLETE: PARTIAL/FAIL until bake/runtime binding is done
PIPELINE_INTEGRATED: FAIL until catalog integration is done
```

---

# Material benchmark

The final asset should not rely on uniform procedural noise alone.

Reference-compatible dark civic materials should preserve:
- low-frequency roughness variation;
- restrained microtexture;
- manufacturing direction where applicable;
- subtle protected-zone dirt;
- sparse plausible wear;
- material-specific variation rather than global random grunge.

The quality target is:

```text
not sterile
not visibly procedural
not heavily damaged
```

The asset should still read as maintained civic infrastructure.

---

# Emissive benchmark

The blue guidance ring and lower marker must be separated into:

```text
asset-side emitter correctness
runtime-side glow/bloom correctness
```

Asset PASS requires:
- correct geometry/mask;
- visible emitter;
- stable blue/cyan hue;
- exported emissive data.

Runtime glow remains `UNVERIFIED` until Engine Profile/post-processing are tested.

---

# Efficiency failures from baseline

The run consumed excessive context partly because it:
- echoed large generated Python files into model context;
- built reusable lathe/profile/QA infrastructure ad hoc;
- returned large diagnostic datasets during image/silhouette analysis;
- performed several compatibility discoveries during production rather than preflight;
- tuned LODs iteratively instead of using reusable cost models/executors from the start.

v0.5 must use:
- Code Artifact and Patch Protocol;
- Tool Output Budget;
- Task Packs;
- Reference Analysis Cache;
- `AXISYMMETRIC_PROFILE` for rotational components;
- Mesh Contract Validator;
- Blender 5.1 Compatibility Matrix;
- explicit completion levels.

---

# v0.5 benchmark targets

Quality is the hard gate. Efficiency targets apply only if quality does not regress.

### Hard gates
- no regression in locked dimensions;
- all reference-critical silhouettes/features pass;
- no hidden emitter feature;
- no destructive builder import side effects;
- all LOD budgets pass;
- exported decal/material references survive;
- completion level reported truthfully.

### Efficiency targets

Baseline total: ~60k tokens.

Target:
- at least 35% total-token reduction on an equivalent run;
- preferred total <= 35k tokens;
- stretch target <= 25k without quality regression;
- no full-source echo for build scripts >120 lines;
- no raw per-row/pixel profile dump unless localized DIAGNOSTIC escalation requires it;
- no more than one corrected retry for the same strategy/preconditions.

### Executor-use target

The run should preferentially reuse:
- `AXISYMMETRIC_PROFILE`;
- `MESH_VALIDATE`;
- runtime compatibility helper;
- QA isolation helper;
- reference measurement executor when validated in the active runtime.

Agent-generated local implementations must be justified when an appropriate reusable executor already exists.

---

# Scorecard

Recommended benchmark score:

```text
Reference fidelity        30%
Runtime correctness       20%
Mesh/LOD/export quality   15%
Material/surface finish   10%
Completion truthfulness   10%
Tool/retry efficiency     10%
Context/token efficiency   5%
```

A token-efficient but visually inferior model does not beat the baseline.

---

# Lessons promoted to canonical library

This benchmark is the evidence source for v0.5 additions covering:
- completion levels;
- Blender 5.1 runtime compatibility traps;
- floating-detail visibility/occlusion rules;
- civic material breakup;
- emissive authoring/runtime separation;
- bake gate;
- asset catalog integration;
- executable artifact/context discipline.
