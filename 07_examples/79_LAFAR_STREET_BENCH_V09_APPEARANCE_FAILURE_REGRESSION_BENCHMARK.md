# Benchmark — Lafar Street Bench v0.9 Appearance-Fidelity Failure

## Purpose

This benchmark is the release driver for BlenderSkill v0.10.0.

It records a critical failure mode not prevented by v0.9:

```text
hard dimensions PASS
+ outer silhouette PASS
+ many locally authored numeric gates PASS
+ LOD/export/package PASS
!=
faithful reconstruction
```

The asset was the Lafar Street Bench / Astera Civic Systems ACS-BCH-200. The run used BlenderSkill v0.9 and produced a technically coherent, game-ready package, but the user rated the visual result **6/10** and identified the side modules, styling and finish as substantially wrong.

The benchmark therefore treats the v0.9 result as **RECONSTRUCTION FAIL despite downstream technical success**.

---

## Source set

Required evidence:
- technical/dimension sheet with FRONT/SIDE/REAR/TOP/BOTTOM/detail views;
- presentation concept sheet / hero view;
- technical prompt;
- final benchmark renders from the v0.9 run;
- execution trace from the v0.9 run.

Canonical hard dimensions in the run:
- width 2000 mm;
- depth 550 mm;
- height 820 mm;
- seat height 460 mm.

The v0.9 run measured the final envelope approximately:
- FRONT 1998.9 x 820.7 mm;
- SIDE 550.1 x 819.5 mm;
- TOP 1998.9 x 551.2 mm;

and declared the silhouette gate PASS.

These results are retained as proof that **global envelope correctness is not enough**.

---

## What v0.9 did well

### T01 — hard dimensions
PASS.

The run correctly prioritized explicit dimensions and kept the final assembly inside the 2000 x 550 x 820 mm envelope.

### T02 — single coherent 3D object
PASS.

FRONT/SIDE/REAR/TOP/BOTTOM were generated from one model rather than view-specific fake geometry.

### T03 — representation-first reasoning
PARTIAL PASS.

The side support was not left as a trivial box. The agent used a multi-section / profile-driven strategy and discovered real geometric failure cases such as:
- tangent point vs arc extremum;
- bevel expanding protected bounds;
- low segment counts degenerating booleans.

### T04 — runtime closure
PASS.

The run eventually produced LODs within budget, collision, UV attributes and clean glTF readback.

These are valuable technical successes. They do not certify reconstruction fidelity.

---

## Primary visual failures

### V01 — side housing silhouette and internal shape language
Severity: MUST / D1.

The final side module reads as a large smooth monolithic slab with an oversized continuous front arc.

The reference shows a more engineered assembly:
- front protective corner with controlled radius;
- broad but bounded metallic trim/cap;
- dark composite side panel with flatter planes;
- distinct lower plinth;
- visible panel boundaries;
- more deliberate transition into the rear/backrest structure.

The outer envelope can still match 550 x 820 while these internal boundaries are wrong.

### V02 — aluminium trim path
Severity: MUST / D2.

The reference trim is a major design feature. It wraps the side assembly as a continuous manufactured path and defines the product family.

The final model reduced it to a narrow/highlight-like strip and did not reproduce the same:
- width distribution;
- path;
- corner wrapping;
- adjacency to dark composite panels;
- continuation toward the backrest/end-cap.

### V03 — side/backrest transition
Severity: MUST / D1-D2.

The reference has a layered shoulder/end-cap transition. The final model uses a simplified wedge/fin and loses the stepped relationship between:
- side housing;
- metallic cap;
- dark shoulder panel;
- backrest shell.

### V04 — rear assembly
Severity: MUST / D2.

The reference rear view contains a clear assembly graph:
- central rear panel;
- horizontal service bands;
- angled transitions into side modules;
- metallic vertical edge families;
- lower rear cover relationship;
- logo placement inside that panel structure.

The final rear is mostly a flat large panel plus a single horizontal slab. The geometry is technically valid but architecturally wrong.

### V05 — seat edge language
Severity: MUST / D1-D4.

The final seat reads too soft and capsule-like. The reference is hard-surface with tighter product radii, planar faces and sharper layer separation.

### V06 — info strip scale and integration
Severity: SHOULD/MUST depending target fidelity.

The final info strip is visually dominant and framed as a large rectangular display. The reference uses a thinner, more integrated strip with subtler border hierarchy.

### V07 — utility panel treatment
Severity: SHOULD/MUST.

Placement is approximately correct, but the panel language is generic and blocky. The reference shows a restrained service interface integrated into the side panel.

### V08 — underglow behavior
Severity: SHOULD/MUST.

The final cyan emitters are too continuous/exposed and read as bright tubes. The reference shows recessed orientation lighting integrated into base/underside architecture.

### V09 — material identity
Severity: MUST for L4/L5.

The final materials are mostly flat Principled placeholders. The run itself explicitly reported missing:
- brushed aluminium anisotropy;
- graphite/composite microtexture;
- roughness breakup;
- usage/weathering evidence.

The reference depends heavily on the contrast between matte dark composite and directional brushed aluminium.

### V10 — detail completeness
Severity: MUST for L5.

Many visible reference details were omitted or simplified:
- panel seams;
- lower plinth segmentation;
- fastener/service cues;
- rear service bands;
- trim boundary steps;
- underside-specific assembly cues;
- local shadow gaps and junctions.

The failure is not 'missing microdetail' only. Several omitted details are design-defining meso-scale features.

---

## Root-cause analysis

### R01 — circular validation

The run created local numeric assumptions and then validated geometry against those same assumptions.

Pattern:

```text
infer R165 / 8.1 deg / custom station positions
-> build using those values
-> local Gate checks those same values
-> PASS
```

This proves implementation consistency, not reference fidelity.

A derived parameter can be useful, but acceptance must be anchored back to registered source evidence.

### R02 — local ad-hoc gates shadowed canonical validators

The run implemented its own `Gate` class and reported 70+ accepted checks.

BlenderSkill v0.9 already required `RECONSTRUCTION_NODE_GATE`, registered view comparison and proof-bearing provenance. The local gate did not provide equivalent reference-anchored evidence.

v0.10 must treat a local substitute as non-authoritative when a canonical validator exists.

### R03 — silhouette metric only covered the outer envelope

Alpha silhouette validation can prove overall bounds and external contour. It cannot prove:
- internal part boundaries;
- trim paths;
- material borders;
- panel seams;
- junction architecture;
- edge-family identity.

The Street Bench demonstrates that a high silhouette score can coexist with a wrong product design.

### R04 — Shape Graph nodes were too coarse for style-critical boundaries

`SIDE_MODULE` as one accepted node hid multiple reference-defining subregions.

The benchmark requires explicit ownership for:
- outer shell;
- front protective corner;
- aluminium cap/trim;
- side composite panel;
- plinth;
- shoulder/end-cap;
- service-panel boundary.

### R05 — G4 edge language was under-specified

The run treated edge work mainly as 'protected dimensions survive the bevel/rim'.

That is necessary but insufficient. Edge language is itself reference evidence:
- radius family;
- chamfer/fillet type;
- where the radius begins/ends;
- hard-to-soft transition ordering;
- continuity across material/part boundaries.

### R06 — G5 surface was accepted as material assignment, not appearance reconstruction

Assigning the correct material name is not proof of:
- roughness response;
- anisotropy direction;
- micro-normal scale;
- material-region boundary;
- emissive intensity/readability;
- wear/detail hierarchy.

### R07 — runtime work began before true appearance lock

Substantial effort went into LOD/export/UV/package validation while the reference match was still visually weak.

v0.10 must make the runtime boundary depend on a canonical appearance-fidelity PASS, not on technical confidence.

---

## v0.10 regression requirements

The benchmark passes only when all of the following are true.

### B01 — no self-certification
Every required node/view acceptance record names:
- canonical validator_id;
- provenance_id;
- source_reference_id for reference-derived evidence;
- registration_id for projected image evidence.

A local builder `PASS` does not count.

### B02 — part-boundary graph
Reference-defining internal boundaries are explicitly modeled and validated per canonical view.

For the Street Bench this includes at minimum:
- side shell / trim boundary;
- side shell / plinth boundary;
- side shell / shoulder-endcap boundary;
- seat / support junction;
- backrest / side-endcap junction;
- rear-panel horizontal service boundaries.

### B03 — trim-path proof
Metal trim uses path/width/continuity evidence, not object existence.

### B04 — edge-family proof
RDL4 cannot pass by checking only protected dimensions. Required edge families need reference-anchored profile evidence.

### B05 — material appearance proof
For target fidelity L4+ material segmentation plus appearance identity is required.

For this benchmark:
- dark composite and aluminium must remain visually distinct under neutral calibrated lighting;
- brushed aluminium directionality must be visible;
- emissive must remain recessed/subtle rather than functioning as silhouette repair.

### B06 — detail coverage
All MUST meso/detail features from the reference inventory are accounted for as:
- PASS;
- explicitly NOT_REQUIRED by authority;
- or blocking deviation.

Missing reference features cannot silently disappear from the graph.

### B07 — final matched-camera review
At least FRONT, SIDE, REAR and HERO require final matched/registered comparison appropriate to their authority.

### B08 — runtime lock
LOD/UV/bake/export is forbidden while canonical appearance fidelity is FAIL or UNVERIFIED.

---

## Benchmark score model

Technical engineering and visual reconstruction are reported separately.

```text
TECHNICAL_PIPELINE_SCORE
REFERENCE_FIDELITY_SCORE
```

A high technical score cannot average away a failed reference score.

For release acceptance:

```text
REFERENCE_FIDELITY_SCORE >= 8.5/10
and
no MUST visual owner FAIL/UNVERIFIED
```

The user rating of the v0.9 run is recorded as:

```text
REFERENCE_FIDELITY_SCORE = 6/10
benchmark_status = FAIL
```

The score is not a replacement for objective evidence. It is an external regression oracle showing that the previous evidence model was incomplete.

---

## Release lesson

v0.9 solved:

```text
what forms exist?
in what order are they built?
which mathematical representation should build them?
```

v0.10 must additionally solve:

```text
which visible boundaries make this the same product?
which source evidence proves each boundary?
which edge/material/detail families define the design language?
is validation independent from the builder's own assumptions?
```

The Street Bench is the canonical v0.10 appearance-fidelity benchmark.