# Furniture Cluster Grammar

## Purpose

Compose semantic dining/meeting/seating units rather than scatter independent meshes.

## Cluster examples

```text
TABLE_ROUND_4 = table + 4 seats + occupancy envelopes + table-light relation
TABLE_2 = table + 2 seats
BOOTH = fixed bench + table + opposing seat(s)
BAR_SEAT_RUN = bar edge + repeated stools + operating clearance
```

Rules:
- seat faces target/table unless source says otherwise;
- cluster owns relative transforms;
- cluster validates wall/neighbor clearances;
- repeated source assets use instancing;
- variation cannot break ergonomics or reference rhythm.
