# Knowledge Router

Version: 0.18.0
Status: CURRENT CONTRACT

The router loads the smallest evidence pack required by the current task. Historical v0.9-v0.17 override sections are not active routing layers; their semantics remain available through Git history, CHANGELOG and regression benchmarks.

## Entry point

```text
USER TASK
→ _RUNTIME_INDEX.json
→ task/reference classification
→ current Blender/project state
→ smallest required skill contracts
→ executor/tool binding
→ evidence-producing execution
→ postcondition and quality gates
```

Do not load `_FULL_LIBRARY.md` as the default routing surface. It is a complete snapshot, not the runtime index.

## Provider-sensitive tasks

For procedural generation, vegetation, external generators, Asset Libraries or add-on-dependent tasks:

```text
BLENDER_RUNTIME_ADDON_DISCOVERY
→ INSTALLED_PROVIDER_DISCOVERY
→ canonical provider registry classification
→ EXPECTED_PROVIDER_GATE when expected installations are known
→ explicit capability probes
→ Blender compatibility
→ requested-domain suitability
→ license policy
→ quality suitability
→ PROVIDER_DECISION_PIPELINE
→ PROVIDER_SELECTION_REPORT
→ execution
```

Hard rules:

- discovery is read-only and never executes provider code;
- installation/discovery never implies capability `PASS`;
- unknown add-on = `UNKNOWN`, never implicit `UTILITY`;
- `builtin_geometry_nodes` remains `PROBE_REQUIRED` until the real probe passes;
- a relevant rejected/blocked provider remains visible in the report;
- missing expected provider produces `DISCOVERY_MISMATCH` and blocks fallback;
- custom/native fallback is legal only after stronger candidates were evaluated and none remains eligible.

Load for this route:

- `12_procedural_generation/237_PROVIDER_STATE_PROTOCOL.md`;
- `12_procedural_generation/238_CANONICAL_PROVIDER_REGISTRY.md`;
- `12_procedural_generation/239_NON_EXECUTING_PROVIDER_DISCOVERY.md`;
- `12_procedural_generation/240_PROVIDER_CAPABILITY_PROBE_EXECUTION.md`;
- `12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md`;
- `05_execution/80_CONTRACT_EXECUTOR_TEST_PARITY_GATE.md` when changing runtime infrastructure;
- `05_execution/81_REAL_BLENDER_RUNTIME_VALIDATION.md` when claiming Blender capability.

## Reference reconstruction

For reference-driven assets:

```text
reference ingestion/calibration
→ property-level authority and conflict resolution
→ Shape Graph
→ Appearance Contract
→ eligible reconstruction node
→ execution authorization
→ one-node mutation
→ mutation postcondition
→ registered source/numeric evidence
→ assembly/topology checks
→ node acceptance
→ RDL barrier
→ geometric integrity
→ appearance fidelity when required
→ reconstruction fidelity
→ runtime finishing
```

Primary reconstruction contracts remain under `10_reconstruction/`. Use the smallest set matching the active RDL, representation class and failing evidence. A builder-local self-check is not canonical acceptance evidence.

## Location design system

For an asset or location assigned to a known location/faction/family:

```text
location identity
→ LOCATION_DESIGN_SYSTEM_RESOLVE
→ inheritance resolve
→ compact resolved design context
→ authoring
→ DESIGN_SYSTEM_CONFORMANCE_GATE
```

Asset-specific technical dimensions remain owned by authoritative asset references. Locked location/organization identity cannot be silently replaced by an asset-local approximation.

## Visual-quality and vegetation composition

For final environment/vegetation/material work:

```text
location material/design context
→ provider decision pipeline
→ source/variation generation
→ physical placement gate
→ planting/composition quality gate
→ reference composition fidelity when applicable
→ early visual-quality barrier
→ LOD/bake/export/runtime
→ context budget gate
```

Runtime compatibility never implies hero-quality suitability. Physical placement PASS never implies composition-quality PASS.

## Game-ready finishing

Game-ready finishing is downstream of accepted reconstruction/appearance state:

```text
runtime path
→ LOD/collision
→ UV contract
→ dirty bake stages
→ bake validation/cache coherence
→ runtime material
→ export/package readback
→ round-trip invariants
→ runtime QA
→ completion gate
```

Do not use runtime LOD as reconstruction progression state.

## Failure routing

Route from the failing evidence dimension, not from generic task intent:

- no runtime provider evidence → provider discovery/probe contracts;
- reference disagreement → reference conflict/evidence contracts;
- intended geometry did not change → mutation postcondition gate;
- contact/interpenetration problem → assembly integrity;
- known-broken fixture passes → validator negative control;
- visual form differs despite valid topology → shape/appearance fidelity;
- stale external image → image cache coherence;
- accepted host changed → dependency invalidation before downstream replay;
- generated artifacts dirty → rebuild and commit them in the feature branch; CI must not commit them.

## Runtime verification authority

A claim that depends on Blender runtime is valid only when supported by a real Blender process. CPython tests can validate parsing, routing and decision logic but cannot substitute for Blender runtime evidence.
