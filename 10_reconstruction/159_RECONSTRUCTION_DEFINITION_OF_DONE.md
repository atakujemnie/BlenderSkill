# Reconstruction Definition of Done

This module defines **reference-reconstruction acceptance**, corresponding primarily to Level A `RECONSTRUCTION_COMPLETE`.

It does not by itself prove `GAME_READY_COMPLETE` or `PIPELINE_INTEGRATED`.
Use `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md` for the full asset lifecycle.

Asset reconstruction is accepted when:

## Evidence
- wszystkie źródła zinwentaryzowane,
- konflikty rozwiązane lub jawnie oznaczone,
- unknowns zapisane.

## Geometry
- hard dimensions pass,
- all canonical silhouettes pass,
- all D0/D1 landmarks pass,
- all MUST geometry features pass.

## Details
- D2/D3 zgodne z evidence,
- branding poprawny lub przekazany do jawnego surface/decal ownera,
- rear/bottom nie pominięte, jeśli mają authority i są wymagane.

## Surface evidence
- material segmentation pass,
- directional material evidence poprawnie sklasyfikowane,
- emissive/glass geometry/material ownership zdefiniowane.

Final runtime textures/bloom do not need to be finished for Level A.

## QA
- multi-view gate pass,
- regression gate pass,
- no unauthorized deviations,
- lighting/material readability has not been used to justify unsupported geometry changes.

## Runtime boundary

Reconstruction completion requires that later optimization has a protected Feature Contract, but it does not require all runtime work to be complete.

For higher levels:
- Level B -> clean authoring model/UV/material segmentation;
- Level C -> LOD/collision/bake/export/runtime material closure;
- Level D -> project catalog/import integration.

## Documentation
- reconstruction report,
- evidence/unknown list,
- inferred geometry list,
- known limitations,
- highest completion level must be reported separately.

## Rule

Do not call the entire asset `DONE` merely because this reconstruction DoD passes.
