# Appearance Owner Coverage and Report Namespaces

## Purpose

A correct aggregate category is not enough if individual MUST details were never implemented or never reported.

The Street Lamp v0.10 run declared a rich Appearance Contract, but the builder could still complete RDL5 while some branding, head cuts and detail owners were absent or unverified.

## Canonical namespaces

```yaml
shape_nodes: {}
appearance_owners: {}
evidence: {}
conflicts: {}
```

Never place an Appearance Owner such as `D_SENSOR_LENSES` inside `shape_nodes`.

## Coverage invariant

Before `APPEARANCE_FIDELITY_GATE`:

```text
expected MUST owner IDs from Appearance Contract
==
reported MUST owner IDs
```

Every MUST owner must be one of:
- `PASS` with canonical evidence;
- `NOT_REQUIRED` with authority record;
- `FAIL`;
- `UNVERIFIED`.

Missing from the report is itself a blocker.

## Coverage report

```yaml
status: PASS
validator_id: APPEARANCE_OWNER_COVERAGE
contract_revision: ac_009
expected_must: 32
accounted_must: 32
missing_must: []
failed_must: []
unverified_must: []
coverage: 1.0
```

For L4/L5 strict acceptance, missing or unverified MUST owner means FAIL of appearance closure.

## Host revision binding

Appearance owner evidence must identify the host node revision it validates. If the host becomes DIRTY, its appearance records become UNVERIFIED until regenerated.

## Canonical executor

`executors/appearance_owner_coverage.py`.
