# Geometric Integrity Gate

## Purpose

Reference fidelity and geometric integrity are separate non-compensating requirements.

The Lafar Street Lamp v0.11 reached green Shape/Appearance/fidelity reports while a severe sensor/arm interpenetration still existed. v0.12 therefore adds a final physical-geometry gate before reconstruction fidelity can unlock runtime.

## Canonical order

```text
all required Shape Nodes accepted
-> mutation postconditions closed
-> assembly relations closed
-> topology records closed
-> required validator negative controls PASS
-> no stale evidence
-> GEOMETRIC_INTEGRITY_GATE
-> RECON_FIDELITY_GATE
-> runtime
```

## Required categories

### Mutation postconditions
Every required production mutation has a current `MUTATION_POSTCONDITION_GATE: PASS` record.

### Assembly integrity
All MUST assembly relations are represented by a current `ASSEMBLY_INTEGRITY_GATE: PASS` aggregate.

### Topology integrity
Required mesh owners provide `MESH_VALIDATE: PASS` records under their topology intents.

### Validator controls
Acceptance validators named by project/asset policy provide `VALIDATOR_NEGATIVE_CONTROL: PASS` records.

### Evidence freshness
No evidence referenced by the current final report is `SUPERSEDED` or bound to a stale node revision.

### Relation closure
No MUST assembly relation remains unresolved/unknown.

## Non-compensation

```text
perfect visual overlay
+ perfect dimensions
+ engine load PASS
+ ASSEMBLY_INTEGRITY FAIL
= GEOMETRIC_INTEGRITY_GATE FAIL
= runtime blocked
```

A human-visible geometric defect cannot be averaged away by an appearance score.

## Canonical executor

`executors/geometric_integrity_gate.py`

Skill ID: `GEOMETRIC_INTEGRITY_GATE`.
