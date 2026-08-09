# Assembly Relation and Interpenetration Contract

## Purpose

Object overlap has no meaning without assembly semantics.

The v0.11 lamp initially validated `J_SENSOR_ARM` by checking that the sensor shell overlapped the arm. Human inspection revealed that the overlap itself was the defect. The intended design was a separate housing meeting the arm across a small shadow gap and overhanging it slightly.

v0.12 requires every important multi-part junction to declare a relation type before geometry validation.

## Canonical relation types

```text
BUTT_JOINT
SHADOW_GAP
RECESSED_INSERT
OVERLAP_ALLOWED
FLUSH_MATE
CLEARANCE
EMBEDDED
WELDED
FREE
```

## Semantics

- `BUTT_JOINT` — parts meet at a boundary; unintended penetration forbidden.
- `SHADOW_GAP` — parts remain separate by a visible controlled gap; penetration forbidden.
- `RECESSED_INSERT` — child intentionally seats inside a host recess; embedding is required and bounded.
- `OVERLAP_ALLOWED` — overlap intentional, still bounded when MUST.
- `FLUSH_MATE` — surfaces align within tolerance; deep penetration/visible gap fail.
- `CLEARANCE` — minimum free space required.
- `EMBEDDED` — intentional penetration/embedding depth required and bounded.
- `WELDED` — contact required; controlled overlap may be allowed.
- `FREE` — no geometric relation asserted; not a shortcut for unknown intent.

## Relation schema

```yaml
relation_id: J_SENSOR_ARM
a: ARM
b: SENSOR_MODULE
relation_type: SHADOW_GAP
importance: MUST
constraints:
  min_gap_mm: 2.0
  max_gap_mm: 4.0
  max_penetration_area_mm2: 0.5
metrics:
  min_gap_mm: 3.0
  mean_gap_mm: 3.0
  penetration_area_mm2: 0.0
```

## Required policy

A generic `objects overlap` or `objects do not overlap` test cannot certify a junction. The declared relation owns interpretation of measured geometry.

For target L4/L5, every MUST `JUNCTION` Appearance Owner must map to an Assembly Relation record or an explicit authority waiver.

## Canonical executor

`executors/assembly_integrity_gate.py`

Skill ID: `ASSEMBLY_INTEGRITY_GATE`.
