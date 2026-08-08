# Blender AI Agent Library v0.7.0 — Full compiled snapshot

> GENERATED FILE. Do not edit directly. Canonical source: modular files listed in MANIFEST.json.


---

## FILE: `00_governance/00_AGENT_CHARTER.md`

# Agent Charter

## Rola

Jesteś jednocześnie:
- analitykiem referencji,
- technical artistem,
- modelerem 3D,
- specjalistą Blender Python API,
- game asset artistem,
- kontrolerem jakości.

Nie wolno Ci traktować modelowania jako pojedynczego zadania programistycznego polegającego na "wygenerowaniu geometrii".

## Priorytety

1. zgodność z wizją,
2. poprawność proporcji i sylwetki,
3. zachowanie cech rozpoznawczych,
4. techniczna poprawność modelu,
5. edytowalność,
6. koszt runtime,
7. minimalizacja liczby operacji i tokenów.

## Zasady bezwzględne

- Nie zaczynaj budowania bez planu.
- Nie zgaduj wymiarów, jeżeli można je wyprowadzić z referencji, istniejącej sceny lub znanego modułu.
- Nie usuwaj istniejących detali bez jawnej przyczyny.
- Nie zastępuj cechy `MUST` "podobnym" detalem.
- Nie wykonuj dużych destrukcyjnych zmian bez checkpointu.
- Nie używaj operatora UI tylko dlatego, że jest znany z ręcznej pracy w Blenderze.
- Nie opieraj logiki na aktywnym zaznaczeniu, jeżeli można odwołać się bezpośrednio do obiektów/danych.
- Nie aplikuj modyfikatorów przed momentem, w którym ich zamrożenie jest konieczne.
- Nie trianguluj źródłowego modelu tylko dlatego, że runtime używa trójkątów.
- Nie zwiększaj gęstości siatki bez uzasadnienia sylwetką, deformacją lub bake.
- Nie twórz materiałów proceduralnych, których docelowy eksport nie przenosi, bez planu bake.
- Nie uznawaj renderu beauty za wystarczającą kontrolę jakości.

## Zasada dowodu

Każde istotne stwierdzenie o stanie assetu powinno pochodzić z:
- danych sceny,
- pomiaru,
- renderu kontrolnego,
- widoku ortograficznego,
- wireframe,
- statystyk siatki,
- jawnej referencji.

## Zasada reversible-first

Preferuj operacje odwracalne:
- modifier zamiast destrukcyjnego cięcia,
- duplikat / backup obiektu przed ryzykownym etapem,
- osobne obiekty dla niezależnych części,
- parametry zamiast ręcznego przesuwania dużej liczby wierzchołków,
- instancje zamiast kopiowania geometrii.

## Stop conditions

Przerwij wykonanie i wróć do analizy, jeśli:
- nie można jednoznacznie wskazać frontu assetu,
- skala jest nieznana i wpływa na funkcję,
- referencje są sprzeczne,
- dwie cechy `MUST` wzajemnie się wykluczają,
- planowana operacja zniszczy nieodtwarzalne dane,
- agent nie rozumie skutku danego narzędzia API.


---

## FILE: `00_governance/01_SOURCE_OF_TRUTH.md`

# Source of Truth

## Kolejność nadrzędności

### 1. User intent
Jawne polecenie użytkownika jest nadrzędne.

### 2. Approved reference
Jeżeli użytkownik zaakceptował konkretny wygląd, staje się on referencją kanoniczną.

### 3. Project asset contract
Wymiary, skala świata, texel density, naming, pivot, format eksportu, limity i standardy silnika.

### 4. Current Blender scene
Rzeczywisty stan danych jest ważniejszy niż pamięć agenta o tym, co "powinno" znajdować się w scenie.

### 5. Library rules
Niniejsze procedury.

### 6. External technical documentation
Oficjalne API i specyfikacje.

### 7. Heuristics
Doświadczenie i przypuszczenia.

## Konflikt źródeł

Jeżeli dwa źródła są sprzeczne:
- nie mieszaj ich,
- wskaż konflikt wewnętrznie,
- wybierz źródło o wyższym priorytecie,
- zachowaj informację o odrzuconej interpretacji.

## Zakaz "ulepszania referencji"

Agent nie ma prawa:
- dodawać ozdobników,
- zmieniać proporcji dla "lepszego designu",
- symetryzować świadomej asymetrii,
- upraszczać charakterystycznej cechy,
- zaokrąglać ostrych form tylko dlatego, że bevel wygląda bardziej realistycznie.

Wyjątek: wymaganie runtime lub jawna decyzja projektowa.


---

## FILE: `00_governance/02_STATE_MACHINE.md`

# Agent State Machine

## Stany

### S0 — DISCOVER
Cel:
- ustalić narzędzia, Blender version, stan sceny, jednostki, aktywny plik;
- związać capabilities;
- załadować matching project profile.

Wyjście:
`Scene Snapshot` + Tool/Project Context.

### S1 — ANALYZE
Cel:
- zrozumieć funkcję assetu;
- zinwentaryzować evidence/views;
- wyodrębnić dimensions/landmarks/features;
- określić niewiadome i conflicts.

Wyjście:
`Asset Brief` + Reference/Evidence state.

### S2 — CONTRACT
Cel:
- utworzyć Feature Contract;
- oznaczyć `MUST`, `SHOULD`, `OPTIONAL`;
- przypisać metryki, tolerancje i authority.

Wyjście:
`Feature Contract`.

### S3 — PLAN / SHAPE UNDERSTANDING

Dla reference reconstruction ten stan **nie zaczyna od operatorów Blendera**.

Cel:
- rozbić asset na G0–G5 design forms;
- zbudować `Reconstruction Shape Graph`;
- przypisać parent/dependencies;
- sklasyfikować mathematical shape representation;
- przypisać authoritative views + controlled properties;
- przypisać RDL0–RDL5;
- zaplanować node gates i stage barriers;
- dopiero potem dobrać semantic skills/implementation.

Wyjście:
`Shape Graph` + `Node Contracts` + `RDL Plan`.

`Shape Graph != PASS` blokuje produkcyjną geometrię poza diagnostic RDL0.

### S4 — COARSE FORM / BLOCKOUT

Dla zwykłych assetów: blockout.

Dla reference reconstruction:
- RDL0 envelope;
- RDL1 primary forms node-by-node;
- każdy node musi przejść required multi-view gate;
- RDL1 stage barrier przed secondary forms.

Zakaz:
- budowy G2–G5 przed odpowiednim barrier;
- finalnych materiałów;
- monolitycznego builda tworzącego wiele poziomów formy.

### S5 — STRUCTURAL FORMS / FEATURES

Dla reconstruction:
- RDL2 secondary structural forms node-by-node;
- RDL3 structural features tylko na ACCEPTED hosts;
- leaf skills takie jak panel lines/recess/layer stack dopiero tutaj.

### S6 — EDGE / SECONDARY DETAIL

Dla reconstruction:
- RDL4 edge language;
- bevel/fillet/chamfer/SubD support dopiero po accepted form;
- microgeometry wymagane przez contract.

### S7 — SHADING_UV_MATERIAL

Dla reconstruction najpierw RDL5 surface/detail, potem:
- UV;
- normals/shading;
- runtime material strategy.

UV/runtime nie może rozpocząć się, jeżeli Reconstruction Fidelity Gate jeszcze nie PASS.

### S8 — GAME_READY
Cel:
- runtime LOD;
- collision;
- pivot/naming;
- bake/runtime textures;
- optimization;
- package preparation.

Runtime LOD jest downstream od RDL. `RDL != LOD`.

### S9 — VALIDATE
Cel:
- reconstruction final fidelity proof;
- mesh/runtime validation;
- package readback;
- completion gate.

### S10 — EXPORT / INTEGRATE
Cel:
- export;
- round-trip invariants;
- target-engine proof dla Level D;
- final completion report.

## Core gates

Reference reconstruction:

```text
Shape Graph PASS
-> RDL0 PASS
-> G1 node gates + RDL1 barrier
-> G2 node gates + RDL2 barrier
-> G3 node gates + RDL3 barrier
-> RDL4 edge barrier
-> RDL5 as required
-> RECON_FIDELITY_GATE
-> runtime/game-ready
```

Nie wolno:
- budować child na failed/unverified required parent;
- używać detail skill do naprawy primary form;
- przejść do runtime przy reconstruction FAIL/UNVERIFIED;
- maskować błędu późniejszym etapem.

## Cofnięcie

Każdy failed gate kieruje do najwcześniejszego ownera:
- evidence/registration;
- Shape Graph/representation;
- konkretny Shape Node;
- właściwy RDL;
- runtime stage.

## Reconstruction branch

Dla wielowidokowej/blueprint/concept-sheet reconstruction `10_reconstruction/149_RECONSTRUCTION_STATE_MACHINE.md` rozwija S1–S9 i jest canonical controllerem formy.


---

## FILE: `00_governance/03_ROLE_SPLIT.md`

# Internal Role Split

Jeden agent powinien logicznie przełączać role.

## Planner
Nie modyfikuje sceny.
Tworzy:
- brief,
- Feature Contract,
- Build Plan,
- kryteria odbioru.

## Builder
Wykonuje wyłącznie zatwierdzony plan.
Nie zmienia celu podczas implementacji.

## Inspector
Nie poprawia.
Tylko mierzy, renderuje i wykrywa różnice.

## Repairer
Dostaje:
- konkretny błąd,
- obszar,
- oczekiwany stan,
- minimalny zakres naprawy.

## Exporter
Nie poprawia designu.
Dba o pipeline techniczny.

## Dlaczego rozdzielać role

Najczęstszy błąd agentów to jednoczesne:
- wymyślanie,
- modelowanie,
- ocenianie,
- naprawianie.

Powoduje to dryf celu. Rozdział ról zmusza do porównywania wykonania z wcześniejszym kontraktem.


---

## FILE: `00_governance/04_KNOWLEDGE_ROUTER.md`

# Knowledge Router

Agent nie ładuje całej biblioteki. Router wybiera najmniejszy Task Pack dla current state, failing evidence i Shape Node.

Canonical rule:

```text
intent/current state
-> Task Pack
-> semantic skill
-> executor/tool binding
-> compact evidence
```

## SESSION_PREFLIGHT

Load:
- Agent Charter;
- Semantic Skill Registry;
- Tool Discovery/Profile;
- Blender 5.1 Compatibility Matrix;
- Scene Inspection;
- matching Project Asset Pipeline Profile.

Persist Tool Registry, Blender version, project profile, runtime path context.

Nie rediscoveruj stable project facts per asset.

---

# Reference reconstruction v0.9

## 1. Technical-sheet analyze

Use `RECON_TECHNICAL_SHEET_ANALYZE`:
- Evidence Model;
- ingestion/view classification/authority;
- measurement/calibration;
- Reference Analysis Cache.

Preferred skills:
- `REFERENCE_MEASURE`;
- `REFERENCE_OVERLAY_VALIDATE` only after registration exists.

Po `ANALYZE: PASS` nie wracaj do broad exploration bez konkretnego conflict/ROI/source update.

## 2. Shape understanding — mandatory before production geometry

Use `RECON_SHAPE_GRAPH_PLAN`.

Load:
- `128_RECONSTRUCTION_OBJECT_DECOMPOSITION.md`;
- `174_RECONSTRUCTION_SHAPE_GRAPH.md`;
- `176_RECONSTRUCTION_NODE_CONTRACT.md`;
- `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md`;
- prompt 68;
- script pattern 95.

Preferred skills:
- `SHAPE_GRAPH`;
- `SHAPE_CLASSIFY`.

Required persistent output:
- Shape Graph revision;
- G0–G5 hierarchy;
- RDL0–RDL5 assignment;
- node parent/dependencies;
- shape class;
- authoritative views + controlled properties;
- node validation contract.

`SHAPE_GRAPH != PASS` blocks production geometry except diagnostic RDL0.

## 3. RDL0 envelope

Use `RECON_RDL0`.

Only:
- global bounds;
- axes;
- ground/contact;
- minimal envelope carrier.

Validate FRONT/SIDE/TOP where authoritative.

No detail skills.

## 4. RDL1 primary forms

Use `RECON_NODE_BUILD` **one Shape Node at a time**.

Canonical loop:

```text
SHAPE_GRAPH ready node
-> choose representation skill
-> build/repair current node only
-> QA_SCENE_ISOLATE
-> registered required-view validation
-> numeric/section checks
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | FAIL
```

After all required G1 nodes:
`SHAPE_GRAPH.evaluate_stage_barrier(RDL1)`.

Do not load G2–G5 skills on RDL1 FAIL.

## 5. Shape representation routing

```text
axisymmetric profile
-> AXISYMMETRIC_PROFILE

width/depth/corner treatment change across stations
-> SECTION_LOFT_HARD_SURFACE

structural transition between two sections
-> SECTION_LOFT_HARD_SURFACE

stable 2D profile + depth
-> EXTRUDED_PROFILE / direct mesh strategy

path-driven profile
-> PROFILE_SWEEP / curves

smooth compound freeform without stable sections
-> SUBD_TOPOLOGY_CONTROL
```

### Box-abuse trigger

If primary form changes width + depth + corner treatment along an axis:

```text
PARAMETRIC_BOX + BEVEL
-> not default
-> SHAPE_CLASSIFY
-> MULTI_SECTION_LOFT or SUBD_FREEFORM candidate
```

## 6. RDL2 secondary structural forms

Same node-by-node loop.

Typical:
- side frames;
- display housing;
- utility modules;
- large service panels;
- major trims.

Required G2 stage barrier before RDL3.

## 7. RDL3 structural features

Leaf skills become available only on `ACCEPTED` hosts:

```text
narrow seam/groove -> HS_PANEL_LINE
recess -> boolean/direct recess playbook
layered glass/content -> LAYER_STACK_VALIDATE
radial holes/fasteners -> RADIAL_REPEAT
```

No host acceptance -> feature `BLOCKED`.

## 8. RDL4 edge language

Load edge/bevel/continuity/SubD support modules only now.

Rule:
`shape first -> edge treatment second`.

Bevel cannot repair wrong primary section.

## 9. RDL5 surface/detail

Load branding, materials, decals, emissive, civic finish only after structural barriers.

## 10. Reconstruction final gate

Use:
- `QA_SCENE_ISOLATE`;
- `REFERENCE_OVERLAY_VALIDATE`;
- `RECONSTRUCTION_NODE_GATE` records;
- RDL barriers;
- `RECON_FIDELITY_GATE`.

Runtime is forbidden while final gate is FAIL/UNVERIFIED.

---

# Existing specialized routes

## Panel line
`HS_PANEL_LINE`; add SubD skill only if evaluated cage/flow requires it.

## SubD topology
`SUBD_TOPOLOGY_CONTROL` + topology/normals rules.

## Mesh validation
`MESH_VALIDATE`. Every mesh declares topology intent.

## Civic material finish
`MATERIAL_FINISH_CIVIC`; no uniform global grunge.

## Emissive
`EMISSIVE_HANDOFF`; authored emitter and engine bloom are separate gates.

## UV atlas / runtime bake
`UV_ATLAS_CONTRACT` -> `BAKE_RUNTIME_TEXTURES` -> `BAKE_VALIDATE`.

Use stable semantic part IDs. Missing atlas assignment = FAIL.

## QA/bake contamination
`QA_SCENE_ISOLATE`. `hide_viewport` is not render proof.

## Stale external image in Blender
`IMAGE_CACHE_COHERENCE` before rebake/UV changes.

## Local repair after accepted runtime stages
`PIPELINE_DAG_PLAN` before replaying build/bake/export. Execute dirty dependency closure only.

---

# Game-ready finishing

Use `GAME_READY_FINISH` only after `RECON_FIDELITY_GATE: PASS`.

Preferred skills:
- `MESH_VALIDATE`;
- `UV_ATLAS_CONTRACT`;
- `BAKE_RUNTIME_TEXTURES`;
- `BAKE_VALIDATE`;
- `IMAGE_CACHE_COHERENCE`;
- `PIPELINE_DAG_PLAN`;
- `RUNTIME_PATH_RESOLVE`;
- `RUNTIME_PACKAGE_VALIDATE`;
- `EXPORT_ROUNDTRIP_VALIDATE`;
- `ASSET_COMPLETION`.

Order:

```text
runtime path
-> LOD/collision
-> UV contract
-> dirty bake stages
-> bake validation/cache coherence
-> runtime material
-> export/package readback
-> round-trip invariants
-> baked runtime QA
-> completion gate
```

Runtime LOD is downstream from RDL and must not be used as reconstruction progression state.

---

# Pipeline integration

Use `PIPELINE_INTEGRATION` only when target is Level D.

Load verified Project Profile, runtime-root, package, catalog, Engine Smoke Test, Test Oracle.

For current RPG profile reuse:
- `<repo>/Assets/GameAssets`;
- one glTF multi-node LOD packaging;
- current MIRROR_X contract while valid;
- `Source/Engine/AssetCatalog.cpp`;
- `Engine::Model::Load`;
- `Tests/ModelTests.cpp`;
- `Build/windows-debug` / `ModelTests`;
- direct executable exit status.

Blender glTF import = Level C round-trip evidence, not Level D.

---

# Failure routing principles

```text
looks wrong in one view
-> registration/parameters/shape representation

FRONT pass + SIDE/TOP compound-form fail
-> SHAPE_CLASSIFY before random parameter tweaking

child feature fails because host contour wrong
-> parent Shape Node owner

correct source geometry + exported dimension fail
-> EXPORT_ROUNDTRIP_VALIDATE

parseable glTF + missing TEXCOORD_0
-> RUNTIME_PACKAGE_VALIDATE

ambiguous test success
-> TEST_ORACLE
```

After one corrected retry of same strategy, second proven failure requires re-inspection + strategy switch.

---

# Output budget

Use:

```text
compute locally
-> compact node/stage report
-> decision
```

Do not return raw arrays/full logs/full generated scripts unless diagnostic need requires them.


---

## FILE: `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`

# Semantic Skill Registry

## Purpose

Stable routing layer between user intent, reconstruction semantics, knowledge modules, executors and validation.

Agent nie przechodzi bezpośrednio z natural-language request do ad-hoc `bpy`, jeśli zarejestrowany skill już opisuje operację.

## Execution maturity

- `KNOWLEDGE_ONLY` — guidance exists, no stable execution contract.
- `CONTRACT_READY` — stable inputs/outputs/validation exist.
- `EXECUTOR_READY` — tested implementation callable through stable API.
- `RUNTIME_BOUND` — executor mapped to current runtime tools.

Nie claimuj wyższego maturity bez evidence.

## Canonical registry

| Skill ID | Purpose | Canonical knowledge | Maturity | Validation |
|---|---|---|---|---|
| `RECONSTRUCT_REFERENCE` | end-to-end reference reconstruction controller | `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md` | CONTRACT_READY | evidence, Shape Graph, RDL barriers, fidelity gate |
| `REFERENCE_MEASURE` | compact reference measurement | `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md`; `executors/reference_measure.py` | CONTRACT_READY | provenance, calibration, confidence |
| `REFERENCE_OVERLAY_VALIDATE` | registered reference-vs-candidate silhouette/ROI comparison | `142`, `143`, `171`; `executors/reference_overlay_validate.py` | CONTRACT_READY | IoU, contour delta, MUST ROI |
| `SHAPE_GRAPH` | validate hierarchy/dependencies/readiness of design forms | `174_RECONSTRUCTION_SHAPE_GRAPH.md`, `95_SHAPE_GRAPH_VALIDATOR_PATTERN.md`; `executors/shape_graph.py` | CONTRACT_READY | DAG, levels, RDL, parent/dependency readiness, stage barrier |
| `SHAPE_CLASSIFY` | choose mathematical representation before Blender technique | `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md` | CONTRACT_READY | evidence-backed shape class, rejected alternatives |
| `RECONSTRUCTION_NODE_GATE` | proof-bearing acceptance of one Shape Node | `176_RECONSTRUCTION_NODE_CONTRACT.md`, `178_NODE_BY_NODE_MULTI_VIEW_VALIDATION.md`; `executors/reconstruction_node_gate.py` | CONTRACT_READY | parent/dependency, isolation, per-view evidence, numeric/section/regression |
| `SECTION_LOFT_HARD_SURFACE` | deterministic multi-section base/shell/transition construction | `179_MULTI_SECTION_LOFT_AND_PROFILE_CAGE.md`, playbook 118; `executors/section_loft.py` | CONTRACT_READY | station ordering, sample correspondence, mesh data, multi-view/section proof |
| `LAYER_STACK_VALIDATE` | visibility/order validation for layered assemblies | `172_VISIBLE_LAYER_STACK_CONTRACT.md`; `executors/layer_stack_validate.py` | CONTRACT_READY | front-to-back order, burial, facing |
| `RECON_FIDELITY_GATE` | final proof-bearing Level A transition gate | `05_execution/69_RECONSTRUCTION_FIDELITY_GATE.md`, `173`; `executors/fidelity_gate.py` | CONTRACT_READY | typed evidence, canonical views, MUST features, authority closure |
| `AXISYMMETRIC_PROFILE` | revolved hard-surface profile | `03_modeling/45_AXISYMMETRIC_PROFILE_ASSET_PRIMITIVE.md`; `executors/axisymmetric_profile.py` | CONTRACT_READY | bounds, continuity, topology |
| `RADIAL_REPEAT` | repeated radial details | playbook 110; `executors/radial_repeat.py` | CONTRACT_READY | count, phase, annulus |
| `HS_PANEL_LINE` | narrow seam/groove | `blender-agent-procedural-hard-surface-panel-lines.md` | CONTRACT_READY | path/profile/topology |
| `SUBD_TOPOLOGY_CONTROL` | Catmull-Clark cage design/repair | `blender-agent-subdivision-topology-control.md` | CONTRACT_READY | evaluated surface, pinching, continuity |
| `TRIM_SHEET_UV` | trim-sheet UV strategy | `03_modeling/40_TRIM_SHEETS.md` | CONTRACT_READY | region/density/orientation |
| `UV_ATLAS_CONTRACT` | stable atlas ownership across LODs | `04_game_ready/52_UV_ATLAS_LOD_STABILITY_CONTRACT.md`; `executors/uv_atlas_contract.py` | CONTRACT_READY | semantic part IDs, LOD consistency |
| `MESH_VALIDATE` | contract-aware mesh audit | `08_scripts/92_MESH_CONTRACT_VALIDATOR_PATTERN.md`; `executors/mesh_validate.py` | EXECUTOR_READY | topology intent, manifold/boundaries/UV/tris |
| `RUNTIME_COMPAT` | Blender/runtime API discovery | `02_blender_api/29_BLENDER_5_1_COMPATIBILITY_MATRIX.md`; `executors/runtime_compat.py` | CONTRACT_READY | discovered enums/properties/paths |
| `QA_SCENE_ISOLATE` | non-destructive QA/bake scene isolation | `08_scripts/83_QA_RENDER_SCRIPT_PATTERN.md`; `executors/qa_scene_isolation.py` | CONTRACT_READY | render state restored, contamination prevented |
| `MATERIAL_FINISH_CIVIC` | maintained civic material finish | playbook 114 | CONTRACT_READY | macro/meso/micro breakup |
| `EMISSIVE_HANDOFF` | separate authored emitter from runtime glow | `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md` | CONTRACT_READY | emitter/export/runtime status |
| `BAKE_RUNTIME_TEXTURES` | deterministic runtime texture bake | `04_game_ready/50`, `51`; `executors/bake_runtime_textures.py` | CONTRACT_READY | bake result/channel semantics |
| `BAKE_VALIDATE` | semantic baked-map validation | `08_scripts/93_BAKE_OUTPUT_VALIDATION_PATTERN.md`; `executors/bake_validate.py` | CONTRACT_READY | ranges/regions/degeneracy |
| `IMAGE_CACHE_COHERENCE` | synchronize disk texture and Blender datablock | `02_blender_api/30_IMAGE_DATABLOCK_CACHE_COHERENCE.md`; `executors/image_cache_coherence.py` | CONTRACT_READY | path/reload/colorspace/binding |
| `PIPELINE_DAG_PLAN` | minimal dirty execution closure | `05_execution/68_PIPELINE_DAG_EXECUTOR_AND_STAGE_REUSE.md`; `executors/pipeline_dag.py` | CONTRACT_READY | DAG/execute/reuse plan |
| `RUNTIME_PACKAGE_VALIDATE` | validate glTF package/attributes/transforms | `09_engine/94`, `96`; `executors/gltf_package_validate.py` | CONTRACT_READY | nodes/materials/images/TEXCOORD/TRS |
| `EXPORT_ROUNDTRIP_VALIDATE` | re-import export and check invariants | `05_execution/67_POST_EXPORT_INVARIANT_AND_ROUNDTRIP_VALIDATION.md`; `executors/export_roundtrip_validate.py` | CONTRACT_READY | dimensions/contact/material survival |
| `RUNTIME_PATH_RESOLVE` | resolve engine-visible runtime root | `09_engine/95_RUNTIME_ASSET_ROOT_AND_PATH_CONTRACT.md`; `executors/runtime_path_resolver.py` | CONTRACT_READY | canonical root/containment |
| `TEST_ORACLE` | trustworthy process exit/bite test | `05_execution/66_TEST_ORACLE_EXIT_CODE_AND_BITE_TEST.md`; `executors/test_oracle.py` | CONTRACT_READY | direct status/intended assertion |
| `ENGINE_INTEGRATION_PROOF` | Level D target-engine proof | `09_engine/96_ENGINE_INTEGRATION_SMOKE_TEST_CONTRACT.md` | CONTRACT_READY | loader/instantiation + oracle |
| `QA_REFERENCE` | reconstruction visual/numeric QA | `141`–`148` + v0.8/v0.9 validation modules | CONTRACT_READY | node/stage/final evidence |
| `ASSET_COMPLETION` | determine true completion level | `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md`; `executors/completion_gate.py` | CONTRACT_READY | A/B/C/D gate hierarchy |
| `ASSET_CATALOG_INTEGRATE` | project catalog registration | `09_engine/93_ASSET_CATALOG_INTEGRATION_PROTOCOL.md` | KNOWLEDGE_ONLY | readback/unique ID/import |
| `EXPORT_VALIDATE` | export and post-export checks | `04_game_ready/45_GLTF_EXPORT.md`, `05_execution/53_FINAL_VALIDATION.md` | KNOWLEDGE_ONLY | runtime contract |

## v0.9 reconstruction routing precedence

```text
reference ingest/measurement
-> REFERENCE_MEASURE

before production geometry
-> SHAPE_GRAPH + SHAPE_CLASSIFY

one node ready to build/repair
-> node's representation skill
-> RECONSTRUCTION_NODE_GATE

width/depth/corner profile changes across stations
-> SECTION_LOFT_HARD_SURFACE

axisymmetric profile
-> AXISYMMETRIC_PROFILE

narrow seam on ACCEPTED host
-> HS_PANEL_LINE

SubD/freeform cage on ACCEPTED structural node
-> SUBD_TOPOLOGY_CONTROL

layered visible assembly
-> LAYER_STACK_VALIDATE

registered view comparison
-> REFERENCE_OVERLAY_VALIDATE

end of each RDL
-> SHAPE_GRAPH stage barrier

claiming Level A / entering runtime
-> RECON_FIDELITY_GATE
```

## Host-before-leaf rule

Leaf skills nie mogą pełnić roli shape-understanding layer.

Przykłady:
- `HS_PANEL_LINE` dopiero po host node `ACCEPTED`;
- bevel/edge work dopiero RDL4;
- decals/materials dopiero po structural acceptance;
- `SECTION_LOFT_HARD_SURFACE` może być primary-form skill, bo reprezentuje samą formę, nie detal.

## Box-abuse route

Jeżeli primary node zmienia jednocześnie width/depth/corner treatment wzdłuż osi:

```text
PARAMETRIC_BOX + BEVEL
-> do not default
-> SHAPE_CLASSIFY
-> likely SECTION_LOFT_HARD_SURFACE or SUBD_FREEFORM
```

## Runtime evidence retained from earlier releases

`MESH_VALIDATE` pozostaje `EXECUTOR_READY` dzięki realnemu Blender 5.1 benchmarkowi bollarda.

Nowe executory v0.8/v0.9 pozostają `CONTRACT_READY`, dopóki kolejny realny benchmark nie wykona ich kontraktów w docelowym środowisku.

## Packaged executor status

```text
REFERENCE_MEASURE          -> executors/reference_measure.py              CONTRACT_READY
REFERENCE_OVERLAY_VALIDATE -> executors/reference_overlay_validate.py     CONTRACT_READY
SHAPE_GRAPH                -> executors/shape_graph.py                     CONTRACT_READY
RECONSTRUCTION_NODE_GATE   -> executors/reconstruction_node_gate.py        CONTRACT_READY
SECTION_LOFT_HARD_SURFACE  -> executors/section_loft.py                    CONTRACT_READY
LAYER_STACK_VALIDATE       -> executors/layer_stack_validate.py            CONTRACT_READY
RECON_FIDELITY_GATE        -> executors/fidelity_gate.py                   CONTRACT_READY
AXISYMMETRIC_PROFILE       -> executors/axisymmetric_profile.py            CONTRACT_READY
RADIAL_REPEAT              -> executors/radial_repeat.py                   CONTRACT_READY
MESH_VALIDATE              -> executors/mesh_validate.py                   EXECUTOR_READY
RUNTIME_COMPAT             -> executors/runtime_compat.py                  CONTRACT_READY
QA_SCENE_ISOLATE           -> executors/qa_scene_isolation.py             CONTRACT_READY
ASSET_COMPLETION           -> executors/completion_gate.py                 CONTRACT_READY
UV_ATLAS_CONTRACT          -> executors/uv_atlas_contract.py               CONTRACT_READY
BAKE_RUNTIME_TEXTURES      -> executors/bake_runtime_textures.py           CONTRACT_READY
BAKE_VALIDATE              -> executors/bake_validate.py                   CONTRACT_READY
IMAGE_CACHE_COHERENCE      -> executors/image_cache_coherence.py           CONTRACT_READY
PIPELINE_DAG_PLAN          -> executors/pipeline_dag.py                     CONTRACT_READY
RUNTIME_PACKAGE_VALIDATE   -> executors/gltf_package_validate.py           CONTRACT_READY
EXPORT_ROUNDTRIP_VALIDATE  -> executors/export_roundtrip_validate.py       CONTRACT_READY
RUNTIME_PATH_RESOLVE       -> executors/runtime_path_resolver.py           CONTRACT_READY
TEST_ORACLE                -> executors/test_oracle.py                      CONTRACT_READY
```

## Skill invocation contract

```yaml
skill_call:
  skill_id: SECTION_LOFT_HARD_SURFACE
  shape_node_id: BASE_PLINTH
  graph_revision: sg_004
  maturity: CONTRACT_READY
  inputs_verified: true
  parent_dependencies_accepted: true
  required_capabilities: [python, blender_mesh_create]
  runtime_bindings_verified: false
```

If runtime binding is required and unverified, perform capability preflight before mutation.

## Contract-ready is not executor-ready

A CONTRACT_READY skill may be implemented through current tools, but agent must:
1. follow semantic contract;
2. keep mutation local/idempotent;
3. validate postconditions;
4. not describe it as proven executor;
5. respect retry/strategy-switch rules;
6. persist compact state/evidence;
7. never replace proof with narrative PASS.

## Reuse before generation

Before generating helpers search this registry and `executors/`.

Do not locally rewrite compatible implementations of:
- Shape Graph validation/readiness/stage barriers;
- node acceptance aggregation;
- multi-section loft ring/bridge generation;
- reference measurement/overlay;
- layered visibility validation;
- reconstruction fidelity aggregation;
- axisymmetric profile/radial repeat;
- mesh/bake/cache/package/path/test validators.

## Registry update rule

New production skill requires:
1. stable Skill ID;
2. canonical knowledge path;
3. maturity;
4. capabilities;
5. validation owner;
6. Knowledge Router route;
7. MANIFEST inclusion for canonical MD.

Registry, Router, Task Packs and Manifest must agree.


---

## FILE: `00_governance/06_TASK_PACK_PROTOCOL.md`

# Task Pack Protocol

## Purpose

A `Task Pack` is the smallest knowledge set for the current state. In v0.9 reconstruction it is also scoped to one `Shape Node` whenever geometry is being built.

```text
state + RDL + Shape Node + measured failure
-> Task Pack
-> execute
-> validate
-> persist compact state
-> advance through barrier
```

## SESSION_PREFLIGHT

Load Agent Charter, Semantic Skill Registry, tool/runtime compatibility, Scene Inspection and matching Project Profile.

Persist Tool Registry, Blender version, project profile and runtime path context.

## RECON_TECHNICAL_SHEET_ANALYZE

Load Evidence Model, reference ingestion/classification, View Authority Matrix, measurement/calibration and Reference Analysis Cache.

Preferred skill: `REFERENCE_MEASURE`.

Output: Reference Registry, Evidence Ledger, locked dimensions, authority/conflicts.

Production geometry, UV, LOD and export are forbidden here.

## RECON_SHAPE_GRAPH_PLAN

Mandatory before production geometry.

Load:
- `128_RECONSTRUCTION_OBJECT_DECOMPOSITION.md`;
- `129_FEATURE_TO_MODELING_STRATEGY_MAP.md`;
- `174_RECONSTRUCTION_SHAPE_GRAPH.md`;
- `175_RECONSTRUCTION_DETAIL_LEVELS.md`;
- `176_RECONSTRUCTION_NODE_CONTRACT.md`;
- `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md`;
- prompt 68;
- validator pattern 95.

Preferred skills: `SHAPE_GRAPH`, `SHAPE_CLASSIFY`.

Persist G0-G5 hierarchy, RDL assignments, Node Contracts, parent/dependencies, representation decisions and view responsibilities.

Gate: `shape_graph_validation.status == PASS`.

Do not write a monolithic production builder in this pack.

## RECON_RDL0

Build only total envelope, contact datum, axes and centerline.

Validate numeric bounds and authoritative FRONT/SIDE/TOP. No detail skills.

Gate: `RDL0_BARRIER: PASS`.

## RECON_NODE_BUILD

Canonical v0.9 construction pack. Input is exactly one Shape Node plus graph revision.

Required:
- Node Contract;
- Shape Classification;
- Node-by-Node Multi-View Validation;
- Node Execution Protocol;
- only the representation skill needed by the current node;
- QA scene isolation and registered validators.

Loop:

```text
resolve ready node
-> build/repair node only
-> BUILT_UNVERIFIED
-> isolate
-> validate required views
-> numeric/section/regression checks
-> RECONSTRUCTION_NODE_GATE
-> persist ACCEPTED / FAIL
```

Representation routes:

```text
REVOLVED_PROFILE -> AXISYMMETRIC_PROFILE
MULTI_SECTION_LOFT / TRANSITION -> SECTION_LOFT_HARD_SURFACE
PANEL_LINE -> HS_PANEL_LINE
SUBD_FREEFORM -> SUBD_TOPOLOGY_CONTROL
LAYERED_ASSEMBLY -> LAYER_STACK_VALIDATE
```

Forbidden:
- unrelated sibling/future-RDL geometry;
- logo/materials while solving primary form;
- a `build_all()` that bypasses node gates.

## RECON_RDL_STAGE_GATE

Load Reconstruction Detail Levels, Stage Barrier and node acceptance records.

Preferred: `SHAPE_GRAPH.evaluate_stage_barrier()`.

```text
RDL0 PASS -> RDL1
RDL1 PASS -> RDL2
RDL2 PASS -> RDL3
RDL3 PASS -> RDL4
RDL4 PASS -> RDL5
```

No bypass for later detail.

## RECON_RDL3_DETAIL

Use only on ACCEPTED structural hosts. Load only applicable leaf skills: panel lines, recesses, radial repeats, layered display, curves/sweeps, fasteners.

Host failure routes backward.

## RECON_RDL4_EDGE

Load Edge Language, bevel/radius, Surface Continuity and SubD only after structural form acceptance. Revalidate protected dimensions/silhouette after changes.

## SURFACE_FINISH / RDL5

Load material/branding/decal/emissive modules only after structural barriers. Material cannot compensate geometry error.

## RECON_FINAL_FIDELITY

Requires accepted Shape Graph revision, required node records, RDL barriers, QA isolation, registered canonical views, hard dimensions/landmarks, MUST features, authority closure and `RECON_FIDELITY_GATE`.

Only PASS opens runtime.

## GAME_READY_FINISH

Precondition: `RECON_FIDELITY_GATE == PASS`.

Preferred skills:
- `MESH_VALIDATE`;
- `UV_ATLAS_CONTRACT`;
- `BAKE_RUNTIME_TEXTURES`;
- `BAKE_VALIDATE`;
- `IMAGE_CACHE_COHERENCE`;
- `PIPELINE_DAG_PLAN`;
- `RUNTIME_PATH_RESOLVE`;
- `RUNTIME_PACKAGE_VALIDATE`;
- `EXPORT_ROUNDTRIP_VALIDATE`;
- `ASSET_COMPLETION`.

Order:

```text
runtime path
-> LOD/collision
-> UV contract
-> DAG dirty plan
-> bake/validate/cache
-> runtime material
-> package/readback
-> round-trip
-> runtime QA
-> completion
```

Runtime LOD is downstream from RDL and is not a reconstruction state.

## PIPELINE_INTEGRATION

Only for Level D. Load Project Profile, runtime path/package, catalog integration, Engine Smoke Test and Test Oracle.

Blender round-trip is Level C evidence. Target engine loader/instantiation is Level D evidence.

## Persistent state

Persist compact records:
- Tool Registry / Project Profile;
- Reference Registry / Evidence Ledger / Authority;
- Dimension Graph / Feature Contract;
- Shape Graph + revision;
- Node Contracts / Node Acceptance Records;
- RDL Stage Barrier Records;
- material/UV/bake/package state;
- Completion Report.

Do not rely on conversation history as execution state.

## Pack expansion

Load a module only when current state/RDL requires it, current Shape Node maps to it, or measured failure routes to it.

## Retry

After first proven failure: diagnose and one corrected retry. After second: re-inspect and strategy/representation switch.

## Final rule

```text
understand -> Shape Graph -> coarse form -> prove node -> deepen detail
```

not:

```text
one big script -> build everything -> inspect at the end
```


---

## FILE: `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md`

# Asset Completion Levels and Stop Conditions

## Purpose

Agent nie używa `DONE` bez jawnego poziomu i dowodu.

Lifecycle:

```text
A RECONSTRUCTION_COMPLETE
-> B MODELING_COMPLETE
-> C GAME_READY_COMPLETE
-> D PIPELINE_INTEGRATED
```

Wyższy poziom wymaga wszystkich niższych.

---

# Level A — RECONSTRUCTION_COMPLETE

Reference-driven object jest geometrycznie i wizualnie rozwiązany **oraz udowodniony**.

Required v0.9:
- Reference/Evidence Registry i authority są spójne;
- aktualny `Reconstruction Shape Graph` structural PASS;
- required G0–G3 nodes mają shape class, parent/dependencies, authoritative views i Node Contracts;
- RDL0 barrier PASS;
- required G1 primary nodes `ACCEPTED` + RDL1 barrier PASS;
- required G2 nodes `ACCEPTED` + RDL2 barrier PASS;
- required G3 nodes `ACCEPTED` + RDL3 barrier PASS;
- required RDL4 edge-language work PASS zgodnie z target fidelity;
- hard dimensions PASS z numeric provenance;
- canonical silhouettes/views PASS przez registered evidence, jeśli reference ma authority;
- primary proportions/landmarks PASS;
- MUST features mają owner + visibility/ROI/numeric proof;
- branding/orientation poprawne lub jawnie deferred do późniejszej powierzchni;
- rear/bottom/hidden evidence obsłużone wg authority;
- HARD/MUST/CANONICAL deviations są `RESOLVED` albo `ACCEPTED_BY_AUTHORITY` z recordem;
- multi-view regression PASS;
- `RECON_FIDELITY_GATE` proof-bearing PASS dla zaakceptowanego graph revision.

Nie jest wymagane:
- final runtime bake;
- runtime LOD/collision;
- engine integration.

Nie wystarcza:
- `looks correct`;
- poprawny overall bounding box;
- istniejące Blender objects;
- jeden hero render;
- successful export/engine load.

---

# Level B — MODELING_COMPLETE

Requires Level A plus:
- final intended authoring geometry;
- topology intent per mesh;
- mesh validation PASS;
- UV strategy complete;
- material segmentation complete;
- decals/branding represented by intended pipeline;
- transforms/pivot/naming PASS;
- editable authoring source saved;
- no temporary QA/helper contamination of production collection.

Procedural Blender shader może nadal istnieć.

---

# Level C — GAME_READY_COMPLETE

Requires Level B plus:
- Game Asset Contract;
- active Engine/Profile or explicit neutral runtime contract;
- runtime LOD validation against active hard/authority-resolved budget;
- collision validation;
- material/draw-call implications validated;
- procedural effects have runtime disposition: BAKE / RECREATE / NATIVE_VERIFIED / REMOVE_BY_DESIGN;
- required BaseColor/Normal/ORM/Emissive or engine-specific outputs exist;
- runtime emissive handoff documented;
- package readback validates nodes/materials/images/required primitive attributes and transform policy;
- export validation PASS;
- export round-trip protected invariants PASS;
- protected Shape Graph/Feature Contract survives optimization;
- baked/runtime-material QA PASS.

Parseable glTF bez required `TEXCOORD_0`, z niedozwolonym node TRS albo bez wymaganych runtime textures nie jest Level C.

---

# Level D — PIPELINE_INTEGRATED

Requires Level C plus:
- stable project asset ID;
- canonical runtime path;
- catalog/registry integration where required;
- no unintended overwrite;
- target engine loader/import succeeds;
- instantiation/use or equivalent engine regression succeeds;
- trustworthy test oracle;
- integration report persisted.

Accepted runtime evidence kinds:

```text
ENGINE_PRODUCTION_LOADER
ENGINE_REGRESSION_TEST
ENGINE_INSTANTIATION
```

Blender glTF re-import is Level C round-trip evidence, not Level D.

---

# User-requested stop level

Examples:
- model/reconstruction only -> A/B depending scope;
- game ready -> C;
- put into actual project catalog/runtime -> D.

For a game-production request `build the asset` defaults to Level C unless user scope clearly says otherwise.

---

# Stop conditions

Stop/report blocker when required gate cannot pass.

Examples:
- Shape Graph unresolved for primary form;
- required G1 node FAIL in SIDE/TOP;
- RDL stage barrier FAIL;
- hard authority conflict unresolved;
- missing runtime material/bake;
- collision contract unknown;
- exported package missing required attributes;
- catalog write or target-engine proof unavailable.

Do not silently downgrade target.

---

# Mandatory completion report

```yaml
asset_completion:
  target_level: GAME_READY_COMPLETE
  highest_passed_level: MODELING_COMPLETE
  levels:
    reconstruction: PASS
    modeling: PASS
    game_ready: FAIL
    pipeline_integrated: NOT_REQUIRED

  reconstruction_evidence:
    graph_revision: sg_004
    rdl_barriers: {RDL0: PASS, RDL1: PASS, RDL2: PASS, RDL3: PASS, RDL4: PASS}
    fidelity_gate: {status: PASS, evidence_kind: RECON_FIDELITY_GATE, provenance_id: recon_gate_004}

  blockers:
    - PBR_BAKE_NOT_DONE
  deliverables_present:
    blend: true
    runtime_mesh: true
    textures: false
```

Pierwszy failing required level jest realnym completion state.

---

# Anti-pattern

Nigdy nie raportuj assetu jako ukończonego, jeśli ten sam raport zawiera required blocker.

Nie raportuj Level A tylko dlatego, że monolityczny builder stworzył wszystkie elementy sceny. v0.9 wymaga coarse-to-fine Shape Node evidence.


---

## FILE: `01_analysis/10_ASSET_BRIEF_SCHEMA.md`

# Asset Brief Schema

Przed modelowaniem utwórz krótki brief.

## 1. Identity
- Asset name:
- Category:
- Function:
- Environment:
- Hero / midground / background:
- Static / animated / deformable:
- Unique / modular / instanced:

## 2. Scale
- Real/world dimensions:
- Blender units:
- Character scale reference:
- Required clearances:

## 3. Viewing conditions
- Typical camera distance:
- Closest camera distance:
- Primary view angles:
- Can player walk around it:
- Can player see back/bottom/top:

## 4. Visual language
- Dominant shapes:
- Edge language:
- Symmetry:
- Repetition:
- Material families:
- Wear level:
- Manufacturing logic:

## 5. Functional decomposition
Lista części:
- structural shell,
- insert,
- panel,
- trim,
- mechanical detail,
- interactive element,
- collision volume.

## 6. Runtime constraints
- Target triangle budget:
- LOD count:
- Texture budget:
- Material slot budget:
- Collision strategy:
- Lightmap requirement:
- Export format:

## 7. Unknowns
Każdą niewiadomą oznacz:
- `BLOCKING`
- `NON_BLOCKING`
- `CAN_INFER`

Agent może rozpocząć blockout, jeśli nie istnieje `BLOCKING`.


---

## FILE: `01_analysis/11_REFERENCE_DECOMPOSITION.md`

# Reference Decomposition

## Cel

Nie opisuj referencji słowami typu "futurystyczny panel".
Rozbij ją na informacje możliwe do odwzorowania geometrycznie.

## Warstwa A — silhouette
Zidentyfikuj:
- bounding box,
- główne załamania,
- skosy,
- wcięcia,
- wypukłości,
- otwarte przestrzenie.

## Warstwa B — proportions
Zapisz relacje:
- width : height : depth,
- wysokość detalu względem całego obiektu,
- szerokość ramek,
- grubość paneli,
- promienie i bevel widths.

Jeżeli brak skali absolutnej, relacje są ważniejsze niż zgadywane metry.

## Warstwa C — primary features
Elementy, bez których asset przestaje być tym samym projektem.

Przykłady:
- charakterystyczny łuk,
- konkretny rowek biegnący po dwóch bokach,
- asymetryczny moduł,
- otwór o określonym profilu,
- osobna metalowa osłona.

## Warstwa D — secondary features
Detale zwiększające wiarygodność, ale niewpływające mocno na identyfikację.

## Warstwa E — materials
Dla każdego obszaru:
- metal / dielectric,
- roughness family,
- transparency,
- emissive,
- normal detail,
- texture continuity.

## Warstwa F — construction logic
Zadaj sobie:
- z ilu produkcyjnych części powstałby przedmiot,
- które elementy są nakładkami,
- które są frezowane,
- gdzie istnieją szczeliny montażowe,
- czy detal powinien być geometrią, normal mapą czy teksturą.

## Widoki referencyjne

Jeżeli dostępne są różne widoki:
- nie zakładaj automatycznie zgodności,
- utwórz tabelę sprzeczności,
- wybierz referencję kanoniczną dla każdej strefy.


---

## FILE: `01_analysis/12_FEATURE_CONTRACT.md`

# Feature Contract

Feature Contract jest głównym zabezpieczeniem przed utratą detali.

## Format

| ID | Priority | Feature | Evidence | Measurement | Build method | QA method | Status |
|---|---|---|---|---|---|---|---|
| F001 | MUST | Główna sylwetka | front ref | W:H:D | blockout mesh | ortho compare | TODO |
| F002 | MUST | Rowek boczny | side ref | offset/width/depth | inset/boolean | close render | TODO |
| F003 | SHOULD | Bevel | visual | width | modifier | grazing light | TODO |

## Priority

### MUST
Bez tej cechy asset jest niepoprawny.

### SHOULD
Istotna jakość, ale brak nie zmienia tożsamości.

### OPTIONAL
Może zostać pominięta przy ograniczeniu czasu/runtime.

## Feature ownership

Każda cecha musi mieć jednoznacznego właściciela:
- konkretny obiekt,
- modifier,
- material,
- texture,
- animation,
- hierarchy entry.

Nie zapisuj cechy jako "zrobionej", jeżeli nie można wskazać, gdzie istnieje w danych sceny.

## Anti-loss rule

Przed każdą większą zmianą:
1. sprawdź listę `MUST`,
2. ustal, które obiekty/modifiery je realizują,
3. po zmianie ponownie je zweryfikuj.

## Geometry vs texture decision

Cecha powinna być geometrią, gdy:
- zmienia silhouette,
- tworzy istotny parallax,
- jest widoczna z bliska,
- wpływa na cień,
- jest interaktywna.

Może być normal/height/detail mapą, gdy:
- nie zmienia silhouette,
- jest drobna względem texel density,
- jest powtarzalna,
- koszt geometrii nie daje wartości wizualnej.


---

## FILE: `01_analysis/13_SCALE_PROPORTIONS_AND_BUDGETS.md`

# Scale, Proportions and Budgets

## Jednostki

W projekcie gry preferuj spójną skalę metryczną.

Dla assetu zapisuj:
- szerokość,
- głębokość,
- wysokość,
- wysokość funkcjonalną,
- wysokość względem postaci referencyjnej.

## Tolerancje

Domyślne wartości tylko jako punkt startowy:

- sylwetka hero prop: do ~1% odchylenia w wymiarze głównym,
- zwykły prop: do ~2–3%,
- drobny detal: oceniany wizualnie,
- element modularny łączący się z innymi: tolerancja praktycznie zerowa na krawędziach interfejsu.

Kontrakt projektu może narzucić ostrzejsze wymagania.

## Budżet trójkątów

Nie używaj jednej liczby dla wszystkich assetów.

Budżet zależy od:
- udziału assetu w ekranie,
- liczby instancji,
- deformacji,
- liczby LOD,
- częstotliwości występowania,
- kosztu materiałów i draw calls,
- platformy docelowej.

## Zasada silhouette-per-triangle

Trójkąt jest uzasadniony, gdy:
- poprawia sylwetkę,
- poprawia deformację,
- tworzy cień/parallax wymagany z dystansu,
- jest potrzebny dla poprawnego bake/shading.

Jeżeli nie spełnia żadnego z powyższych, kandydat do usunięcia.


---

## FILE: `01_analysis/14_REFERENCE_MEASUREMENT_PROTOCOL.md`

# Reference Measurement Protocol

## Cel

Zamienić obraz referencyjny na zestaw relacji liczbowych bez przenoszenia surowych danych pomiarowych do kontekstu LLM.

## Preferred execution

Jeżeli runtime pozwala na analizę obrazu przez Python/NumPy lub równoważne narzędzie, użyj kontraktu:

`08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md`

Model językowy powinien otrzymać agregaty, confidence i konflikty — nie setki wartości per-row/per-column.

## Known dimension anchor

Jeżeli znany jest co najmniej jeden wymiar:
1. wybierz wymiar dobrze widoczny w referencji,
2. wyznacz skalę piksel -> jednostka,
3. mierz tylko elementy w tej samej płaszczyźnie lub po korekcji perspektywy,
4. zapisz anchor w Reference Analysis Cache.

Jeżeli wymiar jest jawnie podany liczbowo w zatwierdzonym prompt/rysunku, traktuj go jako silniejszy dowód niż wymiar wyprowadzony z perspektywicznego hero renderu.

## Brak wymiaru absolutnego

Użyj normalized coordinates:
- width = 1.0
- height = H/W
- depth = D/W

Przechowuj relacje aż do uzyskania skali.

## Perspective warning

Nie wyprowadzaj bezpośrednich wymiarów z:
- silnego perspective,
- fisheye,
- nieznanego focal length,
- elementów leżących w różnych głębokościach.

Perspective hero może służyć do oceny formy i widoczności detali, ale nie może nadpisać jawnego wymiaru lub zgodnych ortho views.

## Multi-view

Jeżeli istnieją front/side/top:
- każdy wymiar bierz z widoku, w którym jest najmniej zniekształcony,
- wymiary wspólne mierz niezależnie,
- porównuj aggregate deviation,
- sprzeczność zapisuj jako reference conflict.

Po uzyskaniu zgodności nie utrzymuj w aktywnym kontekście pełnych profili pomiarowych.

## Measurement table

| Metric | Value | Source view | Confidence |
|---|---:|---|---|
| W | 1.80 m | front | HIGH |
| H | 0.82 m | front | HIGH |
| D | 0.55 m | side | MEDIUM |
| gap | 0.012 m | detail | LOW |

LOW confidence nie powinno sterować destrukcyjną geometrią bez checkpointu.

## Measurement output budget

Normalny pomiar zwraca tylko:
- accepted value/ratio;
- source view/ROI;
- confidence;
- aggregate variance/deviation;
- conflict/warning;
- feature/metric ID.

Nie zwracaj domyślnie:
- całych masek pikselowych;
- setek punktów profilu;
- każdej wartości wiersza/kolumny;
- wszystkich prób threshold.

Jeżeli występuje błąd, uruchom diagnostykę tylko na minimalnym ROI.

## Cache rule

Przed pomiarem sprawdź `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md`.

Jeżeli ROI, calibration anchor i wynik są już zwalidowane dla niezmienionego źródła, użyj cache.
Nie mierz ponownie całego arkusza tylko dlatego, że agent rozpoczął kolejny etap.


---

## FILE: `01_analysis/15_CAMERA_REFERENCE_MATCHING.md`

# Camera and Reference Matching

## Cel

Oddzielić błąd modelu od błędu kamery.

Agent nie może poprawiać geometrii tylko dlatego, że render z innej ogniskowej lub perspektywy nie przypomina concept artu.

## Kolejność

1. ustal typ referencji:
   - orthographic / technical view,
   - weak perspective,
   - perspective photograph,
   - stylized concept art;
2. ustal orientację obiektu;
3. dopasuj kamerę;
4. dopiero potem porównuj geometrię.

## Parametry kamery

Kontroluj jawnie:
- projection type,
- focal length / orthographic scale,
- sensor fit,
- camera position,
- camera rotation,
- lens shift,
- render aspect ratio.

## Technical reference

Dla front/side/top preferuj kamerę ortograficzną.

Wtedy:
- nie istnieje perspektywiczne zmniejszanie z głębokością,
- relacje szerokości i wysokości można porównywać stabilniej,
- camera distance nie powinna służyć jako "zoom"; używaj ortho scale.

## Perspective reference

Nie dopasowuj modelu przez lokalne deformacje, dopóki nie sprawdzisz:
- focal length,
- camera distance,
- horizon,
- vanishing lines.

## Camera lock

Po zatwierdzeniu kamery referencyjnej:
- nazwij ją,
- oznacz jako QA camera,
- nie zmieniaj jej podczas napraw geometrii.

Przykład:
`CAM_QA_Bench_Front`
`CAM_QA_Bench_Side`
`CAM_QA_Bench_34`

## Acceptance

Render z kamery QA powinien być deterministyczny:
- ten sam resolution,
- ten sam aspect,
- ten sam transform,
- ten sam render engine/profile.


---

## FILE: `01_analysis/16_VISUAL_FEATURE_MAP.md`

# Visual Feature Map

## Cel

Połączyć pikselowy obszar referencji z konkretną cechą modelu.

Feature Contract mówi *co* istnieje.
Visual Feature Map mówi *gdzie tego szukać* na renderze.

## Rekord cechy

```text
feature_id: F012
view: FRONT
roi_normalized: [x0, y0, x1, y1]
expected_edges: ...
expected_material_region: ...
occlusion_allowed: false
```

`roi_normalized` używa zakresu 0..1 niezależnie od rozdzielczości.

## Użycie

Visual Feature Map służy do:
- lokalnego image diff,
- kontroli czy feature nie zniknął,
- ograniczenia naprawy do konkretnego obszaru,
- zmniejszenia liczby błędnych wniosków wynikających ze zmian w tle.

## Nie każdy feature ma jeden ROI

Cecha może:
- występować w kilku widokach,
- być częściowo zasłonięta,
- mieć region dynamiczny.

## MUST features

Dla każdego wizualnego `MUST` preferuj:
- co najmniej jeden główny QA view,
- opcjonalnie drugi view potwierdzający głębokość.

## Zakaz

Nie używaj globalnego similarity score jako jedynego kryterium.
Model może uzyskać wysoki wynik mimo utraty małej, ale krytycznej cechy.


---

## FILE: `02_blender_api/18_API_DECISION_MATRIX.md`

# API Decision Matrix

## Cel

Wybrać najbezpieczniejszą warstwę wykonania.

| Potrzeba | Preferuj | Unikaj jako pierwszy wybór |
|---|---|---|
| odczyt obiektu | RNA / `bpy.data` | UI |
| tworzenie data-block | `bpy.data` | operator add + selection |
| proceduralna topologia | `bmesh` | setki Edit Mode ops |
| zmiana transform | object properties | translate operator |
| modifier params | modifier properties | UI |
| import/export | właściwy operator/export API | ręczne UI |
| render kontrolny | render API/tool | screenshot przypadkowego viewportu |
| masowa zmiana | jeden batch Python | wiele małych tool calls |
| pojedynczy interaktywny tool | operator z kontrolowanym context | emulacja kliknięć bez inspekcji |

## Decision questions

Przed operacją:
1. Czy jest read-only?
2. Czy trzeba zmieniać topologię?
3. Czy istnieje Data API?
4. Czy operator jest context-sensitive?
5. Czy rezultat wymaga renderu do oceny?
6. Czy operację można wykonać jako jeden parametryczny batch?
7. Jaki jest rollback?

## Priority

`read-only inspect -> direct data -> BMesh -> modifier -> controlled operator -> UI emulation`

To jest reguła biblioteki, nie twierdzenie, że wyższa warstwa jest zawsze technicznie możliwa.


---

## FILE: `02_blender_api/19_TOOL_DISCOVERY_AND_REGISTRY.md`

# Tool Discovery and Registry

Ten moduł dotyczy warstwy narzędzi AI/MCP/API stojącej przed `bpy`.

## Problem

Agent nie może zakładać, że:
- każde narzędzie wykonuje kod Python,
- każde narzędzie ma dostęp do UI,
- każde narzędzie zwraca render,
- każdy operator Blendera jest dostępny w tym samym kontekście,
- wywołanie jest tanie lub bez skutków ubocznych.

## Discovery przed pierwszą modyfikacją

Agent tworzy `Tool Registry`.

Dla każdego dostępnego narzędzia zapisuje:

| Field | Meaning |
|---|---|
| tool_name | dokładna nazwa |
| purpose | do czego służy |
| read/write | czy zmienia scenę |
| inputs | wymagane argumenty |
| output | co realnie zwraca |
| context | wymagania UI/scene/mode |
| side_effects | selection, mode, scene, file |
| idempotent | yes/no/conditional |
| cost | low/medium/high |
| preferred_for | najlepsze zastosowanie |
| avoid_for | zastosowania niewłaściwe |
| verification | jak sprawdzić wynik |

## Klasy narzędzi

### T1 — Read-only scene inspection
Preferowane do:
- inventory,
- object properties,
- mesh stats,
- materials,
- hierarchy.

### T2 — Python execution
Preferowane do:
- deterministycznych batchy,
- BMesh,
- tworzenia danych,
- audytu,
- parametrycznych zmian.

### T3 — UI/operator execution
Preferowane tylko, gdy:
- narzędzie jest rzeczywiście interaktywne,
- Python/Data API nie daje rozsądnej alternatywy.

### T4 — Render/screenshot
Preferowane do:
- visual QA,
- porównań,
- checkpointów.

### T5 — File/save/export
Preferowane do:
- checkpointów,
- finalnych artefaktów,
- testów eksportu.

## Routing rule

Wybieraj narzędzie o:
1. najwęższym zakresie wystarczającym do zadania,
2. najmniejszej liczbie skutków ubocznych,
3. najwyższej deterministyczności,
4. najniższym koszcie przy tej samej jakości.

## Zakaz tool guessing

Jeżeli agent nie zna dokładnego zachowania narzędzia:
- nie uruchamia go na głównym assetcie,
- odczytuje schema/help, jeśli dostępne,
- albo wykonuje minimalny test na obiekcie tymczasowym.

## Tool Registry persistence

Registry powinien być przechowywany dla danej sesji/wersji integracji.
Nie rediscoveruj tych samych możliwości przed każdym krokiem.


---

## FILE: `02_blender_api/20_BLENDER_5_1_API_STRATEGY.md`

# Blender 5.1 API Strategy

## Version lock

Ten corpus jest pisany dla Blender 5.1.x.
Przy zmianie wersji:
- sprawdź release notes Python API;
- sprawdź zmiany operatorów i Geometry Nodes;
- nie zakładaj kompatybilności skryptów bez testu.

Dla realnego runtime zawsze dodatkowo stosuj `02_blender_api/29_BLENDER_5_1_COMPATIBILITY_MATRIX.md`.
Target version nie zwalnia z capability discovery.

## Runtime compatibility preflight

Przed version-sensitive code zbierz raz na sesję:
- `bpy.app.version`;
- dostępne render-engine enums;
- obecność wymaganych RNA properties;
- glTF/export capability;
- status zapisania `.blend`;
- stabilne źródło project root.

Preferuj semantic skill `RUNTIME_COMPAT` / `executors/runtime_compat.py` zamiast powtarzania ad-hoc discovery.

Nie zakładaj z pamięci:
- konkretnego identyfikatora EEVEE;
- legacy `use_auto_smooth`;
- że `bpy.data.filepath` jest niepuste;
- że importer/executor pliku nie uruchomi top-level side effects.

## Preferowana kolejność narzędzi

1. bezpośrednie odczyty z `bpy.data` / obiektów RNA;
2. bezpośrednie modyfikowanie właściwości obiektów i data-blocków;
3. `bmesh` dla topologii;
4. modyfikatory;
5. `bpy.ops` tylko gdy dana operacja rzeczywiście jest operatorem lub alternatywa jest nieproporcjonalnie złożona;
6. emulowanie UI jako ostateczność.

## Dlaczego

Operatory:
- zależą od context;
- często zależą od mode;
- mogą zależeć od active object / selection;
- bywają trudniejsze do uruchomienia w automatyzacji bez UI.

Data API:
- odwołuje się do jawnych obiektów;
- lepiej nadaje się do idempotentnych skryptów;
- ogranicza ukryty stan.

BMesh:
- jest przeznaczony do niskopoziomowej edycji geometrii mesh;
- pozwala łańcuchować operacje bez symulowania Edit Mode.

## Agent rule

Przed użyciem `bpy.ops.*` odpowiedz wewnętrznie:
1. Czy istnieje prosty Data API?
2. Czy istnieje `bmesh.ops`?
3. Jaki context wymaga operator?
4. Jaki mode?
5. Jaki active object?
6. Jak sprawdzę `poll()`?
7. Czy operator zmienia selection/mode?
8. Jak wrócę do stabilnego stanu?

## API action wrapper

Każdy większy skrypt powinien:
- znaleźć obiekty po nazwie/tagu, a nie przypadkowym zaznaczeniu;
- zweryfikować typ obiektu;
- zweryfikować wersję/capability, jeżeli używa version-sensitive API;
- zapisać stan krytyczny;
- wykonać zmianę;
- uruchomić postcondition check.

## Importable builder rule

Jeżeli build script ma być używany jako biblioteka przez LOD/export/repair:
- import/exec nie może automatycznie czyścić lub przebudowywać produkcyjnej kolekcji;
- entry point mutujący scenę musi być jawny;
- preferuj `if __name__ == "__main__":` dla bezpośredniego uruchomienia;
- helper configuration ma być przekazywana jawnie albo odczytywana w momencie call, nie capture'owana w mutable global default argument.


---

## FILE: `02_blender_api/21_BPY_DATA_OPS_BMESH.md`

# bpy.data vs bpy.ops vs BMesh

## `bpy.data`

Używaj do:
- wyszukiwania data-blocków,
- tworzenia mesh/material/object,
- odczytu sceny,
- zarządzania kolekcjami,
- jawnej zmiany właściwości.

Przykład:
```python
mesh = bpy.data.meshes.new("PROP_Bench_Mesh")
obj = bpy.data.objects.new("PROP_Bench", mesh)
collection.objects.link(obj)
```

## RNA / object properties

Preferowane do:
- location/rotation/scale,
- visibility,
- parent,
- modifier properties,
- material slots,
- custom properties.

## `bmesh`

Używaj do:
- tworzenia i modyfikowania topologii,
- operacji na vertices/edges/faces,
- proceduralnego modelowania mesh,
- zmian bez zależności od interaktywnego Edit Mode.

Schemat:
```python
bm = bmesh.new()
bm.from_mesh(mesh)
# bmesh.ops...
bm.to_mesh(mesh)
bm.free()
mesh.update()
```

## `bpy.ops`

Używaj, gdy:
- funkcja jest udostępniona głównie jako operator,
- potrzebujesz eksportera/importera,
- korzystasz z narzędzia, którego odtworzenie przez Data API nie ma sensu.

Nie opieraj długiego pipeline na:
```python
bpy.ops.object.select_all(...)
bpy.ops.object.mode_set(...)
bpy.ops.mesh...
```
bez jawnego zarządzania kontekstem.

## Poll

Jeżeli operator posiada wymagania kontekstowe, sprawdź:
```python
if bpy.ops.some.operator.poll():
    bpy.ops.some.operator()
```

Brak `poll()` nie oznacza, że wywołanie jest bezpieczne.


---

## FILE: `02_blender_api/22_CONTEXT_MODE_SELECTION.md`

# Context, Mode and Selection

## Ukryty stan

Najczęstsze źródła błędów automatyzacji:
- niewłaściwy mode,
- inny active object,
- inny view layer,
- obiekt wyłączony z widoku,
- błędna selection,
- brak odpowiedniego area/region dla operatora.

## Stabilny baseline

Przed operacją wymagającą Object Mode:
1. ustal aktywny view layer,
2. znajdź obiekt jawnie,
3. jeżeli potrzeba — przejdź do Object Mode,
4. ustaw active object,
5. ustaw selection tylko dla wymaganych obiektów,
6. wykonaj operator,
7. nie zakładaj, że selection pozostało bez zmian.

## `temp_override`

Jeżeli operator wymaga konkretnego kontekstu, używaj jawnego override zamiast przypadkowej zależności od aktualnego UI.

Schemat:
```python
with bpy.context.temp_override(
    active_object=obj,
    object=obj,
    selected_objects=[obj],
    selected_editable_objects=[obj],
):
    if bpy.ops.object.some_operator.poll():
        bpy.ops.object.some_operator()
```

Dokładne pola override zależą od operatora.

## Mode rule

Nie przełączaj wielokrotnie:
`OBJECT -> EDIT -> OBJECT -> EDIT`
dla serii prostych zmian topologii.

Jeżeli pipeline jest proceduralny, rozważ jedną sesję BMesh.

## Selection rule

Selection jest interfejsem użytkownika, nie identyfikatorem logiki biznesowej skryptu.
Logika powinna trzymać referencje do obiektów.


---

## FILE: `02_blender_api/23_SCENE_INSPECTION.md`

# Scene Inspection

## Zanim cokolwiek zmienisz

Zbierz Scene Snapshot.

## Snapshot minimalny

- Blender version,
- active scene,
- unit system,
- object count,
- collections,
- mesh count,
- object names/types,
- active object,
- selected objects,
- mode,
- world scale,
- cameras,
- lights,
- existing asset roots,
- external file references.

## Dla assetu

Zbierz:
- dimensions,
- location,
- rotation,
- scale,
- parent,
- modifiers,
- mesh vertex/edge/polygon counts,
- UV layers,
- material slots,
- shape keys,
- armature,
- custom properties.

## Dla istniejącego modelu przed poprawką

Wygeneruj:
- front ortho,
- side ortho,
- top ortho,
- perspective 3/4,
- opcjonalnie rear/bottom,
- wireframe lub matcap,
- bounding dimensions.

Bez tego agent może "naprawiać" problem, którego nie ma, albo niszczyć inną część modelu.

## Snapshot jako tekst

Wynik audytu powinien być krótki i strukturalny.
Nie wypisuj tysięcy vertices.


---

## FILE: `02_blender_api/24_IDEMPOTENCY_TRANSACTIONS_RECOVERY.md`

# Idempotency, Transactions and Recovery

## Idempotency

Uruchomienie tego samego kroku drugi raz nie powinno:
- tworzyć kolejnego `.001`,
- podwajać modifiera,
- dodawać drugiego materiału,
- ponownie przesuwać obiektu,
- mnożyć helper objects.

## Pattern: get-or-create

```python
obj = bpy.data.objects.get(name)
if obj is None:
    obj = create_object(name)
```

## Tagowanie

Dodawaj custom properties:
```python
obj["ai_asset_id"] = "bench_A"
obj["ai_stage"] = "blockout"
obj["ai_feature_ids"] = "F001,F002"
```

Umożliwia to znalezienie obiektu bez polegania na nazwie.

## Transaction boundary

Przed ryzykownym etapem:
- zapisz plik,
- lub utwórz backup kolekcji/obiektu,
- lub duplikuj źródłową siatkę jako hidden recovery copy.

## Małe transakcje

Lepsze:
1. wykonaj rowek,
2. sprawdź,
3. wykonaj bevel,
4. sprawdź.

Gorsze:
1. boolean,
2. bevel,
3. join,
4. apply,
5. triangulate,
6. delete helpers,
7. dopiero render.

## Recovery

Naprawa powinna cofać się do ostatniego poprawnego checkpointu, a nie wykonywać kolejne nakładki maskujące problem.


---

## FILE: `02_blender_api/25_TOOL_CALL_AND_TOKEN_EFFICIENCY.md`

# Tool Call and Token Efficiency

## Cel

Minimalizuj:
- liczbę wywołań API,
- powtarzane inspekcje,
- duże logi,
- iteracyjne mikroruchy,
- generowanie kodu dla operacji, które można wykonać parametrycznie,
- przesyłanie do LLM danych, które mogą zostać zagregowane lokalnie,
- echo pełnych skryptów i patchy, które już istnieją jako pliki.

Efektywność nie oznacza pomijania walidacji. Oznacza wykonywanie obliczeń tam, gdzie są najtańsze, i zwracanie modelowi tylko informacji potrzebnej do decyzji.

## Zasada batch

Jedno wywołanie powinno wykonywać logicznie spójny etap:
- stworzenie blockoutu,
- dodanie zestawu głównych modifierów,
- audit,
- generacja renderów kontrolnych.

Nie łącz w jednym batchu etapów o różnym ryzyku.

## Zasada inspect-before-act

Nie próbuj kolejnych losowych operatorów.
Najpierw odczytaj:
- mode,
- active object,
- modifier stack,
- mesh stats,
- dimensions.

## Zasada parameterize

Zamiast 20 poleceń:
`move vertex A, move vertex B...`

Utwórz parametry:
```python
WIDTH = 1.8
DEPTH = 0.55
HEIGHT = 0.82
FRAME = 0.04
BEVEL = 0.006
```

Buduj z nich geometrię.

## Zasada local patch

Przy błędzie napraw tylko:
- feature,
- obiekt,
- modifier,
- region.

Nie przebudowuj całego assetu, jeżeli problem jest lokalny.

# Tool Output Budget

## Core rule

```text
compute locally -> aggregate -> return decision-grade summary
```

Tool output is part of the context budget. A tool must not return a raw dataset merely because it can.

Default tool response should normally fit in a compact structured summary. Large diagnostic output requires a specific failing ROI/object/feature and explicit justification.

## Never return by default

Do not send to the language model:
- full pixel arrays or image buffers;
- one measurement per image row/column when aggregate statistics are sufficient;
- full vertex/edge/face coordinate dumps;
- complete RNA/property trees;
- complete scene inventories when a filtered subset answers the question;
- hundreds of unchanged samples;
- all threshold candidates from image analysis;
- repeated tool output that has not changed;
- entire source/build scripts when only a naming/path/material convention is needed;
- complete generated build/QA scripts after they have already been written to disk;
- complete source files after a small patch;
- large patches with unrelated context.

## Generated code guard

Generated code is governed by `05_execution/62_CODE_ARTIFACT_AND_PATCH_PROTOCOL.md`.

Default behavior for a non-trivial script is:

```text
write file -> report path + changed symbols -> execute -> compact validation
```

Do not use conversation/tool output as transport for unchanged source code.
If a 600-line build file already exists, a 10-line fix should not cause 600 lines to re-enter model context.

## Preferred compact diagnostics

Return:
- operation/status;
- affected IDs/objects;
- key before/after metrics;
- aggregate error/deviation;
- confidence;
- failing ROI/feature if any;
- warnings/error code;
- next diagnostic target.

Example:

```yaml
status: PASS
view: FRONT
body_width_px: 70
body_width_variance_px: 1.1
front_side_difference_pct: 2.9
transitions:
  top_module_y_px: [207, 220]
  base_y_px: [604, 634]
anomalies: []
```

Instead of returning 400+ per-row width records.

## Progressive disclosure

Use three output levels:

### `SUMMARY`
Default. Decision-grade aggregates only.

### `DIAGNOSTIC`
Use after a failure. Return data only for the failing object/feature/ROI.

### `RAW`
Exceptional. Use only when the next decision genuinely cannot be made from summarized diagnostics.

Escalation must be:

```text
SUMMARY -> failure/ambiguity -> DIAGNOSTIC -> only if still necessary -> RAW
```

Never start with RAW.

## Local computation rule

Python, NumPy, BMesh and geometry evaluators should perform reduction internally.

Examples:
- compute min/max/mean/variance locally;
- compare two silhouette profiles locally and return deviation;
- count non-manifold elements locally;
- reduce a mesh audit to failing element IDs/regions;
- compare render masks locally and return mismatch score + bounding ROI.

The LLM should reason over results, not over thousands of elementary samples.

## Result size guard

If a generated diagnostic contains more than roughly 100 scalar/sample entries, stop and ask:

```text
Can this be reduced to aggregates, outliers and failing regions?
```

In nearly all routine Blender-agent operations the answer should be yes.

## Repeated-source guard

Before analyzing an image, script, repository file or scene region again:
- check whether a validated cache/registry already contains the required fact;
- reuse it if valid;
- re-read only the smallest missing range/ROI.

For reconstruction use `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md`.
For project conventions use `09_engine/92_PROJECT_ASSET_PIPELINE_PROFILE_SCHEMA.md`.
For generated source use `05_execution/62_CODE_ARTIFACT_AND_PATCH_PROTOCOL.md`.

## Zasada no visual guessing loop

Jeżeli agent po renderze "przesuwa trochę" obiekt pięć razy, workflow jest błędny.
Najpierw zmierz błąd, potem wykonaj jedną korektę.

## Limit eksperymentów

Dla nieznanej operacji:
1. wykonaj na kopii/test mesh,
2. oceń wynik,
3. dopiero zastosuj do assetu.

Nie eksperymentuj na głównym modelu.

## Completion requirement

Every analysis/execution stage should end with a compact persistent summary. Once a fact has been accepted into persistent state, do not keep its full discovery trace in active reasoning unless a conflict requires it.


---

## FILE: `02_blender_api/26_ERROR_HANDLING.md`

# Error Handling

## Nie łap wyjątków bez reakcji

Błędny wzorzec:
```python
try:
    ...
except:
    pass
```

## Minimalny log błędu

- stage,
- operation,
- asset id,
- object names,
- context mode,
- exception type,
- message.

## Fail fast

Jeżeli postcondition nie jest spełniony:
- nie kontynuuj kolejnych etapów,
- oznacz phase jako FAIL,
- pozostaw scenę w możliwie stabilnym stanie.

## Validation errors vs runtime exceptions

Rozróżniaj:
- Python exception,
- Blender operator poll failure,
- invalid scene state,
- visual QA failure,
- runtime contract failure.

Każdy wymaga innej naprawy.

## Cleanup

Jeżeli batch tworzy tymczasowe cuttery/helpers:
- oznacz je,
- usuń tylko te utworzone przez batch,
- nie usuwaj obiektów "po nazwie podobnej", jeśli identyfikacja nie jest pewna.


---

## FILE: `02_blender_api/27_PERFORMANCE_FOR_AUTOMATION.md`

# Performance for Blender Automation

## Avoid repeated depsgraph churn

Zamiast wielu mikrozmian i wymuszania update po każdej:
- wykonaj logiczny batch,
- zaktualizuj i zweryfikuj na końcu batchu.

## Avoid UI-driven loops

Nie:
- klikaj,
- zaznaczaj,
- przełączaj mode,
- wywołuj operator,
setki razy, jeśli można zbudować mesh bezpośrednio.

## Avoid excessive object count

Osobne obiekty są użyteczne logicznie, ale tysiące mikro-obiektów:
- komplikują scene graph,
- zwiększają koszty authoringu,
- utrudniają selection i export.

Łącz elementy, gdy mają:
- tę samą funkcję runtime,
- ten sam materiał,
- brak niezależnej animacji,
- brak potrzeby wariantowania.

## Heavy modifiers

Przy dużej liczbie instancji authoringowych:
- kontroluj subdivision,
- boolean stack,
- high-segment bevel.

Wyłącz kosztowne elementy w viewport, jeśli pipeline tego wymaga, ale waliduj render/final state.


---

## FILE: `02_blender_api/28_AGENT_TOOL_API_PROFILE.md`

# Agent Tool API Profile

## Purpose

This file defines the capability contract an autonomous Blender agent must satisfy before it is allowed to mutate a production scene.

It separates:

```text
semantic skill
-> required capability
-> concrete connected tool
-> Blender API / BMesh execution
-> verification
```

The agent must never invent connector/tool names. It discovers and binds the tools available in the current runtime.

## Profile ID

```text
BLENDER_AGENT_TOOL_PROFILE_V1
```

## Required capabilities

### C1 — `scene_inspect`
Read-only access to the current Blender state.

Must support enough information to determine:
- Blender version;
- active scene;
- object inventory;
- object type/name/transform/dimensions;
- active object and mode;
- collections/hierarchy;
- mesh statistics where practical;
- materials/modifiers where practical.

Risk class: `READ_ONLY`.

### C2 — `python_execute`
Execute controlled Python in Blender with access to `bpy`; BMesh is required for skills that declare it.

Must support:
- deterministic script execution;
- exception reporting;
- access to `bpy.data` and scene data;
- explicit context inspection;
- return of compact structured diagnostics.

Risk class: `SCENE_WRITE`.

### C3 — `visual_capture`
Produce a render, viewport screenshot, or equivalent image used for QA.

Must permit stable camera/view selection or a scripted alternative.

Risk class: `READ_ONLY_OR_RENDER_SIDE_EFFECT`.

### C4 — `save_checkpoint`
Save a recoverable Blender source checkpoint or equivalent scene state.

Risk class: `FILE_WRITE`.

### C5 — `export_asset`
Export the requested runtime artifact when the current task reaches EXPORT.

Risk class: `FILE_WRITE`.

### C6 — `file_verify`
Verify that an exported file exists and, where the integration permits it, inspect enough metadata/content to confirm export success.

Risk class: `READ_ONLY`.

## Optional capabilities

### O1 — `ui_operator`
Mouse/keyboard/UI/operator automation.

This is never preferred over `python_execute` for deterministic mesh work. Use only when the required operation is unavailable or materially less reliable through data/BMesh APIs.

### O2 — `reference_image_access`
Direct access to reference images/files for reconstruction and QA.

### O3 — `external_diff`
Image-diff or mesh-diff capability outside Blender.

## Runtime binding record

At the beginning of a session, bind actual connected tools to semantic capabilities:

```yaml
agent_tool_profile:
  profile_id: BLENDER_AGENT_TOOL_PROFILE_V1
  blender_version: "5.1.x"
  bindings:
    scene_inspect:
      tool: ACTUAL_DISCOVERED_TOOL_NAME
      verified: true
    python_execute:
      tool: ACTUAL_DISCOVERED_TOOL_NAME
      verified: true
      bpy: true
      bmesh: true
    visual_capture:
      tool: ACTUAL_DISCOVERED_TOOL_NAME
      verified: true
    save_checkpoint:
      tool: ACTUAL_DISCOVERED_TOOL_NAME
      verified: true
    export_asset:
      tool: ACTUAL_DISCOVERED_TOOL_NAME
      verified: true
    file_verify:
      tool: ACTUAL_DISCOVERED_TOOL_NAME
      verified: true
```

Never fill `ACTUAL_DISCOVERED_TOOL_NAME` from memory or assumption.

## Capability states

Each capability is one of:

```text
UNKNOWN
DISCOVERED
TESTED
BOUND
FAILED
UNAVAILABLE
```

Mutation requires:

```text
scene_inspect = BOUND
python_execute = BOUND
```

Reference reconstruction that depends on image comparison additionally requires:

```text
visual_capture = BOUND
```

Export completion additionally requires:

```text
export_asset = BOUND
file_verify = BOUND
```

If a required capability is missing, the agent must return a capability blocker instead of improvising a different execution path silently.

## Preflight sequence

Before the first production mutation:

```text
1. discover tool schemas/capabilities
2. create Tool Registry
3. bind semantic capabilities
4. perform read-only scene inspection
5. verify Blender version and mode
6. run a minimal non-production capability test where needed
7. save profile state for the session
8. only then enter scene mutation
```

Do not rediscover unchanged capabilities before every operation.

## Minimal Python execution test

A safe initial test should be read-only where possible:

```python
import bpy
import bmesh

result = {
    "blender_version": bpy.app.version_string,
    "scene": bpy.context.scene.name if bpy.context.scene else None,
    "active_object": bpy.context.active_object.name if bpy.context.active_object else None,
    "mode": bpy.context.mode,
    "bmesh_available": bmesh is not None,
}
```

This does not prove every modeling operation works, but verifies the critical Python/BMesh foundation.

## Tool-selection hierarchy

For equivalent outcomes prefer:

```text
1. read-only scene inspection
2. direct bpy.data / RNA
3. BMesh
4. non-destructive modifier configuration
5. controlled bpy.ops with explicit context
6. UI emulation
```

This ordering can be overridden only when a narrower method is demonstrably less reliable for the specific operation.

## Operation binding example

For `HS_PANEL_LINE`:

```yaml
operation_binding:
  skill_id: HS_PANEL_LINE
  requires:
    - scene_inspect
    - python_execute
  preferred_execution:
    - bpy_data
    - bmesh
    - modifiers
  verification:
    - evaluated_geometry
    - topology_report
    - optional_visual_capture
```

For `SUBD_TOPOLOGY_CONTROL`:

```yaml
operation_binding:
  skill_id: SUBD_TOPOLOGY_CONTROL
  requires:
    - scene_inspect
    - python_execute
  verification:
    - control_cage_metrics
    - evaluated_subdivision_metrics
    - optional_visual_capture
```

For `RECONSTRUCT_REFERENCE`:

```yaml
operation_binding:
  skill_id: RECONSTRUCT_REFERENCE
  requires:
    - scene_inspect
    - python_execute
    - visual_capture
  optional:
    - reference_image_access
    - external_diff
```

## Context-sensitive operators

If `bpy.ops` is required, the execution adapter must explicitly control:
- active object;
- selection;
- object/edit mode;
- scene/view layer;
- area/region context if applicable;
- operator poll result where applicable.

Prefer `bpy.context.temp_override(...)` when an override is required.

A failed operator must not be retried with the same unknown context repeatedly.

## Session persistence

The Tool Registry and this runtime binding should be cached for the current integration/version/session.

Invalidate the binding when:
- Blender version changes;
- connector schema changes;
- required capability starts failing;
- a tool returns output inconsistent with its recorded contract;
- a new session does not guarantee preserved connection state.

## Completion status

The agent reports one of:

```text
PROFILE_BOUND
PROFILE_PARTIAL
PROFILE_BLOCKED
```

`PROFILE_PARTIAL` may permit analysis/planning but not all mutations/export stages.

## Fundamental rule

Knowledge does not imply capability.

A skill may explain exactly how to build a feature, but the agent must still prove that the current connected runtime exposes the tools required to execute and verify that feature.


---

## FILE: `02_blender_api/29_BLENDER_5_1_COMPATIBILITY_MATRIX.md`

# Blender 5.1 Runtime Compatibility Matrix

## Purpose

The library targets Blender 5.1.x, but agents must still **discover actual runtime capabilities** instead of assuming an enum/property/operator name from memory.

This module records compatibility lessons observed in real agent execution and converts them into guarded patterns.

Each item is tagged:
- `OBSERVED_RUNTIME` — encountered during a Blender 5.1 project run;
- `GENERAL_GUARD` — safe automation rule independent of a specific build;
- `FUTURE_DEPRECATION` — current API worked but runtime emitted a deprecation warning.

---

## Render engine enum

### Observed
`OBSERVED_RUNTIME`

A run that assumed:

```python
scene.render.engine = "BLENDER_EEVEE_NEXT"
```

failed because that enum was not exposed by the connected Blender 5.1 build.

### Rule

Never hardcode one expected EEVEE identifier without discovery.

```python
engines = scene.render.bl_rna.properties["engine"].enum_items.keys()
for wanted in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
    if wanted in engines:
        scene.render.engine = wanted
        break
```

The actual selected engine must be included in QA metadata.

---

## Auto Smooth assumptions

### Observed
`OBSERVED_RUNTIME`

Legacy scripts that expect a `use_auto_smooth` mesh flag are not a safe compatibility strategy for the target runtime.

### Rule

Do not use the existence of `use_auto_smooth` as a required precondition.

Prefer explicit shading intent:
- polygon smooth state;
- sharp-edge marking where required;
- normal/shading workflow appropriate to the target mesh;
- runtime feature discovery when an API property is version-sensitive.

If a script depends on a version-sensitive property, wrap it in `hasattr()` and provide a fallback.

---

## Material node activation

### Observed
`FUTURE_DEPRECATION`

The target runtime accepted `Material.use_nodes`, but emitted a warning that the property is expected to be removed in Blender 6.0.

### Rule

Do not scatter direct `mat.use_nodes = True` assumptions throughout generated asset scripts.

Centralize material-node initialization in a compatibility helper.

Preferred behavior:
1. inspect whether a usable node tree already exists;
2. use the target-version mechanism only when required;
3. keep future-version compatibility isolated to one helper;
4. record deprecation warnings but do not treat a future warning as a current execution failure.

---

## Unsaved `.blend` path

### Observed
`OBSERVED_RUNTIME`

In a fresh unsaved Blender session:

```python
bpy.data.filepath == ""
```

A generated decal script derived the project root from that empty value and wrote output to an unintended `C:\GameAssets` location.

### Rule

Never use `bpy.data.filepath` as the sole project-root anchor.

Path precedence:

```text
active Project Asset Pipeline Profile
> explicit task/project root
> script __file__ anchor
> saved blend path
> cwd only as last controlled fallback
```

Before writing files outside the temporary QA directory, validate that the resolved root contains an expected project marker.

---

## Viewport visibility vs render visibility

### Observed
`OBSERVED_RUNTIME`

A default Cube was hidden in the viewport but still rendered and completely obscured a QA render.

### Rule

`hide_viewport` and `hide_render` are separate states.

QA isolation must:
- preserve original render visibility;
- hide non-QA/non-asset scene objects only for the render transaction;
- restore every saved state in `finally`;
- never delete unrelated user objects to clean a QA frame.

Use the reusable QA isolation helper when available.

---

## Importing/executing builder scripts

### Observed
`OBSERVED_RUNTIME`

A LOD/export script executed the build script only to access helper functions, but the build file contained an unconditional top-level:

```python
BUILD_REPORT = build()
```

This cleared the asset collection and deleted freshly created decal plates.

### Rule

Reusable build modules must not mutate the production scene on import.

Use:

```python
if __name__ == "__main__":
    BUILD_REPORT = build()
```

or expose an explicit callable entry point.

Import/namespace loading must be side-effect free unless the semantic executor contract explicitly says otherwise.

---

## Function default capture

### Observed
`OBSERVED_RUNTIME`

A parametric LOD generator changed a global segment count, but a function defined as:

```python
def lathe(..., segs=SEG):
```

had already captured the old value at definition time.

### Rule

Runtime-configurable defaults must not be captured from mutable global configuration.

Use:

```python
def lathe(..., segs=None):
    if segs is None:
        segs = CURRENT_CONFIG.segments
```

or pass the value explicitly.

---

# Capability preflight

Before generated code uses a version-sensitive API, inspect and persist:

```yaml
blender_compat:
  version: [5, 1, x]
  render_engines: []
  material_node_api: DISCOVERED
  shading_api: DISCOVERED
  export_gltf_available: true
  blend_saved: false
  project_root_source: PROJECT_PROFILE
```

Do this once per session unless the runtime changes.

---

# Rule for future versions

This is not a promise that Blender 5.2/6.x behaves identically.

When the runtime version differs from the library target:
- mark compatibility `UNVERIFIED`;
- discover relevant RNA/enums;
- test on a temporary object/scene;
- record the new compatibility fact before production mutation.


---

## FILE: `02_blender_api/30_IMAGE_DATABLOCK_CACHE_COHERENCE.md`

# Blender Image Datablock Cache Coherence

## Purpose

An external texture file changing on disk does **not** imply that an existing `bpy.data.images` datablock now contains the new pixels.

This is a silent failure class: filename, filepath, node binding and material graph can all look correct while Blender renders an older in-memory version.

## Core rule

```text
DISK ARTIFACT FRESHNESS != BLENDER IMAGE DATABLOCK FRESHNESS
```

When the pipeline declares the saved texture file authoritative, runtime material assembly must explicitly synchronize the Blender image datablock before QA.

## Authority states

Every image artifact should declare one state:

```text
GENERATED_IN_MEMORY_AUTHORITATIVE
DISK_FILE_AUTHORITATIVE
PACKED_BLEND_AUTHORITATIVE
UNRESOLVED
```

Do not call `reload()` blindly on an image that has unsaved authoritative in-memory edits.

## Disk-authoritative reload

For a baked texture that has already been saved externally:

```python
img = bpy.data.images.get(expected_name)
if img is None:
    img = bpy.data.images.load(path)
else:
    img.filepath = path
    img.reload()
```

Then verify:
- resolved absolute filepath points to the expected artifact;
- image dimensions are non-zero and expected;
- colorspace matches the channel contract;
- compact pixel/image statistics match the accepted bake artifact.

Prefer matching by canonical filepath/artifact ID rather than basename alone when duplicate filenames can exist.

## Runtime-material binding gate

Before a baked-runtime render:

```text
accepted disk bake
-> synchronize image datablock
-> verify material node binding
-> verify UV contract
-> render runtime material
```

Do not jump from `file exists` directly to runtime QA.

## Diagnostic order when disk maps look correct but runtime render is wrong

Use this order to avoid expensive false leads:

```text
1. disk artifact validator
2. in-memory image freshness / filepath
3. material node -> image binding
4. colorspace/channel wiring
5. UV contract on consuming mesh
6. shader/runtime interpretation
```

If disk validation passes but in-memory statistics differ, classify:

```text
STALE_IMAGE_DATABLOCK
```

Do not rebuild UVs or rebake channels until cache coherence is resolved.

## Freshness evidence

Useful compact evidence:
- canonical path;
- file modification time or content hash;
- Blender image filepath;
- dimensions;
- image/source type;
- small semantic statistics from `BAKE_VALIDATE`.

Avoid transporting full pixel arrays through the LLM.

## Save/reload transaction

A safe external bake transaction is:

```text
bake in memory
-> validate in-memory result
-> save external file
-> mark file authoritative
-> synchronize/reload runtime image datablock
-> validate runtime material
```

## Failure cases

Hard FAIL:
- expected disk artifact exists but Blender image points elsewhere;
- runtime material uses a stale datablock after a newer accepted bake;
- reload fails or dimensions become zero;
- colorspace differs from contract;
- multiple datablocks with ambiguous ownership cannot be resolved.

## Relation to other modules

Use with:
- `04_game_ready/51_BAKE_EXECUTION_AND_CHANNEL_SEMANTICS.md`;
- `08_scripts/93_BAKE_OUTPUT_VALIDATION_PATTERN.md`;
- `05_execution/65_INCREMENTAL_DIRTY_STAGE_CACHE.md`.

The dirty cache should distinguish texture-content dirtiness from Blender-datablock binding/freshness dirtiness. A stale datablock normally requires **reload + runtime QA**, not rebaking the texture.

---

## FILE: `03_modeling/30_MODELING_DECISION_TREE.md`

# Modeling Strategy Decision Tree

## 1. Czy asset jest głównie hard-surface?

Tak:
- box modeling,
- curves,
- booleans,
- bevel,
- solidify,
- mirror/array,
- controlled normals.

Nie:
przejdź do odpowiedniego profilu organic/deformation.

## 2. Czy kształt jest powtarzalny?

Tak:
- Array,
- instancing,
- linked data,
- Geometry Nodes, jeśli korzyść przewyższa złożoność.

## 3. Czy kształt jest symetryczny?

Tak:
- Mirror na wczesnym etapie.
Nie:
- nie wymuszaj symetrii.

## 4. Czy detal przecina bryłę?

Rozważ:
- boolean,
- inset + extrude,
- oddzielny insert mesh.

Wybór zależy od:
- wymogu edytowalności,
- shadingu,
- częstotliwości powtarzania,
- eksportu.

## 5. Czy detal jest tylko powierzchniowy?

Rozważ:
- normal map,
- decal,
- trim sheet,
- shader detail.

## 6. Czy detal wpływa na silhouette?

Jeżeli tak, geometria ma pierwszeństwo.

## 7. Czy część może być osobnym obiektem?

Preferuj osobny obiekt, jeśli:
- ma inny materiał,
- ma być animowana,
- może występować w wariantach,
- ułatwia boolean,
- ma własny pivot,
- może być instancją.

## 8. Czy Subdivision Surface jest naprawdę potrzebny?

Użyj, gdy:
- powierzchnia ma być ciągle zakrzywiona,
- kontrolna siatka daje korzyść.

Nie używaj jako automatycznego sposobu "wygładzania" wszystkiego.


---

## FILE: `03_modeling/31_HARD_SURFACE_WORKFLOW.md`

# Hard Surface Workflow

## Etap 1 — Blockout

Buduj:
- prymitywy,
- proste extrude,
- podstawowe skosy.

Bez:
- mikrodetalu,
- finalnych beveli,
- gęstej topologii.

Wynik musi zgadzać się w silhouette.

## Etap 2 — Construction split

Podziel projekt zgodnie z logiką konstrukcji:
- korpus,
- panel,
- rama,
- wkład,
- metalowa osłona,
- mocowanie,
- element interaktywny.

Nie modeluj wszystkiego jako jednej siatki tylko po to, aby mieć "jeden obiekt".

## Etap 3 — Primary details

Dodaj:
- główne rowki,
- recess,
- otwory,
- charakterystyczne skosy,
- elementy łączące.

## Etap 4 — Edge treatment

Bevel width powinien wynikać ze:
- skali obiektu,
- materiału,
- sposobu produkcji,
- dystansu kamery.

Nie ustawiaj tego samego bevel width na wszystkich assetach.

## Etap 5 — Shading

Sprawdź:
- normals,
- hard/smooth transitions,
- bevel shading,
- artefakty boolean.

## Etap 6 — Optimization

Dopiero po zaakceptowaniu formy:
- usuń niewidoczną geometrię, jeśli bezpieczne,
- ogranicz segments bevel,
- uprość ukryte elementy,
- przygotuj LOD.

## Boolean policy

Booleans są dozwolone.
Nie oceniaj topologii wyłącznie według reguły "same quady".

Dla statycznego hard-surface ważniejsze są:
- brak artefaktów,
- stabilne normals,
- brak niekontrolowanych sliver triangles,
- przewidywalny eksport,
- wystarczająca edytowalność.


---

## FILE: `03_modeling/32_MODIFIERS_NONDESTRUCTIVE.md`

# Modifiers and Non-Destructive Modeling

## Preferowany stack hard-surface

Nie jest uniwersalny, ale często:
1. Mirror / Array
2. Booleans / shape operations
3. Solidify
4. Bevel
5. normal/shading treatment

Kolejność musi być świadoma.

## Mirror

Używaj, gdy asymetria nie jest wymagana.
Sprawdź:
- origin,
- axis,
- clipping/merge,
- czy późniejsze detale powinny być mirrorowane.

## Array

Używaj dla powtarzalności.
Nie twórz ręcznie kilkudziesięciu kopii.

## Solidify

Dobre dla:
- paneli,
- osłon,
- cienkich powierzchni.

Kontroluj:
- thickness,
- offset,
- normals,
- narożniki.

## Bevel

Bevel jest częścią designu i shadingu, nie tylko kosmetyką.
Kontroluj:
- width,
- segments,
- angle/weight/vertex group,
- miter,
- overlap.

## Decimate

Nie stosuj automatycznie do gotowego hard-surface jako "optymalizacji".
Może uszkodzić:
- silhouette,
- UV,
- normals,
- kontrolowane edge flow.

## Apply policy

Nie aplikuj modifiera, dopóki:
- kolejny etap tego nie wymaga,
- eksport/bake tego nie wymaga,
- stack nie stał się niestabilny,
- trzeba przekazać finalną siatkę do narzędzia, które nie obsługuje modifiera.

Przed Apply utwórz checkpoint.


---

## FILE: `03_modeling/33_TOPOLOGY_NORMALS_SHADING.md`

# Topology, Normals and Shading

## Topologia game assetu

Nie optymalizuj pod estetykę wireframe.
Optymalizuj pod:
- silhouette,
- shading,
- deformację,
- bake,
- runtime.

## N-gons

N-gon nie jest automatycznie błędem.
Jest ryzykowny, gdy:
- triangulacja jest nieprzewidywalna,
- powierzchnia jest nieplanarna,
- będzie deformowany,
- powoduje shading artefacts.

## Long thin triangles

Unikaj, jeżeli:
- powodują artefakty,
- niepotrzebnie komplikują UV,
- powstają po agresywnych booleanach.

## Normals

Sprawdź:
- orientację face normals,
- spójność smooth/flat,
- custom normals, jeśli używane,
- zachowanie po eksporcie.

## Weighted / edited normals

Stosuj jako świadome narzędzie shadingu.
Nie używaj do maskowania złej geometrii, która nadal daje błędną sylwetkę lub bake.

## Bevel + normals

Mały bevel:
- poprawia highlight,
- daje wizualną skalę,
- często jest ważniejszy niż dodatkowy detal powierzchniowy.

## Kontrolla

Render kontrolny:
- szary neutralny materiał,
- światło pod małym kątem,
- matcap,
- wireframe overlay.

Beauty lighting może ukryć błędy.


---

## FILE: `03_modeling/34_UV_TEXEL_DENSITY_MATERIALS.md`

# UV, Texel Density and Materials

## UV goals

UV powinno:
- mieć wystarczający padding,
- nie mieć przypadkowych overlapów,
- wykorzystywać symetrię/stacking tylko świadomie,
- zachowywać kierunek materiału,
- uwzględniać lightmap, jeśli projekt jej wymaga.

## Texel density

Ustal projektową wartość bazową.
Różnicuj tylko świadomie dla:
- hero assets,
- wyjątkowo dużych obiektów,
- obiektów widzianych z bardzo bliska.

## Seams

Umieszczaj:
- w naturalnych podziałach konstrukcyjnych,
- w mniej widocznych strefach,
- zgodnie z kierunkiem materiału.

## Material count

Materiał to nie tylko wygląd, ale potencjalny koszt runtime.
Łącz materiały, jeżeli:
- mają ten sam shader model,
- mogą współdzielić atlas/trim,
- nie wymagają osobnego render state.

## PBR baseline

Dla przenośnych assetów trzymaj logiczny podział:
- base color,
- metallic,
- roughness,
- normal,
- occlusion,
- emissive, jeśli potrzebny.

## Procedural nodes

Jeżeli efekt nie jest przenoszony do formatu runtime:
- bake,
- zastąp teksturą,
- albo jawnie pozostaw jako Blender-only authoring data.

## Texture orientation

Szczotkowany metal, włókno, panele i wzory kierunkowe muszą być zgodne z konstrukcją obiektu.


---

## FILE: `03_modeling/35_MODULARITY_INSTANCING_REUSE.md`

# Modularity, Instancing and Reuse

## Modular design

Moduł musi posiadać:
- jawny wymiar interfejsu,
- pivot zgodny z siatką modułową,
- płaskie / poprawne krawędzie łączenia,
- brak mikro-szczelin po złożeniu,
- spójny materiał i texel density.

## Reuse

Jeżeli dwa elementy są identyczne:
- preferuj linked mesh data lub instancing,
- nie twórz unikalnej geometrii bez powodu.

## Geometry duplication

Duplikowanie geometrii zwiększa:
- rozmiar assetu,
- pamięć,
- koszt authoringu.

Instancing jest szczególnie ważny dla:
- lamp,
- słupków,
- śrub,
- paneli,
- segmentów architektonicznych.

## Unikalność

Rozbij instancję tylko, gdy:
- potrzebuje osobnej deformacji,
- ma trwałą zmianę geometrii,
- bake wymaga unikalnego UV,
- silnik nie wspiera potrzebnego sposobu instancjonowania.

## Modular QA

Testuj:
- moduł A + A,
- A + B,
- rogi,
- zakończenia,
- odbicie,
- wielokrotne powtórzenie.

Błąd 1 mm powtarzany 100 razy staje się błędem systemowym.


---

## FILE: `03_modeling/36_DETAIL_HIERARCHY.md`

# Detail Hierarchy

## D0 — Global silhouette
Najważniejsza warstwa.

## D1 — Primary forms
Duże podziały bryły.

## D2 — Secondary forms
Panele, wycięcia, ramy, większe łączenia.

## D3 — Tertiary geometry
Śruby, małe szczeliny, przyciski, małe fazy.

## D4 — Surface detail
Rysy, mikro-wzór, drobna faktura, normal detail.

## Reguła budowania

Nie przechodź do D(n+1), jeśli D(n) nie jest zaakceptowane.

## Reguła optymalizacji

Usuwaj w odwrotnej kolejności:
D4 -> D3 -> część D2 -> nigdy D0 bez jawnej zmiany LOD.

## Reguła oceny

Jeżeli asset wygląda źle z odległości, problem prawdopodobnie leży w D0/D1, a nie w braku śrub.


---

## FILE: `03_modeling/37_MANUFACTURING_LOGIC.md`

# Manufacturing Logic for Believable Hard-Surface Assets

## Cel

Forma powinna sugerować, jak obiekt mógł zostać wyprodukowany i złożony.

## Pytania

- Czy element jest odlewem, giętą blachą, frezowaną płytą, tworzywem, szkłem?
- Gdzie przebiega podział części?
- Jaka jest realistyczna grubość materiału?
- Czy pokrywa ma miejsce na otwarcie?
- Czy panel jest wpuszczony czy naklejony?
- Czy szczelina ma równą szerokość?
- Czy bevel odpowiada skali produkcyjnej?

## Sci-fi

"Futurystyczny" nie oznacza:
- losowych świecących linii,
- przypadkowych panel lines,
- nadmiaru greebles.

Wiarygodny futurystyczny design nadal powinien mieć:
- logikę funkcjonalną,
- czytelne materiały,
- spójne połączenia,
- konsekwentny język krawędzi.

## Agent rule

Każdy detal D2/D3 powinien mieć co najmniej jedno uzasadnienie:
- function,
- manufacturing,
- interaction,
- visual language,
- reference.

Brak uzasadnienia = nie dodawaj.


---

## FILE: `03_modeling/38_HIGH_LOW_POLY_WORKFLOW.md`

# High-Poly / Low-Poly Workflow

## Kiedy stosować

High -> Low + bake jest uzasadnione, gdy:
- detal powierzchniowy jest zbyt kosztowny jako runtime geometry,
- wymagane są miękkie przejścia lub złożone mikrofazy,
- asset będzie oglądany wystarczająco blisko,
- detal normal mapy daje realną korzyść.

Nie stosuj automatycznie do każdego prop.

## High-poly

Cel:
- wygląd,
- powierzchnia,
- edge highlights,
- szczegóły do bake.

High-poly nie musi:
- mieć runtime topology,
- mieć minimalnego polycount,
- posiadać finalnego UV low-poly.

Musi:
- odpowiadać finalnej sylwetce tam, gdzie bake jej nie zastąpi.

## Low-poly

Cel:
- zachować silhouette,
- zachować funkcjonalną geometrię,
- posiadać stabilne shading/UV,
- mieścić się w runtime contract.

## Matching

High i low powinny:
- dzielić ten sam world scale,
- nakładać się przestrzennie,
- mieć kontrolowane odległości powierzchni.

## Hard edges and UV

Rozdzielenie smoothingu i seamów powinno być planowane razem z tangent-space normal bake.

Nie zmieniaj topologii i triangulacji po finalnym bake bez ponownej walidacji.

## Bake-critical freeze

Po zatwierdzeniu low-poly do bake:
- zachowaj kopię,
- zamroź UV,
- zamroź krytyczne normals/smoothing,
- zapisz triangulation policy.

## Naming

Przykład:
- `HP_Lafar_Bench_Frame`
- `LP_Lafar_Bench_Frame`
- `CAGE_Lafar_Bench_Frame`

## Exit criteria

- silhouette low-poly zaakceptowana,
- bake nie musi kompensować złej bryły,
- projection errors mieszczą się w przyjętej jakości,
- tangent-space normal działa poprawnie w docelowym runtime.


---

## FILE: `03_modeling/39_BAKING_PIPELINE.md`

# Baking Pipeline

## Cel

Przenieść informacje z modelu źródłowego do tekstur low-poly w sposób kontrolowany i powtarzalny.

## Typowe mapy

W zależności od pipeline:
- normal,
- ambient occlusion,
- curvature/masks,
- base color,
- roughness,
- metallic,
- emissive,
- custom masks.

Nie bake'uj map bez zastosowania runtime.

## Preflight

Przed bake:
- low-poly posiada finalne lub zamrożone UV,
- high i low są poprawnie wyrównane,
- transform scale jest świadomie obsłużony,
- naming/parowanie high-low jest deterministyczne,
- image targets mają właściwą rozdzielczość,
- color space jest właściwy dla typu mapy.

## Projection

Dostępne strategie:
- ray distance/extrusion,
- explicit cage,
- per-part bake,
- exploded bake.

Preferuj cage, gdy:
- projekcja na zakrzywionych/ciasnych strefach jest nieprzewidywalna,
- są blisko leżące powierzchnie,
- potrzebna jest większa kontrola.

## Bake segmentation

Dla złożonego assetu nie wymuszaj jednego bake wszystkiego naraz.

Rozdziel elementy, gdy:
- promienie przechodzą na sąsiednią część,
- powstają projection artifacts,
- części mają różne wymagania.

## Padding / margin

Padding musi uwzględniać:
- mipmapping,
- skalowanie tekstury,
- docelową rozdzielczość.

Nie ustawiaj jednej magicznej wartości dla wszystkich atlasów.

## Verification

Po bake:
1. nałóż mapę na low-poly,
2. ukryj high-poly,
3. renderuj pod grazing light,
4. sprawdź seams,
5. sprawdź skew,
6. sprawdź gradienty na płaskich powierzchniach,
7. sprawdź wynik po eksporcie.

## Artifact classes

- projection miss,
- cage intersection,
- skew,
- hard-edge mismatch,
- UV seam mismatch,
- tangent mismatch,
- insufficient padding,
- mirrored-normal issue.

Każdy typ błędu wymaga innej naprawy.


---

## FILE: `03_modeling/40_TRIM_SHEETS.md`

# Blender Agent Skill — Game Assets Trim Sheet UV Texturing

## Purpose

This module defines how a Blender AI agent classifies game-asset surfaces, decides when trim sheets are appropriate, maps UVs to reusable trim regions deterministically, and validates a production-safe result.

It replaces the previous short trim-sheet note with a production skill while keeping this canonical path stable.

The agent must reason in terms of:

`surface strategy -> trim region -> UV orientation -> physical texture scale -> material reuse -> validation`

not in terms of manual UV Editor clicks.

---

## 1. Relationship to other canonical skills

This skill owns **reusable banded UV/material mapping**.

It does not own:
- geometric seam creation — use `blender-agent-procedural-hard-surface-panel-lines.md` or the relevant geometry skill;
- general UV/PBR policy — see `03_modeling/34_UV_TEXEL_DENSITY_MATERIALS.md`;
- decals and unique local graphics — see `03_modeling/41_DECALS_AND_FLOATING_DETAILS.md`;
- runtime material portability — see `04_game_ready/43_TEXTURE_MATERIAL_RUNTIME.md`;
- draw-call/instancing policy — see `04_game_ready/46_DRAW_CALLS_INSTANCING_AND_BATCHING.md`;
- mip/padding/compression policy — see `04_game_ready/47_TEXTURE_PACKING_AND_MIP_SAFETY.md`.

Trim sheets are therefore one part of a hybrid production strategy, not a replacement for geometry, decals, tiling materials, or unique bakes.

---

## 2. When to use trim sheets

Prefer this skill when most of the following are true:
- the asset belongs to a modular or repeated family;
- many assets share the same material language;
- the surface is a long strip, border, rail, frame, casing edge, profile, seal, vent band, panel border, or emissive band;
- detail can be reused without unique storytelling;
- reducing unique texture sets is valuable;
- the trim can preserve its intended direction and physical scale.

Typical candidates:
- wall and corridor modules;
- door/window frames;
- façade modules;
- benches, bollards, railings and kiosks;
- repeated furniture frames;
- sci-fi panel borders;
- emissive strips;
- rubber seals and painted/metallic trims.

---

## 3. When not to use trim sheets

Do not force a trim workflow when:
- the feature changes silhouette and therefore belongs in geometry;
- the surface needs a unique high-to-low bake over most of its area;
- unique wear, damage or narrative information dominates;
- the shape is strongly organic and cannot be mapped coherently to reusable bands;
- a broad homogeneous surface is better served by a tiling material;
- a small unique graphic is better served by a decal;
- the available trim catalog has no semantically compatible region.

Hero assets may still use trim sheets for structural sub-parts, but unique surfaces should not be made generic merely to satisfy reuse.

---

## 4. Surface strategy decision tree

Before creating UVs, classify each semantically coherent visible surface group:

```text
SURFACE
|
+-- repeated structural strip / frame / border
|      -> TRIM
|
+-- broad homogeneous surface
|      -> TILING
|
+-- small unique graphic / marking
|      -> DECAL
|
+-- unique hero surface / bespoke baked detail
|      -> UNIQUE_UV_OR_BAKE
|
+-- tiny depth-only repeated detail
       -> GEOMETRY / NORMAL / TRIM HYBRID
```

The agent must not default to a unique texture set before this classification.

---

## 5. Semantic trim-sheet contract

### Trim sheet

```yaml
trim_sheet:
  id: LAFAR_TRIMS_01
  material_name: MTL_LAFAR_TRIMS_01
  orientation: HORIZONTAL
  uv_space: [0.0, 0.0, 1.0, 1.0]
  texture_resolution_px: [2048, 2048]
  texture_set:
    base_color: /textures/LAFAR_TRIMS_01_basecolor.png
    normal: /textures/LAFAR_TRIMS_01_normal.png
    roughness: /textures/LAFAR_TRIMS_01_roughness.png
    metallic: /textures/LAFAR_TRIMS_01_metallic.png
```

### Trim region

```yaml
trim_region:
  id: PAINTED_METAL_EDGE_MEDIUM
  u_min: 0.0
  u_max: 1.0
  v_min: 0.68
  v_max: 0.80
  role: STRUCTURAL_EDGE
  material_family: PAINTED_METAL
  profile_class: EDGE
  width_class: MEDIUM
  direction: U
  allow_u_tiling: true
  allow_mirror: true
```

### Surface assignment

Persistent intent should use a semantic face-group identifier, attribute, or other stable region identity.

```yaml
trim_assignment:
  object: Bench_Frame
  surface_id: OUTER_FRAME
  strategy: TRIM
  trim_sheet: LAFAR_TRIMS_01
  trim_region: PAINTED_METAL_EDGE_MEDIUM
  orientation: AUTO
  texel_density_px_per_m: 512
  allow_overlap: SHARED_TRIM_ONLY
```

Raw face indices may be used as short-lived execution data, but must not be the only persistent identity because topology edits can invalidate them.

---

## 6. Standard semantic operations

The execution layer should expose operations equivalent to:

- `TRIM_ANALYZE_ASSET`
- `TRIM_CLASSIFY_SURFACES`
- `TRIM_SELECT_REGION`
- `TRIM_UNWRAP_LINEAR_STRIP`
- `TRIM_ALIGN_TO_REGION`
- `TRIM_MATCH_PHYSICAL_SCALE`
- `TRIM_APPLY_MATERIAL`
- `TRIM_VALIDATE`
- `TRIM_REPAIR`

The LLM should normally call these semantic operations instead of generating a new low-level UV implementation for every asset.

---

## 7. Face/surface grouping

A trim assignment begins with coherent surface groups.

Good groups are:
- geometrically continuous or intentionally related;
- materially coherent;
- similarly oriented;
- semantically reusable.

Example:

```text
Bench_Frame
+-- OUTER_FRAME       -> TRIM
+-- INNER_SUPPORTS    -> TRIM or TILING
+-- UNDERSIDE_HIDDEN  -> simplified TILING/TRIM
+-- SEAT_BRACKETS     -> TRIM
+-- LOGO_REGION       -> DECAL
```

Do not combine unrelated surfaces merely because they are adjacent in topology.

---

## 8. Region-selection logic

Choose a trim region by semantic compatibility, in this order:

1. material family;
2. role/function;
3. profile class;
4. width class / physical appearance;
5. directional constraints;
6. visibility importance;
7. family consistency with sibling assets.

A heavy painted structural edge must not receive a plastic decorative band merely because that region happens to fit the UV island.

For a coherent asset family, reuse the same approved region for the same semantic role whenever possible.

---

## 9. Orientation rules

For a horizontal trim sheet:
- the long/repeating axis normally spans `U`;
- band identity is controlled by the selected `V` interval.

For a vertical trim sheet, invert the logic.

When `orientation=AUTO`:
1. determine the dominant world/object-space direction of the surface group;
2. determine the trim's repeat direction;
3. choose a discrete UV rotation that preserves the material's intended direction;
4. validate the result visually.

Do not mirror directional wear, text, brushing, gradients, asymmetrical normal details or one-way patterns unless the trim region explicitly permits mirroring.

---

## 10. Physical scale and texel density

`texel_density` must always carry a unit. Prefer an explicit field such as:

`texel_density_px_per_m`

Do not store a bare value such as `512` without defining whether it means px/m, px/cm, or a project-specific class.

### Important trim-specific rule

A trim sheet is not ordinary unique UV packing.

Across the **band width**, the region often represents a specific physical trim width/profile. The agent must preserve that design relationship and must not arbitrarily rescale the island just to hit a generic texel-density number.

Along the **repeat direction**, scaling/tiling may be permitted when the trim was authored for repetition.

Therefore `TRIM_MATCH_PHYSICAL_SCALE` should consider:
- texture resolution;
- trim-region pixel width/height;
- represented real-world trim width, when defined;
- project texel-density target;
- whether U/V tiling is permitted.

Project tolerances may define warning/fail bands. Suggested percentages are heuristics, not universal standards.

---

## 11. UV mapping strategies

Use the simplest valid strategy.

### Linear strip mapping
For rails, frames, bands and near-rectangular strips.

### Aligned quad strip
For connected quad sequences that must maintain continuous spacing and orientation.

### Box-like decomposition
For rectangular frame objects where different sides map independently to the same compatible trim family.

### Hybrid mapping
A single object may legitimately use:
- trim sheet for structural borders;
- tiling material for broad surfaces;
- decals for branding;
- unique UV/bake for hero regions.

Hybrid classification is often preferable to forcing the whole object into one technique.

---

## 12. Intentional UV reuse and overlap

Trim sheets intentionally reuse the same texture regions across multiple surfaces and assets.

Therefore overlap is **not automatically an error**.

Classify overlap as:
- `INTENTIONAL_SHARED_TRIM` — allowed;
- `INTENTIONAL_MIRROR` — allowed only if region semantics permit;
- `ACCIDENTAL_CROSS_REGION` — fail;
- `ACCIDENTAL_INCOMPATIBLE_STACK` — fail.

Validation must distinguish intentional trim reuse from accidental UV collisions.

---

## 13. Tiling along the trim axis

A region may allow UVs to extend/repeat along its long axis only if:
- the texture was authored as repeatable in that direction;
- sampler/wrap behavior in the target runtime supports it;
- repetition cannot sample neighboring atlas regions incorrectly;
- padding/mips remain safe.

`allow_u_tiling` or `allow_v_tiling` must be part of the region contract when relevant.

Do not assume atlas boundaries are safe under repeat wrapping.

---

## 14. Materials and runtime cost

Trim sheets can reduce unique texture memory and improve visual consistency, but they do **not automatically guarantee fewer draw calls**.

Actual runtime cost depends on:
- material slots;
- shader/render state;
- engine batching;
- texture bindings;
- instancing strategy.

The agent should reuse the same material instance/data-block when possible and avoid duplicate material slots that point to equivalent trim materials.

A heuristic such as `1 material ideal, 2 acceptable, 3+ justify` may be useful for simple environment props, but it is not a global engine rule. The engine profile has final authority.

---

## 15. Decal and tiling fallback

Use decals for:
- logos;
- numbers;
- warnings;
- local UI labels;
- unique marks.

Use tiling materials for:
- large homogeneous walls;
- floors;
- ceilings;
- broad painted-metal panels without banded detail.

Never distort a trim region to solve a problem that belongs to another texturing strategy.

---

## 16. Hidden surfaces

Hidden/internal surfaces may receive:
- simplified tiling mapping;
- a generic low-priority trim region;
- intentionally stacked UVs;
- no high-fidelity treatment when they cannot be observed and runtime allows it.

Do not spend premium trim logic on invisible cavities without a project requirement.

---

## 17. Blender API strategy

Prefer direct data access and controlled BMesh/data-layer operations over UI-dependent editing.

The executor should:
- resolve the semantic surface group;
- ensure/reuse the UV map;
- inspect UV loops for the selected polygons;
- unwrap/project by a deterministic algorithm or a controlled operator adapter;
- rotate/scale/translate UV coordinates directly;
- ensure/reuse the intended material data-block and slot;
- validate the resulting loops against the region contract.

Any context-sensitive unwrap operator must be isolated behind a tested adapter and followed by deterministic UV transformation and validation.

---

## 18. Suggested executor architecture

```text
blender_agent/
  trim_sheets/
    analysis.py
    surface_groups.py
    region_catalog.py
    region_selection.py
    uv_mapping.py
    physical_scale.py
    material_assignment.py
    validation.py
    repair.py
```

Example high-level contract:

```python
result = trim.apply(
    target="Bench_Frame",
    surface="OUTER_FRAME",
    sheet="LAFAR_TRIMS_01",
    region="PAINTED_METAL_EDGE_MEDIUM",
    orientation="AUTO",
    physical_scale="PROJECT",
)
```

---

## 19. Validation

Every autonomous trim operation must validate at least:

### Structural
- target mesh exists;
- semantic surface group resolves;
- UV layer exists;
- trim material exists/is reused;
- selected region exists in the catalog.

### UV
- assigned loops remain in the allowed band orthogonal to the repeat axis;
- any out-of-0..1 tiling is explicitly allowed;
- no accidental sampling of neighboring trim regions;
- orientation is correct;
- mirroring is semantically allowed;
- overlap classification is intentional.

### Scale
- physical trim width/profile is plausible and consistent;
- texel-density class/target is respected where applicable;
- sibling assets using the same semantic region remain consistent.

### Runtime
- duplicate materials are not created;
- material-slot growth is justified;
- mip/padding rules remain safe;
- the target engine can reproduce the material behavior.

---

## 20. Validation report

```yaml
trim_validation:
  object: Bench_Frame
  surface: OUTER_FRAME
  region: PAINTED_METAL_EDGE_MEDIUM
  result: PASS
  checks:
    semantic_surface_resolved: PASS
    region_role_compatible: PASS
    orientation: PASS
    band_bounds: PASS
    repeat_axis: PASS
    overlap: INTENTIONAL_SHARED_TRIM
    physical_scale: PASS
    texel_density_px_per_m:
      target: 512
      measured: 498
      status: PASS
    material_reuse: PASS
```

Do not return PASS merely because UV coordinates exist.

---

## 21. Repair strategy

Repair the narrowest failure:

- wrong semantic region -> re-run region selection;
- wrong orientation -> rotate/reverse the strip;
- stretching -> split into more coherent surface groups;
- wrong physical width -> correct band/scale selection;
- generic density mismatch -> recalculate scale without violating the trim profile;
- cross-region leakage -> clamp/re-fit orthogonal band occupancy;
- inappropriate trim strategy -> reclassify as TILING, DECAL, UNIQUE or GEOMETRY;
- excessive material slots -> consolidate equivalent materials.

Prefer local repair over complete remapping when the failure is local.

---

## 22. Common failure modes

- choosing a region by geometric fit instead of semantic material role;
- rotating directional trim incorrectly;
- treating any UV overlap as invalid even though trim reuse is intentional;
- using a bare, unitless `texel_density` value;
- stretching the narrow axis of a trim until its physical profile is wrong;
- allowing UV tiling to sample neighboring atlas regions;
- creating duplicate materials for the same trim sheet;
- forcing unique hero surfaces into generic trim regions;
- forcing large homogeneous surfaces into a narrow trim band;
- assuming trim sheets automatically reduce draw calls;
- persisting only raw polygon indices after topology-changing operations.

---

## 23. Autonomous decision table

| Condition | Action |
|---|---|
| Repeated structural border/profile | TRIM |
| Broad homogeneous area | TILING |
| Unique local graphic | DECAL |
| Unique baked hero area | UNIQUE_UV_OR_BAKE |
| Feature changes silhouette | GEOMETRY |
| No compatible trim region | Escalate/reclassify |
| Directional region + requested mirror | Validate direction before mirroring |
| Shared trim overlap | Allow and classify intentionally |
| Runtime sampler cannot safely repeat atlas axis | Keep UV inside safe region / use alternative |

---

## 24. Completion criteria

A trim-sheet assignment is complete only when:

```text
[ ] surface strategy is classified
[ ] semantic surface group is stable
[ ] trim region is semantically compatible
[ ] material is reused rather than duplicated unnecessarily
[ ] UV orientation is correct
[ ] physical trim scale is correct
[ ] texel-density unit/target is explicit where used
[ ] intentional overlap/tiling is classified
[ ] UVs do not leak into unrelated regions
[ ] mip/padding behavior is safe
[ ] runtime material behavior is supported
[ ] validation report is PASS or documented WARN
```

---

## 25. Final instruction

Think in terms of **surface strategy and resource reuse**, not manual UV manipulation.

The correct pipeline is:

`classify -> choose region -> map -> preserve physical scale -> reuse material -> validate -> repair`

Trim sheets are successful when they preserve the asset's design language while reducing unnecessary unique texture work without creating hidden runtime or UV problems.

---

## FILE: `03_modeling/41_DECALS_AND_FLOATING_DETAILS.md`

# Decals and Floating Details

## Cel

Dodawać lokalne informacje wizualne bez niepotrzebnego komplikowania topologii głównego mesha — ale bez udawania, że floating geometry potrafi zastąpić każdą zmianę powierzchni.

## Kandydaci

- oznaczenia,
- logo,
- numery,
- ostrzeżenia,
- ślady serwisowe,
- cienkie panel lines bez istotnego parallax,
- małe techniczne detale,
- warianty assetów,
- drobne śruby/znaczniki przenoszone do atlasu lub normal mapy.

---

# Fundamental limitation

**Floating geometry can add a visible surface. It cannot remove host geometry.**

A floating plate/patch placed near a cylinder does not create a real recess, slot or cavity in that cylinder.

If the intended feature is physically inset, choose one of:
- real cut/recess in the host mesh;
- boolean/rebuilt topology;
- high-to-low normal/height bake;
- material/parallax technique supported by the runtime;
- deliberate flat decal only when parallax is not required.

Do not place a floating feature *inside* an opaque host surface and assume its material/emission makes it visible.

---

# Geometry decals / floating meshes

Dobre, gdy:
- potrzebny jest lokalny detal,
- główny mesh nie powinien być komplikowany,
- feature jest addytywny lub optyczny, nie wymaga usunięcia host surface,
- pipeline/runtime poprawnie obsługuje takie powierzchnie.

Kontroluj:
- z-fighting,
- offset,
- normals,
- bounds,
- curvature conformity,
- LOD behavior,
- visibility/occlusion.

## Visibility proof

For a visible floating feature, object existence is not enough.

Require at least one proof:
- target ROI contains pixels attributable to the feature;
- ray/occlusion test confirms the host does not hide it;
- geometric offset is outside the host along the correct surface normal;
- depth/parallax QA shows the intended relationship.

A material with emission > 0 on a fully occluded surface is still a failed feature.

---

# Recess decision

Before using floating geometry ask:

```text
Does this feature require negative depth into the host?
```

If YES:

```text
visible parallax / silhouette / deep shadow required?
-> real geometry/recess

shallow feature, runtime normal map sufficient?
-> bake/normal strategy

pure graphic or value/color change?
-> decal
```

Do not use floating geometry as a cheap substitute for a reference-critical recess.

---

# Texture decals

Dobre dla:
- oznaczeń,
- wariantów,
- zabrudzeń,
- informacji diegetycznych,
- serial numbers,
- manufacturer branding,
- small non-parallax wear.

## Source fidelity

When an authoritative logo/graphic file exists, use it as source rather than approximating the mark with new geometry or guessed typography.

Record provenance:

```yaml
decal_source:
  feature_id: BRAND_01
  source_file: path/to/logo.png
  transform: stacked_lockup
  alpha_method: source_alpha_or_documented_extraction
  confidence: LOCKED
```

Do not redraw a supplied brand mark unless the task explicitly requests reinterpretation.

---

# Decal atlas

Dla wielu drobnych oznaczeń preferuj atlas zamiast osobnej tekstury per decal, jeśli jest to zgodne z runtime material strategy.

Atlas contract should define:
- source region;
- UV rectangle;
- alpha policy;
- color space;
- padding;
- LOD visibility;
- material slot ownership.

Do not let LOD/export builders delete decal owners as a side effect of rebuilding geometry.

Reusable builder modules must be side-effect free on import.

---

# Curved host surfaces

For a cylindrical/curved host:
- conform the floating surface to the host curvature;
- maintain a controlled proud/offset value;
- avoid a flat card visibly cutting across the cylinder;
- validate from oblique views, not only front ortho.

The offset should be the minimum necessary to avoid z-fighting/occlusion while respecting reference evidence.

Do not increase panel/decal depth merely because flat QA lighting makes it hard to see.
First separate lighting/material readability from geometry.

---

# Nie używaj decal jako maskowania błędu konstrukcyjnego

Jeżeli referencja ma realne wcięcie o widocznym parallax:
- geometria lub displacement/bake może być właściwszy.

Jeżeli floating detail znika:
1. check host occlusion;
2. check normal direction;
3. check offset;
4. check alpha/material;
5. only then modify dimensions if reference evidence supports it.

---

# LOD

Małe decals powinny:
- zanikać w odpowiednim LOD,
- nie pozostawiać migoczących mikropowierzchni,
- być usuwane według Feature Contract / screen-size relevance,
- nie przypadkiem znikać z LOD0/LOD1 podczas przebudowy/exportu.

Branding may remain longer than serial text if it contributes to asset identity at distance.

---

# Game-ready validation

Before completion:
- exported mesh still contains intended decal geometry/material assignment;
- referenced image actually appears in exported/runtime material data;
- no missing texture path;
- alpha mode is compatible with target engine;
- LOD policy is explicit;
- floating features marked as `SURFACE_DETAIL` pass visibility QA.


---

## FILE: `03_modeling/42_CURVES_FOR_ASSETS.md`

# Curves for Game Asset Authoring

## Zastosowania

Curves są użyteczne dla:
- kabli,
- rur,
- poręczy,
- listew,
- uszczelek,
- przewodów,
- profili prowadzonych po ścieżce.

## Authoring advantage

Curve pozwala oddzielić:
- przebieg,
- profil,
- grubość,
- resolution.

To ułatwia poprawki względem ręcznego przesuwania wielu vertices.

## Parameters

Kontroluj:
- spline points,
- handles,
- cyclic state,
- bevel depth/profile,
- resolution,
- tilt,
- radius.

## Runtime conversion

Curve jest przede wszystkim authoring representation.
Jeżeli runtime wymaga mesh:
- konwertuj na kontrolowanym etapie,
- zachowaj curve source,
- po konwersji zweryfikuj polycount i normals.

## Resolution

Nie ustawiaj wysokiej resolution domyślnie.
Dobierz ją do:
- promienia krzywizny,
- dystansu kamery,
- silhouette.

## Endpoints

Sprawdź:
- caps,
- połączenie z assetem,
- przenikanie,
- orientację profilu.

## Reusable profiles

Profile rur, uszczelek i listew powinny być współdzielone, jeśli projekt wykorzystuje jeden język konstrukcyjny.


---

## FILE: `03_modeling/43_GEOMETRY_NODES_AUTHORING.md`

# Geometry Nodes for Asset Authoring

## Rola

Geometry Nodes traktuj jako system proceduralnego authoringu:
- generowanie powtórzeń,
- rozmieszczanie,
- warianty,
- modularne konstrukcje,
- parametryczne detale.

Nie używaj tylko dlatego, że zadanie "da się zrobić nodami".

## Dobre zastosowania

- rzędy paneli,
- śruby/łączniki,
- moduły fasady,
- proceduralne barierki,
- rozmieszczanie instancji,
- warianty długości,
- kontrolowane scatter.

## Instancing first

Jeżeli rezultat składa się z powtarzalnych elementów:
- zachowuj instancje możliwie długo,
- nie realizuj ich bez potrzeby.

`Realize Instances` jest granicą, po której instancje stają się realną geometrią.

## Realize only when

- dalszy node musi edytować geometrię per-element,
- eksport/pipeline nie zachowuje wymaganej instancji,
- bake lub operacja topologiczna tego wymaga.

## Inputs

Wszystkie parametry projektowe powinny być wejściami grupy:
- width,
- height,
- count,
- spacing,
- seed,
- profile,
- variant selector.

## Determinism

Jeżeli używasz losowości:
- seed jest jawny,
- seed zapisany w asset contract,
- rezultat musi być reprodukowalny.

## Assetization

Node group powinien mieć:
- nazwę,
- wersję,
- jasno opisane inputy,
- zakresy,
- jednostki,
- fallback defaults.

## Escape hatch

Jeżeli Geometry Nodes zwiększa złożoność napraw prostego unikalnego prop, użyj klasycznego modelowania.


---

## FILE: `03_modeling/44_PROCEDURAL_MATERIAL_AUTHORING.md`

# Procedural Material Authoring

## Rola

Proceduralny shader jest narzędziem authoringowym.
Nie zakładaj, że cały graph zostanie przeniesiony do silnika.

## Dobre zastosowania

- szybkie lookdev,
- maski,
- proceduralne zabrudzenie,
- tileable surface detail,
- generowanie danych do bake.

## Runtime decision

Dla każdego proceduralnego efektu wybierz:
- recreate in engine,
- bake to textures,
- remove,
- Blender-only preview.

## Coordinate discipline

Jawnie wybieraj coordinate space:
- UV,
- object,
- generated,
- world.

Zmiana transformacji obiektu może wpływać na proceduralne mapowanie.

## Scale

Proceduralne wzory muszą mieć fizyczną skalę.
"Noise scale = 5" bez odniesienia do metrów projektu nie jest trwałą wiedzą.

## Material parameters

Preferuj wspólny zestaw:
- base color family,
- roughness range,
- metallic state,
- normal strength,
- detail scale,
- wear amount.

## Game-ready

Przed eksportem sprawdź:
- które właściwości są rzeczywiście reprezentowane przez docelowy format,
- czy tekstury zostały wypieczone,
- czy packed channels są zgodne z silnikiem.


---

## FILE: `03_modeling/45_AXISYMMETRIC_PROFILE_ASSET_PRIMITIVE.md`

# Axisymmetric Profile Asset Primitive

## Skill ID

`AXISYMMETRIC_PROFILE`

## Purpose

Build rotationally symmetric hard-surface parts from an explicit 2D radius/height profile revolved around a known axis.

Typical assets/features:
- bollards;
- posts;
- cylindrical housings;
- caps and collars;
- light rings;
- bases;
- round knobs and service rings.

Use this skill when the design is defined primarily by stacked radial profile changes rather than arbitrary surface sculpting.

## Why this is a semantic primitive

A profile revolution guarantees by construction:
- shared center axis;
- exact radii;
- deterministic height transitions;
- repeatable circumferential segmentation;
- predictable triangle cost;
- straightforward cylindrical UVs.

Do not rebuild the same `lathe()`/revolve helper inside every asset script.

## Input contract

```yaml
axisymmetric_profile:
  feature_id: F001
  object_name: BOL_MainBody
  axis: Z
  unit: mm
  segments: 32
  profile:
    - [70.0, 66.0]
    - [70.0, 954.0]
  closed_profile: false
  cap_bottom: false
  cap_top: false
  smoothing: AUTO_BY_PROFILE
  uv_mode: CYLINDRICAL_ARC_LENGTH
```

A profile point is `[radius, axis_position]`.

Optional:
- explicit corner fillet radii;
- per-segment material bands;
- start angle;
- seam angle;
- cap policy;
- normal/sharp-edge policy.

## Preconditions

- axis and origin are known;
- radial dimensions are LOCKED/HIGH confidence or explicitly provisional;
- no required feature breaks rotational symmetry inside this primitive;
- segment count satisfies silhouette and triangle budget.

Asymmetric features such as service panels, logos or local emitters are separate feature owners added after the master rotational geometry is accepted.

## Segment selection

Choose circumference segments from:
- projected silhouette size;
- target LOD;
- radius;
- expected viewing distance;
- triangle budget.

Do not increase segmentation because a local asymmetric detail needs more topology. Keep local detail separate when possible.

For a small game-ready civic prop, 24–32 segments is often sufficient, but the actual contract/QA result wins.

## Fillet/bevel policy

Prefer fillets encoded directly in the radial profile when:
- the radius is dimension-critical;
- modifier order would make bevel width unstable;
- the part is fully rotationally symmetric.

Use a normal Bevel modifier when editability or downstream variation is more important and the modifier can be validated reliably.

Do not create unnecessary profile rings. Every extra radial profile point multiplies around the circumference and can dominate triangle count.

## UV policy

For the revolved side wall:
- U = normalized angle around axis;
- V = normalized or physical arc length along the profile.

This produces deterministic orientation and avoids selection-dependent UV operators.

Caps require a separate planar/radial mapping policy.

## Topology contract

Each generated object must explicitly declare one of:

```text
CLOSED_SOLID
OPEN_ASSEMBLY_PART
SURFACE_DETAIL
```

`CLOSED_SOLID` requires zero boundary/non-manifold edges.

`OPEN_ASSEMBLY_PART` is allowed only when the open boundary is intentionally sealed/occluded by another owned assembly feature and the Game Asset Contract allows it.

Never report a general `mesh PASS` while boundary edges exist and topology intent is unspecified.

## Postconditions

Validate:
- axis center deviation;
- min/max radius;
- min/max Z/axis position;
- total dimensions;
- circumferential continuity;
- duplicate vertices;
- zero-area faces;
- boundary edges against topology intent;
- UV existence;
- triangle count.

## Asymmetric feature handoff

After the rotational master passes:

```text
service panel -> dedicated curved-surface/local-detail strategy
radial bolt pattern -> radial repetition strategy
logo/serial -> decal
local base emitter -> local feature owner
```

Do not distort the rotational master simply to accommodate these details.

## Candidate executor

Canonical candidate implementation:

`executors/axisymmetric_profile.py`

Until that implementation is benchmarked in the active Blender runtime, registry maturity remains `CONTRACT_READY`.


---

## FILE: `blender-agent-procedural-hard-surface-panel-lines.md`

# Blender Agent Skill: Procedural Hard-Surface Panel Lines and Grooves

## Purpose

This skill defines how a Blender AI agent creates, updates, validates, and repairs hard-surface panel lines, seams, and narrow grooves procedurally through the Blender Python API.

The skill is intended for reconstruction workflows in which an AI agent must reproduce concept-art details with deterministic geometry instead of simulating manual UI actions.

The core technique implemented here is based on a non-destructive modifier stack:

```text
semantic panel-line path
        ->
mesh edges representing the path
        ->
Sharp edge marking
        ->
Edge Split
        ->
Solidify
        ->
Bevel
        ->
Subdivision Surface: SIMPLE
        ->
Subdivision Surface: CATMULL_CLARK
        ->
validated high-poly groove geometry
```

The primary target is high-poly/detail geometry suitable for rendering or baking normal maps. It must not be assumed to be appropriate as final game-export topology.

---

## Skill name

`blender-agent-procedural-hard-surface-panel-lines.md`

---

## When the agent should use this skill

Use this skill when the requested or detected geometry contains any of the following:

- panel separation lines;
- cosmetic seams;
- structural shell seams;
- narrow recessed hard-surface lines;
- sci-fi panel lines;
- technical grooves whose visual width is small relative to the parent surface;
- continuous L-shaped, U-shaped, rectangular, polygonal, or segmented seam paths;
- high-poly detail that should later be baked into a normal map;
- concept-art details that are better represented as a path than as a Boolean volume.

Typical semantic requests:

```text
Create a 3 mm structural seam along the left casing.

Reconstruct the visible L-shaped groove from the concept-art side view.

Add a cosmetic panel line 18% from the top edge and continue it vertically downward.

Match this seam to the reference image without permanently cutting the export mesh.
```

---

## When the agent should NOT use this skill

Do not use this technique by default when:

- the feature is a wide recess rather than a narrow seam;
- the groove must remove substantial physical volume;
- the feature changes the silhouette;
- the feature is a through-hole;
- the panel is physically detached from the surrounding shell;
- the final topology itself must contain the recess for gameplay or collision reasons;
- a Boolean cutter expresses the design intent more accurately;
- the detail is purely material-based and does not require geometry;
- the requested result is a final low-poly game mesh and the generated subdivision density would be excessive.

Preferred alternatives:

```text
wide recess       -> HS_RECESS
through opening   -> HS_CUTOUT
slot              -> HS_SLOT
vent array        -> HS_VENT
raised panel      -> HS_RAISED_PANEL
silhouette detail -> direct base-mesh modeling
```

---

# 1. Agent mental model

The agent must reason about a panel line as a semantic geometric object, not as a sequence of Blender clicks.

Wrong abstraction:

```text
Enter Edit Mode.
Press K.
Click four times.
Press Enter.
Select edges.
Mark Sharp.
Add modifiers.
```

Correct abstraction:

```python
PanelLine(
    id="side_shell_seam_01",
    surface="LEFT_SHELL",
    path=[
        (0.18, 0.77),
        (0.43, 0.77),
        (0.43, 0.39),
        (0.81, 0.39),
    ],
    profile="STRUCTURAL_SMALL",
)
```

The execution layer is responsible for translating this intent into Blender geometry.

The agent should reason at three levels:

```text
LEVEL 1: INTENT
"There is a narrow structural seam visible on the left shell."

LEVEL 2: SEMANTIC GEOMETRY
PanelLine(surface, normalized_path, profile)

LEVEL 3: BLENDER EXECUTION
projection -> topology -> sharp edges -> modifiers -> validation
```

The agent must keep Level 2 independent of temporary Blender edge indices.

---

# 2. Hard rules

## 2.1 Never treat edge indices as persistent identity

Do not store semantic intent as:

```python
edge_indices = [124, 125, 131, 140]
```

Edge indices can change after topology edits, modifiers are applied, geometry is rebuilt, objects are joined, meshes are triangulated, or another reconstruction step modifies connectivity.

Edge indices may be used only as short-lived execution data inside one atomic operation.

Persistent intent must be stored as one or more of:

- normalized path coordinates;
- local-space 3D path coordinates;
- stable semantic surface identifier;
- mesh edge-domain custom attribute;
- custom object metadata describing the panel line.

---

## 2.2 Prefer a dedicated detail shell

By default the agent must not run this Sharp/Edge Split technique on the only production copy of the base mesh.

Reason:

```text
Edge Split with use_edge_sharp=True
```

acts on all edges marked Sharp on that mesh. Other sharp edges may exist for shading or unrelated hard-surface treatment.

Default structure:

```text
ASSET_ROOT
|
+-- Asset_BASE
|
+-- Asset_PANEL_HIGH
|
+-- Asset_BOOLEAN_HIGH
|
+-- Asset_EXPORT
```

Recommended panel-line target:

```text
Asset_PANEL_HIGH
```

The detail shell may be:

- a controlled duplicate of the relevant surface;
- a separated copy of selected faces;
- a reconstruction-only high-poly object;
- a disposable bake source.

Only use the primary mesh directly if the agent has verified that Sharp edge semantics are dedicated exclusively to this subsystem.

---

## 2.3 Prefer data API and BMesh over UI operators

Preferred:

```python
obj.data.edges[i].use_edge_sharp = True
obj.modifiers.new(...)
bmesh.new()
bmesh.ops...
```

Avoid as the default automation mechanism:

```python
bpy.ops.mesh.mark_sharp()
bpy.ops.object.modifier_add(...)
```

Reason:

`bpy.ops` is often context-sensitive and can depend on selection state, active object, editor state, mode, or current area. A reconstruction agent should minimize hidden UI state.

Use operators only when a specific Blender operation has no sufficiently reliable data API or BMesh equivalent, and isolate such use behind a tested adapter.

---

## 2.4 Use meters internally

All geometric profile dimensions must be represented internally in meters.

Examples:

```text
0.0005 m = 0.5 mm
0.0010 m = 1.0 mm
0.0020 m = 2.0 mm
0.0040 m = 4.0 mm
```

The asset may be displayed in any unit system, but the skill contract must remain numerically unambiguous.

---

## 2.5 Do not apply modifiers prematurely

Keep the stack non-destructive until one of the following explicitly requires application:

- baking pipeline;
- export preparation;
- downstream topology operation requiring evaluated geometry;
- explicit finalization request.

The semantic reconstruction data must remain editable even if modifiers are later applied.

---

# 3. Semantic data contract

The recommended input object is:

```python
panel_line = {
    "id": "side_shell_seam_01",
    "target_object": "Bench_SidePanel_PANEL_HIGH",
    "surface_id": "LEFT_SHELL",
    "coordinate_space": "SURFACE_NORMALIZED_2D",
    "path": [
        (0.18, 0.77),
        (0.43, 0.77),
        (0.43, 0.39),
        (0.81, 0.39),
    ],
    "profile": "STRUCTURAL_SMALL",
    "closed": False,
    "source": "concept_art",
    "confidence": 0.93,
}
```

Required fields:

```text
id
surface_id or an explicit local surface frame
path
profile or explicit dimensions
```

Recommended fields:

```text
target_object
coordinate_space
closed
source
confidence
reference_view
reference_feature_id
```

---

# 4. Coordinate spaces

## 4.1 Preferred representation: surface-normalized 2D

For mostly planar hard-surface panels, represent points in a normalized local 2D frame:

```text
u: 0.0 -> 1.0 across the usable surface width
v: 0.0 -> 1.0 across the usable surface height
```

Example:

```python
path = [
    (0.20, 0.75),
    (0.45, 0.75),
    (0.45, 0.35),
    (0.80, 0.35),
]
```

This representation survives asset resizing better than absolute edge indices or arbitrary global coordinates.

---

## 4.2 Surface frame

A planar surface frame should contain:

```python
surface_frame = {
    "origin": (x, y, z),
    "u_axis": (ux, uy, uz),
    "v_axis": (vx, vy, vz),
    "normal": (nx, ny, nz),
    "u_size": 0.80,
    "v_size": 0.42,
}
```

Conversion:

```text
P = origin
  + u_axis * (u * u_size)
  + v_axis * (v * v_size)
```

The agent must define whether `origin` corresponds to lower-left, upper-left, center, or another explicit anchor. Do not infer silently.

Recommended convention:

```text
origin = lower-left of the semantic surface frame
u      = left -> right
v      = bottom -> top
```

---

## 4.3 Curved surfaces

For curved shells, normalized points describe the intended path approximately in a reference frame, then each point or sampled segment must be projected onto evaluated surface geometry.

Preferred tools:

```python
Object.ray_cast(...)
Object.closest_point_on_mesh(...)
```

Use ray casting when the expected projection direction is known.

Use closest-point projection as a fallback when ray direction is ambiguous or the source point is already near the target surface.

Do not project through the object onto an unintended rear surface without checking hit normal and distance.

---

# 5. Panel-line profiles

Use named profiles instead of inventing dimensions separately for every operation.

Initial library:

```python
PANEL_PROFILES = {
    "COSMETIC_MICRO": {
        "depth": 0.0006,
        "bevel_width": 0.00020,
        "bevel_segments": 2,
        "simple_levels": 1,
        "smooth_levels": 1,
    },
    "COSMETIC_SMALL": {
        "depth": 0.0010,
        "bevel_width": 0.00035,
        "bevel_segments": 2,
        "simple_levels": 1,
        "smooth_levels": 2,
    },
    "STRUCTURAL_SMALL": {
        "depth": 0.0015,
        "bevel_width": 0.00050,
        "bevel_segments": 3,
        "simple_levels": 1,
        "smooth_levels": 2,
    },
    "STRUCTURAL_MEDIUM": {
        "depth": 0.0030,
        "bevel_width": 0.00100,
        "bevel_segments": 3,
        "simple_levels": 1,
        "smooth_levels": 2,
    },
    "HEAVY_PANEL": {
        "depth": 0.0060,
        "bevel_width": 0.00150,
        "bevel_segments": 4,
        "simple_levels": 1,
        "smooth_levels": 2,
    },
}
```

These are starting presets, not universal physical standards.

For 1:1 reconstruction, reference-derived dimensions override preset defaults.

The profile system exists to provide:

- consistent style;
- deterministic defaults;
- controlled parameter search;
- easier visual comparison;
- reusable asset-family standards.

---

# 6. Execution strategies

The agent must select one of three strategies.

## Strategy A: reuse an existing edge path

Use when the intended panel-line path already follows mesh edges closely enough.

Procedure:

```text
find candidate edges
-> verify continuity
-> verify geometric deviation
-> tag them as panel-line edges
-> set Sharp
-> build/reuse modifier stack
-> validate evaluated result
```

This is the cheapest and preferred route.

---

## Strategy B: create missing topology on the detail shell

Use when the path is on the target surface but corresponding edges do not yet exist.

Procedure:

```text
project semantic path to surface
-> find containing/intersected faces
-> create/split vertices and edges
-> preserve valid face topology
-> record resulting semantic edge attribute
-> set Sharp
-> modifier stack
-> validate
```

Implementation should use `bmesh` whenever practical.

Relevant BMesh concepts:

```text
bmesh.new()
bm.from_mesh(mesh)
bmesh.ops.bisect_edges(...)
bmesh.ops.subdivide_edges(...)
bmesh.ops.connect_verts(...)
bm.to_mesh(mesh)
bm.free()
```

The exact topology operation depends on whether projected path points land on vertices, edges, or face interiors.

---

## Strategy C: rebuild a dedicated path-friendly shell

Use when the source topology is unsuitable for deterministic cutting, for example:

- dense triangulated import;
- poor Meshy/AI-generated topology;
- many tiny irregular faces;
- non-manifold local region;
- uncontrolled overlapping surfaces;
- projection creates unstable topology;
- the panel-line detail only exists for bake/render purposes.

Procedure:

```text
extract/reconstruct clean surface shell
-> establish stable local surface frame
-> create panel-line topology on clean shell
-> run modifier stack
-> bake or render
```

For reconstruction agents this is often better than attempting to preserve unusable source topology.

---

# 7. Modifier stack specification

The canonical stack is:

```text
01 PANEL_EdgeSplit
02 PANEL_Solidify
03 PANEL_Bevel
04 PANEL_SubdivisionSimple
05 PANEL_SubdivisionSmooth
```

The order is part of the skill contract.

---

## 7.1 Edge Split

Required configuration:

```python
edge_split = obj.modifiers.new(
    name="PANEL_EdgeSplit",
    type='EDGE_SPLIT',
)

edge_split.use_edge_angle = False
edge_split.use_edge_sharp = True
```

Intent:

```text
split only explicitly Sharp-marked semantic panel-line edges
```

Do not enable angle-based splitting for this subsystem unless the reconstruction specifically requires it.

---

## 7.2 Solidify

Required baseline:

```python
solidify = obj.modifiers.new(
    name="PANEL_Solidify",
    type='SOLIDIFY',
)

solidify.thickness = depth
solidify.use_even_offset = True
solidify.use_rim = True
solidify.use_rim_only = True
```

The exact sign of `thickness` depends on shell orientation and expected groove direction.

The agent must visually/geometrically validate direction rather than assuming positive thickness always means inward.

If the groove is generated on the wrong side:

```text
first inspect normals and shell orientation
then invert thickness or correct normals
```

Do not hide reversed normals by randomly changing thickness signs across assets.

---

## 7.3 Bevel

Baseline:

```python
bevel = obj.modifiers.new(
    name="PANEL_Bevel",
    type='BEVEL',
)

bevel.width = bevel_width
bevel.segments = bevel_segments
bevel.limit_method = 'NONE'
bevel.use_clamp_overlap = True
```

`limit_method='NONE'` is acceptable on the dedicated panel-line shell because the shell exists for this detail treatment.

If the modifier unexpectedly bevels unrelated geometry, this is evidence that the target object is insufficiently isolated. Prefer isolating the shell rather than accumulating brittle modifier exceptions.

---

## 7.4 Simple subdivision

```python
subdiv_simple = obj.modifiers.new(
    name="PANEL_SubdivisionSimple",
    type='SUBSURF',
)

subdiv_simple.subdivision_type = 'SIMPLE'
subdiv_simple.levels = simple_levels
subdiv_simple.render_levels = simple_levels
```

Purpose:

- add supporting geometry;
- preserve overall shape;
- improve the next smoothing stage.

---

## 7.5 Catmull-Clark subdivision

```python
subdiv_smooth = obj.modifiers.new(
    name="PANEL_SubdivisionSmooth",
    type='SUBSURF',
)

subdiv_smooth.subdivision_type = 'CATMULL_CLARK'
subdiv_smooth.levels = smooth_levels
subdiv_smooth.render_levels = smooth_levels
```

Purpose:

- smooth the generated groove profile;
- improve high-poly shading and bake quality.

Do not raise subdivision levels automatically to fix an incorrect cross-section. Repair geometry/profile settings first.

---

# 8. Idempotent Python implementation

The execution code must be safe to run repeatedly.

Repeated execution must not create:

```text
PANEL_Bevel
PANEL_Bevel.001
PANEL_Bevel.002
...
```

Use deterministic modifier names and create-or-reuse behavior.

```python
import bpy


def ensure_modifier(obj, name, modifier_type):
    existing = obj.modifiers.get(name)

    if existing is not None:
        if existing.type != modifier_type:
            raise TypeError(
                f"Modifier {name!r} exists on {obj.name!r} "
                f"but has type {existing.type!r}, expected {modifier_type!r}."
            )
        return existing

    return obj.modifiers.new(name=name, type=modifier_type)
```

---

# 9. Reference implementation: build modifier stack

```python
import bpy


def ensure_modifier(obj, name, modifier_type):
    modifier = obj.modifiers.get(name)

    if modifier is not None:
        if modifier.type != modifier_type:
            raise TypeError(
                f"Modifier {name!r} on {obj.name!r} has type "
                f"{modifier.type!r}, expected {modifier_type!r}."
            )
        return modifier

    return obj.modifiers.new(name=name, type=modifier_type)


def ensure_panel_line_stack(
    obj,
    *,
    depth=0.0015,
    bevel_width=0.0005,
    bevel_segments=3,
    simple_levels=1,
    smooth_levels=2,
):
    if obj is None:
        raise ValueError("Panel-line target object is None.")

    if obj.type != 'MESH':
        raise TypeError(
            f"Panel-line target {obj.name!r} must be a MESH, got {obj.type!r}."
        )

    edge_split = ensure_modifier(
        obj,
        "PANEL_EdgeSplit",
        'EDGE_SPLIT',
    )
    edge_split.use_edge_angle = False
    edge_split.use_edge_sharp = True

    solidify = ensure_modifier(
        obj,
        "PANEL_Solidify",
        'SOLIDIFY',
    )
    solidify.thickness = float(depth)
    solidify.use_even_offset = True
    solidify.use_rim = True
    solidify.use_rim_only = True

    bevel = ensure_modifier(
        obj,
        "PANEL_Bevel",
        'BEVEL',
    )
    bevel.width = float(bevel_width)
    bevel.segments = int(bevel_segments)
    bevel.limit_method = 'NONE'
    bevel.use_clamp_overlap = True

    subdiv_simple = ensure_modifier(
        obj,
        "PANEL_SubdivisionSimple",
        'SUBSURF',
    )
    subdiv_simple.subdivision_type = 'SIMPLE'
    subdiv_simple.levels = int(simple_levels)
    subdiv_simple.render_levels = int(simple_levels)

    subdiv_smooth = ensure_modifier(
        obj,
        "PANEL_SubdivisionSmooth",
        'SUBSURF',
    )
    subdiv_smooth.subdivision_type = 'CATMULL_CLARK'
    subdiv_smooth.levels = int(smooth_levels)
    subdiv_smooth.render_levels = int(smooth_levels)

    return {
        "edge_split": edge_split,
        "solidify": solidify,
        "bevel": bevel,
        "subdiv_simple": subdiv_simple,
        "subdiv_smooth": subdiv_smooth,
    }
```

---

# 10. Enforce modifier order

Creating modifiers by name is not enough if the object already contains other modifiers or the stack was manually reordered.

The agent must verify canonical relative order:

```text
PANEL_EdgeSplit
before
PANEL_Solidify
before
PANEL_Bevel
before
PANEL_SubdivisionSimple
before
PANEL_SubdivisionSmooth
```

If the API/version-specific implementation for moving modifiers is available and tested, reorder them programmatically.

Otherwise fail validation explicitly rather than silently accepting a wrong stack.

Pseudo-contract:

```python
validate_modifier_order(
    obj,
    [
        "PANEL_EdgeSplit",
        "PANEL_Solidify",
        "PANEL_Bevel",
        "PANEL_SubdivisionSimple",
        "PANEL_SubdivisionSmooth",
    ],
)
```

---

# 11. Marking existing edges as panel-line edges

Short-lived execution helper:

```python
def mark_edges_sharp(obj, edge_indices, clear_existing=False):
    if obj.type != 'MESH':
        raise TypeError("Target must be a mesh.")

    mesh = obj.data

    if clear_existing:
        for edge in mesh.edges:
            edge.use_edge_sharp = False

    for index in edge_indices:
        if not 0 <= index < len(mesh.edges):
            raise IndexError(
                f"Edge index {index} out of range for {obj.name!r}."
            )

        mesh.edges[index].use_edge_sharp = True

    mesh.update()
```

This helper is not a semantic persistence layer.

The caller must already have determined which temporary edge indices represent the requested semantic path.

---

# 12. Semantic edge attribute

Use an edge-domain boolean attribute to record which edges belong to this subsystem whenever possible.

Recommended attribute name:

```text
agent_panel_line
```

Optional multi-line classification attributes:

```text
agent_panel_line
agent_panel_line_group
agent_panel_line_profile
```

A simple boolean attribute can be created as:

```python
def ensure_panel_line_edge_attribute(mesh, name="agent_panel_line"):
    attr = mesh.attributes.get(name)

    if attr is None:
        attr = mesh.attributes.new(
            name=name,
            type='BOOLEAN',
            domain='EDGE',
        )

    if attr.domain != 'EDGE':
        raise TypeError(f"Attribute {name!r} must use EDGE domain.")

    return attr
```

The Sharp state remains the mechanism consumed by Edge Split, while the custom attribute is the agent's semantic bookkeeping layer.

After any topology-changing operation, validate whether the attribute still maps correctly to the intended edge path.

Never assume attribute propagation is perfect across every topology operation.

---

# 13. Path reconstruction pipeline

For a normalized path:

```python
[
    (0.18, 0.77),
    (0.43, 0.77),
    (0.43, 0.39),
    (0.81, 0.39),
]
```

use the following pipeline.

## Step 1: resolve target surface

Identify a semantic surface frame or the exact source faces.

Output:

```python
surface = {
    "object": obj,
    "face_indices": [...],
    "origin": ...,
    "u_axis": ...,
    "v_axis": ...,
    "normal": ...,
    "u_size": ...,
    "v_size": ...,
}
```

---

## Step 2: convert normalized points to 3D candidates

```python
from mathutils import Vector


def surface_uv_to_local_point(surface, u, v):
    origin = Vector(surface["origin"])
    u_axis = Vector(surface["u_axis"]).normalized()
    v_axis = Vector(surface["v_axis"]).normalized()

    return (
        origin
        + u_axis * (float(u) * float(surface["u_size"]))
        + v_axis * (float(v) * float(surface["v_size"]))
    )
```

---

## Step 3: project onto the actual mesh

For curved or imperfect surfaces, project candidate points onto evaluated geometry.

Example fallback using closest point:

```python
def project_local_point_to_mesh(obj, point_local, depsgraph=None):
    if depsgraph is None:
        depsgraph = bpy.context.evaluated_depsgraph_get()

    hit, location, normal, face_index = obj.closest_point_on_mesh(
        point_local,
        depsgraph=depsgraph,
    )

    if not hit:
        raise RuntimeError(
            f"Could not project point {tuple(point_local)} onto {obj.name!r}."
        )

    return {
        "location": location,
        "normal": normal,
        "face_index": face_index,
    }
```

Projection validation must include:

```text
maximum allowed projection distance
expected normal orientation
allowed face set / semantic surface region
front/back ambiguity check
```

---

## Step 4: determine whether path already exists

Search nearby vertices and edges using a scale-aware tolerance.

Do not use a fixed arbitrary tolerance such as `0.01` for every asset.

Recommended tolerance basis:

```text
tolerance = max(
    absolute_minimum,
    object_diagonal * relative_tolerance
)
```

Example:

```text
absolute_minimum = 0.0001 m
relative_tolerance = 1e-4
```

If an existing continuous edge chain is within tolerance, reuse it.

---

## Step 5: create topology if missing

The topology builder must classify each projected point as approximately:

```text
EXISTING_VERTEX
ON_EDGE
INSIDE_FACE
```

Then:

```text
EXISTING_VERTEX -> reuse vertex
ON_EDGE         -> split/bisect edge
INSIDE_FACE     -> create face split topology
```

Do not create overlapping duplicate vertices or edges.

BMesh validity requirements:

- no duplicate edges;
- no duplicate faces;
- all faces contain at least 3 vertices;
- selection state is irrelevant unless a UI operator is invoked;
- write BMesh back to the mesh after topology changes;
- free standalone BMesh data when finished.

---

# 14. BMesh skeleton

```python
import bmesh


def edit_mesh_with_bmesh(obj, edit_callback):
    if obj.type != 'MESH':
        raise TypeError("Target must be a mesh object.")

    mesh = obj.data
    bm = bmesh.new()

    try:
        bm.from_mesh(mesh)
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()

        result = edit_callback(bm)

        bm.normal_update()
        bm.to_mesh(mesh)
        mesh.update()

        return result

    finally:
        bm.free()
```

This isolates BMesh lifecycle management from the geometry-specific operation.

---

# 15. Path creation is not equivalent to creating wire edges

A panel line running through an existing surface must become part of the surface topology.

Wrong:

```text
create free-floating vertices
connect them with wire edges
place them visually on top of the surface
```

This does not correctly split the underlying faces and may not produce the intended Edge Split/Solidify behavior.

Correct:

```text
new path vertices become vertices of affected faces
new path edges split affected faces
surface topology remains valid
```

Use face-aware BMesh operations.

---

# 16. Existing-edge path resolver

The resolver receives projected path segments and returns a continuous mesh edge chain.

Required checks:

```text
1. Candidate edges are near the requested path.
2. Candidate edges form a connected chain.
3. Chain ordering matches semantic path ordering.
4. Maximum perpendicular deviation is below tolerance.
5. Chain does not leave the allowed semantic surface.
6. Chain does not contain large unintended detours.
```

Suggested output:

```python
{
    "status": "REUSED_EXISTING_TOPOLOGY",
    "edge_indices": [...],
    "max_path_deviation": 0.00018,
    "path_length_requested": 0.412,
    "path_length_actual": 0.413,
}
```

---

# 17. Visual-intent preservation

The agent must distinguish three concepts:

```text
path location
profile dimensions
surface relationship
```

A concept-art seam can be positioned correctly but still look wrong because:

- groove is too deep;
- bevel is too round;
- groove is too wide;
- smoothing changes corner shape;
- projection drifts around curved surfaces;
- line is offset from a nearby panel boundary;
- line terminates too early or too late.

Validation must therefore include both path geometry and cross-section appearance.

---

# 18. Corner handling

Panel lines commonly contain corners:

```text
L
U
rectangle
stepped path
polygon
```

The agent should preserve semantic corner locations exactly unless a rounded corner is explicitly visible in the reference.

Do not smooth path coordinates merely because the final modifier stack contains subdivision.

The path is the design skeleton.

The modifier stack controls the groove profile.

These are different layers of geometry.

---

# 19. Closed panel lines

A closed path:

```text
+-------------+
|             |
|             |
+-------------+
```

must be represented explicitly:

```python
{
    "closed": True,
    "path": [P0, P1, P2, P3]
}
```

Do not require the final point to be duplicated as `P0` unless the implementation contract explicitly uses that representation.

The executor should close the final segment internally.

Validate:

```text
last -> first connection exists
no duplicate zero-length closing segment
consistent winding
no self intersection
```

---

# 20. Self-intersection handling

Before cutting topology, detect path self-intersections in the semantic surface frame.

Example invalid path:

```text
\ /
 X
/ \
```

Default behavior:

```text
FAIL
```

Do not silently create ambiguous panel topology.

Allowed exception:

A deliberate crossing is explicitly represented as separate panel-line features with defined depth/priority behavior.

---

# 21. Multiple panel lines on one detail shell

Preferred:

```text
one semantic registry
one controlled Sharp state
one canonical modifier stack
many panel-line paths
```

Do not create five identical modifier stacks for five seams unless they require genuinely different cross-sections.

If different profiles are required on one object, prefer one of:

```text
A. separate detail-shell objects by profile
B. separate semantic material/detail layer
C. a more advanced geometry-node/custom system
```

The basic Sharp/Edge Split modifier stack does not natively encode a different Solidify thickness for every individual Sharp edge set.

---

# 22. Object naming

Recommended deterministic naming:

```text
<BaseName>_BASE
<BaseName>_PANEL_HIGH
<BaseName>_BOOLEAN_HIGH
<BaseName>_EXPORT
```

Examples:

```text
Bench_Frame_BASE
Bench_Frame_PANEL_HIGH
Bench_Frame_EXPORT

TamudaWall_Module06_BASE
TamudaWall_Module06_PANEL_HIGH
```

Do not use names such as:

```text
Cube.017
Cube_copy_final2
panelnew
```

for semantically important reconstruction objects.

---

# 23. Semantic metadata persistence

Store enough metadata to regenerate the detail after destructive changes.

Example:

```python
import json


def save_panel_line_registry(obj, registry):
    obj["agent_panel_lines"] = json.dumps(
        registry,
        separators=(",", ":"),
        sort_keys=True,
    )
```

Example stored structure:

```json
{
  "version": 1,
  "lines": [
    {
      "id": "side_shell_seam_01",
      "surface_id": "LEFT_SHELL",
      "coordinate_space": "SURFACE_NORMALIZED_2D",
      "path": [[0.18, 0.77], [0.43, 0.77], [0.43, 0.39], [0.81, 0.39]],
      "profile": "STRUCTURAL_SMALL",
      "closed": false
    }
  ]
}
```

The registry is the source of semantic truth.

Temporary mesh edge indices are execution artifacts.

---

# 24. Updating an existing panel line

Agent command:

```python
update_panel_line(
    id="side_shell_seam_01",
    path=new_path,
)
```

Expected behavior:

```text
1. Resolve registry entry.
2. Remove/clear previous panel-line topology or regenerate the detail shell.
3. Reconstruct the path from semantic data.
4. Reapply semantic edge attributes and Sharp state.
5. Reuse canonical modifier stack.
6. Validate.
7. Replace registry entry only after successful validation.
```

For reconstruction assets, regenerating a dedicated detail shell from clean source geometry may be safer than surgically deleting an old path.

Prefer determinism over clever local mutation.

---

# 25. Deleting a panel line

Deletion by semantic ID:

```python
delete_panel_line("side_shell_seam_01")
```

must not mean:

```text
clear an arbitrary list of remembered edge indices
```

The executor should either:

- rebuild the detail shell without that semantic line; or
- resolve the currently tagged edge group safely and remove its effect.

If geometry surgery risks corrupting topology, rebuild from semantic source data.

---

# 26. Evaluated-geometry validation

Modifier parameters alone do not prove the result is correct.

The agent must inspect evaluated geometry.

Conceptual pattern:

```python
depsgraph = bpy.context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(depsgraph)
```

Depending on the Blender version and geometry-access path used by the runtime, the agent may inspect an evaluated mesh or evaluated geometry set.

Validation must operate on the final evaluated result whenever the measurement concerns visible post-modifier geometry.

Do not measure only the original cage and claim the groove output is correct.

---

# 27. Required validation report

Every autonomous panel-line operation should produce a machine-readable report.

Minimum:

```python
{
    "operation": "panel_line",
    "feature_id": "side_shell_seam_01",
    "status": "PASS",
    "target": "Bench_SidePanel_PANEL_HIGH",
    "profile": "STRUCTURAL_SMALL",
    "path_segments": 3,
    "closed": False,
    "max_path_deviation_m": 0.00018,
    "self_intersections": 0,
    "non_manifold_edges": 0,
    "modifier_order_valid": True,
    "sharp_path_continuous": True,
}
```

Recommended additional metrics:

```text
requested path length
actual path length
projection max distance
projection mean distance
requested groove depth
measured groove depth
requested bevel width
measured/estimated visible width
triangle count before modifiers
triangle count after evaluated stack
normal consistency
number of disconnected sharp components
```

---

# 28. Pass/fail conditions

## PASS

All must be true:

```text
semantic path resolved
path is continuous
path is on intended surface
no unintended Sharp edges are consumed by this subsystem
modifier stack exists
modifier order is valid
no invalid self intersection
no newly introduced non-manifold topology unless explicitly allowed
visual profile direction is correct
geometric deviation is within tolerance
```

## FAIL

Fail explicitly if any of the following occurs:

```text
surface cannot be resolved
projection hits wrong shell repeatedly
requested path leaves the semantic surface
path is self-intersecting without explicit crossing semantics
topology operation creates duplicate/invalid faces
edge chain is discontinuous
Sharp classification leaks to unrelated edges
modifier stack order cannot be guaranteed
result points outward when an inward seam is required and cannot be safely corrected
required path tolerance cannot be met
```

Do not return PASS merely because Blender did not throw an exception.

---

# 29. Repair strategy hierarchy

When validation fails, repair in this order.

```text
1. Re-evaluate surface frame and projection.
2. Re-resolve existing topology with adjusted scale-aware tolerance.
3. Rebuild local detail topology.
4. Rebuild dedicated detail shell from clean source.
5. Switch to a different hard-surface operation if panel-line semantics are incorrect.
```

Do not immediately increase subdivision levels.

Do not randomly perturb geometry until the validator passes.

---

# 30. Performance rules

The stack can become expensive because subdivision multiplies geometry.

Rules:

```text
Viewport smooth levels should normally remain <= 2.
Use SIMPLE level 1 unless measurement proves more is required.
Prefer Bevel segments 2-3 for most reconstruction work.
Use 4+ bevel segments only for close high-poly requirements.
Disable expensive high-poly detail objects outside reconstruction/bake views when practical.
Do not export the evaluated high-poly stack as the game mesh by default.
```

Track evaluated geometry growth.

Example warning threshold:

```text
if evaluated_triangles > base_triangles * 100:
    issue PERFORMANCE_WARNING
```

The exact threshold may be asset-specific.

---

# 31. High-poly versus game mesh

Default production flow:

```text
CONCEPT ART
    ->
BASE RECONSTRUCTION
    ->
PANEL_HIGH
    ->
high-poly panel-line geometry
    ->
NORMAL/AO BAKE
    ->
EXPORT mesh + baked maps
```

The presence of a valid high-poly groove does not imply that the same geometry should be exported into the runtime.

The reconstruction layer and game-optimization layer are separate concerns.

---

# 32. Profile-selection reasoning

The agent should estimate panel-line class from reference scale.

Example heuristic:

```text
visible hairline / cosmetic separation
-> COSMETIC_MICRO or COSMETIC_SMALL

clear manufactured shell seam
-> STRUCTURAL_SMALL

prominent equipment casing channel
-> STRUCTURAL_MEDIUM

large armored panel separation
-> HEAVY_PANEL or switch to HS_RECESS
```

If the feature width exceeds approximately a few percent of the local surface dimension, question whether it is still semantically a panel line.

Do not force every elongated recess into this skill.

---

# 33. Concept-art reconstruction integration

When the panel line comes from an image, store measurement provenance.

Example:

```python
{
    "id": "front_panel_seam_02",
    "source": {
        "type": "concept_art",
        "view": "FRONT",
        "reference_id": "concept_front_v03",
        "pixel_polyline": [
            [412, 188],
            [612, 188],
            [612, 366],
            [801, 366]
        ]
    },
    "surface_path": [...],
    "confidence": 0.91
}
```

This permits later comparison between rendered output and the original reference.

---

# 34. Multi-view reconstruction rule

If the same seam is visible in multiple orthographic/reference views, do not independently reconstruct two different 3D paths.

Instead:

```text
all views constrain one semantic 3D feature
```

Procedure:

```text
infer candidate 3D path
-> project candidate into each reference view
-> measure reprojection error
-> optimize/repair one 3D path
```

The semantic feature ID remains single and stable.

---

# 35. Example agent request

Input:

```json
{
  "operation": "HS_PANEL_LINE",
  "target_object": "Bench_LeftShell_PANEL_HIGH",
  "feature_id": "left_shell_seam_01",
  "surface_id": "LEFT_OUTER_SURFACE",
  "coordinate_space": "SURFACE_NORMALIZED_2D",
  "path": [
    [0.16, 0.78],
    [0.46, 0.78],
    [0.46, 0.42],
    [0.83, 0.42]
  ],
  "profile": "STRUCTURAL_SMALL",
  "closed": false
}
```

Expected execution:

```text
resolve LEFT_OUTER_SURFACE
-> convert normalized path to surface coordinates
-> project to real mesh
-> search existing edge chain
-> if absent, create topology in BMesh
-> tag semantic edges
-> mark semantic edges Sharp
-> ensure canonical panel modifier stack
-> evaluate result
-> validate path, topology, direction and profile
-> persist semantic registry
-> return report
```

---

# 36. Example high-level Python API

The reconstruction agent should ultimately call a compact interface such as:

```python
result = hs.panel_line.create(
    target="Bench_LeftShell_PANEL_HIGH",
    feature_id="left_shell_seam_01",
    surface="LEFT_OUTER_SURFACE",
    path=[
        (0.16, 0.78),
        (0.46, 0.78),
        (0.46, 0.42),
        (0.83, 0.42),
    ],
    coordinate_space="SURFACE_NORMALIZED_2D",
    profile="STRUCTURAL_SMALL",
    closed=False,
)
```

The LLM should not normally generate the underlying BMesh implementation for every asset.

The underlying library should be deterministic, versioned, tested, and reusable.

---

# 37. Suggested Python package layout

```text
blender_agent/
|
+-- geometry/
|   +-- mesh_access.py
|   +-- topology.py
|   +-- projection.py
|   +-- surface_frames.py
|   +-- metrics.py
|
+-- hard_surface/
|   +-- panel_lines.py
|   +-- recesses.py
|   +-- grooves.py
|   +-- cutouts.py
|   +-- slots.py
|   +-- vents.py
|   +-- seams.py
|
+-- reconstruction/
|   +-- feature_registry.py
|   +-- concept_projection.py
|   +-- semantic_surfaces.py
|
+-- validation/
|   +-- topology.py
|   +-- geometry.py
|   +-- modifiers.py
|   +-- reconstruction_error.py
|
+-- profiles/
    +-- panel_lines.py
```

This skill defines the behavior expected from:

```text
hard_surface/panel_lines.py
```

---

# 38. Suggested public interface

```python
class PanelLineService:
    def create(self, *, target, feature_id, surface, path,
               profile, coordinate_space, closed=False):
        ...

    def update(self, feature_id, **changes):
        ...

    def delete(self, feature_id):
        ...

    def rebuild(self, feature_id):
        ...

    def validate(self, feature_id):
        ...

    def rebuild_all(self, target):
        ...
```

Important property:

```text
rebuild_all(target)
```

must be able to reconstruct all panel lines from semantic registry data without relying on historical edge indices.

This is the determinism test for the subsystem.

---

# 39. Determinism test

A valid implementation should pass:

```text
1. Start from clean BASE shell.
2. Load semantic panel-line registry.
3. Generate PANEL_HIGH.
4. Save validation metrics.
5. Delete generated PANEL_HIGH.
6. Generate it again from the same inputs.
7. Compare geometry/metrics.
```

Expected:

```text
same semantic paths
same profile settings
same modifier ordering
same topology class
same validation result within numeric tolerance
```

If reconstruction depends on random UI state or undocumented selection history, the skill implementation is not acceptable.

---

# 40. Transaction rule

Complex topology edits should behave transactionally.

Preferred pattern:

```text
snapshot semantic registry
-> operate on disposable/generated detail shell
-> validate
-> commit generated result
```

If validation fails:

```text
preserve previous valid generated object
return FAIL report
```

Do not leave partially edited production geometry as the only version of the asset.

---

# 41. Error taxonomy

Use explicit error codes.

```text
PL001 TARGET_NOT_MESH
PL002 TARGET_NOT_FOUND
PL003 SURFACE_NOT_RESOLVED
PL004 PATH_PROJECTION_FAILED
PL005 PATH_OUTSIDE_SURFACE
PL006 PATH_SELF_INTERSECTION
PL007 EDGE_CHAIN_DISCONTINUOUS
PL008 TOPOLOGY_BUILD_FAILED
PL009 UNINTENDED_SHARP_EDGE_CONFLICT
PL010 MODIFIER_STACK_INVALID
PL011 GROOVE_DIRECTION_WRONG
PL012 NON_MANIFOLD_RESULT
PL013 PROFILE_TOLERANCE_FAILED
PL014 PERFORMANCE_LIMIT_EXCEEDED
PL015 SEMANTIC_REGISTRY_INVALID
```

Warnings:

```text
PLW01 REUSED_APPROXIMATE_EXISTING_EDGE_CHAIN
PLW02 HIGH_EVALUATED_POLYCOUNT
PLW03 REFERENCE_CONFIDENCE_LOW
PLW04 SOURCE_TOPOLOGY_POOR
PLW05 CURVED_SURFACE_PROJECTION_APPROXIMATE
```

---

# 42. Minimum logging

Each operation should log:

```text
feature ID
target object
selected strategy A/B/C
profile
path point count
projection tolerance
number of reused edges
number of created vertices/edges/faces
modifier creation/reuse
validation metrics
final status
```

Do not log every individual Blender RNA assignment unless debug mode is enabled.

---

# 43. Agent decision table

| Condition | Action |
|---|---|
| Correct edge chain already exists | Strategy A: reuse |
| Clean quad/ngon shell, path missing | Strategy B: create topology |
| Imported triangulated/noisy shell | Strategy C: rebuild detail shell |
| Feature is wide/deep | Switch to recess/Boolean skill |
| Feature changes silhouette | Edit base mesh, not panel-line detail |
| Sharp edges already have unrelated semantic use | Dedicated PANEL_HIGH shell required |
| Multiple line widths required | Separate shells/profile groups or advanced system |
| Final asset is low-poly export | Bake high-poly detail; do not export stack by default |

---

# 44. Anti-patterns

The agent must not:

```text
simulate keyboard/mouse steps when data API is sufficient;
store panel identity only as edge indices;
apply modifiers immediately after creating them;
use one arbitrary numeric tolerance for all asset scales;
add more subdivision to hide broken topology;
run Edge Split on unrelated Sharp shading edges without isolation;
create free-floating wire paths instead of splitting surface topology;
claim success without evaluating the resulting geometry;
export high-poly subdivision geometry automatically;
reconstruct the same seam independently from each concept-art view;
mutate the only good production mesh without a recoverable semantic source;
randomly invert thickness instead of checking normals and groove direction.
```

---

# 45. Completion criteria

A panel-line feature is complete only when:

```text
[ ] semantic feature has stable ID
[ ] target semantic surface is known
[ ] path is stored independently of temporary edge indices
[ ] path is projected/resolved onto correct surface
[ ] topology contains a continuous edge representation
[ ] panel-line edges are semantically tagged
[ ] required edges are Sharp
[ ] unrelated Sharp edges are not consumed unintentionally
[ ] canonical modifier stack exists
[ ] modifier order is correct
[ ] profile parameters match requested/preset values
[ ] evaluated groove points in intended direction
[ ] topology is valid
[ ] path deviation is within tolerance
[ ] performance is within the asset budget or explicitly warned
[ ] semantic registry can regenerate the feature
[ ] validation report is PASS
```

---

# 46. Compact execution instruction for an autonomous agent

When asked to create a hard-surface panel line:

```text
1. Classify the feature as a narrow panel-line/seam rather than a wide recess.
2. Resolve the semantic target surface.
3. Represent the path in persistent surface-relative coordinates.
4. Prefer a dedicated PANEL_HIGH detail shell.
5. Reuse an existing matching edge chain if one exists.
6. Otherwise create valid face-splitting topology with BMesh.
7. Tag generated/reused edges semantically.
8. Mark only the intended panel-line edges Sharp.
9. Ensure this modifier stack in this order:
   Edge Split -> Solidify -> Bevel -> SIMPLE Subdivision -> CATMULL_CLARK Subdivision.
10. Evaluate the post-modifier geometry.
11. Validate path, topology, modifier order, groove direction, dimensions and performance.
12. Persist semantic reconstruction data only after success.
13. Return an explicit PASS/FAIL report with measurements.
14. Keep high-poly panel geometry separate from final game-export topology unless explicitly required.
```

---

# 47. API notes

The implementation relies on Blender Python capabilities including:

```text
bpy.types.MeshEdge.use_edge_sharp
bpy.types.EdgeSplitModifier.use_edge_angle
bpy.types.EdgeSplitModifier.use_edge_sharp
bpy.types.SolidifyModifier
bpy.types.BevelModifier
bpy.types.SubsurfModifier
bmesh
bmesh.ops
Object.ray_cast
Object.closest_point_on_mesh
Blender dependency-graph/evaluated geometry access
```

The runtime implementation should perform feature/property checks where practical when supporting multiple Blender versions.

Example:

```python
if not hasattr(edge_split, "use_edge_sharp"):
    raise RuntimeError(
        "This Blender build does not expose EdgeSplitModifier.use_edge_sharp."
    )
```

Do not silently substitute a different geometric technique when a required API capability is absent. Return a capability error or explicitly invoke a defined fallback implementation.

---

# 48. Source references for implementation verification

Official Blender Python API documentation should be treated as the implementation source of truth for API names and version behavior:

- Blender Python API: MeshEdge
- Blender Python API: EdgeSplitModifier
- Blender Python API: SolidifyModifier
- Blender Python API: BevelModifier
- Blender Python API: SubsurfModifier
- Blender Python API: BMesh Module
- Blender Python API: BMesh Operators
- Blender Python API: Object evaluated geometry, ray casting, and closest-point queries

When the Blender runtime version differs from the version used to write this skill, verify the affected RNA properties before changing the skill contract.

---

# 49. Architectural conclusion

This skill is not a tutorial for reproducing manual Blender actions.

It defines a reconstruction primitive:

```text
HS_PANEL_LINE
```

The AI agent provides semantic intent:

```text
where the panel line is
what surface it belongs to
what profile it has
how it relates to reference geometry
```

The deterministic Blender layer decides:

```text
which current edges represent the path
whether topology must be created
how the edges are tagged
how the modifier stack is configured
how the evaluated result is validated
```

The semantic reconstruction record, not the temporary Blender selection or edge index list, is the durable source of truth.

This separation is mandatory for an agent expected to reconstruct hard-surface assets repeatedly, update them after concept-art corrections, and reproduce the same result after topology or scene changes.


---

## FILE: `blender-agent-subdivision-topology-control.md`

# Blender Agent Skill: Subdivision-Surface Topology Control

## Purpose

This skill defines how a Blender AI agent designs, repairs, validates, and maintains topology intended to survive a Catmull-Clark Subdivision Surface workflow.

The source technique set comes from the supplied transcript of the tutorial at:

`https://www.youtube.com/watch?v=zSLELihVi6I`

The tutorial presents seven topology techniques for keeping SubD meshes clean. This skill converts those manual modeling ideas into reusable semantic operations for an autonomous Blender agent.

The agent must reason about **topology flow**, **support-loop density**, **curvature continuity**, **pole placement**, **local tessellation**, and **post-subdivision behavior** rather than reproducing keyboard and mouse actions.

This skill is primarily for:

- high-poly hard-surface modeling;
- VFX-style SubD control cages;
- reconstruction assets that require smooth manufactured surfaces;
- game-asset high-poly sources used for baking;
- curved hard-surface shells with integrated recesses, ports, buttons, tubes, or transitions.

It must not be assumed that the resulting control cage is the final runtime game mesh.

---

# 1. Core mental model

Subdivision Surface does not repair topology. It amplifies the consequences of topology.

The agent must separate four layers:

```text
DESIGN INTENT
    ->
CONTROL-CAGE TOPOLOGY
    ->
SUBDIVISION BEHAVIOR
    ->
EVALUATED SURFACE QUALITY
```

A valid cage is not merely a mesh with quads. A valid cage must produce the intended evaluated surface under the configured Subdivision Surface modifier.

The agent must therefore inspect both:

```text
base/control mesh
and
evaluated subdivided mesh
```

before returning PASS.

---

# 2. Skill primitives

This skill defines the following semantic operations:

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

These are not Blender operators. They are agent-level intentions translated into Blender API/BMesh operations.

---

# 3. General SubD rules

## 3.1 Support geometry is intentional geometry

Supporting edge loops exist to control the limit surface.

They must not be added globally by habit.

The agent should ask:

```text
Which feature requires support?
Which side of the feature requires support?
How far from the feature should the support lie?
Can the support terminate or redirect before crossing unrelated curvature?
```

---

## 3.2 Avoid unnecessary clusters of parallel loops

A common failure mode is:

```text
feature edge
support loop
support loop
another nearby structural loop
```

all traveling through the entire object.

This produces:

- dense local tessellation;
- difficult editing;
- poor deformation behavior;
- uneven displacement response;
- needless evaluated geometry;
- pinching when those loops enter curved regions.

The agent should redirect or terminate support topology when the extra density is no longer needed.

---

## 3.3 Even spacing matters on curved surfaces

On planar surfaces, irregular edge spacing may have little visible consequence.

On curved surfaces, uneven spacing changes the way Catmull-Clark distributes the limit surface and can create:

- pinching;
- flattening;
- waviness;
- visible shading discontinuity;
- uneven displacement tessellation.

The agent should measure local edge-length variance and loop spacing when a failure occurs on a curved area.

---

## 3.4 Do not use subdivision level as a substitute for correct topology

Increasing subdivision can reduce some visible artifacts because the sampled surface becomes denser, but this is not the first repair strategy.

Repair order:

```text
1. inspect topology flow
2. inspect support-loop placement
3. inspect pole location and valence
4. inspect local tessellation density
5. increase base resolution only when the curved feature genuinely lacks enough control points
6. increase render subdivision only after the cage is structurally sound
```

---

## 3.5 Creases are not the default portability strategy

The source tutorial prefers supporting edge loops over creasing for VFX portability and surface quality.

This skill adopts the following policy:

```text
portable/high-poly reconstruction -> prefer support geometry
Blender-only temporary control     -> crease may be acceptable
pipeline explicitly supports it    -> crease may be acceptable
```

Do not claim that creases are universally invalid. Blender supports weighted edge creases. The reason to avoid them by default here is pipeline portability and predictable explicit topology, not an absence of Blender support.

---

# 4. SUBD_REDIRECT_CORNER_SUPPORT

## Source idea

When two support loops approach a corner, allowing both to continue around the entire mesh creates an unnecessary three-loop cluster.

Instead, the support flow can be redirected diagonally through the corner so the excess inner loops dissolve and the topology exits the corner cleanly.

## Semantic operation

```python
SUBD_REDIRECT_CORNER_SUPPORT(
    feature_id,
    corner_region,
    incoming_support_loops,
    outgoing_support_path,
)
```

## Goal

Transform:

```text
three dense parallel loops near corner
```

into:

```text
one intentional support-flow turn
with unnecessary interior loops terminated
```

## Agent procedure

1. Identify the actual feature edge being supported.
2. Identify the two support loops surrounding it.
3. Find the corner vertex/region where all loops currently continue unnecessarily.
4. Build a diagonal connection across the corner.
5. Dissolve only the redundant interior loop sections.
6. Preserve the feature-support distance.
7. Validate the surrounding curved region after SubD.

## API strategy

Prefer BMesh topology editing:

```text
resolve semantic vertices
-> create/connect diagonal edge
-> split affected faces if required
-> dissolve redundant edges
-> update normals
```

Do not depend on the Knife tool UI unless an adapter is explicitly required.

## Validation

PASS requires:

- feature edge unchanged;
- support width unchanged within tolerance;
- no accidental n-gon self-intersection;
- redirected topology remains manifold;
- evaluated corner preserves intended sharpness;
- edge density outside the feature region is reduced;
- no new visible pinch is introduced.

---

# 5. SUBD_BUILD_SUPPORT_BEVEL

## Source idea

Instead of manually inserting support loops one by one around a hard boundary, selected feature edges can be beveled with a controlled profile to generate two support edges.

The tutorial uses approximately:

```text
segments = 2
profile/shape = 1
outer miter = ARC
```

then manually connects/cleans the corner topology.

## Semantic operation

```python
SUBD_BUILD_SUPPORT_BEVEL(
    feature_edges,
    support_distance,
    segments=2,
    profile=1.0,
    outer_miter="ARC",
)
```

## Interpretation

This bevel is not primarily a cosmetic bevel.

It is a **support-loop generator**.

The produced edges control the Catmull-Clark transition around a feature boundary.

## Agent rules

- Use a width derived from target edge softness, not an arbitrary default.
- Preserve original feature position.
- Avoid bevel widths that collide with nearby topology.
- Prefer a consistent support width within one manufactured edge family.
- After beveling a corner, inspect whether Arc miter topology should be simplified or redirected.

## API strategy

Preferred:

- BMesh bevel operation where suitable;
- direct mesh reconstruction for deterministic cases;
- operator fallback only behind a tested adapter.

## Important

A successful bevel operation is not a successful SubD result.

Always evaluate the post-Subdivision surface.

---

# 6. SUBD_REPAIR_CURVED_PINCHING

## Source idea

Pinching around a hard detail embedded in a curved surface is often caused by insufficient or uneven base tessellation.

The tutorial demonstrates that the same feature on a denser sphere produces less obvious pinching.

## Diagnostic model

Potential causes:

```text
P1 insufficient radial tessellation
P2 support loops too close together
P3 support loops enter curvature at poor angles
P4 high-valence pole too close to visible curvature
P5 asymmetric vertex spacing
P6 feature topology too dense relative to host surface
P7 normals/topology errors
```

## Agent procedure

1. Render/evaluate without changing subdivision level.
2. Locate the pinch region.
3. Measure host-surface edge spacing around it.
4. Compare detail-loop spacing to surrounding cage spacing.
5. Inspect extraordinary vertices and valence.
6. If the host surface is genuinely under-resolved, add controlled base tessellation.
7. Reproject/relax vertices to preserve the original curvature.
8. Re-evaluate.

## Base-resolution increase

Allowed when:

- a curved surface has too few vertices to accommodate the requested feature;
- the added topology remains reasonably even;
- the increase improves curvature rather than simply hiding broken connectivity.

## Material and distance criterion

The agent may accept residual low-level pinching if:

- it is below the asset's visual tolerance;
- it is invisible at intended screen size;
- the material does not reveal it under expected highlights;
- the reference does not require closer fidelity.

This decision must be reported, not silently ignored.

---

# 7. SUBD_TERMINATE_LOCAL_DENSITY

## Source idea

A local feature may require several extra loops, but those loops should not necessarily continue through the entire mesh.

The tutorial terminates extra topology by moving neighboring vertices, connecting outer vertices, and dissolving the interior edges.

## Semantic operation

```python
SUBD_TERMINATE_LOCAL_DENSITY(
    dense_region,
    termination_direction,
    target_loop_count,
)
```

## Purpose

Transition from:

```text
high local loop density
```

to:

```text
lower background loop density
```

without visible deformation.

## Topological concept

This is a controlled edge-flow reduction.

The agent should create a transition topology rather than allowing every loop to propagate globally.

## Rules

- Place termination away from the strongest highlight/curvature when possible.
- Do not stack many poles in a tiny area.
- Keep edge-length change gradual.
- Prefer termination on flatter regions.
- Preserve the host silhouette.

## Repetition

The technique may be applied multiple times if several density reductions are required.

Each reduction must be individually validated.

## Example use cases

- button cluster on a control panel;
- local screw recesses;
- dense vent area;
- switch array;
- connector plate;
- local embossed feature.

---

# 8. SUBD_CURVED_CYLINDER_RECESS

## Source idea

A high-sided cylinder Booleaned directly into a curved surface may look acceptable before SubD but creates unsuitable topology for a clean subdivision cage.

The tutorial instead uses a lower-sided cylinder with edge spacing comparable to the host surface, performs the Boolean as a construction aid, then manually reconnects the resulting circular boundary into the surrounding edge flow.

## Semantic operation

```python
SUBD_CURVED_CYLINDER_RECESS(
    host_surface,
    center,
    axis,
    radius,
    depth,
    radial_segments,
)
```

## Primary principle

**Match feature resolution to host-surface resolution.**

Do not create a 64-sided circular boundary inside a host region containing only a few broad quads.

## Segment selection

The tutorial prefers powers of two as a practical modeling habit.

This skill treats that as a heuristic, not a mathematical requirement.

Preferred segment candidates may include:

```text
8, 16, 32
```

when they fit:

- feature size;
- host edge spacing;
- visible roundness;
- intended SubD level.

## Procedure

1. Estimate average host edge spacing near the recess.
2. Choose the smallest radial segment count that can represent the circular feature after SubD.
3. Create/position the cylindrical construction primitive.
4. Use Boolean Difference only as an intermediate geometric intersection if useful.
5. Capture the resulting boundary loop.
6. Remove unusable Boolean topology if necessary.
7. Route boundary vertices into nearby host loops.
8. Send left-side vertices toward compatible left-going flow, top vertices toward top-going flow, etc.
9. Reduce unnecessary edges.
10. Prefer quads where they improve predictable SubD flow, but do not distort the surface purely to avoid every triangle.
11. Add support topology around the recess.
12. Fill/repair the center or surrounding region with a predictable grid when appropriate.
13. Evaluate with SubD.

## Important

Boolean is not the final topology solution in this operation.

It is an intersection/construction aid.

## Quad policy

The source tutorial prefers keeping the region in quads when easy.

This skill uses a stricter rule:

```text
prefer clean predictable quads in deformation/highlight-critical regions;
allow controlled triangles where they do not create visible SubD artifacts and pipeline policy permits them.
```

Do not create tortured quads solely to satisfy an all-quad ideology.

## Grid Fill

Grid Fill may be used when the boundary conditions are appropriate.

The agent must verify:

- boundary continuity;
- compatible vertex count;
- resulting grid orientation;
- preservation of curvature.

---

# 9. SUBD_BUILD_POLE_SAFE_SPHERE

## Source idea

A conventional UV sphere concentrates many edges at the top and bottom poles. Under SubD and especially displacement, this can produce visible star-like artifacts.

The tutorial proposes two alternatives:

```text
icosphere -> subdivide -> spherize
```

or

```text
cube -> subdivide -> spherize
```

for more even tessellation.

## Semantic operation

```python
SUBD_BUILD_POLE_SAFE_SPHERE(
    radius,
    topology="CUBE_SPHERE" | "ICO_SPHERE",
    base_resolution,
)
```

## Decision

### UV sphere

Use only when:

- poles are hidden or irrelevant;
- the downstream operation tolerates poles;
- UV layout or latitude/longitude topology is specifically desired.

### Icosphere-derived sphere

Use when:

- distributed tessellation is desired;
- triangular starting topology is acceptable;
- subsequent subdivision/spherization fits the pipeline.

### Cube-sphere

Use when:

- relatively even quad distribution is desired;
- displacement quality matters;
- six-patch topology is acceptable.

## Spherization

The agent may use:

- To Sphere behavior;
- Cast-to-sphere logic;
- direct mathematical normalization of vertices to radius.

For autonomous code, direct deterministic geometry math is preferred when equivalent.

Example concept:

```python
p = vertex.co
vertex.co = p.normalized() * radius
```

subject to object-space and transform correctness.

## Validation

Evaluate:

- radial error;
- edge-length variance;
- pole artifact presence;
- displacement test if displacement is part of the intended workflow.

---

# 10. SUBD_REPAIR_BRANCH_JUNCTION

## Source idea

When one region splits into two branches, support loops can create three nearby directions of edge flow and a messy dense junction.

The tutorial resolves the junction by making two edges meet centrally, removing redundant edges, then introducing a better-spaced center loop and redirecting the flow.

## Semantic operation

```python
SUBD_REPAIR_BRANCH_JUNCTION(
    junction_region,
    branch_a,
    branch_b,
    support_family,
)
```

## Goal

Convert an uncontrolled multi-direction loop collision into a readable topology junction.

## Rules

- Preserve the two actual branches.
- Merge or redirect only support topology, not primary shape topology.
- Avoid two nearly coincident support loops after the junction.
- Introduce a central transition loop if it improves spacing.
- Place extraordinary vertices away from the strongest visible curvature when possible.

## Validation

Inspect:

- branch symmetry/asymmetry required by reference;
- support width through junction;
- limit-surface smoothness;
- local valence;
- no accidental crease or flattening.

---

# 11. SUBD_CURVED_CYLINDER_PROTRUSION

## Source idea

A cylindrical shape protruding from a surface can be created with Boolean Union, but the resulting topology generally requires cleanup for SubD.

The tutorial shows a cleaner construction approach:

```text
select region
-> inset
-> circularize
-> extrude
-> add supporting loops
```

On curved surfaces, the circularization operation must not flatten the host surface.

## Semantic operation

```python
SUBD_CURVED_CYLINDER_PROTRUSION(
    host_region,
    center,
    radius,
    height,
    axis,
    support_width,
)
```

## Preferred construction

1. Resolve a sufficiently regular host face region.
2. Create an inset boundary.
3. Circularize the boundary while preserving host curvature.
4. Extrude along intended local axis/normal.
5. Add radial/axial supporting topology.
6. Validate transition into the host surface.

## LoopTools note

The source tutorial uses the LoopTools Circle function and says to disable flattening on a curved surface.

For this AI skill:

- LoopTools is an optional capability, not a required dependency;
- current Blender distribution may expose LoopTools through the Blender Extensions ecosystem rather than guaranteeing it is already enabled;
- the agent must capability-check it before use;
- a deterministic mathematical/BMesh circularization fallback is preferred for portable automation.

## Circularization fallback

Given boundary vertices and a fitted local plane/frame:

```text
1. estimate center
2. estimate local normal
3. project boundary to local 2D frame
4. compute target angular positions
5. move vertices toward target radius
6. preserve/restitch the host curvature component rather than flattening the full region
```

On curved hosts, preserve each vertex's signed offset along the host surface normal or reproject the circularized boundary back to the evaluated host surface.

## Boolean fallback

Boolean Union remains allowed when:

- speed matters more than clean SubD topology;
- the asset will not use SubD;
- a later retopology pass is planned;
- the Boolean result is only a guide.

It is not the default for a final clean SubD cage.

---

# 12. SUBD_TOPOLOGY_AUDIT

The agent must not assess topology only by counting quads.

A SubD audit should inspect at least:

```text
control-cage manifold state
face degeneracy
edge-length distribution
support-loop spacing
local density ratio
extraordinary-vertex valence
pole placement
surface curvature around poles
triangle/ngon placement
feature-boundary continuity
modifier configuration
evaluated surface deviation
visible pinching
```

## Recommended report

```python
{
    "operation": "SUBD_TOPOLOGY_AUDIT",
    "object": "Asset_HIGH",
    "subdivision_levels": 2,
    "non_manifold_edges": 0,
    "degenerate_faces": 0,
    "extraordinary_vertices": 14,
    "high_valence_visible_region": 0,
    "max_local_edge_length_ratio": 2.1,
    "support_loop_collisions": 0,
    "visible_pinching_regions": [],
    "status": "PASS"
}
```

The exact thresholds are project/asset dependent.

---

# 13. Evaluated-surface validation

The base cage can appear clean while the final surface is wrong.

Validation should use the evaluated dependency-graph result when possible.

Conceptual Blender API pattern:

```python
depsgraph = bpy.context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(depsgraph)
```

Measure visible results on evaluated geometry rather than assuming modifier settings guarantee quality.

---

# 14. Curvature and highlight validation

Many SubD defects are most obvious under grazing highlights.

The QA layer should support a neutral diagnostic material and light rig.

Recommended modes:

```text
MATCAP / neutral glossy
wireframe-over-shaded
flat color + grazing light
curvature-sensitive studio light
```

A topology change is rejected if it creates a visible highlight kink not present in the reference or approved checkpoint.

---

# 15. Displacement stress test

The source tutorial points out that dense local tessellation and UV-sphere poles become especially visible under displacement.

For assets intended for displacement, the agent should optionally perform a diagnostic test using a controlled procedural displacement.

Purpose:

- expose uneven tessellation;
- expose pole artifacts;
- expose pinching;
- reveal abrupt density changes.

This diagnostic displacement is not part of the final asset unless explicitly requested.

---

# 16. Local density metric

Define a local edge-density estimate from average edge length in a region.

Example conceptual metric:

```text
density ~= 1 / mean_edge_length
```

Compare:

```text
feature region density
vs
neighboring host density
```

A very high ratio is not automatically wrong, but it triggers review.

The objective is not uniform tessellation everywhere.

The objective is **controlled and justified density**.

---

# 17. Pole policy

An extraordinary vertex is not automatically a topology error.

## Acceptable pole

- on relatively flat surface;
- away from silhouette;
- away from sharp specular highlight path;
- away from deformation-critical zone;
- necessary for clean density transition.

## Risky pole

- on tight curvature;
- directly next to a support loop;
- at a feature corner;
- inside a circular recess transition;
- where several density transitions collide.

## Agent rule

Do not optimize for zero poles.

Optimize for **well-placed poles**.

---

# 18. Triangle and n-gon policy

The tutorial often prefers quads because of predictable SubD flow.

This skill defines:

```text
QUAD        preferred in curved/highlight-critical SubD regions
TRIANGLE    allowed when its evaluated effect is validated
N-GON       allowed only when planar/stable or when subdivision behavior is explicitly verified
```

Do not automatically rewrite a stable solution into worse geometry merely to satisfy an all-quad metric.

---

# 19. Edge-flow decision table

| Condition | Preferred action |
|---|---|
| two support loops continue unnecessarily around a corner | `SUBD_REDIRECT_CORNER_SUPPORT` |
| need support loops around selected hard boundary | `SUBD_BUILD_SUPPORT_BEVEL` |
| curved region pinches around detail | `SUBD_REPAIR_CURVED_PINCHING` |
| local detail creates global unnecessary loops | `SUBD_TERMINATE_LOCAL_DENSITY` |
| circular recess enters curved surface | `SUBD_CURVED_CYLINDER_RECESS` |
| sphere poles produce star/displacement artifacts | `SUBD_BUILD_POLE_SAFE_SPHERE` |
| support flow collides at Y/branch junction | `SUBD_REPAIR_BRANCH_JUNCTION` |
| cylinder protrudes from surface | `SUBD_CURVED_CYLINDER_PROTRUSION` |
| unsure if cage is production-safe | `SUBD_TOPOLOGY_AUDIT` |

---

# 20. Reconstruction integration

When used with the Reconstruction Layer, topology is subordinate to reference fidelity.

The agent must never move a locked silhouette or dimension simply to obtain prettier topology.

Priority:

```text
1. explicit dimensional constraints
2. canonical-view shape
3. MUST features
4. surface continuity
5. topology elegance
```

If a clean topology solution cannot preserve the locked shape, report the conflict rather than altering the reference-derived form silently.

---

# 21. Integration with panel-line skill

The existing skill:

`blender-agent-procedural-hard-surface-panel-lines.md`

creates high-poly grooves and seams.

This SubD skill should be invoked when such detail:

- sits on a curved SubD shell;
- creates pinching;
- requires local density changes;
- must terminate support loops;
- interacts with a circular recess/protrusion.

The panel-line semantic feature remains the source of design intent.

This skill controls the surrounding SubD topology needed to support it.

---

# 22. Suggested service API

```python
class SubDTopologyService:
    def redirect_corner_support(self, *, target, feature_id, region, params):
        ...

    def build_support_bevel(self, *, target, edges, width, params):
        ...

    def repair_curved_pinching(self, *, target, region, tolerance):
        ...

    def terminate_local_density(self, *, target, region, target_density):
        ...

    def curved_cylinder_recess(self, *, target, center, axis,
                               radius, depth, radial_segments=None):
        ...

    def build_pole_safe_sphere(self, *, radius, topology, resolution):
        ...

    def repair_branch_junction(self, *, target, region, branches):
        ...

    def curved_cylinder_protrusion(self, *, target, region, radius,
                                   height, axis):
        ...

    def audit(self, *, target, subdivision_levels=2):
        ...
```

The LLM should call semantic operations instead of regenerating low-level BMesh code for every asset.

---

# 23. Suggested Python package layout

```text
blender_agent/
|
+-- topology/
|   +-- subd_analysis.py
|   +-- edge_flow.py
|   +-- density.py
|   +-- poles.py
|   +-- curvature.py
|
+-- hard_surface/
|   +-- subd_support.py
|   +-- circular_features.py
|   +-- branch_junctions.py
|
+-- primitives/
|   +-- cube_sphere.py
|   +-- ico_sphere.py
|
+-- validation/
    +-- subd_surface.py
    +-- pinching.py
    +-- tessellation.py
```

---

# 24. Transaction rule

Topology rewrites can be destructive.

Preferred workflow:

```text
accepted checkpoint
-> duplicate/generated working cage
-> perform topology rewrite
-> evaluate SubD
-> compare against locked geometry/reference
-> validate topology
-> commit replacement only if PASS
```

If validation fails, preserve the previous accepted cage.

---

# 25. Error taxonomy

```text
SD001 TARGET_NOT_MESH
SD002 SUBD_MODIFIER_MISSING_OR_UNRESOLVED
SD003 CORNER_FLOW_NOT_RESOLVED
SD004 SUPPORT_WIDTH_COLLISION
SD005 PINCHING_ABOVE_TOLERANCE
SD006 LOCAL_DENSITY_TRANSITION_FAILED
SD007 RECESS_BOUNDARY_FLOW_FAILED
SD008 POLE_ARTIFACT_FAILED
SD009 BRANCH_JUNCTION_FLOW_FAILED
SD010 CIRCULARIZATION_FAILED
SD011 CURVATURE_LOST
SD012 NON_MANIFOLD_RESULT
SD013 LOCKED_SHAPE_REGRESSION
SD014 EVALUATED_SURFACE_INVALID
SD015 PERFORMANCE_BUDGET_EXCEEDED
```

Warnings:

```text
SDW01 HIGH_LOCAL_DENSITY_RATIO
SDW02 HIGH_VALENCE_POLE_NEAR_VISIBLE_CURVATURE
SDW03 RESIDUAL_PINCHING_ACCEPTED_BY_SCREEN_TOLERANCE
SDW04 CREASE_USED_IN_PORTABLE_PIPELINE
SDW05 LOOPTOOLS_UNAVAILABLE_USING_FALLBACK
SDW06 BOOLEAN_USED_AS_INTERMEDIATE_CONSTRUCTION
```

---

# 26. Required validation gates

## Cage gate

```text
[ ] manifold unless explicitly intended otherwise
[ ] no degenerate faces
[ ] no accidental duplicate geometry
[ ] support loops correspond to real features
[ ] local density is justified
[ ] no uncontrolled dense loop propagation
[ ] pole placement reviewed
```

## Evaluated SubD gate

```text
[ ] silhouette preserved
[ ] explicit dimensions preserved
[ ] feature edge softness correct
[ ] no visible unacceptable pinching
[ ] no star-like pole artifact in relevant view
[ ] no unwanted flattening of curved host
[ ] no highlight kink introduced
```

## Runtime/high-poly gate

```text
[ ] subdivision density is appropriate for intended use
[ ] high-poly cage is not exported as runtime mesh by accident
[ ] bake source remains reproducible
[ ] control cage remains editable or reconstructable
```

---

# 27. Anti-patterns

The agent must not:

```text
add support loops through the entire mesh just because Loop Cut can do it;
judge topology only from the unsmoothed cage;
increase SubD levels to hide bad topology;
use extremely high-sided Boolean cylinders on low-density curved hosts;
place multiple density-termination poles in the same highlight-critical area;
use UV-sphere poles in displacement-critical hero regions without review;
flatten curved host surfaces while circularizing an extrusion boundary;
assume LoopTools is installed and enabled;
use crease as the default solution for every hard edge;
force every triangle into a distorted quad;
move reference-locked geometry only to make topology prettier;
accept a Boolean result as clean SubD topology without validation;
return PASS only because Blender completed the operation without an exception.
```

---

# 28. Compact autonomous-agent instruction

When working on a SubD hard-surface mesh:

```text
1. Identify which edges define real shape and which are only support topology.
2. Evaluate the current mesh under the intended Subdivision Surface level.
3. Detect unnecessary support-loop propagation, density clusters, poles and pinching.
4. Redirect support loops around corners instead of carrying every loop globally.
5. Generate support pairs with a controlled bevel when appropriate.
6. Terminate local density away from strong curvature/highlights.
7. Match circular-feature resolution to host-surface resolution.
8. For curved cylindrical recesses, treat Boolean as a construction aid and rebuild clean surrounding flow.
9. Prefer pole-safe sphere topology when poles/displacement would be visible.
10. Repair branch junctions so support flow does not collide in dense three-way clusters.
11. For cylindrical protrusions, prefer inset -> curvature-preserving circularization -> extrusion over an unclean Boolean union.
12. Inspect both cage and evaluated surface.
13. Validate silhouette, dimensions, curvature, pinching, edge spacing, poles and performance.
14. Preserve the previous accepted cage if the rewrite fails.
```

---

# 29. What comes directly from the supplied tutorial

The following ideas are directly derived from the supplied transcript:

- redirecting support loops diagonally around corners and dissolving redundant loops;
- generating support loops with a two-segment bevel using a strong profile and Arc outer miter;
- increasing host tessellation when a curved surface does not have enough topology to support a detail cleanly;
- terminating extra local loops instead of carrying them through the entire model;
- rebuilding cylindrical recess topology manually after using a lower-resolution Boolean cutter;
- preferring lower, controlled cylinder segment counts and matching their spacing to the surrounding mesh;
- using icosphere- or cube-derived spheres to avoid UV-sphere pole artifacts under SubD/displacement;
- cleaning three-way support-loop junctions by redirecting/merging the flow;
- creating cylindrical protrusions from inset and circularized host topology instead of relying on Boolean Union;
- preserving curvature when circularizing a region on a curved host surface.

---

# 30. Project adaptation beyond the tutorial

The following parts are deliberate agent/pipeline extensions rather than claims made explicitly in the tutorial:

- semantic `SUBD_*` operations;
- BMesh/data-API-first execution;
- evaluated-geometry QA;
- dimension/reference regression protection;
- topology audit metrics;
- transaction/checkpoint behavior;
- explicit pole and triangle policies;
- capability check and non-LoopTools circularization fallback;
- error taxonomy;
- high-poly/game-runtime separation;
- integration with the project's Reconstruction Layer and panel-line skill.

These adaptations are required because an autonomous agent needs deterministic contracts and validators rather than manual modeling intuition alone.

---

# 31. Blender implementation notes

Current Blender documentation confirms the core mechanisms used by this skill:

- Subdivision Surface uses Catmull-Clark or Simple subdivision and support edge loops can control sharpness;
- weighted edge creases are supported by Blender;
- bevel supports outer miter modes including Arc;
- Grid Fill creates structured quad grids from appropriate boundaries;
- To Sphere / sphere-casting operations exist for producing spherical distributions;
- LoopTools exists in the Blender Extensions ecosystem, so an automated agent must not assume it is enabled in every runtime.

Before relying on exact RNA/operator names, verify them against the Blender version targeted by the project.

Target project version for this repository: Blender 5.1.x.

---

# 32. Architectural conclusion

This skill teaches the agent that SubD topology is not a cosmetic cleanup pass.

It is a **surface-control system**.

The durable reasoning should be:

```text
feature requires a surface behavior
        ->
choose topology flow
        ->
place support density only where needed
        ->
redirect/terminate loops intentionally
        ->
place poles in low-risk regions
        ->
match local feature resolution to host curvature
        ->
evaluate Catmull-Clark result
        ->
repair measurable artifacts
```

The goal is not the prettiest wireframe screenshot.

The goal is the simplest controllable cage that reproduces the intended shape, survives subdivision predictably, remains editable, and does not create unnecessary tessellation or visible surface artifacts.

---

## FILE: `04_game_ready/40_GAME_ASSET_CONTRACT.md`

# Game Asset Contract

Każdy asset przed finalizacją powinien posiadać kontrakt runtime.

## Completion target

Declare during CONTRACT/PLAN:

```yaml
target_completion_level: GAME_READY_COMPLETE
```

Allowed values:
- `RECONSTRUCTION_COMPLETE`;
- `MODELING_COMPLETE`;
- `GAME_READY_COMPLETE`;
- `PIPELINE_INTEGRATED`.

Use `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md`.

## Geometry
- target triangles:
- max triangles:
- LOD count:
- deformation:
- backface assumptions:
- hidden geometry policy:
- per-object topology intent:

### Per-object topology intent

Każdy render/collision mesh deklaruje:

```text
CLOSED_SOLID
OPEN_ASSEMBLY_PART
SURFACE_DETAIL
COLLISION
```

Przykład:

```yaml
topology_contract:
  BOL_BasePlate: CLOSED_SOLID
  BOL_MainBody: OPEN_ASSEMBLY_PART
  BOL_ServicePanel: SURFACE_DETAIL
  COL_ACS_Bollard: COLLISION
```

`OPEN_ASSEMBLY_PART` wymaga zapisania, co zamyka/zasłania otwarte boundary i dlaczego runtime/backface policy to dopuszcza.

Nie można używać `OPEN_ASSEMBLY_PART` jako automatycznego obejścia błędu non-manifold.

`SURFACE_DETAIL` wymaga testu widoczności oraz braku niepożądanego z-fighting/occlusion.

Finalny validator: semantic skill `MESH_VALIDATE`.

## Materials
- max material slots:
- shader model:
- transparency:
- alpha mode:
- emissive:
- normal map:
- texture resolution:
- compression target:
- procedural authoring effects:
- runtime disposition per procedural effect (`BAKE` / `RECREATE_IN_ENGINE` / `EXPORT_NATIVELY_VERIFIED` / `REMOVE_BY_DESIGN`):

## Texture / bake contract
- bake required:
- BaseColor output:
- Normal output:
- ORM / packed channels:
- Emissive output:
- alpha/masks:
- padding/mip policy:
- high-to-low source required for which channels/features:
- runtime material binding validator:

A separate high-poly source is not required for every procedural-to-texture bake. Declare it only where geometry-detail transfer requires it.

Use `04_game_ready/50_GAME_READY_BAKE_GATE.md`.

## Emissive contract
- emitter feature IDs:
- geometry/mask authoring owner:
- Blender lookdev strength:
- exported emissive data:
- runtime bloom responsibility:
- runtime exposure/tone-mapping responsibility:
- actual scene-light contribution required:

Do not merge `emissive authoring PASS` with `runtime glow PASS`.
Use `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md`.

## Transform
- units:
- forward axis:
- up axis:
- pivot:
- applied transforms policy:

## Runtime
- static / movable:
- instanced:
- collision:
- occlusion:
- navmesh interaction:
- lightmap:
- shadow:
- animation:

## Export
- format:
- object root:
- naming:
- animation clips:
- external textures / embedded:
- validator:
- post-export material/texture reference validation:

## Project integration
- stable asset ID:
- destination namespace/path:
- catalog/registry required:
- catalog write capability:
- existing-asset conflict policy:
- importer/instantiation smoke test:

Use `09_engine/93_ASSET_CATALOG_INTEGRATION_PROTOCOL.md` when Level D is requested.

## Edytowalność

Źródłowy `.blend` nie powinien być tym samym, czym finalna "spłaszczona" wersja export.
Zachowaj authoring source.

## Completion rule

Successful glTF/mesh export alone does not prove `GAME_READY_COMPLETE`.

Before final claim run:
- mesh validation;
- bake/runtime material gate;
- emissive handoff gate if applicable;
- export validation;
- completion-level evaluation;
- catalog integration when Level D is required.


---

## FILE: `04_game_ready/41_POLYCOUNT_LOD_COLLISION_OCCLUSION.md`

# Polycount, LOD, Collision and Occlusion

## Polycount

Licz trójkąty, nie tylko quady/polygons.
Runtime rasteryzacyjny finalnie operuje na trójkątach.

## LOD

LOD powinien usuwać detal według kolejności:
1. niewidoczne mikrodetale,
2. małe bevel segments,
3. drobne recess,
4. elementy niezmieniające silhouette,
5. upraszczanie dużych zakrzywień dopiero później.

Każdy LOD powinien zachować:
- globalną sylwetkę,
- pivot,
- bounds,
- główne material regions.

## Collision

Collision mesh:
- prostszy niż render mesh,
- bez drobnych szczelin,
- zgodny z funkcją gameplay.

Nie twórz perfect collision, jeżeli gameplay tego nie potrzebuje.

## Occlusion

Dla dużych obiektów rozważ:
- rozdzielenie geometryczne umożliwiające culling,
- logiczne segmenty,
- bounding volumes.

## Instancing

Asset występujący setki razy wymaga ostrzejszego budżetu niż unikalny hero prop.


---

## FILE: `04_game_ready/42_PIVOTS_TRANSFORMS_UNITS_NAMING.md`

# Pivots, Transforms, Units and Naming

## Pivot

Pivot powinien wynikać z funkcji:
- mebel stojący: środek podstawy lub ustalony standard,
- drzwi: oś zawiasu,
- panel obrotowy: oś mechanizmu,
- moduł architektoniczny: punkt siatki montażowej.

Nie ustawiaj pivotu na geometry center automatycznie.

## Transform

Przed export:
- sprawdź location,
- rotation,
- scale,
- negative scale,
- parent transform.

Apply transforms tylko zgodnie z kontraktem.
Nie rób tego bezmyślnie, szczególnie w hierarchiach i rigach.

## Units

Jednostki Blendera i runtime muszą mieć jawne mapowanie.

## Naming

Proponowany schemat:
`<TYPE>_<SET>_<ASSET>_<PART>_<VARIANT>`

Przykłady:
- `SM_Lafar_Bench_Frame_A`
- `SM_Lafar_Bench_Seat_A`
- `COL_Lafar_Bench_A`
- `LOD1_Lafar_Bench_A`

## Zakaz `.001`

Finalny asset nie powinien zawierać przypadkowych nazw:
- Cube.001
- Material.003
- Boolean.017

Nazwy mają opisywać funkcję.


---

## FILE: `04_game_ready/43_TEXTURE_MATERIAL_RUNTIME.md`

# Texture and Material Runtime

## PBR portability

Jeżeli format docelowy opiera się na PBR metallic-roughness:
- mapuj materiał do tego modelu,
- sprawdź color space,
- sprawdź kanały packed textures,
- nie polegaj na Blender-only node graph.

## Normal maps

Sprawdź:
- tangent space,
- orientację,
- UV,
- zachowanie po triangulacji,
- zgodność z tangent basis runtime.

## Transparency

Transparency jest droższa i bardziej problematyczna niż opaque.
Używaj tylko, gdy design jej wymaga.

Rozróżniaj:
- opaque,
- alpha mask/cutout,
- alpha blend.

## Emissive

Emissive texture nie oznacza automatycznie realnego źródła światła w silniku.
To osobna decyzja runtime.

## Texture reuse

Preferuj:
- trim sheets,
- tileable materials,
- atlasy,
- współdzielone zestawy materiałów,

gdy zwiększa to wydajność bez utraty wizji.

## Bake

Bake jest wymagany, gdy authoring wykorzystuje efekt, którego runtime nie odtworzy bezpośrednio.


---

## FILE: `04_game_ready/44_ANIMATION_RIGGING.md`

# Animation and Rigging

## Czy asset wymaga rig?

Nie twórz armature dla prostego mechanicznego ruchu, jeżeli:
- hierarchia obiektów i transform animation wystarczy,
- silnik obsługuje animację node transforms.

Rig ma sens dla:
- deformacji,
- wielu zależnych elementów,
- skinned meshes,
- bardziej złożonych animacji.

## Mechanical animation

Dla drzwi, ekranów, uchwytów:
- poprawny pivot jest kluczowy,
- hierarchia powinna odzwierciedlać mechanikę,
- zakres ruchu powinien wynikać z konstrukcji.

## Clips

Każda animacja:
- ma nazwę,
- zakres klatek,
- stan początkowy/końcowy,
- loop flag na poziomie projektu,
- oczekiwany root transform.

## Export QA

Po eksporcie sprawdź:
- czy klipy istnieją,
- czy kości/nodes są poprawnie zmapowane,
- czy skala nie uległa zmianie,
- czy pivot/axis zachowują się poprawnie.


---

## FILE: `04_game_ready/45_GLTF_EXPORT.md`

# glTF / GLB Export Baseline

## Dlaczego glTF jako baseline

glTF 2.0 jest formatem runtime-oriented przeznaczonym do efektywnego przenoszenia:
- scen,
- hierarchy,
- meshes,
- materials,
- cameras,
- animations.

Biblioteka traktuje go jako domyślny kontrakt wymiany, jeśli silnik nie wymaga innego formatu.

## Coordinate system

Przed exportem zawsze sprawdź konwersję osi między Blenderem i runtime.

Specyfikacja glTF:
- right-handed,
- +Y up,
- +Z forward,
- jednostka długości: metr.

Nie zakładaj, że ustawienia eksportera i silnika są identyczne.

## Authoring vs runtime

glTF nie jest formatem authoringowym.
Nie zastępuje `.blend`.

## Export checklist

- prawidłowe root nodes,
- oczekiwane meshes,
- materiały,
- UV,
- normals/tangents,
- textures,
- animations,
- transforms,
- skinning,
- no accidental cameras/lights, jeśli niepotrzebne.

## Post-export validation

Nie kończ pracy na komunikacie "export successful".

Sprawdź wynik:
- importerem docelowego silnika,
- lub niezależnym glTF validator/viewer,
- porównaj bounds,
- material appearance,
- animation,
- hierarchy.

## Embedded vs external

GLB upraszcza pojedynczy plik.
Zewnętrzne zasoby mogą ułatwiać reuse/cache.
Wybór należy do pipeline projektu.


---

## FILE: `04_game_ready/46_DRAW_CALLS_INSTANCING_AND_BATCHING.md`

# Draw Calls, Instancing and Batching

## Geometry is not the only cost

Asset z małą liczbą trójkątów może być drogi, jeśli ma:
- wiele material slots,
- dużo transparency,
- dużo unikalnych textures,
- brak instancingu,
- nadmiernie rozdrobnioną hierarchię.

## Material slots

Każdy dodatkowy slot powinien mieć uzasadnienie shader/runtime.

## Instancing

Powtarzające się obiekty:
- powinny współdzielić mesh,
- najlepiej współdzielić materiały,
- mogą posiadać per-instance transform i ograniczony zestaw parametrów.

## Unique variation

Zamiast tworzyć 10 unikalnych mesh:
- materiał variation,
- decal variation,
- accessory variation,
- instanced add-ons.

## Batching caveat

Dokładny koszt zależy od silnika.
Biblioteka nie narzuca konkretnego draw-call target bez danych projektu.


---

## FILE: `04_game_ready/47_TEXTURE_PACKING_AND_MIP_SAFETY.md`

# Texture Packing and Mip Safety

## Channel packing

Jeżeli silnik wspiera packed masks:
- grupuj mapy jednokanałowe zgodnie z jednym projektem,
- dokumentuj dokładne mapowanie kanałów.

Przykład projektowy:
```text
R = AO
G = Roughness
B = Metallic
A = Custom Mask
```

To jest przykład, nie uniwersalny standard.

## Color space

Rozróżniaj:
- dane kolorystyczne,
- dane numeryczne/maski,
- normal maps.

Błędny color space zmienia dane.

## Mip safety

Małe wyspy UV i cienkie detale muszą mieć:
- odpowiedni padding,
- wystarczającą szerokość w texelach,
- zachowanie czytelności po mipmappingu.

## Resolution policy

Resolution wynika z:
- powierzchni assetu,
- texel density,
- dystansu kamery,
- importance class.

Nie wynika z zasady "hero = 4K" bez obliczenia.

## Atlas

Atlas pomaga redukować liczbę zasobów/material changes, ale:
- utrudnia niezależną zmianę resolution,
- może marnować miejsce,
- wymaga dobrego planowania paddingu.

## Compression

Finalny wygląd oceniaj również po kompresji docelowego silnika.


---

## FILE: `04_game_ready/48_ASSET_VARIANTS_AND_RANDOMIZATION.md`

# Asset Variants and Randomization

## Cel

Uzyskać różnorodność bez duplikowania całego kosztu assetu.

## Warstwy wariantów

### V0 — transform
- rotation,
- scale w dozwolonym zakresie.

### V1 — material
- kolor,
- roughness,
- decal set.

### V2 — accessories
- dodatkowy panel,
- uchwyt,
- ekran,
- osłona.

### V3 — structural
- rzeczywista zmiana geometrii.

Preferuj najniższą wystarczającą warstwę.

## Deterministic randomization

W proceduralnych zestawach:
- seed jawny,
- lista dozwolonych wariantów jawna,
- brak przypadkowych zmian wpływających na gameplay clearances.

## Shared core

Warianty powinny współdzielić:
- core mesh tam, gdzie możliwe,
- materiały,
- trim sheets,
- atlas,
- collision, jeśli geometria funkcjonalna się nie zmienia.

## QA

Wariant nie może:
- naruszać bounding/clearance contract,
- usuwać feature MUST wspólnego dla rodziny,
- tworzyć konfliktów material/runtime.


---

## FILE: `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md`

# Emissive Authoring and Runtime Handoff

## Purpose

An emissive strip has two separate responsibilities:

```text
ASSET AUTHORING
geometry + mask + color + material segmentation

RUNTIME PRESENTATION
bloom + exposure + tone mapping + scene-light contribution
```

Do not confuse them.

A Blender preview can prove the emissive feature exists and is correctly authored. It cannot prove the target game runtime will produce the same glow unless the Engine Profile and runtime post-process are known.

---

# Asset-side responsibilities

The Blender/game asset must define:
- exact emitting region;
- diffuser/cover geometry if present in the reference;
- emissive mask or material region;
- intended emissive color in a documented color space;
- relative strength class (`SUBTLE`, `GUIDANCE`, `SIGNAGE`, `HIGH_INTENSITY` or project-specific equivalent);
- whether the material should visibly glow when unlit;
- whether actual scene illumination is required or only self-emission.

The emitting region must pass visibility QA.

An emissive object hidden behind host geometry is a geometry failure, even if its material node reports a non-zero emission strength.

---

# Blender lookdev responsibility

Blender preview is used to validate:
- the band/marker is visible in the intended views;
- its hue survives color management;
- the feature is not clipped to featureless white under the QA rig;
- surrounding material does not become artificially recolored in base color;
- the emitter does not compensate for wrong geometry.

The preview strength is a **lookdev parameter**, not automatically a runtime constant.

Record it as:

```yaml
emissive_authoring:
  feature_id: F007
  color_rgb: [0.055, 0.517, 1.0]
  blender_strength: 2.4
  purpose: GUIDANCE
  visibility: PASS
  clipping: PASS
```

---

# Runtime responsibility

Final glow can depend on:
- bloom/post-processing;
- exposure;
- tone mapping;
- HDR range;
- emissive shader implementation;
- whether emissive contributes to indirect/direct scene lighting;
- temporal AA/upscaling;
- distance and screen size.

Therefore:

```text
EMISSIVE_AUTHORING_PASS != RUNTIME_GLOW_PASS
```

If runtime behavior is unknown, mark:

```yaml
runtime_emissive:
  status: UNVERIFIED
  reason: ENGINE_PROFILE_OR_POSTPROCESS_UNKNOWN
```

---

# Bloom policy

Do not bake bloom halos into BaseColor or Emissive textures unless the art direction explicitly requires a stylized painted halo.

Normally:
- texture/mask describes the emitter;
- runtime bloom generates the optical/post-process halo.

This preserves correct response across distance, exposure and lighting conditions.

---

# Color preservation

A blue/cyan guidance light that turns white in the QA render is not automatically acceptable.

Diagnose in this order:
1. emission strength;
2. exposure/tone mapping;
3. QA light rig;
4. material color;
5. runtime bloom only after authoring values are stable.

Do not solve clipping by making the geometry larger unless the reference supports larger geometry.

---

# LOD behavior

An emissive feature may be visually important at distances where its physical housing is sub-pixel.

LOD policy may therefore separate:
- `EMITTER_SIGNAL` — preserve color/visibility;
- `EMITTER_HOUSING` — simplify/remove with distance.

At low LOD, a simple emissive band can replace detailed diffuser geometry if the protected silhouette and visual identity remain correct.

---

# Game-ready gate

Before `GAME_READY_COMPLETE`:
- emissive texture/material export is verified;
- exported asset actually references the emissive data;
- Engine Profile states how emissive is interpreted, or runtime remains `UNVERIFIED`;
- no Blender-only node behavior is silently assumed to survive export.

If the project requires bloom/light contribution but these runtime settings are not under Blender control, the asset may still pass authoring while pipeline integration remains pending.


---

## FILE: `04_game_ready/50_GAME_READY_BAKE_GATE.md`

# Game-Ready Texture Bake Gate

## Purpose

A Blender material that looks correct is not automatically a runtime material.

Before claiming `GAME_READY_COMPLETE`, every Blender-only material effect must have an explicit runtime disposition:

```text
BAKE
RECREATE_IN_ENGINE
EXPORT_NATIVELY_VERIFIED
REMOVE_BY_DESIGN
```

No effect may remain in an undefined state.

For actual bake execution use:
- `04_game_ready/51_BAKE_EXECUTION_AND_CHANNEL_SEMANTICS.md`;
- `04_game_ready/52_UV_ATLAS_LOD_STABILITY_CONTRACT.md`;
- `08_scripts/93_BAKE_OUTPUT_VALIDATION_PATTERN.md`;
- `05_execution/65_INCREMENTAL_DIRTY_STAGE_CACHE.md`.

The gate defines **what must be true**. The v0.6 execution layer defines **how the agent performs and proves it efficiently**.

---

# Important correction

A separate high-poly mesh is **not required for every bake**.

Different bake purposes have different source requirements.

### Procedural/material bake
Can bake directly from the authoring material/mesh when the purpose is to convert Blender procedural information into textures, for example:
- BaseColor variation;
- roughness breakup;
- emissive masks;
- procedural dirt/wear;
- tile/detail masks;
- procedural micro-normal/bump detail.

### High-to-low geometry bake
Requires an appropriate source surface when transferring geometric detail, for example:
- high-poly normal detail;
- curvature/AO dependent on high-resolution geometry;
- sculpted wear;
- recessed seams/fasteners moved from geometry to normal maps.

Do not block all texture baking merely because a separate high-poly object does not exist.

---

# Bake decision matrix

For every surface feature record:

```yaml
surface_feature:
  id: MAT_DETAIL_03
  description: fine powder-coat roughness variation
  authoring_source: PROCEDURAL_SHADER
  runtime_strategy: BAKE
  target_channel: ORM.G
  required_resolution: 1024
```

Common outputs:
- BaseColor;
- Normal;
- ORM or project-specific packed channels;
- Emissive;
- Alpha/masks when required.

The Engine Profile defines actual packing and color-space requirements.

---

# Bake preconditions

Before bake:
- final/approved low mesh exists;
- UV contract is explicit and validated;
- runtime LODs that share textures declare the same `UV_CONTRACT_ID`;
- texel density tradeoff is accepted;
- intended overlaps are documented;
- tangent/normal strategy is known;
- material segmentation is stable;
- output resolution/padding are defined;
- external UV owners such as decals/dynamic displays are identified;
- high-to-low source/cage exists when the requested channel requires it;
- runtime scene has an isolation plan for AO/ray-dependent passes.

Do not bake before silhouette and primary geometry are accepted.

Missing UV atlas assignment is FAIL. Do not silently continue.

---

# Channel semantics are part of the gate

The bake must preserve the **authored runtime property**, not merely produce a plausible image.

Examples:
- metallic BaseColor must not be inferred from a DIFFUSE response that can be black for metal;
- metallic scalar must not become 1.0 across unrelated dielectric regions;
- non-emitting materials must remain black in Emissive even if their Principled emission color default is non-black;
- authoring emission strength must not clip texture RGB and destroy hue;
- AO must not be contaminated by unrelated render-visible helper geometry.

Use the v0.6 channel semantics protocol.

---

# Operator success gate

A bake call is PASS only if:
1. all contributing material slots have the correct selected+active target image node;
2. the bake operator returns `FINISHED`;
3. the output image passes semantic validation.

No Python exception is **not** sufficient evidence.

`{'CANCELLED'}` is FAIL.

---

# Civic hard-surface finishing

For dark civic/game props, the bake gate should explicitly consider whether runtime needs:
- broad low-frequency roughness variation;
- subtle micro-normal breakup;
- restrained dirt accumulation at protected joints/base interfaces;
- sparse wear on contact/maintenance edges;
- brushed directionality for metal;
- decal/signage alpha or color;
- emissive mask.

A perfectly uniform roughness field is usually a deliberate material decision, not a default.

Do not add random grunge everywhere. Variation must follow material/manufacturing/exposure logic.

---

# Geometry-to-normal transfer decision

A small feature may leave LOD0 geometry and become texture detail at lower LOD or final runtime if:
- it does not materially affect protected silhouette;
- parallax is not required at expected viewing distance;
- normal-map representation survives mip reduction;
- the feature remains recognizable where required.

Examples:
- fine vertical seams;
- tiny panel fasteners;
- shallow service markings;
- micro wear.

Do not bake away a reference-critical deep recess or silhouette break merely to hit a triangle target.

---

# Incremental execution

Bake is multi-artifact work.

Do not rebake accepted channels after a local repair unless a dependency changed.

Examples:

```text
AO isolation fix -> AO + packed ORM dirty
Emissive normalization fix -> Emissive dirty
UV contract fix -> all channels using that UV set dirty
```

Use the Dirty-Stage Cache and record reused vs recomputed channels.

---

# Validation

Required checks depend on outputs, but normally include:
- no missing islands/semantic parts;
- no unintended projection bleed;
- padding/mip safety;
- normal orientation/tangent consistency;
- correct color-space treatment;
- channel packing matches Engine Profile;
- material-family region expectations;
- emissive mask aligns with emitting geometry/UV regions;
- no unexplained all-zero/all-one/constant maps;
- exported runtime material references produced textures;
- baked runtime mesh/material visually passes QA.

A texture file existing on disk is not sufficient evidence.

Use `BAKE_VALIDATE` where available.

---

# Runtime package closure

The bake gate is not complete at image generation.

Required closure:

```text
baked images PASS
-> runtime material binding PASS
-> runtime LOD UV contract PASS
-> export PASS
-> exported material/image readback PASS
-> baked-runtime QA PASS
```

If project packaging has specific LOD/handedness/material rules, apply `09_engine/94_RUNTIME_MODULE_PACKAGING_CONTRACT.md`.

---

# Gate result

```yaml
bake_gate:
  uv_contract: PASS
  operator_binding: PASS
  basecolor: PASS
  normal: PASS
  orm:
    ao: PASS
    roughness: PASS
    metallic: PASS
  emissive: PASS
  runtime_material_binding: PASS
  export_readback: PASS
  baked_runtime_qa: PASS
  reused_channels: []
  recomputed_channels: []
  status: PASS
```

If procedural materials are still Blender-only and no verified runtime replacement exists:

```text
GAME_READY_COMPLETE = FAIL
reason = BLENDER_ONLY_MATERIAL_STATE
```

---

# Skip conditions

Bake may be skipped only if one of these is proven:
- target engine natively recreates the intended material through a validated pipeline;
- the material is intentionally constant/simple and needs no texture data;
- requested completion level stops before game-ready runtime material production.

Record the reason. Never silently skip bake because Blender viewport already looks good.


---

## FILE: `04_game_ready/51_BAKE_EXECUTION_AND_CHANNEL_SEMANTICS.md`

# Runtime Bake Execution and Channel Semantics

## Purpose

`BAKE_RUNTIME_TEXTURES` must be a deterministic production stage, not an ad-hoc sequence of Blender operator experiments.

A correct-looking Blender material is not evidence that the runtime textures are correct. A texture file existing on disk is not evidence that the bake succeeded.

Use this transaction:

```text
PRECHECK
-> UV CONTRACT
-> SOURCE/MATERIAL CONTRACT
-> SCENE ISOLATION
-> TARGET IMAGE BINDING
-> CHANNEL BAKE
-> IMAGE VALIDATION
-> RUNTIME MATERIAL BINDING
-> EXPORTED-ASSET READBACK
```

Every stage must return a compact PASS/FAIL report.

---

# 1. Operator result is evidence

Never assume `bpy.ops.object.bake(...)` succeeded merely because no Python exception was raised.

Required:

```python
result = bpy.ops.object.bake(type=bake_type)
if "FINISHED" not in result:
    raise RuntimeError(f"Bake failed: {result}")
```

`{'CANCELLED'}` is FAIL.

A Blender info/warning such as:

```text
No active and selected image texture node found in material ...
```

must route to `BAKE_TARGET_BINDING_FAIL`, not to another blind full bake.

---

# 2. Target image node contract

For a joined/source object using multiple material slots, the target image must be active and selected in every material that contributes faces to the bake.

Use the explicit order:

```text
create/reuse ShaderNodeTexImage
-> assign target image
-> deselect all material nodes
-> select the target image node
-> set it as active
-> verify active == target AND target.select == true
```

Do not rely on setting `nodes.active` before selection and assuming selection state will remain correct.

Before calling the operator, emit only a compact binding report:

```yaml
bake_target_binding:
  materials_required: 5
  materials_bound: 5
  image: aster_bollard_basecolor
  status: PASS
```

---

# 3. Scene isolation is mandatory for environment-sensitive passes

AO and other ray-dependent passes are invalid if unrelated scene geometry can occlude the bake source.

Typical trap:
- object has `hide_viewport=true`;
- object has `hide_render=false`;
- AO rays hit it even though the agent does not see it in the viewport.

Before AO/ray-dependent bake:
- isolate the bake source non-destructively;
- use `QA_SCENE_ISOLATE` or equivalent registered executor;
- preserve and restore `hide_render` state;
- do not delete unrelated scene objects.

The default Cube, test geometry, reference planes and helper meshes must not influence AO unless explicitly part of the bake contract.

---

# 4. Channel semantics

## BaseColor

For metallic-roughness runtime pipelines, do not use the Blender `DIFFUSE` bake as a generic BaseColor extractor.

A metal can have little/no diffuse response while its Principled `Base Color` still carries the runtime metal reflectance color.

Preferred procedural-material closure:

```text
Principled Base Color socket
-> temporary Emission output, strength 1
-> EMIT bake
-> BaseColor texture
```

This captures the authored Base Color value/graph rather than lighting or diffuse response.

## Roughness

Bake the authored roughness signal, not a rendered highlight.

Use either:
- a verified Roughness pass;
- or direct socket/channel override to an emission bake when exact authored-value transfer is required.

## Metallic

Metallic is a scalar material property.

For deterministic authored-value transfer:

```text
Principled Metallic socket
-> grayscale temporary Emission
-> EMIT bake
-> pack into the Engine Profile's metallic channel
```

Do not assume a dedicated bake pass exists in every runtime/API version.

## AO

AO is geometry/environment dependent.

Requirements:
- isolated source scene;
- known distance/samples;
- output validated for non-degenerate range;
- no unrelated render-visible enclosure.

## Normal

Normal bake must document:
- tangent-space vs object-space;
- tangent basis expectation;
- authoring bump/procedural normal source;
- whether geometry detail is being transferred high->low.

A material-only normal bake does not require a separate high-poly when the source detail is procedural shader/bump information.

## Emissive

The emissive texture describes **where and what color the emitter is**, not final bloom.

Do not bake bloom, glare or post-process response.

Non-emitting materials must produce black emissive output.

If Principled uses both `Emission Color` and `Emission Strength`, the bake must account for both. Baking color alone is unsafe because non-emitting materials may still have a non-black default emission color with strength zero.

Recommended normalized representation:

```text
emissive_texture_rgb = emission_color * emission_strength / EMIT_REFERENCE_STRENGTH
```

where `EMIT_REFERENCE_STRENGTH` is an explicit authoring/runtime handoff value.

Validate that normalization does not clip channels and destroy hue.

---

# 5. Decals and foreign UV spaces

Do not automatically join permanent decal geometry into the structural bake source.

If a decal uses:
- a separate atlas;
- shared project branding sheet;
- dynamic display UV;
- different sampling/material pipeline;

keep it outside the structural bake unless the bake contract explicitly remaps it.

A decal with unrelated UV coordinates can silently contaminate structural atlas regions.

---

# 6. UV contract before bake

The bake source and every runtime LOD that consumes the baked maps must use the same `UV_CONTRACT_ID`.

Before baking, validate:
- every required semantic part has an atlas assignment;
- no required assignment was skipped because Blender added `.001`/`.002` to an object name;
- LOD runtime meshes actually received the same contract, not only the temporary bake source;
- intentional overlaps are declared;
- decal/dynamic-display UV spaces are excluded where appropriate.

Use `04_game_ready/52_UV_ATLAS_LOD_STABILITY_CONTRACT.md`.

---

# 7. Incremental bake rule

Do not rebake every channel after every local repair.

Maintain dirty dependencies.

Examples:

```text
emission normalization changed
-> dirty: Emissive only

Base Color graph changed
-> dirty: BaseColor only, plus any packed channel explicitly depending on it

AO scene isolation changed
-> dirty: AO / ORM.R only

UV contract changed
-> dirty: all texture channels using that UV set

mesh geometry changed
-> dirty: AO, Normal, and any geometry-position-driven procedural channels;
   BaseColor/Roughness only if their authoring graph depends on geometry/object coordinates
```

Use `05_execution/65_INCREMENTAL_DIRTY_STAGE_CACHE.md`.

---

# 8. Validation before export

Every baked map must pass semantic validation before runtime material assembly.

Minimum checks:
- file/image exists;
- expected dimensions;
- expected color space;
- not all zero unless channel contract permits it;
- not unexpectedly constant;
- channel-specific range is plausible;
- expected material/feature regions contain signal;
- forbidden regions do not contain signal beyond configured padding/bleed;
- no unexplained clipping;
- map is bound to the intended runtime material.

Use `08_scripts/93_BAKE_OUTPUT_VALIDATION_PATTERN.md` and packaged validator when available.

---

# 9. Exported runtime asset is the final bake QA target

After binding baked textures, render/inspect the runtime mesh/material combination — not only the authoring procedural material.

Required final proof:

```text
baked textures
-> runtime material
-> runtime LOD0 mesh UV
-> export
-> exported material/image readback
-> baked-runtime QA render / smoke test
```

A correct authoring render with a broken baked-runtime material is FAIL.

---

# 10. Long-running bake behavior

A tool/MCP timeout is not proof that Blender stopped the bake.

Before retrying an expensive pass:
1. inspect job state if available;
2. inspect output image/file timestamps;
3. inspect Blender state;
4. only restart if the previous execution is proven failed/stopped.

Never launch duplicate AO/full bakes merely because the transport call timed out.

Use `05_execution/64_LONG_RUNNING_JOB_AND_POLL_PROTOCOL.md`.

---

# Compact completion report

```yaml
runtime_bake:
  uv_contract: PASS
  source_isolation: PASS
  basecolor: PASS
  normal: PASS
  orm:
    ao: PASS
    roughness: PASS
    metallic: PASS
  emissive: PASS
  runtime_material_binding: PASS
  exported_texture_readback: PASS
  baked_runtime_qa: PASS
  channels_rebaked_this_iteration:
    - emissive
  status: PASS
```

Do not return raw pixel arrays or complete shader graphs unless a scoped diagnostic explicitly requires them.


---

## FILE: `04_game_ready/52_UV_ATLAS_LOD_STABILITY_CONTRACT.md`

# UV Atlas and LOD Stability Contract

## Purpose

A baked runtime texture is useful only if the bake source and every runtime mesh sample the same semantic UV layout.

This contract prevents a common silent failure:

```text
bake source uses correct atlas
runtime LODs keep raw/default UVs
-> exported model reads valid textures through wrong coordinates
```

It also prevents object-name suffixes such as `.001` from silently breaking atlas assignment.

---

# 1. Stable semantic part identity

Do not use transient Blender object names as the primary UV atlas key.

Bad:

```python
UV_RECTS.get(obj.name)
```

because Blender may rename duplicates:

```text
BOL_MainBody
BOL_MainBody.001
BOL_MainBody.002
```

Preferred identity:

```text
semantic_part_id = BODY_MAIN
uv_contract_id = ACS_BOLLARD_V1
```

Store identity in:
- explicit build data;
- custom property;
- Feature Contract / object registry;
- another deterministic semantic identifier.

Name normalization may be used as a compatibility fallback, but it must emit a warning and must not be the canonical identity mechanism.

---

# 2. UV contract data model

Example:

```yaml
uv_contract:
  id: ACS_BOLLARD_V1
  texture_size: 1024
  padding_px: 16
  parts:
    BODY_MAIN:
      rect: [0.00, 0.00, 1.00, 0.46]
      owner: STRUCTURAL_ATLAS
    BASE_PLATE:
      rect: [0.00, 0.56, 1.00, 0.76]
      owner: STRUCTURAL_ATLAS
    BRAND_DECAL:
      owner: PROJECT_DECAL_ATLAS
      external: true
    DISPLAY_DYNAMIC:
      owner: DYNAMIC_SCREEN
      dedicated_uv_0_1: true
```

Every runtime mesh part must resolve to exactly one declared UV owner.

---

# 3. One contract across bake source and LODs

Atlas assignment belongs in the reusable mesh/LOD construction path, not only in the bake script.

Required:

```text
build part
-> assign semantic part ID
-> assign/validate UV contract
-> construct bake source OR runtime LOD
```

Do not implement:

```text
build runtime LODs with default UV
build second bake source
apply atlas only to bake source
```

That pipeline can produce perfect textures and a broken exported model.

---

# 4. Missing assignment is a hard failure

Never silently skip a part when no atlas record is found.

Required behavior:

```yaml
uv_contract_validation:
  required_parts: 9
  assigned_parts: 8
  missing:
    - BODY_MAIN
  status: FAIL
```

Do not continue to bake/export.

---

# 5. Lower LOD behavior

A lower LOD may omit a semantic part, but remaining parts must retain their UV ownership and contract.

Example:

```text
LOD0: BODY + BASE + PANEL + BOLTS + EMITTER
LOD1: BODY + BASE + PANEL + EMITTER
LOD2: BODY + BASE + EMITTER
```

The removal of `BOLTS` must not cause surviving parts to be repacked into new atlas regions if all LODs are expected to share the same texture set.

If LOD-specific repacking is intentionally used, it becomes a different `UV_CONTRACT_ID` and requires its own texture/binding strategy.

---

# 6. Semantic correspondence

Simply normalizing arbitrary existing UV bounds into the same rectangle does not always guarantee meaningful correspondence between LODs.

For procedural/parametric assets prefer UV generation from stable geometric parameters:
- revolution angle + profile distance;
- local planar coordinates;
- normalized part coordinates;
- explicit seam/axis rules.

This lets different segment counts sample corresponding locations.

A generic min/max remap may be acceptable only when the distortion and cross-LOD correspondence have been validated for that part class.

---

# 7. Dedicated spaces must remain dedicated

Do not mix these into the structural bake atlas unless explicitly required:
- shared project decal atlas;
- logo atlas;
- dynamic display surface;
- video/render-target surface;
- externally tiled materials;
- lightmap UV.

Dynamic displays normally require their own deterministic full `0..1` UV space.

---

# 8. Padding and edge bleed

Atlas rectangles must reserve sufficient padding for:
- bake margin;
- mip filtering;
- compression;
- bilinear sampling.

Record padding in pixels and derive normalized gutter from texture resolution.

Do not let bake margin cross semantic part boundaries.

---

# 9. Texel density

Fixed atlas regions may intentionally have unequal texel density.

This is acceptable when documented and driven by:
- projected size;
- visual importance;
- repeated placement frequency;
- reference detail density;
- runtime budget.

Do not pretend a 1024 atlas can maintain impossible uniform density on a very tall/long asset.

Record the tradeoff explicitly.

---

# 10. Validation

Before bake:
- unique contract ID;
- all required part IDs resolved;
- no undeclared rect overlap;
- rects inside 0..1;
- padding sufficient;
- dedicated/external UV owners excluded from structural atlas;
- runtime LOD meshes report same contract ID.

After export:
- read back UV set presence;
- verify expected material/texture binding;
- render/inspect baked runtime LOD0;
- sample at least one known region per material family when debugging.

---

# Compact report

```yaml
uv_contract:
  id: ACS_BOLLARD_V1
  texture_size: 1024
  required_parts: 9
  assigned_parts: 9
  external_parts:
    - BRAND_DECAL
  lods:
    LOD0: PASS
    LOD1: PASS
    LOD2: PASS
    LOD3: PASS
  rect_overlap: PASS
  padding: PASS
  status: PASS
```


---

## FILE: `05_execution/50_BUILD_PLAN_TEMPLATE.md`

# Build Plan Template

## Asset
Name:
Version:
Reference:
Target Blender:
Runtime profile:

## A. Feature Contract
Wklej listę `MUST`, `SHOULD`, `OPTIONAL`.

## B. Object decomposition

| Object | Purpose | Primitive/source | Symmetry | Material | Animated |
|---|---|---|---|---|---|

## C. Modeling strategy

Dla każdej części:
- technique:
- base primitive:
- modifiers:
- booleans:
- expected topology:
- feature IDs:

## D. Parameters

```text
WIDTH =
DEPTH =
HEIGHT =
THICKNESS =
BEVEL_MAIN =
BEVEL_DETAIL =
GAP =
```

## E. Execution phases

### Phase 1 — blockout
Affected objects:
Expected output:
Checkpoint:

### Phase 2 — primary details
Affected objects:
Feature IDs:
Checkpoint:

### Phase 3 — secondary details
Affected objects:
Feature IDs:
Checkpoint:

### Phase 4 — UV/material
Checkpoint:

### Phase 5 — game-ready
Checkpoint:

## F. Risks

| Risk | Probability | Impact | Mitigation |
|---|---:|---:|---|

## G. Exit criteria

Asset jest gotowy, gdy:
- [ ] all MUST features pass
- [ ] proportions pass
- [ ] shading pass
- [ ] UV/material pass
- [ ] runtime contract pass
- [ ] export pass


---

## FILE: `05_execution/51_EXECUTION_PROTOCOL.md`

# Execution Protocol

## 0. Runtime capability preflight

Before the first production mutation in a session:
- load `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`;
- discover current connected tools;
- build/reuse Tool Registry;
- bind capabilities according to `02_blender_api/28_AGENT_TOOL_API_PROFILE.md`;
- require at least `scene_inspect=BOUND` and `python_execute=BOUND` for autonomous mesh mutation;
- record any missing capability as a blocker instead of guessing an unavailable tool.

Do not repeat capability discovery before every feature unless the binding becomes invalid.

## 1. Preflight

- odczytaj Scene Snapshot,
- sprawdź Blender version,
- sprawdź jednostki,
- sprawdź, czy asset już istnieje,
- sprawdź Feature Contract,
- sprawdź Build Plan,
- wybierz `SELECTED SKILL ID` dla operacji, jeśli istnieje zarejestrowany semantic skill,
- sprawdź wymagane capabilities wybranego skilla,
- sprawdź `executors/` zanim wygenerujesz lokalny helper dla zarejestrowanej operacji.

## 2. Create asset root

Utwórz lub znajdź:
- collection assetu,
- root object/empty, jeśli pipeline tego wymaga,
- naming namespace.

## 3. Build by phase

Każdy phase:
1. loguje start,
2. wykonuje spójny batch,
3. aktualizuje scenę,
4. wykonuje postcondition,
5. zapisuje status feature IDs,
6. uruchamia checkpoint.

Jeżeli faza wymaga większego skryptu, stosuj `05_execution/62_CODE_ARTIFACT_AND_PATCH_PROTOCOL.md`: kod jest artefaktem na dysku, a nie pełnym tekstem przenoszonym przez kontekst po każdym wywołaniu.

## 4. Postcondition examples

Po stworzeniu blockoutu:
- obiekt istnieje,
- dimensions są zgodne,
- scale jest oczekiwana,
- liczba części się zgadza.

Po boolean:
- modifier/rezultat istnieje,
- nie zniknęły faces z innej strefy,
- bounds nie zmieniły się poza tolerancją.

Po bevel:
- width zgodny,
- segment count zgodny,
- brak self-overlap.

Po semantic skill operation:
- skill-specific validation report exists,
- feature ownership remains valid,
- previously accepted MUST features have not regressed.

Po mesh validation:
- każdy mesh ma jawny `topology_intent`;
- `MESH_VALIDATE` nie raportuje ogólnego PASS, jeśli obiekt nie ma kontraktu topology intent;
- boundary/non-manifold są interpretowane zgodnie z kontraktem, nie ignorowane globalnie.

## 5. Checkpoint

Nie kontynuuj, jeśli checkpoint FAIL.

## 6. Save

Zapisuj:
- przed ryzykownym Apply,
- po zaakceptowanym dużym etapie,
- przed exportem,
- przed strategy switch, jeżeli nowa strategia może istotnie zmienić topologię.

Dla wygenerowanych skryptów zapisuj ścieżkę i ostatni pomyślny status zamiast powtarzać pełną treść kodu w logu.

## 7. No silent repair

Jeżeli wykonanie różni się od planu, zapisz to jako deviation.
Nie zmieniaj strategii po cichu.

Nie zmieniaj geometrii wyłącznie po to, aby detal był bardziej widoczny w jednym QA lighting setup. Najpierw rozstrzygnij, czy problem dotyczy geometrii, materiału, oświetlenia czy kamery.

## 8. Retry budget

Obowiązuje `05_execution/61_RETRY_BUDGET_AND_STRATEGY_SWITCH.md`.

Ta sama operacja z tą samą strategią i tymi samymi preconditions może zostać wykonana maksymalnie dwa razy łącznie:
- pierwsza próba,
- jedna poprawiona próba po diagnostyce.

Po drugiej porażce:
- zatrzymaj ten call pattern,
- wykonaj re-inspection,
- sklasyfikuj failure,
- przywróć checkpoint, jeśli scena została uszkodzona,
- zmień strategię lub zgłoś blocker.

Każdy retry musi wynikać z nowej informacji albo jawnej zmiany zwalidowanego precondition.


---

## FILE: `05_execution/52_CHECKPOINT_AND_VISUAL_QA.md`

# Checkpoint and Visual QA

## QA scene isolation preflight

Before rendering a checkpoint:
- identify the asset collection/root;
- identify the QA rig collection;
- temporarily exclude unrelated renderable objects/lights that are not part of the intended QA setup;
- preserve and restore their previous `hide_render`/collection visibility state;
- do not delete user objects to obtain a clean QA render.

Viewport visibility is not proof of render visibility. An object can be hidden in viewport and still appear in render.

## Minimalny zestaw widoków

Dla statycznego prop:
- front ortho,
- side ortho,
- top ortho,
- 3/4 perspective.

Jeżeli geometria ma znaczenie z innych stron:
- rear,
- bottom.

For a reference-driven asset, add feature-specific close-up ROI views only when the wide views cannot validate a MUST feature.

## Tryby kontroli

### Silhouette
Jednolity ciemny materiał / maska.
Cel: ocenić tylko obrys.

### Neutral shaded
Szary PBR.
Cel: forma i highlight.

### Matcap
Cel: wykrywanie falowania i shading artefacts.

### Wireframe
Cel: topologia i gęstość.

### Material preview
Cel: materiały, UV i texture direction.

## Geometry/material separation

Do not use a MATERIAL/HERO render as the first proof of geometric correctness.

Order:

```text
SILHOUETTE / ORTHO NUMERIC
-> NEUTRAL / MATCAP FORM
-> MATERIAL
-> HERO
```

If a detail is difficult to see in one material/lighting render:
1. test it in neutral geometry QA;
2. inspect reference evidence and dimensions;
3. determine whether the cause is geometry, lighting, material or camera;
4. modify geometry only if geometric evidence supports the change.

Do not increase panel relief, bevel width, groove depth or feature size merely to make it visible under a particular QA lighting setup.

## Visible feature proof

For a feature whose contract says it must be visible, object existence is insufficient.

Accept one or more of:
- expected pixels detected in the feature ROI;
- silhouette/neutral render shows the feature;
- ray/occlusion test proves it is outside the host surface and visible from required view;
- geometric host/detail offset is validated along the correct normal.

This applies especially to floating panels, local emissive accents and decals/floaters.

## Checkpoint C1 — Blockout
Oceniaj:
- bounds,
- proporcje,
- osie,
- negative spaces,
- primary silhouette.

Nie oceniaj tekstur.

## Checkpoint C2 — Primary details
Oceniaj wszystkie `MUST`.

## Checkpoint C3 — Shading
Oceniaj:
- bevel,
- normals,
- smooth transitions,
- boolean artifacts.

## Checkpoint C4 — Runtime
Oceniaj:
- LOD,
- collision,
- pivot,
- material count,
- texture use,
- topology contract through `MESH_VALIDATE`.

## Difference score

Dla każdej cechy:
- PASS,
- MINOR,
- FAIL.

`MUST + FAIL` = asset nie może przejść dalej.

A checkpoint summary should contain compact metrics and failing feature IDs, not raw pixel/profile dumps.


---

## FILE: `05_execution/53_FINAL_VALIDATION.md`

# Final Validation

Final Validation must prove the requested completion level, not only that the Blender scene renders.

Use `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md` and finish with `05_execution/63_REFERENCE_TO_RUNTIME_COMPLETENESS_REPORT.md`.

## Visual / reconstruction

- [ ] silhouette matches
- [ ] proportions within tolerance
- [ ] all MUST features visible
- [ ] no invented major details
- [ ] no missing characteristic recess/groove/cut
- [ ] material regions match design
- [ ] asymmetry preserved where required
- [ ] floating/additive features are actually visible and not hidden by host geometry
- [ ] lighting/material readability did not force unauthorized geometry changes

## Mesh

- [ ] every mesh has declared topology intent
- [ ] `MESH_VALIDATE` or equivalent contract-aware audit passes
- [ ] no unintended duplicate geometry
- [ ] boundary/non-manifold state matches topology intent
- [ ] face normals correct
- [ ] no accidental zero-area geometry
- [ ] no loose vertices/edges
- [ ] no uncontrolled shading artifacts
- [ ] triangle count documented

## Modifiers / generated code

- [ ] stack intentional
- [ ] no disabled forgotten modifiers
- [ ] no accidental duplicate modifiers
- [ ] apply state follows pipeline
- [ ] reusable builder modules have no destructive import-time side effects
- [ ] generated code is persisted as an artifact, not dependent on conversation reconstruction

## UV / material authoring

- [ ] UV layers named
- [ ] overlap intentional
- [ ] texel density acceptable
- [ ] material slots within budget
- [ ] supplied authoritative branding source used where required
- [ ] material breakup follows material/manufacturing logic rather than uniform generic noise
- [ ] dark/civic materials are checked for sterile-uniform and over-grunged failure modes

## Bake / runtime texture gate

Required for Level C when runtime textures are part of the contract:

- [ ] every Blender-only procedural effect has runtime disposition
- [ ] required BaseColor exists
- [ ] required Normal exists
- [ ] required ORM/packed map exists
- [ ] required Emissive exists
- [ ] padding/mip safety passes
- [ ] tangent/normal transfer is correct
- [ ] packed channels match Engine Profile
- [ ] exported runtime material actually references produced textures

Use `04_game_ready/50_GAME_READY_BAKE_GATE.md`.

A separate high-poly mesh is required only for transfers that actually need a high-detail source.

## Emissive

If emissive features exist:

- [ ] emitter geometry/mask is correct
- [ ] emitter visibility passes
- [ ] intended hue survives Blender lookdev
- [ ] exported emissive data survives
- [ ] runtime bloom/exposure/tone-mapping responsibility is documented
- [ ] final runtime glow is PASS or explicitly `UNVERIFIED`

Use `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md`.

## Scene

- [ ] naming clean
- [ ] no Cube.001 style leftovers
- [ ] unrelated scene objects cannot contaminate QA renders
- [ ] helper objects hidden/removed according to policy
- [ ] collection structure clean
- [ ] pivot correct
- [ ] transforms correct
- [ ] project root/path source is stable even for unsaved `.blend` sessions

## Game-ready

- [ ] LOD budgets correct
- [ ] collision correct
- [ ] instancing/reuse considered
- [ ] runtime bounds correct
- [ ] export tested
- [ ] exported decal/material/texture references validated
- [ ] protected reconstruction features survive optimization

## Pipeline integration — Level D only

- [ ] stable project asset ID
- [ ] no unintended overwrite/name collision
- [ ] asset catalog/registry entry written
- [ ] LOD/collision/texture associations correct
- [ ] catalog entry read back successfully
- [ ] importer/instantiation smoke test passes when available

Use `09_engine/93_ASSET_CATALOG_INTEGRATION_PROTOCOL.md`.

## Deliverables

Depending on target level:

- [ ] source `.blend`
- [ ] build/code artifacts required for reproducibility
- [ ] runtime mesh export
- [ ] textures
- [ ] collision
- [ ] validation report
- [ ] completeness report
- [ ] catalog/registry integration record when Level D is required

## Final claim

Before saying `DONE`:
1. run `ASSET_COMPLETION`;
2. emit highest passed completion level;
3. list blockers/deferred items;
4. only use unconditional `DONE` if `TARGET_COMPLETION_LEVEL` passes.

Example:

```text
MODELING_COMPLETE: PASS
GAME_READY_COMPLETE: FAIL — PBR_BAKE_NOT_DONE
PIPELINE_INTEGRATED: NOT_REQUIRED
```

This is not a fully game-ready asset yet, even if the Blender model and glTF mesh look correct.


---

## FILE: `05_execution/54_FAILURE_RECOVERY_PLAYBOOK.md`

# Failure Recovery Playbook

## Failure: asset "podobny", ale niezgodny

Przyczyna:
brak Feature Contract.

Naprawa:
1. wróć do referencji,
2. wypisz MUST,
3. porównaj je z obiektami,
4. napraw tylko brakujące/niepoprawne features.

## Failure: detal zniknął po modyfikacji

Przyczyna:
operacja destrukcyjna lub zmiana stacku.

Naprawa:
- zidentyfikuj feature owner,
- porównaj z checkpointem,
- przywróć owner lub modifier,
- nie odtwarzaj całego modelu.

## Failure: operator API nic nie robi / robi coś innego

Przyczyna:
context/mode/selection.

Naprawa:
- sprawdź `poll`,
- sprawdź mode,
- active object,
- selection,
- view layer,
- użyj `temp_override`,
- rozważ Data API/BMesh.

## Failure: powstają `.001`, `.002`

Przyczyna:
brak idempotency.

Naprawa:
- get-or-create,
- tagowanie asset id,
- jawne usuwanie/aktualizacja starych helperów.

## Failure: bevel niszczy narożniki

Sprawdź:
- scale,
- width,
- overlap,
- segments,
- topology,
- modifier order.

## Failure: boolean daje artefakty

Sprawdź:
- coplanar surfaces,
- bardzo małe odległości,
- non-manifold cutter,
- normals,
- modifier order.

## Failure: zbyt dużo polygonów

Nie uruchamiaj od razu Decimate.

Najpierw:
- bevel segments,
- cylinders/spheres segments,
- ukryte geometry,
- duplicate geometry,
- microdetail,
- LOD separation.

## Failure: eksport wygląda inaczej

Porównaj:
- axis,
- scale,
- normals/tangents,
- material node compatibility,
- texture color spaces,
- modifiers apply/export settings,
- animation hierarchy.


---

## FILE: `05_execution/55_METRICS_AND_SCORECARD.md`

# Asset Quality Scorecard

Scorecard nie zastępuje bramek MUST.

## Categories

### A. Reference fidelity — 0–30
- silhouette 10
- proportions 8
- primary features 8
- material regions 4

### B. Modeling quality — 0–20
- topology appropriate 5
- shading 5
- modifier strategy 5
- editability 5

### C. Game readiness — 0–25
- geometry budget 5
- materials/textures 5
- pivot/transforms/naming 5
- LOD/collision 5
- export 5

### D. API/process quality — 0–15
- deterministic operations 5
- idempotency 4
- checkpoint discipline 3
- efficient tool usage 3

### E. Documentation — 0–10
- feature mapping 4
- build parameters 2
- manifest 2
- known limitations 2

## Thresholds

- 90–100: production-ready
- 80–89: acceptable with minor fixes
- 70–79: requires repair
- <70: return to planning/modeling

## Hard fail

Niezależnie od score:
- dowolny `MUST = FAIL`,
- błędny pivot dla funkcjonalnego assetu,
- brakujący wymagany materiał/animation,
- uszkodzony export,
- poważny shading/runtime defect.


---

## FILE: `05_execution/56_CHANGE_IMPACT_PROTOCOL.md`

# Change Impact Protocol

Każda poprawka może powodować regresję.

## Przed zmianą

Zidentyfikuj:
- target feature,
- owner object,
- dependencies,
- neighboring features,
- modifiers downstream,
- UV/material impact,
- export impact.

## Impact classes

### LOCAL
Zmiana nie wpływa poza jeden feature.
Przykład: szerokość szczeliny.

### STRUCTURAL
Zmiana wpływa na kilka cech i proporcje.
Przykład: szerokość korpusu.

### PIPELINE
Zmiana wpływa na UV/export/rig.
Przykład: zastosowanie modifiera zmieniającego vertex order.

## Test regresji

LOCAL:
- target + adjacent MUST.

STRUCTURAL:
- pełny silhouette + wszystkie MUST.

PIPELINE:
- pełna walidacja od odpowiedniego etapu do export.


---

## FILE: `05_execution/57_AGENT_EVALUATION_HARNESS.md`

# Agent Evaluation Harness

Biblioteka powinna być testowana na benchmarkach, a nie oceniana wyłącznie opisowo.

## Benchmark classes

### B1 — Primitive fidelity
Zbuduj asset z dokładnymi wymiarami i kilkoma cechami MUST.
Mierzy precision, naming, transforms, idempotency.

### B2 — Reference fidelity
Zbuduj hard-surface prop z front/side/top.
Mierzy silhouette, proportions, feature retention.

### B3 — Repair
Dostarcz celowo wadliwy asset.
Mierzy scene inspection, local patch, regression avoidance.

### B4 — API trap
Ustaw zły active object/Edit Mode/selection, unsaved `.blend` i version-sensitive API differences.
Mierzy context safety, runtime discovery i path stability.

### B5 — Optimization
Dostarcz zbyt ciężki asset.
Mierzy protected-feature retention, LOD generation, triangle reduction bez ślepego Decimate.

### B6 — Export
Dostarcz hierarchy + materials + texture/animation references as applicable.
Mierzy transform/export/readback i survival runtime bindings.

### B7 — End-to-end asset completion

```text
reference -> reconstruction -> modeling -> surface -> bake/runtime closure
-> LOD/collision -> export -> completion -> optional catalog integration
```

Canonical first B7:
- `07_examples/74_LAFAR_CIVIC_BOLLARD_BENCHMARK.md`.

### B8 — Bake/runtime closure regression

Start from accepted geometry/material authoring state and require Level C game-ready closure.

```text
UV contract -> dirty-channel plan -> bake -> bake validation
-> runtime material -> package export/readback -> baked-runtime QA
```

Measures:
- bake cancellation/target binding;
- BaseColor/Metallic/Emissive semantics;
- AO isolation;
- UV/LOD stability;
- foreign decal UV separation;
- clean channel reuse;
- long-job timeout handling;
- import-safe helper behavior;
- runtime package correctness.

Canonical B8:
- `07_examples/75_LAFAR_CIVIC_BOLLARD_BAKE_REGRESSION_BENCHMARK.md`.

### B9 — Pipeline integration proof and infrastructure reuse

Start from a Level C/game-ready exported asset and require truthful `PIPELINE_INTEGRATED`.

```text
canonical runtime root
-> package/round-trip invariants
-> catalog registration
-> target engine loader/test
-> trustworthy test oracle
-> completion gate with evidence kind
```

Measures:
- stale Blender image datablock detection without unnecessary rebake;
- canonical engine-visible asset-root reuse;
- absence of lookalike-root writes;
- final exported hard dimensions/contact datum;
- Blender round-trip kept separate from engine proof;
- engine loader/test actually resolves the final artifact;
- direct executable exit status rather than formatter/pipeline status;
- controlled bite-test validity for new assertions;
- Pipeline DAG stage reuse after local repairs;
- zero repeated build-system discovery when a matching project profile exists.

Canonical v0.7 B9:
- `07_examples/76_LAFAR_CIVIC_BOLLARD_PIPELINE_INTEGRATION_REGRESSION_BENCHMARK.md`.

## Metrics

Quality/runtime:
- MUST pass rate;
- hard dimension/contact error after export;
- silhouette/reference deviation;
- triangle count per LOD;
- collision cost;
- bake/runtime material status;
- BaseColor/Normal/ORM/Emissive semantic validation;
- image cache coherence status;
- UV contract status;
- package node/material/image readback;
- runtime asset root status;
- engine loader status/evidence kind;
- test oracle status;
- completion level;
- runtime contract violations;
- human visual score when available.

Efficiency:
- total/stage token usage;
- tool calls and Blender mutation calls;
- failed tool calls/retries/strategy switches;
- broad reference rescans;
- complete code echoes after artifact creation;
- full multichannel bake runs;
- channels rebaked;
- stages executed vs reused;
- full pipeline restarts;
- project profile rediscovery calls;
- build-system discovery calls;
- test runs and invalid/ambiguous test results;
- expensive jobs relaunched after timeout;
- time to requested completion.

Unknown metrics remain `null`; do not invent them.

## Najważniejsze metryki agenta

1. `MUST pass rate`
2. `reference/runtime correctness`
3. `regressions per repair`
4. `failed API/tool calls`
5. `completion truthfulness`
6. `token/context efficiency at equal quality`
7. `full-stage recomputes avoided`
8. `baked-runtime package correctness`
9. `runtime-root correctness`
10. `engine-proof/test-oracle integrity`

## Release gate biblioteki

Nowa wersja nie jest lepsza tylko dlatego, że ma więcej treści.

Release passes only if benchmark evidence shows at least one of:
- higher quality with comparable cost;
- lower cost with no quality regression;
- elimination of a previously observed failure class;
- stronger proven completion level without breaking protected features.

## Efficiency comparison rule

Token reduction is secondary to fidelity and runtime correctness.

Known Bollard evidence:
- first full baseline: ~60k tokens;
- captured v0.5 B8 continuation: ~36k tokens before full closure;
- final continuation after that: user-reported ~45k additional tokens;
- combined post-v0.5 continuation cost: roughly ~81k tokens.

Preferred v0.6 B8 target for an equivalent accepted hard-surface game-ready finish:

```yaml
stage_tokens: <= 15000
blender_python_mutation_calls: <= 10
full_multichannel_bake_runs: <= 2
accepted_silent_cancelled_bakes: 0
missing_uv_contracts: 0
baked_runtime_qa_required: true
```

Preferred v0.7 B9 target once Level C is already accepted and a matching project profile exists:

```yaml
pipeline_integration_tokens: <= 10000
project_profile_rediscovery_calls: 0
ambiguous_runtime_root_writes: 0
false_green_test_results: 0
blender_import_used_as_level_d_proof: 0
full_pipeline_restarts_after_local_repair: 0
engine_evidence_kind_required: true
```

These are benchmark goals, not universal limits.

---

## FILE: `05_execution/58_AUTOMATED_VISUAL_DIFF.md`

# Automated Visual Diff

## Cel

Wykrywać regresje wizualne pomiędzy:
- referencją a renderem,
- checkpointem A a checkpointem B,
- wersją assetu przed i po naprawie.

## Render determinism

Diff ma sens tylko, gdy stałe są:
- camera,
- resolution,
- framing,
- lighting,
- world/background,
- render engine,
- material QA profile,
- color management.

## Rodzaje diff

### Silhouette diff
Najważniejszy dla D0/D1.
Porównuj maskę obiektu.

Metryki:
- IoU,
- area difference,
- contour distance.

### Edge diff
Przydatny dla:
- rowków,
- paneli,
- dużych podziałów.

### ROI diff
Porównuje tylko obszar przypisany do Feature ID.

### Pixel diff
Używaj ostrożnie.
Materiały i anti-aliasing mogą generować różnice nieistotne geometrycznie.

## Thresholds

Nie istnieje jeden globalny próg.
Ustal osobno dla:
- silhouette,
- primary feature,
- material,
- shading.

## Regression mode

Najbardziej wartościowe zastosowanie:
`last accepted checkpoint -> current build`

Wtedy zmiana poza expected ROI jest sygnałem możliwej regresji.

## Human/reference ambiguity

Automatyczny diff nie rozstrzyga sam:
- stylizowanej perspektywy,
- różnego oświetlenia concept artu,
- ukrytej geometrii.

Jest narzędziem dowodowym, nie arbitrem designu.


---

## FILE: `05_execution/59_REFERENCE_FIDELITY_PROTOCOL.md`

# Reference Fidelity Protocol

## Poziomy zgodności

### L0 — category
Asset jest tego samego rodzaju.

Za mało.

### L1 — silhouette
Główna bryła zgadza się.

### L2 — primary features
Wszystkie cechy rozpoznawcze istnieją.

### L3 — proportions
Relacje wielkości cech są zgodne.

### L4 — material segmentation
Obszary materiałowe są zgodne.

### L5 — production fidelity
Detale, edge treatment, shading i materiały tworzą tę samą intencję projektową.

Docelowy asset powinien osiągać poziom wymagany przez klasę importance.

## Hero prop

Zwykle wymaga L4/L5.

## Background prop

Może być zaakceptowany przy L2/L3, jeśli runtime i dystans to uzasadniają.

## No compensation rule

Nie kompensuj błędu:
- materiałem za złą geometrię,
- światłem za zły shading,
- detalem D3 za złą sylwetkę,
- normal mapą za brakującą primary form.

## Fidelity report

Raportuj osobno:
- form,
- proportions,
- features,
- materials,
- surface.


---

## FILE: `05_execution/60_AUTHORING_TO_RUNTIME_HANDOFF.md`

# Authoring to Runtime Handoff

## Artefakty

Minimalny pakiet może zawierać:
- source `.blend`,
- export mesh/scene,
- textures,
- material mapping,
- collision,
- animation,
- asset manifest,
- validation report.

## Manifest

```text
asset_id
version
source_blender_version
export_format
units
bounds
pivot_policy
objects
materials
textures
triangle_counts
lods
collision
animations
dependencies
known_limitations
```

## Source retention

Nie nadpisuj źródła edytowalnego finalnym flattened mesh.

## Re-import test

Jeśli pipeline pozwala:
1. export,
2. import do czystej sceny/test runtime,
3. porównanie manifestu,
4. visual smoke test.

## Version

Każdy istotny export powinien być możliwy do powiązania z:
- wersją source asset,
- wersją biblioteki agenta,
- wersją Blendera,
- profilem eksportu.

## Handoff failure

Brak błędu eksportera nie oznacza poprawnego handoff.
Poprawność ocenia wynik po stronie konsumenta.


---

## FILE: `05_execution/61_RETRY_BUDGET_AND_STRATEGY_SWITCH.md`

# Retry Budget and Strategy Switching

## Purpose

This protocol prevents autonomous Blender agents from wasting tool calls, tokens, and scene integrity on repeated failed attempts with unchanged assumptions.

A retry is justified only when new information or a controlled parameter change makes success more likely.

## Core rule

```text
same operation + same preconditions + same strategy
-> maximum 1 retry
```

After the second failure, the agent must not repeat the same call pattern.

It must inspect, diagnose, and either change strategy or roll back.

## Failure loop

```text
ATTEMPT 1
-> fail
-> inspect failure state
-> one corrected retry allowed

ATTEMPT 2
-> fail
-> STOP same-strategy retries
-> restore/checkpoint if needed
-> re-inspect scene and assumptions
-> classify failure
-> switch strategy or escalate
```

A third attempt is allowed only if at least one of these changed materially:
- execution strategy;
- topology approach;
- tool/capability binding;
- scene/context precondition;
- validated parameter set;
- source geometry;
- target object/surface selection.

## Failure classes

### F1 — Context failure
Examples:
- wrong mode;
- wrong active object;
- operator poll failure;
- selection mismatch.

Repair:
- inspect context;
- set explicit context;
- prefer data/BMesh route if possible.

Do not repeatedly call the same operator hoping context changes.

### F2 — Geometry precondition failure
Examples:
- non-manifold region;
- missing edge chain;
- topology too noisy for requested operation;
- Boolean input invalid.

Repair:
- local topology repair;
- dedicated detail shell;
- alternate modeling strategy;
- rebuild affected local region.

### F3 — Parameter failure
Examples:
- bevel width self-overlap;
- projection tolerance too small;
- depth sign wrong after normals check.

Repair:
- change one documented parameter based on measured evidence;
- revalidate.

No random parameter sweeping on the production mesh.

### F4 — Capability failure
Examples:
- required connector tool unavailable;
- Python execution absent;
- render capture unavailable;
- unsupported Blender API property.

Repair:
- update Agent Tool API Profile;
- invoke defined fallback if one exists;
- otherwise block/escalate.

Do not silently replace a required technique with unrelated UI automation.

### F5 — Reference/constraint failure
Examples:
- conflicting views;
- unresolved dimension datum;
- ambiguous hidden geometry.

Repair:
- return to reconstruction authority/conflict/uncertainty modules;
- do not keep changing geometry until one view looks better.

### F6 — Regression failure
A local repair passes its feature but breaks an already accepted MUST feature.

Repair:
- rollback;
- inspect change-impact graph;
- choose a narrower patch or different strategy.

## Retry budget per feature

Track:

```yaml
retry_state:
  feature_id: F023
  operation: HS_PANEL_LINE
  attempts: 2
  same_strategy_failures: 2
  inspections_after_failure: 2
  strategy_switches: 0
  rollback_count: 0
  status: STRATEGY_SWITCH_REQUIRED
```

## Tool-call budget behavior

The agent should optimize for accepted features, not raw action count.

Important metric:

```text
tool_calls_per_accepted_feature
```

A feature that needs 25 blind operations is a diagnostic failure even if the final result eventually looks acceptable.

## Batch rule

Batch coherent deterministic changes when:
- they share validated preconditions;
- failure can be attributed clearly;
- postconditions can still identify which feature failed.

Do not batch unrelated risky operations merely to reduce call count.

## Parameter search rule

Allowed:

```text
measure -> adjust one relevant parameter -> validate
```

Disallowed:

```text
try 0.01
try 0.02
try 0.03
try 0.04
until screenshot seems acceptable
```

If parameter optimization is genuinely required, define bounded search criteria and objective metrics first.

## Local patch vs rebuild

Prefer local repair when:
- source topology is sound;
- failure is isolated;
- Feature Contract ownership is clear;
- regression risk is low.

Prefer controlled rebuild when:
- source topology is AI-generated/noisy;
- multiple local fixes have accumulated;
- semantic source data can regenerate the part deterministically;
- local surgery risks more regressions than reconstruction.

## Checkpoint rule

Before a strategy switch that can materially alter topology:
- preserve the last valid checkpoint;
- record the reason for abandoning the previous strategy.

If the new strategy fails, restore the last valid state rather than stacking fixes on top of a failed experiment.

## Escalation

Escalate when:
- two materially different strategies fail;
- a MUST feature cannot be satisfied without breaking another MUST feature;
- required capability is unavailable;
- reference authority cannot resolve a high-impact contradiction;
- runtime/export contract is unknown and required for completion.

## Agent response requirement

After repeated failure, the agent must report compactly:

```text
FAILED OPERATION
ROOT CAUSE CLASS
EVIDENCE
ATTEMPTS
WHY SAME RETRY IS FORBIDDEN
NEXT STRATEGY OR BLOCKER
LAST VALID CHECKPOINT
```

Do not hide retry churn inside a final narrative.

## Fundamental rule

Every retry must buy information or change a validated precondition.

If nothing meaningful changed, do not call the tool again.


---

## FILE: `05_execution/62_CODE_ARTIFACT_AND_PATCH_PROTOCOL.md`

# Code Artifact and Patch Protocol

## Purpose

Generated Blender Python is an executable artifact, not conversational prose.

The language model must not repeatedly place complete build scripts, complete QA scripts or large patches into its own reasoning context when the file already exists on disk.

## Core rule

```text
plan in context
-> write/update artifact on disk
-> execute artifact
-> return compact result
-> inspect only the failing symbol/range
```

## File-first policy

If generated code is more than roughly 120 lines or contains reusable helpers, write it to a file and treat the path as persistent state.

After creation, return only:
- path;
- changed symbols/functions;
- approximate line count;
- execution status;
- compact diagnostics.

Do not echo the complete source unless the user explicitly asks to see it.

## Patch policy

For an existing script:

1. identify the failing function or constant;
2. read only the required range;
3. apply the smallest coherent patch;
4. report the changed symbols and reason;
5. execute tests/validation.

Do not re-read or re-print the entire file after every edit.

## Tool output contract

Preferred result:

```yaml
code_artifact:
  path: build_asset.py
  action: PATCHED
  changed_symbols:
    - build_base_accent
    - ACCENT_DEPTH
  lines_touched: 18
  syntax: PASS
  execution: PASS
  validation:
    visible_pixels: 214
    mesh_issues: 0
```

Not acceptable by default:
- full 600-line source after creation;
- full source after a 5-line patch;
- complete unified diff containing unrelated context;
- repeated unchanged function bodies;
- long stderr/stdout when a compact error classification is sufficient.

## Read budget

Read source in this order:

```text
symbol index / grep
-> targeted line range
-> local dependency function
-> whole file only when architecture cannot be inferred otherwise
```

## Generated helper reuse

Before writing a helper such as:
- lathe/profile revolution;
- fillet generation;
- radial repetition;
- mesh validation;
- QA scene isolation;
- reference measurement;

check the Semantic Skill Registry and `executors/` directory.

If a compatible reusable executor exists, import/use it instead of generating another local implementation.

## Artifact persistence

Persist:
- build script path;
- QA script path;
- last successful execution hash/mtime when available;
- produced asset collection/object IDs;
- validation summary.

A later phase should reference the artifact, not reconstruct its source from conversation history.

## Failure diagnostics

On failure, return:
- error class;
- file/function/line when available;
- relevant state;
- smallest required source range.

Raw stack traces may be retained on disk. The LLM should normally receive only the decisive portion.

## Token objective

Code generation should consume tokens for design decisions, not for transporting unchanged source code between tools and the model.


---

## FILE: `05_execution/63_REFERENCE_TO_RUNTIME_COMPLETENESS_REPORT.md`

# Reference-to-Runtime Completeness Report

## Purpose

At the end of an asset task the agent must produce a compact, machine-readable report that distinguishes:
- reference fidelity;
- authoring-model completeness;
- game-ready completeness;
- project integration.

This report replaces vague endings such as "asset finished".

It also records execution efficiency so benchmark runs can compare library versions.

---

# Required report

```yaml
asset_report:
  asset_id: SM_EXAMPLE
  target_completion_level: GAME_READY_COMPLETE
  highest_passed_level: MODELING_COMPLETE

  completion:
    reconstruction: PASS
    modeling: PASS
    game_ready: FAIL
    pipeline_integrated: NOT_REQUIRED

  geometry:
    dimensions_mm: [210, 210, 1050]
    tris:
      LOD0: 2716
      LOD1: 1152
      LOD2: 480
      LOD3: 128
    collision_tris: 88
    mesh_validation: PASS

  surface:
    uv: PASS
    material_segmentation: PASS
    bake_gate: FAIL
    runtime_textures: MISSING
    emissive_authoring: PASS
    emissive_runtime: UNVERIFIED

  export:
    files_exist: true
    post_export_validation: PASS

  integration:
    asset_catalog: NOT_DONE

  blockers:
    - PBR_BAKE_NOT_DONE

  known_deviations: []
  deferred_features: []

  efficiency:
    approximate_tokens: 60000
    tool_calls: null
    failed_tool_calls: null
    retries: null
    broad_reference_rescans: null
```

Unknown metrics should be `null`, not invented.

---

# Fidelity section

For reconstruction-driven work include:
- locked dimensions and deviation;
- silhouette/multi-view status;
- known source conflicts;
- intentionally inferred geometry;
- human/reference-critical deviations.

Do not restate the full Evidence Ledger. Summarize only accepted facts and unresolved issues.

---

# Surface completeness

The report must distinguish:

```text
MATERIAL_LOOKDEV_PASS
TEXTURE_BAKE_PASS
RUNTIME_MATERIAL_BINDING_PASS
```

These are separate gates.

A procedural material that looks good in Blender may pass lookdev and still fail runtime completion.

---

# Emissive completeness

Report separately:

```yaml
emissive:
  geometry_mask_authoring: PASS
  blender_preview: PASS
  exported_data: PASS
  engine_bloom_tonemapping: UNVERIFIED
```

Do not claim final glow fidelity when only the Blender lookdev was tested.

---

# Pipeline integration

If the asset is exported but not registered in the project's asset catalog/database:

```text
pipeline_integrated = FAIL or NOT_REQUIRED
```

depending on the requested target.

Do not hide the distinction in prose.

---

# Efficiency metrics

For benchmark-capable runs record when available:
- total token usage;
- tokens before first blockout;
- tool calls;
- failed calls;
- repeated strategy attempts;
- raw outputs above Tool Output Budget;
- full-source echoes;
- full-reference rescans;
- number of localized repair cycles;
- time-to-first-valid-blockout;
- time-to-target-completion.

The purpose is to detect a system that becomes more verbose without becoming more capable.

---

# Completion wording

Allowed:

> Modeling complete; game-ready completion is blocked by texture bake and runtime material binding.

Not allowed:

> Asset complete.

when required downstream gates remain unfinished.

---

# Benchmark comparison

When comparing agent/library versions, prioritize in order:
1. no regression of MUST reference fidelity;
2. no regression of runtime correctness;
3. fewer unrecovered failures;
4. fewer repeated operations;
5. lower context/token cost;
6. lower wall-clock/tool cost.

Efficiency gains never justify losing protected features.


---

## FILE: `05_execution/64_LONG_RUNNING_JOB_AND_POLL_PROTOCOL.md`

# Long-Running Blender Job and Poll Protocol

## Purpose

Expensive Blender operations such as AO bake, high-resolution bake, export and heavy Geometry Nodes evaluation may outlive a tool/MCP request timeout.

A transport timeout is not the same thing as a Blender failure.

Without this distinction an agent may launch the same expensive operation multiple times, corrupt state, overwrite outputs or waste large amounts of time/tokens.

---

# Core rule

```text
REQUEST TIMEOUT != PROVEN JOB FAILURE
```

After timeout:

```text
inspect state/artifacts
-> classify RUNNING / FINISHED / FAILED / UNKNOWN
-> only retry if FAILED or proven absent
```

Do not immediately execute the same expensive operation again.

---

# Job record

For a long-running stage maintain a compact record:

```yaml
job:
  id: BOLLARD_BAKE_ORM_001
  stage: BAKE
  operation: AO
  status: RUNNING
  started_at:
  expected_outputs:
    - aster_bollard_tmp_ao
  checkpoint_before:
  dirty_channels:
    - orm_ao
  last_error:
```

Status vocabulary:

```text
PENDING
RUNNING
FINISHED
FAILED
CANCELLED
UNKNOWN
```

---

# Evidence order after timeout

Check in this order:

1. explicit runtime/job status if the integration exposes one;
2. Blender scene/image state;
3. expected image/file existence and modification time;
4. compact output validation;
5. only then consider rerunning.

If output exists but its validity is uncertain, validate it. Do not recompute it merely to gain confidence.

---

# Blender threading caution

Do not move normal `bpy` scene mutation/bake logic into arbitrary Python background threads just to avoid an MCP timeout.

Blender API operations are generally expected to run in Blender's main execution context. Use mechanisms compatible with the active runtime, for example:
- supported timer/modal workflow;
- controlled external Blender process;
- integration-provided async job mechanism;
- synchronous execution followed by artifact/status inspection when transport timeout is possible.

Do not invent asynchronous capabilities that the connected tool does not expose.

---

# Channel checkpoints

Expensive multi-channel bake should checkpoint after each accepted channel:

```text
BaseColor PASS
Normal PASS
AO PASS
Roughness PASS
Metallic PASS
Emissive PASS
```

If Emissive later fails, do not destroy/recompute accepted BaseColor/Normal/AO unless a changed dependency invalidates them.

Use `05_execution/65_INCREMENTAL_DIRTY_STAGE_CACHE.md`.

---

# Retry policy

For an expensive job:
- at most one launch while state is `RUNNING` or `UNKNOWN`;
- timeout triggers inspection, not retry;
- proven `FAILED` may use one corrected retry of the same strategy;
- second proven failure requires strategy switch according to the global retry protocol.

---

# Compact polling

Poll only decision-grade state:

```yaml
job_status:
  id: BOLLARD_BAKE_AO_001
  status: FINISHED
  output_exists: true
  output_validation: PASS
  elapsed_s: 41.2
```

Do not return render logs, complete image arrays or full Blender console output during normal polling.

---

# Completion

A long-running job is complete only when:
- Blender/tool status is finished or artifact evidence proves completion;
- expected artifact exists;
- semantic validator accepts it;
- job state is persisted.

File existence without semantic validation is not enough.


---

## FILE: `05_execution/65_INCREMENTAL_DIRTY_STAGE_CACHE.md`

# Incremental Dirty-Stage Cache

## Purpose

A local fix must not force the agent to rerun the entire build/bake/export pipeline when earlier accepted artifacts are still valid.

The cache tracks dependencies and marks only affected stages/channels as dirty.

This is an execution-efficiency contract, not merely an optimization suggestion.

---

# Core model

```text
INPUT FACT
-> dependency graph
-> dirty artifacts only
-> targeted execution
-> validation
-> update signatures
```

Persist the cache as compact structured state or a small project-side file.

---

# Artifact record

```yaml
artifact:
  id: TEXTURE_EMISSIVE
  path: .../astera_bollard_emissive.png
  status: PASS
  dependencies:
    - UV_CONTRACT_ACS_BOLLARD_V1
    - MATERIAL_EMISSIVE_GRAPH
    - EMIT_REFERENCE_STRENGTH
  signature:
  dirty: false
  last_validation:
```

---

# Canonical dependencies

Typical artifacts:

```text
BLOCKOUT
FINAL_GEOMETRY
UV_CONTRACT
BASECOLOR
NORMAL
AO
ROUGHNESS
METALLIC
ORM
EMISSIVE
RUNTIME_MATERIAL
LOD0
LOD1
LOD2
LOD3
COLLISION
EXPORT_MODULE
EXPORT_COLLISION
CATALOG_ENTRY
```

---

# Dirty propagation examples

## Emission normalization change

```text
EMIT_REFERENCE_STRENGTH changed
-> EMISSIVE dirty
-> RUNTIME_MATERIAL dirty only if binding/parameter changes
-> EXPORT_MODULE dirty
```

Do not rebake BaseColor/Normal/AO/Roughness/Metallic.

## AO isolation fix

```text
AO source/isolation changed
-> AO dirty
-> ORM dirty
-> EXPORT_MODULE dirty
```

Do not rebake BaseColor/Normal/Emissive.

## Base Color graph change

```text
material Base Color graph changed
-> BaseColor dirty
-> EXPORT_MODULE dirty
```

Other channels remain clean unless they share the changed nodes/data.

## UV contract change

```text
UV contract changed
-> all maps using that UV set dirty
-> all LOD mesh UV validation dirty
-> runtime material QA dirty
-> export dirty
```

## Geometry change

At minimum consider:
- AO dirty;
- Normal dirty when geometry/tangent source changes;
- geometry-position/object-coordinate procedural channels dirty;
- affected LOD/export meshes dirty;
- collision only if collision-relevant volume changed.

Do not blindly dirty all material channels if they are independent of geometry.

## Decal change

If decals use a separate project atlas/material:

```text
decal content changed
-> decal asset/material dirty
-> export dirty
```

Structural PBR maps remain clean.

---

# Signatures

A signature may use:
- stable content hash;
- selected parameter hash;
- file modification state plus explicit dependencies;
- another deterministic project mechanism.

Do not hash or serialize the entire Blender scene when a narrow parameter signature is sufficient.

---

# Accepted artifact reuse

Before running an expensive operation:

```text
if artifact PASS
and dirty == false
and dependencies unchanged
-> REUSE
```

Report:

```yaml
bake_plan:
  reuse:
    - BaseColor
    - Normal
    - AO
    - Roughness
    - Metallic
  execute:
    - Emissive
```

This report should be small enough to remain in active context.

---

# Failure behavior

A failed artifact does not automatically invalidate siblings.

Example:
- Emissive mask outside allowed emitter region -> Emissive FAIL;
- BaseColor PASS remains valid.

Invalidate siblings only when they share the failed dependency.

---

# Pipeline boundary

Changing exported packaging without changing mesh/material data should not force rebake.

Changing runtime material bindings without changing texture content should not force rebake.

Changing catalog registration should not force Blender rebuild/export unless the project contract explicitly requires regenerated metadata inside the asset.

---

# Benchmark metric

Track:

```text
full_stage_recomputes
channels_rebaked
clean_artifacts_reused
expensive_operations_avoided
```

A v0.6 agent should reduce full bake reruns substantially compared with the v0.5 bollard continuation benchmark.


---

## FILE: `05_execution/66_TEST_ORACLE_EXIT_CODE_AND_BITE_TEST.md`

# Test Oracle, Exit Code and Bite-Test Integrity

## Purpose

A test result is useful only if the agent is reading the status of the **test process itself** and has evidence that the newly added assertion can actually fail.

A green-looking command is not proof of a green test.

## Core rules

```text
DISPLAY PIPELINE EXIT CODE != TEST EXIT CODE
TEST THAT NEVER BITES != VERIFIED REGRESSION TEST
PROCESS CRASH != ASSERTION FAILURE
```

## 1. Never lose the real exit status

Unsafe shell pattern:

```bash
./ModelTests.exe 2>&1 | tail -20
echo $?
```

Without `pipefail`, `$?` is normally the status of `tail`, not the test executable.

Preferred patterns:

```bash
./ModelTests.exe >test.out 2>test.err
status=$?
tail -20 test.out
tail -20 test.err
exit $status
```

or, when supported:

```bash
set -o pipefail
./ModelTests.exe 2>&1 | tail -20
status=$?
```

Better still, invoke the test process directly through a subprocess/tool API that returns its own exit code.

## 2. Classify the result

Use explicit states:

```text
PASS
ASSERTION_FAIL
LOAD_FAIL
BUILD_FAIL
CRASH
TIMEOUT
UNKNOWN
```

Do not interpret a non-zero code as a valid bite test until output shows the intended assertion failed.

Example:
- expected triangle count intentionally changed;
- process exits 1;
- stderr contains the exact bollard regression message;
- restore correct expectation;
- rebuild;
- process exits 0.

That is a valid bite test.

An `abort()`/CRT crash with exit 3 is **not** proof that the assertion bites.

## 3. Bite-test protocol

When adding a new engine/project regression assertion, perform one controlled negative proof when practical:

```text
GREEN BASELINE
-> controlled mutation of one expected value or fixture
-> rebuild only affected test target
-> run test
-> verify intended assertion fails with readable diagnostic
-> restore mutation
-> rebuild
-> verify clean PASS
```

The mutation must be:
- narrow;
- reversible;
- owned by the agent;
- never left committed;
- not destructive to production assets.

Do not run a bite test if the mutation would be unsafe or expensive; record `BITE_TEST_NOT_SAFE` instead.

## 4. Non-interactive failure requirement

Automated tests used by an agent must fail through machine-readable output/exit state rather than modal dialogs where possible.

Asset loading in a test should surface exceptions as a readable test failure. A modal CRT/error dialog that blocks automation is a test infrastructure defect.

## 5. Build/test target reuse

Before inventing commands:
1. read active Project Asset Pipeline Profile;
2. use the known build directory/configuration;
3. build the narrow test target;
4. run the known executable/test selector;
5. capture the real exit code.

Do not rediscover CMake presets, binaries and test locations every asset.

## Compact report

```yaml
test_oracle:
  build_target: ModelTests
  build_status: PASS
  command_mode: DIRECT_PROCESS
  exit_code: 0
  stderr_tail: ""
  bite_test:
    performed: true
    mutated_expectation: triangle_count_lod0
    failing_exit_code: 1
    expected_failure_message_seen: true
    restored_and_green: true
  status: PASS
```

## Completion impact

`PIPELINE_INTEGRATED` must not accept a runtime test result whose process exit status is ambiguous.

If the agent used a shell pipeline and cannot prove the executable's status:

```text
ENGINE_TEST_STATUS = UNVERIFIED
```

Rerun the test correctly; do not mark Level D PASS from the ambiguous invocation.

---

## FILE: `05_execution/67_POST_EXPORT_INVARIANT_AND_ROUNDTRIP_VALIDATION.md`

# Post-Export Invariant and Round-Trip Validation

## Purpose

Authoring-state correctness is not enough. Modifiers, bevels, export copies, coordinate conversion and packaging can change dimensions, ground contact, materials or LOD structure.

The final exported artifact must be measured again.

## Core rule

```text
AUTHORING PASS != EXPORTED ARTIFACT PASS
BLENDER IMPORT PASS != ENGINE IMPORT PASS
```

Use two distinct proof layers:

```text
LEVEL C / GAME_READY:
exported artifact -> neutral/Blender round-trip -> invariant checks

LEVEL D / PIPELINE_INTEGRATED:
exported artifact -> target engine loader/importer -> engine-side checks
```

## Protected export invariants

For each asset declare only the invariants that matter, for example:
- hard dimensions;
- ground/contact datum;
- pivot/origin;
- handedness/readable asymmetry;
- LOD family and node names;
- triangle budgets;
- material/image presence;
- UV presence;
- required vertex colors/custom attributes;
- collision packaging.

Example:

```yaml
export_invariants:
  dimensions_mm: [210, 210, 1050]
  tolerance_mm: 2
  ground_datum_z_mm: 0
  lods:
    LOD0: 2844
    LOD1: 1152
    LOD2: 480
    LOD3: 128
  required_maps:
    - basecolor
    - normal
    - metallic_roughness
```

## Round-trip order

After export:

```text
1. parse/read back package metadata
2. import final artifact into an isolated scratch context
3. measure protected invariants on imported data
4. remove scratch import
5. only then proceed to catalog/runtime integration
```

Do not measure the pre-export source and assume the exported copy retained the same bounds.

## Modifier/contact regression

A bevel or underside/profile change can preserve apparent height in the build script while moving the true lowest vertex above the ground datum.

Therefore hard height should normally be checked as:

```text
max_axis - min_axis
```

and contact datum separately as:

```text
abs(min_axis - expected_ground) <= tolerance
```

This catches an asset that is nominally tall enough but floats above the ground, or one whose fillet removes 1–2 mm from the hard product dimension.

## Runtime material round-trip

The round-trip check should inspect the baked runtime material, not procedural authoring materials.

Verify:
- images resolve;
- image dimensions are non-zero;
- expected material slots exist;
- LOD UVs sample the intended atlas;
- decals/dynamic materials remain separate when required.

## Engine proof is a different gate

A Blender glTF import proves that Blender's importer can read the exported file. It does **not** prove the custom engine can resolve the same asset path, parse its LOD convention or load its materials.

Required Level D evidence must come from the target engine/importer or an engine test that calls the same production loader.

## Dirty propagation

If a post-export invariant fails:
- repair the narrow upstream owner;
- dirty only dependent stages;
- do not automatically rebake unrelated texture channels.

Example:

```text
underside geometry changes ground datum
-> geometry/affected LOD dirty
-> AO/normal/geometry-driven channels as applicable
-> export + round-trip dirty
-> catalog entry content usually clean
-> engine test dirty
```

A separate decal atlas normally remains clean.

## Compact report

```yaml
export_roundtrip:
  package_readback: PASS
  imported_lods: 4
  dimensions:
    LOD0_mm: [210, 210, 1050]
    LOD1_mm: [210, 210, 1050]
  ground_datum: PASS
  texture_resolution: PASS
  material_bindings: PASS
  engine_proof: UNVERIFIED
  status: PASS
```

`engine_proof` remains separate until the Level D pack runs.

---

## FILE: `05_execution/68_PIPELINE_DAG_EXECUTOR_AND_STAGE_REUSE.md`

# Pipeline DAG Executor and Stage Reuse

## Purpose

`Incremental Dirty-Stage Cache` is not optional advice. The agent must execute the smallest dependency closure required by the current repair.

A manual sequence such as:

```text
build -> decals -> bake all -> export -> import -> test
```

is forbidden when some stages are already clean and independent.

## Canonical DAG

A typical hard-surface runtime asset may use:

```text
REFERENCE/CONTRACT
      |
   BUILD_GEOMETRY
      |\
      | UV_CONTRACT
      |    |
      | BAKE_CHANNELS
      |    |
DECAL_ASSET   RUNTIME_MATERIAL
      \       /
       PACKAGE_EXPORT
            |
     EXPORT_ROUNDTRIP
            |
      CATALOG_REGISTER
            |
       ENGINE_SMOKE_TEST
            |
      COMPLETION_GATE
```

Project profiles may override dependencies, but the dependency graph must be explicit.

## Stage record

```yaml
stage:
  id: BAKE_AO
  dependencies:
    - BUILD_GEOMETRY
    - UV_CONTRACT
    - AO_ISOLATION_PROFILE
  outputs:
    - TEXTURE_ORM_R
  signature: ...
  status: PASS
  dirty: false
```

## Execution planner

Before any non-trivial rebuild emit:

```yaml
execution_plan:
  changed_inputs:
    - UNDER_RIM_PROFILE
  dirty:
    - BUILD_GEOMETRY
    - BAKE_AO
    - BAKE_NORMAL
    - PACKAGE_EXPORT
    - EXPORT_ROUNDTRIP
    - ENGINE_SMOKE_TEST
  reuse:
    - DECAL_ASSET
    - BASECOLOR
    - ROUGHNESS
    - METALLIC
    - EMISSIVE
```

Then execute only the dirty topological order.

## Geometry change does not mean all textures are dirty

A geometry edit dirties channels only through declared dependencies.

Examples:
- tangent normal from geometry/procedural bump: likely dirty;
- AO: dirty;
- position-dependent dirt mask: dirty;
- constant/UV-authored metallic: normally clean;
- separate decal atlas: normally clean;
- emissive mask on unchanged diffuser UV/geometry: may remain clean.

When uncertain, mark the specific dependency `UNVERIFIED`; do not automatically execute every stage.

## Runtime binding/cache change

A stale Blender image datablock dirties:

```text
RUNTIME_IMAGE_BINDING
BAKED_RUNTIME_QA
```

It does **not** dirty the accepted texture file itself.

Expected repair:

```text
reload/synchronize image -> QA
```

not:

```text
rebake all maps
```

## Runtime-root change

Correcting export destination from one filesystem tree to another normally dirties:
- package copy/export destination;
- package readback;
- catalog path verification;
- engine smoke test.

It does not by itself dirty geometry or baked pixels if the accepted artifacts can be copied/re-exported without recomputation.

## Cache signatures

Use narrow signatures:
- geometry parameters/hash;
- UV contract ID;
- channel graph/parameter hash;
- decal source hash;
- runtime profile ID;
- export packaging profile ID;
- runtime asset root ID.

Do not hash the entire scene for every stage.

## No implicit top-level side effects

A stage runner may import stage modules only if they are import-safe.

Every production mutation must be behind an explicit callable entry point.

## Failure semantics

If stage `X` fails:
- dependents of `X` remain blocked/dirty;
- independent previously accepted stages remain clean;
- repair `X` or its failed dependency;
- rerun only the affected closure.

## Metrics

Track:

```text
stages_executed
stages_reused
expensive_stages_reused
full_pipeline_restarts
channels_rebaked
```

For an accepted hard-surface asset, `full_pipeline_restarts` after a local repair should normally be zero.

## Candidate executor

Use `executors/pipeline_dag.py` for deterministic dependency closure/planning when its contract fits the project.

The executor plans work; asset-specific stage callables remain owned by the project.

---

## FILE: `06_prompts/60_SYSTEM_PROMPT.md`

# System Prompt — Blender Asset Agent v0.9

Jesteś technical artistem/modelerem 3D specjalizującym się w Blender 5.1 i runtime game assets.

Twoim zadaniem nie jest "wygenerować model". Masz przeprowadzić kontrolowany, dowodowy pipeline od referencji do zwalidowanego assetu.

## 1. State and completion

Używaj Agent State Machine oraz, dla reference reconstruction, `10_reconstruction/149_RECONSTRUCTION_STATE_MACHINE.md`.

Zawsze ustal `TARGET_COMPLETION_LEVEL`:
- `RECONSTRUCTION_COMPLETE`;
- `MODELING_COMPLETE`;
- `GAME_READY_COMPLETE`;
- `PIPELINE_INTEGRATED`.

Wyższy poziom wymaga niższych. Nie używaj bezwarunkowego `DONE` przy niespełnionym gate.

## 2. Fundamental v0.9 rule — understand shape before modeling

Dla rekonstrukcji z concept art/technical sheet/blueprint:

```text
reference evidence
-> constraints/authority
-> Reconstruction Shape Graph
-> Shape Node contracts
-> mathematical shape classification
-> coarse-to-fine RDL execution
-> proof-bearing node gates
-> final reconstruction fidelity gate
-> runtime
```

Nie przechodź bezpośrednio:

```text
image -> operator -> large build script
```

## 3. Shape Graph is mandatory

Przed produkcyjną geometrią zbuduj `Reconstruction Shape Graph`.

Canonical hierarchy:

```text
G0 GLOBAL_ENVELOPE
G1 PRIMARY_FORM
G2 SECONDARY_STRUCTURAL_FORM
G3 STRUCTURAL_FEATURE
G4 EDGE_LANGUAGE
G5 SURFACE_DETAIL
```

Każdy required Shape Node ma:
- stable ID;
- parent/dependencies;
- G-level i RDL;
- semantic role;
- importance;
- shape class;
- authoritative views + properties controlled by each view;
- numeric/relationship constraints;
- validation contract;
- implementation skill.

`Shape Graph != PASS` blokuje produkcyjne modelowanie poza diagnostic RDL0.

`Shape Graph != Blender Object hierarchy`.

## 4. Representation before operator

Najpierw sklasyfikuj formę:

```text
ENVELOPE
PARAMETRIC_PRIMITIVE
EXTRUDED_PROFILE
REVOLVED_PROFILE
PROFILE_SWEEP
MULTI_SECTION_LOFT
MULTI_SECTION_TRANSITION
SUBD_FREEFORM
BOOLEAN_RECESS
PANEL_LINE
LAYERED_ASSEMBLY
HYBRID_ASSEMBLY
```

Dopiero potem wybierz semantic skill/BMesh/modifier/operator.

Nie defaultuj do `cube + bevel`.

Jeśli primary form zmienia jednocześnie width, depth i corner/chamfer behavior wzdłuż osi, route do `SHAPE_CLASSIFY`; typowym rozwiązaniem jest `SECTION_LOFT_HARD_SURFACE` albo `SUBD_FREEFORM`.

Po jednej poprawionej ponownej próbie tej samej strategii, drugi udowodniony FAIL wymaga re-inspection i representation/strategy switch.

## 5. Reconstruction Detail Levels

`RDL` nie jest runtime `LOD`.

```text
RDL0 envelope
RDL1 primary forms
RDL2 secondary structural forms
RDL3 structural features
RDL4 edge language
RDL5 surface/detail
```

Dopiero zaakceptowany authoring model generuje runtime LOD0/1/2/3.

Nie używaj runtime LOD jako substytutu coarse-to-fine reconstruction.

## 6. One-node execution

Canonical geometry transaction:

```text
resolve one READY Shape Node
-> build/repair current node only
-> mark BUILT_UNVERIFIED
-> isolate QA scene
-> validate required registered views
-> numeric/section/regression validation
-> RECONSTRUCTION_NODE_GATE
-> persist ACCEPTED / FAIL
```

Domyślnie jedna transakcja nie może tworzyć nowych produkcyjnych node'ów z wielu RDL.

Regresja:

```text
build body + base + screen + vents + logo + bevel + materials
-> one quick render
```

Nie używaj monolitycznego `build_all()` do ominięcia node gates.

## 7. Parent/child and host rules

Required parent/dependency musi być `ACCEPTED` przed budową zależnego child.

Przykłady:
- panel line nie powstaje na failed shell;
- logo nie jest finalizowane na failed panel;
- glass/content nie powstają przy failed display recess host;
- bevel nie naprawia failed base cross-section.

Leaf skills są downstream od accepted host geometry.

## 8. RDL stage barriers

Po node gates wykonuj barrier:

```text
RDL0 PASS
-> RDL1 nodes + RDL1 barrier
-> RDL2 nodes + RDL2 barrier
-> RDL3 nodes + RDL3 barrier
-> RDL4 barrier
-> RDL5 as required
-> RECON_FIDELITY_GATE
```

Nie przeskakuj bariery, bo późniejszy detal jest prosty.

## 9. Reference authority and registration

Technical-sheet authority:

```text
explicit numeric dimensions/datum
> authoritative orthographic view
> real section/detail
> supporting perspective/hero
> prose approximation
> visual inference
```

Konflikt HARD/MUST/CANONICAL nie może zostać zamknięty komentarzem `card wins`. Wymaga `RESOLVED` albo `ACCEPTED_BY_AUTHORITY` z provenance.

Dla `NEAR_ORTHOGRAPHIC` dopuszczaj osobną kalibrację X/Y. Nie zakładaj jednego mm/px.

Nie deformuj geometrii zanim nie wykluczysz błędu projection/registration/camera/scale.

## 10. Node multi-view proof

Każdy node definiuje, co kontrolują widoki, np.:

```text
FRONT -> width/height/front contour
SIDE  -> depth/height/side profile
TOP   -> width/depth/corner plan
REAR  -> rear feature boundaries
HERO  -> supporting continuity/material interpretation
```

`looks correct` nie jest dowodem.

Dla authoritative views użyj registered comparison bez lokalnego warp.

Node affecting global silhouette wymaga również global regression check.

## 11. Multi-section loft

Dla `MULTI_SECTION_LOFT/TRANSITION`:
- definiuj semantic stations;
- zachowaj common point correspondence;
- station order musi być monotonic;
- waliduj width/depth/corner plan per station;
- sprawdzaj twist/continuity;
- nie zastępuj continuous shell overlapping boxes bez evidence equivalence.

Preferred skill: `SECTION_LOFT_HARD_SURFACE`.

## 12. Reconstruction QA discipline

Kolejność:

```text
numeric/silhouette
-> neutral/matcap form
-> material
-> hero
```

`QA_SCENE_ISOLATE` przed reconstruction QA; collision/LOD/export proxy nie może zanieczyścić renderu.

Object existence nie dowodzi widoczności feature. Używaj ROI/ray/layer/geometry evidence.

Dla glass/content/recess stosuj `LAYER_STACK_VALIDATE`.

## 13. Final reconstruction gate

Przed runtime wymagaj:
- valid Shape Graph revision;
- required nodes `ACCEPTED`;
- required RDL barriers PASS;
- hard dimensions;
- canonical registered views;
- primary landmarks/proportions;
- MUST features;
- material segmentation, jeśli target >= L4;
- authority/deviation closure;
- `RECON_FIDELITY_GATE` proof-bearing PASS.

Bare `PASS` bez evidence kind/provenance = `UNVERIFIED`.

Runtime/engine PASS nigdy nie back-propaguje do reconstruction PASS.

## 14. Modeling/API discipline

- Preferuj Data API/BMesh; `bpy.ops` tylko ze świadomym context/mode/selection.
- Skrypty idempotentne.
- Reusable Python modules import-safe; mutation tylko explicit entry point.
- Przed helperem sprawdź Semantic Skill Registry i `executors/`.
- Każdy finalny mesh ma topology intent.
- Nie dodawaj edge loops bez shape/shading/topology reason.
- Nie zmieniaj geometrii tylko po to, aby feature był widoczny w jednym lighting setup.

## 15. Specialized leaf skills

Route tylko na właściwym accepted host/stage:
- `HS_PANEL_LINE` — narrow seam/groove;
- `SUBD_TOPOLOGY_CONTROL` — Catmull-Clark cage/flow;
- `AXISYMMETRIC_PROFILE` — revolved profile;
- `RADIAL_REPEAT` — circular repetitions;
- `SECTION_LOFT_HARD_SURFACE` — multi-section form;
- decals/branding — RDL5 unless structural relief says otherwise.

## 16. Surface discipline

Dla civic hard-surface:

```text
material identity
-> macro variation
-> meso maintenance/exposure
-> micro manufacturing texture
-> sparse evidence-driven wear
```

Nie używaj global Noise/grunge jako substytutu materiału.

Emissive emitter i runtime bloom są oddzielnymi gate'ami.

## 17. UV/bake/runtime boundary

Runtime work rozpoczyna się dopiero po reconstruction gate.

- shared atlas uses semantic part IDs + `UV_CONTRACT_ID`;
- missing atlas assignment = FAIL;
- bake operator must return `FINISHED`;
- selected+active target image node required for contributing materials;
- AO/ray bake isolates unrelated render geometry;
- BaseColor/Metallic/Emissive use explicit channel semantics;
- correct PNG on disk != fresh `bpy.data.images`;
- route stale image to `IMAGE_CACHE_COHERENCE`, not automatic rebake;
- validate baked maps semantically, not by file existence.

## 18. Incremental runtime execution

After local repair use `PIPELINE_DAG_PLAN` before replaying multiple stages.

Do not rerun full build/decal/bake/export/test chain unless dependency closure proves it dirty.

Timeout is not proven FAIL until job/artifact state is checked.

## 19. Runtime paths/package/export

Resolve one canonical Runtime Path Context before external writes.

Authority:

```text
project profile
> engine/build definition
> production loader
> engine test
> sibling exporter
> heuristic
```

For current verified RPG profile reuse `<repo>/Assets/GameAssets`; `<repo>/GameAssets` is forbidden lookalike while profile remains valid.

Package readback checks nodes/materials/images/required primitive attributes such as `TEXCOORD_0` and active node-transform policy.

Hard dimensions/contact are rechecked on exported/re-imported artifact.

## 20. Level D proof

Blender glTF import = Level C round-trip evidence.

Level D requires one of:
- `ENGINE_PRODUCTION_LOADER`;
- `ENGINE_REGRESSION_TEST`;
- `ENGINE_INSTANTIATION`.

Capture test executable exit status directly. `./test | tail; echo $?` is not trusted without correct status preservation.

New regression assertion should perform controlled bite test when safe: intended assertion FAIL -> restore -> final PASS.

## 21. Tool output budget

Default:

```text
SUMMARY
-> minimal DIAGNOSTIC on failure
-> RAW only if unavoidable
```

Compute locally, return aggregates and blockers. Do not send raw pixel arrays/full logs/full scripts without diagnostic need.

For code:

```text
path/symbol lookup
-> targeted change
-> execute
-> compact report
```

## 22. Operational response format

When useful report:
- STATE;
- TASK PACK;
- TARGET COMPLETION LEVEL;
- ACTIVE PROJECT PROFILE;
- SHAPE GRAPH REVISION;
- RDL;
- CURRENT SHAPE NODE;
- SHAPE CLASS / SELECTED SKILL;
- REQUIRED VIEWS;
- ACTION;
- NODE GATE RESULT;
- STAGE BARRIER;
- COMPLETION STATUS.

## Final principle

Nie myśl:

```text
"mam zrobić pylon — jakich operatorów użyć?"
```

Myśl:

```text
co jest globalną formą?
z jakich primary forms się składa?
jakie są dependencies i hosty?
które rzuty definiują każdy node?
jaka reprezentacja matematyczna opisuje ten node?
jak udowodnić go przed dodaniem detalu?
```

Dopiero potem modeluj.


---

## FILE: `06_prompts/61_TASK_PROMPT_TEMPLATE.md`

# Task Prompt Template

## Goal
Zbuduj / popraw:
`<asset>`

## Reference
`<reference description / file IDs>`

## Must preserve
- ...
- ...
- ...

## Scale
- width:
- depth:
- height:

## Runtime
- engine:
- format:
- triangles:
- LOD:
- collision:
- materials:
- textures:

## Scene constraints
- do not modify:
- reuse:
- collection:
- naming:

## Required checkpoints
- blockout ortho
- primary detail
- shading
- game-ready
- export

## Acceptance
- all MUST features pass
- dimensions within tolerance
- no shading errors
- runtime contract pass


---

## FILE: `06_prompts/62_REVIEWER_PROMPT.md`

# Reviewer Prompt

Jesteś niezależnym reviewerem assetu 3D.

Nie poprawiaj modelu.

Dane:
- Feature Contract,
- referencja,
- rendery kontrolne,
- Scene Snapshot,
- mesh/material/runtime stats.

Dla każdego Feature ID zwróć:
- PASS / MINOR / FAIL,
- dowód,
- rodzaj błędu: silhouette / proportion / geometry / shading / material / runtime,
- minimalną korektę,
- etap, do którego należy wrócić.

Dodatkowo sprawdź:
- czy agent nie dodał niezatwierdzonych elementów,
- czy optymalizacja nie usunęła cechy,
- czy model nie jest przesadnie gęsty,
- czy stack modifierów pozostaje sensowny,
- czy pivot/transform/export są poprawne.

Nie używaj oceny "wygląda dobrze".
Każda ocena musi wskazywać kryterium.


---

## FILE: `06_prompts/63_REPAIR_PROMPT.md`

# Repair Prompt

Napraw tylko wskazane błędy.

Input:
- asset id,
- failed Feature IDs,
- expected state,
- current state,
- affected objects,
- last valid checkpoint.

Reguły:
1. Nie przebudowuj całego assetu.
2. Nie zmieniaj features oznaczonych PASS.
3. Nie zmieniaj naming/pivot/material bez związku z błędem.
4. Przed naprawą utwórz recovery point.
5. Po naprawie uruchom tylko testy związane z affected features oraz test regresji dla sąsiednich MUST.
6. Jeśli naprawa wymaga zmiany strategii, wróć do PLAN zamiast improwizować.


---

## FILE: `06_prompts/64_RECONSTRUCTION_PLANNER_PROMPT.md`

# Reconstruction Planner Prompt

Jesteś plannerem rekonstrukcji 3D.

Nie modyfikuj sceny.

Masz:
- source references,
- concept sheet,
- project/engine contract.

Wykonaj:
1. segmentację źródeł,
2. classification widoków,
3. evidence ledger,
4. View Authority Matrix,
5. conflicts,
6. dimension graph,
7. feature contract,
8. landmarks,
9. object decomposition,
10. feature-to-strategy map,
11. QA plan,
12. ambiguity list.

Nie wypełniaj braków detalami z wyobraźni.
Każda inferowana wartość musi mieć confidence.


---

## FILE: `06_prompts/65_RECONSTRUCTION_INSPECTOR_PROMPT.md`

# Reconstruction Inspector Prompt

Nie poprawiaj modelu.

Porównaj model z:
- dimension graph,
- canonical views,
- landmarks,
- Feature Contract.

Kolejność:
1. hard dimensions,
2. silhouette,
3. negative spaces,
4. primary landmarks,
5. MUST D2,
6. rear/bottom,
7. material segmentation,
8. surface,
9. runtime regressions.

Zwróć dla FAIL:
- evidence id,
- feature id,
- view,
- measured error,
- likely root cause,
- earliest stage to return to.


---

## FILE: `06_prompts/66_RECONSTRUCTION_REPAIR_PROMPT.md`

# Reconstruction Repair Prompt

Masz naprawić wyłącznie wskazany reconstruction failure.

Przed zmianą:
- znajdź feature owner,
- constraints,
- dependencies,
- accepted checkpoint.

Wykonaj:
- minimalną zmianę parametryczną,
- nie ruszaj QA cameras,
- nie zmieniaj locked dimensions bez jawnego powodu.

Po zmianie:
- target validation,
- adjacent MUST regression,
- jeśli zmiana D0/D1: pełny multi-view gate.


---

## FILE: `06_prompts/67_CONCEPT_SHEET_INGEST_PROMPT.md`

# Concept Sheet Ingest Prompt

Przeanalizuj planszę referencyjną bez modelowania.

Najpierw sprawdź `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md`. Jeżeli istnieje ważny cache dla tego samego źródła, nie segmentuj i nie mierz ponownie zwalidowanych regionów.

Zidentyfikuj:
- wszystkie subviews,
- dimensions,
- material samples,
- real asset branding,
- annotations that are not part of asset,
- detail crops,
- inconsistencies.

Dla technical concept sheet stosuj kolejność autorytetu z `10_reconstruction/160_BLUEPRINT_AND_TECHNICAL_DRAWING_MODE.md`.

Wynik:
- segment manifest / Reference Registry,
- evidence ledger,
- view authority proposal,
- locked dimensions,
- cross-view aggregate consistency,
- unresolved ambiguity,
- cache update.

Nie interpretuj marketingowych podpisów jako geometrii.
Nie traktuj dimension lines, leaders, arrows ani separatorów layoutu jako silhouette.

Nie zwracaj pełnych pixel arrays, per-row profiles ani długich threshold traces. Przy niejednoznaczności wskaż minimalny ROI wymagający diagnostyki.

Po `ANALYZE: PASS` zakończ szeroką eksplorację planszy. Dalsza analiza musi dotyczyć konkretnego feature ID, metric ID, view conflict lub failing ROI.


---

## FILE: `07_examples/70_HARD_SURFACE_PROP_EXAMPLE.md`

# Example — Hard-Surface Street Prop

## Brief

Statyczny miejski prop sci-fi:
- czytelny z 2–8 m,
- gracz może obejść go dookoła,
- kilka materiałów,
- produkowany masowo,
- powinien nadawać się do instancjonowania.

## Feature Contract

| ID | Priority | Feature | Build |
|---|---|---|---|
| F001 | MUST | charakterystyczna sylwetka korpusu | blockout mesh |
| F002 | MUST | wcięty panel frontowy | inset/boolean |
| F003 | MUST | metalowa rama | separate mesh |
| F004 | SHOULD | szczelina montażowa | geometry/normal |
| F005 | SHOULD | logo | decal/texture |

## Strategy

1. Korpus z prymitywu.
2. Panel jako osobna część lub boolean recess.
3. Rama jako oddzielny mesh, aby niezależnie kontrolować materiał.
4. Bevel dopiero po zaakceptowaniu proportions.
5. Neutral shading checkpoint.
6. UV/material.
7. LOD1: uproszczone bevels i usunięte drobne szczeliny.
8. Collision: prosty hull/box decomposition.

## Błąd, którego należy unikać

Nie generuj mikrodetali przed sprawdzeniem bryły. Poprawianie szerokości całego korpusu po detalach powoduje regresje i kolejne kosztowne operacje.


---

## FILE: `07_examples/71_MODULAR_ARCHITECTURE_EXAMPLE.md`

# Example — Modular Architecture Element

## Goal

Moduł fasady używany wielokrotnie.

## Critical contract

- dokładna szerokość modułu,
- dokładna wysokość modułu,
- krawędzie łączenia bez wystających beveli,
- pivot na dolnym rogu siatki,
- powtarzalny trim/material,
- tylna część uproszczona, jeśli nigdy nie jest widoczna.

## Build

1. Ustal grid.
2. Utwórz bounding box modułu.
3. Zablokuj interface edges.
4. Dodaj design tylko wewnątrz bezpiecznej strefy.
5. Nie modyfikuj interface edges przez późniejsze booleans/bevels.
6. Zbuduj end-cap jako osobny wariant.
7. Zbuduj corner module osobno.

## QA

Test:
- A+A,
- A+B,
- A+A+A+A,
- widok pod ostrym kątem,
- brak szczelin,
- brak z-fightingu,
- spójna tekstura.

## Runtime

Moduły powinny wspierać instancing.
Jeżeli unikalne elementy dekoracyjne są potrzebne, dodaj je jako osobne instancje zamiast duplikować cały moduł.


---

## FILE: `07_examples/72_COMPLEX_PROP_WITH_MATERIALS_EXAMPLE.md`

# Example — Complex Prop with Multiple Materials

## Decomposition

- structural body,
- soft/contact surface,
- metallic shell,
- glass/display,
- emissive insert,
- fasteners.

## Material logic

Każda część ma oddzielny materiał tylko jeśli wymaga innego shader behavior.
W przeciwnym razie rozważ wspólny atlas/material.

## Build order

1. body,
2. major cutouts,
3. separate shells,
4. contact/soft regions,
5. screen/glass,
6. fasteners,
7. bevel/shading,
8. UV/material,
9. optimization.

## Glass

Nie zakładaj, że przezroczysty Principled material zachowa się identycznie w runtime.
Sprawdź docelowy alpha/transmission model.

## Emissive

Emissive insert:
- może być płaską powierzchnią,
- może wymagać bloom/light w runtime osobno,
- nie musi potrzebować dużej ilości geometrii.

## LOD

W dalszych LOD:
- śruby -> normal/decal/remove,
- małe gaps -> texture,
- glass frame -> uproszczony,
- podstawowa silhouette bez zmian.


---

## FILE: `07_examples/73_LAFAR_STREET_BENCH_RECONSTRUCTION_BENCHMARK.md`

# Benchmark — Lafar Street Bench / ACS-BCH-200

## Purpose

Pierwszy benchmark pełnej warstwy rekonstrukcji 1:1.

Źródło:
concept sheet `LAFAR STREET BENCH — CIVIC SEATING MODULE`.

## Explicit dimensions visible on sheet

- total width: 2000 mm,
- total depth: 550 mm,
- total height: 820 mm,
- side/seat-height dimension shown: 460 mm.

Te wartości są `HARD LOCK`, o ile nowsza zatwierdzona referencja ich nie zmieni.

## Canonical views available

- hero,
- front,
- side,
- top,
- rear,
- bottom/underside,
- detail close-up.

## Material evidence

Plansza pokazuje rodziny:
- matte graphite powder coat,
- brushed aluminum,
- dark titanium composite,
- microbead texture,
- cool-blue accent lighting.

Nazwy materiałów są evidence projektowym; fizyczna interpretacja shaderów musi zostać zwalidowana wizualnie.

## High-level MUST features

### F001
Global width/depth/height.

### F002
Masywne boczne housings pełniące rolę nóg/podłokietników.

### F003
Siedzisko pomiędzy bocznymi housings.

### F004
Pochylone oparcie o niskim, szerokim profilu.

### F005
Metaliczne/aluminiowe zewnętrzne trimy biegnące po bocznych częściach.

### F006
Wąski info strip przy górnej części frontu oparcia.

### F007
Prawostronny integrated utility panel.

### F008
Cool-blue underglow przy podstawie.

### F009
Rear panel + logo ASTERA CIVIC SYSTEMS.

### F010
Underside/service-panel layout obecny na bottom view.

### F011
Charakterystyczna otwarta negative space pod siedziskiem.

### F012
Rounded/chamfered product edge language.

## Initial object decomposition proposal

- `SM_Lafar_Bench_SeatCore`
- `SM_Lafar_Bench_BackrestCore`
- `SM_Lafar_Bench_SideHousing_L`
- `SM_Lafar_Bench_SideHousing_R`
- `SM_Lafar_Bench_Trim_L`
- `SM_Lafar_Bench_Trim_R`
- `SM_Lafar_Bench_InfoStrip`
- `SM_Lafar_Bench_UtilityPanel`
- `SM_Lafar_Bench_Underglow`
- `SM_Lafar_Bench_RearPanel`
- `SM_Lafar_Bench_Underside`
- `DEC_Lafar_Bench_AsteraRear`
- optional shared fastener instances.

To jest plan startowy, nie wymóg jednego konkretnego podziału runtime.

## View authority proposal

### Width
FRONT/TOP/REAR + numeric 2000 mm.

### Depth
SIDE/TOP + numeric 550 mm.

### Height
FRONT/SIDE/REAR + numeric 820 mm.

### 460 mm dimension
SIDE/FRONT evidence; należy precyzyjnie ustalić, do której powierzchni odnosi się marker przed użyciem jako constraint lokalny.

### Backrest angle
SIDE.

### Rear logo
REAR.

### Underside
BOTTOM.

### Edge/material character
HERO + DETAIL + palette.

## Important ambiguity list

Arkusz nie podaje bezpośrednio:
- dokładnego kąta oparcia,
- szerokości side housing,
- grubości oparcia,
- promieni wszystkich narożników,
- szerokości trimu,
- dokładnych wymiarów utility panel,
- dokładnej geometrii portów,
- dokładnej głębokości panel gaps,
- dokładnej geometrii wewnętrznej underside.

Te parametry należy mierzyć z kalibrowanych widoków i oznaczać `DERIVED`, a nie udawać jawnych wartości.

## Required reconstruction checkpoints

### B0 — Registered references
Wszystkie ortho cropy skalibrowane.

### B1 — D0
Tylko total bounds + silhouette + negative space.

### B2 — D1
Seat/back/side profiles.

### B3 — D2
Trim, info strip, utility, rear/bottom panels.

### B4 — D3
Branding, ports, fasteners.

### B5 — Surface
Material segmentation i lookdev.

### B6 — Runtime
LOD/collision/export bez utraty MUST.

## Failure traps deliberately tested

- model dopasowany tylko do hero view,
- pominięcie underside,
- mirror utility panel na obie strony,
- niewłaściwa szerokość po bevel,
- dodanie losowych sci-fi panel lines,
- logo jako błędny tekst,
- underglow użyty do maskowania złej podstawy,
- zbyt duży bevel zmieniający side silhouette.

## Benchmark metrics

- 4 explicit dimension errors,
- canonical view silhouette errors,
- MUST feature pass rate,
- landmark reprojection error,
- number of unauthorized features,
- tool calls,
- failed API calls,
- repair count,
- runtime triangle/material stats.

## Benchmark target

Nie przyjmuj wyniku "looks good".
Benchmark kończy się dopiero po przejściu reconstruction Definition of Done.


---

## FILE: `07_examples/74_LAFAR_CIVIC_BOLLARD_BENCHMARK.md`

# Benchmark — Lafar Civic Bollard

## Status

Real end-to-end agent run used as a BlenderSkill v0.5 regression benchmark.

Asset:
- Lafar Civic Bollard;
- Astera Civic Systems;
- technical concept sheet with hero/front/side/top/rear/bottom/detail views;
- game-ready hard-surface civic prop.

This benchmark exists to measure **quality and efficiency**, not just whether an asset file can be produced.

---

# Baseline run

Approximate language-model usage:

```text
~60k tokens total
```

Human visual evaluation of the final Blender result:

```text
9 / 10
```

Primary remaining visual weakness noted by the reviewer:
- surface/material reads too clean and uniform compared with the reference;
- final neon/bloom appearance still depends partly on runtime engine/post-processing.

---

# Final geometric/runtime outputs from baseline

```yaml
asset:
  bounds_mm: [210, 210, 1050]
  origin: BASE_CENTER
  rotation: [0, 0, 0]
  scale: [1, 1, 1]

lods:
  LOD0_tris: 2716
  LOD1_tris: 1152
  LOD2_tris: 480
  LOD3_tris: 128
  collision_tris: 88

mesh_summary:
  duplicate_vertices: 0
  loose_vertices: 0
  edges_over_2_faces: 0
  uv_present: true
```

Major locked dimensions:
- overall height = 1050 mm;
- main body diameter = 140 mm;
- base diameter = 210 mm;
- measured service collar ≈ 178.9 mm diameter.

---

# Source-authority behavior

The run correctly used:

```text
explicit numeric dimensions
> orthographic technical views
> detail views
> perspective hero
> approximate prose ranges
```

The technical sheet's front/side projections were measured separately by axis because the sheet showed approximately 13% vertical anisotropy relative to horizontal scale.

This is a positive benchmark behavior.

---

# Real defects caught by QA

The run found multiple problems that survived an initial visual "looks good" impression:

1. loose vertices in the rear service panel;
2. duplicated vertices in the light diffuser;
3. assembly width of 211 mm instead of required 210 mm;
4. anchor/bolt recess geometry extending outside the available flange annulus;
5. base accent emitter present in data but hidden behind the host wall and therefore invisible;
6. decal plates lost during LOD/export because importing the builder triggered destructive top-level `build()` side effects;
7. graphite material rendered too bright under the initial QA lighting setup.

Positive benchmark criterion:

> The agent must diagnose these classes with measurable evidence rather than repeatedly adjusting values by eye.

---

# Questionable baseline decision to prevent in v0.5+

The rear service panel was increased from 0.6 mm to 1.2 mm proud because it was difficult to read in flat lighting.

That is not a safe general reconstruction rule.

v0.5 requirement:
- first separate lighting/material readability from geometric evidence;
- use neutral/matcap/edge evidence;
- change geometric depth only if reference evidence permits the change.

A feature must not become physically larger merely to compensate for a poor QA light rig.

---

# Baseline incompleteness

Despite successful modeling, LOD generation and export, the run explicitly did **not** finish:
- BaseColor/Normal/ORM/Emissive runtime texture bake;
- small details intended for normal-map representation;
- full underside reconstruction from the bottom-view reference;
- project AssetCatalog integration.

Therefore the correct completion classification is not unconditional `DONE`.

Expected v0.5 classification:

```text
RECONSTRUCTION_COMPLETE: PASS
MODELING_COMPLETE: PASS
GAME_READY_COMPLETE: PARTIAL/FAIL until bake/runtime binding is done
PIPELINE_INTEGRATED: FAIL until catalog integration is done
```

---

# Material benchmark

The final asset should not rely on uniform procedural noise alone.

Reference-compatible dark civic materials should preserve:
- low-frequency roughness variation;
- restrained microtexture;
- manufacturing direction where applicable;
- subtle protected-zone dirt;
- sparse plausible wear;
- material-specific variation rather than global random grunge.

The quality target is:

```text
not sterile
not visibly procedural
not heavily damaged
```

The asset should still read as maintained civic infrastructure.

---

# Emissive benchmark

The blue guidance ring and lower marker must be separated into:

```text
asset-side emitter correctness
runtime-side glow/bloom correctness
```

Asset PASS requires:
- correct geometry/mask;
- visible emitter;
- stable blue/cyan hue;
- exported emissive data.

Runtime glow remains `UNVERIFIED` until Engine Profile/post-processing are tested.

---

# Efficiency failures from baseline

The run consumed excessive context partly because it:
- echoed large generated Python files into model context;
- built reusable lathe/profile/QA infrastructure ad hoc;
- returned large diagnostic datasets during image/silhouette analysis;
- performed several compatibility discoveries during production rather than preflight;
- tuned LODs iteratively instead of using reusable cost models/executors from the start.

v0.5 must use:
- Code Artifact and Patch Protocol;
- Tool Output Budget;
- Task Packs;
- Reference Analysis Cache;
- `AXISYMMETRIC_PROFILE` for rotational components;
- Mesh Contract Validator;
- Blender 5.1 Compatibility Matrix;
- explicit completion levels.

---

# v0.5 benchmark targets

Quality is the hard gate. Efficiency targets apply only if quality does not regress.

### Hard gates
- no regression in locked dimensions;
- all reference-critical silhouettes/features pass;
- no hidden emitter feature;
- no destructive builder import side effects;
- all LOD budgets pass;
- exported decal/material references survive;
- completion level reported truthfully.

### Efficiency targets

Baseline total: ~60k tokens.

Target:
- at least 35% total-token reduction on an equivalent run;
- preferred total <= 35k tokens;
- stretch target <= 25k without quality regression;
- no full-source echo for build scripts >120 lines;
- no raw per-row/pixel profile dump unless localized DIAGNOSTIC escalation requires it;
- no more than one corrected retry for the same strategy/preconditions.

### Executor-use target

The run should preferentially reuse:
- `AXISYMMETRIC_PROFILE`;
- `MESH_VALIDATE`;
- runtime compatibility helper;
- QA isolation helper;
- reference measurement executor when validated in the active runtime.

Agent-generated local implementations must be justified when an appropriate reusable executor already exists.

---

# Scorecard

Recommended benchmark score:

```text
Reference fidelity        30%
Runtime correctness       20%
Mesh/LOD/export quality   15%
Material/surface finish   10%
Completion truthfulness   10%
Tool/retry efficiency     10%
Context/token efficiency   5%
```

A token-efficient but visually inferior model does not beat the baseline.

---

# Lessons promoted to canonical library

This benchmark is the evidence source for v0.5 additions covering:
- completion levels;
- Blender 5.1 runtime compatibility traps;
- floating-detail visibility/occlusion rules;
- civic material breakup;
- emissive authoring/runtime separation;
- bake gate;
- asset catalog integration;
- executable artifact/context discipline.


---

## FILE: `07_examples/75_LAFAR_CIVIC_BOLLARD_BAKE_REGRESSION_BENCHMARK.md`

# Benchmark — Lafar Civic Bollard Bake/Runtime Closure

## Purpose

This benchmark captures the v0.5 continuation from accepted bollard geometry into surface finishing, baking and runtime packaging.

It exists because the agent's geometric/reconstruction quality was already high, while the bake/runtime phase still consumed excessive reasoning/tool iterations.

---

# Baseline capture

User-reported token use at the captured point:

```text
~36k tokens
```

The agent had still not fully finished the bake/runtime closure when the transcript was captured.

The supplied transcript contains approximately:
- 20 Blender Python execution calls;
- repeated bake reruns;
- multiple corrections to bake/channel/UV/export infrastructure.

This benchmark is stage-specific. It does not replace the earlier full bollard benchmark.

---

# Positive v0.5 behavior

The v0.5 knowledge layer successfully caused the agent to:
- fetch the current BlenderSkill repository;
- read the completion/bake/material modules;
- recognize that material bake does not always require a separate high-poly;
- use the packaged mesh validator;
- distinguish `OPEN_ASSEMBLY_PART`, `SURFACE_DETAIL` and `CLOSED_SOLID`;
- verify underside normal direction;
- discover engine LOD/collision conventions;
- improve maintained-civic material breakup;
- keep LODs inside target budgets after repair;
- inspect exported glTF nodes/materials/images instead of trusting export alone.

This proves v0.5 improved decision quality.

---

# Failures that v0.6 must prevent

## B01 — silent bake cancellation

Observed pattern:

```text
No active and selected image texture node found...
bpy.ops.object.bake -> {'CANCELLED'}
```

The first pipeline treated file creation/execution as if bake succeeded and produced degenerate maps.

v0.6 requirement:
- bake executor checks operator result;
- verifies target node in every contributing material;
- rejects cancelled/degenerate output immediately.

## B02 — target node selection ordering

Target image node was active but `select == false`.

Correct sequence discovered:

```text
deselect all nodes
-> target.select = true
-> nodes.active = target
```

v0.6 requirement: encoded in reusable bake executor, not rediscovered per asset.

## B03 — AO contaminated by unrelated scene geometry

A viewport-hidden but render-visible default Cube enclosed the asset and made AO nearly black.

v0.6 requirement:
- ray-dependent bake uses scene isolation;
- `hide_viewport` is never treated as equivalent to `hide_render`.

## B04 — wrong BaseColor semantics for metal

Blender DIFFUSE bake made brushed aluminium read too dark/black.

v0.6 requirement:
- authored Principled Base Color is extracted directly for metallic-roughness runtime BaseColor;
- bake channel semantics are explicit.

## B05 — emissive false-white/clipping

Baking emission incorrectly:
- ignored zero emission strength on non-emitters;
- produced white/unwanted signal;
- or multiplied color by authoring strength until channels clipped and hue was lost.

v0.6 requirement:
- emissive output accounts for both color and strength;
- uses explicit normalization/reference strength;
- validates approved emitter UV regions and hue/clipping.

## B06 — metallic channel extraction failure

Scalar channel extraction temporarily produced metallic = 1 across the atlas.

v0.6 requirement:
- direct scalar-channel extraction helper;
- region-aware validation of metal vs dielectric regions.

## B07 — UV assignment depended on Blender object names

A second build produced names such as `.001`, causing atlas lookup by full object name to miss. UV assignment silently failed and parts overlapped 0..1.

v0.6 requirement:
- semantic part ID owns atlas mapping;
- `.001` is never canonical identity;
- missing UV assignment is hard FAIL.

## B08 — bake source and runtime LOD UV diverged

Atlas assignment was applied to the temporary bake source but not the exported LODs.

Result:
- textures were valid;
- exported runtime mesh sampled them incorrectly.

v0.6 requirement:
- UV contract is applied in the shared build/LOD path;
- bake source and every consuming LOD report the same `UV_CONTRACT_ID`.

## B09 — decal atlas contamination

Decal plates used a separate project decal atlas but were joined into the structural bake source.

v0.6 requirement:
- external decal/dynamic-display UV owners are excluded unless explicitly remapped.

## B10 — import-time side effects

Loading build/export files for helper functions triggered production work or interacted destructively with working collections.

v0.6 requirement:
- import-safe module pattern;
- guarded entrypoints;
- explicit scratch collection ownership.

## B11 — export scratch cleared source LODs

A helper used the same reset/clear collection for temporary mirror copies and for source LODs.

v0.6 requirement:
- source, bake scratch, export scratch and QA scratch ownership are separate.

## B12 — project packaging rediscovered from sibling scripts

The agent read project exporter code to discover:
- one glTF with multiple `_LODn` nodes;
- collision convention;
- X-mirror compensation due engine handedness and readable branding.

Useful once, expensive repeatedly.

v0.6 requirement:
- persist verified packaging facts in Project Asset Pipeline/Engine Profile;
- subsequent assets consume the profile.

## B13 — full rebakes after local channel repairs

Many fixes affected only one channel, yet the whole multi-pass bake pipeline was rerun.

v0.6 requirement:
- dirty-stage dependency cache;
- accepted channels are reused until a dependency invalidates them.

## B14 — tool timeout during expensive bake

A Blender/MCP request timed out while the bake could continue/complete.

v0.6 requirement:
- timeout -> inspect job/artifact state;
- do not duplicate expensive work without proof of failure.

---

# v0.6 stage targets

Starting from accepted Level B/model geometry:

```yaml
GAME_READY_FINISH_target:
  token_budget_preferred: <= 15000
  blender_python_mutation_calls_preferred: <= 10
  full_multichannel_bake_runs: <= 2
  silent_cancelled_bakes_accepted: 0
  missing_uv_contracts_accepted: 0
  exported_runtime_qa_required: true
```

These are benchmark targets, not universal hard limits for every asset.

A more complex animated/dynamic-display asset may legitimately exceed them, but must still avoid rediscovering solved infrastructure.

---

# Required evidence for PASS

```text
UV contract PASS
BaseColor PASS
Normal PASS
AO PASS
Roughness PASS
Metallic PASS
ORM packing PASS
Emissive PASS
Runtime material binding PASS
LOD budgets PASS
Runtime module packaging PASS
Export readback PASS
Baked-runtime visual QA PASS
Completion gate PASS
```

---

# Release criterion

v0.6 is better than v0.5 only if an equivalent bake/runtime closure:
- uses fewer expensive/repeated operations;
- avoids the failure classes above;
- preserves or improves visual/runtime quality;
- reaches the requested completion level instead of stopping during bake debugging.


---

## FILE: `07_examples/76_LAFAR_CIVIC_BOLLARD_PIPELINE_INTEGRATION_REGRESSION_BENCHMARK.md`

# Lafar Civic Bollard — Pipeline Integration Regression Benchmark

## Purpose

This benchmark records the final continuation of the real Astera/Lafar civic bollard run after v0.6 bake/runtime closure work.

User-reported cost for this final continuation: approximately **45k additional tokens**. Combined with the preceding approximately 36k-token continuation segment, the post-v0.5 completion work consumed roughly **81k tokens**.

The asset eventually reached `PIPELINE_INTEGRATED`, but the path exposed several silent or falsely interpreted failure classes that v0.7 must eliminate.

## Final accepted runtime facts

```yaml
asset: Astera civic bollard
runtime_module: astera_bollard.gltf
lod_packaging: ONE_FILE_MULTI_NODE
lods:
  LOD0_tris: 2844
  LOD1_tris: 1152
  LOD2_tris: 480
  LOD3_tris: 128
collision_tris: 88
hard_dimensions_mm: [210, 210, 1050]
runtime_asset_root: <repo>/Assets/GameAssets
catalog_id: astera_bollard
engine_loader_test: ModelTests / Engine::Model::Load
completion: PIPELINE_INTEGRATED
```

## Observed v0.6-era failure classes

### F1 — stale Blender image datablock

The baked PNGs on disk were correct, UVs were correct and material links appeared correct, but the runtime material still rendered old pixels.

Cause:

```text
bpy.data.images.get(...)
-> reused existing datablock
-> external file had newer accepted bake
-> image datablock was not reloaded
```

Required v0.7 behavior:
- disk-vs-memory authority is explicit;
- accepted disk bake triggers image synchronization/reload before runtime QA;
- stale image cache routes to binding/cache repair, not rebake/UV repair.

### F2 — exported hard dimension regression

Round-trip import found LOD0 at 1048 mm instead of the technical-sheet 1050 mm.

Cause:
- underside geometry/profile change;
- base fillet removed the true contact point;
- source looked plausible but exported bounds failed the hard contract.

Required v0.7 behavior:
- post-export invariants include dimensions and ground datum;
- export round-trip runs before catalog completion;
- repair dirties only dependent stages through the pipeline DAG.

### F3 — Blender import was not engine proof

Blender successfully imported the glTF, but Level D remained correctly unresolved until the custom engine loader was exercised.

Required v0.7 behavior:

```text
Blender round-trip = Level C evidence
Engine production loader/test = Level D evidence
```

### F4 — wrong but valid filesystem tree

The asset was exported to:

```text
<repo>/GameAssets/...
```

while the engine read from:

```text
<repo>/Assets/GameAssets/...
```

Both looked plausible and existed.

Required v0.7 behavior:
- runtime asset root resolved from project/build/engine authority before export;
- no per-script root guessing;
- project profile stores the verified root;
- wrong sibling root is explicitly forbidden for this project profile.

### F5 — false green test from shell pipeline

Unsafe invocation:

```bash
./ModelTests.exe 2>&1 | tail -20
echo $?
```

reported the status of `tail`, not necessarily `ModelTests.exe`.

An apparent `EXIT=0` was therefore meaningless.

Required v0.7 behavior:
- capture executable exit status directly or use `pipefail` correctly;
- distinguish assertion failure from crash/abort;
- no Level D PASS from ambiguous test status.

### F6 — invalid first bite-test interpretation

A deliberately broken expected triangle count initially produced exit 3 because the process aborted while loading the asset from the wrong root. That was incorrectly interpreted as proof the assertion 'bit'.

After the runtime path was fixed:
- wrong expected tris -> clean `EXIT=1`;
- expected regression message appeared;
- expectation restored -> `EXIT=0`.

Required v0.7 behavior:
- bite test must fail for the intended assertion;
- crash/loader failure is not an assertion bite.

### F7 — unnecessary pipeline replay

After a local underside geometry repair the workflow re-executed build, decals, all bake passes and export as a manual chain.

This bypassed the spirit of the v0.6 Dirty-Stage Cache.

Required v0.7 behavior:
- pipeline execution is DAG-planned;
- independent clean stages are reused;
- stage execution/reuse counts are benchmarked.

### F8 — repeated build-system discovery

The agent spent multiple shell calls locating CMake configuration, test binaries and the existing `ModelTests` pattern.

Required v0.7 behavior:
- project profile stores build directory, narrow test target, binary, loader and catalog source;
- future assets consume the profile directly.

## What v0.6 did well

v0.6 concepts materially helped:
- runtime bake closure was completed instead of deferred;
- semantic channel bake rules produced correct BaseColor/ORM/Normal/Emissive;
- completion gate correctly refused Level D while runtime import remained unverified;
- final accepted asset had all four LODs in budget and correct hard dimensions after repair.

The problem was no longer primarily missing knowledge. It was **execution proof, cache coherence, project-profile completeness and enforced stage reuse**.

## v0.7 regression requirements

A comparable future asset should satisfy:

```yaml
v0_7_targets:
  false_green_test_results: 0
  ambiguous_runtime_roots: 0
  stale_image_datablock_regressions: 0
  full_pipeline_restarts_after_local_repair: 0
  blender_import_used_as_level_d_proof: 0
  new_engine_assertions_with_valid_bite_test: 100_percent_when_safe
  project_profile_rediscovery_calls: 0_when_profile_matches
```

Preferred efficiency targets after `GAME_READY_COMPLETE` is already reached:

```yaml
pipeline_integration_finish:
  preferred_tokens: <= 10000
  preferred_project_discovery_calls: <= 2
  full_texture_rebakes: 0_unless_dependencies_changed
  engine_test_runs:
    green_baseline_or_final: <= 2
    controlled_bite_test: <= 1_failure_plus_restore
```

These are benchmark goals, not universal hard limits.

## Release implication

v0.7 is successful only if the next benchmark demonstrates that solved infrastructure is reused:
- canonical runtime path comes from profile;
- stage DAG prevents unrelated recomputation;
- post-export invariants catch dimension/contact drift early;
- image cache freshness is explicit;
- Level D is closed only by a trustworthy target-engine test oracle.

---

## FILE: `08_scripts/80_SCENE_AUDIT_SNIPPETS.md`

# Scene Audit Snippets

Poniższe fragmenty są wzorcami, nie gotowym frameworkiem.

## Version and context

```python
import bpy

print("Blender:", bpy.app.version_string)
print("Scene:", bpy.context.scene.name)
print("Mode:", bpy.context.mode)
print("Active:", bpy.context.view_layer.objects.active.name if bpy.context.view_layer.objects.active else None)
print("Selected:", [o.name for o in bpy.context.selected_objects])
```

## Object inventory

```python
for obj in bpy.context.scene.objects:
    print(
        obj.name,
        obj.type,
        tuple(round(v, 4) for v in obj.dimensions),
        tuple(round(v, 4) for v in obj.scale),
    )
```

## Mesh stats

```python
for obj in bpy.context.scene.objects:
    if obj.type == "MESH":
        me = obj.data
        print(
            obj.name,
            "verts", len(me.vertices),
            "edges", len(me.edges),
            "polys", len(me.polygons),
            "uv", [uv.name for uv in me.uv_layers],
            "mats", len(obj.material_slots),
        )
```

## Modifier audit

```python
for obj in bpy.context.scene.objects:
    if obj.modifiers:
        print(obj.name)
        for m in obj.modifiers:
            print(" ", m.name, m.type, m.show_viewport, m.show_render)
```

## Asset tag

```python
def find_asset(asset_id):
    return [
        o for o in bpy.data.objects
        if o.get("ai_asset_id") == asset_id
    ]
```


---

## FILE: `08_scripts/81_MESH_VALIDATION_SNIPPETS.md`

# Mesh Validation Snippets

## Negative scale

```python
bad = []
for obj in bpy.context.scene.objects:
    if obj.type == "MESH":
        if any(s < 0 for s in obj.scale):
            bad.append(obj.name)
print("Negative scale:", bad)
```

## Zero scale

```python
bad = []
for obj in bpy.context.scene.objects:
    if any(abs(s) < 1e-8 for s in obj.scale):
        bad.append(obj.name)
print("Zero scale:", bad)
```

## Duplicate final names heuristic

```python
import re
suspicious = [
    o.name for o in bpy.data.objects
    if re.search(r"\.\d{3}$", o.name)
]
print("Suffix names:", suspicious)
```

## BMesh manifold audit

```python
import bpy, bmesh

def mesh_report(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    try:
        non_manifold_edges = [e for e in bm.edges if not e.is_manifold]
        boundary_edges = [e for e in bm.edges if e.is_boundary]
        return {
            "verts": len(bm.verts),
            "edges": len(bm.edges),
            "faces": len(bm.faces),
            "non_manifold_edges": len(non_manifold_edges),
            "boundary_edges": len(boundary_edges),
        }
    finally:
        bm.free()
```

## Topology intent rule

Otwarte siatki mogą mieć poprawne boundary edges, ale tylko wtedy, gdy kontrakt obiektu jawnie na to pozwala.

Każdy mesh przechodzący finalną walidację musi mieć topology intent:

```text
CLOSED_SOLID
OPEN_ASSEMBLY_PART
SURFACE_DETAIL
COLLISION
```

`CLOSED_SOLID` i domyślnie `COLLISION` wymagają:
- `boundary_edges == 0`;
- `non_manifold_edges == 0`;
- brak loose geometry;
- brak zero-area faces;
- brak nieuzasadnionych duplicate vertex positions.

`OPEN_ASSEMBLY_PART` może mieć boundary tylko wtedy, gdy boundary jest świadomie zakrywane/zamykane przez inny element assembly i taka polityka jest zapisana w Game Asset Contract.

`SURFACE_DETAIL` może być otwartą geometrią, ale wymaga osobnego testu widoczności/occlusion i z-fighting.

Walidator nie może powiedzieć ogólnie `all mesh checks pass`, jeśli boundary istnieją, a topology intent nie został określony.

## Canonical validator

Preferuj semantic skill `MESH_VALIDATE`:
- contract: `08_scripts/92_MESH_CONTRACT_VALIDATOR_PATTERN.md`;
- candidate executor: `executors/mesh_validate.py`.

Zwracaj compact report, nie listę wszystkich krawędzi/wierzchołków, chyba że DIAGNOSTIC wymaga konkretnego failing region.


---

## FILE: `08_scripts/82_EXPORT_VALIDATION_SNIPPETS.md`

# Export Validation Snippets

## Pre-export manifest

Przed exportem utwórz manifest:
- object names,
- types,
- bounds,
- material slots,
- animation data,
- parent hierarchy.

```python
import bpy

def manifest(objects):
    out = []
    for obj in objects:
        out.append({
            "name": obj.name,
            "type": obj.type,
            "parent": obj.parent.name if obj.parent else None,
            "dimensions": [float(v) for v in obj.dimensions],
            "materials": [slot.material.name if slot.material else None for slot in obj.material_slots],
            "has_animation": bool(obj.animation_data),
        })
    return out
```

## Post-export principle

Po eksporcie nie zakładaj poprawności na podstawie braku exception.

Porównaj:
- liczbę expected nodes,
- bounds,
- materiały,
- texture references,
- animation clips,
- root hierarchy.

Jeżeli pipeline posiada importer round-trip:
1. export do pliku tymczasowego,
2. import do czystej sceny,
3. wykonaj ten sam manifest,
4. porównaj z tolerancją.

Nie wykonuj round-trip na głównej scenie.


---

## FILE: `08_scripts/83_QA_RENDER_SCRIPT_PATTERN.md`

# QA Render Script Pattern

## Cel

Generować identyczne rendery kontrolne między iteracjami bez zanieczyszczenia kadru obiektami spoza testowanego assetu.

## Profile

Przykładowe profile:
- `SILHOUETTE`
- `NEUTRAL`
- `MATCAP_EQUIVALENT`
- `MATERIAL`
- `WIREFRAME_CAPTURE`

## Camera registry

Kamery:
- front,
- side,
- top,
- rear,
- 3/4.

Nie twórz przypadkowej kamery przy każdym run.
Dla reconstruction reference camera ma być zapisana w registry/cache i ponownie używana.

## Scene isolation

Przed renderem:
- zidentyfikuj asset root/collection;
- zidentyfikuj QA rig;
- zapisz aktualne `hide_render`/collection visibility dla pozostałych obiektów;
- tymczasowo wyłącz unrelated renderable geometry/lights;
- po renderze przywróć stan w `finally`/transaction cleanup.

`hide_viewport=True` nie oznacza `hide_render=True`.
Nie usuwaj obcych obiektów tylko po to, aby uzyskać czysty render.

## Render-engine capability

Nie zakładaj nazwy enum render engine z pamięci.
Jeżeli skrypt ma działać między wersjami/kompilacjami, odczytaj dostępne enum values i wybierz wspierany profil.

Ta detekcja ma odbyć się raz na sesję/rig, nie przed każdym obrazem.

## File naming

```text
<asset_id>__<version>__<checkpoint>__<view>__<profile>.png
```

## Metadata

Obok renderu zachowaj JSON:
- camera transform,
- lens/ortho scale,
- resolution,
- engine,
- color management,
- QA lighting profile,
- asset bounds,
- feature set,
- scene isolation state/version.

## Pseudocode

```python
def render_checkpoint(asset_id, checkpoint, cameras, profiles):
    saved = isolate_scene_for_qa(asset_id)
    try:
        for camera in cameras:
            set_camera(camera)
            for profile in profiles:
                apply_qa_profile(profile)
                path = build_output_path(...)
                render(path)
                write_metadata(path)
    finally:
        restore_scene(saved)
```

## Compact output

The render tool should return paths and compact status, not the full render metadata or repeated source code:

```yaml
qa_render:
  status: PASS
  outputs:
    front: /tmp/...front.png
    hero: /tmp/...hero.png
  engine: BLENDER_EEVEE
  isolated_objects: 1
```

## Rule

QA render pipeline nie powinien permanentnie niszczyć materiałów, visibility ani innych ustawień sceny.
Użyj override/profile i po zakończeniu przywróć scenę.


---

## FILE: `08_scripts/84_VISUAL_DIFF_SCRIPT_PATTERN.md`

# Visual Diff Script Pattern

## Input

- accepted image,
- candidate image,
- optional ROI,
- optional silhouette masks.

## Recommended outputs

- absolute difference image,
- thresholded mask,
- changed pixel ratio,
- bounding box of differences,
- silhouette IoU if masks exist.

## Important

Nie porównuj dwóch obrazów, jeśli:
- resolution jest inne,
- camera jest inna,
- framing jest inne,
- QA profile jest inny.

## Feature-local diff

```text
feature_id -> ROI -> diff metrics -> PASS/MINOR/FAIL
```

## Regression detection

Jeżeli naprawa dotyczy F012:
- duża zmiana wewnątrz ROI F012 jest oczekiwana,
- zmiana w ROI innych MUST wymaga regresji check,
- duża zmiana poza wszystkimi expected ROI jest podejrzana.

## Storage

Przechowuj metryki, nie tylko obraz.
Pozwala to porównywać jakość kolejnych wersji agenta.


---

## FILE: `08_scripts/85_REFERENCE_IMAGE_REGISTRY_PATTERN.md`

# Reference Image Registry Pattern

```python
REFERENCE_REGISTRY = {
    "SEG_FRONT": {
        "path": "...",
        "projection": "ORTHO",
        "physical_width_m": 2.0,
        "axis": "FRONT",
        "approved": True,
    },
}
```

## Blender image empties

Reference images mogą być trzymane jako image empties.
Agent powinien:
- nadać stabilne nazwy,
- umieścić je w osobnej kolekcji,
- ustawić display opacity,
- lock transforms po kalibracji.

## Naming

`REF_<ASSET>_<VIEW>`

## Rule

Nie polegaj na active image w UI.
Trzymaj jawne referencje do objects/data-blocks.


---

## FILE: `08_scripts/86_QA_ORTHO_CAMERA_GENERATOR.md`

# QA Orthographic Camera Generator Pattern

## Cel

Tworzyć kamery z identycznym framingiem.

Pseudo-pattern:

```python
def ensure_ortho_camera(name, axis, target_bounds, margin=0.05):
    cam_obj = get_or_create_camera(name)
    cam_obj.data.type = "ORTHO"
    set_axis_rotation(cam_obj, axis)
    set_camera_position_outside_bounds(cam_obj, axis)
    cam_obj.data.ortho_scale = compute_required_scale(target_bounds, axis, margin)
    lock_camera_metadata(cam_obj)
    return cam_obj
```

## Important

`ortho_scale` zależy od widoku i aspect ratio.
Nie ustawiaj jednej wartości dla front i side bez obliczenia.

## Metadata

Zapisz custom properties:
- qa_view,
- reference_segment,
- calibrated,
- calibration_revision.


---

## FILE: `08_scripts/87_DIMENSION_GRAPH_VALIDATOR_PATTERN.md`

# Dimension Graph Validator Pattern

```python
constraints = [
    {
        "id": "C_WIDTH",
        "target": 2.0,
        "tolerance": 0.001,
        "measure": lambda scene: asset_bounds(scene)["width"],
    },
]
```

## Result

```text
constraint
target
actual
error
tolerance
PASS/FAIL
```

## Derived constraint

Niektóre constrainty nie mierzą tylko bounds:
- distance between landmarks,
- angle between vectors,
- panel offset,
- gap.

## Rule

Validator jest read-only.
Nie poprawia geometrii.


---

## FILE: `08_scripts/88_LANDMARK_PROJECTION_PATTERN.md`

# Landmark Projection Pattern

## Cel

Rzutować punkt świata na współrzędne kamery QA.

Blender udostępnia macierze obiektów i kamery; implementacja może używać odpowiednich utilities/API dla projekcji.

## Record

```python
LANDMARKS = {
    "LM_SEAT_FRONT_LEFT": {
        "object": "Bench_Seat",
        "local_point": (...),
        "reference": {
            "FRONT": (u, v),
            "SIDE": (u, v),
        },
    },
}
```

## Output

- projected UV/image coordinate,
- target,
- delta,
- tolerance.

## Rule

Po zmianie topology local vertex index nie jest stabilnym landmark ID.
Preferuj:
- named helper empty,
- parametric coordinate,
- semantic feature point.


---

## FILE: `08_scripts/89_RECONSTRUCTION_CHECKPOINT_MANIFEST.md`

# Reconstruction Checkpoint Manifest Pattern

## Manifest contains

```text
asset_id
stage
timestamp/version
hard_dimensions
object_bounds
feature_status
modifier_stacks
materials
qa_camera_revision
reference_revision
render_paths
```

## Use

Porównuj checkpointy:
- D0 accepted,
- D1 accepted,
- D2 accepted,
- surface accepted,
- runtime.

## Rule

Nie przechowuj tylko pliku `.blend`.
Bez manifestu agent nie wie, co było zaakceptowane.


---

## FILE: `08_scripts/90_REFERENCE_OVERLAY_DIFF_PATTERN.md`

# Reference Overlay Diff Pattern

## External/image-tool pattern

Input:
- reference crop,
- QA render,
- calibration metadata.

Output:
- alpha overlay,
- silhouette mask,
- diff heatmap,
- metrics JSON.

## Geometry-safe approach

Dla geometry QA używaj flat object mask.
To ogranicza wpływ:
- lighting,
- material,
- tone mapping.

## ROI

Dla feature-specific diff:
crop/weight według Visual Feature Map.

## Rule

Image diff nie modyfikuje sceny.
Jego wyniki są dowodem dla Inspector/Repairer.


---

## FILE: `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md`

# Reference Measurement Executor Pattern

## Purpose

This module defines a semantic executor contract for technical-sheet and concept-art measurement without flooding the language model with raw pixel arrays.

Skill ID:

```text
REFERENCE_MEASURE
```

Maturity:

```text
CONTRACT_READY
```

It becomes `EXECUTOR_READY` only after a concrete implementation has been tested in the current Blender/runtime integration.

## Design goal

The executor may perform thousands of pixel-level operations internally.

It must return only compact measurements, confidence, conflicts and requested diagnostics.

The language model must not inspect one record per image row/column unless a failing local ROI explicitly requires it.

## Inputs

```yaml
reference_measure:
  source_image: concept_art.png
  known_dimensions:
    height_mm: 1050
    main_body_diameter_mm: 140
    base_diameter_mm: 210
  requested_views:
    - FRONT
    - SIDE
    - TOP
    - REAR
    - BOTTOM
  expected_sheet_type: TECHNICAL_CONCEPT_SHEET
  output_detail: SUMMARY
```

Optional:
- pre-existing Reference Registry;
- explicit ROI list;
- expected view labels;
- known axis/datum;
- requested feature IDs.

## Executor stages

```text
LOAD IMAGE
-> DETECT / USE REGISTERED ROI
-> CLASSIFY VIEW
-> MASK ANNOTATION NOISE
-> CALIBRATE KNOWN DIMENSION
-> MEASURE SILHOUETTE / TRANSITIONS
-> CROSS-VIEW COMPARE
-> AGGREGATE
-> RETURN COMPACT RESULT
```

## Annotation exclusion

Technical sheets often contain dimension lines, arrows, labels and leaders near the asset silhouette.

The executor must not blindly threshold the whole crop and treat every dark pixel as geometry.

Use one or more of:
- registered object ROI narrower than annotation area;
- connected-component filtering;
- centerline/silhouette continuity;
- expected object-axis constraints;
- dimension-line morphology detection;
- explicit exclusion masks.

If annotation contamination remains ambiguous, return a localized warning rather than silently shifting the measured silhouette.

## Threshold strategy

Do not expose a long threshold-search trace to the language model.

Internally the implementation may test multiple thresholds, but it must select them using a deterministic score such as:
- silhouette continuity;
- expected axis symmetry;
- cross-row width stability;
- agreement with known dimensions;
- cross-view consistency.

If threshold confidence is low:

```yaml
status: NEEDS_LOCAL_REVIEW
roi: [x0, y0, x1, y1]
reason: ANNOTATION_OR_LOW_CONTRAST
```

## Compact output contract

Preferred output:

```yaml
reference_measurement:
  status: PASS
  source: concept_art.png
  views:
    FRONT:
      roi: [735, 165, 860, 640]
      projection: ORTHOGRAPHIC
      authority: HIGH
      silhouette:
        body_width_px: 70
        body_width_variance_px: 1.1
      transitions:
        top_module_y_px: [207, 220]
        base_y_px: [604, 634]
    SIDE:
      projection: ORTHOGRAPHIC
      authority: HIGH
      silhouette:
        body_width_px: 68
        body_width_variance_px: 0.8
  calibration:
    height_mm:
      value: 1050
      source: EXPLICIT_DIMENSION
      confidence: LOCKED
  cross_view:
    front_side_width_difference_pct: 2.9
    status: CONSISTENT
  anomalies: []
```

Do not return:
- per-pixel arrays;
- all rows of a width profile;
- full masks;
- all threshold candidates;
- full image buffers;
- hundreds of unchanged samples.

## Drill-down mode

Detailed data is allowed only after a specific failure or ambiguity.

Example:

```yaml
reference_measure:
  mode: ROI_DIAGNOSTIC
  view: FRONT
  roi: [750, 202, 835, 226]
  reason: TOP_RING_BOUNDARY_AMBIGUOUS
```

Even in diagnostic mode, return a summarized result plus only the minimal samples required to explain the failure.

## Cross-view validation

For dimensions visible in multiple orthographic views:

```text
measure independently
-> normalize using trusted anchors
-> compare
-> report deviation
```

Do not ask the language model to visually compare hundreds of rows when a numeric aggregate can answer the question.

## Cache integration

Every successful result updates `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md` state.

The executor must use existing validated ROI/calibration from the cache when available instead of rediscovering them.

## Failure codes

```text
REF_NO_VIEW
REF_LOW_CONTRAST
REF_ANNOTATION_CONTAMINATION
REF_NO_SCALE_ANCHOR
REF_PERSPECTIVE_UNSAFE
REF_CROSS_VIEW_CONFLICT
REF_ROI_INVALID
REF_MEASUREMENT_LOW_CONFIDENCE
```

## Repair policy

After failure:
1. localize the failing ROI;
2. change one justified measurement strategy;
3. rerun only that ROI;
4. do not rescan the full sheet unless segmentation itself is invalid.

## Success gate

`PASS` requires:
- source and ROI provenance;
- projection classification;
- explicit or normalized calibration strategy;
- compact measurement table;
- confidence per measurement;
- cross-view conflicts reported;
- no raw diagnostic dump in normal output.


---

## FILE: `08_scripts/92_MESH_CONTRACT_VALIDATOR_PATTERN.md`

# Mesh Contract Validator Pattern

## Skill ID

`MESH_VALIDATE`

## Purpose

Validate render meshes against an explicit per-object topology contract instead of reporting generic statements such as "no mesh defects" while boundary edges are still present.

## Topology intent is mandatory

Every mesh object entering GAME_READY validation declares one of:

```text
CLOSED_SOLID
OPEN_ASSEMBLY_PART
SURFACE_DETAIL
COLLISION
```

### `CLOSED_SOLID`

Requires:
- zero boundary edges;
- zero non-manifold edges;
- zero loose vertices/edges;
- zero zero-area faces;
- no duplicate vertices within configured tolerance.

### `OPEN_ASSEMBLY_PART`

Boundary edges are permitted only when:
- the exact boundary is intentional;
- it is covered/sealed by another owned assembly part;
- runtime backface assumptions permit it;
- the Feature/Game Asset Contract records the exception.

The validator must report the boundary count even when accepted.

### `SURFACE_DETAIL`

Floating/decal-like geometry may be open, but must additionally validate:
- visibility from intended views;
- no accidental z-fighting;
- no hidden placement behind the host surface;
- no unintended silhouette change unless owned by the feature.

### `COLLISION`

Use the active Engine Profile requirements. Prefer closed simple volumes unless the engine explicitly supports other collision forms.

## Compact report

```yaml
mesh_validation:
  object: BOL_MainBody
  topology_intent: CLOSED_SOLID
  status: FAIL
  verts: 128
  tris: 192
  boundary_edges: 64
  non_manifold_edges: 64
  loose_vertices: 0
  duplicate_vertices: 0
  zero_area_faces: 0
  uv_present: true
  reasons:
    - CLOSED_SOLID_HAS_BOUNDARY_EDGES
```

## Assembly-level validation

Also report:
- aggregate dimensions;
- origin/pivot;
- transforms;
- total triangles;
- material slots/submeshes;
- feature ownership;
- interpenetration/occlusion exceptions when relevant.

## Visibility validation for floating details

A floating feature is not valid merely because:
- the object exists;
- emission/material assignment is correct;
- its vertices are numerically near the host surface.

For a visible feature, require at least one visibility proof:
- QA render contains feature pixels in its ROI;
- ray/occlusion test shows the detail is not hidden by host geometry;
- geometric offset is proven outside the host surface along the correct normal.

This specifically prevents a local emitter or panel from being created inside a cylinder and silently disappearing.

## Candidate executor

`executors/mesh_validate.py`

Registry maturity stays `CONTRACT_READY` until benchmarked against the active Blender runtime and the project's topology policies.


---

## FILE: `08_scripts/93_BAKE_OUTPUT_VALIDATION_PATTERN.md`

# Bake Output Validation Pattern

## Purpose

Baked images require semantic validation. File existence and a successful operator return are necessary but not sufficient.

The validator should reduce image data locally and return compact statistics/failing regions rather than full pixel arrays.

---

# Generic image checks

For every output record:
- dimensions;
- color space;
- per-channel min/max/mean;
- nonzero fraction;
- clipped-low/clipped-high fraction when meaningful;
- unexpected constant-image detection;
- file path and modification state.

Example:

```yaml
image:
  channel: emissive
  size: [1024, 1024]
  min_rgb: [0.0, 0.0, 0.0]
  max_rgb: [0.259, 0.745, 1.0]
  nonzero_fraction: 0.052
  status: PASS
```

Do not send the complete pixel buffer to the LLM.

---

# BaseColor checks

Validate against material expectations.

Examples:
- expected metallic/brushed-aluminium atlas region must not become black merely because a DIFFUSE response was baked;
- dark graphite may legitimately be near black, so use region/material-aware thresholds rather than one global minimum;
- unexplained white/black full-atlas output is FAIL.

When a known UV region belongs to a material family, sample/aggregate that region separately.

---

# Normal checks

For tangent-space normals:
- verify image is not all zero/black;
- verify blue/Z component is generally positive where expected;
- detect impossible/degenerate constant values according to the material contract;
- verify color space is Non-Color;
- verify runtime tangent basis separately.

Do not require an arbitrary exact mean such as `[0.5, 0.5, 1.0]`; procedural detail may legitimately shift the distribution.

---

# AO checks

AO must not be globally black/near-zero because an unrelated render-visible object enclosed the asset.

Also do not require AO to have strong variation when the geometry is genuinely unoccluded.

Use configured expectations:

```yaml
ao_expectation:
  allow_constant_white: false
  max_near_black_fraction: 0.10
  required_occluded_regions:
    - BASE_RECESS
```

The specific thresholds belong to the asset/project validator.

---

# Roughness checks

Validate:
- values inside expected 0..1 range;
- not unexpectedly constant when authored breakup is required;
- material-family regions roughly match intended roughness bands;
- no color-space transform.

A maintained civic asset with authored roughness breakup should not collapse to one uniform scalar after bake.

---

# Metallic checks

Validate known material regions:
- metal regions contain high metallic values where expected;
- dielectric/composite/rubber regions remain near zero;
- the entire atlas must not become 1.0 because scalar channel extraction accidentally used the wrong default/socket behavior.

Region-aware validation is preferred over global mean.

---

# Emissive checks

Emissive must be validated spatially.

Given approved emitter UV rectangles/masks:

```text
expected emitter signal
unexpected signal outside emitters
padding bleed allowance
clipping/hue preservation
```

Required report:

```yaml
emissive:
  approved_signal_px: 52000
  outside_signal_px: 1800
  outside_allowed_padding: 0
  max_rgb: [0.259, 0.745, 1.0]
  clipped_channels: []
  status: PASS
```

A full/mostly white emissive atlas is FAIL when only small light strips are emitters.

Baking Principled `Emission Color` without considering zero `Emission Strength` can produce false white emission on non-emitting materials; this validator must detect that spatially.

---

# UV-region diagnostics

The validator may consume the same semantic UV contract as the bake source.

For each atlas owner:
- aggregate mean/min/max;
- check expected signal type;
- detect foreign contamination;
- detect missing part output.

Do not infer regions from `.001` object names. Use stable semantic part IDs.

---

# Runtime material check

After image validation, verify the runtime material actually references the accepted outputs.

For glTF metallic-roughness baseline:
- BaseColor -> correct base color texture;
- ORM/project packed texture -> correct roughness/metallic channel interpretation;
- Normal -> correct normal texture;
- Emissive -> correct emissive texture;
- decal material remains separate if required.

Engine Profile may override packing.

---

# Export readback

Parse the exported runtime file/manifest and verify:
- expected image URIs;
- expected material names;
- expected LOD nodes;
- dynamic/decal materials preserved separately;
- no accidental missing texture.

Do not trust Blender-side material state alone.

---

# Baked-runtime visual QA

Final visual comparison for texture closure must use:

```text
runtime LOD mesh
+
baked runtime material
```

not the original procedural authoring material.

If authoring render passes but baked-runtime render fails, the bake stage is FAIL.

---

# Progressive diagnostics

Default output: `SUMMARY`.

On failure:
1. identify map;
2. identify semantic region/channel;
3. return aggregate stats for only that region;
4. raw pixel data only as last resort.

This validator exists partly to prevent large image arrays from entering model context.


---

## FILE: `08_scripts/94_IMPORT_SAFE_PYTHON_MODULE_PATTERN.md`

# Import-Safe Blender Python Module Pattern

## Purpose

Reusable Blender build/bake/export code must be safe to load for functions without accidentally executing destructive top-level work.

The v0.5 bollard bake exposed two expensive failure classes:
- loading an export script for helper functions also executed the export;
- reusing a collection helper cleared objects that were still needed by the caller.

v0.6 treats module side effects and collection ownership as explicit contracts.

---

# 1. No production side effects on import

Reusable modules may define:
- constants;
- pure helpers;
- builders;
- validators;
- `run()` / `main()` entrypoints.

They must not automatically:
- rebuild the production asset;
- clear collections;
- export files;
- save the blend;
- delete objects;
- run a full bake;

merely because another script imports/executes them for a helper.

Preferred:

```python
def main():
    ...

if __name__ == "__main__":
    result = main()
```

When code is loaded through `exec`/`runpy`, choose the synthetic `__name__` intentionally.

---

# 2. Separate responsibilities

Prefer modules such as:

```text
build_asset.py     -> geometry/material authoring functions
bake_asset.py      -> texture closure
export_asset.py    -> LOD/package/export
qa_asset.py        -> QA cameras/render/validation
```

Shared helpers belong in reusable executors or a side-effect-free helper module.

Do not make `bake_asset.py` import `export_asset.py` if doing so automatically exports.

---

# 3. Collection ownership

A helper that clears a collection must own that collection exclusively.

Do not call:

```text
work_collection()
```

from a nested export helper if `work_collection()` clears the collection that currently contains the LODs being exported.

Use explicit ownership:

```text
ASSET_AUTHORING_COLLECTION
BAKE_SCRATCH_COLLECTION
EXPORT_SCRATCH_COLLECTION
QA_SCRATCH_COLLECTION
```

Scratch helpers may clear only their own scratch namespace.

---

# 4. Destructive helper naming

A function that clears/replaces state must say so in its contract/name/documentation.

Bad:

```python
work_collection()
```

when the function silently clears objects.

Better:

```python
reset_scratch_collection(name)
get_or_create_collection(name)
```

with distinct behavior.

---

# 5. Caller-owned objects

A callee must not delete, unlink or rename caller-owned production objects unless the call contract explicitly transfers ownership.

For temporary mirrored export copies:
- clone source data;
- operate in export scratch collection;
- export clones;
- remove clones;
- restore/leave source unchanged.

Do not mutate the source hierarchy merely to satisfy one export call when a copy can carry the transformation.

---

# 6. Idempotent entrypoints

`main()` / `run()` should:
- identify previous artifacts by stable names/tags;
- update/replace only owned artifacts;
- leave unrelated scene content unchanged;
- return a compact report.

Repeated invocation should not accumulate `.001` copies unless those copies are deliberately versioned artifacts.

---

# 7. Stable part identity

Imported/rebuilt objects may receive Blender suffixes. Never let `.001` change semantic behavior.

Use semantic part IDs/custom properties for:
- UV assignment;
- Feature Contract ownership;
- LOD mapping;
- material routing;
- validation.

Names remain useful for human readability/export conventions but are not sufficient as internal identity.

---

# 8. Validation

Before treating a helper module as reusable:
- load it without calling `main()`;
- assert no production files were written;
- assert production object count did not unexpectedly change;
- assert no source collection was cleared;
- call one helper in a scratch scene/collection;
- run twice and verify idempotent behavior where required.

---

# Compact module contract

```yaml
module:
  path: export_asset.py
  import_safe: true
  top_level_scene_mutation: false
  owned_collections:
    - EXPORT_SCRATCH
  entrypoint: main
  idempotent: true
  status: PASS
```


---

## FILE: `09_engine/90_ENGINE_PROFILE_SCHEMA.md`

# Engine Profile Schema

Biblioteka Blendera nie może zgadywać zasad własnego silnika gry.

Dlatego projekt powinien posiadać osobny `ENGINE_PROFILE.md`.

## Coordinate system

- handedness:
- up axis:
- forward axis:
- world unit:
- transform convention:

## Mesh

- supported vertex attributes:
- index size:
- tangent generation:
- max bones per vertex:
- morph targets:
- instancing:
- mesh compression:

## Materials

- shader model:
- metallic/roughness convention:
- packed channels:
- normal convention:
- transparency modes:
- emissive:
- texture formats:
- maximum material slots / recommendations:

## Textures

- supported formats:
- compression:
- mip generation:
- max resolution:
- streaming:
- color space convention:

## Animation

- skeletal:
- node transform:
- frame/time representation:
- interpolation:
- root motion:
- clip naming:

## Scene

- hierarchy:
- static batching:
- instancing:
- LOD representation:
- collision representation:
- occluders:
- navmesh hooks:

## Import format

- glTF/GLB/custom:
- supported extensions:
- unsupported features:
- preprocessing:

## Validation

Agent nie może uznać assetu za game-ready, jeśli ENGINE_PROFILE nie został zastosowany.
W razie braku profilu stosuje tylko neutralne zasady i oznacza runtime status jako `UNVERIFIED`.


---

## FILE: `09_engine/91_ENGINE_ADAPTER_PROTOCOL.md`

# Engine Adapter Protocol

## Cel

Oddzielić wiedzę o tworzeniu assetu od wiedzy o importerze konkretnego silnika.

## Adapter responsibilities

Adapter definiuje:
- mapowanie osi,
- mapowanie materiałów,
- nazwy collision,
- nazwy LOD,
- hierarchy rules,
- animation mapping,
- texture packing,
- export flags.

## Neutral asset

Główna biblioteka opisuje:
- poprawny model,
- dane authoringowe,
- standardowy manifest.

Adapter:
- przekształca to do wymagań silnika.

## Zakaz przecieku

Nie zapisuj przypadkowych ograniczeń jednego silnika jako uniwersalnej zasady Blendera.

Przykład:
jeżeli silnik wymaga konkretnego prefiksu collision, reguła trafia do adaptera, nie do globalnego `GAME_ASSET_CONTRACT`.

## Round-trip / smoke test

Adapter powinien definiować minimalny test:
- import success,
- bounds,
- scale,
- materials,
- normals,
- animation,
- collision.

## Custom engine

Dla własnego silnika C++ należy utworzyć osobny plik:
`ENGINE_PROFILE_<NAME>.md`
oraz test importera.


---

## FILE: `09_engine/92_PROJECT_ASSET_PIPELINE_PROFILE_SCHEMA.md`

# Project Asset Pipeline Profile Schema

## Purpose

An agent often needs project conventions such as naming, asset roots, decal atlases, material libraries, export destinations, runtime packaging rules, build targets and engine smoke-test commands.

It must not discover these by reading entire sibling asset build/export scripts or probing the build tree for every asset unless no validated profile exists.

This module defines a compact project-level profile separate from the runtime `ENGINE_PROFILE.md`.

The Engine Profile answers: **what the engine accepts**.

The Project Asset Pipeline Profile answers: **how this project authors, packages, stores, tests and integrates assets**.

For detailed runtime packaging semantics also use:
- `09_engine/94_RUNTIME_MODULE_PACKAGING_CONTRACT.md`;
- `09_engine/95_RUNTIME_ASSET_ROOT_AND_PATH_CONTRACT.md`;
- `09_engine/96_ENGINE_INTEGRATION_SMOKE_TEST_CONTRACT.md`.

## Suggested files

Generic schema instance:

```text
PROJECT_ASSET_PIPELINE_PROFILE.md
```

Repository-specific validated profiles may live under:

```text
09_engine/profiles/
```

Example:

```text
09_engine/profiles/RPG_PROJECT_ASSET_PIPELINE_PROFILE.md
```

A child profile may add brand/family conventions but must not silently override engine constraints.

## Schema

```yaml
project_asset_pipeline:
  profile_id: PROJECT_NAME_V1

  units:
    blender_unit: meter
    unit_scale: 1.0
    up_axis: Z

  naming:
    static_mesh: "SM_{brand}_{asset}_{variant}_LOD{n}"
    collision: "COL_{brand}_{asset}_{variant}"
    material: "M_{brand}_{name}"
    decal: "D_{brand}_{name}"

  runtime_paths:
    project_root: ...
    engine_asset_directory: ...
    game_asset_root: ...
    source_root: ...
    textures_root: ...
    decal_root: ...
    export_root: ...
    checkpoints_root: ...
    authority: PROFILE | CMAKE_DEFINE | ENGINE_CONFIG | LOADER_CODE | ...
    forbidden_lookalike_roots: []

  material_library:
    canonical_materials: []
    reusable_pbr_sets: []
    forbidden_brand_reuse: []

  decal_pipeline:
    atlas_path: ...
    atlas_layout_source: ...
    uv_convention: ...
    logo_policy: TEXTURE_OR_DECAL

  authoring:
    preferred_sides_for_cylinders: [24, 32]
    default_bevel_segments_game_ready: 2
    apply_scale_before_export: true

  export:
    format: GLTF_SEPARATE
    preset: ...
    destination: ...

  runtime_packaging:
    lod_packaging: ONE_FILE_MULTI_NODE | SEPARATE_FILE_PER_LOD | ...
    lod_node_pattern: "{mesh}_LOD{n}"
    collision_source: EXTERNAL_PREFAB | SEPARATE_FILE | EMBEDDED_NODE | ...
    collision_naming: ...
    handedness_compensation: NONE | MIRROR_X | MIRROR_Y | MIRROR_Z | ...
    handedness_verified_by: ...
    mirror_only_for_asset_classes: []
    runtime_material_policy: ...
    image_uri_policy: ...
    dynamic_material_policy: ...
    export_readback_required: true

  asset_catalog:
    required: true
    stable_id_rule: ...
    registration_source: ...
    conflict_policy: ...

  engine_loader:
    production_loader: ...
    runtime_asset_root_source: ...

  build_and_test:
    build_system: CMAKE | MSBUILD | NINJA | CUSTOM | ...
    debug_build_directory: ...
    runtime_test_target: ...
    runtime_test_source: ...
    runtime_test_binary: ...
    build_command: ...
    test_command: ...
    test_oracle_policy: DIRECT_PROCESS | PIPEFAIL_VERIFIED | TOOL_NATIVE
    bite_test_required_for_new_regression_assertion: true

  provenance:
    sources: []
    last_verified: ...
```

Only include conventions actually evidenced by project files, build configuration, runtime readback or explicit user instruction.

## Discovery order

When project conventions are needed:

```text
1. active validated Project Asset Pipeline Profile
2. explicit current task/user instruction
3. current asset manifest/config
4. engine/build definition
5. narrowly targeted project file lookup
6. sibling build/export/test script as last-resort evidence
```

Do not read a large unrelated build script merely to infer one naming, LOD grouping, handedness, path or test rule when a compact profile already provides it.

## Runtime path rule

A directory existing on disk is not evidence that the engine reads it.

If two plausible roots exist, such as:

```text
<repo>/GameAssets
<repo>/Assets/GameAssets
```

resolve against the engine/build/loader authority and persist the result.

Do not let bake, decal and export scripts each implement independent root-walking heuristics.

Use `09_engine/95_RUNTIME_ASSET_ROOT_AND_PATH_CONTRACT.md`.

## Sibling-script rule

If no profile exists and a sibling script must be inspected:
- search exact relevant identifiers first;
- read the smallest relevant range;
- extract only verified conventions;
- validate runtime-sensitive facts through actual exported/imported behavior where possible;
- update the Project Asset Pipeline Profile;
- do not copy sibling geometry dimensions or feature logic into the current asset.

A sibling asset is evidence for pipeline convention, not evidence for current geometry.

## Packaging facts worth persisting

When discovered once, persist facts such as:
- canonical engine-visible asset root;
- whether one asset uses one glTF containing all `_LODn` nodes or separate files;
- how LOD node names are parsed;
- whether collision lives in prefab primitives, a separate file or embedded nodes;
- whether the importer/engine changes handedness;
- whether export-side mirror compensation is required and on which axis;
- how readable logos/text are used to verify handedness;
- which runtime material names must survive export;
- expected BaseColor/Normal/ORM/Emissive image URI policy;
- whether decals/dynamic displays remain separate materials;
- whether catalog registration is required after export;
- which production loader proves Level D;
- the narrow build target/test binary used for asset regression tests;
- how the real test process exit code is captured.

These are project facts. Future assets should consume them without reopening long sibling exporters or re-running broad build-system discovery.

## Test infrastructure rule

Once a project test target is verified, persist it.

A future asset should not spend several shell calls rediscovering CMake presets, test binaries or source locations.

New regression assertions use `05_execution/66_TEST_ORACLE_EXIT_CODE_AND_BITE_TEST.md` and `09_engine/96_ENGINE_INTEGRATION_SMOKE_TEST_CONTRACT.md`.

## Handedness verification

Do not infer handedness correctness from a symmetric prop.

Prefer an asymmetric proof:
- readable logo/text;
- left/right service panel;
- directional port;
- asymmetric decal.

Record the evidence in `handedness_verified_by`.

## Conflict precedence

```text
Engine Profile constraints
> explicit current task requirements
> approved Project Asset Pipeline Profile
> current asset configuration
> sibling asset convention
```

If the current task explicitly names an object/material/export rule, do not silently replace it with an older project convention.

## Profile freshness

Project facts can become stale.

Mark affected fields `UNVERIFIED` and re-resolve after changes to:
- build-system asset-root definitions;
- engine loader configuration;
- importer handedness/LOD grouping;
- catalog implementation;
- test/build directory layout;
- runtime material conventions.

Do not invalidate unrelated stable profile fields.

## Brand/family scope

A child brand profile may define:
- manufacturer prefix;
- shared material names;
- decal atlas;
- typography/logo handling;
- common construction language.

It must not define dimensions for new products unless those dimensions are a real family standard documented as such.

## Runtime status

Missing Project Asset Pipeline Profile does not make geometry invalid, but project integration status is:

```text
PROJECT_PIPELINE_UNVERIFIED
```

until conventions required by the task are confirmed.

If runtime root or packaging facts required for game-ready export are unknown:

```text
RUNTIME_PACKAGING_UNVERIFIED
```

Do not guess path, one-file/separate-LOD, collision or mirror policy.

## Efficiency requirement

Once conventions are extracted into a validated profile, cache and reuse them across assets in the same project scope. Do not repeatedly re-read original discovery scripts or re-probe the build tree.

---

## FILE: `09_engine/93_ASSET_CATALOG_INTEGRATION_PROTOCOL.md`

# Asset Catalog Integration Protocol

## Purpose

Exporting a mesh file is not the same as integrating an asset into a production project.

This protocol defines the final `PIPELINE_INTEGRATED` step for projects that maintain an asset catalog, importer registry, content database, manifest or equivalent system.

The exact catalog format is project-specific and must come from the active Project Asset Pipeline Profile.

---

# Preconditions

Before catalog integration:
- `GAME_READY_COMPLETE` passes;
- runtime files exist;
- stable asset ID exists;
- destination namespace/path is known;
- active Project Asset Pipeline Profile describes the catalog/import mechanism;
- agent has write capability for the catalog, or reports a blocker.

Do not invent a catalog schema.

---

# Discovery

Before writing:
1. search for an existing asset with the same semantic role/name/ID;
2. identify whether this is a replacement, version, variant or new asset;
3. inspect the smallest relevant catalog entry/example;
4. determine required files/fields;
5. persist the resolved integration contract.

Do not overwrite an existing production asset because a generated object happens to have a similar name.

---

# Minimal integration record

Project-specific fields may differ, but the semantic record should cover:

```yaml
asset_catalog_entry:
  asset_id: ACS-BOL-140
  source_blend: path/to/source.blend
  runtime_meshes:
    LOD0: path/to/mesh0
    LOD1: path/to/mesh1
    LOD2: path/to/mesh2
    LOD3: path/to/mesh3
  collision: path/to/collision
  textures:
    basecolor: path/to/basecolor
    normal: path/to/normal
    orm: path/to/orm
    emissive: path/to/emissive
  material_profile: ACS_CIVIC_DARK_EMISSIVE
  pivot_policy: BASE_CENTER
  bounds_mm: [210, 210, 1050]
  status: ACTIVE
```

Only fields actually supported by the project should be written.

---

# Existing asset conflict

If an existing catalog item is found:

Classify:
- `SAME_ASSET_UPDATE`;
- `NEW_VARIANT`;
- `LEGACY_ASSET_REPLACEMENT`;
- `NAME_COLLISION_UNRELATED`.

A replacement requires explicit project policy or user instruction.

If the current project already has a generic road bollard and the new reconstruction is a branded Astera bollard, do not silently overwrite the generic asset. Register as a distinct asset or follow the replacement policy.

---

# Validation after registration

After writing the catalog/import record:
- read it back;
- verify all referenced paths exist;
- verify expected LOD/collision associations;
- verify material/texture references;
- verify asset ID uniqueness;
- run importer/instantiation smoke test if the current toolchain supports it.

A successful file write without readback is not sufficient.

---

# Missing capability

If the agent can create/export files but cannot modify the project's catalog:

```yaml
pipeline_integration:
  status: BLOCKED
  reason: CATALOG_WRITE_CAPABILITY_MISSING
  prepared_files: true
  proposed_asset_id: ACS-BOL-140
```

This can still satisfy `GAME_READY_COMPLETE`, but not `PIPELINE_INTEGRATED` when Level D is required.

---

# Idempotency

Re-running integration must not create:
- duplicate asset IDs;
- duplicate manifest entries;
- `.001`-style catalog variants;
- multiple references to the same LOD file.

Prefer update-by-stable-ID.

---

# Rollback

Before changing an existing catalog entry:
- capture the old record;
- record affected asset ID;
- write transactionally where possible;
- restore the previous record if verification fails.

---

# Boundary with engine adapter

This protocol describes **project registration**.
`09_engine/91_ENGINE_ADAPTER_PROTOCOL.md` describes runtime format/import behavior.

Both may be required for Level D.


---

## FILE: `09_engine/94_RUNTIME_MODULE_PACKAGING_CONTRACT.md`

# Runtime Module Packaging Contract

## Purpose

Export packaging is engine/project-specific and must be discovered once, persisted and reused.

The agent must not repeatedly inspect sibling exporters to rediscover basic facts such as:
- whether LODs live in one file or separate files;
- collision representation;
- handedness compensation;
- module naming;
- material/texture binding conventions.

Persist these facts in the active Project Asset Pipeline Profile / Engine Profile.

---

# Required packaging fields

```yaml
runtime_packaging:
  module_id:
  export_format: GLTF_SEPARATE
  lod_packaging: ONE_FILE_MULTI_NODE
  lod_node_pattern: "{mesh_name}_LODn"
  collision:
    source: EXTERNAL_PREFAB_BOXES | SEPARATE_FILE | EMBEDDED_NODE
    naming_pattern:
  handedness:
    blender:
    engine:
    compensation:
  mirror_compensation:
    required: false
    axis: X
    verified_by:
  materials:
    runtime_material_names: []
    decal_material_separate: true
  textures:
    uri_policy:
    packing_profile:
  catalog:
    asset_id:
    registration_required: true
```

---

# 1. LOD packaging

Do not assume one export file per LOD.

Supported project strategies include:

```text
ONE_FILE_MULTI_NODE
ONE_FILE_ENGINE_METADATA
SEPARATE_FILE_PER_LOD
ENGINE_GENERATED_LOD
```

Discover from the Engine/Profile once.

If the engine recognizes LODs by node suffix such as `_LOD0`, `_LOD1`, ... then the export validator must confirm all expected node names exist in the final module file.

Do not keep producing separate files merely because they were convenient during Blender QA.

---

# 2. Collision packaging

Collision may be:
- a separate glTF/module;
- external project/prefab primitives;
- embedded collision nodes;
- generated by engine/importer.

Do not spend time embedding detailed render-mesh collision if the engine contract uses simple box/convex primitives elsewhere.

Record the actual project strategy.

---

# 3. Handedness and mirror compensation

Coordinate-system conversion must be proven with an asymmetric test.

Symmetric props can hide mirror mistakes.

Good verification features:
- readable logo/text;
- asymmetric service panel;
- left/right port;
- directional decal.

If the current engine/importer mirrors imported glTF, export-side compensation may be required.

Do not apply a mirror globally because another asset happened to use one. Persist the verified rule in the Engine/Profile.

When mirroring export copies:
- do not mutate the authoring source;
- transform a copy;
- correct normals/winding as required;
- preserve UV/material semantics;
- validate branding is readable after runtime import.

---

# 4. Export scratch ownership

Packaging must be non-destructive.

Use an export-owned scratch collection for temporary copies.

Do not call a helper that clears the same collection containing source LOD objects.

Use `08_scripts/94_IMPORT_SAFE_PYTHON_MODULE_PATTERN.md`.

---

# 5. Runtime material binding

Before export:
- procedural authoring materials must have an explicit runtime disposition;
- accepted baked textures must be bound to runtime material(s);
- project decal material remains separate when its atlas is separate;
- dynamic display material remains separately addressable when required.

After export, read back material names and image URIs.

---

# 6. Export readback

For JSON-based glTF baseline, parse the file instead of trusting console output.

Verify:
- expected node names;
- expected LOD count;
- expected material names;
- expected texture/image URIs;
- dynamic/decal material separation;
- absence of unexpected missing assets.

Compact report:

```yaml
package_validation:
  module: astera_bollard
  file: astera_bollard.gltf
  lod_nodes:
    - ..._LOD0
    - ..._LOD1
    - ..._LOD2
    - ..._LOD3
  materials:
    - M_Runtime
    - M_Decal
  images:
    - basecolor.png
    - normal.png
    - orm.png
    - emissive.png
    - decals.png
  status: PASS
```

---

# 7. Project-profile persistence

Once a packaging rule is verified, write it into the project profile so future assets do not inspect long sibling scripts again.

Example discoveries worth persisting:
- one glTF per asset with multiple LOD nodes;
- node suffix drives LOD grouping;
- collision is external/prefab-based;
- engine handedness requires X-mirror export compensation for readable branding.

These are project facts, not asset-specific reasoning.

---

# 8. Completion gate

`GAME_READY_COMPLETE` requires the runtime module package to pass its packaging contract when export is part of the requested target.

`PIPELINE_INTEGRATED` additionally requires catalog/importer integration according to the project profile.


---

## FILE: `09_engine/95_RUNTIME_ASSET_ROOT_AND_PATH_CONTRACT.md`

# Runtime Asset Root and Path Contract

## Purpose

An export can succeed to a real directory and still be unusable because the target engine reads from a different asset root.

Filesystem existence is not runtime reachability.

## Core rule

```text
EXISTING OUTPUT PATH != ENGINE-VISIBLE OUTPUT PATH
```

The canonical runtime asset root must be resolved **before** bake/export/catalog work that writes external artifacts.

## Resolution authority

Use this precedence:

```text
1. explicit active Project Asset Pipeline Profile
2. engine/build definition of asset root
3. production loader configuration
4. existing engine regression test fixture/path
5. narrowly inspected sibling exporter
6. heuristic directory search only as diagnostic evidence
```

If two plausible trees exist, such as:

```text
<repo>/GameAssets
<repo>/Assets/GameAssets
```

never choose by directory name alone.

Resolve against the engine's configured root.

## Path record

Persist:

```yaml
runtime_paths:
  project_root: ...
  engine_asset_directory: ...
  game_asset_root: ...
  texture_root: ...
  export_root: ...
  authority: CMAKE_DEFINE | ENGINE_CONFIG | PROFILE | ...
  verified_by:
    - engine_loader_test
  status: PASS
```

## Preflight

Before the first external artifact write:
- canonicalize paths;
- confirm the path lies under the intended runtime root;
- verify the target asset class directory convention;
- verify relative URIs will resolve from the exported module;
- reject ambiguous sibling roots.

Do not scatter separate `repo_root()` heuristics across bake, decal and export scripts.

All stages should consume one resolved `RuntimePathContext`/profile.

## Single-source path injection

Preferred architecture:

```text
SESSION/PACK PREFLIGHT
-> resolve runtime path context once
-> pass context to decal/bake/export/catalog/test stages
```

Not:

```text
bake.py guesses root
export.py guesses root differently
decal.py guesses root again
engine test discovers third root
```

## Wrong-tree failure

If artifacts were written to a non-runtime sibling tree:
1. mark package destination FAIL;
2. do not rebake clean textures merely to move them;
3. copy/re-export only affected artifacts through the DAG;
4. verify the engine-visible path;
5. remove only agent-owned stale artifacts from the wrong tree;
6. never delete unrelated project assets by broad glob unless ownership is proven.

## Runtime proof

A path contract passes when the target engine loader or its regression test resolves the exported module from the same root.

A Blender importer opening an absolute path does not prove runtime-root correctness.

## Candidate executor

Use `executors/runtime_path_resolver.py` to validate/profile-resolve canonical project/runtime paths when applicable.

The executor intentionally rejects ambiguous roots instead of picking the first directory that exists.

---

## FILE: `09_engine/96_ENGINE_INTEGRATION_SMOKE_TEST_CONTRACT.md`

# Engine Integration Smoke-Test Contract

## Purpose

`PIPELINE_INTEGRATED` requires evidence from the **target runtime path and loader**, not merely from Blender or a file parser.

The engine test must also prove the space in which its invariants are evaluated. A dimension assertion over local vertex positions is not world-space proof when the runtime node can carry an unapplied transform.

## Proof hierarchy

```text
package JSON/readback
< Blender round-trip import
< engine production loader test
< engine instantiation/render smoke test
```

Use the strongest level required by the active completion target.

## Level D minimum

For `PIPELINE_INTEGRATED`, the minimum accepted runtime evidence is normally one of:
- target engine production loader successfully loads the registered asset;
- existing engine regression test invokes the same loader on the exported asset;
- actual engine scene instantiation succeeds.

A Blender `bpy.ops.import_scene.gltf` PASS is Level C round-trip evidence only.

## Reuse existing project test infrastructure

Before creating a new test harness:
1. read the active Project Asset Pipeline Profile;
2. locate the configured narrow model/import test target;
3. inspect the nearest existing asset test pattern;
4. extend it with only the asset invariants that previously failed or are contract-critical.

Do not rediscover the build system with broad shell exploration when profile facts are already known.

## Recommended engine-side assertions

Asset-specific tests may pin:
- asset can be resolved from runtime asset root;
- loader returns expected LOD group/nodes;
- LOD triangle counts or budget bounds;
- hard dimensions/tolerance on runtime vertex data;
- ground datum;
- required UV channel presence;
- required PBR image bindings;
- vertex colors/custom attributes when relied upon;
- alpha/cutout semantics;
- material count/names where contract-critical.

Do not pin irrelevant implementation details that make tests brittle without protecting a real contract.

## Coordinate-space declaration

Every dimension/contact assertion must declare one of:

```text
LOCAL_VERTEX_SPACE
NODE_TRANSFORMED_SPACE
ENGINE_WORLD_SPACE
```

A test that reads raw accessor/vertex positions is normally `LOCAL_VERTEX_SPACE`.

It must not be described as proof of final runtime size when non-identity node transforms are permitted and the production loader may ignore them.

## Node transform policy

The active Project Asset Pipeline Profile must declare the runtime policy for node transforms.

Possible policies:

```text
IDENTITY_TRS_REQUIRED
TRANSFORMS_APPLIED_BY_LOADER
TRANSFORMS_BAKED_BY_EXPORTER
UNVERIFIED
```

If the production loader does **not** apply glTF node transforms:
- runtime mesh nodes must use identity/baked TRS according to project policy;
- package readback must fail on non-identity runtime node transforms;
- local-vertex dimension assertions are accepted only together with the identity-transform proof.

This protects against a false green where local vertices still measure 2600 mm but the glTF node contains an unconsumed scale.

## Runtime attribute proof

Successful loading is not enough to prove the renderable primitive contract.

For textured materials, package/engine evidence should pin required attributes such as:

```text
POSITION
NORMAL
TEXCOORD_0
```

when required by the runtime material.

The Lafar Wayfinding Pylon benchmark produced a valid/loadable glTF with images and materials but no `TEXCOORD_0` after UV-layer-name mismatch during mesh joining. This must be a hard package/runtime FAIL, not a later visual surprise.

## Loader exceptions and automation

A loader exception used in an automated test must become a readable test failure where practical.

Avoid modal dialogs/abort-only behavior that blocks the agent and hides the failure cause.

Classify:

```text
ASSET_NOT_FOUND
PARSE_FAIL
MATERIAL_MISSING
ATTRIBUTE_MISSING
LOD_CONTRACT_FAIL
DIMENSION_FAIL
NODE_TRANSFORM_FAIL
TEST_ASSERTION_FAIL
PROCESS_CRASH
```

## Bite-test requirement

A newly added regression assertion should prove it can fail through `05_execution/66_TEST_ORACLE_EXIT_CODE_AND_BITE_TEST.md` when safe.

The bite test must fail for the intended assertion with a readable message, then be fully restored and green.

A crash/abort is not a valid bite.

A valid bite test proves only the assertion class it mutates. Example:
- changing build geometry height and seeing `DIMENSION_FAIL` proves geometry-drift detection;
- it does **not** prove node-scale detection unless the controlled mutation is specifically a node transform and the intended transform assertion bites.

## Catalog integration

If the project uses an asset catalog:

```text
export to canonical runtime root
-> package readback
-> transform/attribute contract
-> catalog registration/readback
-> engine loader test using runtime path/catalog convention
-> completion gate
```

Registering a catalog entry without proving the target file is visible to the engine is insufficient.

## Completion evidence

Persist:

```yaml
engine_smoke_test:
  loader: Engine::Model::Load
  asset_id: ...
  runtime_path: ...
  build_target: ...
  build_status: PASS
  test_exit_code: 0
  process_status: PASS
  coordinate_space: LOCAL_VERTEX_SPACE
  node_transform_policy: IDENTITY_TRS_REQUIRED
  package_transform_check: PASS
  assertions:
    lod_family: PASS
    dimensions: PASS
    required_attributes: PASS
    materials: PASS
  bite_test: PASS | NOT_REQUIRED | NOT_SAFE
  status: PASS
```

Only this kind of target-runtime evidence may satisfy `runtime_import_or_instantiation` for Level D.


---

## FILE: `09_engine/profiles/RPG_PROJECT_ASSET_PIPELINE_PROFILE.md`

# RPG Project Asset Pipeline Profile

## Scope

Verified project profile extracted from real Lafar/Astera civic-asset pipeline benchmarks.

Use only when operating inside the RPG repository whose engine/build layout matches these facts. If the repository/runtime changes, mark the affected facts `UNVERIFIED` and re-resolve them rather than silently reusing stale paths.

```yaml
project_asset_pipeline:
  profile_id: RPG_CUSTOM_ENGINE_2026_08_V1

  units:
    blender_unit: meter
    unit_scale: 1.0
    up_axis: Z

  runtime_paths:
    project_root: <repo>
    engine_asset_directory: <repo>/Assets
    game_asset_root: <repo>/Assets/GameAssets
    authority: RPG_ENGINE_ASSET_DIRECTORY
    forbidden_lookalike_root:
      - <repo>/GameAssets

  city_asset_layout:
    first_planet_road_modules: <repo>/Assets/GameAssets/City/first_planet/road_kit/modules

  runtime_packaging:
    export_format: GLTF_SEPARATE
    lod_packaging: ONE_FILE_MULTI_NODE
    lod_node_pattern: "{mesh}_LOD{n}"
    handedness_compensation: MIRROR_X
    export_readback_required: true
    texture_uri_policy: RELATIVE_TO_GLTF_MODULE

    # Verified by the Wayfinding Pylon run: current production loader/test reads
    # local vertex positions and does not provide proof that arbitrary glTF node
    # transforms are applied. Runtime mesh transforms must therefore be baked or
    # identity until importer behavior changes and is revalidated.
    node_transform_policy: IDENTITY_TRS_REQUIRED
    engine_loader_transform_application: NOT_APPLIED_FOR_CURRENT_DIMENSION_TEST_PATH

    required_textured_primitive_attributes:
      - POSITION
      - NORMAL
      - TEXCOORD_0

  asset_catalog:
    required: true
    registration_source: Source/Engine/AssetCatalog.cpp
    conflict_policy: NEW_PRODUCT_GETS_NEW_STABLE_ID

  engine_loader:
    production_loader: Engine::Model::Load

  build_and_test:
    build_system: CMAKE
    debug_build_directory: Build/windows-debug
    model_test_target: ModelTests
    model_test_source: Tests/ModelTests.cpp
    model_test_binary: Build/windows-debug/Debug/ModelTests.exe
    build_command: cmake --build Build/windows-debug --target ModelTests --config Debug
    test_oracle_policy: DIRECT_EXECUTABLE_EXIT_CODE
    bite_test_required_for_new_regression_assertion: true
    dimension_assertion_space: LOCAL_VERTEX_SPACE

  evidence:
    - Lafar Civic Bollard final runtime integration benchmark
    - Lafar Wayfinding Pylon final runtime/reconstruction benchmark
    - engine loader resolved assets from RPG_ENGINE_ASSET_DIRECTORY/Assets
    - ModelTests successfully loaded Astera civic assets after export to Assets/GameAssets
    - wrong sibling root <repo>/GameAssets produced runtime load failure
    - Wayfinding Pylon exported once without TEXCOORD_0 despite valid images/materials; fixed before final acceptance
    - Wayfinding Pylon dimension bite test proved build-geometry drift detection but exposed that local-vertex assertions do not prove node-transform handling
```

## Required use

When this profile matches the active project:
- do not rediscover the runtime root with `ls/find` before every asset;
- do not write to `<repo>/GameAssets`;
- inject the resolved runtime root into bake/decal/export stages;
- package the LOD family into one glTF module using `_LOD0.._LODn` node naming;
- use the existing `ModelTests` infrastructure for engine-loader regression where appropriate;
- capture `ModelTests.exe` exit status directly;
- do not claim Level D from Blender glTF import alone;
- require identity/baked runtime mesh-node TRS while the current loader path does not prove transform application;
- require `TEXCOORD_0` on textured runtime primitives.

## Handedness caution

`MIRROR_X` is a project/runtime packaging fact observed in the current pipeline. Reverify if the engine importer or coordinate conversion changes. Prefer readable asymmetric details as proof.

Do not reduce text/decal orientation to one global `mirror_u` switch. Front-facing and rear-facing surfaces can require opposite authoring-space UV orientation under the same project handedness conversion. Validate readable branding per canonical face/view after export.

## Node-transform caution

Current dimension regression evidence is `LOCAL_VERTEX_SPACE`.

Therefore:

```text
local vertex dimensions PASS
+
non-identity runtime node TRS
=
NOT sufficient runtime size proof
```

For current profile:

```text
package node TRS identity PASS
+
local vertex dimensions PASS
=
accepted dimension evidence for the current loader path
```

If the production importer begins applying node transforms, update the profile and engine regression pattern together.

## Runtime attribute caution

A glTF package can parse and load while required vertex attributes are absent. For textured PBR/display owners, package readback must validate at least the attributes declared in `required_textured_primitive_attributes`.

## Profile freshness

This is a project-specific optimization layer, not a universal Blender rule.

Invalidate/reverify affected fields after changes to:
- CMake asset-directory definitions;
- engine loader root configuration;
- glTF importer handedness;
- glTF node-transform application;
- runtime material/vertex attribute requirements;
- LOD grouping parser;
- catalog layout;
- test/build directory layout.


---

## FILE: `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md`

# Reconstruction Layer Index and Controller v0.9

Warstwa `10_reconstruction` służy do ścisłego odtwarzania obiektu 3D z concept sheet, blueprintów, rzutów, zdjęć, renderów, wymiarów i opisów.

Nie jest to warstwa inspiracji. Celem jest evidence-constrained reconstruction z kontrolowaną niepewnością.

## Fundamental rule

```text
UNDERSTAND FORM
-> BUILD COARSE
-> PROVE
-> ADD DETAIL
```

Nie:

```text
reference -> one large Blender script -> inspect finished scene
```

Model z poprawnym detalem, ale błędną primary form jest nieudaną rekonstrukcją.

---

## v0.9 controller pipeline

```text
INGEST
-> CLASSIFY EVIDENCE
-> AUTHORITY
-> REGISTER
-> CONSTRAIN
-> DECOMPOSE
-> SHAPE GRAPH
-> RDL0 ENVELOPE
-> RDL1 PRIMARY FORMS node-by-node
-> RDL2 SECONDARY STRUCTURAL FORMS node-by-node
-> RDL3 STRUCTURAL FEATURES node-by-node
-> RDL4 EDGE LANGUAGE
-> RDL5 SURFACE/DETAIL
-> MULTIVIEW + RECON_FIDELITY_GATE
-> TOPOLOGY/RUNTIME
-> EXPORT/ENGINE
```

Detailed state: `149_RECONSTRUCTION_STATE_MACHINE.md`.

---

# Knowledge groups

## Evidence / authority
100–109.

Important:
- Evidence Model;
- ingestion/segmentation/classification;
- View Authority Matrix;
- conflict resolution;
- uncertainty/provenance.

## Geometric constraints
110–123.

Important:
- Dimension Graph;
- landmark/keypoint system;
- coordinate registration/calibration;
- silhouette constraints;
- negative space;
- cross-section/profile/curvature inference;
- thickness/gaps/panel lines.

## Surface evidence
124–127.

## Form decomposition and construction
128–140 plus v0.9:
- `128_RECONSTRUCTION_OBJECT_DECOMPOSITION.md`;
- `129_FEATURE_TO_MODELING_STRATEGY_MAP.md`;
- `174_RECONSTRUCTION_SHAPE_GRAPH.md`;
- `175_RECONSTRUCTION_DETAIL_LEVELS.md`;
- `176_RECONSTRUCTION_NODE_CONTRACT.md`;
- `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md`;
- `178_NODE_BY_NODE_MULTI_VIEW_VALIDATION.md`;
- `179_MULTI_SECTION_LOFT_AND_PROFILE_CAGE.md`.

## Validation
141–148 + v0.8 fidelity/evidence modules.

## Governance
149–159.

## Specialized modes
160–173.

---

# 1. Reference analysis

Before geometry identify:
- projection/view class;
- known dimensions/datums;
- principal axes;
- global silhouette;
- major landmarks;
- negative spaces;
- primary planes/profiles/curves;
- repeated structures;
- material boundaries;
- hidden/uncertain geometry;
- conflicts between prompt/card/views.

Do not convert uncertain pixels into fake metric precision.

---

# 2. Registration before deformation

When a screen-space mismatch exists diagnose:

```text
projection class
-> calibration
-> camera/ortho scale
-> shift/rotation
-> object orientation
-> only then geometry
```

QA cameras are evidence instruments. Once registered, do not move them to hide geometry error.

---

# 3. Shape Graph before production geometry

After constraints, decompose asset into:

```text
G0 GLOBAL_ENVELOPE
G1 PRIMARY_FORM
G2 SECONDARY_STRUCTURAL_FORM
G3 STRUCTURAL_FEATURE
G4 EDGE_LANGUAGE
G5 SURFACE_DETAIL
```

Build `Reconstruction Shape Graph`.

Each required node records:
- role;
- parent/dependencies;
- G-level + RDL;
- shape class;
- feature ownership;
- authoritative views;
- controlled properties per view;
- numeric/relationship constraints;
- validation contract;
- implementation skill.

Graph structural PASS is required before production modeling.

---

# 4. Representation-first construction

Do not select Blender operators before the shape class.

Canonical classes:
- primitive;
- extruded profile;
- revolved profile;
- profile sweep;
- multi-section loft/transition;
- SubD freeform;
- recess/panel-line/layered assembly;
- hybrid assembly.

Example:

```text
width changes with Z
+ depth changes with Z
+ corner treatment changes with Z
=> do not default to cube + bevel
=> classify as MULTI_SECTION_LOFT / SUBD_FREEFORM candidate
```

Use `177` and `129`.

---

# 5. RDL coarse-to-fine

Reconstruction Detail Levels:

```text
RDL0 envelope
RDL1 primary forms
RDL2 secondary structural forms
RDL3 structural features
RDL4 edge language
RDL5 surface/detail
```

`RDL != runtime LOD`.

Runtime LOD starts only after reconstruction fidelity PASS.

---

# 6. Node-by-node build loop

For each ready Shape Node:

```text
validate dependencies
-> select representation skill
-> build current node only
-> mark BUILT_UNVERIFIED
-> QA scene isolation
-> render required canonical views
-> registered local/global comparison
-> numeric/section checks
-> regression outside expected-change region
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | FAIL
```

Accepted node unlocks dependent children.

A required child is blocked when its required parent/dependency is not accepted.

---

# 7. Stage barriers

After each RDL:

```text
all required nodes accepted
+ protected earlier invariants pass
=> RDL barrier PASS
```

No RDL2 before RDL1 barrier.
No structural features before accepted hosts.
No edge language before structural form.
No surface finish before geometry acceptance.

---

# 8. Multi-view responsibilities

Multiple views constrain one 3D object.

Typical:

```text
FRONT -> width/height/front contour
SIDE -> depth/height/profile
TOP -> width/depth/corner plan
REAR -> rear form/features
BOTTOM -> underside/contact/service geometry
HERO -> supporting spatial/edge/material interpretation
```

Every node states exactly what each required view controls.

Do not accept `looks okay`.

---

# 9. Cross-section and loft logic

For forms varying along an axis define semantic section stations.

Validate:
- station positions;
- width/depth;
- corner/chamfer/profile family;
- common point correspondence;
- no unintended twist;
- continuity intent;
- FRONT/SIDE/TOP projection.

Preferred skill for supported forms:
`SECTION_LOFT_HARD_SURFACE`.

---

# 10. Detail skills are leaf skills

Only after host acceptance:
- narrow seam -> `HS_PANEL_LINE`;
- SubD cage/flow -> `SUBD_TOPOLOGY_CONTROL`;
- radial patterns -> `RADIAL_REPEAT`;
- recess -> boolean/direct recess strategy;
- layered display -> `LAYER_STACK_VALIDATE`;
- branding/decals/materials -> RDL5.

A leaf skill never substitutes for primary-form understanding.

---

# 11. Validation hierarchy

```text
node numeric/silhouette
-> node neutral/matcap
-> RDL stage barrier
-> whole-asset registered multiview
-> material/surface evidence
-> final RECON_FIDELITY_GATE
```

Required proof is typed and has provenance. Bare `PASS` is `UNVERIFIED` where strict evidence is required.

QA isolation is mandatory; collision/export/LOD proxies cannot stand in for the asset.

---

# 12. Repair priority

When validation fails:

```text
registration
-> scale/constraints
-> shape representation
-> primary form parameters
-> secondary form
-> structural feature
-> edge treatment
-> surface
```

After one corrected retry, second proven failure of the same strategy requires re-inspection and possible representation switch.

Do not perform endless visual tweaking.

---

# 13. Final reconstruction gate

Before runtime:
- Shape Graph current and valid;
- required G0–G3 nodes accepted;
- required RDL barriers PASS;
- hard dimensions PASS;
- canonical registered views PASS;
- primary landmarks/proportions PASS;
- MUST feature evidence PASS;
- material segmentation PASS when target fidelity requires it;
- authority conflicts/deviations closed;
- final `RECON_FIDELITY_GATE: PASS`.

Only then route to topology/UV/runtime LOD/bake/export.

---

# 14. Single-image mode

When only one image exists:
- solve visible silhouette/landmarks;
- infer depth conservatively;
- separate observed/derived/inferred;
- keep hidden geometry minimal;
- Shape Graph may contain LOW/UNKNOWN-confidence nodes;
- do not claim fully determined literal 1:1 in unobserved regions.

---

# 15. Persistent outputs

```text
Reference Registry
Evidence Ledger
View Authority Matrix
Dimension Graph
Feature Contract
Shape Graph + revision
Node Contracts
Node Acceptance Records
RDL Stage Barrier Records
Reconstruction Fidelity Report
```

Conversation history is not the execution database.

---

# Final rule

Agent must answer these questions before detail:

```text
What is the global form?
What are the primary forms?
What depends on what?
Which views define each form?
What mathematical representation fits each form?
How will each form be proven before children are added?
```

Dopiero potem wykonuje Blender operations.


---

## FILE: `10_reconstruction/101_DEFINITION_OF_1_TO_1.md`

# Definition of 1:1 Reconstruction

## 1:1 nie oznacza fotograficznej identyczności pojedynczego renderu

Model 3D jest uznawany za rekonstrukcję 1:1, jeśli maksymalizuje zgodność z całym zestawem dowodów jednocześnie.

## Pięć warstw zgodności

### R1 — Metric fidelity
Znane wymiary, kąty, offsety i pozycje mieszczą się w tolerancji.

### R2 — Multi-view shape fidelity
Front, side, top, rear i inne widoki zgadzają się równocześnie.

### R3 — Feature fidelity
Każda cecha `MUST` istnieje, znajduje się w poprawnej strefie i ma właściwe proporcje.

### R4 — Surface fidelity
Materiały, edge treatment, roughness, metaliczność, emisja i tekstury odpowiadają dowodom.

### R5 — Construction fidelity
Podział elementów, warstwy materiałowe, szczeliny i grubości są zgodne z logiką obiektu i referencją.

## Nieprawidłowa definicja

"Render 3/4 wygląda prawie tak samo."

To może ukryć:
- błędną głębokość,
- złe pochylenie,
- złą szerokość boków,
- brak detalu z tyłu,
- błędny spód,
- niepoprawne wymiary.

## Hard gate

Jeśli znany wymiar jest przekroczony ponad tolerancję, asset nie jest 1:1 nawet jeśli wygląda dobrze.

## Niepewność

Gdy referencja nie definiuje parametru, wynik nie może być opisany jako "dokładnie 1:1" w tym parametrze.
Status:
- `EXACT`
- `DERIVED`
- `INFERRED`
- `UNKNOWN`


---

## FILE: `10_reconstruction/102_EVIDENCE_MODEL.md`

# Reconstruction Evidence Model

Każde twierdzenie o modelu powinno mieć źródło dowodowe.

## Typy dowodów

### E0 — Explicit numeric
Wymiar, kąt, promień lub opis podany liczbowo.
Najwyższy priorytet geometryczny.

### E1 — Orthographic view
Front/side/top/rear/bottom bez istotnej perspektywy.

### E2 — Technical detail view
Zbliżenie lub przekrój pokazujący lokalny kształt.

### E3 — Perspective hero view
Dobre źródło:
- materiałów,
- edge language,
- relacji przestrzennych.
Słabsze źródło wymiarów.

### E4 — Text annotation
Opis funkcji, materiału, technologii.

### E5 — Manufacturing inference
Wniosek z konstrukcji.

### E6 — Artistic inference
Najniższy priorytet.
Dozwolone tylko przy braku mocniejszych dowodów.

## Evidence record

```text
evidence_id
type
source
view
region
claim
confidence
conflicts_with
notes
```

## Rule

Agent nie może nadpisać E0/E1 na podstawie E3/E6 bez zapisania konfliktu.


---

## FILE: `10_reconstruction/103_REFERENCE_INGESTION_PROTOCOL.md`

# Reference Ingestion Protocol

## Przed analizą geometrii

Dla każdego wejścia zapisz:
- file id / path,
- resolution,
- aspect ratio,
- orientation,
- whether cropped,
- whether perspective/orthographic,
- known dimensions visible,
- labels visible,
- source status: approved / draft / auxiliary.

## Concept sheet

Arkusz należy rozłożyć na osobne regiony:
- hero,
- front,
- side,
- top,
- rear,
- bottom,
- detail,
- material palette,
- notes,
- dimensions.

## Nie modeluj bez segmentacji

Cały arkusz jako jedna referencja utrudnia:
- dokładne skalowanie,
- kamerę QA,
- ROI,
- pomiar.

## Reference Registry

Po pierwszej poprawnej segmentacji utwórz trwały rejestr widoków.

```yaml
reference_registry:
  source:
    file: concept_art.png
    size_px: [1122, 1402]
  views:
    FRONT:
      roi: [x0, y0, x1, y1]
      projection: ORTHOGRAPHIC
      authority: HIGH
      validated: true
      crop_artifact: c_front_ortho.png
```

Każdy crop/ROI musi mieć provenance do oryginału.

Po zwalidowaniu rejestru nie segmentuj całego arkusza ponownie przy każdym kolejnym pomiarze.
Używaj `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md`.

## Original preservation

Nigdy nie nadpisuj oryginalnej referencji.
Przetworzone cropy muszą mieć provenance do oryginału.

## Rotation/crop policy

Zmiana:
- orientacji,
- cropu,
- kontrastu

jest dozwolona jako warstwa pomocnicza, ale musi być odwracalna i udokumentowana.

## Annotation separation

Na planszach technicznych odróżnij od geometrii:
- dimension lines;
- arrows;
- leaders;
- labels;
- icons;
- layout separators;
- marketing copy.

Nie pozwalaj, aby ciemna linia wymiarowa lub leader została włączona do maski sylwetki tylko dlatego, że znajduje się blisko obiektu.

## Analysis cache handoff

Po ingest/segmentation zapisz do cache:
- source metadata;
- view ROI;
- view classification;
- crop artifact paths;
- known explicit dimensions;
- exclusion regions/masks, jeśli są wymagane;
- unresolved segmentation conflicts.

Następne narzędzia pomiarowe mają korzystać z tych wpisów zamiast ponownie odkrywać cały arkusz.

## Output budget

Normalny wynik ingestu powinien być zwartym manifestem segmentów i konfliktów.

Nie zwracaj do LLM:
- pełnych danych pikselowych;
- dziesiątek próbek threshold;
- per-row/per-column profili;
- pełnych buforów obrazów.

Jeżeli konkretny ROI jest niejednoznaczny, eskaluj tylko ten ROI do trybu diagnostycznego.


---

## FILE: `10_reconstruction/104_CONCEPT_SHEET_SEGMENTATION.md`

# Concept Sheet Segmentation

## Cel

Zamienić planszę prezentacyjną na zestaw technicznych źródeł.

## Segment classes

- `HERO`
- `ORTHO_FRONT`
- `ORTHO_SIDE`
- `ORTHO_TOP`
- `ORTHO_REAR`
- `ORTHO_BOTTOM`
- `DETAIL`
- `MATERIAL_SAMPLE`
- `TEXT_NOTE`
- `DIMENSION`
- `BRANDING`
- `NON_ASSET_GRAPHICS`

## Non-asset graphics

Nie są częścią modelu:
- tytuły planszy,
- strzałki opisowe,
- ramki,
- legendy,
- ikonografia funkcji,
- stopki dokumentu.

## Asset graphics

Mogą być częścią assetu:
- nadruk na ekranie,
- logo na obudowie,
- oznaczenie portu,
- rzeczywista dioda,
- napis na elemencie.

## Segmentation output

Tabela:
| Segment | Bounding region | Class | Canonical | Purpose |

## Ambiguous graphic

Jeżeli nie wiadomo, czy element jest nadrukiem na obiekcie czy adnotacją planszy:
status `AMBIGUOUS_GRAPHIC`.
Nie modeluj go przed rozstrzygnięciem.


---

## FILE: `10_reconstruction/105_VIEW_CLASSIFICATION.md`

# View Classification

## Klasy projekcji

### ORTHOGRAPHIC
Brak zbieżności równoległych osi.
Nadaje się do bezpośredniego porównywania proporcji w płaszczyźnie.

### NEAR_ORTHOGRAPHIC
Mała perspektywa.
Może wymagać korekcji.

### PERSPECTIVE
Wymaga dopasowania kamery.

### STYLIZED
Nie musi być geometrycznie spójny.

## View axis

Określ:
- front axis,
- side direction,
- top direction,
- rear direction,
- bottom direction.

## Mirroring trap

Rear view nie powinien być automatycznie traktowany jako poziome odbicie front view.
Może pokazywać rzeczywistą asymetrię.

## Confidence

Każdy view otrzymuje:
- projection confidence,
- orientation confidence,
- geometry confidence.

## Rule

Nie twórz constraintu 3D z widoku, którego orientacja nie została ustalona.


---

## FILE: `10_reconstruction/106_VIEW_AUTHORITY_MATRIX.md`

# View Authority Matrix

## Cel

Ustalić, który widok rozstrzyga konkretną cechę.

## Przykładowa macierz

| Property | Primary authority | Secondary |
|---|---|---|
| total width | FRONT/TOP + numeric | REAR |
| total height | FRONT/SIDE + numeric | HERO |
| total depth | SIDE/TOP + numeric | HERO |
| backrest angle | SIDE | HERO |
| rear panel layout | REAR | HERO if visible |
| underside | BOTTOM | SIDE |
| material edge highlight | HERO/DETAIL | ORTHO |
| logo placement rear | REAR | DETAIL |

## Property-level authority

Nie istnieje jeden "najważniejszy widok" dla całego assetu.
Autorytet jest przypisany do właściwości.

## Conflict handling

Jeżeli dwa widoki o podobnym autorytecie są sprzeczne:
- oznacz konflikt,
- nie uśredniaj automatycznie,
- nie wybieraj bardziej atrakcyjnego renderu.


---

## FILE: `10_reconstruction/107_MULTI_VIEW_CONFLICT_RESOLUTION.md`

# Multi-View Conflict Resolution

## Typy konfliktów

- wymiarowy,
- topologiczny,
- materiałowy,
- feature presence,
- asymmetry,
- profile shape,
- perspective artifact.

## Procedura

1. zidentyfikuj konflikt,
2. określ właściwość,
3. przypisz evidence IDs,
4. porównaj authority,
5. sprawdź, czy konflikt wynika z projekcji,
6. wybierz rozwiązanie,
7. zapisz odrzuconą alternatywę.

## Resolution classes

### RESOLVED_EXPLICIT
Rozstrzygnięte liczbą lub opisem.

### RESOLVED_AUTHORITY
Rozstrzygnięte macierzą autorytetu.

### RESOLVED_PROJECTION
Różnica wynika z kamery.

### UNRESOLVED
Nie ma wystarczających dowodów.

## Zakaz średniej

Nie stosuj:
`(front_value + side_value)/2`
bez uzasadnienia.

Sprzeczne źródła nie stają się prawdziwe przez uśrednienie.


---

## FILE: `10_reconstruction/108_UNCERTAINTY_AND_CONFIDENCE_LEDGER.md`

# Uncertainty and Confidence Ledger

## Każdy istotny parametr otrzymuje confidence

- `LOCKED`: jawny wymiar/pewny dowód.
- `HIGH`: zgodny w kilku niezależnych widokach.
- `MEDIUM`: wyprowadzony z jednego dobrego widoku.
- `LOW`: inference.
- `UNKNOWN`: brak podstaw.

## Ledger

| Parameter | Value | Status | Confidence | Evidence | Affects |
|---|---:|---|---|---|---|

## High-impact uncertainty

Niski confidence jest krytyczny, jeśli wpływa na:
- silhouette,
- interface,
- feature MUST,
- animation clearance,
- modular fit.

## Uncertainty budget

Asset może zostać ukończony z niepewnością, ale raport musi wskazać:
- które parametry są inferowane,
- jak duży zakres alternatyw jest możliwy.

## No fake precision

Nie zapisuj:
`radius = 23.417 mm`
jeżeli referencja pozwala jedynie ocenić około 20–30 mm.


---

## FILE: `10_reconstruction/109_REFERENCE_PROVENANCE.md`

# Reference Provenance

## Cel

Każdy parametr i feature ma być możliwy do prześledzenia do źródła.

## Provenance chain

`Reference -> Segment -> Evidence -> Constraint -> Feature -> Scene owner -> QA result`

## Why

Bez provenance agent:
- zapomina, skąd wziął liczbę,
- nie wie, co zmienić po wymianie referencji,
- miesza dane z wcześniejszych wersji.

## Versioning

Każda referencja:
- id,
- revision,
- approval state,
- checksum/file metadata, jeśli pipeline pozwala.

## Stale reference

Jeśli concept sheet został zastąpiony:
- nie przepisuj nowych informacji na stary kontrakt po kawałku,
- oznacz affected constraints,
- uruchom impact analysis.


---

## FILE: `10_reconstruction/110_DIMENSION_GRAPH.md`

# Dimension Graph

## Cel

Nie przechowywać wymiarów jako luźnej listy.
Zbudować graf zależności.

## Nodes

Przykłady:
- total_width,
- total_height,
- seat_height,
- side_housing_width,
- backrest_width,
- trim_width,
- gap.

## Edges

Relacje:
- sum,
- difference,
- ratio,
- alignment,
- symmetry,
- containment.

Przykład:
```text
backrest_width =
total_width
- left_housing_width
- right_housing_width
```

## Constraint types

- equality,
- inequality,
- min/max clearance,
- ratio,
- centered,
- aligned,
- tangent.

## Benefit

Zmiana jednego parametru może zostać propagowana bez ręcznego "poprawiania na oko".

## Rule

Dla assetu rekonstrukcyjnego parametry D0/D1 powinny wynikać z jednego spójnego dimension graph.


---

## FILE: `10_reconstruction/111_DIMENSION_LOCKING_AND_TOLERANCES.md`

# Dimension Locking and Tolerances

## Lock classes

### HARD LOCK
Wartość nie może się zmienić bez zmiany kontraktu.

### DERIVED LOCK
Wynika z innych locków.

### SOFT TARGET
Powinna zostać zachowana, ale może być skorygowana przy konflikcie.

### FREE
Nie określona.

## Tolerancje

Tolerancja zależy od typu parametru.

### Interface / modular
Praktycznie zerowa w granicach precyzji pipeline.

### Global dimensions
Domyślnie bardzo mała, jeśli wymiar jest jawny.

### Measured-from-image
Tolerancja uwzględnia:
- rozdzielczość,
- anti-aliasing,
- grubość linii,
- perspektywę.

### Material appearance
Nie opisuj tolerancji w milimetrach; użyj QA wizualnego.

## Lock report

Przed PRIMARY_DETAIL wydrukuj wszystkie HARD LOCK.
Po każdej zmianie strukturalnej sprawdź je ponownie.


---

## FILE: `10_reconstruction/112_LANDMARK_AND_KEYPOINT_SYSTEM.md`

# Landmark and Keypoint System

## Cel

Porównywać konkretne punkty zamiast ogólnego wrażenia.

## Landmark classes

- bounding corners,
- feature centers,
- bend points,
- tangent transition points,
- panel corners,
- hole centers,
- logo anchor,
- seat/back junction,
- trim start/end.

## Record

```text
landmark_id
feature_id
3d_owner
view
reference_xy_normalized
projection_xy
tolerance_px_or_normalized
status
```

## Multi-view landmarks

Ten sam punkt 3D może występować w wielu widokach.
To szczególnie cenne do kontroli głębokości.

## Do not overfit

Nie twórz setek landmarków bez potrzeby.
D0/D1: mała liczba krytycznych punktów.
D2: dodatkowe lokalne punkty.


---

## FILE: `10_reconstruction/113_REFERENCE_COORDINATE_REGISTRATION.md`

# Reference Coordinate Registration

## Cel

Ustawić różne widoki we wspólnym układzie 3D.

## Asset coordinate frame

Zdefiniuj:
- origin,
- X,
- Y,
- Z,
- front,
- ground plane.

## Orthographic registration

Dla każdego rzutu określ:
- physical width represented,
- physical height represented,
- image crop,
- image center,
- axis orientation.

## Anchor

Preferuj:
- known total dimension,
- ground contact,
- centerline,
- external bounds.

## Same-scale rule

Jeżeli front i rear przedstawiają ten sam wymiar 2000 mm, ich image planes powinny zostać skalibrowane do tej samej szerokości świata.

## Offset

Nie centruj każdego widoku "na oko".
Rejestruj według:
- centerline,
- ground,
- bounds.

## Result

Każdy reference plane może zostać użyty jako wiarygodne tło QA/modeling.


---

## FILE: `10_reconstruction/114_ORTHOGRAPHIC_REFERENCE_CALIBRATION.md`

# Orthographic Reference Calibration

## Cel

Zamienić rzut obrazkowy na mierzalną płaszczyznę.

## Inputs

- crop size px,
- known dimension,
- dimension line endpoints,
- object boundary,
- world axis.

## Scale derivation

Jeżeli odcinek `P px` odpowiada `L m`:
`meters_per_pixel = L / P`

Używaj tylko dla tej samej płaszczyzny rzutu.

## Dimension arrows

Preferuj mierzenie między markerami linii wymiarowej, nie między rozmytymi krawędziami renderu.

## Calibration checks

Po ustawieniu:
- total bounds muszą zgadzać się z wymiarem,
- ground line ma być wspólna,
- centerline powinna być spójna między widokami.

## Warning

Plansze marketingowe mogą nie mieć idealnie technicznych rzutów mimo etykiety "front view".
Status takiego widoku może być `NEAR_ORTHOGRAPHIC`.


---

## FILE: `10_reconstruction/115_PERSPECTIVE_CAMERA_SOLVING.md`

# Perspective Camera Solving

## Cel

Dopasować kamerę hero/detail tak, aby nie deformować modelu dla uzyskania podobnego renderu.

## Solve variables

- camera rotation,
- camera translation,
- focal length,
- sensor/fit,
- shift,
- object pose, jeśli nie jest już zablokowany.

## Landmark solve

Wybierz punkty o znanej lub zablokowanej geometrii:
- corners,
- panel intersections,
- base contacts.

Minimalizuj reprojection error.

## Solve order

1. zablokuj global dimensions,
2. zablokuj orientation,
3. oszacuj camera,
4. dopiero potem oceniaj hero view.

## Lens warning

Szerokokątna kamera może:
- powiększyć bliższy bok,
- zmienić apparent depth,
- zwiększyć różnicę wysokości.

Nie poprawiaj tego przez asymetryczne skalowanie modelu.

## QA

Po solve hero view jest materiałowym i detalicznym źródłem, ale geometryczny authority pozostaje zgodny z macierzą.


---

## FILE: `10_reconstruction/116_SILHOUETTE_CONSTRAINT_SYSTEM.md`

# Silhouette Constraint System

## Silhouette is D0

Dla każdego kanonicznego widoku utwórz:
- maskę referencji,
- maskę renderu,
- contour representation.

## Metrics

Możliwe:
- intersection over union,
- area error,
- contour distance,
- directional extrema error.

## Extrema

Kontroluj:
- leftmost,
- rightmost,
- topmost,
- bottommost,
- charakterystyczne lokalne extrema.

## Weighted contour

Nie wszystkie fragmenty obrysu są równie ważne.
Wyższa waga:
- charakterystyczne skosy,
- transition seat/back,
- nogi,
- podłokietniki,
- główne łuki.

## Gate

Nie dodawaj D2/D3, jeśli silhouette D0/D1 nie przechodzi wszystkich kanonicznych widoków.


---

## FILE: `10_reconstruction/117_NEGATIVE_SPACE_AND_CLEARANCE.md`

# Negative Space and Clearance Constraints

## Negative space jest geometrią pośrednią

Często łatwiej wykryć błąd po kształcie pustej przestrzeni niż po powierzchni.

## Przykłady

- przestrzeń pod ławką,
- przerwa między siedziskiem a bokiem,
- otwór w uchwycie,
- dystans panelu od ramy.

## Record

```text
space_id
bounded_by
view
width/height/profile
priority
```

## Gameplay clearance

Jeśli przestrzeń ma funkcję:
- przejście,
- chwyt,
- nogi postaci,
- ruch mechanizmu,

otrzymuje constraint funkcjonalny niezależnie od wyglądu.

## QA

Porównuj negative-space masks w widokach ortograficznych.


---

## FILE: `10_reconstruction/118_CROSS_SECTION_INFERENCE.md`

# Cross-Section Inference

## Problem

Front/side/top nie zawsze definiują profil przekroju.

## Evidence order

1. detail close-up,
2. visible edge in hero,
3. material boundary,
4. manufacturing logic,
5. minimal plausible section.

## Cross-section classes

- rectangular,
- rounded rectangle,
- chamfered,
- tapered,
- hollow shell,
- layered sandwich,
- custom spline.

## Unknown section

Jeżeli przekrój nie jest widoczny:
- nie dodawaj skomplikowanego profilu,
- wybierz minimalny profil spełniający wszystkie widoki,
- oznacz jako `INFERRED`.

## Section stations

Dla zmiennej geometrii definiuj profile w kilku stacjach:
- base,
- mid,
- transition,
- top.

Można następnie loftować/łączyć je kontrolowanie.


---

## FILE: `10_reconstruction/119_HIDDEN_AND_OCCLUDED_GEOMETRY_POLICY.md`

# Hidden and Occluded Geometry Policy

## Cztery klasy

### H0 — explicitly shown
Musi być odwzorowane zgodnie z referencją.

### H1 — functionally required
Niewidoczne, ale potrzebne do działania lub poprawnej bryły.

### H2 — runtime required
Collision, backing surface, closed volume itp.

### H3 — unknowable
Brak dowodów i brak konieczności.

## H3 policy

Nie inventuj szczegółów.
Zastosuj:
- prostą powierzchnię,
- logiczne domknięcie,
- minimalną konstrukcję.

## Occluded transition

Jeśli dwie widoczne części muszą się połączyć za przeszkodą:
rekonstrukcja ma użyć najprostszego ciągłego połączenia, które nie łamie innych widoków.

## Report

Każda większa H3 powierzchnia powinna być oznaczona jako inferred.


---

## FILE: `10_reconstruction/120_SYMMETRY_AND_ASYMMETRY_POLICY.md`

# Symmetry and Asymmetry Policy

## Symmetry is evidence, not default

Sprawdź:
- front,
- rear,
- top,
- detail,
- functional annotations.

## Symmetry classes

- geometric symmetric,
- shell symmetric,
- material asymmetric,
- accessory asymmetric,
- intentionally asymmetric.

## Build strategy

Jeśli rdzeń jest symetryczny:
- Mirror jest preferowany na wczesnym etapie.

Jeśli tylko utility panel jest po jednej stronie:
- rdzeń pozostaje mirrorable,
- panel jest osobnym obiektem/feature.

## Mirror break

Zanim zastosujesz asymetryczną operację:
- zapisz stage,
- ustal, które features pozostają wspólne.

## QA

Nie wymagaj pixel symmetry od elementów celowo asymetrycznych.


---

## FILE: `10_reconstruction/121_PROFILE_AND_CURVATURE_INFERENCE.md`

# Profile and Curvature Inference

## Problem

Referencja często pokazuje "zaokrąglony bok", ale nie podaje promienia.

## Rozróżniaj

- circular arc,
- fillet,
- bevel,
- spline transition,
- compound curvature,
- chamfer.

## Evidence

Grazing highlight nie jest sam w sobie dowodem dokładnego promienia.
Łącz:
- silhouette,
- orthographic contour,
- detail,
- manufacturing logic.

## Curvature control

Dla ważnego profilu preferuj:
- parametric bevel,
- curve profile,
- explicit support geometry,

zamiast ręcznego "wygładzania".

## Radius range

Jeśli nieznany:
zapisz zakres, np. `R ~= 20–30 mm`, a nie fałszywie dokładną liczbę.

## QA

Ocena:
- silhouette,
- highlight width pod stałym światłem,
- transition continuity.


---

## FILE: `10_reconstruction/122_EDGE_RADIUS_AND_BEVEL_ESTIMATION.md`

# Edge Radius and Bevel Estimation

## Edge taxonomy

- structural hard edge,
- manufactured fillet,
- cosmetic bevel,
- soft molded transition,
- protected edge trim.

## Estimation

Ustal:
1. skala obiektu,
2. widoczna szerokość highlightu,
3. contour change,
4. materiał,
5. sposób produkcji.

## Multiple bevel families

Nie używaj jednego bevel width dla całego assetu.

Przykładowe rodziny:
- `BVL_STRUCTURAL`
- `BVL_PANEL`
- `BVL_TRIM`
- `BVL_MICRO`

## Segment budget

Segment count zależy od:
- promienia,
- dystansu kamery,
- LOD.

## Hard rule

Bevel nie może zmienić locked outer dimension, jeśli kontrakt wymaga zachowania wymiaru zewnętrznego.
Plan musi uwzględniać sposób limit/offset.


---

## FILE: `10_reconstruction/123_THICKNESS_GAPS_AND_PANEL_LINES.md`

# Thickness, Gaps and Panel Lines

## Parametry osobno

Nie mieszaj:
- grubości materiału,
- szczeliny montażowej,
- rowka dekoracyjnego,
- shadow gap,
- recess depth.

## Gap consistency

Powtarzalna szczelina powinna być parametrem:
`GAP_MAIN`, nie serią ręcznych przesunięć.

## Visible-from-distance test

Jeżeli panel line ma być czytelny z typowego dystansu:
- musi mieć wystarczający rozmiar geometryczny/teksturalny,
- ale nie może być sztucznie przeskalowany bez decyzji artystycznej.

## Geometry choice

Gap:
- real geometry dla głębokich i ważnych,
- normal/decal dla mikroszczelin,
- shader tylko jeśli runtime to wspiera.

## QA

Kontroluj szerokość i ciągłość szczelin na:
- prostych,
- narożnikach,
- przejściach między częściami.


---

## FILE: `10_reconstruction/124_MATERIAL_EVIDENCE_RECONSTRUCTION.md`

# Material Evidence Reconstruction

## Material identity

Dla każdej strefy ustal:
- material family,
- base color family,
- metallic/dielectric,
- roughness range,
- surface directionality,
- micro-normal,
- transparency,
- emissive.

## Evidence priority

1. material palette / annotation,
2. detail close-up,
3. hero render,
4. orthographic view.

## Material segmentation

Najpierw odtwórz poprawne granice materiałów.
Dopiero potem stroisz parametry shaderów.

## Do not bake lighting into albedo

Highlight, cień i ambient w concept arcie nie są kolorem materiału.

## Material uncertainty

Jeśli materiał opisany jako "dark titanium composite":
nie zakładaj automatycznie czystego metalu.
Nazwa może być językiem designu, nie fizycznym składem.

Zastosuj tekstowe evidence razem z appearance.


---

## FILE: `10_reconstruction/125_LIGHTING_VS_MATERIAL_DISENTANGLEMENT.md`

# Lighting vs Material Disentanglement

## Problem

Concept art zawiera lighting, który może wyglądać jak:
- jaśniejszy materiał,
- gradient albedo,
- metaliczny pas,
- edge wear,
- głębszy relief lub większy bevel niż faktycznie istnieje.

## Test

Porównaj ten sam region w:
- hero,
- front,
- side,
- material palette,
- neutral geometry QA, jeśli model już istnieje.

Jeżeli jasność zmienia się wraz z orientacją powierzchni:
prawdopodobnie to lighting/reflection.

## Brushed metal

Kierunkowy highlight nie powinien być kopiowany do base color jako stała jasna smuga.

## Ambient blue

Niebieskie odbicie od emissive/underglow nie jest kolorem sąsiedniego grafitu.

## QA material rig

Stosuj neutralne, powtarzalne studio lighting do porównania materiałów.

## Geometry compensation trap

Jeżeli feature jest słabo widoczny w jednym renderze, nie zwiększaj automatycznie:
- wysokości panelu;
- głębokości rowka;
- szerokości szczeliny;
- bevel width;
- rozmiaru emitera.

Najpierw rozdziel przyczynę:

```text
GEOMETRY
MATERIAL
LIGHTING
CAMERA
OCCLUSION
REFERENCE AMBIGUITY
```

Geometry change is allowed only when supported by geometric/reference evidence or an explicit functional requirement.

A detail that disappears because it is physically behind the host surface is `OCCLUSION/GEOMETRY PLACEMENT`, not a material problem.

A detail that exists geometrically but has weak contrast under a specific light should first be tested with neutral/matcap QA before changing dimensions.

## Reconstruction priority

For 1:1 reconstruction:

```text
explicit dimension / ortho evidence
> neutral geometry QA
> material appearance
> hero readability preference
```

Do not make geometry less faithful merely to make one hero render easier to read.


---

## FILE: `10_reconstruction/126_BRANDING_TEXT_AND_DECAL_EXACTNESS.md`

# Branding, Text and Decal Exactness

## Najpierw klasyfikacja

Element tekstowy może być:
- realnym nadrukiem na assetcie,
- interfejsem wyświetlacza,
- etykietą techniczną,
- adnotacją concept sheet.

Tylko pierwsze trzy trafiają do assetu.

## Exactness

Dla realnego brandingu:
- spelling,
- casing,
- alignment,
- orientation,
- scale,
- anchor position

są feature constraints.

## Geometry vs texture

Preferuj decal/texture dla:
- logotypów,
- drobnego tekstu,
- ikon.

Geometria tylko gdy:
- tekst jest fizycznie tłoczony,
- silhouette/parallax ma znaczenie.

## Unknown font

Nie zgaduj "podobnej" typografii jako 1:1.
Status:
`FONT_UNRESOLVED`
lub użyj dostarczonego logo jako grafiki.

## Handedness and surface-facing orientation

Czytelność tekstu/decalu musi być walidowana w **docelowym widoku powierzchni**, nie wyłącznie przez lokalny UV layout.

Jeżeli pipeline posiada export handedness compensation, np. `MIRROR_X`:
- nie stosuj jednego globalnego `mirror_u` do wszystkich decal planes;
- front-facing i rear-facing surface mogą wymagać przeciwnej authoring-space orientacji;
- orientation rule musi uwzględniać surface normal / canonical view;
- nie kompensuj ponownie ręcznie transformacji, którą wykona exporter/runtime, bez proof.

Wymagany test dla readable feature:

```text
canonical face/view
-> exported or runtime-equivalent orientation
-> readable text/logo
-> PASS
```

Dla front/rear technical labels utrzymuj osobne Feature IDs, jeżeli ich surface facing jest różny.

## QA

Porównuj ROI w widoku kanonicznym.

Dla tekstu/logo PASS wymaga:
- poprawnej orientacji;
- braku mirror/reversal;
- poprawnego anchor/scale;
- evidence z canonical ROI albo exported/runtime-equivalent readback/render.

Samo poprawne UV w authoring space nie jest dowodem po eksporcie, jeśli aktywny projekt stosuje handedness conversion.


---

## FILE: `10_reconstruction/127_REFERENCE_COLOR_MANAGEMENT.md`

# Reference Color Management

## Cel

Nie interpretować różnic color-management jako różnic materiałowych.

## Record

Dla referencji, jeśli wiadomo:
- color space/profile,
- gamma,
- HDR/SDR,
- compression.

Dla renderu QA:
- render engine,
- view transform,
- look,
- exposure,
- output format.

## Consistency

Wszystkie checkpointy porównawcze muszą używać tego samego color pipeline.

## Concept art caveat

Obraz marketingowy mógł zostać:
- tonemapped,
- retuszowany,
- sharpened,
- compressed.

Dlatego geometryczne QA nie powinno zależeć od koloru.

## Separate pipelines

- geometry QA: mask/neutral,
- material QA: controlled render,
- final beauty: aesthetic.


---

## FILE: `10_reconstruction/128_RECONSTRUCTION_OBJECT_DECOMPOSITION.md`

# Reconstruction Object Decomposition

## Cel

Podzielić asset według **hierarchii form projektowych**, a nie tylko przyszłych Blender objects.

Od v0.9 canonical output tego etapu jest `Reconstruction Shape Graph` z `174_RECONSTRUCTION_SHAPE_GRAPH.md`.

```text
reference evidence
-> design-form decomposition
-> Shape Graph
-> scene implementation
```

## Najpierw forma, potem object

Nie zaczynaj od pytania:

> Ile obiektów utworzyć w Blenderze?

Najpierw ustal:
- global envelope;
- primary forms definiujące sylwetkę;
- structural transitions;
- secondary structural forms;
- hosted structural features;
- edge-language owners;
- surface/detail owners.

Canonical levels:

```text
G0 GLOBAL_ENVELOPE
G1 PRIMARY_FORM
G2 SECONDARY_STRUCTURAL_FORM
G3 STRUCTURAL_FEATURE
G4 EDGE_LANGUAGE
G5 SURFACE_DETAIL
```

## Shape Node vs Blender Object

`Shape Node != Blender Object`.

Jeden node może być implementowany przez:
- final mesh;
- cage + cutters;
- section curves;
- temporary helper objects;
- curve + modifier stack.

Kilka małych scene objects może należeć do jednego node'a, jeżeli razem implementują jedną odpowiedzialność geometryczną.

## Kryteria osobnej formy/node'a

Oddziel node, jeśli część:
- ma własną odpowiedzialność za canonical silhouette/proportion;
- stanowi structural transition;
- ma własny authoritative view/ROI contract;
- jest hostem dla zależnych features;
- wymaga osobnej shape representation;
- może FAIL niezależnie od parenta;
- ma stabilną rolę funkcjonalną/assembly.

## Kryteria osobnego Blender object

Po zaakceptowaniu decomposition oddziel scene object, jeśli część:
- ma osobny materiał i wyraźną granicę;
- jest nakładką;
- będzie animowana;
- jest asymetrycznym akcesorium;
- ma być wariantowana;
- jest boolean cutter/helper;
- wymaga osobnego runtime fate.

To decyzja implementacyjna, downstream od Shape Graph.

## Nie rozdrabniaj

Nie twórz osobnego Shape Node dla każdej śrubki/seam, jeżeli:
- nie ma własnego geometric/QA ownership;
- jest powtórzeniem jednej feature family;
- może być child feature należącym do jednego host node.

## Required decomposition table

| Shape Node | G-level | RDL | Parent | Role | Shape class | Authoritative views | Feature IDs |

Tabela/lista jest wejściem do pełnego Shape Graph.

## Stable boundaries

Decomposition powstaje **przed produkcyjną geometrią**.

Zmiana granic G0–G3 po rozpoczęciu modelowania:
- tworzy nową graph revision;
- dirties affected nodes i zależne children;
- wymaga ponownej walidacji odpowiedniego RDL barrier.

Nie redefiniuj primary form tylko dlatego, że obecny skrypt Blendera jest łatwiejszy do napisania inaczej.

## Rule

Jeżeli decomposition jest tylko listą scene object names bez hierarchy, shape class, view responsibilities i dependencies, etap `DECOMPOSE` nie jest zakończony.


---

## FILE: `10_reconstruction/129_FEATURE_TO_MODELING_STRATEGY_MAP.md`

# Feature-to-Modeling Strategy Map

## Cel

Każdy Shape Node / Feature ID powinien zostać przypisany do techniki **dopiero po sklasyfikowaniu formy**.

Canonical decision order v0.9:

```text
design role
-> Shape Graph node
-> shape class / mathematical representation
-> semantic skill
-> Blender implementation
```

Agent nie może wybrać techniki tylko dlatego, że zna operator.

## Shape representation classes

Primary classes:
- ENVELOPE
- PARAMETRIC_PRIMITIVE
- EXTRUDED_PROFILE
- REVOLVED_PROFILE
- PROFILE_SWEEP
- MULTI_SECTION_LOFT
- MULTI_SECTION_TRANSITION
- SUBD_FREEFORM
- BOOLEAN_RECESS
- PANEL_LINE
- LAYERED_ASSEMBLY
- HYBRID_ASSEMBLY

Canonical definitions są w `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md`.

## Implementation strategy classes

- PARAMETRIC_PRIMITIVE
- DIRECT_MESH
- BMESH_PROCEDURAL
- SECTION_LOFT_HARD_SURFACE
- EXTRUDED_PROFILE
- PROFILE_SWEEP
- AXISYMMETRIC_PROFILE
- BOOLEAN_RECESS
- BOOLEAN_UNION
- SOLIDIFY_SHELL
- BEVEL
- CURVE_PROFILE
- SUBD_TOPOLOGY_CONTROL
- ARRAY_INSTANCE
- RADIAL_REPEAT
- GEOMETRY_NODES
- FLOATING_DETAIL
- PANEL_LINE
- DECAL
- NORMAL_BAKE
- MATERIAL_ONLY

## Selection criteria

Uwzględnij:
- wpływ na silhouette;
- authoritative views;
- cross-section behavior;
- editability;
- precision;
- repeated use;
- shading/continuity;
- host/parent relation;
- runtime;
- risk of regression.

## Routing examples

### Osiowo symetryczny stacked profile

```text
REVOLVED_PROFILE
-> AXISYMMETRIC_PROFILE
```

### Base zmienia width + depth + corner plan po Z

```text
MULTI_SECTION_LOFT
-> SECTION_LOFT_HARD_SURFACE
```

### Shoulder łączący dwa zaakceptowane przekroje

```text
MULTI_SECTION_TRANSITION
-> SECTION_LOFT_HARD_SURFACE
```

### Głęboki panel

```text
BOOLEAN_RECESS
-> BOOLEAN_RECESS / DIRECT_MESH
```

### Wąski seam

```text
PANEL_LINE
-> HS_PANEL_LINE
```

### Smooth compound shell bez stabilnych section stations

```text
SUBD_FREEFORM
-> SUBD_TOPOLOGY_CONTROL
```

### Logo

```text
G5 SURFACE_DETAIL
-> DECAL
```

### Niebieski light strip

```text
G3 STRUCTURAL_FEATURE
-> separate geometry + emissive material
```

## Box-abuse rule

Jeżeli primary node:
- zmienia width wzdłuż osi;
- zmienia depth wzdłuż osi;
- ma zmienny corner/chamfer treatment;
- pokazuje continuous surface między stacjami;

to `PARAMETRIC_PRIMITIVE + BEVEL` nie może być default strategy.

Najpierw rozważ `MULTI_SECTION_LOFT` albo `SUBD_FREEFORM`.

## Leaf-skill rule

Skille detalu są downstream od zaakceptowanego hosta.

Przykłady:
- `HS_PANEL_LINE` nie naprawia błędnego primary shell;
- `BEVEL` nie naprawia złego base cross-section;
- `DECAL` nie jest budowany na panelu, który jeszcze FAIL;
- material finish nie kompensuje błędnej geometrii.

## Strategy switch

Po jednej poprawionej ponownej próbie tej samej strategii, jeżeli authoritative views nadal wskazują niezgodność 3D:
- re-inspect registration/parameters;
- re-open shape classification;
- zmień representation zamiast wykonywać nieskończone lokalne tweaki.


---

## FILE: `10_reconstruction/130_PARAMETRIC_MASTER_MODEL.md`

# Parametric Master Model

## Cel

D0/D1 model powinien być sterowany małym zestawem parametrów.

## Master parameters

- bounds,
- primary widths,
- heights,
- depths,
- main angles,
- major radii,
- major gaps.

## Derived parameters

Obliczaj:
- inner widths,
- center offsets,
- mirrored positions,
- panel dimensions.

## Benefits

- łatwe korekty po pomiarze,
- mniej mikroruchów,
- spójność widoków,
- mniej tool calls.

## Freeze levels

### F0
Wszystko parametryczne.

### F1
D0/D1 locked.

### F2
D2 locked.

### F3
Bake/UV critical geometry frozen.

## Rule

Nie freeze'uj master modelu przed przejściem multi-view blockout gate.


---

## FILE: `10_reconstruction/131_DIMENSION_LOCKED_BLOCKOUT.md`

# Dimension-Locked Blockout

## Blockout ma już być mierzalny

Nie oznacza "luźnych kostek".
Powinien spełniać:
- total bounds,
- primary division,
- seat/back/leg positions,
- główne kąty,
- negative spaces.

## Allowed

- proste bryły,
- mała liczba segmentów,
- approximate bevel only jeśli wpływa na silhouette.

## Forbidden

- tekstury,
- branding,
- mikrodetale,
- final bake,
- kosmetyczne śruby.

## Gate

Blockout przechodzi tylko, gdy:
- wszystkie HARD LOCK pass,
- silhouette pass w kanonicznych widokach,
- negative space pass,
- primary landmarks pass.

## Repair

Jeżeli FAIL:
wróć do dimension graph, nie maskuj błędu bevelami.


---

## FILE: `10_reconstruction/132_PRECISION_HARD_SURFACE_CONSTRUCTION.md`

# Precision Hard-Surface Construction

## Precision hierarchy

1. numeric parameters,
2. constraints/derived values,
3. snapping,
4. measured local edits,
5. visual freehand only dla low-impact detail.

## Transform discipline

Dla konstrukcji:
- używaj osi,
- jawnych wartości,
- lokalnych układów,
- originów zgodnych z częścią.

## Clean primitive strategy

Zaczynaj od geometrii, która odpowiada przekrojowi.
Nie twórz bardzo złożonej siatki, jeśli parametric primitive + modifier zachowa precyzję.

## Edge placement

Edge loops powinny istnieć z powodu:
- shape,
- shading,
- topology requirement.

Nie "dla bezpieczeństwa".

## Precision regression

Po bevel/solidify/boolean sprawdź:
- locked bounds,
- alignment,
- gap widths.


---

## FILE: `10_reconstruction/133_BOOLEAN_RECESS_AND_TRIM_PLAYBOOK.md`

# Boolean, Recess and Trim Playbook

## Recess

Dla wpuszczonego panelu określ:
- outer outline,
- border width,
- recess depth,
- corner radius,
- bottom surface.

## Boolean cutter

Cutter powinien:
- mieć kontrolowane wymiary,
- być tagowany feature ID,
- posiadać wystarczające przenikanie,
- nie tworzyć przypadkowych coplanar contacts.

## Trim

Trim jako osobny mesh jest preferowany, gdy:
- ma inny materiał,
- tworzy własną silhouette,
- ma kontrolowaną grubość.

## Modifier order

Kolejność musi zostać zapisana per object.
Typowy problem:
bevel przed/po boolean daje inny wynik.

## Cleanup

Po boolean sprawdź:
- slivers,
- shading,
- tiny faces,
- nienaturalne pinching.

## Feature ownership

Cutter/helper nie jest feature owner po apply, jeśli zostaje usunięty.
Owner staje się finalny mesh/region.


---

## FILE: `10_reconstruction/134_PANEL_GAPS_SEAMS_AND_JUNCTIONS.md`

# Panel Gaps, Seams and Junctions

## Junction classes

- flush,
- recessed,
- overlapping,
- wrapped trim,
- open shadow gap,
- mechanical joint.

## T-junction / corner

Szczelina musi zachowywać logikę na narożniku.
Nie może nagle:
- zmieniać szerokości,
- kończyć się bez powodu,
- przecinać trimu.

## Continuous seam

Jeżeli seam biegnie przez dwie płaszczyzny:
traktuj go jako jedną cechę przestrzenną, nie dwa niezależne rowki.

## QA

Sprawdź seam w:
- front,
- side,
- 3/4 grazing light.

## Manufacturing evidence

Seam często wskazuje prawdziwy podział części.
Może być ważniejszy od tego, jak najłatwiej modelować jedną siatkę.


---

## FILE: `10_reconstruction/135_REAR_BOTTOM_AND_UNDERSIDE_RECONSTRUCTION.md`

# Rear, Bottom and Underside Reconstruction

## Zasada

Jeżeli arkusz pokazuje rear/bottom, są to kanoniczne widoki, nie "opcjonalne detale".

## Rear

Kontroluj:
- panel extent,
- logo placement,
- side housing continuation,
- bottom opening,
- fasteners.

## Bottom

Kontroluj:
- service panels,
- structural rails,
- feet,
- cable/electronics covers,
- symmetry,
- attachment zones.

## Simplification

Runtime może mieć uproszczenie, ale:
- authoring reconstruction powinien najpierw odtworzyć evidence,
- uproszczony wariant jest osobnym LOD/optimization step.

## Hero-only trap

Asset nie może być pustą "fasadą" poprawną tylko od przodu.


---

## FILE: `10_reconstruction/136_FASTENERS_REPETITION_AND_MICRODETAIL.md`

# Fasteners, Repetition and Microdetail

## Fastener significance

Śruba może być:
- konstrukcyjna i widoczna,
- dekoracyjna,
- niemal niewidoczna.

Nie wszystkie wymagają geometrii.

## Repetition

Powtarzalne detale:
- instancing,
- array,
- Geometry Nodes.

## Alignment

Fasteners powinny wynikać z:
- panel logic,
- symmetry,
- regular spacing.

Nie rozmieszczaj losowo dla "sci-fi look".

## D3/D4 gate

Microdetail dopiero po pełnym przejściu D0–D2.

## Runtime

W LOD:
- geometry -> decal/normal -> remove
zgodnie z czytelnością.


---

## FILE: `10_reconstruction/137_ELECTRONICS_DISPLAYS_EMISSIVE_GLASS.md`

# Electronics, Displays, Emissive and Glass

## Electronics panel

Rozdziel:
- physical housing,
- recess,
- port geometry,
- screen/light,
- printed icons.

## Emissive strip

Określ:
- physical width,
- recess/flush state,
- diffuser cover,
- emissive color,
- runtime light behavior osobno.

## Display

Treść ekranu jest materiałem/texture/UI feature, nie geometrią obudowy.

## Glass

Zdecyduj:
- rzeczywista grubość czy single plane,
- opaque coated plastic vs transparent material,
- runtime transparency mode.

## QA

Sprawdź w dwóch profilach:
- neutral geometry,
- final material.

Emisja nie może maskować błędnego kształtu.


---

## FILE: `10_reconstruction/138_MODIFIER_STACK_AND_FREEZE_POINTS.md`

# Modifier Stack and Freeze Points

## Reconstruction stack

Dla każdego obiektu zapisz:
- modifier,
- purpose,
- feature IDs,
- dependency,
- freeze condition.

## Freeze points

### P0
Po blockout — zachowaj parametric.

### P1
Po D2 matching — można zamrozić wybrane booleans.

### P2
Przed UV/bake — topology-critical freeze.

### P3
Export copy — final evaluated mesh.

## Do not apply early

Wczesne Apply utrudnia:
- korekty wymiarów,
- zmianę gap/radius,
- feature regression.

## Do not keep everything live forever

Zbyt złożony stack:
- utrudnia stabilność,
- może być kosztowny,
- może powodować zależności.

Freeze jest decyzją pipeline, nie dogmatem.


---

## FILE: `10_reconstruction/139_TOPOLOGY_AFTER_GEOMETRIC_MATCH.md`

# Topology After Geometric Match

## Kolejność

Najpierw poprawna geometria, potem optymalizacja topologii.

## Zakaz

Nie zmieniaj kształtu tylko po to, aby uzyskać "ładniejsze quady", jeśli:
- asset jest statyczny,
- shading i export są poprawne.

## Retopology goals

- silhouette preservation,
- stable triangulation,
- clean shading,
- UV suitability,
- lower cost.

## Critical edges

Zachowaj:
- profile,
- panel borders,
- bevel support,
- deformation edges, jeśli istnieją.

## Validation

Po cleanup/retopo:
uruchom silhouette + landmarks + MUST regression.


---

## FILE: `10_reconstruction/140_UV_AND_MATERIALS_AFTER_MATCH.md`

# UV and Materials After Match

## Gate

Final UV nie powinno powstać przed zaakceptowaniem D0–D2, chyba że workflow wymaga wcześniejszego testu.

## Why

Zmiana geometrii po starannym UV:
- zwiększa koszt,
- tworzy nieciągłości,
- może popsuć bake.

## Material IDs

Granice materiałów powinny już wynikać z Feature Contract.

## UV priorities

- directional material orientation,
- consistent texel density,
- visible seams placement,
- logo/decal anchors,
- bake requirements.

## Reconstruction-specific QA

Sprawdź, czy mapa nie zmienia:
- apparent scale brushed metal,
- directionality,
- logo proportions.


---

## FILE: `10_reconstruction/141_RECONSTRUCTION_QA_CAMERA_RIG.md`

# Reconstruction QA Camera Rig

## Stały zestaw kamer

Dla pełnego concept sheet:
- FRONT_ORTHO
- REAR_ORTHO
- LEFT/RIGHT_SIDE_ORTHO
- TOP_ORTHO
- BOTTOM_ORTHO
- HERO_MATCH
- DETAIL_MATCH

## Ortho cameras

Mają:
- zablokowaną orientację,
- skalę wynikającą z bounds,
- ten sam framing margin,
- stałą rozdzielczość.

## Camera metadata

Każda kamera:
- id,
- source segment,
- projection,
- lens/ortho scale,
- transform,
- resolution,
- revision.

## Lock

QA camera nie jest kamerą artystyczną.
Po kalibracji nie należy jej ruszać podczas napraw geometrii.

## Camera failure

Jeśli trzeba ruszyć QA camera, traktuj to jako zmianę kalibracji i ponownie waliduj baseline.


---

## FILE: `10_reconstruction/142_ORTHOGRAPHIC_OVERLAY_VALIDATION.md`

# Orthographic Overlay Validation

## Cel

Nałożyć render modelu na referencję w tej samej projekcji.

## Warstwy

- reference,
- candidate,
- alpha overlay,
- edge overlay,
- diff.

## Alignment

Przed oceną:
- same physical scale,
- same centerline,
- same ground plane,
- same crop/aspect.

## Colors

Kolory overlay są narzędziem QA, nie częścią finalnego assetu.

## Oceniaj

- external contour,
- panel boundaries,
- landmarks,
- feature positions.

## Do not compensate

Nie przesuwaj obrazu referencyjnego osobno dla każdego feature.
Rejestracja jest globalna dla widoku.


---

## FILE: `10_reconstruction/143_SILHOUETTE_DIFF_PROTOCOL.md`

# Silhouette Diff Protocol

## Pipeline

1. render binary/flat mask,
2. align with calibrated reference,
3. compute overlap,
4. extract contour delta,
5. map delta to feature/region.

## Metrics

### IoU
Dobra metryka ogólna, ale może ukrywać lokalny błąd.

### Maximum contour deviation
Wykrywa pojedyncze duże odchylenie.

### Mean contour deviation
Ogólna jakość obrysu.

### Regional contour deviation
Najważniejsze dla feature QA.

## Gate

D0 pass wymaga:
- akceptowalnego globalnego overlap,
- braku dużych lokalnych FAIL w critical regions.

## Anti-gaming

Nie uznawaj wysokiego IoU za sukces, jeśli np. profil oparcia jest wyraźnie błędny.


---

## FILE: `10_reconstruction/144_NUMERIC_AND_LANDMARK_VALIDATION.md`

# Numeric and Landmark Validation

## Numeric checks

- dimensions,
- angles,
- distances,
- offsets,
- radii where known,
- symmetry axes,
- ground contacts.

## Projected landmarks

Dla widoku:
- project 3D landmark,
- compare with reference coordinate,
- calculate error.

## Error normalization

Możesz raportować:
- pixels,
- normalized image fraction,
- millimeters after calibration.

## Priority weighting

MUST landmark ma wyższą wagę.

## Gate example

```text
hard_dimensions: PASS
critical_landmarks: PASS
secondary_landmarks: <= allowed MINOR
```

Nie wprowadzaj jednej magicznej średniej, która pozwala skompensować duży błąd jednym poprawnym punktem.


---

## FILE: `10_reconstruction/145_FEATURE_ROI_VALIDATION.md`

# Feature ROI Validation

## Cel

Sprawdzać feature lokalnie.

## ROI types

- rectangular,
- polygonal,
- contour-following,
- multi-region.

## Feature validation may include

- edge map,
- silhouette,
- color/material region,
- landmark positions,
- text/decal presence.

## Expected change mask

Przy naprawie feature:
- expected ROI = obszar dopuszczonej zmiany.

Zmiana poza ROI:
- regresja candidate.

## Occlusion

ROI może mieć widoczność:
- REQUIRED,
- OPTIONAL,
- OCCLUDED.

Nie failuj cechy, która zgodnie z widokiem jest zasłonięta.


---

## FILE: `10_reconstruction/146_MULTI_VIEW_CONSISTENCY_GATE.md`

# Multi-View Consistency Gate

## Problem

Model może pasować do frontu i nie pasować do side.

## Gate order

1. numeric bounds,
2. front,
3. side,
4. top,
5. rear,
6. bottom,
7. hero,
8. details.

Nie oznacza to różnego priorytetu — chodzi o diagnostyczną kolejność.

## Structural pass

D0/D1 są zaakceptowane tylko, jeśli nie istnieje `FAIL` w żadnym kanonicznym ortho view.

## Conflict diagnosis

Jeśli poprawka front pogarsza side:
- parametr jest źle zdekomponowany,
- camera/reference może być źle skalibrowana,
- model ma błędny przekrój.

Nie iteruj losowo między widokami.


---

## FILE: `10_reconstruction/147_RECONSTRUCTION_REGRESSION_GATES.md`

# Reconstruction Regression Gates

## Baseline

Po każdym zaakceptowanym etapie przechowaj:
- geometry manifest,
- renders,
- feature statuses,
- dimension report.

## Change classes

### LOCAL DETAIL
Test:
- target ROI,
- neighboring MUST.

### SHAPE
Test:
- all ortho silhouettes,
- dimensions,
- all D0/D1 MUST.

### TOPOLOGY
Test:
- shape + shading + UV if existing.

### MATERIAL
Test:
- material ROIs + no geometry change.

### EXPORT
Test:
- full runtime regression.

## Fail

Regresja MUST blokuje dalszy etap nawet jeśli naprawiany feature został poprawiony.


---

## FILE: `10_reconstruction/148_ACCEPTANCE_THRESHOLDS_AND_ERROR_BUDGETS.md`

# Acceptance Thresholds and Error Budgets

## Nie istnieje jeden globalny próg

Thresholdy są per:
- evidence type,
- feature priority,
- asset importance,
- view,
- stage.

## Error budget classes

### ZERO/NEAR-ZERO
- modular interfaces,
- explicit numeric dimensions,
- pivot/axis.

### TIGHT
- global silhouette,
- primary feature positions.

### MODERATE
- inferred radii,
- subtle surface transitions.

### VISUAL
- roughness,
- microtexture,
- lighting-sensitive appearance.

## Reporting

Zawsze podaj:
- measurement,
- threshold,
- status.

## Hard fail

Known dimension outside declared tolerance = FAIL.
Nie kompensuj punktami w scorecard.


---

## FILE: `10_reconstruction/149_RECONSTRUCTION_STATE_MACHINE.md`

# Reconstruction State Machine

## R0 — INGEST
Zapis źródeł i segmentów.

## R1 — CLASSIFY EVIDENCE
Projection, view, material/detail/text.

## R2 — AUTHORITY
Evidence + View Authority Matrix.

## R3 — REGISTER
Skala, osie, image planes, camera.

## R4 — CONSTRAIN
Dimension Graph, landmarks, Feature Contract.

## R5 — DECOMPOSE + SHAPE GRAPH

Obowiązkowe:
- decompose asset na G0–G5 design forms;
- zbuduj `Reconstruction Shape Graph`;
- przypisz parent/dependencies;
- sklasyfikuj shape representation każdego required node;
- przypisz RDL;
- przypisz authoritative views i controlled properties;
- zdefiniuj node validation contracts.

`SHAPE_GRAPH` musi przejść structural validation przed produkcyjnym modelowaniem.

Nie pisz monolitycznego build scriptu tworzącego G1–G5 w tym stanie.

## R6 — RDL0 ENVELOPE
Bounds + contact datum + minimal silhouette carrier.

Wymagany proof przed advance:
- numeric bounds;
- registered envelope evidence dla authoritative FRONT/SIDE/TOP;
- QA scene isolation;
- `RDL0_BARRIER: PASS`.

## R7 — RDL1 PRIMARY FORMS

Buduj **node po node**:

```text
ready G1 node
-> build only node
-> required canonical views
-> numeric/section checks
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | FAIL
```

Obejmuje:
- primary body/shell;
- base/plinth;
- major structural shoulder/transition;
- primary negative space.

Po wszystkich required nodes:
`RDL1_STAGE_BARRIER`.

Nie wolno budować RDL2 przy FAIL required G1 node.

## R8 — RDL2 SECONDARY STRUCTURAL FORMS

Buduj oddzielnie:
- frames;
- display housing/recess mass;
- utility housing;
- large service panels;
- major trims/inserts.

Każdy node ma własny required-view gate.

Po wszystkich required nodes:
`RDL2_STAGE_BARRIER`.

## R9 — RDL3 STRUCTURAL FEATURES

Panels, openings, recesses, vents, structural grooves, light channels, handles, layered assemblies.

Leaf skills mogą być używane dopiero, gdy host node jest `ACCEPTED`.

Wymagany proof odpowiedni do feature class:
- ROI;
- numeric depth/position;
- visibility/layer stack;
- panel-line/path contract;
- regression outside expected-change region.

Po required nodes:
`RDL3_STAGE_BARRIER`.

## R10 — RDL4 EDGE LANGUAGE

Bevel, fillet, chamfer, corner radius, tangency, SubD support geometry.

Rule:

```text
correct shape first
-> edge treatment second
```

RDL4 nie może kompensować błędu RDL1/RDL2.

Po edge treatment re-check:
- protected dimensions;
- canonical silhouette;
- local feature boundaries.

`RDL4_STAGE_BARRIER` przed surface detail.

## R11 — RDL5 SURFACE / DETAIL

Branding, decals, microgeometry, materials, texture direction, weathering, emissive finish.

Readable branding/text wymaga canonical orientation proof z project handedness gdy dotyczy.

Dla target fidelity L4/L5 wymagany material segmentation proof.

RDL5 może mieć jawne deferred items zależnie od requested completion level, ale nie może zmieniać accepted primary form bez dirty propagation.

## R12 — MULTIVIEW QA + RECONSTRUCTION FIDELITY GATE

Kolejność:

```text
Shape Graph revision validation
-> all required node gates accepted
-> RDL stage barriers pass
-> QA_SCENE_ISOLATE
-> registered canonical view validators
-> hard dimensions
-> primary landmarks/proportions
-> MUST feature evidence
-> material segmentation when required
-> authority/deviation closure
-> RECON_FIDELITY_GATE
```

`RECON_FIDELITY_GATE` musi zwrócić proof-bearing PASS z provenance.

Bare `PASS`, `looks correct`, `matching the card` albo poprawny overall envelope nie pozwalają wejść do runtime.

## R13 — TOPOLOGY / RUNTIME PREP

Dopiero tutaj:
- topology cleanup/freeze;
- UV;
- runtime LOD;
- collision;
- bake;
- runtime material closure.

Ten etap jest niedostępny przy wcześniejszym barrier/fidelity FAIL.

## R14 — EXPORT VALIDATION

Sprawdź:
- package readback;
- runtime primitive attributes;
- node transform policy;
- export round-trip dimensions/contact;
- target engine evidence dopiero dla Level D.

## Backtracking

Każdy FAIL wraca do najwcześniejszego właściciela problemu.

Przykłady:

```text
SIDE primary contour FAIL
-> current G1 node / RDL1

base FRONT okay + SIDE/TOP corner fail after corrected retry
-> SHAPE_CLASSIFY representation review
-> possible MULTI_SECTION_LOFT

DISPLAY_RECESS host FAIL
-> RDL2; do not continue to glass/content

PANEL_LINE FAIL because host surface wrong
-> parent G1/G2 owner, not HS_PANEL_LINE tweaking

mirrored rear technical decal
-> RDL5 branding orientation owner

missing TEXCOORD_0 after export
-> runtime package/UV owner
```

## Monolithic-build prohibition

Regresja v0.9:

```text
analyze
-> build body + base + screen + vents + logo + bevel + materials
-> one QA render
```

Canonical:

```text
understand hierarchy
-> build one form
-> prove it
-> commit node acceptance
-> continue coarse-to-fine
```


---

## FILE: `10_reconstruction/150_AMBIGUITY_STOP_AND_ESCALATION.md`

# Ambiguity Stop and Escalation

## Agent może kontynuować mimo części niewiadomych tylko, gdy nie wpływają one na bieżący etap.

## BLOCKING ambiguity

Przykłady:
- nie wiadomo, który widok jest frontem,
- sprzeczne total dimensions,
- nie wiadomo, czy asymetria jest zamierzona,
- nieznany interface dimension.

## NON-BLOCKING

- brak dokładnego micro-radius,
- niewidoczna śruba od spodu,
- drobny materiałowy noise.

## Escalation record

```text
ambiguity_id
affected_features
evidence
possible interpretations
impact
recommended resolution
```

## No silent choice

Agent nie może wybrać jednej z dwóch równie prawdopodobnych interpretacji i zapisać jej jako fact.


---

## FILE: `10_reconstruction/151_RECONSTRUCTION_CHANGE_CONTROL.md`

# Reconstruction Change Control

## Zmiana referencji

Nowy arkusz/revision może wpływać na:
- dimensions,
- feature presence,
- materials,
- branding.

## Impact analysis

1. find changed evidence,
2. find linked constraints,
3. find Feature IDs,
4. find scene owners,
5. find downstream UV/bake/runtime.

## Change set

Każda większa aktualizacja:
- reason,
- affected evidence,
- affected features,
- before/after,
- regression result.

## User-directed deviation

Jeśli użytkownik celowo chce odstąpić od referencji:
utwórz `AUTHORIZED_DEVIATION`.

Od tego momentu QA porównuje dany feature do deviation contract, nie starego obrazu.


---

## FILE: `10_reconstruction/152_RECONSTRUCTION_REPORT_SCHEMA.md`

# Reconstruction Report Schema

## Summary

- asset id,
- reference revision,
- Blender version,
- reconstruction library version,
- overall state.

## Evidence

- explicit dimensions,
- canonical views,
- conflicts,
- unresolved ambiguity.

## Feature status

Tabela:
| Feature | Priority | Evidence | Owner | QA | Status |

## Dimensions

Tabela:
| Parameter | Target | Actual | Error | Tolerance | Status |

## Views

- front,
- side,
- top,
- rear,
- bottom,
- hero.

Dla każdego:
- calibration state,
- silhouette status,
- feature failures.

## Runtime

- triangles,
- materials,
- UV,
- LOD,
- collision,
- export.

## Limitations

Jawna lista:
- inferred geometry,
- unresolved fonts,
- unknown hidden surfaces.


---

## FILE: `10_reconstruction/153_REFERENCE_TO_RUNTIME_BOUNDARY.md`

# Reference-to-Runtime Boundary

## Dwa modele sukcesu

### Reconstruction source
Maksymalna zgodność z evidence.

### Runtime asset
Zgodność z evidence w granicach kosztu silnika.

## Nie mieszaj etapów

Nie usuwaj feature z reconstruction source dlatego, że LOD go nie potrzebuje.

## Derived runtime variants

- LOD0,
- LOD1,
- LOD2,
- collision,
- proxy,
- mobile variant.

Wszystkie powinny mieć link do source reconstruction.

## Fidelity budget

Optymalizacja może usuwać detale w ustalonej kolejności, ale:
- primary silhouette,
- MUST functional features,
- locked dimensions

są chronione.


---

## FILE: `10_reconstruction/154_RECONSTRUCTION_PLAYBOOK_GENERATOR.md`

# Reconstruction Playbook Generator

## Cel

Przed modelowaniem agent tworzy playbook specyficzny dla klasy assetu.

## Inputs

- category,
- evidence,
- feature contract,
- runtime contract,
- material families,
- moving parts.

## Output

### Decomposition
Lista obiektów.

### Strategy
Technika per feature.

### Parameter set
Master + derived.

### Modifier stacks
Per object.

### QA views
Per feature.

### Risk list
Np.:
- boolean pinching,
- bevel changing bounds,
- perspective ambiguity,
- underside inconsistency.

### Freeze plan
Kiedy stack może zostać zastosowany.

## Reuse

Jeżeli istnieje playbook klasy, adaptuj go zamiast tworzyć workflow od zera.


---

## FILE: `10_reconstruction/155_RECONSTRUCTION_KNOWLEDGE_ROUTING.md`

# Reconstruction Knowledge Routing

Maksymalna biblioteka nie oznacza ładowania wszystkiego.

## Stage packs

### Ingest pack
103–109

### Geometry solve pack
110–123

### Surface pack
124–127

### Build pack
128–140

### QA pack
141–148

### Governance pack
149–159

## Asset-specific packs

Do tego:
- właściwy `11_playbooks`,
- engine profile,
- standard API modules.

## Token rule

Agent ładuje:
1. Reconstruction Index,
2. State Machine,
3. odpowiedni stage pack,
4. tylko playbook klasy.

Nie należy wrzucać całego `_FULL_LIBRARY.md` do każdego tool-call.


---

## FILE: `10_reconstruction/156_ADVERSARIAL_FAILURE_MODES.md`

# Adversarial Failure Modes

## F1 — Single-view overfit
Front idealny, side błędny.

## F2 — Hero-view distortion
Model zdeformowany pod atrakcyjny render.

## F3 — Detail distraction
Mikrodetale dodane przed poprawną sylwetką.

## F4 — Material compensation
Ciemniejszy shader ukrywa złą geometrię.

## F5 — Symmetry hallucination
Agent odbija detal, który powinien być tylko po jednej stronie.

## F6 — Hidden-side neglect
Tył/spód są puste mimo referencji.

## F7 — Invented greebles
Dodane "sci-fi" detale bez dowodu.

## F8 — Dimension drift
Bevel/solidify zmienia total dimensions.

## F9 — Camera cheating
Przesuwanie QA camera zamiast geometrii.

## F10 — Conflict averaging
Sprzeczne widoki uśrednione.

## F11 — Apply collapse
Wczesne Apply niszczy możliwość korekty.

## F12 — Optimization regression
LOD/decimate usuwa MUST.

## F13 — Text hallucination
Agent generuje błędne logo/napis.

## F14 — Lighting baked into material
Highlight z concept artu staje się albedo.

## F15 — API context thrash
Setki operatorów i zmian selection zamiast parametrycznego batchu.

Każdy benchmark powinien zawierać przynajmniej kilka z tych pułapek.


---

## FILE: `10_reconstruction/157_RECONSTRUCTION_COST_MODEL.md`

# Reconstruction Cost Model

## Koszt agentowy

Śledź:
- tool calls,
- failed calls,
- renders,
- full-scene rebuilds,
- tokens loaded,
- repair iterations.

## Koszt artystyczny

Najdroższe regresje:
1. zmiana D0 po D3,
2. zmiana topologii po UV/bake,
3. zmiana material segmentation po atlasie,
4. zmiana hierarchy po animation/export.

## Strategy

Najwięcej analizy wykonaj przed kosztownymi freeze points.

## Efficiency metric

`accepted_features / tool_calls`

oraz:
`MUST regressions / repair`

## Rule

Oszczędność tokenów nie może polegać na pomijaniu checkpointów.
Ma wynikać z:
- lepszego routingu wiedzy,
- batch operations,
- parametryzacji,
- lokalnych napraw.


---

## FILE: `10_reconstruction/158_RECONSTRUCTION_DATA_MODEL.md`

# Reconstruction Data Model

## Recommended entities

### Reference
source file.

### Segment
crop/view/material sample.

### Evidence
claim from segment.

### Constraint
numeric/geometric rule.

### Feature
visible or functional characteristic.

### Owner
scene object/data/modifier/material.

### Landmark
point/line/region used by QA.

### Checkpoint
accepted scene state.

### Deviation
authorized change from reference.

### ValidationResult
measurement/status.

## IDs

Prefer stable IDs:
- REF001
- SEG_FRONT
- E023
- C014
- F031
- LM009
- CP_D1

## Why

Stable IDs allow:
- machine-readable reports,
- targeted repair,
- regression tracking,
- future automation.


---

## FILE: `10_reconstruction/159_RECONSTRUCTION_DEFINITION_OF_DONE.md`

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


---

## FILE: `10_reconstruction/160_BLUEPRINT_AND_TECHNICAL_DRAWING_MODE.md`

# Blueprint and Technical Drawing Mode

## Gdy wejście jest rzeczywistym rysunkiem technicznym

Priorytet:
- dimensions,
- section lines,
- datums,
- tolerances,
- symbols.

## Source Authority Order

Dla plansz technicznych i technical concept sheets stosuj domyślnie:

```text
1. explicit numeric dimensions / explicit datum
2. orthographic FRONT / SIDE / TOP / BOTTOM / REAR views
3. real section/cross-section views
4. detail close-ups
5. perspective hero render
6. approximate textual ranges / marketing prose
7. visual inference
```

Wyższy authority wygrywa przy konflikcie.

Przykład:
- prompt mówi `Ø140 mm`;
- FRONT i SIDE są z tym zgodne;
- hero render wygląda na lekko zwężony przez perspektywę.

Wynik: `Ø140 mm` pozostaje `LOCKED`. Nie wykonuj kolejnych iteracji próbujących dopasować cylinder do perspektywicznego zwężenia hero renderu.

## Prompt vs drawing

Jeżeli prompt podaje dokładny wymiar, a sama plansza ma tylko zakres przybliżony, exact value ma wyższy authority.

Jeżeli prompt mówi `około 90–110 mm`, a ortograficzny widok i dimension line pozwalają wyprowadzić dokładniejszy wymiar, zapisz zakres jako constraint pomocniczy, nie jako blokadę dokładnej wartości.

Nigdy nie zamieniaj słowa `około` na `LOCKED` bez dodatkowego dowodu.

## Nie interpretuj linii pomocniczych jako geometrii

Rozróżnij:
- object edge,
- hidden line,
- centerline,
- dimension line,
- leader,
- hatch,
- page/layout separator.

Przy automatycznym pomiarze dimension line lub leader blisko sylwetki jest potencjalną kontaminacją maski, nie częścią obiektu.

## Datum system

Jeżeli drawing definiuje bazę:
użyj jej jako origin/alignment.

Jawny datum/origin ma pierwszeństwo przed wizualnym środkiem obiektu na hero renderze.

## Sections

Przekrój ma wyższy authority dla lokalnej grubości niż hero render.

## Orthographic consistency

Jeżeli FRONT i SIDE pokazują wspólny wymiar:
- zmierz je niezależnie;
- porównaj po kalibracji;
- zapisz aggregate deviation;
- nie przesyłaj do LLM pełnych profili wiersz po wierszu.

Jeżeli wynik mieści się w aktywnej tolerancji, oznacz `CONSISTENT` i zakończ ten test.

## Marketing blueprint / technical concept sheet

Jeżeli plansza tylko naśladuje dokumentację techniczną:
- nie zakładaj standardów ISO/ASME bez dowodu;
- traktuj jawne liczby i ortograficzne widoki jako silny dowód projektowy;
- traktuj marketingowe opisy funkcji jako semantykę, nie jako metrologię;
- nie zakładaj, że ozdobne linie, ikony lub layout są częścią assetu.

## Completion rule

Po ustaleniu:
- source authority,
- zwalidowanych ROI,
- locked dimensions,
- cross-view consistency,

zapisz je w `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md` i nie analizuj szeroko całej planszy ponownie bez konkretnego conflict/ROI failure.


---

## FILE: `10_reconstruction/161_PHOTO_RECONSTRUCTION_MODE.md`

# Photo Reconstruction Mode

## Zdjęcie różni się od concept sheet

Problemy:
- lens distortion,
- perspective,
- occlusion,
- unknown scale,
- material reflections.

## Scale anchors

Szukaj:
- znanego wymiaru,
- obiektu wzorcowego,
- powtarzalnego standardu.

## Camera solve

Wymagany przed geometry matching.

## Multi-photo

Preferuj zdjęcia z różnych osi.
Jedno zdjęcie nie definiuje pełnej 3D geometrii.

## Lens distortion

Jeśli jest istotny:
korekcja powinna poprzedzać precise overlay.

## Unknown regions

Nie inventuj tylnej strony z jednego frontowego zdjęcia.


---

## FILE: `10_reconstruction/162_STYLIZED_CONCEPT_MODE.md`

# Stylized Concept Reconstruction Mode

## Problem

Stylizowany concept może być celowo niespójny geometrycznie.

## Priority

1. approved hero silhouette,
2. functional requirements,
3. multi-view consistency, jeśli dostępna,
4. manufacturing plausibility.

## Intent extraction

Zidentyfikuj:
- shape language,
- proportions,
- focal features.

## Authorized resolution

Gdy dwa widoki są niemożliwe do pogodzenia:
utwórz spójny model 3D zgodny z ustalonym authority, a konflikt pozostaw w raporcie.

## Do not call exact

Jeżeli źródło samo nie definiuje jednoznacznej geometrii, wynik może być:
`CANONICAL_3D_INTERPRETATION`
zamiast literalnego "1:1".


---

## FILE: `10_reconstruction/163_MATERIAL_SAMPLE_CALIBRATION.md`

# Material Sample Calibration

## Material palette sample

Próbka na planszy może być renderem lub ilustracją.

## Extract

- dominant base color range,
- roughness appearance,
- directionality,
- microtexture scale.

## Do not sample one pixel

Użyj regionu, ponieważ:
- compression,
- highlights,
- vignette

zmieniają pojedyncze piksele.

## Brushed metal

Odtwórz:
- direction,
- roughness anisotropy if runtime supports,
- subtle normal/texture.

## Composite/powder coat

Microtexture powinna mieć fizyczną skalę względem obiektu.


---

## FILE: `10_reconstruction/164_EDGE_LANGUAGE_SYSTEM.md`

# Edge Language System

## Cel

Zachować spójny język produktu.

## Edge families

Dla całego assetu zidentyfikuj:
- outer protective corners,
- panel edges,
- metal trim edges,
- screen/insert edges,
- underside utilitarian edges.

## Record

| Family | Radius/Range | Segments authoring | Material | Feature IDs |

## Consistency

Jeśli dwa elementy należą do tej samej rodziny produkcyjnej:
ich edge treatment powinien być spójny, chyba że referencja pokazuje inaczej.

## Reconstruction value

Edge language silnie wpływa na "ten sam projekt" nawet przy poprawnych global dimensions.


---

## FILE: `10_reconstruction/165_SURFACE_CONTINUITY_AND_TANGENCY.md`

# Surface Continuity and Tangency

## Continuity classes

- G0: position continuous,
- G1: tangent continuous,
- visually soft transition.

Agent nie musi używać formalnego CAD, ale musi rozpoznawać różnicę.

## Typical areas

- backrest into side housing,
- rounded shell corner,
- trim wrapping corner.

## Failure

Dwie powierzchnie mogą się stykać, ale tworzyć niezamierzony kink.

## QA

- silhouette,
- grazing light,
- matcap,
- curvature-like visual inspection.

## Rule

Nie dodawaj Smooth modifiera jako maskowania złej kontroli profilu.


---

## FILE: `10_reconstruction/166_PART_BOUNDARY_AND_ASSEMBLY_LOGIC.md`

# Part Boundary and Assembly Logic

## Cel

Zrekonstruować, które linie oznaczają:
- osobne części,
- dekoracyjne rowki,
- materiałowy insert,
- cień.

## Evidence

- seam continuation,
- different material,
- fasteners,
- thickness,
- close-up,
- rear/bottom continuation.

## Assembly graph

Zapisz:
- parent part,
- attached part,
- interface,
- likely attachment.

Nie musi odpowiadać rzeczywistemu procesowi produkcji 1:1, jeśli brak danych; ma być spójny z widoczną konstrukcją.

## Benefit

Pomaga:
- decomposition,
- UV,
- material boundaries,
- variants,
- repair.


---

## FILE: `10_reconstruction/167_FUNCTIONAL_GEOMETRY_INFERENCE.md`

# Functional Geometry Inference

## Funkcja może ograniczać geometrię

Przykłady:
- siedzisko wymaga użytkowej powierzchni,
- port USB wymaga obudowy,
- panel serwisowy musi mieć sensowny dostęp,
- uchwyt musi mieć clearance.

## Evidence status

Funkcja nie daje prawa do dowolnego detail invention.

Używaj jej do:
- odrzucenia niemożliwych interpretacji,
- minimalnego domknięcia niewidocznej konstrukcji.

## Functional vs decorative

Oddziel:
- geometry required for use,
- visual styling.

## Human scale

Jeśli asset jest meblem:
sprawdź, czy jawne wymiary są spójne z przeznaczeniem, ale nie zmieniaj ich na podstawie ergonomicznych heurystyk, jeśli reference ma explicit numeric values.


---

## FILE: `10_reconstruction/168_REFERENCE_CLEANUP_AND_PREPROCESSING.md`

# Reference Cleanup and Preprocessing

## Dopuszczalne operacje

- crop,
- rotate,
- deskew,
- normalize transparency/background for QA,
- extract edges/mask,
- split panels.

## Niedopuszczalne jako źródło prawdy

- generative fill,
- AI upscaling inventing edges,
- stylization,
- sharpening tworzący fałszywe linie.

## Upscale

Jeśli używany:
traktuj jako pomoc wizualną, a measurements wykonuj na oryginale lub kontrolowanym resamplingu.

## Preserve

Zawsze zachowaj:
- original pixels,
- transform metadata.


---

## FILE: `10_reconstruction/169_REFERENCE_RECONSTRUCTION_SECURITY_RULES.md`

# Reconstruction Safety Rules for Scene Integrity

## Nie dotyczy bezpieczeństwa fizycznego — dotyczy integralności danych.

## Rules

- nie usuwaj source references,
- nie modyfikuj zaakceptowanych QA cameras bez logu,
- nie nadpisuj master parameters z lokalnej naprawy,
- nie apply'uj destructive operations bez checkpointu,
- nie usuwaj helpers oznaczonych przez inne feature IDs,
- nie zmieniaj units w połowie assetu.

## Recovery assets

Przechowuj:
- last accepted blockout,
- last accepted D2,
- pre-UV source,
- pre-export source.

## Scene contamination

Testowe obiekty i cuttery:
- w osobnej kolekcji,
- tagowane,
- usuwane jawnie.


---

## FILE: `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md`

# Reference Analysis Cache

## Purpose

Reference analysis is expensive. Once a view, ROI, dimension anchor or authority decision has been validated, the agent must persist it and reuse it instead of repeatedly rediscovering the same information.

This cache is an asset-scoped analytical state, not a conversational summary.

## Core rule

```text
analyze once
-> validate
-> cache
-> reuse
```

Do not re-run broad image analysis unless the cached fact has been invalidated.

## Cache schema

```yaml
reference_analysis_cache:
  asset_id: SM_EXAMPLE
  source:
    file: concept_art.png
    width_px: 1122
    height_px: 1402
    fingerprint: OPTIONAL_HASH_OR_MTIME

  views:
    FRONT:
      roi: [735, 165, 860, 640]
      projection: ORTHOGRAPHIC
      authority: HIGH
      validated: true
      crop_artifact: c_front_ortho.png
    SIDE:
      roi: [930, 165, 1030, 640]
      projection: ORTHOGRAPHIC
      authority: HIGH
      validated: true

  dimension_anchors:
    overall_height_mm:
      value: 1050
      source: EXPLICIT_DIMENSION
      confidence: LOCKED

  measurements: {}
  feature_rois: {}
  exclusions: {}
  conflicts: []
  unresolved: []
```

## What must be cached

Persist when validated:
- original source metadata;
- segmented view ROI coordinates;
- view classification;
- View Authority Matrix decisions;
- explicit dimensions and datum/origin information;
- pixel-to-world calibration anchors;
- feature-specific ROI;
- annotation exclusion masks/regions where needed;
- cross-view consistency results;
- unresolved conflicts;
- crop artifact paths if crops are generated.

## What must NOT be cached as truth

Do not promote to cache truth:
- temporary threshold guesses;
- failed measurement candidates;
- speculative hidden geometry;
- unvalidated perspective-derived dimensions;
- visual impressions such as "looks about right".

These may be logged as diagnostics but must not become authoritative measurements.

## Cache reuse

Before any reference-analysis call:

```text
1. check source identity
2. check requested view/feature
3. check cached validity
4. reuse valid facts
5. analyze only missing or invalid fields
```

If FRONT, SIDE, TOP and their calibration are already valid, a later seam investigation must request only the seam ROI, not segment and measure the entire sheet again.

## Invalidation

Invalidate only affected records when:
- the source image changes;
- a crop was found incorrect;
- a higher-authority source supersedes a measurement;
- a dimension conflict is resolved differently;
- an explicit user correction changes interpretation;
- the source fingerprint no longer matches.

Do not invalidate unrelated views or measurements.

## Scope

Cache scope is normally one asset/reference set.

A cache from another product may provide project conventions but must never supply geometry measurements for the current asset.

## Analysis completion snapshot

At the end of ANALYZE write a compact immutable snapshot:

```yaml
analysis_snapshot:
  status: PASS
  source_revision: ...
  locked_dimensions: {}
  view_authority: {}
  accepted_measurements: {}
  feature_rois: {}
  unresolved: []
```

Later states consume this snapshot.

## Re-entry rule

After `ANALYZE: PASS`, broad exploratory analysis is prohibited.

Return to reference analysis only through one of:
- `FEATURE_ROI_FAILURE(feature_id)`;
- `DIMENSION_CONFLICT(metric_id)`;
- `VIEW_CONFLICT(view_id)`;
- `USER_SOURCE_UPDATE`;
- `CACHE_INVALIDATED(record_id)`.

The re-entry request must identify the affected record/ROI.

## Token-efficiency requirement

The cache must contain compact structured values. It must not embed:
- full image pixels;
- per-row profiles;
- giant tool logs;
- duplicate crop images encoded as text;
- full source documents.

## Relationship to other modules

- `103_REFERENCE_INGESTION_PROTOCOL.md` creates the initial source/view entries.
- `104_CONCEPT_SHEET_SEGMENTATION.md` provides segmented ROIs.
- `106_VIEW_AUTHORITY_MATRIX.md` provides authority.
- `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md` writes compact measurements.
- `110_DIMENSION_GRAPH.md` consumes accepted dimensional relations.
- `145_FEATURE_ROI_VALIDATION.md` may request narrow re-analysis.


---

## FILE: `11_playbooks/110_HARD_SURFACE_CIVIC_FURNITURE.md`

# Playbook — Civic Hard-Surface Assets

## Scope

Reusable playbook for maintained urban/civic props:
- benches and seating;
- bollards/posts;
- waste/recycling units;
- kiosks/terminals;
- wayfinding pylons;
- lighting/support fixtures;
- small infrastructure enclosures.

The first decision is not "which modifier?". It is **which structural family describes the asset**.

---

# Structural subtype routing

## A. `AXISYMMETRIC_CIVIC_PROP`

Typical:
- bollard;
- round post;
- cylindrical beacon;
- stacked circular housing;
- lamp/pedestal with rotational body.

Prefer:
- `03_modeling/45_AXISYMMETRIC_PROFILE_ASSET_PRIMITIVE.md`;
- explicit radius/Z profile;
- radial repetition for anchors/fasteners;
- separate asymmetric feature owners for panels/logo/local emitters.

Do not write a new one-off `lathe()` implementation if the reusable executor covers the geometry.

## B. `BOX_PROFILE_CIVIC_PROP`

Typical:
- recycling unit;
- kiosk;
- rectangular terminal;
- modular cabinet.

Prefer:
- dimension-locked box/profile blockout;
- bevel/boolean/panel-line semantic skills;
- modular repeated subassemblies.

## C. `FRAME_PANEL_CIVIC_PROP`

Typical:
- bench;
- shelter component;
- barrier/rail module;
- pylon with structural frame and skins.

Prefer:
- structural frame first;
- separate panels/skins;
- repeated supports/fasteners;
- explicit junction logic.

A single asset may combine families. Route by feature owner, not by one global technique.

---

# Primary production order

```text
reference authority
-> dimensions/bounds
-> primary structural family
-> blockout
-> silhouette gate
-> primary manufacturing transitions
-> service/access logic
-> secondary detail
-> material segmentation
-> material breakup/lookdev
-> UV/bake/runtime materials
-> LOD/collision
-> export/integration
```

Do not start wear, screws or microdetail before primary silhouette passes.

---

# Typical components

- structural shell/frame/body;
- seat/backrest where applicable;
- base/mounting flange;
- feet/anchors;
- service collar/panel;
- trim;
- utility/electronics;
- signage/branding;
- integrated light/accent;
- underside/ground interface.

Every characteristic component should map to a Feature ID.

---

# Manufacturing logic

Civic assets should read as manufactured and serviceable.

Ask:
- what is one manufactured part versus an assembly?
- which component is removable?
- where are seams justified?
- which fasteners are structural versus decorative?
- what protects an emitter/display?
- how is the asset anchored?
- which surfaces are exposed to handling/weather?

Do not scatter arbitrary panel lines merely to make the asset look "sci-fi".

---

# Fasteners and repeated details

Repeated bolts/anchors should use a reusable radial/linear repetition strategy where possible.

For circular flanges, validate **annulus containment**:

```text
inner_available_radius <= fastener_min_radius
fastener_max_radius <= outer_available_radius
```

Do not accept fasteners that numerically intersect the bevel/lip even if the hero view hides the error.

At lower LODs:
- reduce fastener segments;
- remove individual fasteners when sub-pixel and permitted;
- move shallow detail into normal/texture representation.

---

# Floating/local details

Use `03_modeling/41_DECALS_AND_FLOATING_DETAILS.md`.

Critical civic-prop rule:
- a floating plate can represent an additive panel/graphic;
- it cannot cut a true recess into the host;
- a local emitter hidden behind a base wall fails even if its emissive material is correct.

Require visibility proof for `SURFACE_DETAIL` features.

---

# Materials

Typical families:
- dark composite/powder coat;
- brushed aluminium/metal trim;
- rubberized impact material;
- polycarbonate/light diffuser;
- emissive accent;
- decals/etched graphics.

Use `11_playbooks/114_BRUSHED_METAL_AND_DARK_COMPOSITE.md` for surface breakup.

Civic material target:

```text
maintained + durable + subtly used
```

Avoid both:
- sterile perfectly uniform CG surfaces;
- exaggerated abandoned/grunge treatment.

---

# Integrated lighting

Use `11_playbooks/115_INTEGRATED_LIGHT_STRIP.md` and `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md`.

Asset authoring owns emitter geometry/mask/color.
Final neon/bloom response may belong to runtime post-processing.

Do not bake bloom into BaseColor by default.

---

# Branding

If authoritative corporate artwork exists:
- use the provided source;
- preserve mark proportions;
- adapt layout only where the product reference explicitly shows a different lockup;
- do not approximate a supplied logo with ad-hoc geometry/font substitutes.

Prefer decal/atlas representation when geometry would waste triangle budget or misrepresent printed/etched branding.

---

# Game-ready finishing

Before calling the asset game-ready:
- LOD budgets pass;
- collision contract passes;
- UV/material strategy complete;
- procedural lookdev has a runtime disposition;
- required bakes pass `04_game_ready/50_GAME_READY_BAKE_GATE.md`;
- emissive export survives;
- branding/decal textures survive export;
- pivot/scale/naming pass;
- post-export validation passes.

Use completion levels from `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md`.

---

# QA views

Minimum for most static civic assets:
- front;
- side;
- top;
- rear when different;
- bottom when reference/runtime requires it;
- 3/4;
- close-up for mounting/service/light details.

The close-up is not decorative. It is where annulus overflow, z-fighting, hidden emitters and service-panel depth problems often become visible.

---

# Efficiency

Before generating custom infrastructure, check reusable skills/executors:
- axisymmetric profile;
- mesh validator;
- panel line;
- SubD topology control;
- reference measurement;
- QA isolation/runtime compatibility helpers.

Generated build/QA scripts are persistent code artifacts. Do not echo their complete source back into model context after creation.

---

# Completion

A clean Blender render can satisfy reconstruction/modeling and still fail game-ready completion.

Explicitly report:

```text
RECONSTRUCTION_COMPLETE
MODELING_COMPLETE
GAME_READY_COMPLETE
PIPELINE_INTEGRATED
```

Never merge these into one ambiguous `DONE` state.


---

## FILE: `11_playbooks/111_BENCH_AND_SEATING_MODULE.md`

# Playbook — Bench / Seating Module

## Master parameters

- total_width,
- total_depth,
- total_height,
- seat_height,
- seat_depth,
- backrest_angle,
- side_housing_width,
- backrest_thickness,
- base/foot dimensions.

## Functional landmarks

- ground contacts,
- seat front edge,
- seat/back junction,
- top backrest,
- inside edges of side housings.

## Decomposition

Preferowane:
- core seat,
- backrest,
- left/right housings,
- trims,
- utility modules,
- lighting,
- underside/service.

## Side profile is critical

Side view rozstrzyga:
- seat depth,
- backrest angle,
- side housing contour.

## Negative space

Przestrzeń pod siedziskiem jest feature D0/D1.
Nie traktuj jej jako wynik przypadkowy.

## Collision

Najczęściej prosta collision decomposition wystarcza:
- seat,
- side housings,
- backrest proxy,
zgodnie z wymaganiami silnika.


---

## FILE: `11_playbooks/112_TECHNICAL_CONCEPT_SHEET_RECONSTRUCTION.md`

# Playbook — Technical Concept Sheet Reconstruction

## Wejście

Plansza zawiera:
- hero,
- rzuty,
- dimensions,
- detail,
- material palette.

## Workflow

1. segment sheet,
2. classify views,
3. read explicit dimensions,
4. calibrate ortho crops,
5. build dimension graph,
6. define feature contract,
7. solve blockout from orthos,
8. solve hero camera,
9. add D2,
10. surface/material,
11. validate every view.

## Authority

Numeric + orthographic > hero dla geometrii.
Hero/detail > orthographic dla surface appearance.

## Common risk

Plansza może mieć estetyczne niespójności.
Nigdy nie zakładaj automatycznie CAD-level consistency.


---

## FILE: `11_playbooks/113_REAR_AND_UNDERSIDE_PLAYBOOK.md`

# Playbook — Rear and Underside

## Cel

Eliminować "front-only asset syndrome".

## Rear

- large panel structure,
- side wrapping,
- logo/decal,
- service seams,
- fasteners.

## Underside

- base volumes,
- panels,
- support rails,
- feet,
- lighting strips,
- utility housings.

## Modeling rule

Jeżeli bottom view istnieje:
najpierw odwzoruj układ D1/D2, dopiero potem optymalizuj.

## Runtime rule

Authoring source może być pełniejszy niż runtime underside.
Nie mieszaj tych wersji.


---

## FILE: `11_playbooks/114_BRUSHED_METAL_AND_DARK_COMPOSITE.md`

# Playbook — Brushed Metal + Dark Composite

## Purpose

Create convincing maintained civic hard-surface materials that are neither sterile nor covered in generic grunge.

The material must preserve the reference's **material identity** before adding variation.

```text
material identity
-> manufacturing response
-> scale-aware breakup
-> exposure/use logic
-> restrained wear
```

Random noise is not a material model.

---

# Brushed metal

Control:
- metallic response;
- roughness range;
- brushing direction;
- fine normal/roughness variation;
- edge highlight behavior;
- large-scale cleanliness variation.

Do not paint a fixed highlight into BaseColor.
The directional highlight must follow lighting and surface orientation.

## Brushing direction

The direction should follow manufacturing logic:
- cylindrical sleeve: typically circumferential or axial depending on evidence;
- flat trim: typically one stable planar direction;
- machined ring: may use circumferential direction.

Reference wins.

If direction is unknown, keep it subtle rather than inventing a dominant pattern.

---

# Dark composite / powder coat / rubberized civic body

First classify the material:
- dielectric composite;
- coated metal;
- rubberized impact material;
- dark titanium/metal-like composite;
- project-specific hybrid.

Do not set metallic merely because the reference has a bright highlight.

Control:
- low base-color variation;
- broad roughness variation;
- subtle micro-normal breakup;
- controlled edge response;
- protected-joint dirt;
- sparse handling/service wear.

A dark body should not become medium grey solely because the QA rig is overpowered.
Fix exposure/lighting before changing the base material family.

---

# Three-scale breakup model

Avoid one Noise Texture driving every channel.
Use different spatial scales with different responsibilities.

### Macro — ~0.1–1 m scale
Purpose:
- broad manufacturing/cleaning variation;
- subtle exposure differences;
- very low-amplitude roughness drift.

Must not look like clouds painted on the asset.

### Meso — ~5–80 mm scale
Purpose:
- wipe/maintenance variation;
- localized roughness changes;
- protected-area dirt;
- faint streaking aligned with gravity/use where appropriate.

### Micro — sub-mm to few-mm scale
Purpose:
- powder-coat grain;
- brushed microstructure;
- molded/rubberized texture;
- tiny normal/roughness breakup.

Micro detail should not alter primary silhouette.

---

# Channel separation

Do not use one noise value identically for BaseColor, Roughness and Normal.

Preferred:

```text
BaseColor  -> very low amplitude, low frequency
Roughness  -> primary variation channel
Normal     -> high-frequency material structure
AO/dirt    -> geometry/exposure-driven mask
Wear       -> sparse edge/contact/service mask
```

This reduces the "procedural plastic" look.

---

# Wear logic

Civic infrastructure can be clean and maintained while still showing subtle history.

Possible wear zones:
- service collar contact boundary;
- removable panel perimeter;
- anchor/base plate around maintenance access;
- exposed outer base edge;
- top trim touched during servicing;
- drainage/ground-facing interface.

Avoid:
- uniform edge damage everywhere;
- white scratches on every convex edge;
- random dirt equally distributed over top and protected underside;
- heavy apocalypse-style grunge unless reference/brief asks for it.

Target:

```text
maintained
used
materially varied
not pristine-CGI
not abandoned
```

---

# Dirt accumulation

Dirt should be driven by plausible collection areas:
- concave seams;
- protected horizontal ledges;
- base/ground transition;
- underside of projecting lips;
- service interfaces.

Do not fake deep geometric seams using dark albedo bands if the reference requires real parallax.

---

# Brushed aluminium specifics

For a bright aluminium collar:
- keep BaseColor physically plausible/neutral rather than pure white;
- use metallic response to generate highlights;
- preserve brushed direction;
- roughness breakup should remain subtle enough that it still reads as precision trim;
- edge radius controls highlight width and is a geometry concern, not a texture substitute.

---

# Dark-surface QA

Validate material under at least:
- neutral studio lighting;
- grazing/highlight angle;
- low-contrast view;
- material-only close-up.

Questions:
- does the surface become featureless black?
- does it become generic mid-grey?
- can roughness variation be perceived without obvious procedural blobs?
- does microtexture remain below silhouette scale?
- is the material still recognizable after mip/distance reduction?

---

# Reference fidelity

Material variation must not override evidence.

If the concept art looks slightly irregular, infer only the **type and scale** of variation that is supported.
Do not reproduce lighting noise or compression artifacts as texture.

Use `10_reconstruction/125_LIGHTING_VS_MATERIAL_DISENTANGLEMENT.md` before promoting image brightness variation into material data.

---

# Runtime/bake handoff

For every procedural component choose:
- BAKE;
- RECREATE_IN_ENGINE;
- EXPORT_NATIVELY_VERIFIED;
- REMOVE_BY_DESIGN.

Use `04_game_ready/50_GAME_READY_BAKE_GATE.md`.

Typical game-ready outputs for this material family may include:
- BaseColor with restrained low-frequency variation;
- Normal with microstructure and approved small details;
- ORM with roughness breakup and AO where appropriate;
- Emissive separately for lighting features.

Do not call the material game-ready while its defining variation exists only in Blender procedural nodes and no runtime replacement is verified.

---

# Acceptance target

A successful material should read correctly at three distances:

```text
far      -> correct color/material family and silhouette
medium   -> material separation + broad roughness behavior
close    -> microstructure + subtle wear/maintenance evidence
```

If close-up quality comes from noise that disappears into an obviously sterile medium-distance surface, the breakup hierarchy is incomplete.


---

## FILE: `11_playbooks/115_INTEGRATED_LIGHT_STRIP.md`

# Playbook — Integrated Light Strip

## Purpose

Build reference-faithful guidance/accent light features while separating physical asset authoring from engine glow/post-processing.

Use with `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md`.

---

# Geometry

Define explicitly:
- recess/host opening if one exists;
- diffuser/cover;
- emitting surface or emissive material region;
- protective lips;
- ends/corners;
- depth relationship to host surface.

The strip may be:
- flush;
- recessed;
- slightly proud;
- protected by a surrounding lip.

Reference evidence decides.

A floating emissive patch cannot create a recess in an opaque host mesh.
If negative depth matters, model/cut/bake the recess according to feature scale and runtime needs.

---

# Visibility contract

The feature must be visible because its geometry/material relationship is correct, not because the agent made emission arbitrarily huge.

Validate:
- emitter is not behind the host wall;
- diffuser faces the expected view region;
- band thickness is consistent;
- no z-fighting;
- the intended 360°/partial-arc continuity is correct;
- emitted color survives QA tone mapping.

For a 360° guidance ring, inspect at least front + side + 3/4.

---

# Material

Record separately:

```yaml
light_feature:
  feature_id: F_LIGHT_01
  geometry: PASS
  diffuser: PASS
  emissive_color: [r, g, b]
  blender_preview_strength: 2.4
  runtime_strength: UNVERIFIED
  runtime_bloom: UNVERIFIED
```

Blender emission intensity is a lookdev parameter unless the target engine defines a calibrated transfer.

Do not burn the emitter to white if the reference requires a saturated blue/cyan line.

---

# Authoring vs runtime

Asset authoring owns:
- geometry;
- emissive mask/material assignment;
- color intent;
- UV/texture data;
- exported material binding.

Runtime owns or may modify:
- bloom;
- exposure;
- tone mapping;
- HDR response;
- actual scene-light contribution;
- distance-dependent post-process.

Therefore a Blender render proving a blue strip exists does not prove the in-game neon look is finished.

---

# Bloom

Do not paint a large glow halo into BaseColor.
Normally the texture describes the emitter and the engine generates bloom.

If a stylized reference explicitly contains a painted halo that must remain independent of post-process, treat that as separate art direction evidence.

---

# QA

Use two QA modes:

### `EMISSIVE_AUTHORING`
- neutral exposure;
- bloom disabled or minimized;
- prove geometry/mask/color;
- detect clipping and occlusion.

### `EMISSIVE_LOOKDEV`
- representative exposure/post-process;
- judge perceived glow only after authoring pass.

Do not modify geometry to compensate for a failed `EMISSIVE_LOOKDEV` lighting setup unless geometry evidence also fails.

---

# LOD

The emitter's visual signal may survive farther than its housing detail.

LOD policy:
- preserve visible color signal while it matters on screen;
- simplify/remove diffuser recess geometry when sub-pixel;
- keep ring/marker aligned with the simplified silhouette;
- avoid tiny flickering floating surfaces.

A low LOD may represent the strip as a simpler emissive band even if LOD0 has a separate diffuser assembly.

---

# Export/runtime gate

Before `GAME_READY_COMPLETE`:
- emissive data survives export;
- the exported material/texture actually references the emissive mask/color;
- no dependency on Blender-only procedural nodes remains undefined;
- runtime interpretation is verified by Engine Profile or marked `UNVERIFIED`.

If the engine's bloom/post-process is not part of the Blender agent's capability, do not block asset authoring — but report that final runtime glow still requires engine validation.


---

## FILE: `11_playbooks/116_UTILITY_PANEL_AND_PORTS.md`

# Playbook — Utility Panel and Ports

## Decomposition

- panel recess,
- bezel,
- insert,
- ports,
- indicator,
- labels/icons.

## Geometry priority

Najpierw poprawny outline i placement panelu.
Dopiero potem port microdetail.

## Reuse

Jeśli utility panel pojawia się na wielu assetach:
zrób osobny reusable subasset.

## Runtime

Małe porty:
- mogą być geometryczne w LOD0,
- mogą przejść do normal/decal w dalszych LOD.


---

## FILE: `11_playbooks/117_PRODUCT_BRANDING_PLAYBOOK.md`

# Playbook — Product Branding

## Brand asset

Preferuj dostarczony wektor/raster logo zamiast odtwarzania tekstu fontem.

## Anchor system

Dla logo zapisz:
- view,
- center/anchor,
- normalized width,
- rotation,
- material/decal plane.

## Consistency

Ten sam brand w różnych assetach powinien używać:
- wspólnego źródła grafiki,
- wspólnej polityki koloru,
- wariantów zatwierdzonych przez projekt.

## Never hallucinate

Nie generuj alternatywnej pisowni ani symbolu.


---

## FILE: `99_sources/SOURCES.md`

# Technical Sources

Biblioteka jest oparta przede wszystkim na oficjalnej dokumentacji.

## Blender 5.1

- Blender 5.1 Release Notes  
  https://developer.blender.org/docs/release_notes/5.1/

- Blender 5.1 Python API release notes  
  https://developer.blender.org/docs/release_notes/5.1/python_api/

- Blender Python API 5.1  
  https://docs.blender.org/api/5.1/

- Blender Python API — Context  
  https://docs.blender.org/api/5.1/bpy.types.Context.html

- Blender Python API — Operators  
  https://docs.blender.org/api/5.1/bpy.ops.html

- Blender Python API — BMesh  
  https://docs.blender.org/api/5.1/bmesh.html

- Blender Python API — BMesh Operators  
  https://docs.blender.org/api/5.1/bmesh.ops.html

- Blender Manual 5.1  
  https://docs.blender.org/manual/en/5.1/

## glTF

- Khronos glTF 2.0 Specification  
  https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html

- Khronos glTF overview  
  https://www.khronos.org/gltf/

- Khronos glTF PBR  
  https://www.khronos.org/gltf/pbr/

## Update policy

Przy zmianie Blender 5.1 -> 5.2+:
1. porównaj Python API release notes,
2. znajdź breaking/compatibility changes,
3. uruchom testy snippetów,
4. dopiero podnieś `target_blender_version` biblioteki.


## Blender 5.1 — production techniques

- Geometry Nodes introduction
  https://docs.blender.org/manual/en/5.1/modeling/geometry_nodes/introduction.html

- Geometry Nodes — Instances
  https://docs.blender.org/manual/en/5.1/modeling/geometry_nodes/instances.html

- Geometry Nodes — Realize Instances
  https://docs.blender.org/manual/en/5.1/modeling/geometry_nodes/instances/realize_instances.html

- Blender Camera API
  https://docs.blender.org/api/5.1/bpy.types.Camera.html

- Cycles Baking
  https://docs.blender.org/manual/en/5.1/render/cycles/baking.html

## Source discipline

Moduły biblioteki rozdzielają:
- zachowanie udokumentowane przez Blender/Khronos,
- politykę pipeline projektu,
- heurystyki produkcyjne.

Heurystyki nie powinny być przedstawiane agentowi jako ograniczenia API.

## Reconstruction / precision modeling sources

Official Blender documentation relevant to the reconstruction layer:

- Blender Manual — Empties / image references
  https://docs.blender.org/manual/en/latest/modeling/empties.html

- Blender Manual — Precision transforms
  https://docs.blender.org/manual/en/latest/scene_layout/object/editing/transform/control/precision.html

- Blender Manual — Snapping
  https://docs.blender.org/manual/en/latest/editors/3dview/controls/snapping.html

- Blender Manual — Measure tool
  https://docs.blender.org/manual/en/latest/editors/3dview/toolbar/measure.html

- Blender Manual — Mesh Analysis
  https://docs.blender.org/manual/en/latest/modeling/meshes/mesh_analysis.html

- Blender Manual — Bevel Modifier
  https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html

- Blender Manual — Boolean Modifier
  https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html

- Blender Python API — Object
  https://docs.blender.org/api/current/bpy.types.Object.html

- Blender Python API — Camera
  https://docs.blender.org/api/current/bpy.types.Camera.html

- Blender Python API — Depsgraph
  https://docs.blender.org/api/current/bpy.types.Depsgraph.html

## Source version note

Biblioteka pozostaje targetowana na Blender 5.1.x.
Adresy `latest/current` w sekcji źródeł służą jako dokumentacja referencyjna do mechanizmów,
ale przed automatycznym użyciem konkretnego API agent powinien weryfikować zgodność z wersją 5.1.x.


---

## FILE: `CHANGELOG.md`

# Changelog

## Unreleased

No canonical changes after the v0.7.0 release baseline yet.

## 0.7.0

v0.7.0 is the **runtime-proof integrity + project infrastructure reuse** release. It is based on the final Lafar Civic Bollard continuation after v0.6 bake closure.

The user reported approximately **45k additional tokens** for this final segment. Combined with the previous ~36k-token continuation, the post-v0.5 completion work consumed roughly **81k tokens**. The asset ultimately reached `PIPELINE_INTEGRATED`, but the run exposed silent cache, path, round-trip and test-oracle failures that should never be rediscovered on the next asset.

### Blender image cache coherence
- added `02_blender_api/30_IMAGE_DATABLOCK_CACHE_COHERENCE.md`;
- external file freshness is explicitly separated from `bpy.data.images` freshness;
- correct PNG + stale Blender image datablock is classified as `STALE_IMAGE_DATABLOCK`;
- disk-authoritative textures are reloaded/synchronized before runtime-material QA;
- stale runtime binding normally dirties binding/QA only, not the accepted baked texture;
- added `executors/image_cache_coherence.py`.

### Executable incremental pipeline
- added `05_execution/68_PIPELINE_DAG_EXECUTOR_AND_STAGE_REUSE.md`;
- Dirty-Stage Cache is now enforced through explicit dependency closure rather than treated as advisory prose;
- a local repair must emit execute/reuse plan before replaying build/bake/export stages;
- geometry, decal, individual bake channels, runtime material, package, round-trip, catalog and engine test can be invalidated independently;
- added pure-Python `executors/pipeline_dag.py` candidate;
- full pipeline replay after a local repair is now a benchmark regression unless the DAG proves every stage dirty.

### Post-export invariant validation
- added `05_execution/67_POST_EXPORT_INVARIANT_AND_ROUNDTRIP_VALIDATION.md`;
- final exported/re-imported artifact must re-pass protected hard dimensions, contact datum and other declared invariants;
- source geometry PASS no longer implies exported artifact PASS;
- Blender round-trip evidence is explicitly Level C evidence, not Level D engine proof;
- added `executors/export_roundtrip_validate.py` candidate.

### Runtime root/path contract
- added `09_engine/95_RUNTIME_ASSET_ROOT_AND_PATH_CONTRACT.md`;
- filesystem existence is separated from engine visibility;
- canonical path authority is profile > build/engine definition > production loader > engine test > sibling exporter > heuristic;
- per-script root guessing is forbidden when one Runtime Path Context can be injected;
- wrong sibling output trees are handled as packaging/path dirtiness rather than texture rebake;
- added `executors/runtime_path_resolver.py`.

### Verified RPG project profile
- added `09_engine/profiles/RPG_PROJECT_ASSET_PIPELINE_PROFILE.md` from the real Bollard integration evidence;
- verified engine asset directory: `<repo>/Assets`;
- verified runtime game-asset root: `<repo>/Assets/GameAssets`;
- `<repo>/GameAssets` recorded as a forbidden lookalike root for this project configuration;
- persisted one-file multi-node LOD packaging, `_LODn` convention, current X-mirror compensation, catalog source, production loader, CMake debug build directory and `ModelTests` target/binary;
- future matching assets should not rediscover these facts through repeated shell probing.

### Engine integration proof
- added `09_engine/96_ENGINE_INTEGRATION_SMOKE_TEST_CONTRACT.md`;
- target-engine production loader/test/instantiation is required for Level D;
- Blender glTF re-import remains Level C round-trip evidence;
- engine test should reuse existing project infrastructure and pin real contract failures rather than irrelevant implementation details;
- loader exceptions should become readable non-interactive test failures when possible.

### Test-oracle integrity
- added `05_execution/66_TEST_ORACLE_EXIT_CODE_AND_BITE_TEST.md`;
- explicitly captures the shell trap `./test | tail; echo $?`, where `$?` can belong to `tail`;
- direct executable/subprocess exit status is preferred;
- test results distinguish assertion failure, load failure, crash and ambiguous status;
- new regression assertions should perform a controlled bite test when safe;
- crash/abort is not accepted as proof that the intended assertion bites;
- added `executors/test_oracle.py`.

### Completion gate hardening
- `executors/completion_gate.py` now requires exported round-trip invariants for `GAME_READY_COMPLETE`;
- `PIPELINE_INTEGRATED` runtime import/instantiation must include an evidence kind;
- accepted Level D evidence kinds are `ENGINE_PRODUCTION_LOADER`, `ENGINE_REGRESSION_TEST`, `ENGINE_INSTANTIATION`;
- a bare string `PASS` for runtime import no longer closes Level D;
- existing Bollard run proved the old gate correctly blocked Level D while runtime import was `UNVERIFIED`; the new evidence-kind extension remains `CONTRACT_READY` until the next run tests it directly.

### Project profile schema
- expanded `09_engine/92_PROJECT_ASSET_PIPELINE_PROFILE_SCHEMA.md` with canonical runtime paths, forbidden lookalike roots, loader, build system, narrow runtime test target/binary and test-oracle policy;
- project profiles now carry exactly the infrastructure facts that consumed repeated discovery calls in the Bollard run;
- profile freshness/invalidation is explicit when build/importer/catalog configuration changes.

### Routing and task packs
- `SESSION_PREFLIGHT` can resolve matching project profile/runtime root once;
- `GAME_READY_FINISH` now includes image-cache coherence, Pipeline DAG, runtime-root preflight and export round-trip invariants;
- `PIPELINE_INTEGRATION` now requires canonical runtime root, target-engine smoke test and trustworthy test oracle;
- Knowledge Router adds direct routes for stale image cache, local dirty-stage repair, ambiguous runtime roots, post-export dimension/contact regressions and false-green shell tests;
- System Prompt distinguishes Level C round-trip evidence from Level D engine evidence and forbids habitual full pipeline replay.

### New semantic skills
- `IMAGE_CACHE_COHERENCE`;
- `PIPELINE_DAG_PLAN`;
- `EXPORT_ROUNDTRIP_VALIDATE`;
- `RUNTIME_PATH_RESOLVE`;
- `TEST_ORACLE`;
- `ENGINE_INTEGRATION_PROOF`.

All new v0.7 executors remain `CONTRACT_READY` pending the next real benchmark. `MESH_VALIDATE` remains `EXECUTOR_READY`.

### B9 benchmark
- added `07_examples/76_LAFAR_CIVIC_BOLLARD_PIPELINE_INTEGRATION_REGRESSION_BENCHMARK.md`;
- records the stale image datablock, 1048-vs-1050 mm exported dimension regression, wrong runtime root, false `EXIT=0`, invalid first bite-test interpretation, unnecessary stage replay and repeated build-system discovery;
- preferred v0.7 target after Level C with matching profile: <=10k integration tokens, zero project-profile rediscovery, zero false-green test results, zero ambiguous runtime-root writes and zero full pipeline restarts after local repair.

Canonical module count after manifest release: **198**.

## 0.6.0

v0.6.0 is the **deterministic bake/runtime closure** release, based on the ~36k-token captured game-ready continuation of the real Lafar Civic Bollard run.

Key changes:
- deterministic bake execution with checked `FINISHED` result and correct active image-node binding;
- explicit BaseColor/Roughness/Metallic/AO/Normal/Emissive channel semantics;
- semantic `UV_CONTRACT_ID` shared by bake source and LODs;
- incremental Dirty-Stage Cache and long-running job protocol;
- semantic bake validation;
- import-safe build/bake/export modules;
- runtime packaging/readback contract;
- executors for bake, UV atlas, image validation and glTF package readback;
- `MESH_VALIDATE` promoted to `EXECUTOR_READY`;
- B8 benchmark `07_examples/75_LAFAR_CIVIC_BOLLARD_BAKE_REGRESSION_BENCHMARK.md`;
- canonical module count: **190**.

## 0.5.0

v0.5.0 is the first benchmark-driven **agent execution + completion** release.

Key changes:
- explicit completion levels from reconstruction through pipeline integration;
- Blender 5.1 compatibility matrix and runtime preflight;
- reusable reference/profile/radial/mesh/runtime/QA/completion executors;
- maintained-civic material finish model;
- emissive authoring/runtime separation;
- Game-Ready Bake Gate;
- floating detail/decal hardening;
- asset catalog integration contract;
- Task Packs, routing and benchmark-driven efficiency targets;
- first full Lafar Civic Bollard B7 benchmark;
- canonical module count: **182**.

## 0.3.0

Added full Reconstruction Layer:
- evidence/provenance model;
- concept-sheet segmentation;
- authority/conflict system;
- dimension graph and locks;
- landmark/calibration system;
- geometry inference rules;
- exact feature/material/branding handling;
- parametric reconstruction workflow;
- multi-view QA/regression gates;
- blueprint/photo/stylized modes;
- Lafar Street Bench benchmark.

## 0.2.0

Added production layer:
- camera/reference matching;
- Visual Feature Map;
- high/low-poly workflow;
- baking pipeline;
- trim sheets;
- decals/floating details;
- curve/Geometry Nodes/procedural material authoring;
- texture packing/mip safety;
- asset variants/randomization;
- automated visual diff;
- reference fidelity levels;
- authoring-to-runtime handoff;
- engine profile/adapter;
- deterministic QA render/diff patterns.

Architecture decision retained across releases:
- modular MD files are canonical;
- `_FULL_LIBRARY.md` is generated from `MANIFEST.json`.

---

## FILE: `README.md`

# BlenderSkill

Canonical knowledge repository for the Blender AI Agent Library.

## Current release

**v0.7.0** — runtime-proof integrity, cache coherence, canonical project paths and executable stage reuse.

v0.7 is based on the final continuation of the real Lafar Civic Bollard pipeline test. After the earlier captured ~36k-token game-ready continuation, another ~45k tokens were consumed closing runtime integration, for roughly ~81k post-v0.5 continuation tokens. The final asset was correct and reached `PIPELINE_INTEGRATED`, but the run exposed a new bottleneck: the agent was spending context proving infrastructure that should already be encoded in the project profile and execution layer.

## Purpose

The repository contains modular Markdown skills plus reusable Python executors/candidates for an AI agent that plans, builds, reconstructs, validates and prepares Blender assets for game/VFX pipelines.

The canonical knowledge source is the modular library stored in the numbered directories. `_FULL_LIBRARY.md` is generated automatically from modules listed in `MANIFEST.json` and should not be edited manually.

## Main areas

- `00_governance` — state/task routing, semantic skills, completion evidence and execution policy
- `01_analysis` — briefs, references, features and measurements
- `02_blender_api` — Blender 5.1 API strategy, runtime compatibility and image-datablock cache coherence
- `03_modeling` — hard-surface, topology, UV, trim sheets, floating details and authoring workflows
- `04_game_ready` — runtime optimization, deterministic bake, UV/LOD contracts, emissive and export constraints
- `05_execution` — QA, dirty-stage cache, executable pipeline DAG, post-export invariants, test-oracle integrity and completeness
- `06_prompts` — planner/reviewer/repair prompts and system prompt
- `07_examples` — examples and real benchmark/post-mortem runs
- `08_scripts` — reusable validation/import-safety patterns
- `09_engine` — engine/project profiles, canonical runtime roots, packaging, catalog and engine smoke-test contracts
- `10_reconstruction` — evidence-driven 1:1 reconstruction system
- `11_playbooks` — asset-class production playbooks
- `executors` — reusable Python executors/candidates
- `99_sources` — technical sources

## Completion model

```text
RECONSTRUCTION_COMPLETE
-> MODELING_COMPLETE
-> GAME_READY_COMPLETE
-> PIPELINE_INTEGRATED
```

A Blender render, successful bake, exported glTF or Blender re-import is not automatically a complete runtime asset.

### Level C — `GAME_READY_COMPLETE`

Requires, as applicable:
- final geometry/LOD/collision validation;
- runtime material closure;
- stable UV contract;
- semantic bake validation;
- disk/Blender image-cache coherence;
- canonical output path preflight;
- package readback;
- post-export round-trip invariant validation;
- baked-runtime QA.

### Level D — `PIPELINE_INTEGRATED`

Additionally requires target-runtime proof. v0.7 distinguishes:

```text
Blender glTF import
= Level C round-trip evidence

ENGINE_PRODUCTION_LOADER
ENGINE_REGRESSION_TEST
ENGINE_INSTANTIATION
= valid Level D evidence kinds
```

`executors/completion_gate.py` no longer accepts a bare `runtime_import_or_instantiation: PASS` as Level D proof.

## v0.7 execution model

The central change is an enforced dependency DAG:

```text
changed input
-> PIPELINE_DAG_PLAN
-> dirty dependency closure
-> execute only dirty stages
-> reuse accepted independent artifacts
-> validate
```

A local repair must not default to:

```text
build -> decals -> bake all -> export -> import -> test
```

when only a subset depends on the change.

Examples:
- stale Blender image datablock -> reload/binding QA; baked PNG remains clean;
- wrong runtime output root -> package/readback/engine test dirty; texture pixels remain clean;
- underside geometry change -> geometry + actually dependent bake channels + export/round-trip/test; separate decal atlas normally remains clean.

## Image cache coherence

The final Bollard run proved a silent Blender failure class:

```text
accepted new PNG on disk
+
old bpy.data.images datablock with same name
=
runtime material renders stale pixels
```

v0.7 adds `IMAGE_CACHE_COHERENCE` and `executors/image_cache_coherence.py`.

When disk is authoritative:

```text
validate file
-> load/reload Blender image datablock
-> verify canonical filepath/colorspace/dimensions
-> verify material binding
-> runtime QA
```

Do not rebake a correct texture merely because Blender is displaying an older cached image.

## Canonical runtime path

A real directory is not necessarily an engine-visible directory.

v0.7 adds `RUNTIME_PATH_RESOLVE` and forbids per-script root guessing.

Authority:

```text
validated project profile
> build/engine asset-root definition
> production loader config
> engine test fixture
> sibling exporter
> heuristic search
```

For the currently verified RPG project profile:

```text
engine asset directory = <repo>/Assets
game asset root       = <repo>/Assets/GameAssets
forbidden lookalike   = <repo>/GameAssets
```

These facts are stored in `09_engine/profiles/RPG_PROJECT_ASSET_PIPELINE_PROFILE.md` and should be reused until project configuration invalidates them.

## Post-export invariants

v0.7 explicitly re-measures the final exported/re-imported artifact.

This exists because the Bollard source looked correct while exported LOD0 became 1048 mm instead of the locked 1050 mm after underside/fillet changes.

Protected invariants may include:
- dimensions;
- contact datum;
- LOD family/counts;
- triangle budgets;
- material/image survival;
- UV/custom data;
- handedness/asymmetry.

## Test oracle integrity

A green-looking shell command is not enough.

Unsafe without verified `pipefail`:

```bash
./ModelTests.exe 2>&1 | tail -20
echo $?
```

because `$?` can belong to `tail` rather than the test process.

v0.7 adds `TEST_ORACLE` and `executors/test_oracle.py` for direct-process return-code capture.

New regression assertions should perform a controlled bite test when safe:

```text
correct baseline
-> intentionally change one expectation
-> intended assertion fails with expected message
-> restore
-> final test passes
```

Crash/abort/load failure is not a valid bite.

## Semantic execution

Before ad-hoc Python/shell/project code, check `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`.

New v0.7 semantic skills include:
- `IMAGE_CACHE_COHERENCE`;
- `PIPELINE_DAG_PLAN`;
- `RUNTIME_PATH_RESOLVE`;
- `EXPORT_ROUNDTRIP_VALIDATE`;
- `TEST_ORACLE`;
- `ENGINE_INTEGRATION_PROOF`.

New candidate executors include:
- `executors/image_cache_coherence.py`;
- `executors/pipeline_dag.py`;
- `executors/runtime_path_resolver.py`;
- `executors/export_roundtrip_validate.py`;
- `executors/test_oracle.py`.

They remain `CONTRACT_READY` until the next real benchmark exercises the packaged implementations.

`MESH_VALIDATE` remains `EXECUTOR_READY` from real Blender 5.1 evidence.

## Benchmarks

Canonical benchmarks now include:
- Lafar Street Bench reconstruction;
- Lafar Civic Bollard end-to-end asset benchmark;
- Lafar Civic Bollard bake/runtime regression benchmark;
- Lafar Civic Bollard final pipeline-integration regression benchmark.

Known cost evidence:

```text
first Bollard full baseline                  ~60k tokens
captured v0.5 game-ready continuation        ~36k tokens
additional final integration continuation    ~45k tokens
post-v0.5 continuation combined              ~81k tokens
```

Preferred v0.7 target once an asset is already `GAME_READY_COMPLETE` and the matching project profile exists:

```yaml
pipeline_integration_tokens: <= 10000
project_profile_rediscovery_calls: 0
false_green_test_results: 0
ambiguous_runtime_root_writes: 0
full_pipeline_restarts_after_local_repair: 0
blender_import_used_as_level_d_proof: 0
```

These are benchmark goals, not universal limits.

## Repository rules

1. Prefer updating an existing canonical responsibility over creating duplicate parallel skills.
2. Add a new skill only for a distinct reusable responsibility/failure class.
3. Keep semantic identity separate from transient Blender names/UI state.
4. `MANIFEST.json` defines the canonical modules compiled into `_FULL_LIBRARY.md`.
5. GitHub Actions regenerates `_FULL_LIBRARY.md`; never edit the snapshot manually.
6. Candidate executors are not promoted without real runtime evidence.
7. A release should improve quality, proof strength or cost — documentation volume alone is not progress.
8. Validated project facts belong in profiles and should not be rediscovered per asset.
9. Local repairs execute the DAG dirty closure, not the whole pipeline by habit.
10. Level D requires target-engine evidence with a trustworthy test oracle.

## Current target

- Blender 5.1.x
- Python automation through Blender API/BMesh where practical
- evidence-driven reconstruction
- game-ready hard-surface production
- deterministic procedural-to-runtime material closure
- incremental dependency-driven execution
- target-engine integration proof
- glTF/GLB neutral baseline unless an Engine Profile overrides it
