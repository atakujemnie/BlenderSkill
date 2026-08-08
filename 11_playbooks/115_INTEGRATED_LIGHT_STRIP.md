# Playbook — Integrated Light Strip

## Purpose

Build reference-faithful guidance/accent light features while separating physical asset authoring from engine glow/post-processing.

Use with `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md`.

---

# Geometry

Define explicitly:
- recess/host opening if one exists;
- diffuser/cover;
- emitting surface or emissive material region;
- protective lips;
- ends/corners;
- depth relationship to host surface.

The strip may be:
- flush;
- recessed;
- slightly proud;
- protected by a surrounding lip.

Reference evidence decides.

A floating emissive patch cannot create a recess in an opaque host mesh.
If negative depth matters, model/cut/bake the recess according to feature scale and runtime needs.

---

# Visibility contract

The feature must be visible because its geometry/material relationship is correct, not because the agent made emission arbitrarily huge.

Validate:
- emitter is not behind the host wall;
- diffuser faces the expected view region;
- band thickness is consistent;
- no z-fighting;
- the intended 360°/partial-arc continuity is correct;
- emitted color survives QA tone mapping.

For a 360° guidance ring, inspect at least front + side + 3/4.

---

# Material

Record separately:

```yaml
light_feature:
  feature_id: F_LIGHT_01
  geometry: PASS
  diffuser: PASS
  emissive_color: [r, g, b]
  blender_preview_strength: 2.4
  runtime_strength: UNVERIFIED
  runtime_bloom: UNVERIFIED
```

Blender emission intensity is a lookdev parameter unless the target engine defines a calibrated transfer.

Do not burn the emitter to white if the reference requires a saturated blue/cyan line.

---

# Authoring vs runtime

Asset authoring owns:
- geometry;
- emissive mask/material assignment;
- color intent;
- UV/texture data;
- exported material binding.

Runtime owns or may modify:
- bloom;
- exposure;
- tone mapping;
- HDR response;
- actual scene-light contribution;
- distance-dependent post-process.

Therefore a Blender render proving a blue strip exists does not prove the in-game neon look is finished.

---

# Bloom

Do not paint a large glow halo into BaseColor.
Normally the texture describes the emitter and the engine generates bloom.

If a stylized reference explicitly contains a painted halo that must remain independent of post-process, treat that as separate art direction evidence.

---

# QA

Use two QA modes:

### `EMISSIVE_AUTHORING`
- neutral exposure;
- bloom disabled or minimized;
- prove geometry/mask/color;
- detect clipping and occlusion.

### `EMISSIVE_LOOKDEV`
- representative exposure/post-process;
- judge perceived glow only after authoring pass.

Do not modify geometry to compensate for a failed `EMISSIVE_LOOKDEV` lighting setup unless geometry evidence also fails.

---

# LOD

The emitter's visual signal may survive farther than its housing detail.

LOD policy:
- preserve visible color signal while it matters on screen;
- simplify/remove diffuser recess geometry when sub-pixel;
- keep ring/marker aligned with the simplified silhouette;
- avoid tiny flickering floating surfaces.

A low LOD may represent the strip as a simpler emissive band even if LOD0 has a separate diffuser assembly.

---

# Export/runtime gate

Before `GAME_READY_COMPLETE`:
- emissive data survives export;
- the exported material/texture actually references the emissive mask/color;
- no dependency on Blender-only procedural nodes remains undefined;
- runtime interpretation is verified by Engine Profile or marked `UNVERIFIED`.

If the engine's bloom/post-process is not part of the Blender agent's capability, do not block asset authoring — but report that final runtime glow still requires engine validation.
