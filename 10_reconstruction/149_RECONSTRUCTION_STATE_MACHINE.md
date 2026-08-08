# Reconstruction State Machine

## R0 — INGEST
Zapis źródeł i segmentów.

## R1 — CLASSIFY EVIDENCE
Projection, view, material/detail/text.

## R2 — AUTHORITY
Evidence + View Authority Matrix.

## R3 — REGISTER
Skala, osie, image planes, camera.

## R4 — CONSTRAIN
Dimension Graph, landmarks, Feature Contract.

## R5 — DECOMPOSE + SHAPE GRAPH

Obowiązkowe:
- decompose asset na G0–G5 design forms;
- zbuduj `Reconstruction Shape Graph`;
- przypisz parent/dependencies;
- sklasyfikuj shape representation każdego required node;
- przypisz RDL;
- przypisz authoritative views i controlled properties;
- zdefiniuj node validation contracts.

`SHAPE_GRAPH` musi przejść structural validation przed produkcyjnym modelowaniem.

Nie pisz monolitycznego build scriptu tworzącego G1–G5 w tym stanie.

## R6 — RDL0 ENVELOPE
Bounds + contact datum + minimal silhouette carrier.

Wymagany proof przed advance:
- numeric bounds;
- registered envelope evidence dla authoritative FRONT/SIDE/TOP;
- QA scene isolation;
- `RDL0_BARRIER: PASS`.

## R7 — RDL1 PRIMARY FORMS

Buduj **node po node**:

```text
ready G1 node
-> build only node
-> required canonical views
-> numeric/section checks
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | FAIL
```

Obejmuje:
- primary body/shell;
- base/plinth;
- major structural shoulder/transition;
- primary negative space.

Po wszystkich required nodes:
`RDL1_STAGE_BARRIER`.

Nie wolno budować RDL2 przy FAIL required G1 node.

## R8 — RDL2 SECONDARY STRUCTURAL FORMS

Buduj oddzielnie:
- frames;
- display housing/recess mass;
- utility housing;
- large service panels;
- major trims/inserts.

Każdy node ma własny required-view gate.

Po wszystkich required nodes:
`RDL2_STAGE_BARRIER`.

## R9 — RDL3 STRUCTURAL FEATURES

Panels, openings, recesses, vents, structural grooves, light channels, handles, layered assemblies.

Leaf skills mogą być używane dopiero, gdy host node jest `ACCEPTED`.

Wymagany proof odpowiedni do feature class:
- ROI;
- numeric depth/position;
- visibility/layer stack;
- panel-line/path contract;
- regression outside expected-change region.

Po required nodes:
`RDL3_STAGE_BARRIER`.

## R10 — RDL4 EDGE LANGUAGE

Bevel, fillet, chamfer, corner radius, tangency, SubD support geometry.

Rule:

```text
correct shape first
-> edge treatment second
```

RDL4 nie może kompensować błędu RDL1/RDL2.

Po edge treatment re-check:
- protected dimensions;
- canonical silhouette;
- local feature boundaries.

`RDL4_STAGE_BARRIER` przed surface detail.

## R11 — RDL5 SURFACE / DETAIL

Branding, decals, microgeometry, materials, texture direction, weathering, emissive finish.

Readable branding/text wymaga canonical orientation proof z project handedness gdy dotyczy.

Dla target fidelity L4/L5 wymagany material segmentation proof.

RDL5 może mieć jawne deferred items zależnie od requested completion level, ale nie może zmieniać accepted primary form bez dirty propagation.

## R12 — MULTIVIEW QA + RECONSTRUCTION FIDELITY GATE

Kolejność:

```text
Shape Graph revision validation
-> all required node gates accepted
-> RDL stage barriers pass
-> QA_SCENE_ISOLATE
-> registered canonical view validators
-> hard dimensions
-> primary landmarks/proportions
-> MUST feature evidence
-> material segmentation when required
-> authority/deviation closure
-> RECON_FIDELITY_GATE
```

`RECON_FIDELITY_GATE` musi zwrócić proof-bearing PASS z provenance.

Bare `PASS`, `looks correct`, `matching the card` albo poprawny overall envelope nie pozwalają wejść do runtime.

## R13 — TOPOLOGY / RUNTIME PREP

Dopiero tutaj:
- topology cleanup/freeze;
- UV;
- runtime LOD;
- collision;
- bake;
- runtime material closure.

Ten etap jest niedostępny przy wcześniejszym barrier/fidelity FAIL.

## R14 — EXPORT VALIDATION

Sprawdź:
- package readback;
- runtime primitive attributes;
- node transform policy;
- export round-trip dimensions/contact;
- target engine evidence dopiero dla Level D.

## Backtracking

Każdy FAIL wraca do najwcześniejszego właściciela problemu.

Przykłady:

```text
SIDE primary contour FAIL
-> current G1 node / RDL1

base FRONT okay + SIDE/TOP corner fail after corrected retry
-> SHAPE_CLASSIFY representation review
-> possible MULTI_SECTION_LOFT

DISPLAY_RECESS host FAIL
-> RDL2; do not continue to glass/content

PANEL_LINE FAIL because host surface wrong
-> parent G1/G2 owner, not HS_PANEL_LINE tweaking

mirrored rear technical decal
-> RDL5 branding orientation owner

missing TEXCOORD_0 after export
-> runtime package/UV owner
```

## Monolithic-build prohibition

Regresja v0.9:

```text
analyze
-> build body + base + screen + vents + logo + bevel + materials
-> one QA render
```

Canonical:

```text
understand hierarchy
-> build one form
-> prove it
-> commit node acceptance
-> continue coarse-to-fine
```
