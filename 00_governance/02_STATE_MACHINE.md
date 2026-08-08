# Agent State Machine v0.11

## Core principle

The reconstruction state machine is executable state, not narrative guidance.

For reference-driven work:

```text
DISCOVER
-> ANALYZE
-> CONTRACT
-> SHAPE/APPEARANCE PLAN
-> AUTHORIZE ONE NODE
-> BUILD ONE NODE
-> BUILT_UNVERIFIED
-> SOURCE-ANCHORED QA
-> ACCEPT / FAIL / UNVERIFIED
-> repeat
-> appearance + reconstruction gates
-> runtime
```

## Reconstruction node states

```text
DECLARED
-> CONSTRAINED
-> READY_TO_BUILD
-> BUILT_UNVERIFIED
-> ACCEPTED
```

Failure/rework states: `UNVERIFIED`, `FAIL`, `BLOCKED`, `DIRTY`, `SUPERSEDED`.

### Hard ownership
- only `EXECUTION_AUTHORIZATION_GATE` allows `CONSTRAINED/DIRTY/FAIL/UNVERIFIED -> READY_TO_BUILD`;
- only a node-scoped builder mutation creates `BUILT_UNVERIFIED`;
- only `RECONSTRUCTION_NODE_GATE` allows `BUILT_UNVERIFIED -> ACCEPTED`;
- `BUILT_UNVERIFIED` never unlocks children.

## S0 DISCOVER
Bind Blender 5.1, tools, project profile, canonical BlenderSkill version/commit/source root. `CANONICAL_SKILL_RUNTIME_PIN` must PASS before benchmark execution.

## S1 ANALYZE
Create source registry, view classes, calibration, dimensions, landmarks, conflicts and uncertainty ledger. Reuse canonical analysis executors before writing local scanners.

## S2 CONTRACT
Create Feature Contract, property-level authority and MUST/SHOULD/OPTIONAL inventory.

## S3 PLAN
Create Shape Graph, per-view node contracts, shape representations, RDL plan and Appearance Contract for L4/L5. Resolve or explicitly block material conflicts before dependent geometry.

## S4 RDL0/RDL1
RDL0 produces neutral diagnostic geometry and registered FRONT/SIDE/TOP proof as applicable. Then build G1 one authorized node at a time.

## S5 RDL2/RDL3
Secondary forms and structural features only on ACCEPTED hosts. Major boundaries/trim/junction owners are proven while their geometry is still isolated.

## S6 RDL4
Reference edge-family proof. Bevel is implementation, not acceptance.

## S7 RDL5
Production material/branding/detail work. All MUST Appearance Owners must be accounted in separate namespace before appearance closure.

## S8/S9 FINAL RECONSTRUCTION
`APPEARANCE_OWNER_COVERAGE`, `APPEARANCE_FIDELITY_GATE`, `RECON_FIDELITY_GATE`.

## S10 RUNTIME
Only after reconstruction acceptance: UV, bake, runtime LOD, collision, export, round-trip, engine integration.

## Non-negotiable stop rules

```text
no READY_TO_BUILD + authorization -> no geometry mutation
BUILT_UNVERIFIED -> stop branch
MUST parent not ACCEPTED -> child blocked
prior RDL barrier FAIL -> next RDL blocked
unresolved equal-authority reference conflict -> dependent property blocked
missing MUST appearance owner -> appearance gate FAIL
stale/duplicate BlenderSkill runtime -> preflight FAIL
```
