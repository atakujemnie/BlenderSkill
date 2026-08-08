# Asset Completion Levels and Stop Conditions

## Purpose

An AI Blender agent must never use the word `DONE` without declaring **what level is complete**.

A visually convincing render is not equivalent to a complete game asset.
A successful export is not equivalent to pipeline integration.

The asset lifecycle has four explicit completion levels.

```text
A RECONSTRUCTION_COMPLETE
-> B MODELING_COMPLETE
-> C GAME_READY_COMPLETE
-> D PIPELINE_INTEGRATED
```

A higher level requires all lower levels to pass.

---

# Level A — `RECONSTRUCTION_COMPLETE`

The reference-driven object is geometrically and visually solved.

Required:
- hard dimensions pass;
- canonical silhouettes pass;
- primary proportions pass;
- all reference-required MUST features have owners;
- branding/signage placement is correct or explicitly deferred to surface authoring;
- rear/bottom/hidden evidence has been handled according to authority policy;
- unresolved geometry is listed;
- multi-view regression gate passes.

Not required yet:
- final texture bake;
- runtime LOD package;
- collision;
- engine integration.

Output status example:

```yaml
completion:
  reconstruction: PASS
  modeling: NOT_EVALUATED
  game_ready: NOT_EVALUATED
  pipeline_integrated: NOT_EVALUATED
  highest_level: RECONSTRUCTION_COMPLETE
```

---

# Level B — `MODELING_COMPLETE`

The editable Blender asset is production-clean as an authoring asset.

Requires Level A plus:
- final intended authoring geometry exists;
- topology intent is declared for each mesh;
- mesh validation passes;
- UV strategy is complete;
- material segmentation is complete;
- decals/branding are represented by the intended pipeline;
- transforms/pivot/naming pass;
- authoring source is saved;
- no temporary helper or QA object contaminates the production collection.

A procedural Blender shader may still exist at this level.

`MODELING_COMPLETE` does **not** mean the game-runtime texture/material package is complete.

---

# Level C — `GAME_READY_COMPLETE`

The asset can be consumed by the target runtime without relying on undefined Blender-only state.

Requires Level B plus:
- active Game Asset Contract;
- active Engine Profile or explicit neutral-baseline contract;
- LODs validated;
- collision validated;
- material count/draw-call implications validated;
- procedural material effects either baked, recreated in runtime, or explicitly removed;
- required BaseColor/Normal/ORM/Emissive or engine-specific texture outputs exist;
- emissive authoring/runtime handoff is documented;
- exported files pass post-export validation;
- protected reconstruction features survive optimization.

If the Engine Profile is absent, runtime status remains `UNVERIFIED` and Level C cannot be claimed for an engine-specific task.

---

# Level D — `PIPELINE_INTEGRATED`

The asset is not only exported; it is registered and usable inside the actual project pipeline.

Requires Level C plus:
- stable project asset ID;
- destination path conforms to Project Asset Pipeline Profile;
- LODs/collision/textures are associated with the correct asset entry;
- no unintended overwrite of an existing asset;
- asset catalog/registry/import database integration is complete where the project requires one;
- engine/project import succeeds;
- an instantiation/use test succeeds or is explicitly marked unavailable;
- pipeline integration report is persisted.

If the project has a catalog but the agent has no capability to register the asset, report:

```text
GAME_READY_COMPLETE
PIPELINE_INTEGRATED: BLOCKED
reason: ASSET_CATALOG_WRITE_CAPABILITY_MISSING
```

Do not call this fully complete.

---

# User-requested stop level

The user may request only a specific level.

Examples:
- "make the Blender model" -> Level B may be sufficient;
- "make it game ready" -> Level C is required;
- "put it into the game/project asset catalog" -> Level D is required.

The agent must determine `TARGET_COMPLETION_LEVEL` during CONTRACT/PLAN.

If the user says only "build the asset" in a game-production project, default target is **Level C**, not Level A.

---

# Stop conditions

The agent must stop and report a blocker when a required gate cannot be validated.

Do not silently downgrade the target.

Examples:
- missing runtime material specification;
- required bake not possible with available tools;
- collision contract unknown;
- export succeeded but textures are missing;
- catalog registration capability unavailable.

---

# Mandatory completion report

At every claimed finish emit:

```yaml
asset_completion:
  target_level: GAME_READY_COMPLETE
  highest_passed_level: MODELING_COMPLETE
  levels:
    reconstruction: PASS
    modeling: PASS
    game_ready: FAIL
    pipeline_integrated: NOT_REQUIRED
  blockers:
    - PBR_BAKE_NOT_DONE
    - RUNTIME_EMISSIVE_NOT_VERIFIED
  deferred_items: []
  deliverables_present:
    blend: true
    runtime_mesh: true
    textures: false
    validation_report: true
```

The first failing required level defines the real completion state.

---

# Anti-pattern

Never report:

> Asset finished and exported.

when the same report also says:
- textures were not baked;
- runtime-only details were not produced;
- catalog integration was not done.

That state is `MODELING_COMPLETE` or partial Level C, not full completion.
