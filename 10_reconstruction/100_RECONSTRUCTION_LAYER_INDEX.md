# Reconstruction Layer Index and Controller v0.11

The reconstruction layer performs evidence-constrained 1:1 modeling from concept sheets, blueprints, photos, dimensions and text specifications.

## v0.11 controller

```text
PRELIGHT runtime pin
-> INGEST / CLASSIFY / CALIBRATE
-> PROPERTY-LEVEL AUTHORITY
-> CONFLICT ARBITRATION
-> SHAPE GRAPH
-> APPEARANCE CONTRACT
-> RDL0 DIAGNOSTIC GEOMETRY
-> AUTHORIZE ONE NODE
-> BUILD ONE NODE
-> BUILT_UNVERIFIED
-> PER-VIEW SOURCE PROOF
-> NODE GATE
-> ACCEPTED
-> repeat + RDL barriers
-> APPEARANCE OWNER COVERAGE
-> APPEARANCE FIDELITY GATE
-> RECON FIDELITY GATE
-> runtime
```

## Knowledge groups
- 100–109: evidence, authority, conflict and provenance;
- 110–123: dimensions, landmarks, calibration, silhouette, sections and profiles;
- 124–127: surface/material evidence;
- 128–140: decomposition/construction;
- 141–159: QA, gates, state and governance;
- 160–173: specialized modes/proof integrity;
- 174–179: Shape Graph, RDL, node contracts and multi-section construction;
- 180–183: Reference Appearance Contract, anti-circular validation, part/trim/junction and edge/material/detail fidelity;
- 184–188: v0.11 conflict arbitration, per-view evidence/derived provenance, appearance-owner closure, diagnostic RDL geometry and runtime pin/reuse.

## Fundamental rules
1. No production geometry before Shape Graph/Appearance planning.
2. `CONSTRAINED` is not build permission.
3. Production mutation requires `READY_TO_BUILD` + canonical authorization.
4. `BUILT_UNVERIFIED` blocks children.
5. Every view uses the evidence mode appropriate to its projection/function.
6. Every significant derived parameter is source-backed.
7. Reference conflicts are resolved per property, never by silent averaging.
8. RDL0–RDL3 are judged with neutral diagnostic shading by default.
9. All MUST Appearance Owners are inventoried and accounted before L4/L5 closure.
10. Runtime starts only after appearance/reconstruction gates PASS.

Canonical regression benchmark: `07_examples/80_LAFAR_STREET_LAMP_V010_EXECUTION_DETAIL_REGRESSION_BENCHMARK.md`.
