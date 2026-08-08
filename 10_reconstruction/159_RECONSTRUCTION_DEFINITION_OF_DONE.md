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

## Shape understanding
- istnieje aktualny `Reconstruction Shape Graph`;
- graph structural validator PASS;
- required design forms są sklasyfikowane G0–G5;
- required nodes mają parent/dependency relations;
- required nodes mają shape class i implementation strategy;
- authoritative views mają jawne responsibilities per node;
- nie ma `UNRESOLVED_REPRESENTATION` dla required G0–G3 node;
- final acceptance odnosi się do konkretnego graph revision.

## Coarse-to-fine execution
- `RDL0_BARRIER: PASS`;
- wszystkie required G1 nodes `ACCEPTED` i `RDL1_BARRIER: PASS`;
- wszystkie required G2 nodes `ACCEPTED` i `RDL2_BARRIER: PASS`;
- wszystkie required G3 nodes `ACCEPTED` i `RDL3_BARRIER: PASS`;
- required G4 edge-language work zaakceptowane zgodnie z target fidelity;
- G5 wymagane przez target fidelity wykonane albo jawnie deferred zgodnie z completion boundary;
- nie istnieje child accepted na failed/unverified required parent revision.

## Geometry
- hard dimensions pass z numeric provenance;
- all canonical silhouettes/views pass poprzez registered comparison, jeśli authority posiada reference dla widoku;
- all primary landmarks/proportions pass z validator evidence;
- all MUST geometry features pass z odpowiednim ROI/numeric/visibility proof;
- multi-section/profile nodes mają station/cross-section proof, jeśli reprezentacja tego wymaga.

## Details
- structural features zgodne z evidence;
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
- każdy required Shape Node ma własny node acceptance record;
- multi-view gate pass;
- regression gate pass;
- RDL barriers pass;
- `RECON_FIDELITY_GATE` pass;
- no unauthorized deviations;
- lighting/material readability has not been used to justify unsupported geometry changes;
- final acceptance bundle zawiera typed evidence + provenance dla wymaganych ownerów.

## Runtime boundary

Reconstruction completion requires that later optimization has a protected Feature Contract **i zaakceptowany Shape Graph**, ale nie wymaga całego runtime finish.

For higher levels:
- Level B -> clean authoring model/UV/material segmentation;
- Level C -> LOD/collision/bake/package/export/runtime material closure;
- Level D -> project catalog/import integration.

Runtime/engine PASS nigdy nie back-propaguje do Level A.

## Documentation
- reconstruction report;
- Shape Graph + graph revision;
- node acceptance records;
- RDL stage barrier records;
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
  graph_revision: sg_...
  rdl_barriers:
    RDL0: PASS
    RDL1: PASS
    RDL2: PASS
    RDL3: PASS
    RDL4: PASS
  target_fidelity: L4_or_L5
  canonical_views: {...}
  must_features: [...]
  deviations: [...]
```

## Rule

Do not call the entire asset `DONE` merely because this reconstruction DoD passes.
Do not call reconstruction `PASS` merely because the builder reports that it looks correct.
Do not call reconstruction `PASS`, jeśli primary forms nie zostały rozwiązane node-by-node przed detalem.
