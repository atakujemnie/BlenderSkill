# v0.15 Location Reconstruction and Environment Assembly Extension

## Purpose

v0.15 adds the missing hierarchy above single-asset reconstruction. A location is not a bag of assets. It is a constrained spatial system whose architecture, zones, hero anchors, circulation, materials, lighting and repeated instances must be solved and validated together.

## Canonical hierarchy

```text
LOCATION
-> ZONE
-> SYSTEM
-> ASSET
-> INSTANCE
```

The existing Shape Graph remains authoritative inside each reference-driven asset. The Location Scene Graph owns relationships between assets and the environment.

## Non-negotiable laws

```text
LOCATION_PLAN != PASS -> no final location population
ASSET state not ACCEPTED -> final instance forbidden
PROXY present -> LOCATION_COMPLETE FAIL
MISSING required HERO -> LOCATION_COMPLETE FAIL
unintended interpenetration -> LOCATION_COMPLETE FAIL
blocked required circulation -> LOCATION_COMPLETE FAIL
reference composition gate != PASS -> final fidelity unresolved
```

A proxy is legal only during blockout and must remain explicitly typed as `PROXY`.

## Build order

```text
reference ingest
-> location design system
-> Location Scene Graph + Asset Manifest
-> architectural envelope
-> modular wall/floor/ceiling systems
-> HERO anchors
-> fixed assets
-> furniture clusters
-> circulation/clearance closure
-> lighting + vegetation + table props
-> material/art-direction pass
-> reference composition fidelity
-> location completeness
-> runtime partitioning/instancing
```

## Scope separation

- `10_reconstruction/` owns fidelity of one asset to its references.
- `12_procedural_generation/` owns procedural source generation and placement domains.
- `13_environment_assembly/` owns complete authored locations and spatial composition.

All v0.12 geometric-integrity and negative-control laws remain active inside the new layer.
