# Circulation and Clearance Contract

## Purpose

Protect declared guest/service/door paths and local operating space.

## Records

```yaml
clearance_id: GUEST_AISLE_01
required_mm: 900
measured_mm: 1040
penetration_mm: 0
max_penetration_mm: 0
importance: MUST
```

Declare constraints from project/reference authority. Defaults are design heuristics only and are not a building-code certification.

Check:
- furniture to wall;
- chair pull-out/occupancy envelope;
- table cluster to neighbor;
- guest path;
- service path;
- door swing/access;
- bar operating side;
- fixed equipment access.

Canonical executor: `executors/clearance_gate.py`.
