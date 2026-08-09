# Execution Authorization Gate

## Purpose

Shape Graph state is executable rather than advisory.

Production geometry mutation requires all of:

```text
node.state == READY_TO_BUILD
EXECUTION_AUTHORIZATION_GATE == PASS
parent/dependencies == ACCEPTED
all earlier MUST RDL barriers == PASS
authorization.graph_revision == current graph revision
authorization.node_revision == requested node revision
```

No `READY_TO_BUILD` node means no production geometry mutation.

## Eligibility is not authorization

```text
CONSTRAINED
-> Shape Graph eligible
-> EXECUTION_AUTHORIZATION_GATE
-> persist READY_TO_BUILD
-> can_mutate
```

Do not treat `CONSTRAINED`, `DIRTY`, `FAIL` or `UNVERIFIED` as build permission.

## v0.12 post-mutation boundary

Authorization permits the mutation; it does not prove its result.

```text
READY_TO_BUILD
-> build/repair current node only
-> MUTATION_POSTCONDITION_GATE
-> PASS: BUILT_UNVERIFIED
-> STOP branch
-> source QA + ASSEMBLY_INTEGRITY_GATE where required
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | UNVERIFIED | FAIL
```

A Boolean/transform/loft operation that returns normally but fails its geometric postcondition cannot reach `BUILT_UNVERIFIED`.

## Required authorization record

```yaml
authorization:
  status: PASS
  validator_id: EXECUTION_AUTHORIZATION_GATE
  authorization_id: auth:sg_012:HEAD:n_004:BUILD
  graph_revision: sg_012
  node_id: HEAD
  node_revision: n_004
  action: BUILD
```

The asset-local builder may not fabricate this record.

## Mutation wrapper

Every builder entry point conceptually performs:

```text
can_mutate(node_id, authorization)
-> FAIL: return before bpy/BMesh mutation
-> PASS: capture before metrics
-> mutate one node
-> capture after metrics
-> MUTATION_POSTCONDITION_GATE
```

A convenience `build_all()` may exist only as an orchestrator that requests and closes each node transaction sequentially.

## Failure classes

- `NODE_NOT_READY_TO_BUILD`
- `AUTHORIZATION_RECORD_REQUIRED`
- `DEPENDENCY_NOT_ACCEPTED`
- `PRIOR_RDL_BARRIER_NOT_ACCEPTED`
- `AUTHORIZATION_GRAPH_REVISION_MISMATCH`
- `AUTHORIZATION_NODE_MISMATCH`
- `AUTHORIZATION_ACTION_MISMATCH`
- downstream `MUTATION_POSTCONDITION_REQUIRED`

## Canonical executor

`executors/execution_authorization_gate.py`

Skill ID: `EXECUTION_AUTHORIZATION_GATE`.
