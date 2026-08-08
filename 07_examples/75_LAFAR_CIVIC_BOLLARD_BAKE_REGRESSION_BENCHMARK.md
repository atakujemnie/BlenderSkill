# Benchmark — Lafar Civic Bollard Bake/Runtime Closure

## Purpose

This benchmark captures the v0.5 continuation from accepted bollard geometry into surface finishing, baking and runtime packaging.

It exists because the agent's geometric/reconstruction quality was already high, while the bake/runtime phase still consumed excessive reasoning/tool iterations.

---

# Baseline capture

User-reported token use at the captured point:

```text
~36k tokens
```

The agent had still not fully finished the bake/runtime closure when the transcript was captured.

The supplied transcript contains approximately:
- 20 Blender Python execution calls;
- repeated bake reruns;
- multiple corrections to bake/channel/UV/export infrastructure.

This benchmark is stage-specific. It does not replace the earlier full bollard benchmark.

---

# Positive v0.5 behavior

The v0.5 knowledge layer successfully caused the agent to:
- fetch the current BlenderSkill repository;
- read the completion/bake/material modules;
- recognize that material bake does not always require a separate high-poly;
- use the packaged mesh validator;
- distinguish `OPEN_ASSEMBLY_PART`, `SURFACE_DETAIL` and `CLOSED_SOLID`;
- verify underside normal direction;
- discover engine LOD/collision conventions;
- improve maintained-civic material breakup;
- keep LODs inside target budgets after repair;
- inspect exported glTF nodes/materials/images instead of trusting export alone.

This proves v0.5 improved decision quality.

---

# Failures that v0.6 must prevent

## B01 — silent bake cancellation

Observed pattern:

```text
No active and selected image texture node found...
bpy.ops.object.bake -> {'CANCELLED'}
```

The first pipeline treated file creation/execution as if bake succeeded and produced degenerate maps.

v0.6 requirement:
- bake executor checks operator result;
- verifies target node in every contributing material;
- rejects cancelled/degenerate output immediately.

## B02 — target node selection ordering

Target image node was active but `select == false`.

Correct sequence discovered:

```text
deselect all nodes
-> target.select = true
-> nodes.active = target
```

v0.6 requirement: encoded in reusable bake executor, not rediscovered per asset.

## B03 — AO contaminated by unrelated scene geometry

A viewport-hidden but render-visible default Cube enclosed the asset and made AO nearly black.

v0.6 requirement:
- ray-dependent bake uses scene isolation;
- `hide_viewport` is never treated as equivalent to `hide_render`.

## B04 — wrong BaseColor semantics for metal

Blender DIFFUSE bake made brushed aluminium read too dark/black.

v0.6 requirement:
- authored Principled Base Color is extracted directly for metallic-roughness runtime BaseColor;
- bake channel semantics are explicit.

## B05 — emissive false-white/clipping

Baking emission incorrectly:
- ignored zero emission strength on non-emitters;
- produced white/unwanted signal;
- or multiplied color by authoring strength until channels clipped and hue was lost.

v0.6 requirement:
- emissive output accounts for both color and strength;
- uses explicit normalization/reference strength;
- validates approved emitter UV regions and hue/clipping.

## B06 — metallic channel extraction failure

Scalar channel extraction temporarily produced metallic = 1 across the atlas.

v0.6 requirement:
- direct scalar-channel extraction helper;
- region-aware validation of metal vs dielectric regions.

## B07 — UV assignment depended on Blender object names

A second build produced names such as `.001`, causing atlas lookup by full object name to miss. UV assignment silently failed and parts overlapped 0..1.

v0.6 requirement:
- semantic part ID owns atlas mapping;
- `.001` is never canonical identity;
- missing UV assignment is hard FAIL.

## B08 — bake source and runtime LOD UV diverged

Atlas assignment was applied to the temporary bake source but not the exported LODs.

Result:
- textures were valid;
- exported runtime mesh sampled them incorrectly.

v0.6 requirement:
- UV contract is applied in the shared build/LOD path;
- bake source and every consuming LOD report the same `UV_CONTRACT_ID`.

## B09 — decal atlas contamination

Decal plates used a separate project decal atlas but were joined into the structural bake source.

v0.6 requirement:
- external decal/dynamic-display UV owners are excluded unless explicitly remapped.

## B10 — import-time side effects

Loading build/export files for helper functions triggered production work or interacted destructively with working collections.

v0.6 requirement:
- import-safe module pattern;
- guarded entrypoints;
- explicit scratch collection ownership.

## B11 — export scratch cleared source LODs

A helper used the same reset/clear collection for temporary mirror copies and for source LODs.

v0.6 requirement:
- source, bake scratch, export scratch and QA scratch ownership are separate.

## B12 — project packaging rediscovered from sibling scripts

The agent read project exporter code to discover:
- one glTF with multiple `_LODn` nodes;
- collision convention;
- X-mirror compensation due engine handedness and readable branding.

Useful once, expensive repeatedly.

v0.6 requirement:
- persist verified packaging facts in Project Asset Pipeline/Engine Profile;
- subsequent assets consume the profile.

## B13 — full rebakes after local channel repairs

Many fixes affected only one channel, yet the whole multi-pass bake pipeline was rerun.

v0.6 requirement:
- dirty-stage dependency cache;
- accepted channels are reused until a dependency invalidates them.

## B14 — tool timeout during expensive bake

A Blender/MCP request timed out while the bake could continue/complete.

v0.6 requirement:
- timeout -> inspect job/artifact state;
- do not duplicate expensive work without proof of failure.

---

# v0.6 stage targets

Starting from accepted Level B/model geometry:

```yaml
GAME_READY_FINISH_target:
  token_budget_preferred: <= 15000
  blender_python_mutation_calls_preferred: <= 10
  full_multichannel_bake_runs: <= 2
  silent_cancelled_bakes_accepted: 0
  missing_uv_contracts_accepted: 0
  exported_runtime_qa_required: true
```

These are benchmark targets, not universal hard limits for every asset.

A more complex animated/dynamic-display asset may legitimately exceed them, but must still avoid rediscovering solved infrastructure.

---

# Required evidence for PASS

```text
UV contract PASS
BaseColor PASS
Normal PASS
AO PASS
Roughness PASS
Metallic PASS
ORM packing PASS
Emissive PASS
Runtime material binding PASS
LOD budgets PASS
Runtime module packaging PASS
Export readback PASS
Baked-runtime visual QA PASS
Completion gate PASS
```

---

# Release criterion

v0.6 is better than v0.5 only if an equivalent bake/runtime closure:
- uses fewer expensive/repeated operations;
- avoids the failure classes above;
- preserves or improves visual/runtime quality;
- reaches the requested completion level instead of stopping during bake debugging.
