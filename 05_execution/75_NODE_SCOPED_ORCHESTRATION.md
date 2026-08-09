# Node-Scoped Orchestration

## Purpose

Code organization into `node_foot()`, `node_arm()`, `node_head()` is not enough. The execution transaction itself must be node-scoped and postcondition-verified.

## Canonical v0.12 loop

```text
load checkpoint
-> validate Shape Graph
-> resolve one eligible node
-> issue EXECUTION_AUTHORIZATION_GATE
-> persist READY_TO_BUILD
-> capture compact before-state geometry metrics
-> execute exactly that node
-> capture after-state metrics
-> MUTATION_POSTCONDITION_GATE
-> PASS: persist BUILT_UNVERIFIED
-> isolate accepted ancestors + current node
-> render required source evidence
-> ASSEMBLY_INTEGRITY_GATE for relations touched by node
-> topology/section/layer validation as required
-> RECONSTRUCTION_NODE_GATE
-> persist ACCEPTED / FAIL / UNVERIFIED
-> repeat
```

A failed mutation postcondition stops before source QA. A failed assembly relation stops node acceptance.

## Builder API

Preferred asset-local interface:

```python
BUILDERS = {
    'FOOT_PLATE': build_foot,
    'PLINTH': build_plinth,
    'POLE': build_pole,
    'ARM': build_arm,
}

def build_node(node_id, context, authorization):
    assert EXECUTION_AUTHORIZATION_GATE.can_mutate(...)
    before = capture_geometry_state(...)
    result = BUILDERS[node_id](context)
    after = capture_geometry_state(...)
    post = MUTATION_POSTCONDITION_GATE.evaluate(...)
    return {
        'status': 'PASS' if post['status'] == 'PASS' else 'FAIL',
        'validator_id': 'LOCAL_BUILDER',
        'artifact_id': result.artifact_id,
        'mutation_postcondition': post,
    }
```

Asset-local code may capture metrics. Canonical executors decide acceptance.

CLI pattern:

```text
build_asset.py --node ARM --authorization auth.json --checkpoint state.json
```

## Forbidden main

```python
def main():
    build_foot()
    build_plinth()
    build_pole()
    build_arm()
    build_sensor()
    build_materials()
```

Even when functions are ordered correctly, this bypasses per-node postconditions and acceptance.

## RDL orchestration

One RDL may contain many nodes, but each node closes independently.

```text
all RDL1 MUST nodes ACCEPTED
-> RDL1 barrier PASS
-> only then authorize RDL2 nodes
```

## RDL0

RDL0 produces neutral diagnostic geometry, not only a dimensions dictionary. It exists to falsify envelope interpretation early.

## Repair orchestration

For repair of accepted geometry:

```text
change intent
-> DEPENDENCY_INVALIDATOR
-> persist new revisions/states
-> rebuild affected closure node-by-node
```

Do not mutate an accepted host first and invalidate descendants afterwards.

## Replay

A deterministic full replay is allowed after acceptance for reproducibility. Replay uses frozen accepted node revisions and cannot mint new acceptance evidence by itself.
