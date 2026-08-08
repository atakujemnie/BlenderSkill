# Emissive Authoring and Runtime Handoff

## Purpose

An emissive strip has two separate responsibilities:

```text
ASSET AUTHORING
geometry + mask + color + material segmentation

RUNTIME PRESENTATION
bloom + exposure + tone mapping + scene-light contribution
```

Do not confuse them.

A Blender preview can prove the emissive feature exists and is correctly authored. It cannot prove the target game runtime will produce the same glow unless the Engine Profile and runtime post-process are known.

---

# Asset-side responsibilities

The Blender/game asset must define:
- exact emitting region;
- diffuser/cover geometry if present in the reference;
- emissive mask or material region;
- intended emissive color in a documented color space;
- relative strength class (`SUBTLE`, `GUIDANCE`, `SIGNAGE`, `HIGH_INTENSITY` or project-specific equivalent);
- whether the material should visibly glow when unlit;
- whether actual scene illumination is required or only self-emission.

The emitting region must pass visibility QA.

An emissive object hidden behind host geometry is a geometry failure, even if its material node reports a non-zero emission strength.

---

# Blender lookdev responsibility

Blender preview is used to validate:
- the band/marker is visible in the intended views;
- its hue survives color management;
- the feature is not clipped to featureless white under the QA rig;
- surrounding material does not become artificially recolored in base color;
- the emitter does not compensate for wrong geometry.

The preview strength is a **lookdev parameter**, not automatically a runtime constant.

Record it as:

```yaml
emissive_authoring:
  feature_id: F007
  color_rgb: [0.055, 0.517, 1.0]
  blender_strength: 2.4
  purpose: GUIDANCE
  visibility: PASS
  clipping: PASS
```

---

# Runtime responsibility

Final glow can depend on:
- bloom/post-processing;
- exposure;
- tone mapping;
- HDR range;
- emissive shader implementation;
- whether emissive contributes to indirect/direct scene lighting;
- temporal AA/upscaling;
- distance and screen size.

Therefore:

```text
EMISSIVE_AUTHORING_PASS != RUNTIME_GLOW_PASS
```

If runtime behavior is unknown, mark:

```yaml
runtime_emissive:
  status: UNVERIFIED
  reason: ENGINE_PROFILE_OR_POSTPROCESS_UNKNOWN
```

---

# Bloom policy

Do not bake bloom halos into BaseColor or Emissive textures unless the art direction explicitly requires a stylized painted halo.

Normally:
- texture/mask describes the emitter;
- runtime bloom generates the optical/post-process halo.

This preserves correct response across distance, exposure and lighting conditions.

---

# Color preservation

A blue/cyan guidance light that turns white in the QA render is not automatically acceptable.

Diagnose in this order:
1. emission strength;
2. exposure/tone mapping;
3. QA light rig;
4. material color;
5. runtime bloom only after authoring values are stable.

Do not solve clipping by making the geometry larger unless the reference supports larger geometry.

---

# LOD behavior

An emissive feature may be visually important at distances where its physical housing is sub-pixel.

LOD policy may therefore separate:
- `EMITTER_SIGNAL` — preserve color/visibility;
- `EMITTER_HOUSING` — simplify/remove with distance.

At low LOD, a simple emissive band can replace detailed diffuser geometry if the protected silhouette and visual identity remain correct.

---

# Game-ready gate

Before `GAME_READY_COMPLETE`:
- emissive texture/material export is verified;
- exported asset actually references the emissive data;
- Engine Profile states how emissive is interpreted, or runtime remains `UNVERIFIED`;
- no Blender-only node behavior is silently assumed to survive export.

If the project requires bloom/light contribution but these runtime settings are not under Blender control, the asset may still pass authoring while pipeline integration remains pending.
