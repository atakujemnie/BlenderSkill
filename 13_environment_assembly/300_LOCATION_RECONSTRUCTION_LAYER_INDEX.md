# Location Reconstruction Layer Index v0.15

## Purpose

This layer owns complete authored locations: interiors, exteriors, streets, plazas and room-scale assemblies composed from architecture, reconstructed assets, procedural content and repeated instances.

## Core rule

```text
asset fidelity
!= location fidelity
```

A location can fail even when every individual asset is valid, because placement, zoning, circulation, focal hierarchy, materials, lighting or completeness can still be wrong.

## Modules

- 301 — reference ingestion
- 302 — Location Scene Graph
- 303 — Location Asset Manifest
- 304 — Location Design System
- 305 — architectural assembly
- 306 — zoning/program
- 307 — spatial relation graph
- 308 — circulation/clearance
- 309 — placement anchors
- 310 — HERO composition
- 311 — furniture cluster grammar
- 312 — interpenetration gate
- 313 — material/lighting language
- 314 — stage barriers
- 315 — reference composition fidelity
- 316 — completeness gate
- 317 — runtime partitioning/instancing
- 318 — definition of done

## Canonical hierarchy

```text
LOCATION -> ZONE -> SYSTEM -> ASSET -> INSTANCE
```

Shape Graph remains nested inside ASSET nodes.
