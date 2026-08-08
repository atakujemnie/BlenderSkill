# Reconstruction Node Execution Protocol v0.11

## Execution unit

```text
ONE AUTHORIZED SHAPE NODE
-> ONE MUTATION SCOPE
-> BUILT_UNVERIFIED
-> ONE SOURCE-ANCHORED VALIDATION PACKAGE
-> ACCEPTED | UNVERIFIED | FAIL
```

Code organization into node functions is insufficient. The transaction itself must be node-scoped.

## Preconditions
- graph structural PASS;
- node contract complete;
- node is eligible;
- canonical `EXECUTION_AUTHORIZATION_GATE` record exists;
- node state has been persisted as `READY_TO_BUILD`;
- parent/dependencies are `ACCEPTED`;
- all earlier MUST RDL barriers PASS;
- per-view evidence contracts exist;
- shape class and implementation skill are known.

## Transaction
1. call `can_mutate`;
2. mutate current node and explicit helpers only;
3. persist mutation artifact and `BUILT_UNVERIFIED`;
4. stop branch;
5. isolate QA scene;
6. run source-fit numeric/registered/detail evidence according to each view contract;
7. validate derived parameters/conflict decisions;
8. run `RECONSTRUCTION_NODE_GATE`;
9. persist final node state;
10. only `ACCEPTED` unlocks children.

## Forbidden

```python
def main():
    build_foot()
    build_plinth()
    build_pole()
    build_arm()
    build_details()
```

unless every call is separated by persisted authorization, `BUILT_UNVERIFIED`, QA and canonical acceptance.

## Repair
An accepted ancestor change marks dependent nodes `DIRTY` and host-bound appearance evidence `UNVERIFIED`. Do not rebuild unrelated accepted branches.

## Replay
Full deterministic replay may recreate already accepted geometry, but replay itself is not new acceptance evidence.
