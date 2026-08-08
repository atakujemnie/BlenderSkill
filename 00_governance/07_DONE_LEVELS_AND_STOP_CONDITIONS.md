# Asset Completion Levels and Stop Conditions

## Purpose

An AI Blender agent must never use the word `DONE` without declaring **what level is complete**.

A visually convincing render is not equivalent to a complete game asset.
A successful export is not equivalent to pipeline integration.
A bare `PASS` flag is not equivalent to proof.

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

The reference-driven object is geometrically and visually solved **with proof-bearing reconstruction evidence**.

Required:
- hard dimensions pass with numeric provenance;
- canonical silhouettes/views pass through registered comparison where authoritative references exist;
- primary proportions/landmarks pass;
- all reference-required MUST features have owners and appropriate visibility/ROI/numeric proof;
- branding/signage placement is correct or explicitly deferred to surface authoring;
- rear/bottom/hidden evidence has been handled according to authority policy;
- HARD/MUST/CANONICAL deviations are `RESOLVED` or `ACCEPTED_BY_AUTHORITY` with identifiable records;
- unresolved geometry is listed;
- multi-view regression gate passes;
- `RECON_FIDELITY_GATE` passes with evidence provenance.

A narrative `looks correct`, `matching the card`, correct bounding box, successful export or successful engine test cannot substitute for this evidence.

Not required yet:
- final texture bake;
- runtime LOD package;
- collision;
- engine integration.

Output status example:

```yaml
completion:
  reconstruction:
    status: PASS
    evidence_kind: RECON_FIDELITY_GATE
    provenance_id: recon_gate_report_004
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
- LODs validated against the active hard/authority-resolved budget;
- collision validated;
- material count/draw-call implications validated;
- procedural material effects either baked, recreated in runtime, or explicitly removed;
- required BaseColor/Normal/ORM/Emissive or engine-specific texture outputs exist;
- emissive authoring/runtime handoff is documented;
- exported package readback passes required node/material/image/primitive-attribute/transform contracts;
- exported files pass post-export validation;
- protected reconstruction features survive optimization;
- post-export round-trip invariants pass.

A parseable/loadable glTF without required `TEXCOORD_0` or with a node transform forbidden by the active runtime profile is not Level C.

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
- runtime test coordinate space and node-transform policy are compatible with the active profile;
- pipeline integration report is persisted.

If the project has a catalog but the agent has no capability to register the asset, report:

```text
GAME_READY_COMPLETE
PIPELINE_INTEGRATED: BLOCKED
reason: ASSET_CATALOG_WRITE_CAPABILITY_MISSING
```

Do not call this fully complete.

Target-engine evidence that exists while Level C is failing does not promote the asset to Level D.

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
- reconstruction PASS lacks registered/provenance evidence;
- HARD authority conflict remains open;
- missing runtime material specification;
- required bake not possible with available tools;
- collision contract unknown;
- export succeeded but required primitive attributes are missing;
- runtime node transforms violate project policy;
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
  evidence:
    reconstruction_fidelity_gate:
      status: PASS
      evidence_kind: RECON_FIDELITY_GATE
      provenance_id: recon_gate_report_004
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
- reconstruction evidence is unverified;
- textures were not baked;
- runtime-only details were not produced;
- required UV attributes disappeared after export;
- catalog integration was not done.

That state is the highest lower level that actually passed, not full completion.
