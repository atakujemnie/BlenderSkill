# Reconstruction Node Execution Protocol

## Purpose

Replace monolithic asset builds with one authorized, postcondition-verified Shape Node transaction at a time.

Canonical v0.12 unit:

```text
ONE SHAPE NODE
-> ONE AUTHORIZATION
-> ONE MUTATION SCOPE
-> ONE MUTATION POSTCONDITION
-> ONE SOURCE/INTEGRITY VALIDATION PACKAGE
-> ACCEPT / FAIL / UNVERIFIED
```

## Preconditions

Before production mutation:
- current Shape Graph revision exists;
- node is eligible and can receive canonical authorization;
- parent/dependencies are `ACCEPTED`;
- prior RDL barriers pass;
- shape class is selected;
- required views/controls are declared;
- expected-change scope is explicit;
- touched Assembly Relations are declared;
- QA isolation and required canonical validators are available.

Missing required precondition = `BLOCKED`, not improvisation.

## Transaction

### 1. Authorize

```text
CONSTRAINED
-> EXECUTION_AUTHORIZATION_GATE
-> persist READY_TO_BUILD
```

### 2. Capture before state

Record compact mutation metrics appropriate to the operation: signature/topology/bounds/volume/transforms/modifiers/helpers.

### 3. Build/repair current node only

Modify only:
- node owner;
- explicit helpers/cutters;
- expected-change region.

### 4. Capture after state + postcondition

```text
before + after
-> MUTATION_POSTCONDITION_GATE
```

A builder return or applied modifier is not sufficient. A silent Boolean no-op is FAIL.

Only postcondition PASS permits:

```text
READY_TO_BUILD -> BUILT_UNVERIFIED
```

### 5. Source and integrity validation

Run as required:
- numeric checks;
- registered canonical views / local reference ROI;
- section/profile/layer validators;
- `ASSEMBLY_INTEGRITY_GATE` for touched relations;
- `MESH_VALIDATE`;
- parent/sibling/global regression.

### 6. Canonical node gate

`RECONSTRUCTION_NODE_GATE` returns:
- `ACCEPTED`;
- `FAIL`;
- `BLOCKED`;
- `UNVERIFIED`.

Only `ACCEPTED` unlocks dependants.

### 7. Persist

Persist current revisions, evidence provenance and transition history before resolving next node.

## No bulk-add rule

One transaction cannot create many independent forms and validate afterwards.

If an assembly node organizes children, production geometry still closes at the appropriate structural/leaf nodes unless a justified `atomic_group_id` makes separation impossible.

## Builder architecture

Preferred interface:

```python
BUILDERS = {
    'PRIMARY_BODY': build_primary_body,
    'BASE_PLINTH': build_base_plinth,
    'LOWER_SHOULDER': build_lower_shoulder,
}
```

Orchestrator:

```text
resolve eligible node
-> authorize
-> capture before
-> invoke one builder
-> capture after
-> mutation postcondition
-> source/integrity validation
-> canonical node gate
-> persist
-> resolve next node
```

A convenience full replay may iterate this protocol, but may not mint new acceptance proof merely because replay succeeded.

## Repair semantics

Before mutating an accepted host:

```text
repair/change intent
-> DEPENDENCY_INVALIDATOR
-> new revisions/states persisted
-> affected closure rebuilt node-by-node
```

Do not repair first and invalidate descendants later. Old evidence is `SUPERSEDED`, not deleted or silently reused.

## Retry and strategy switch

After first FAIL:
- diagnose the actual failed owner/property;
- one corrected retry of the same strategy.

After second proven FAIL:
- re-inspect evidence;
- consider registration/parameter/representation error;
- route to `SHAPE_CLASSIFY` if representation is inadequate.

Do not loop `tweak -> render` without changing the model of the problem.

## Compact output

```yaml
node_execution:
  node_id: SENSOR_MODULE
  node_revision: sensor_007
  authorization_id: auth:sg_020:SENSOR_MODULE:sensor_007:REPAIR
  mutation_postcondition: PASS
  source_views: {FRONT: PASS, SIDE: PASS}
  assembly_relations: {J_SENSOR_ARM: PASS}
  topology: PASS
  node_gate: ACCEPTED
  blockers: []
```

Do not echo full scripts/raw mesh arrays unless required for a concrete diagnostic.
