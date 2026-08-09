# Mutation Postcondition Gate

## Purpose

v0.11 proved that an authorized one-node transaction can still produce the wrong geometry while every execution-state rule is obeyed.

The Lafar Street Lamp v0.11 benchmark exposed multiple silent mutation failures:
- a Boolean modifier could be applied without producing the intended recess;
- transform/context state could differ from the active-object assumption;
- lofted geometry could carry incorrect volume orientation;
- a builder could return `PASS` because Python completed, not because geometry changed as intended.

v0.12 inserts a mandatory postcondition between mutation and `BUILT_UNVERIFIED`.

## Canonical order

```text
READY_TO_BUILD
-> authorized mutation
-> MUTATION_POSTCONDITION_GATE
-> PASS: persist BUILT_UNVERIFIED
-> FAIL: persist FAIL / repair current node
```

`LOCAL_BUILDER: PASS` means only that the builder transaction returned normally. It is not geometric proof.

## Required evidence

Capture compact before/after metrics for the mutated owner:
- object existence;
- vertex/face counts;
- geometry signature;
- bounds;
- volume when meaningful;
- signed volume for closed solids when meaningful;
- transform identity where Apply is expected;
- modifier list;
- cutter/helper existence;
- feature-probe result;
- operation kind and stable operation ID.

## Boolean rule

A Boolean is not successful because the modifier disappeared.

For `BOOLEAN_CUT`, `BOOLEAN_UNION` or `BOOLEAN_INTERSECT`, require evidence that the target actually changed: topology delta, volume delta or geometry-signature delta, plus an operation-specific feature probe when declared.

```text
modifier applied
+ target unchanged
= BOOLEAN_NO_OP
= FAIL
```

## Transform rule

When a mutation depends on transform application:
- active/selected context is explicit;
- expected object matrix is identity after Apply;
- depsgraph update/readback is recorded;
- unrelated selected objects must not change accidentally.

## Loft / closed-volume rule

For closed section-loft geometry, the postcondition may require positive signed volume. Inverted closed volume is a build failure even when the viewport render looks plausible.

## Material-only rule

A material-only mutation should keep geometry signature stable while material response/signature changes. Geometry drift during RDL5 lookdev is a regression.

## Canonical executor

`executors/mutation_postcondition_gate.py`

Skill ID: `MUTATION_POSTCONDITION_GATE`.
