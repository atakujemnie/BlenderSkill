# Shape Graph Validator Pattern

## Cel

Walidować strukturę Reconstruction Shape Graph przed modelowaniem i przy każdym revision change.

Preferred executor:
`executors/shape_graph.py`.

---

## Structural checks

Validator sprawdza:
- unique node IDs;
- root exists;
- parent IDs exist;
- dependency IDs exist;
- graph is acyclic;
- hierarchy level jest canonical G0–G5;
- RDL jest canonical RDL0–RDL5;
- hierarchy/RDL relation jest spójna;
- required nodes mają shape class;
- required nodes mają validation contract;
- child nie może zależeć od późniejszego RDL bez jawnego wyjątku;
- ready node ma zaakceptowane wymagane dependencies.

---

## Canonical level mapping

Default:

```text
G0 -> RDL0
G1 -> RDL1
G2 -> RDL2
G3 -> RDL3
G4 -> RDL4
G5 -> RDL5
```

Wyjątek musi być jawny i uzasadniony w node contract.

---

## Readiness computation

Executor może wyliczyć:

```yaml
ready_nodes:
  - BASE_PLINTH
blocked_nodes:
  - LOWER_SHOULDER:
      reason: dependency PRIMARY_BODY not ACCEPTED
```

Gotowość nie oznacza ACCEPTED; oznacza tylko, że node może wejść do transakcji build/repair.

---

## Stage barrier computation

Dla wskazanego RDL:
- znajdź required nodes;
- sprawdź ich states/evidence status;
- zwróć blockers;
- `can_advance` tylko przy pełnym PASS.

---

## Compact output

```yaml
shape_graph_validation:
  status: PASS
  node_count: 17
  root: PYLON
  graph_revision: sg_004
  ready_nodes: [BASE_PLINTH]
  blocked_nodes: 6
  errors: []
  warnings: []
```

Nie zwracaj pełnego graph dump, jeśli caller już go posiada.

---

## Failure IDs

Canonical examples:
- `DUPLICATE_NODE_ID`;
- `ROOT_MISSING`;
- `PARENT_MISSING`;
- `DEPENDENCY_MISSING`;
- `GRAPH_CYCLE`;
- `INVALID_LEVEL`;
- `INVALID_RDL`;
- `LEVEL_RDL_MISMATCH`;
- `SHAPE_CLASS_MISSING`;
- `VALIDATION_CONTRACT_MISSING`;
- `DEPENDENCY_NOT_ACCEPTED`;
- `FUTURE_LEVEL_DEPENDENCY`.

---

## Rule

Shape Graph validator nie ocenia, czy geometria wygląda dobrze. Pilnuje, aby system miał poprawny plan zależności i nie mógł ominąć coarse-to-fine execution.
