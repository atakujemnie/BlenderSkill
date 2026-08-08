# Persistent Node State and Checkpoints

## Purpose

A reconstruction state machine is useless if state exists only in comments or transient Python variables.

v0.11 requires a persistent checkpoint separating design state, appearance state and evidence.

## Canonical node states

```text
DECLARED
-> CONSTRAINED
-> READY_TO_BUILD
-> BUILT_UNVERIFIED
-> ACCEPTED
```

Failure/rework states:

```text
UNVERIFIED
FAIL
BLOCKED
DIRTY
SUPERSEDED
```

`UNVERIFIED` is now a canonical state rather than only a gate return value.

## Transition ownership

- `DECLARED -> CONSTRAINED`: planner/contract completion;
- `CONSTRAINED -> READY_TO_BUILD`: only with `EXECUTION_AUTHORIZATION_GATE`;
- `READY_TO_BUILD -> BUILT_UNVERIFIED`: one-node mutation artifact;
- `BUILT_UNVERIFIED -> ACCEPTED`: only with `RECONSTRUCTION_NODE_GATE`;
- `ACCEPTED -> DIRTY`: change-impact record required.

## Checkpoint schema

```yaml
asset_id: LAFAR_3470
state_revision: state_018
graph_revision: sg_012
appearance_revision: ac_007
current_rdl: RDL1
shape_nodes:
  ARM:
    state: ACCEPTED
    node_revision: arm_006
    last_transition_provenance: gate_arm_006
appearance_owners:
  T_HEAD_BLUE_STRIP:
    status: UNVERIFIED
    host_revision: arm_006
evidence:
  gate_arm_006:
    type: NODE_GATE
history: []
```

## Separate namespaces

Never mix:

```text
Shape Node IDs
Appearance Owner IDs
Evidence IDs
```

The lamp v0.10 builder recorded an Appearance Owner such as `D_SENSOR_LENSES` inside a generic `REPORT['nodes']` namespace. v0.11 forbids that ambiguity.

## Persistence rule

After every state transition persist the checkpoint before requesting the next authorization.

A full scene reset/rebuild may be used for deterministic replay, but the orchestrator must restore and enforce canonical node states. Resetting Blender data is not permission to reset acceptance history.

## Dirty propagation

When an accepted node changes:
- mark dependent geometry nodes `DIRTY` when their host relationship may change;
- mark appearance owners tied to the old host revision `UNVERIFIED`;
- keep unrelated accepted nodes reusable;
- invalidate later RDL barriers that depended on the changed node.

## Canonical executor

`executors/node_state_store.py` validates transitions and checkpoint namespace integrity.
