# Semantic Skill Registry

## Purpose

This registry is the stable routing layer between user intent, knowledge modules, executable primitives, Blender capabilities and validation.

The agent must not jump directly from a natural-language request to ad-hoc `bpy` code when a registered semantic skill already covers the operation.

## Execution maturity

Every semantic skill has one maturity state:

- `KNOWLEDGE_ONLY` — guidance exists, but no stable execution contract.
- `CONTRACT_READY` — stable semantic inputs/outputs, validation and fallback rules exist.
- `EXECUTOR_READY` — a tested implementation is callable through a stable API.
- `RUNTIME_BOUND` — executor is mapped to the tools available in the current agent/Blender integration.

Never claim a skill is `EXECUTOR_READY` or `RUNTIME_BOUND` without evidence from the current runtime.

## Canonical registry

| Skill ID | Purpose | Canonical knowledge | Current maturity | Required capabilities | Validation |
|---|---|---|---|---|---|
| `RECONSTRUCT_REFERENCE` | camera/scale/silhouette/proportion-first reconstruction | `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md` + stage modules | CONTRACT_READY | scene inspect, image/reference access, camera/render | multi-view, silhouette, landmarks, dimensions |
| `REFERENCE_MEASURE` | compact technical-sheet/reference measurement and cross-view aggregation | `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md` + `01_analysis/14_REFERENCE_MEASUREMENT_PROTOCOL.md` | CONTRACT_READY | reference image access, Python/NumPy or equivalent image analysis | provenance, calibration, confidence, cross-view deviation, output budget |
| `HS_PANEL_LINE` | narrow hard-surface seam/groove | `blender-agent-procedural-hard-surface-panel-lines.md` | CONTRACT_READY | Python, BMesh, modifiers, evaluated mesh | path continuity, topology, profile, modifier order |
| `SUBD_TOPOLOGY_CONTROL` | SubD cage design and topology repair | `blender-agent-subdivision-topology-control.md` | CONTRACT_READY | Python/BMesh, Subdivision evaluation | evaluated surface, pinching, density, continuity |
| `TRIM_SHEET_UV` | trim-sheet classification and deterministic UV assignment | `03_modeling/40_TRIM_SHEETS.md` | CONTRACT_READY | mesh UV access, materials | region bounds, density, orientation, intentional overlap |
| `QA_REFERENCE` | visual/numeric reconstruction QA | `10_reconstruction/141_RECONSTRUCTION_QA_CAMERA_RIG.md` through `148_ACCEPTANCE_THRESHOLDS_AND_ERROR_BUDGETS.md` | CONTRACT_READY | camera/render/screenshot, geometry metrics | stage-specific gates |
| `EXPORT_VALIDATE` | export and post-export checks | `04_game_ready/45_GLTF_EXPORT.md`, `05_execution/53_FINAL_VALIDATION.md`, engine profile | KNOWLEDGE_ONLY | save/export/file inspect | runtime contract |

## Registered SubD sub-operations

`SUBD_TOPOLOGY_CONTROL` exposes these semantic operations:

```text
SUBD_REDIRECT_CORNER_SUPPORT
SUBD_BUILD_SUPPORT_BEVEL
SUBD_REPAIR_CURVED_PINCHING
SUBD_TERMINATE_LOCAL_DENSITY
SUBD_CURVED_CYLINDER_RECESS
SUBD_BUILD_POLE_SAFE_SPHERE
SUBD_REPAIR_BRANCH_JUNCTION
SUBD_CURVED_CYLINDER_PROTRUSION
SUBD_TOPOLOGY_AUDIT
```

## Routing precedence

When multiple skills could solve a feature, route by design intent:

```text
technical-sheet/reference measurement
-> REFERENCE_MEASURE

changes silhouette / primary mass
-> base-mesh or reconstruction geometry

wide/deep recess or cutout
-> Boolean/recess modeling knowledge

narrow seam represented as a path
-> HS_PANEL_LINE

smooth control cage under Catmull-Clark
-> SUBD_TOPOLOGY_CONTROL

repeated structural surface treatment
-> TRIM_SHEET_UV

unique local graphic
-> decal workflow
```

A lower-level skill must not override a higher-level reconstruction constraint.

## Skill invocation contract

Before execution the agent records:

```yaml
skill_call:
  skill_id: HS_PANEL_LINE
  feature_id: F023
  maturity: CONTRACT_READY
  inputs_verified: true
  required_capabilities:
    - python_execute
    - bmesh
    - evaluated_geometry
  runtime_bindings_verified: false
```

If `runtime_bindings_verified=false`, the agent must run the Agent Tool API Profile preflight before scene mutation.

For read-only analysis skills such as `REFERENCE_MEASURE`, capability binding may occur without scene mutation, but the agent still must not invent unavailable tools.

## Contract-ready is not executor-ready

A semantic skill can define excellent behavior without having a packaged Python executor.

In that case the agent may still implement the operation through available tools, but it must:

1. follow the skill contract;
2. keep the implementation local and transactional where scene writes occur;
3. validate against the skill's postconditions;
4. avoid presenting an ad-hoc implementation as a permanent library executor;
5. record failed calls and repair iterations;
6. respect the Tool Output Budget.

## Registry update rule

Whenever a new specialized skill is added:

1. assign a stable Skill ID;
2. add its canonical file here;
3. define maturity;
4. define required runtime capabilities;
5. define validation ownership;
6. add routing in `00_governance/04_KNOWLEDGE_ROUTER.md` if it changes task loading;
7. include the canonical file in `MANIFEST.json`.

The registry, Knowledge Router and Manifest must never disagree about the existence of a production skill.
