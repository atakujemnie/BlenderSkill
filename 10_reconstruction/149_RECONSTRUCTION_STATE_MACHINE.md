# Reconstruction State Machine

## R0 — INGEST
Zapis źródeł i segmentów.

## R1 — CLASSIFY
Projection, view, material/detail/text.

## R2 — AUTHORITY
Evidence + View Authority Matrix.

## R3 — REGISTER
Skala, osie, image planes, camera.

## R4 — CONSTRAIN
Dimension graph, landmarks, feature contract.

## R5 — DECOMPOSE
Object decomposition i strategy map.

## R6 — D0 BLOCKOUT
Bounds + silhouette.

## R7 — D1 PRIMARY FORMS
Major profiles i negative space.

## R8 — D2 FEATURES
Panels, trim, recess, functional details.

## R9 — D3 DETAIL
Fasteners, branding, microgeometry.

## R10 — SURFACE
Materials, UV, decals, emissive.

## R11 — MULTIVIEW QA
Wszystkie kanoniczne widoki.

## R12 — TOPOLOGY/RUNTIME
Optimization bez utraty fidelity.

## R13 — EXPORT VALIDATION

## Backtracking

Każdy FAIL wraca do najwcześniejszego etapu, który może go naprawić.
