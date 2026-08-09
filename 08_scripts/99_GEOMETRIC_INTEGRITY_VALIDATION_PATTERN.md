# Geometric Integrity Validation Pattern

## Purpose

Reusable Blender-side measurement pattern consumed by v0.12 pure decision executors.

Canonical gates own acceptance logic. Asset-local Blender code only measures geometry and returns compact records.

## Mutation snapshot

Before and after a risky mutation record:

```python
{
  "object_exists": True,
  "vertices": len(mesh.vertices),
  "faces": len(mesh.polygons),
  "volume_mm3": measured_volume,
  "signed_volume_mm3": signed_volume,
  "geometry_signature": stable_hash,
  "matrix_identity": matrix_is_identity,
  "modifiers": [m.name for m in obj.modifiers],
}
```

Feed the pair into `MUTATION_POSTCONDITION_GATE`.

## Assembly relation measurement

For each declared relation pair, measure only metrics required by the relation contract:
- penetration surface area / estimated volume;
- minimum/mean gap;
- contact area;
- embedding depth;
- clearance;
- host containment where explicitly intended.

Feed measured metrics into `ASSEMBLY_INTEGRITY_GATE`.

Do not let the measurement helper decide whether overlap is correct. It does not know the semantic relation.

## Surface interpenetration

AABB overlap is only broad phase. It is not proof of collision.

Containment ratio alone is also insufficient: the lamp defect was a surface intersection, not complete burial.

Preferred pipeline:
1. broad-phase bounding overlap;
2. narrow-phase surface/triangle intersection or robust sampled surface penetration;
3. relation-specific tolerance;
4. compact area/volume/gap metrics;
5. canonical assembly decision gate.

## Boolean bite test

For a Boolean expected to create a recess:
- capture target signature/face-count/volume before;
- apply operation;
- force evaluated readback;
- capture after;
- verify non-zero intended change;
- verify cutter/modifier lifecycle;
- run a feature probe anchored to the predeclared feature ROI/volume.

## Negative control

Every new MUST integrity validator needs:
- a known-good fixture -> PASS;
- at least one known-broken fixture -> FAIL.

Use `VALIDATOR_NEGATIVE_CONTROL` to record the proof.
