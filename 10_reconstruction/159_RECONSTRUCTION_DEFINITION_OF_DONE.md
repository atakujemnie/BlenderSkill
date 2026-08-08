# Reconstruction Definition of Done

This module defines **reference-reconstruction acceptance**, corresponding primarily to Level A `RECONSTRUCTION_COMPLETE`.

It does not by itself prove `GAME_READY_COMPLETE` or `PIPELINE_INTEGRATED`.
Use `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md` for the full asset lifecycle.

Asset reconstruction is accepted only when the final state is supported by proof-bearing evidence records, not by narrative self-certification.

## Evidence
- wszystkie źródła zinwentaryzowane;
- konflikty rozwiązane lub jawnie oznaczone;
- unknowns zapisane;
- HARD/MUST/CANONICAL deviations mają status `RESOLVED` z resolution evidence albo `ACCEPTED_BY_AUTHORITY` z authority record;
- bare `PASS` bez evidence kind/provenance nie zamyka wymaganej bramki.

## Geometry
- hard dimensions pass z numeric provenance;
- all canonical silhouettes/views pass poprzez registered comparison, jeśli authority posiada reference dla widoku;
- all D0/D1 landmarks pass z validator evidence;
- all MUST geometry features pass z odpowiednim ROI/numeric/visibility proof.

## Details
- D2/D3 zgodne z evidence;
- branding poprawny lub przekazany do jawnego surface/decal ownera;
- readable front/rear branding ma poprawną orientation po uwzględnieniu project handedness;
- rear/bottom nie pominięte, jeśli mają authority i są wymagane.

## Surface evidence
- material segmentation pass dla target fidelity L4+;
- directional material evidence poprawnie sklasyfikowane;
- emissive/glass geometry/material ownership zdefiniowane;
- visible layered assemblies, takie jak glass/content/recess, mają poprawny layer-stack/visibility proof.

Final runtime textures/bloom do not need to be finished for Level A.

## QA
- QA scene isolation potwierdza brak collision/export proxy contamination;
- multi-view gate pass;
- regression gate pass;
- `RECON_FIDELITY_GATE` pass;
- no unauthorized deviations;
- lighting/material readability has not been used to justify unsupported geometry changes;
- final acceptance bundle zawiera typed evidence + provenance dla wymaganych ownerów.

## Runtime boundary

Reconstruction completion requires that later optimization has a protected Feature Contract, but it does not require all runtime work to be complete.

For higher levels:
- Level B -> clean authoring model/UV/material segmentation;
- Level C -> LOD/collision/bake/package/export/runtime material closure;
- Level D -> project catalog/import integration.

Runtime/engine PASS nigdy nie back-propaguje do Level A.

## Documentation
- reconstruction report;
- reconstruction acceptance evidence bundle;
- evidence/unknown list;
- inferred geometry list;
- known limitations;
- highest completion level must be reported separately.

## Required final record

```yaml
reconstruction_complete:
  status: PASS
  evidence_kind: RECON_FIDELITY_GATE
  provenance_id: recon_gate_report_...
  target_fidelity: L4_or_L5
  canonical_views: {...}
  must_features: [...]
  deviations: [...]
```

## Rule

Do not call the entire asset `DONE` merely because this reconstruction DoD passes.
Do not call reconstruction `PASS` merely because the builder reports that it looks correct.
