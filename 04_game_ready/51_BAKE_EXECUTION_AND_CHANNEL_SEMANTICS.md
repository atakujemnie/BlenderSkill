# Runtime Bake Execution and Channel Semantics

## Purpose

`BAKE_RUNTIME_TEXTURES` must be a deterministic production stage, not an ad-hoc sequence of Blender operator experiments.

A correct-looking Blender material is not evidence that the runtime textures are correct. A texture file existing on disk is not evidence that the bake succeeded.

Use this transaction:

```text
PRECHECK
-> UV CONTRACT
-> SOURCE/MATERIAL CONTRACT
-> SCENE ISOLATION
-> TARGET IMAGE BINDING
-> CHANNEL BAKE
-> IMAGE VALIDATION
-> RUNTIME MATERIAL BINDING
-> EXPORTED-ASSET READBACK
```

Every stage must return a compact PASS/FAIL report.

---

# 1. Operator result is evidence

Never assume `bpy.ops.object.bake(...)` succeeded merely because no Python exception was raised.

Required:

```python
result = bpy.ops.object.bake(type=bake_type)
if "FINISHED" not in result:
    raise RuntimeError(f"Bake failed: {result}")
```

`{'CANCELLED'}` is FAIL.

A Blender info/warning such as:

```text
No active and selected image texture node found in material ...
```

must route to `BAKE_TARGET_BINDING_FAIL`, not to another blind full bake.

---

# 2. Target image node contract

For a joined/source object using multiple material slots, the target image must be active and selected in every material that contributes faces to the bake.

Use the explicit order:

```text
create/reuse ShaderNodeTexImage
-> assign target image
-> deselect all material nodes
-> select the target image node
-> set it as active
-> verify active == target AND target.select == true
```

Do not rely on setting `nodes.active` before selection and assuming selection state will remain correct.

Before calling the operator, emit only a compact binding report:

```yaml
bake_target_binding:
  materials_required: 5
  materials_bound: 5
  image: aster_bollard_basecolor
  status: PASS
```

---

# 3. Scene isolation is mandatory for environment-sensitive passes

AO and other ray-dependent passes are invalid if unrelated scene geometry can occlude the bake source.

Typical trap:
- object has `hide_viewport=true`;
- object has `hide_render=false`;
- AO rays hit it even though the agent does not see it in the viewport.

Before AO/ray-dependent bake:
- isolate the bake source non-destructively;
- use `QA_SCENE_ISOLATE` or equivalent registered executor;
- preserve and restore `hide_render` state;
- do not delete unrelated scene objects.

The default Cube, test geometry, reference planes and helper meshes must not influence AO unless explicitly part of the bake contract.

---

# 4. Channel semantics

## BaseColor

For metallic-roughness runtime pipelines, do not use the Blender `DIFFUSE` bake as a generic BaseColor extractor.

A metal can have little/no diffuse response while its Principled `Base Color` still carries the runtime metal reflectance color.

Preferred procedural-material closure:

```text
Principled Base Color socket
-> temporary Emission output, strength 1
-> EMIT bake
-> BaseColor texture
```

This captures the authored Base Color value/graph rather than lighting or diffuse response.

## Roughness

Bake the authored roughness signal, not a rendered highlight.

Use either:
- a verified Roughness pass;
- or direct socket/channel override to an emission bake when exact authored-value transfer is required.

## Metallic

Metallic is a scalar material property.

For deterministic authored-value transfer:

```text
Principled Metallic socket
-> grayscale temporary Emission
-> EMIT bake
-> pack into the Engine Profile's metallic channel
```

Do not assume a dedicated bake pass exists in every runtime/API version.

## AO

AO is geometry/environment dependent.

Requirements:
- isolated source scene;
- known distance/samples;
- output validated for non-degenerate range;
- no unrelated render-visible enclosure.

## Normal

Normal bake must document:
- tangent-space vs object-space;
- tangent basis expectation;
- authoring bump/procedural normal source;
- whether geometry detail is being transferred high->low.

A material-only normal bake does not require a separate high-poly when the source detail is procedural shader/bump information.

## Emissive

The emissive texture describes **where and what color the emitter is**, not final bloom.

Do not bake bloom, glare or post-process response.

Non-emitting materials must produce black emissive output.

If Principled uses both `Emission Color` and `Emission Strength`, the bake must account for both. Baking color alone is unsafe because non-emitting materials may still have a non-black default emission color with strength zero.

Recommended normalized representation:

```text
emissive_texture_rgb = emission_color * emission_strength / EMIT_REFERENCE_STRENGTH
```

where `EMIT_REFERENCE_STRENGTH` is an explicit authoring/runtime handoff value.

Validate that normalization does not clip channels and destroy hue.

---

# 5. Decals and foreign UV spaces

Do not automatically join permanent decal geometry into the structural bake source.

If a decal uses:
- a separate atlas;
- shared project branding sheet;
- dynamic display UV;
- different sampling/material pipeline;

keep it outside the structural bake unless the bake contract explicitly remaps it.

A decal with unrelated UV coordinates can silently contaminate structural atlas regions.

---

# 6. UV contract before bake

The bake source and every runtime LOD that consumes the baked maps must use the same `UV_CONTRACT_ID`.

Before baking, validate:
- every required semantic part has an atlas assignment;
- no required assignment was skipped because Blender added `.001`/`.002` to an object name;
- LOD runtime meshes actually received the same contract, not only the temporary bake source;
- intentional overlaps are declared;
- decal/dynamic-display UV spaces are excluded where appropriate.

Use `04_game_ready/52_UV_ATLAS_LOD_STABILITY_CONTRACT.md`.

---

# 7. Incremental bake rule

Do not rebake every channel after every local repair.

Maintain dirty dependencies.

Examples:

```text
emission normalization changed
-> dirty: Emissive only

Base Color graph changed
-> dirty: BaseColor only, plus any packed channel explicitly depending on it

AO scene isolation changed
-> dirty: AO / ORM.R only

UV contract changed
-> dirty: all texture channels using that UV set

mesh geometry changed
-> dirty: AO, Normal, and any geometry-position-driven procedural channels;
   BaseColor/Roughness only if their authoring graph depends on geometry/object coordinates
```

Use `05_execution/65_INCREMENTAL_DIRTY_STAGE_CACHE.md`.

---

# 8. Validation before export

Every baked map must pass semantic validation before runtime material assembly.

Minimum checks:
- file/image exists;
- expected dimensions;
- expected color space;
- not all zero unless channel contract permits it;
- not unexpectedly constant;
- channel-specific range is plausible;
- expected material/feature regions contain signal;
- forbidden regions do not contain signal beyond configured padding/bleed;
- no unexplained clipping;
- map is bound to the intended runtime material.

Use `08_scripts/93_BAKE_OUTPUT_VALIDATION_PATTERN.md` and packaged validator when available.

---

# 9. Exported runtime asset is the final bake QA target

After binding baked textures, render/inspect the runtime mesh/material combination — not only the authoring procedural material.

Required final proof:

```text
baked textures
-> runtime material
-> runtime LOD0 mesh UV
-> export
-> exported material/image readback
-> baked-runtime QA render / smoke test
```

A correct authoring render with a broken baked-runtime material is FAIL.

---

# 10. Long-running bake behavior

A tool/MCP timeout is not proof that Blender stopped the bake.

Before retrying an expensive pass:
1. inspect job state if available;
2. inspect output image/file timestamps;
3. inspect Blender state;
4. only restart if the previous execution is proven failed/stopped.

Never launch duplicate AO/full bakes merely because the transport call timed out.

Use `05_execution/64_LONG_RUNNING_JOB_AND_POLL_PROTOCOL.md`.

---

# Compact completion report

```yaml
runtime_bake:
  uv_contract: PASS
  source_isolation: PASS
  basecolor: PASS
  normal: PASS
  orm:
    ao: PASS
    roughness: PASS
    metallic: PASS
  emissive: PASS
  runtime_material_binding: PASS
  exported_texture_readback: PASS
  baked_runtime_qa: PASS
  channels_rebaked_this_iteration:
    - emissive
  status: PASS
```

Do not return raw pixel arrays or complete shader graphs unless a scoped diagnostic explicitly requires them.
