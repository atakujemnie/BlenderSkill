# Playbook — Civic Hard-Surface Assets

## Scope

Reusable playbook for maintained urban/civic props:
- benches and seating;
- bollards/posts;
- waste/recycling units;
- kiosks/terminals;
- wayfinding pylons;
- lighting/support fixtures;
- small infrastructure enclosures.

The first decision is not "which modifier?". It is **which structural family describes the asset**.

---

# Structural subtype routing

## A. `AXISYMMETRIC_CIVIC_PROP`

Typical:
- bollard;
- round post;
- cylindrical beacon;
- stacked circular housing;
- lamp/pedestal with rotational body.

Prefer:
- `03_modeling/45_AXISYMMETRIC_PROFILE_ASSET_PRIMITIVE.md`;
- explicit radius/Z profile;
- radial repetition for anchors/fasteners;
- separate asymmetric feature owners for panels/logo/local emitters.

Do not write a new one-off `lathe()` implementation if the reusable executor covers the geometry.

## B. `BOX_PROFILE_CIVIC_PROP`

Typical:
- recycling unit;
- kiosk;
- rectangular terminal;
- modular cabinet.

Prefer:
- dimension-locked box/profile blockout;
- bevel/boolean/panel-line semantic skills;
- modular repeated subassemblies.

## C. `FRAME_PANEL_CIVIC_PROP`

Typical:
- bench;
- shelter component;
- barrier/rail module;
- pylon with structural frame and skins.

Prefer:
- structural frame first;
- separate panels/skins;
- repeated supports/fasteners;
- explicit junction logic.

A single asset may combine families. Route by feature owner, not by one global technique.

---

# Primary production order

```text
reference authority
-> dimensions/bounds
-> primary structural family
-> blockout
-> silhouette gate
-> primary manufacturing transitions
-> service/access logic
-> secondary detail
-> material segmentation
-> material breakup/lookdev
-> UV/bake/runtime materials
-> LOD/collision
-> export/integration
```

Do not start wear, screws or microdetail before primary silhouette passes.

---

# Typical components

- structural shell/frame/body;
- seat/backrest where applicable;
- base/mounting flange;
- feet/anchors;
- service collar/panel;
- trim;
- utility/electronics;
- signage/branding;
- integrated light/accent;
- underside/ground interface.

Every characteristic component should map to a Feature ID.

---

# Manufacturing logic

Civic assets should read as manufactured and serviceable.

Ask:
- what is one manufactured part versus an assembly?
- which component is removable?
- where are seams justified?
- which fasteners are structural versus decorative?
- what protects an emitter/display?
- how is the asset anchored?
- which surfaces are exposed to handling/weather?

Do not scatter arbitrary panel lines merely to make the asset look "sci-fi".

---

# Fasteners and repeated details

Repeated bolts/anchors should use a reusable radial/linear repetition strategy where possible.

For circular flanges, validate **annulus containment**:

```text
inner_available_radius <= fastener_min_radius
fastener_max_radius <= outer_available_radius
```

Do not accept fasteners that numerically intersect the bevel/lip even if the hero view hides the error.

At lower LODs:
- reduce fastener segments;
- remove individual fasteners when sub-pixel and permitted;
- move shallow detail into normal/texture representation.

---

# Floating/local details

Use `03_modeling/41_DECALS_AND_FLOATING_DETAILS.md`.

Critical civic-prop rule:
- a floating plate can represent an additive panel/graphic;
- it cannot cut a true recess into the host;
- a local emitter hidden behind a base wall fails even if its emissive material is correct.

Require visibility proof for `SURFACE_DETAIL` features.

---

# Materials

Typical families:
- dark composite/powder coat;
- brushed aluminium/metal trim;
- rubberized impact material;
- polycarbonate/light diffuser;
- emissive accent;
- decals/etched graphics.

Use `11_playbooks/114_BRUSHED_METAL_AND_DARK_COMPOSITE.md` for surface breakup.

Civic material target:

```text
maintained + durable + subtly used
```

Avoid both:
- sterile perfectly uniform CG surfaces;
- exaggerated abandoned/grunge treatment.

---

# Integrated lighting

Use `11_playbooks/115_INTEGRATED_LIGHT_STRIP.md` and `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md`.

Asset authoring owns emitter geometry/mask/color.
Final neon/bloom response may belong to runtime post-processing.

Do not bake bloom into BaseColor by default.

---

# Branding

If authoritative corporate artwork exists:
- use the provided source;
- preserve mark proportions;
- adapt layout only where the product reference explicitly shows a different lockup;
- do not approximate a supplied logo with ad-hoc geometry/font substitutes.

Prefer decal/atlas representation when geometry would waste triangle budget or misrepresent printed/etched branding.

---

# Game-ready finishing

Before calling the asset game-ready:
- LOD budgets pass;
- collision contract passes;
- UV/material strategy complete;
- procedural lookdev has a runtime disposition;
- required bakes pass `04_game_ready/50_GAME_READY_BAKE_GATE.md`;
- emissive export survives;
- branding/decal textures survive export;
- pivot/scale/naming pass;
- post-export validation passes.

Use completion levels from `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md`.

---

# QA views

Minimum for most static civic assets:
- front;
- side;
- top;
- rear when different;
- bottom when reference/runtime requires it;
- 3/4;
- close-up for mounting/service/light details.

The close-up is not decorative. It is where annulus overflow, z-fighting, hidden emitters and service-panel depth problems often become visible.

---

# Efficiency

Before generating custom infrastructure, check reusable skills/executors:
- axisymmetric profile;
- mesh validator;
- panel line;
- SubD topology control;
- reference measurement;
- QA isolation/runtime compatibility helpers.

Generated build/QA scripts are persistent code artifacts. Do not echo their complete source back into model context after creation.

---

# Completion

A clean Blender render can satisfy reconstruction/modeling and still fail game-ready completion.

Explicitly report:

```text
RECONSTRUCTION_COMPLETE
MODELING_COMPLETE
GAME_READY_COMPLETE
PIPELINE_INTEGRATED
```

Never merge these into one ambiguous `DONE` state.
