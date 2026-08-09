# BlenderSkill

Canonical knowledge repository for the Blender AI Agent Library.

## Current release

**v0.12.0 — geometric integrity, mutation postconditions and adversarial validation.**

v0.12 is driven by the Lafar Street Lamp v0.11 benchmark. v0.11 successfully enforced node-scoped execution and produced the strongest reconstruction process so far, but human review still found a severe arm/sensor interpenetration after the Shape Graph, Appearance Owner inventory and final fidelity gates had gone green.

That failure establishes the v0.12 boundary:

```text
correct execution process
+ correct reference evidence
!=
proven physically correct geometry
```

## Canonical v0.12 node transaction

```text
eligible Shape Node
-> EXECUTION_AUTHORIZATION_GATE
-> persist READY_TO_BUILD
-> mutate exactly one node
-> MUTATION_POSTCONDITION_GATE
-> PASS: persist BUILT_UNVERIFIED
-> source-anchored per-view QA
-> ASSEMBLY_INTEGRITY_GATE for touched relations
-> topology/regression proof
-> RECONSTRUCTION_NODE_GATE
-> persist ACCEPTED / FAIL / UNVERIFIED
-> only ACCEPTED unlocks dependants
```

`LOCAL_BUILDER: PASS` only proves that code returned normally. It does not prove that a Boolean cut, transform, loft or other geometry operation produced the intended result.

## Core v0.12 additions

### Mutation Postcondition Gate

Every production mutation must prove its postcondition before the node may enter `BUILT_UNVERIFIED`.

Typical evidence:
- before/after geometry signature;
- vertex/face delta;
- volume or signed-volume delta where meaningful;
- expected transform identity/readback;
- applied modifier and cutter lifecycle;
- predeclared feature probe.

A Boolean modifier that disappears while the target remains unchanged is `FAIL`.

### Assembly Relation Contract

Multi-part junctions declare semantics before validation:

```text
BUTT_JOINT
SHADOW_GAP
RECESSED_INSERT
OVERLAP_ALLOWED
FLUSH_MATE
CLEARANCE
EMBEDDED
WELDED
FREE
```

The validator measures gap/contact/embedding/interpenetration and applies the declared relation. Generic `parts overlap` is not a junction proof.

### Adversarial validator controls

A MUST acceptance validator must demonstrate that it can reject a known-broken fixture:

```text
KNOWN_GOOD   -> PASS
KNOWN_BROKEN -> FAIL
```

If a negative fixture returns PASS, the validator is toothless and cannot provide MUST acceptance evidence.

### Repair invalidation

Repairing an accepted host automatically invalidates dependent state:

```text
changed node            -> DIRTY
built descendants       -> DIRTY
unbuilt descendants     -> BLOCKED
hosted Appearance Owners-> UNVERIFIED
old revision evidence   -> SUPERSEDED
unrelated branches      -> preserved
```

Stale green evidence cannot survive a geometry revision.

### Final Geometric Integrity Gate

Before reconstruction fidelity can unlock runtime, current physical proof is aggregated:

```text
mutation postconditions
+ Assembly Relation closure
+ topology records
+ validator negative controls
+ zero stale evidence
+ zero unresolved MUST relations
-> GEOMETRIC_INTEGRITY_GATE
```

This gate is non-compensating. Perfect dimensions, overlays or appearance cannot override physical interpenetration or invalid topology.

### Mesh integrity classification

`MESH_VALIDATE` now distinguishes topology risk instead of treating all n-gons alike. It reports high-order n-gons, non-planar n-gons, concave n-gons and signed closed volume in addition to manifold/loose/duplicate/zero-area checks. Non-planar n-gons and inverted closed volumes are failures; concavity can be policy-driven.

### Reference-mask contamination

Registered technical-sheet QA can explicitly remove annotation ROIs and select the intended product component before silhouette metrics. Dimension lines, leaders and text cannot silently become part of the product mask. Registration remains global; no local warp is allowed.

## Foundations retained

### v0.9 — Shape understanding

Reference-driven assets are decomposed into design forms:

```text
G0 GLOBAL_ENVELOPE
G1 PRIMARY_FORM
G2 SECONDARY_STRUCTURAL_FORM
G3 STRUCTURAL_FEATURE
G4 EDGE_LANGUAGE
G5 SURFACE_DETAIL
```

RDL0–RDL5 is reconstruction progression and remains separate from runtime LOD0–LOD3.

### v0.10 — Appearance fidelity

For 1:1/L4/L5 work, Shape Graph is paired with a Reference Appearance Contract containing visible owners such as:

```text
PART_BOUNDARY
TRIM_PATH
JUNCTION
EDGE_FAMILY
MATERIAL_REGION
MATERIAL_RESPONSE
EMISSIVE_REGION
BRANDING_REGION
DETAIL_FEATURE
DETAIL_DENSITY_REGION
NEGATIVE_SPACE
```

Correct envelope or dimensions cannot compensate for failed MUST product architecture.

### v0.11 — Enforced execution

Node state is executable, not advisory:

```text
DECLARED
-> CONSTRAINED
-> READY_TO_BUILD
-> one authorized mutation
-> BUILT_UNVERIFIED
-> canonical proof
-> ACCEPTED
```

Parents/dependencies and RDL barriers are enforced; Shape Nodes, Appearance Owners, Evidence and Conflicts use separate persistent namespaces.

## Reconstruction Detail Levels

```text
RDL0 envelope / diagnostic geometry
RDL1 primary forms
RDL2 secondary structural forms / product architecture
RDL3 structural features
RDL4 edge language
RDL5 surface/detail
```

Runtime LOD, UV, bake, export and engine work remain downstream from reconstruction acceptance.

## Final runtime lock

For target fidelity L4/L5:

```text
GEOMETRIC_INTEGRITY_GATE != PASS
or
APPEARANCE_FIDELITY_GATE != PASS
or
RECON_FIDELITY_GATE != PASS
-> LOD / UV / bake / export / runtime FORBIDDEN
```

A successful glTF parse, triangle budget or engine load never overrides unresolved reconstruction geometry.

## New v0.12 semantic skills

- `MUTATION_POSTCONDITION_GATE`;
- `ASSEMBLY_INTEGRITY_GATE`;
- `DEPENDENCY_INVALIDATOR`;
- `VALIDATOR_NEGATIVE_CONTROL`;
- `GEOMETRIC_INTEGRITY_GATE`.

Strengthened:
- `NODE_STATE_STORE`;
- `RECONSTRUCTION_NODE_GATE`;
- `RECON_FIDELITY_GATE`;
- `ASSET_COMPLETION`;
- `MESH_VALIDATE`;
- `REFERENCE_OVERLAY_VALIDATE`.

New executors remain `CONTRACT_READY` until a fresh Blender 5.1 end-to-end benchmark proves runtime maturity. `MESH_VALIDATE` retains its existing executor maturity while its v0.12 checks are covered by regression tests.

## Canonical benchmark

`07_examples/81_LAFAR_STREET_LAMP_V011_GEOMETRIC_INTEGRITY_REGRESSION_BENCHMARK.md`

It protects against:
- unintended interpenetration hidden behind green visual gates;
- wrong junction semantics;
- silent Boolean no-op;
- transform/context and inverted-volume hazards;
- validators that cannot fail a known-broken fixture;
- stale evidence after repairs;
- unclassified risky topology;
- concept-sheet annotation contamination.

## Repository structure

- `00_governance` — state, routing, semantic skills, completion
- `01_analysis` — briefs, references, measurements
- `02_blender_api` — Blender 5.1 API/runtime rules
- `03_modeling` — hard-surface/topology/UV/procedural modeling
- `04_game_ready` — LOD/collision/bake/export/runtime contracts
- `05_execution` — authorization, postconditions, integrity and fidelity gates
- `06_prompts` — planner/reviewer/repair prompts
- `07_examples` — benchmark and regression post-mortems
- `08_scripts` — reusable validation patterns
- `09_engine` — project/runtime profiles and engine proof
- `10_reconstruction` — evidence-driven 1:1 reconstruction
- `11_playbooks` — asset-class production playbooks
- `executors` — reusable Python decision/execution components
- `99_sources` — technical sources

## Canonical source

Modular Markdown files listed in `MANIFEST.json` are canonical. `_FULL_LIBRARY.md` is generated from the manifest and must not be edited manually.
