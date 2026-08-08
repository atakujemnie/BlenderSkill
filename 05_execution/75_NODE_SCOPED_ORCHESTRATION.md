# Node-Scoped Orchestration

## Purpose

Code organization into `node_foot()`, `node_arm()`, `node_head()` is not enough. The execution transaction itself must be node-scoped.

The Lafar Street Lamp v0.10 builder had good node functions but `main()` invoked the entire asset from RDL0 through RDL5 in one run. v0.11 treats that as a regression.

## Canonical loop

```text
load checkpoint
-> validate Shape Graph
-> resolve one eligible node
-> issue EXECUTION_AUTHORIZATION_GATE
-> persist READY_TO_BUILD
-> execute exactly that node
-> persist BUILT_UNVERIFIED
-> isolate accepted ancestors + current node
-> render required evidence
-> canonical node gate
-> persist ACCEPTED / FAIL / UNVERIFIED
-> repeat
```

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
    return BUILDERS[node_id](context)
```

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

Even if functions are ordered correctly, this bypasses acceptance between nodes.

## RDL orchestration

One RDL may contain many nodes, but each node closes independently. When all MUST nodes through the target RDL are `ACCEPTED`, run the canonical stage barrier.

```text
all RDL1 MUST nodes ACCEPTED
-> RDL1 barrier PASS
-> only then authorize RDL2 nodes
```

## RDL0

RDL0 must produce diagnostic geometry, not only a dictionary of dimensions. It exists to falsify envelope interpretation early.

## Replay

A deterministic full replay is allowed after acceptance for reproducibility. Replay must use frozen accepted node revisions and may not create new acceptance evidence by itself.
