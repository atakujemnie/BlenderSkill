# Execution Authorization Gate

## Purpose

v0.11 makes Shape Graph state executable rather than advisory.

The Lafar Street Lamp v0.10 benchmark exposed a hard loophole:

```text
SHAPE_GRAPH = PASS
ready_nodes = []
-> asset-local builder still created RDL0..RDL5 in one run
```

That is forbidden in v0.11.

## Fundamental rule

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

`SHAPE_GRAPH` may report a node as `eligible_nodes` when:
- its contract is complete;
- parent/dependencies are accepted;
- prior RDL barriers are closed.

Eligibility means only that an authorization may be requested.

```text
CONSTRAINED
-> eligible
-> EXECUTION_AUTHORIZATION_GATE
-> persist READY_TO_BUILD
-> can_mutate
```

Do not treat `CONSTRAINED`, `DIRTY`, `FAIL` or `UNVERIFIED` as build permission.

## BUILT_UNVERIFIED hard barrier

After mutation:

```text
READY_TO_BUILD
-> build/repair current node only
-> BUILT_UNVERIFIED
-> STOP branch
-> QA + source-anchored proof
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | UNVERIFIED | FAIL
```

A `BUILT_UNVERIFIED` parent never unlocks children.

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

Every builder entry point must conceptually perform:

```text
can_mutate(node_id, authorization)
-> FAIL: return before bpy/BMesh mutation
-> PASS: open one-node transaction
```

A convenience `build_all()` may exist only as a replay/orchestrator that requests and closes each node gate sequentially. It may never call all node functions directly.

## Failure classes

- `NODE_NOT_READY_TO_BUILD`
- `AUTHORIZATION_RECORD_REQUIRED`
- `DEPENDENCY_NOT_ACCEPTED`
- `PRIOR_RDL_BARRIER_NOT_ACCEPTED`
- `AUTHORIZATION_GRAPH_REVISION_MISMATCH`
- `AUTHORIZATION_NODE_MISMATCH`
- `AUTHORIZATION_ACTION_MISMATCH`

Any one blocks mutation.

## Canonical executor

`executors/execution_authorization_gate.py`

Skill ID: `EXECUTION_AUTHORIZATION_GATE`.
