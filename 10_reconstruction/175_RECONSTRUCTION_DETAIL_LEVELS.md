# Reconstruction Detail Levels

## Cel

Oddzielić **coarse-to-fine reconstruction** od runtime LOD.

Agent nie zaczyna od kompletnego authoring mesh i nie dodaje wszystkich detali w jednym buildzie. Rekonstrukcja przechodzi przez jawne poziomy `RDL` (Reconstruction Detail Level), a każdy poziom ma własny zakres i gate.

`RDL` nie jest `LOD`.

```text
RDL = kolejność rozwiązywania formy z referencji
LOD = późniejsza optymalizacja runtime zaakceptowanego modelu
```

---

## RDL0 — ENVELOPE

Zakres:
- total width/depth/height;
- ground/contact datum;
- principal axes;
- global centerline;
- minimal silhouette carrier.

Zakazane:
- bevel;
- panel lines;
- screen internals;
- vents;
- logo;
- microdetail;
- final materials.

Gate:
- hard bounds;
- required FRONT/SIDE/TOP envelope projections;
- datum/contact.

---

## RDL1 — PRIMARY FORMS

Zakres:
- wszystkie `G1 PRIMARY_FORM` Shape Nodes;
- główne shells, body, bases, plinths, structural shoulders/transitions;
- major negative space, jeżeli definiuje primary silhouette.

Gate dla każdego node'a:
- wymagane canonical views;
- local silhouette/landmark contract;
- parent/contact relation;
- representation invariant;
- brak unresolved HARD conflict.

Po node-level PASS uruchom `RDL1_STAGE_GATE` dla całego zestawu primary forms.

Nie wolno wejść do RDL2 przy FAIL dowolnego required G1 node.

---

## RDL2 — SECONDARY STRUCTURAL FORMS

Zakres:
- side frames;
- display housings/recess masses;
- utility housings;
- large service panels;
- major trims;
- secondary structural inserts.

Każdy node nadal przechodzi własny multi-view/ROI gate.

RDL2 nie może zmieniać zaakceptowanej RDL1 silhouette poza jawnie zadeklarowanym expected-change region.

---

## RDL3 — STRUCTURAL FEATURES

Zakres:
- recesses;
- openings;
- vents;
- panel gaps;
- structural grooves;
- LED channels;
- handles/latches;
- functional cutouts;
- layered display stack.

Tutaj zaczynają być routowane leaf skills, np.:
- `HS_PANEL_LINE`;
- boolean recess playbook;
- `LAYER_STACK_VALIDATE`;
- radial repeat dla otworów/fastenerów;
- profile/sweep skills.

Host G1/G2 musi być wcześniej `ACCEPTED`.

---

## RDL4 — EDGE LANGUAGE

Zakres:
- bevel;
- fillet;
- chamfer;
- edge families;
- corner radius;
- local G0/G1 tangency;
- subdivision support geometry, gdy wymagane.

Rule:

```text
correct form first
-> edge treatment second
```

RDL4 nie może być używane do kompensacji błędnej RDL1/RDL2 formy.

Po RDL4 ponownie waliduj protected dimensions, silhouette i local feature boundaries.

---

## RDL5 — SURFACE / DETAIL

Zakres:
- branding;
- decals;
- screws i micro-fasteners;
- micro-grooves;
- materials;
- texture direction;
- weathering;
- emissive finish;
- cosmetic variation.

RDL5 może być częściowo deferred do późniejszego `SURFACE_FINISH`, zależnie od target completion level, ale nie może nadpisywać geometrii zaakceptowanej na RDL0–RDL4.

---

## Stage barrier

Canonical transition:

```text
RDL0 PASS
-> RDL1 node-by-node PASS
-> RDL1_STAGE_GATE PASS
-> RDL2 node-by-node PASS
-> RDL2_STAGE_GATE PASS
-> RDL3 node-by-node PASS
-> RDL3_STAGE_GATE PASS
-> RDL4 PASS
-> RDL5 PASS / allowed defer
-> RECON_FIDELITY_GATE
-> runtime topology/LOD/UV/bake/export
```

Nie przeskakuj poziomu tylko dlatego, że kolejny detal jest łatwy do wykonania.

---

## One-level mutation rule

Jedna transakcja wykonawcza nie może tworzyć nowych produkcyjnych node'ów z wielu RDL, chyba że są one nieodłącznie jednym atomowym feature contractem i zostało to jawnie zapisane.

Domyślne zachowanie:

```text
one Shape Node
-> one build/repair transaction
-> one validation result
```

Monolityczne:

```text
build body + base + screen + vents + logo + bevel + materials
```

jest regresją v0.9.

---

## Relation to runtime LOD

Dopiero zaakceptowany authoring model może generować:

```text
LOD0
LOD1
LOD2
LOD3
```

RDL1/RDL2 mogą być źródłem wiedzy dla uproszczonych LOD, ale nie są runtime assetami i nie muszą mieć tej samej topologii.

---

## Persistent state

Po każdym gate zapisuj:

```yaml
rdl_state:
  level: RDL1
  graph_revision: sg_004
  accepted_nodes: [PRIMARY_BODY, BASE_PLINTH]
  blocked_nodes: [LOWER_SHOULDER]
  dirty_nodes: []
  stage_status: FAIL
```

Nie opieraj postępu na historii rozmowy ani tym, że obiekt "już jest w scenie".
