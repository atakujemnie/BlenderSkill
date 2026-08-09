# Location Design System Layer Index

## Purpose

`14_design_system/` owns persistent reusable visual language above individual assets and alongside v0.15 location assembly.

It does not replace:
- `10_reconstruction/` — fidelity of one reference-driven asset;
- `12_procedural_generation/` — procedural generation domains;
- `13_environment_assembly/` — spatial assembly of complete locations.

It supplies all three with reusable location/faction/family resources.

## Canonical flow

```text
LOCATION_DESIGN_SYSTEM_RESOLVE
-> BUILD if missing / LOAD if present
-> ingest authoritative location + organization references
-> design tokens + form language
-> material language
-> branding/graphics
-> reusable components/profiles/nodegroups
-> lighting + weathering language
-> Blender Asset Library packaging
-> inheritance resolution for current asset family
-> asset consumes canonical resources
-> DESIGN_SYSTEM_CONFORMANCE_GATE
-> promote approved reusable additions back into system
```

## Modules

- `401` Build/Bootstrap from references and accepted assets
- `402` Directory/path/source-of-truth contract
- `403` Machine-readable manifest contract
- `404` Inheritance and override semantics
- `405` Resource provenance, promotion and deduplication
- `406` Material and texture language
- `407` Branding, graphics and signage library
- `408` Reusable components, profiles and node groups
- `409` Shape, edge, seam and detail language
- `410` Weathering/environment-response language
- `411` Lighting and emissive language
- `412` Blender Asset Library packaging/API contract
- `413` Asset consumption/reuse protocol
- `414` Design System Conformance Gate
- `415` Versioning/change propagation
