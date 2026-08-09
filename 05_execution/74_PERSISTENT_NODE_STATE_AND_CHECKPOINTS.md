# Persistent Node State and Checkpoints

## Purpose

A reconstruction state machine is useless if state exists only in comments or transient Python variables.

Persistent checkpoints separate design state, appearance state, assembly state and evidence.

## Canonical states

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

## Transition ownership

- `DECLARED -> CONSTRAINED`: planner/contract completion;
- `CONSTRAINED -> READY_TO_BUILD`: canonical `EXECUTION_AUTHORIZATION_GATE`;
- authorized mutation occurs while node is `READY_TO_BUILD`;
- `READY_TO_BUILD -> BUILT_UNVERIFIED`: requires `LOCAL_BUILDER` artifact **and** nested `MUTATION_POSTCONDITION_GATE: PASS` proof;
- `BUILT_UNVERIFIED -> ACCEPTED`: only canonical `RECONSTRUCTION_NODE_GATE`;
- `ACCEPTED -> DIRTY`: change-impact record required.

A successful Python return without geometric postcondition cannot advance state.

## Checkpoint schema

```yaml
asset_id: LAFAR_3470
state_revision: state_018
graph_revision: sg_012
appearance_revision: ac_007
assembly_revision: assembly_004
current_rdl: RDL2
shape_nodes:
  ARM:
    state: ACCEPTED
    node_revision: arm_006
    last_transition_provenance: gate_arm_006
appearance_owners:
  T_HEAD_BLUE_STRIP:
    status: PASS
    hosts: [ARM]
evidence:
  mutation_arm_006:
    type: MUTATION_POSTCONDITION
    status: PASS
    node_id: ARM
  gate_arm_006:
    type: NODE_GATE
    status: PASS
    node_id: ARM
conflicts: {}
history: []
```

## Separate namespaces

Do not mix Shape Node IDs, Appearance Owner IDs, Assembly Relation IDs and Evidence IDs.

## Persistence rule

After every state transition persist checkpoint before requesting the next authorization. A scene reset/rebuild may be deterministic replay, but it does not reset acceptance history.

## v0.12 repair invalidation

Do not manually dirty one node and leave descendants/evidence green.

```text
accepted host repair
-> DEPENDENCY_INVALIDATOR
-> changed node revision bump + DIRTY
-> built descendants DIRTY
-> unbuilt descendants BLOCKED
-> hosted Appearance Owners UNVERIFIED
-> old revision evidence SUPERSEDED
-> later dependent barriers invalid
```

Unrelated accepted branches remain reusable.

## Evidence freshness

Final reports must reference evidence bound to current node/graph/appearance/assembly revisions. `SUPERSEDED` proof stays in history but cannot satisfy a current gate.

## Canonical executors

- `executors/node_state_store.py` — transitions/checkpoint namespace integrity;
- `executors/dependency_invalidator.py` — repair invalidation/supersession.
