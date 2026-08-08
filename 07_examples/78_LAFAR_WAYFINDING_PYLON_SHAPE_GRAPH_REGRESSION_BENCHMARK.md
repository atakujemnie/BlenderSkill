# Lafar Wayfinding Pylon — Shape Graph Regression Benchmark

## Purpose

Drugi benchmark `ACS-WP-3470`, tym razem dotyczący **rozumienia formy i kolejności konstrukcji**.

v0.8 powstało po ~67k-tokenowym runie i naprawiło proof-bearing reconstruction QA. Kolejna ręczna inspekcja finalnego pylona ujawniła jednak błąd wcześniejszy: system potrafił wykrywać fidelity failure, ale nadal budował złożone formy jako luźne zbiory boxów/beveli i tworzył wiele poziomów detalu w jednym monolitycznym skrypcie.

## Observed failure

Concept base/lower transition jest spójnym hard-surface assembly:

```text
narrow body
-> diagonal structural shoulder
-> widening collar/plinth
-> broad base
-> lower lip
```

Przekrój zmienia jednocześnie:
- width;
- depth;
- corner treatment;
- chamfer/transition behavior.

v0.8-era model reprezentował tę formę głównie przez:
- stacked boxes;
- wedges;
- bevels;
- overlapping local pieces.

W FRONT część relacji mogła wyglądać plausibly, ale corner language i 3D transition nie odpowiadały conceptowi.

## Root cause A — no persistent form hierarchy

Biblioteka mówiła `primary forms before detail`, ale nie wymagała trwałego modelu hierarchii.

Agent mógł przejść:

```text
analyze
-> build body + base + display + decals + vents + bevels
-> quick QA
```

bez proof, że każda primary form została osobno rozwiązana.

## Root cause B — operator-first representation

Istniały skille do:
- panel lines;
- SubD;
- bevel/edge treatment;
- booleans;
- materials;

ale brakowało warstwy:

```text
what mathematical class of shape is this?
```

W efekcie trudny base był traktowany jako `box + bevel`, mimo że evidence wymagało `MULTI_SECTION_LOFT`.

## Root cause C — validation too late

Cały asset był oceniany po dodaniu wielu elementów. Błąd base powinien zostać wykryty przy RDL1, zanim istnieją:
- screen content;
- logo;
- vents;
- panel seams;
- materials;
- runtime LOD.

## v0.9 required architecture

```text
REFERENCE EVIDENCE
-> SHAPE GRAPH
-> RDL0 ENVELOPE
-> node gate
-> RDL1 PRIMARY FORMS, one node at a time
-> stage barrier
-> RDL2 SECONDARY STRUCTURAL FORMS
-> stage barrier
-> RDL3 STRUCTURAL FEATURES
-> RDL4 EDGE LANGUAGE
-> RDL5 SURFACE DETAIL
-> final RECON_FIDELITY_GATE
-> runtime
```

## Example target graph

```text
PYLON [G0]
├── PRIMARY_BODY [G1, EXTRUDED_PROFILE]
├── BASE_PLINTH [G1, MULTI_SECTION_LOFT]
├── LOWER_SHOULDER [G1, MULTI_SECTION_TRANSITION]
├── SIDE_FRAME [G2, PROFILE_SWEEP]
├── DISPLAY_ASSEMBLY [G2]
│   ├── DISPLAY_RECESS [G3, BOOLEAN_RECESS]
│   ├── GLASS [G3, LAYERED_ASSEMBLY]
│   └── CONTENT [G3, LAYERED_ASSEMBLY]
├── FRONT_UTILITY_MODULE [G2]
└── REAR_SERVICE_ASSEMBLY [G2]
```

## Representation regression

For base/plinth:

```text
width changes with Z = true
depth changes with Z = true
corner treatment changes with Z = true
```

Expected:

```text
shape_class = MULTI_SECTION_LOFT
preferred_skill = SECTION_LOFT_HARD_SURFACE
```

Regression if:

```text
primary_strategy = STACKED_BOXES / PARAMETRIC_BOX + BEVEL
```

without evidence proving equivalence across canonical views/sections.

## Node-level QA target

Before any RDL2 child:

```yaml
RDL1:
  PRIMARY_BODY: ACCEPTED
  BASE_PLINTH: ACCEPTED
  LOWER_SHOULDER: ACCEPTED
  stage_barrier: PASS
```

Each accepted node must have its own proof-bearing required-view records.

## v0.9 regression targets

```yaml
v0_9_targets:
  production_geometry_created_before_shape_graph: 0
  monolithic_transactions_spanning_multiple_rdl: 0
  child_nodes_built_on_failed_parent: 0
  must_primary_nodes_without_per_view_gate: 0
  box_abuse_for_multisection_primary_form: 0
  specialist_detail_skill_invoked_before_host_acceptance: 0
  rdl_stage_barrier_bypasses: 0
  runtime_started_before_recon_fidelity_pass: 0
```

Operational target for similar civic prop:
- initial Shape Graph <= 5k tokens;
- RDL0/RDL1 solve uses only node-relevant modules;
- first primary-form mismatch is detected before RDL2;
- representation switch occurs after at most one corrected retry when evidence shows the original shape class is insufficient.

## Release implication

v0.9 jest udane, gdy następny complex reference asset nie tylko odrzuca błędny model, lecz **najpierw rozumie jego hierarchię brył, buduje primary forms oddzielnie i dobiera właściwą reprezentację geometrii przed detalem**.
