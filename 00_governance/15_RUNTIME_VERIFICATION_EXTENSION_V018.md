# Runtime Verification Extension v0.18

Version: 0.18.0
Status: CURRENT CONTRACT

## Purpose

BlenderSkill v0.18 changes provider handling from documented intent to runtime-verifiable behavior. Discovery evidence, capability evidence, compatibility, domain suitability, license policy, quality and final selection are separate dimensions and must remain auditable.

## Mandatory invariants

1. Provider discovery is read-only and does not execute provider code.
2. Provider identity and static metadata come only from `data/provider_registry.json`.
3. Unknown add-ons use `source_kind=UNKNOWN`, `classification_known=false`, and no inferred domains.
4. Discovery of a provider never implies capability `PASS`.
5. `builtin_geometry_nodes` is `PROBE_REQUIRED` after discovery and becomes `PASS` only after the executable Geometry Nodes probe succeeds.
6. Capability probes must be isolated and must report cleanup state and side effects.
7. Provider selection consumes discovery, expected-provider gate, probe, Blender compatibility, domain, license and quality evidence.
8. Rejected or blocked relevant candidates remain visible in the provider selection report.
9. Custom/native fallback is legal only after stronger candidates have been evaluated and none remains eligible.
10. `EXECUTOR_READY` requires a real executor and at least one executable test.

## Runtime authority

Runtime evidence outranks catalog assumptions. Static registry data describes expected identity and compatibility constraints; it cannot manufacture successful capability evidence.

## Required release evidence

A v0.18 release requires at minimum a real Blender 5.1.x process proving runtime discovery, Geometry Nodes execution and complete cleanup under `--background --factory-startup --disable-autoexec`.
