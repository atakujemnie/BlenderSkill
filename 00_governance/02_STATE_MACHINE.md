# Agent State Machine

## v0.12 geometric-integrity amendment

This amendment has precedence over v0.11 where the rules differ.

Canonical production-node transition is now:

```text
DECLARED -> CONSTRAINED
CONSTRAINED -> READY_TO_BUILD          only via EXECUTION_AUTHORIZATION_GATE
READY_TO_BUILD -> authorized mutation
mutation -> MUTATION_POSTCONDITION_GATE
MUTATION_POSTCONDITION_GATE PASS -> BUILT_UNVERIFIED
BUILT_UNVERIFIED -> source QA + ASSEMBLY_INTEGRITY_GATE
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | UNVERIFIED | FAIL
```

`LOCAL_BUILDER: PASS` is never enough to reach `BUILT_UNVERIFIED`. An authorized mutation must prove that its intended geometric postcondition actually occurred. For assembly nodes, semantic relation integrity is non-compensating: unintended interpenetration, invalid gap/contact/embedding or a missing relation contract blocks acceptance.

When an accepted host is repaired, run `DEPENDENCY_INVALIDATOR` before new work: affected descendants become `DIRTY/BLOCKED`, hosted Appearance Owners become `UNVERIFIED`, and revision-bound evidence becomes `SUPERSEDED`. Stale green evidence cannot survive a geometry revision.

---

## v0.11 execution-enforcement amendment

This amendment supersedes any weaker execution wording below while preserving the full v0.10 state-machine knowledge.

Canonical reconstruction node transition:

```text
DECLARED -> CONSTRAINED
CONSTRAINED -> READY_TO_BUILD       only via EXECUTION_AUTHORIZATION_GATE
READY_TO_BUILD -> BUILT_UNVERIFIED one-node mutation only
BUILT_UNVERIFIED -> ACCEPTED       only via RECONSTRUCTION_NODE_GATE
```

`UNVERIFIED`, `FAIL`, `BLOCKED`, `DIRTY`, `SUPERSEDED` are persistent states. `BUILT_UNVERIFIED` is a hard branch stop and never unlocks children. No `READY_TO_BUILD` node plus canonical authorization means no production geometry mutation. RDL0 must create neutral diagnostic geometry. Preflight also requires `CANONICAL_SKILL_RUNTIME_PIN`.

---

## Stany

### S0 — DISCOVER
Cel:
- ustalić narzędzia, Blender version, stan sceny, jednostki, aktywny plik;
- związać capabilities;
- załadować matching project profile.

Wyjście:
`Scene Snapshot` + Tool/Project Context.

### S1 — ANALYZE
Cel:
- zrozumieć funkcję assetu;
- zinwentaryzować evidence/views;
- wyodrębnić dimensions/landmarks/features;
- określić niewiadome i conflicts.

Wyjście:
`Asset Brief` + Reference/Evidence state.

### S2 — CONTRACT
Cel:
- utworzyć Feature Contract;
- oznaczyć `MUST`, `SHOULD`, `OPTIONAL`;
- przypisać metryki, tolerancje i authority.

Wyjście:
`Feature Contract`.

### S3 — PLAN / SHAPE UNDERSTANDING

Dla reference reconstruction ten stan **nie zaczyna od operatorów Blendera**.

Cel:
- rozbić asset na G0–G5 design forms;
- zbudować `Reconstruction Shape Graph`;
- przypisać parent/dependencies;
- sklasyfikować mathematical shape representation;
- przypisać authoritative views + controlled properties;
- przypisać RDL0–RDL5;
- zaplanować node gates i stage barriers;
- dopiero potem dobrać semantic skills/implementation.

Wyjście:
`Shape Graph` + `Node Contracts` + `RDL Plan`.

`Shape Graph != PASS` blokuje produkcyjną geometrię poza diagnostic RDL0.

### S4 — COARSE FORM / BLOCKOUT

Dla zwykłych assetów: blockout.

Dla reference reconstruction:
- RDL0 envelope;
- RDL1 primary forms node-by-node;
- każdy node musi przejść required multi-view gate;
- RDL1 stage barrier przed secondary forms.

Zakaz:
- budowy G2–G5 przed odpowiednim barrier;
- finalnych materiałów;
- monolitycznego builda tworzącego wiele poziomów formy.

### S5 — STRUCTURAL FORMS / FEATURES

Dla reconstruction:
- RDL2 secondary structural forms node-by-node;
- RDL3 structural features tylko na ACCEPTED hosts;
- leaf skills takie jak panel lines/recess/layer stack dopiero tutaj.

### S6 — EDGE / SECONDARY DETAIL

Dla reconstruction:
- RDL4 edge language;
- bevel/fillet/chamfer/SubD support dopiero po accepted form;
- microgeometry wymagane przez contract.

### S7 — SHADING_UV_MATERIAL

Dla reconstruction najpierw RDL5 surface/detail, potem:
- UV;
- normals/shading;
- runtime material strategy.

UV/runtime nie może rozpocząć się, jeżeli Reconstruction Fidelity Gate jeszcze nie PASS.

### S8 — GAME_READY
Cel:
- runtime LOD;
- collision;
- pivot/naming;
- bake/runtime textures;
- optimization;
- package preparation.

Runtime LOD jest downstream od RDL. `RDL != LOD`.

### S9 — VALIDATE
Cel:
- reconstruction final fidelity proof;
- mesh/runtime validation;
- package readback;
- completion gate.

### S10 — EXPORT / INTEGRATE
Cel:
- export;
- round-trip invariants;
- target-engine proof dla Level D;
- final completion report.

## Core gates

Reference reconstruction:

```text
Shape Graph PASS
-> RDL0 PASS
-> G1 node gates + RDL1 barrier
-> G2 node gates + RDL2 barrier
-> G3 node gates + RDL3 barrier
-> RDL4 edge barrier
-> RDL5 as required
-> RECON_FIDELITY_GATE
-> runtime/game-ready
```

Nie wolno:
- budować child na failed/unverified required parent;
- używać detail skill do naprawy primary form;
- przejść do runtime przy reconstruction FAIL/UNVERIFIED;
- maskować błędu późniejszym etapem.

## Cofnięcie

Każdy failed gate kieruje do najwcześniejszego ownera:
- evidence/registration;
- Shape Graph/representation;
- konkretny Shape Node;
- właściwy RDL;
- runtime stage.

## Reconstruction branch

Dla wielowidokowej/blueprint/concept-sheet reconstruction `10_reconstruction/149_RECONSTRUCTION_STATE_MACHINE.md` rozwija S1–S9 i jest canonical controllerem formy.
