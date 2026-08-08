# Blender AI Agent Library v0.3.0 — Full compiled snapshot

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
- ustalić narzędzia,
- wersję Blendera,
- stan sceny,
- jednostki,
- aktywny plik,
- obecne kolekcje i assety.

Wyjście:
`Scene Snapshot`.

### S1 — ANALYZE
Cel:
- zrozumieć funkcję assetu,
- rozbić referencję na bryły,
- wyodrębnić cechy rozpoznawcze,
- określić niewiadome.

Wyjście:
`Asset Brief`.

### S2 — CONTRACT
Cel:
- utworzyć Feature Contract,
- oznaczyć `MUST`, `SHOULD`, `OPTIONAL`,
- przypisać metryki i tolerancje.

Wyjście:
`Feature Contract`.

### S3 — PLAN
Cel:
- dobrać technikę modelowania,
- rozdzielić obiekt na części,
- ustalić modyfikatory,
- zaplanować checkpointy,
- przewidzieć UV/material/export.

Wyjście:
`Build Plan`.

### S4 — BLOCKOUT
Cel:
- zbudować tylko bryły główne,
- zweryfikować skalę, proporcje i sylwetkę.

Zakaz:
- drobnych detali,
- finalnych materiałów,
- kosztownych beveli.

### S5 — PRIMARY_DETAIL
Cel:
- dodać cechy rozpoznawcze,
- rowki, wycięcia, obramowania, główne łączenia.

### S6 — SECONDARY_DETAIL
Cel:
- śruby, szczeliny, uchwyty, panele, drobne zaokrąglenia,
- tylko jeżeli wpływają na odbiór lub specyfikację.

### S7 — SHADING_UV_MATERIAL
Cel:
- poprawić normalne,
- przygotować UV,
- utworzyć materiały zgodne z runtime.

### S8 — GAME_READY
Cel:
- pivot,
- naming,
- LOD/collision według potrzeb,
- porządek sceny,
- optymalizacja.

### S9 — VALIDATE
Cel:
- test wizualny,
- test techniczny,
- porównanie z Feature Contract.

### S10 — EXPORT
Cel:
- wyeksportować,
- sprawdzić wynik po eksporcie,
- nie tylko stan w Blenderze.

## Gates

Nie wolno przejść:
- S4 -> S5 bez pozytywnego silhouette check,
- S5 -> S6 bez spełnienia cech `MUST`,
- S7 -> S8 przy błędnym shadingu,
- S9 -> S10 przy niespełnionym `MUST`.

## Cofnięcie

Każdy failed gate kieruje do najwcześniejszego stanu, w którym powstał błąd.
Nie maskuj błędu późniejszym etapem.

## Reconstruction branch

Jeżeli zadanie jest rekonstrukcją z wielowidokowej referencji lub blueprint-like concept sheet,
przed standardowym `BLOCKOUT` uruchom `10_reconstruction/149_RECONSTRUCTION_STATE_MACHINE.md`.

Standardowa state machine pozostaje warstwą nadrzędną dla authoring/runtime,
a Reconstruction State Machine rozwija ANALYZE/CONTRACT/PLAN/BUILD/VALIDATE.


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

Agent nie powinien ładować całej biblioteki do każdego zadania.

Przed wyborem modułów stosuj `00_governance/06_TASK_PACK_PROTOCOL.md`.
Knowledge Router wybiera najmniejszy wymagany pakiet dla bieżącego STATE i task subtype.

## Session startup / first scene mutation
Load Task Pack `SESSION_PREFLIGHT`:
- `00_governance/00_AGENT_CHARTER.md`
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `02_blender_api/19_TOOL_DISCOVERY_AND_REGISTRY.md`
- `02_blender_api/25_TOOL_CALL_AND_TOKEN_EFFICIENCY.md`
- `02_blender_api/28_AGENT_TOOL_API_PROFILE.md`
- `02_blender_api/23_SCENE_INSPECTION.md`

Before production mutation, bind the current connected tools to the semantic capabilities required by the selected skill.
Do not assume that knowledge about Blender implies that the current integration can execute it.

## Nowy asset hard-surface
Load:
- Agent Charter
- State Machine
- Semantic Skill Registry
- Asset Brief Schema
- Reference Decomposition
- Feature Contract
- Modeling Decision Tree
- Hard Surface Workflow
- Game Asset Contract
- Build Plan
- Execution Protocol
- Retry Budget and Strategy Switching
- Visual QA

Do not preload UV/material/LOD/export modules before their state is reached.

## Poprawka istniejącego assetu
Load:
- Agent Charter
- Semantic Skill Registry
- Feature Contract
- Scene Inspection
- API Strategy
- Idempotency/Recovery
- Retry Budget and Strategy Switching
- Visual QA
- Failure Recovery
- Repair Prompt

## Problem z Blender API
Load:
- API Strategy
- Tool Discovery and Registry
- Agent Tool API Profile
- bpy.data vs bpy.ops vs BMesh
- Context/Mode/Selection
- Scene Inspection
- Tool Call Efficiency
- Retry Budget and Strategy Switching

## Procedural panel line / narrow groove
Load:
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `blender-agent-procedural-hard-surface-panel-lines.md`
- `02_blender_api/28_AGENT_TOOL_API_PROFILE.md`
- `05_execution/61_RETRY_BUDGET_AND_STRATEGY_SWITCH.md`

If the host surface is SubD-controlled or pinching/topology flow becomes relevant, additionally load:
- `blender-agent-subdivision-topology-control.md`

Do not route wide/deep recesses or silhouette-changing features to `HS_PANEL_LINE`.

## Subdivision topology problem
Load:
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `blender-agent-subdivision-topology-control.md`
- `03_modeling/33_TOPOLOGY_NORMALS_SHADING.md`
- `02_blender_api/21_BPY_DATA_OPS_BMESH.md`
- `05_execution/61_RETRY_BUDGET_AND_STRATEGY_SWITCH.md`

Typical triggers:
- support loops bunching around corners;
- curved-surface pinching;
- local density that should terminate;
- cylindrical recess/protrusion on curved SubD surface;
- branch junction cleanup;
- pole-safe sphere requirement.

## Optymalizacja do gry
Load Task Pack `GAME_READY`:
- Game Asset Contract
- Polycount/LOD/Collision
- Pivots/Transforms
- Texture/Material Runtime
- active Engine Profile
- active Project Asset Pipeline Profile
- glTF Export
- Final Validation

## Asset modularny
Dodatkowo:
- Modularity/Instancing
- Modular Architecture Example

## Animowany asset
Dodatkowo:
- Animation and Rigging

## Reviewer
Load:
- Feature Contract
- Visual QA
- Final Validation
- Reviewer Prompt

## Token budget rule

Jeżeli agent potrzebuje jednej informacji, nie ładuj całego folderu.
Najpierw użyj Task Pack, potem routera, potem najwęższego modułu.

Zawsze stosuj `02_blender_api/25_TOOL_CALL_AND_TOKEN_EFFICIENCY.md`:
- obliczaj lokalnie;
- agreguj;
- nie wysyłaj raw arrays/profiles do LLM bez konkretnego diagnostic need.

## Retry budget rule

Po pierwszej porażce agent diagnozuje i może wykonać tylko jedną poprawioną próbę tej samej strategii.
Po drugiej porażce tej samej strategii musi załadować `05_execution/61_RETRY_BUDGET_AND_STRATEGY_SWITCH.md`, przeprowadzić re-inspection i zmienić strategię albo zatrzymać zadanie jako blocker.

## High -> low + bake
Load:
- High-Poly / Low-Poly Workflow
- Baking Pipeline
- UV/Texel Density/Materials
- Texture Packing and Mip Safety
- Automated Visual Diff
- Authoring to Runtime Handoff

## Trim-sheet UV texturing
Load:
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `03_modeling/40_TRIM_SHEETS.md`
- `03_modeling/34_UV_TEXEL_DENSITY_MATERIALS.md`
- `04_game_ready/43_TEXTURE_MATERIAL_RUNTIME.md`
- `04_game_ready/47_TEXTURE_PACKING_AND_MIP_SAFETY.md`

If unique local graphics are present, additionally load:
- `03_modeling/41_DECALS_AND_FLOATING_DETAILS.md`

If runtime material/draw-call cost is part of the task, additionally load:
- `04_game_ready/46_DRAW_CALLS_INSTANCING_AND_BATCHING.md`
- the active Engine Profile.

## Procedural / repeated asset
Load:
- Geometry Nodes Authoring
- Curves for Assets, jeśli dotyczy
- Modularity/Instancing
- Asset Variants and Randomization
- Draw Calls/Instancing/Batching

## Reference reconstruction
Load first:
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `00_governance/06_TASK_PACK_PROTOCOL.md`
- `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md`

Then load only the modules required by the current/failing reconstruction stage.

Do not load detail/modeling skills before the controller has passed camera, scale, silhouette and primary-form gates.

When a validated detail feature is reached, route it through the Semantic Skill Registry rather than improvising a modeling technique.

## Technical concept sheet / blueprint ANALYZE

Use Task Pack `RECON_TECHNICAL_SHEET_ANALYZE`.

Required core:
- `10_reconstruction/102_EVIDENCE_MODEL.md`
- `10_reconstruction/103_REFERENCE_INGESTION_PROTOCOL.md`
- `10_reconstruction/106_VIEW_AUTHORITY_MATRIX.md`
- `01_analysis/14_REFERENCE_MEASUREMENT_PROTOCOL.md`
- `10_reconstruction/160_BLUEPRINT_AND_TECHNICAL_DRAWING_MODE.md`
- `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md`
- `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md`
- `06_prompts/67_CONCEPT_SHEET_INGEST_PROMPT.md`

Route technical image measurement to semantic skill `REFERENCE_MEASURE`.

After segmentation and calibration are validated:
- reuse cached ROI/view authority/dimensions;
- do not rescan the full sheet;
- re-enter analysis only for a specific failing ROI, metric, feature or source update.

Do not read unrelated sibling build scripts for project conventions if an active `PROJECT_ASSET_PIPELINE_PROFILE.md` is available.
If no profile exists, inspect the smallest relevant range and persist the discovered convention according to `09_engine/92_PROJECT_ASSET_PIPELINE_PROFILE_SCHEMA.md`.

## Runtime integration
Load:
- Agent Tool API Profile
- Game Asset Contract
- Engine Profile Schema
- Engine Adapter Protocol
- Project Asset Pipeline Profile Schema
- Authoring to Runtime Handoff
- właściwy format eksportu

## Full 1:1 reconstruction

Load core:
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `00_governance/06_TASK_PACK_PROTOCOL.md`
- `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md`
- `10_reconstruction/101_DEFINITION_OF_1_TO_1.md`
- `10_reconstruction/149_RECONSTRUCTION_STATE_MACHINE.md`
- `10_reconstruction/155_RECONSTRUCTION_KNOWLEDGE_ROUTING.md`

Then load only the current Task Pack/stage pack.

### Concept sheet ingest
- 102–109
- 160
- 168
- 170
- script 91
- prompt 67

### Geometry solve
- 110–123
- 128–134
- appropriate `11_playbooks`

### Rear/bottom
- 119
- 135
- playbook 113

### Surface
- 124–127
- 140
- appropriate material playbook

### Reconstruction QA
- 141–148
- scripts 86–90
- prompt 65

### Lafar bench benchmark
- example 73
- playbooks 110, 111, 112, 113, 114, 115, 116, 117


---

## FILE: `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`

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
- sprawdź release notes Python API,
- sprawdź zmiany operatorów i Geometry Nodes,
- nie zakładaj kompatybilności skryptów bez testu.

## Preferowana kolejność narzędzi

1. bezpośrednie odczyty z `bpy.data` / obiektów RNA,
2. bezpośrednie modyfikowanie właściwości obiektów i data-blocków,
3. `bmesh` dla topologii,
4. modyfikatory,
5. `bpy.ops` tylko gdy dana operacja rzeczywiście jest operatorem lub alternatywa jest nieproporcjonalnie złożona,
6. emulowanie UI jako ostateczność.

## Dlaczego

Operatory:
- zależą od context,
- często zależą od mode,
- mogą zależeć od active object / selection,
- bywają trudniejsze do uruchomienia w automatyzacji bez UI.

Data API:
- odwołuje się do jawnych obiektów,
- lepiej nadaje się do idempotentnych skryptów,
- ogranicza ukryty stan.

BMesh:
- jest przeznaczony do niskopoziomowej edycji geometrii mesh,
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
- znaleźć obiekty po nazwie/tagu, a nie przypadkowym zaznaczeniu,
- zweryfikować typ obiektu,
- zweryfikować wersję,
- zapisać stan krytyczny,
- wykonać zmianę,
- uruchomić postcondition check.


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
- przesyłanie do LLM danych, które mogą zostać zagregowane lokalnie.

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
- entire source/build scripts when only a naming/path/material convention is needed.

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

Dodawać lokalne informacje wizualne bez cięcia głównej topologii.

## Kandydaci

- oznaczenia,
- logo,
- numery,
- ostrzeżenia,
- ślady serwisowe,
- cienkie panel lines,
- małe techniczne detale.

## Geometry decals / floating meshes

Dobre, gdy:
- potrzebny jest lokalny detal,
- główny mesh nie powinien być komplikowany,
- pipeline/runtime poprawnie obsługuje takie powierzchnie.

Kontroluj:
- z-fighting,
- offset,
- normals,
- bounds,
- LOD behavior.

## Texture decals

Dobre dla:
- oznaczeń,
- wariantów,
- zabrudzeń,
- informacji diegetycznych.

## Decal atlas

Dla wielu drobnych oznaczeń preferuj atlas zamiast osobnej tekstury per decal.

## Nie używaj decal jako maskowania błędu konstrukcyjnego

Jeżeli referencja ma realne wcięcie o widocznym parallax:
- geometria lub displacement/bake może być właściwszy.

## LOD

Małe decals powinny:
- zanikać w odpowiednim LOD,
- nie pozostawiać migoczących mikropowierzchni.


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

## Geometry
- target triangles:
- max triangles:
- LOD count:
- deformation:
- backface assumptions:
- hidden geometry policy:

## Materials
- max material slots:
- shader model:
- transparency:
- alpha mode:
- emissive:
- normal map:
- texture resolution:
- compression target:

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

## Edytowalność

Źródłowy `.blend` nie powinien być tym samym, czym finalna "spłaszczona" wersja export.
Zachowaj authoring source.


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
- sprawdź wymagane capabilities wybranego skilla.

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

## 5. Checkpoint

Nie kontynuuj, jeśli checkpoint FAIL.

## 6. Save

Zapisuj:
- przed ryzykownym Apply,
- po zaakceptowanym dużym etapie,
- przed exportem,
- przed strategy switch, jeżeli nowa strategia może istotnie zmienić topologię.

## 7. No silent repair

Jeżeli wykonanie różni się od planu, zapisz to jako deviation.
Nie zmieniaj strategii po cichu.

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

## Minimalny zestaw widoków

Dla statycznego prop:
- front ortho,
- side ortho,
- top ortho,
- 3/4 perspective.

Jeżeli geometria ma znaczenie z innych stron:
- rear,
- bottom.

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
- texture use.

## Difference score

Dla każdej cechy:
- PASS,
- MINOR,
- FAIL.

`MUST + FAIL` = asset nie może przejść dalej.


---

## FILE: `05_execution/53_FINAL_VALIDATION.md`

# Final Validation

## Visual

- [ ] silhouette matches
- [ ] proportions within tolerance
- [ ] all MUST features visible
- [ ] no invented major details
- [ ] no missing characteristic recess/groove/cut
- [ ] material regions match design
- [ ] asymmetry preserved where required

## Mesh

- [ ] no unintended duplicate geometry
- [ ] no obvious non-manifold issues where mesh should be closed
- [ ] face normals correct
- [ ] no accidental zero-area geometry
- [ ] no uncontrolled shading artifacts
- [ ] triangle count documented

## Modifiers

- [ ] stack intentional
- [ ] no disabled forgotten modifiers
- [ ] no accidental duplicate modifiers
- [ ] apply state follows pipeline

## UV / materials

- [ ] UV layers named
- [ ] overlap intentional
- [ ] texel density acceptable
- [ ] material slots within budget
- [ ] Blender-only material features baked/replaced where required

## Scene

- [ ] naming clean
- [ ] no Cube.001 style leftovers
- [ ] helper objects hidden/removed according to policy
- [ ] collection structure clean
- [ ] pivot correct
- [ ] transforms correct

## Game-ready

- [ ] LOD correct
- [ ] collision correct
- [ ] instancing/reuse considered
- [ ] runtime bounds correct
- [ ] export tested

## Deliverables

- [ ] source `.blend`
- [ ] runtime export
- [ ] textures
- [ ] validation report


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

Mierzy:
- precision,
- naming,
- transforms,
- idempotency.

### B2 — Reference fidelity
Zbuduj hard-surface prop z front/side/top.

Mierzy:
- silhouette,
- proportions,
- feature retention.

### B3 — Repair
Dostarcz celowo wadliwy asset.

Mierzy:
- scene inspection,
- local patch,
- regression avoidance.

### B4 — API trap
Ustaw:
- zły active object,
- Edit Mode,
- nietypową selection.

Mierzy:
- odporność na context.

### B5 — Optimization
Dostarcz zbyt ciężki asset.

Mierzy:
- czy agent redukuje koszt bez utraty MUST,
- czy nie używa bezmyślnie Decimate.

### B6 — Export
Dostarcz hierarchy + materials + animation.

Mierzy:
- poprawność transform,
- export,
- post-export verification.

## Metrics

- feature pass rate,
- MUST regression count,
- dimension error,
- triangle count,
- material slot count,
- number of tool calls,
- number of failed tool calls,
- repair iterations,
- bytes/tokens instrukcji załadowanych do zadania,
- time-to-valid-asset.

## Najważniejsze metryki agenta

1. `MUST pass rate`
2. `regressions per repair`
3. `failed API calls`
4. `tool calls per accepted feature`
5. `reference deviation`
6. `runtime contract violations`

## Release gate biblioteki

Nowa wersja biblioteki nie powinna być uznana za lepszą tylko dlatego, że ma więcej treści.
Musi poprawiać wynik benchmarków albo zmniejszać koszt przy tej samej jakości.


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

## FILE: `06_prompts/60_SYSTEM_PROMPT.md`

# System Prompt — Blender Asset Agent

Jesteś technical artistem i modelerem 3D specjalizującym się w Blender 5.1 oraz assetach runtime do gier.

Twoim zadaniem nie jest "wygenerować model", lecz przeprowadzić kontrolowany pipeline od analizy referencji do zwalidowanego assetu.

Obowiązuje state machine:
DISCOVER -> ANALYZE -> CONTRACT -> PLAN -> BLOCKOUT -> PRIMARY_DETAIL -> SECONDARY_DETAIL -> SHADING_UV_MATERIAL -> GAME_READY -> VALIDATE -> EXPORT.

Reguły:
1. Nie modyfikuj sceny przed analizą stanu.
2. Utwórz Feature Contract dla wszystkich charakterystycznych cech.
3. Każda cecha MUST musi mieć właściciela w scenie i test QA.
4. Preferuj jawny Blender Data API i BMesh. `bpy.ops` używaj tylko ze świadomym context/mode/selection.
5. Skrypty mają być idempotentne.
6. Buduj parametrycznie tam, gdzie to możliwe.
7. Po każdej fazie wykonuj checkpoint.
8. Nie kontynuuj przy FAIL cechy MUST.
9. Nie dodawaj elementów, których nie ma w briefie/referencji, chyba że są technicznie konieczne.
10. Nie usuwaj detali przy optymalizacji bez sprawdzenia Feature Contract.
11. Zawsze utrzymuj edytowalne źródło.
12. Export jest osobnym etapem i wymaga walidacji wyniku poza stanem authoringowym.
13. Przed pierwszą mutacją produkcyjnej sceny zbuduj Tool Registry i zwiąż wymagane capabilities zgodnie z `02_blender_api/28_AGENT_TOOL_API_PROFILE.md`.
14. Nie wymyślaj nazw narzędzi ani możliwości integracji. Knowledge o Blenderze nie oznacza, że bieżący runtime ma capability do wykonania operacji.
15. Jeżeli istnieje zarejestrowany Semantic Skill dla żądanej operacji, użyj jego kontraktu zamiast generować ad-hoc workflow.
16. Dla tej samej operacji z tymi samymi preconditions dozwolona jest maksymalnie jedna poprawiona ponowna próba. Po drugiej porażce wymagany jest re-inspection i strategy switch zgodnie z `05_execution/61_RETRY_BUDGET_AND_STRATEGY_SWITCH.md`.

W odpowiedzi operacyjnej utrzymuj format:
- STATE
- INPUT FACTS
- UNKNOWN / ASSUMPTIONS
- FEATURE IDS
- SELECTED SKILL ID
- REQUIRED CAPABILITIES / BINDING STATUS
- ACTION
- POSTCONDITIONS
- CHECKPOINT RESULT
- NEXT STATE

Nie generuj długich opisów, jeżeli agent może zamiast tego wykonać pomiar.
Nie wykonuj serii prób "na oko". Najpierw zdiagnozuj różnicę.

## Semantic skill routing

Przed implementacją sprawdź `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`.

Przykłady:
- narrow seam/groove path -> `HS_PANEL_LINE`;
- SubD topology flow/pinching/local density -> `SUBD_TOPOLOGY_CONTROL`;
- repeated trim-compatible surface -> `TRIM_SHEET_UV`;
- reference-driven form solve -> `RECONSTRUCT_REFERENCE`.

Jeśli skill ma status `CONTRACT_READY`, ale nie `EXECUTOR_READY`, możesz wykonać zgodną z kontraktem lokalną implementację przez `bpy`/BMesh, ale nie przedstawiaj jej jako trwałego packaged executora i zawsze przeprowadź walidację zdefiniowaną przez skill.

## Reconstruction mode

Jeżeli użytkownik wymaga odtworzenia 1:1 z referencji:
- uruchom Reconstruction State Machine,
- nie używaj "looks similar" jako kryterium,
- twórz Evidence Ledger, Dimension Graph i View Authority Matrix,
- nie inventuj unknown geometry,
- nie pozwalaj hero view nadpisać explicit dimensions/orthographic authority,
- przeprowadź multi-view QA przed runtime optimization,
- nie uruchamiaj detail skills przed przejściem camera/scale/silhouette/primary-form gates.

## Failure behavior

Po nieudanej operacji:
1. odczytaj realny stan sceny i błąd;
2. sklasyfikuj przyczynę;
3. popraw precondition lub jeden uzasadniony parametr;
4. wykonaj najwyżej jedną poprawioną próbę tej samej strategii;
5. po ponownej porażce nie powtarzaj call pattern — zmień strategię, przywróć checkpoint lub zgłoś blocker.

Każdy retry musi dostarczać nową informację lub zmieniać zwalidowany precondition.


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

Uwaga:
otwarte siatki mogą mieć poprawne boundary edges.
Walidator nie powinien oznaczać każdego boundary jako błąd bez znajomości kontraktu.


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

Generować identyczne rendery kontrolne między iteracjami.

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
- asset bounds,
- feature set.

## Pseudocode

```python
def render_checkpoint(asset_id, checkpoint, cameras, profiles):
    for camera in cameras:
        set_camera(camera)
        for profile in profiles:
            apply_qa_profile(profile)
            path = build_output_path(...)
            render(path)
            write_metadata(path)
```

## Rule

QA render pipeline nie powinien permanentnie niszczyć materiałów assetu.
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

## FILE: `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md`

# Reconstruction Layer Index and Reference Reconstruction Controller

Warstwa `10_reconstruction` służy do ścisłego odtwarzania obiektu 3D na podstawie:
- concept sheet,
- blueprintów,
- rzutów ortograficznych,
- zdjęć,
- renderów,
- detail close-upów,
- wymiarów,
- opisów funkcjonalnych i materiałowych.

Nie jest to warstwa "inspiracji".
Celem jest maksymalnie wierna rekonstrukcja przy jawnej obsłudze niepewności.

Ten plik jest również **wysokopoziomowym controllerem rekonstrukcji z obrazu**. Nie powiela szczegółowych algorytmów z pozostałych modułów; ustala kolejność pracy i routuje agent do właściwych kompetencji.

---

## 1. Fundamental rule

**Reconstruct shape and proportion before detail.**

Model z perfekcyjnymi rowkami, śrubami i materiałami, ale błędną sylwetką lub proporcjami, jest nieudaną rekonstrukcją.

Nie używaj detalu do maskowania błędów bryły.

---

## 2. Task-facing reconstruction priority

Dla rekonstrukcji z reference images agent optymalizuje wynik w tej kolejności:

```text
CAMERA
-> SCALE
-> BOUNDING BOX
-> SILHOUETTE
-> PRIMARY MASSES
-> PROPORTIONS
-> SECONDARY MASSES
-> MAJOR CUTOUTS / STRUCTURAL TRANSITIONS
-> EDGE TREATMENT
-> PANEL LINES / GROOVES / VENTS / SEAMS
-> MICRODETAIL
-> MATERIALS / TEXTURING
-> RUNTIME
```

Ta kolejność jest warstwą kontrolną. Szczegółowy stan procesu znajduje się w `149_RECONSTRUCTION_STATE_MACHINE.md`.

---

## 3. Full reconstruction pipeline

`INGEST -> SEGMENT -> CLASSIFY -> AUTHORITY -> REGISTER -> CONSTRAIN -> DECOMPOSE -> PLAN -> BLOCKOUT -> MATCH -> DETAIL -> SHADE -> MULTIVIEW_QA -> RUNTIME`

### Mapping controller -> pipeline

- `CAMERA` -> CLASSIFY / REGISTER
- `SCALE + BOUNDING BOX` -> CONSTRAIN
- `SILHOUETTE + PRIMARY MASSES` -> BLOCKOUT / MATCH
- `PROPORTIONS` -> CONSTRAIN / MATCH
- `SECONDARY MASSES` -> DETAIL
- `SURFACE` -> SHADE
- `VALIDATION` -> MULTIVIEW_QA
- `GAME READY` -> RUNTIME

---

## 4. Packages of knowledge

### Evidence
100–109

Key modules:
- `102_EVIDENCE_MODEL.md`
- `103_REFERENCE_INGESTION_PROTOCOL.md`
- `104_CONCEPT_SHEET_SEGMENTATION.md`
- `105_VIEW_CLASSIFICATION.md`
- `106_VIEW_AUTHORITY_MATRIX.md`
- `107_MULTI_VIEW_CONFLICT_RESOLUTION.md`
- `108_UNCERTAINTY_AND_CONFIDENCE_LEDGER.md`

### Geometry constraints
110–123

Key modules:
- `110_DIMENSION_GRAPH.md`
- `111_DIMENSION_LOCKING_AND_TOLERANCES.md`
- `112_LANDMARK_AND_KEYPOINT_SYSTEM.md`
- `113_REFERENCE_COORDINATE_REGISTRATION.md`
- `114_ORTHOGRAPHIC_REFERENCE_CALIBRATION.md`
- `115_PERSPECTIVE_CAMERA_SOLVING.md`
- `116_SILHOUETTE_CONSTRAINT_SYSTEM.md`
- `117_NEGATIVE_SPACE_AND_CLEARANCE.md`
- `119_HIDDEN_AND_OCCLUDED_GEOMETRY_POLICY.md`

### Surface/material evidence
124–127

### Construction planning
128–140

### Validation
141–148

### Governance
149–159

### Specialized reconstruction
160–169

---

## 5. Reference input contract

The controller should receive as much of the following as available:

```yaml
reference_set:
  asset_id: bench_01
  target_scale_unit: METERS
  known_dimensions:
    - id: WIDTH
      value_m: 1.80
      confidence: LOCKED

  images:
    - id: front
      type: ORTHOGRAPHIC_OR_APPROX_FRONT
      path: /references/bench_front.png

    - id: side
      type: ORTHOGRAPHIC_OR_APPROX_SIDE
      path: /references/bench_side.png

    - id: perspective
      type: PERSPECTIVE
      path: /references/bench_perspective.png
```

If only one image exists, continue only with explicit uncertainty tracking. Do not manufacture unsupported depth or hidden detail.

---

## 6. Reference analysis before modeling

Before geometry creation the agent must identify:

```text
REFERENCE
|
+-- object bounding box
+-- principal axes / orientation
+-- projection class
+-- symmetry evidence
+-- outer silhouette
+-- internal silhouette breaks / negative spaces
+-- major landmarks
+-- dominant planes / curves
+-- repeated structures
+-- depth / perspective cues
+-- material boundaries
+-- hidden or uncertain geometry
```

The authoritative data model for these observations is the Evidence/Constraint/Feature system defined by the detailed reconstruction modules.

---

## 7. Camera-first mismatch rule

The agent must never deform geometry merely because a perspective reference does not line up.

When a screen-space mismatch is detected, diagnose in this order:

```text
1. projection class
2. reference calibration
3. focal length / ortho scale
4. camera rotation and shift
5. object/reference orientation
6. only then geometry
```

Detailed camera behavior belongs to:
- `01_analysis/15_CAMERA_REFERENCE_MATCHING.md`
- `114_ORTHOGRAPHIC_REFERENCE_CALIBRATION.md`
- `115_PERSPECTIVE_CAMERA_SOLVING.md`
- `141_RECONSTRUCTION_QA_CAMERA_RIG.md`

QA cameras are evidence instruments, not artistic cameras. Once calibrated they must not be moved to hide geometric error.

---

## 8. Bounding volume and normalized proportion model

Before detailed modeling, create a proportion model from known dimensions and calibrated views.

Use normalized ratios when exact metric data is incomplete:

```text
object width  = 1.000
object height = 0.540
object depth  = 0.430
seat height   = 0.287
seat depth    = 0.438
```

If one dimension is known, resolve derived dimensions from ratios only when the relevant view/calibration supports that inference.

Do not convert an uncertain pixel estimate into fake metric precision.

The canonical implementation is the Dimension Graph plus the confidence/evidence ledger.

---

## 9. Landmark system

Use semantic landmarks to constrain reconstruction, such as:
- extreme corners;
- seat/front/back junctions;
- major panel corners;
- centers of circular features;
- armrest peaks;
- attachment points;
- dominant transition edges.

Landmarks should use normalized image coordinates where practical and remain semantically stable across topology changes.

Do not use transient vertex indices as landmark identity.

Detailed representation and projection rules are defined in `112_LANDMARK_AND_KEYPOINT_SYSTEM.md` and the QA scripts.

---

## 10. Silhouette-first blockout

The first real geometry must solve:
- world-scale bounds;
- primary silhouette;
- negative spaces;
- primary landmarks;
- primary mass relationships.

Preferred blockout primitives:
- cube/box;
- plane/extruded profile;
- cylinder;
- sphere only when appropriate;
- Mirror;
- Array for actual repetition.

Forbidden as a substitute for unresolved primary form:
- panel lines;
- vents;
- screws;
- decorative booleans;
- micro-bevels;
- final UV/textures.

The blockout gate is controlled by `131_DIMENSION_LOCKED_BLOCKOUT.md` and `146_MULTI_VIEW_CONSISTENCY_GATE.md`.

---

## 11. Primitive/part decomposition

Before topology refinement, decompose the asset into semantic masses.

Example:

```text
BENCH
+-- seat shell
+-- back shell
+-- left structural housing
+-- right structural housing
+-- base / feet
+-- utility insert
+-- trim / lighting / branding
```

For each part record:
- semantic role;
- primitive/profile class;
- symmetry relationship;
- feature ownership;
- likely modeling strategy.

Use `128_RECONSTRUCTION_OBJECT_DECOMPOSITION.md` and `129_FEATURE_TO_MODELING_STRATEGY_MAP.md` for the canonical data model.

---

## 12. Symmetry controller rule

Classify the asset as:
- `FULL_SYMMETRY`
- `PARTIAL_SYMMETRY`
- `ASYMMETRIC`

Use Mirror for the symmetric core when evidence supports it.

Do not mirror asymmetric utility panels, branding, wear, ports, or reference-specific detail merely because the base shell is symmetric.

The canonical policy is `120_SYMMETRY_AND_ASYMMETRY_POLICY.md`.

---

## 13. Multi-view consistency

Multiple views constrain one 3D object.

Typical authority:

```text
FRONT -> width, height
SIDE  -> depth, height, profile
TOP   -> width, depth
REAR  -> rear features/material boundaries
BOTTOM -> underside/service geometry
HERO  -> material/edge language and spatial confirmation
```

Do not silently average contradictory drawings.

Conflicts must be recorded and resolved using the Evidence Model and View Authority Matrix.

---

## 14. Confidence-aware reconstruction

Use the canonical confidence vocabulary from `108_UNCERTAINTY_AND_CONFIDENCE_LEDGER.md`:

- `LOCKED`
- `HIGH`
- `MEDIUM`
- `LOW`
- `UNKNOWN`

When helpful, evidence provenance may separately classify a value as observed/derived/inferred.

For low-confidence hidden geometry:

**Use the simplest continuous solution compatible with all visible evidence.**

Do not add speculative decorative detail to increase perceived sophistication.

---

## 15. Screen-space validation loop

At each accepted stage:

```text
matched QA camera
-> deterministic render/mask
-> compare against reference
-> measure error
-> identify highest-level cause
-> repair
-> revalidate
```

Minimum categories:
- bounding box;
- silhouette;
- landmarks;
- negative spaces;
- major internal feature boundaries.

Prefer measurements over statements such as "looks close".

Use:
- `142_ORTHOGRAPHIC_OVERLAY_VALIDATION.md`
- `143_SILHOUETTE_DIFF_PROTOCOL.md`
- `144_NUMERIC_AND_LANDMARK_VALIDATION.md`
- `145_FEATURE_ROI_VALIDATION.md`
- `146_MULTI_VIEW_CONSISTENCY_GATE.md`

---

## 16. Quality-gate defaults

Project contracts and explicit dimensions always override generic defaults.

For image-derived reconstruction, the following can be used as **starting heuristics**, not universal truth:

### Blockout gate
- bounding-box error < 3%
- major landmark error < 5%

### Primary geometry gate
- silhouette mean error < 2%
- major landmark mean error < 2%

### Final image-reconstruction gate
- silhouette mean error < 1%
- major landmark mean error < 1.5%

These thresholds must be tightened or relaxed according to:
- reference resolution;
- projection confidence;
- asset importance;
- explicit project tolerances;
- whether the input is a real technical drawing or stylized concept art.

Hard numeric dimensions use the tolerance rules in `111` and `148`, not these image-space heuristics.

---

## 17. Repair priority

When validation fails, repair the highest-level error first:

```text
1. camera/reference registration
2. metric scale / bounding box
3. silhouette
4. primary masses
5. primary landmarks / proportions
6. secondary geometry
7. edge treatment
8. detail
9. materials
```

Never repair a panel line while the primary silhouette is still failing.

---

## 18. Detail routing after primary pass

Only after primary geometry passes should the controller route work to specialized skills.

Examples:

```text
structural/cosmetic narrow seam
-> blender-agent-procedural-hard-surface-panel-lines.md

SubD topology / support-loop problem
-> blender-agent-subdivision-topology-control.md

reusable structural texture band
-> 03_modeling/40_TRIM_SHEETS.md

logo / unique marking
-> 03_modeling/41_DECALS_AND_FLOATING_DETAILS.md

high-to-low detail
-> 03_modeling/38_HIGH_LOW_POLY_WORKFLOW.md
-> 03_modeling/39_BAKING_PIPELINE.md
```

This controller orchestrates. Specialized skills execute.

---

## 19. Single-image mode

When only one image exists:

1. classify projection;
2. estimate/match camera;
3. extract visible silhouette and landmarks;
4. solve known dimensions or normalized proportions;
5. infer depth conservatively;
6. explicitly separate observed, derived and inferred information;
7. assign confidence;
8. keep hidden geometry minimal;
9. do not claim literal full 1:1 certainty in unobserved regions.

A single-view result may be an evidence-constrained 3D interpretation rather than a fully determined reconstruction.

---

## 20. Output contract

A controller pass should be able to emit:

```yaml
reconstruction_result:
  asset: bench_01
  stage: PRIMARY_GEOMETRY
  status: PASS

  dimensions:
    width_error_pct: 0.8
    height_error_pct: 1.1
    depth_error_pct: 1.4

  silhouette:
    mean_error_pct: 0.9
    max_error_pct: 2.8

  landmarks:
    mean_error_pct: 1.2
    max_error_pct: 2.1

  unresolved_geometry:
    - underside_rear_shell
```

The detailed final report schema is defined in `152_RECONSTRUCTION_REPORT_SCHEMA.md`.

---

## 21. Controller completion criteria

Before routing to final detail/material/runtime, verify:

```text
[ ] reference projection/classification is resolved sufficiently
[ ] camera/reference registration is validated
[ ] known scale/dimensions are respected
[ ] bounding volume is within tolerance
[ ] primary silhouette passes required views
[ ] major negative spaces pass
[ ] primary landmarks pass
[ ] multi-view conflicts are resolved or explicitly documented
[ ] low-confidence regions are identified
[ ] primary object decomposition is stable
[ ] no lower-level detail contradicts the accepted primary form
```

The full asset is complete only when `159_RECONSTRUCTION_DEFINITION_OF_DONE.md` also passes.

---

## 22. Final rule

Reconstruction 1:1 does not mean "one render looks similar".

It means:
- known dimensions are respected;
- canonical views are simultaneously consistent;
- silhouette and proportions are controlled;
- features do not disappear;
- uncertainty is explicit;
- hidden geometry is not hallucinated;
- detail is added only after the primary form is proven;
- every accepted stage can be validated and regressed.

The controller's permanent priority is:

`CAMERA -> SCALE -> BOUNDING BOX -> SILHOUETTE -> PRIMARY MASSES -> PROPORTIONS -> SECONDARY MASSES -> DETAIL -> MATERIALS -> RUNTIME`.

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
- edge wear.

## Test

Porównaj ten sam region w:
- hero,
- front,
- side,
- material palette.

Jeżeli jasność zmienia się wraz z orientacją powierzchni:
prawdopodobnie to lighting/reflection.

## Brushed metal

Kierunkowy highlight nie powinien być kopiowany do base color jako stała jasna smuga.

## Ambient blue

Niebieskie odbicie od emissive/underglow nie jest kolorem sąsiedniego grafitu.

## QA material rig

Stosuj neutralne, powtarzalne studio lighting do porównania materiałów.


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

## QA

Porównuj ROI w widoku kanonicznym.


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

Podzielić asset według konstrukcji i odpowiedzialności features.

## Kryteria osobnego obiektu

Oddziel, jeśli część:
- ma osobny materiał i wyraźną granicę,
- jest nakładką,
- będzie animowana,
- jest asymetrycznym akcesorium,
- ma być wariantowana,
- jest boolean cutter/helper,
- ma własny feature ownership.

## Nie rozdrabniaj

Nie twórz osobnego object dla każdej śrubki, jeśli:
- mogą być instancjami,
- nie potrzebują niezależnej logiki.

## Decomposition table

| Object | Feature IDs | Material | Modeling method | Runtime fate |

## Stable boundaries

Podział powinien powstać przed detail phase.
Ciągłe łączenie i rozdzielanie obiektów utrudnia regression tracking.


---

## FILE: `10_reconstruction/129_FEATURE_TO_MODELING_STRATEGY_MAP.md`

# Feature-to-Modeling Strategy Map

Każdy Feature ID powinien zostać przypisany do techniki.

## Strategy classes

- PARAMETRIC_PRIMITIVE
- DIRECT_MESH
- BMESH_PROCEDURAL
- BOOLEAN_RECESS
- BOOLEAN_UNION
- SOLIDIFY_SHELL
- BEVEL
- CURVE_PROFILE
- ARRAY_INSTANCE
- GEOMETRY_NODES
- FLOATING_DETAIL
- DECAL
- NORMAL_BAKE
- MATERIAL_ONLY

## Selection criteria

Uwzględnij:
- wpływ na silhouette,
- editability,
- precision,
- repeated use,
- shading,
- runtime,
- risk of regression.

## Example

Głęboki panel:
`BOOLEAN_RECESS` lub `DIRECT_MESH`

Logo:
`DECAL`

Niebieski light strip:
separate geometry + emissive material.

## Rule

Agent nie może wybrać techniki tylko dlatego, że "zna operator".
Technika wynika z feature requirements.


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

Asset jest zakończony dopiero, gdy:

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
- branding poprawny,
- rear/bottom nie pominięte, jeśli istnieją.

## Surface
- material segmentation pass,
- directional materials poprawne,
- emissive/glass logic poprawna.

## QA
- multi-view gate pass,
- regression gate pass,
- no unauthorized deviations.

## Runtime
- optimization nie zmienia chronionych features,
- export validated.

## Documentation
- report,
- manifest,
- inferred geometry list,
- known limitations.


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

## FILE: `11_playbooks/110_HARD_SURFACE_CIVIC_FURNITURE.md`

# Playbook — Hard-Surface Civic Furniture

## Typowe komponenty

- structural side housings,
- seat,
- backrest,
- trim,
- feet/base,
- utility/electronics,
- signage,
- service panels.

## Priorytety

1. ergonomiczna i produktowa silhouette zgodna z reference,
2. masywność i grubości,
3. junction seat/back/sides,
4. materiałowe granice,
5. odporne edge treatment,
6. underside/service logic.

## Typowe techniki

- parametric box/profile modeling,
- Mirror dla core,
- separate trim meshes,
- booleans dla recess/panels,
- curves dla cienkich pasków/profili,
- decals dla logo,
- instancing dla fasteners.

## QA

Wymagane:
- front,
- side,
- top,
- rear,
- bottom,
- 3/4.

## Runtime

Civic asset bywa wielokrotnie instancjonowany.
Kontroluj:
- material slots,
- repeated meshes,
- LOD,
- collision.


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

## Brushed metal

Kontroluj:
- metallic response,
- roughness,
- brushing direction,
- fine normal/roughness variation.

Nie maluj stałego highlightu w base color.

## Dark composite / powder coat

Kontroluj:
- dielectric/metal decision,
- roughness,
- subtle microtexture,
- minimal color variation.

## Boundary

Trim vs body musi mieć:
- poprawną geometrię,
- poprawną material boundary.

Shader sam nie naprawi źle ułożonego trimu.


---

## FILE: `11_playbooks/115_INTEGRATED_LIGHT_STRIP.md`

# Playbook — Integrated Light Strip

## Geometry

Zdefiniuj:
- recess,
- diffuser/cover,
- light-emitting surface,
- ends/corners.

## Design

Pasek może:
- być flush,
- recessed,
- protected by lip.

Reference rozstrzyga.

## Material

Emissive intensity w Blenderze jest lookdev parameter.
Runtime illumination może wymagać osobnego light.

## LOD

Z daleka:
- utrzymaj widoczny akcent,
- uprość fizyczną obudowę jeśli nie wpływa na silhouette.


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

Integrated two reviewed production skills without creating redundant parallel modules:
- expanded `03_modeling/40_TRIM_SHEETS.md` into a full semantic trim-sheet UV texturing skill;
- integrated the reference-image proportion/silhouette workflow into `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md` as the high-level reconstruction controller;
- added explicit trim-sheet routing and controller-first reference routing to the Knowledge Router.

Important integration corrections:
- texel density is now unit-explicit (`px_per_m`) instead of a bare numeric value;
- intentional trim-sheet UV reuse is distinguished from accidental overlap;
- trim-sheet reuse is not treated as an automatic draw-call reduction;
- persistent surface identity should not rely only on transient polygon indices;
- reconstruction confidence vocabulary is aligned with the existing `LOCKED/HIGH/MEDIUM/LOW/UNKNOWN` ledger;
- image-space quality thresholds are defined as overridable heuristics, not universal hard limits.

Agent-runtime readiness pass:
- added `00_governance/05_SEMANTIC_SKILL_REGISTRY.md` as the stable intent -> skill -> capability -> validation routing layer;
- added `02_blender_api/28_AGENT_TOOL_API_PROFILE.md` with required runtime capabilities, discovery/binding states and preflight rules;
- added `05_execution/61_RETRY_BUDGET_AND_STRATEGY_SWITCH.md` to stop blind repeated API/tool attempts;
- registered `HS_PANEL_LINE` and `SUBD_TOPOLOGY_CONTROL` as canonical skills;
- added the existing panel-line and SubD skill files to `MANIFEST.json`, so they are now included in `_FULL_LIBRARY.md`;
- expanded the Knowledge Router with session preflight, panel-line routing, SubD routing and retry-budget loading;
- updated the system prompt to require capability binding, semantic skill selection and a strategy switch after repeated failure;
- canonical module count increased from 163 to 168.

## 0.3.0

Added full Reconstruction Layer:
- 70 reconstruction modules/playbooks/scripts/prompts/benchmark elements,
- evidence/provenance model,
- concept-sheet segmentation,
- authority/conflict system,
- dimension graph and locks,
- landmark and calibration system,
- geometry inference rules,
- exact feature/material/branding handling,
- parametric reconstruction workflow,
- multi-view QA and regression gates,
- specialized modes for blueprint/photo/stylized references,
- Lafar Street Bench reconstruction benchmark.

## 0.2.0

Added production layer:
- camera/reference matching,
- Visual Feature Map,
- high/low-poly workflow,
- baking pipeline,
- trim sheets,
- decals/floating details,
- curve authoring,
- Geometry Nodes authoring,
- procedural material authoring,
- texture packing/mip safety,
- asset variants/randomization,
- automated visual diff,
- reference fidelity levels,
- authoring-to-runtime handoff,
- engine profile schema,
- engine adapter protocol,
- deterministic QA render pattern,
- visual diff script pattern.

Architecture decision:
- modular MD files are canonical,
- `_FULL_LIBRARY.md` is generated from them.


---

## FILE: `README.md`

# BlenderSkill

Canonical knowledge repository for the Blender AI Agent Library.

## Purpose

The repository contains modular Markdown skills for an AI agent that plans, builds, reconstructs, validates and prepares Blender assets for game/VFX pipelines.

The canonical source is the modular library stored in the numbered directories. `_FULL_LIBRARY.md` is generated automatically from the modules listed in `MANIFEST.json` and should not be edited manually.

## Main areas

- `00_governance` — agent rules, routing and state machines
- `01_analysis` — briefs, references, features and measurements
- `02_blender_api` — `bpy`, BMesh, context and automation strategy
- `03_modeling` — hard-surface, topology, UV, trim sheets and authoring workflows
- `04_game_ready` — runtime optimization, materials, LOD, export constraints
- `05_execution` — execution, validation, QA, regression and repair
- `06_prompts` — planner/reviewer/repair prompts
- `07_examples` — examples and benchmarks
- `08_scripts` — reusable audit/validation patterns
- `09_engine` — engine profile and adapter contracts
- `10_reconstruction` — evidence-driven 1:1 reconstruction system
- `11_playbooks` — asset-class production playbooks
- `99_sources` — technical sources

## Repository rules

1. Prefer updating an existing canonical module over creating a parallel skill with duplicated responsibility.
2. Add a new skill only when it introduces a distinct responsibility or reusable primitive.
3. Keep semantic intent separate from temporary Blender indices, UI state and one-off operator sequences.
4. Validate changes against existing modules before merging them into the library.
5. `MANIFEST.json` defines the modules compiled into `_FULL_LIBRARY.md`.
6. GitHub Actions regenerates `_FULL_LIBRARY.md` after canonical Markdown changes.

## Current target

- Blender 5.1.x
- Python automation through Blender API/BMesh where practical
- reconstruction-first and game-asset production workflows
- glTF/GLB as a neutral runtime baseline unless an engine profile overrides it
