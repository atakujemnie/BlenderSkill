# Playbook — Brushed Metal + Dark Composite

## Purpose

Create convincing maintained civic hard-surface materials that are neither sterile nor covered in generic grunge.

The material must preserve the reference's **material identity** before adding variation.

```text
material identity
-> manufacturing response
-> scale-aware breakup
-> exposure/use logic
-> restrained wear
```

Random noise is not a material model.

---

# Brushed metal

Control:
- metallic response;
- roughness range;
- brushing direction;
- fine normal/roughness variation;
- edge highlight behavior;
- large-scale cleanliness variation.

Do not paint a fixed highlight into BaseColor.
The directional highlight must follow lighting and surface orientation.

## Brushing direction

The direction should follow manufacturing logic:
- cylindrical sleeve: typically circumferential or axial depending on evidence;
- flat trim: typically one stable planar direction;
- machined ring: may use circumferential direction.

Reference wins.

If direction is unknown, keep it subtle rather than inventing a dominant pattern.

---

# Dark composite / powder coat / rubberized civic body

First classify the material:
- dielectric composite;
- coated metal;
- rubberized impact material;
- dark titanium/metal-like composite;
- project-specific hybrid.

Do not set metallic merely because the reference has a bright highlight.

Control:
- low base-color variation;
- broad roughness variation;
- subtle micro-normal breakup;
- controlled edge response;
- protected-joint dirt;
- sparse handling/service wear.

A dark body should not become medium grey solely because the QA rig is overpowered.
Fix exposure/lighting before changing the base material family.

---

# Three-scale breakup model

Avoid one Noise Texture driving every channel.
Use different spatial scales with different responsibilities.

### Macro — ~0.1–1 m scale
Purpose:
- broad manufacturing/cleaning variation;
- subtle exposure differences;
- very low-amplitude roughness drift.

Must not look like clouds painted on the asset.

### Meso — ~5–80 mm scale
Purpose:
- wipe/maintenance variation;
- localized roughness changes;
- protected-area dirt;
- faint streaking aligned with gravity/use where appropriate.

### Micro — sub-mm to few-mm scale
Purpose:
- powder-coat grain;
- brushed microstructure;
- molded/rubberized texture;
- tiny normal/roughness breakup.

Micro detail should not alter primary silhouette.

---

# Channel separation

Do not use one noise value identically for BaseColor, Roughness and Normal.

Preferred:

```text
BaseColor  -> very low amplitude, low frequency
Roughness  -> primary variation channel
Normal     -> high-frequency material structure
AO/dirt    -> geometry/exposure-driven mask
Wear       -> sparse edge/contact/service mask
```

This reduces the "procedural plastic" look.

---

# Wear logic

Civic infrastructure can be clean and maintained while still showing subtle history.

Possible wear zones:
- service collar contact boundary;
- removable panel perimeter;
- anchor/base plate around maintenance access;
- exposed outer base edge;
- top trim touched during servicing;
- drainage/ground-facing interface.

Avoid:
- uniform edge damage everywhere;
- white scratches on every convex edge;
- random dirt equally distributed over top and protected underside;
- heavy apocalypse-style grunge unless reference/brief asks for it.

Target:

```text
maintained
used
materially varied
not pristine-CGI
not abandoned
```

---

# Dirt accumulation

Dirt should be driven by plausible collection areas:
- concave seams;
- protected horizontal ledges;
- base/ground transition;
- underside of projecting lips;
- service interfaces.

Do not fake deep geometric seams using dark albedo bands if the reference requires real parallax.

---

# Brushed aluminium specifics

For a bright aluminium collar:
- keep BaseColor physically plausible/neutral rather than pure white;
- use metallic response to generate highlights;
- preserve brushed direction;
- roughness breakup should remain subtle enough that it still reads as precision trim;
- edge radius controls highlight width and is a geometry concern, not a texture substitute.

---

# Dark-surface QA

Validate material under at least:
- neutral studio lighting;
- grazing/highlight angle;
- low-contrast view;
- material-only close-up.

Questions:
- does the surface become featureless black?
- does it become generic mid-grey?
- can roughness variation be perceived without obvious procedural blobs?
- does microtexture remain below silhouette scale?
- is the material still recognizable after mip/distance reduction?

---

# Reference fidelity

Material variation must not override evidence.

If the concept art looks slightly irregular, infer only the **type and scale** of variation that is supported.
Do not reproduce lighting noise or compression artifacts as texture.

Use `10_reconstruction/125_LIGHTING_VS_MATERIAL_DISENTANGLEMENT.md` before promoting image brightness variation into material data.

---

# Runtime/bake handoff

For every procedural component choose:
- BAKE;
- RECREATE_IN_ENGINE;
- EXPORT_NATIVELY_VERIFIED;
- REMOVE_BY_DESIGN.

Use `04_game_ready/50_GAME_READY_BAKE_GATE.md`.

Typical game-ready outputs for this material family may include:
- BaseColor with restrained low-frequency variation;
- Normal with microstructure and approved small details;
- ORM with roughness breakup and AO where appropriate;
- Emissive separately for lighting features.

Do not call the material game-ready while its defining variation exists only in Blender procedural nodes and no runtime replacement is verified.

---

# Acceptance target

A successful material should read correctly at three distances:

```text
far      -> correct color/material family and silhouette
medium   -> material separation + broad roughness behavior
close    -> microstructure + subtle wear/maintenance evidence
```

If close-up quality comes from noise that disappears into an obviously sterile medium-distance surface, the breakup hierarchy is incomplete.
