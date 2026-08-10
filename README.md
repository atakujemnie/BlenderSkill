# BlenderSkill

Canonical knowledge repository for the Blender AI Agent Library.

## Current release

**v0.18.0 — Runtime Verification & Contract Convergence.**

v0.13 adds a second authoring domain beside reference reconstruction: procedural organic/environment generation. The first benchmark target is a Lafar planter containing a reconstructed hard-surface container plus generated vegetation.


## v0.18 Runtime Verification & Contract Convergence

v0.18 moves BlenderSkill from documented provider behavior to executable runtime evidence. Provider states and metadata are canonicalized, discovery is non-executing, capability probes are explicit and cleanup-verified, version constraints replace exact-only gating, and provider selection preserves discovery/probe/domain/compatibility/license/quality evidence independently.

Normal CI is read-only. A separate pinned Blender 5.1.x workflow proves runtime discovery and a real Geometry Nodes evaluation. `MANIFEST.json` uses schema v2, `_RUNTIME_INDEX.json` is the compact routing entry point, and release tagging is isolated to the manual release workflow.

Canonical regression: **Benchmark 87 — Lafar Runtime Capability Probe v0.18**.

## v0.17 runtime provider discovery and selection transparency

v0.17 fixes the provider-discovery failure exposed by the Lafar planter workflow. BlenderSkill no longer treats an empty ready-made vegetation Asset Library as proof that no procedural providers are installed.

```text
active Blender runtime
-> installed/enabled add-on + Asset Library discovery
-> normalized source buckets
-> expected-provider mismatch gate when user/project supplied known installations
-> provider-specific execution probe
-> requested-domain + quality suitability
-> mandatory provider selection report
-> selected backend or explicit BLOCKED
```

The inventory distinguishes `READY_ASSET_SOURCE`, `PROCEDURAL_GENERATOR`, `EXTERNAL_GENERATOR`, `UTILITY` and `BUILTIN_BACKEND`. Relevant discovered providers remain visible even when rejected. A custom fallback is illegal when an expected installed provider disappeared from discovery.

Canonical regression: **Benchmark 86 — Lafar Provider Discovery v0.17**.

## v0.16 persistent Location Design Systems

v0.16 promotes the thin v0.15 Location Design System requirement into a persistent reusable authoring layer. Future assets resolve one canonical location/faction/family language before final appearance instead of recreating materials, logos, components and style rules per asset.

```text
<repo>/Blender/DesignSystems/<location_id>/
-> LOCATION_DESIGN_SYSTEM.md + design_system.json
-> source/provenance registry
-> materials + branding + components + decals + profiles + nodegroups
-> optional canonical Blender Asset Library .blend
-> inheritance: LOCATION -> ORGANIZATION -> FAMILY -> ASSET
-> asset consumption
-> DESIGN_SYSTEM_CONFORMANCE_GATE
```

The v0.14 runtime material library remains linked but separate under `Assets/GameAssets/Materials/Locations/<location_id>`. Canonical resources can be hash-deduplicated/promoted from accepted assets, and future asset prompts receive exact reusable paths rather than regenerating the same visual language.

Canonical regression: **Benchmark 85 — Lafar Location Design System v0.16**.

## v0.15 location reconstruction and environment assembly

v0.15 introduces the hierarchy above single-asset reconstruction. Complete authored interiors/exteriors are now planned and validated as spatial systems rather than as independent object builds.

```text
location references
-> Location Design System
-> Location Scene Graph + Asset Manifest
-> architecture
-> HERO anchors
-> fixed assets
-> furniture clusters
-> spatial relations + circulation/clearance
-> lighting/vegetation/props
-> reference composition fidelity
-> Location Completeness Gate
-> runtime partitioning/instancing
```

Hard final blockers include missing required HERO assets, final proxies, unintended interpenetration, blocked required circulation and failed reference composition. The canonical v0.15 regression is **Benchmark 84 — Lafar Restaurant Full Location Reconstruction**.

## v0.14 quality/material additions

v0.14 keeps the v0.13 deterministic vegetation contracts but adds a production-quality barrier before runtime finishing:

```text
location material library find-or-create
-> installed asset/provider discovery
-> runtime probe
-> quality-tier selection
-> physical composition
-> planting massing/composition quality
-> reference composition fidelity when applicable
-> shared material-language reuse/adaptation
-> early visual-quality barrier
-> runtime finishing
-> context-budget gate
```

For the RPG profile, location material language defaults to:
`<repo>/Assets/GameAssets/Materials/Locations/<location_id>/`.
Every material task must return the resolved path. Existing compatible families are reused before any new texture generation; new approved families are written back to the same location library.

Provider compatibility and provider quality are separate. A runtime-safe C-tier procedural generator cannot displace an installed A-tier source for a HERO asset merely because it is available first.

The v0.14 Lafar regression target reduces the previous approximately 80k-token three-planter run to <=30k tokens (stretch <=20k) by moving reusable probing, selection, material-library and composition logic into canonical executors.

The new boundary is:

```text
can create/scatter procedural geometry
!=
understands plant structure
!=
proves deterministic generation
!=
proves a game-ready vegetation asset
```

Existing v0.12 hard-surface reconstruction and geometric-integrity rules remain authoritative for the planter/container and other manufactured geometry.

## Canonical v0.13 planter pipeline

```text
PLANTER_CONTAINER
-> existing Shape/Appearance/Geometric Integrity pipeline
-> expose usable soil footprint/depth

VEGETATION_ASSEMBLY
-> PROCEDURAL_GENERATOR_PROVIDER discovery/probe
-> PlantSpec / VEGETATION_BOTANICAL_GRAMMAR
-> deterministic generation
-> fixed-seed reproduction proof
-> VEGETATION_GENERATION_GATE

COMPOSITION
-> PLANTER_VEGETATION_COMPOSITION
-> rootball/soil/wall/stem constraints

RUNTIME
-> VEGETATION_RUNTIME_PREP
-> LOD / leaf-card / impostor strategy
-> wind/runtime attributes
-> existing UV/bake/package/export/runtime gates
```

## Procedural provider architecture

Third-party generators are adapters, not agent-facing semantics. BlenderSkill requests a stable `PlantSpec`, `ScatterSpec` or runtime vegetation contract; a provider translates that request into its own API only after a capability probe.

Every provider records:
- provider/version;
- Blender compatibility window known by current evidence;
- execution type;
- UI/background requirements;
- deterministic seed capability;
- input/output capabilities;
- code and asset-license boundaries;
- isolated runtime probe;
- output/postcondition validation.

Canonical status is runtime-derived:

```text
AVAILABLE
BLOCKED
PROBE_REQUIRED
SOURCE_ONLY
```

Documentation alone never authorizes a production call.

## v0.13 provider policy

### Primary

- Blender 5.1 Geometry Nodes — primary built-in procedural backend.
- NodeToPython — optional reference/development tool only; it is not a required BlenderSkill 5.1 runtime dependency.

### Optional after probe

- `geonodes` — Python-first Geometry Nodes authoring;
- Sapling Tree Gen — tree backend;
- IvyGen — surface-growth backend;
- Sverchok — parametric/computational geometry;
- A.N.T. Landscape — future terrain backend;
- Archimesh — future structural blockout backend;
- engon/botaniq — optional licensed asset/scatter provider.

### Source/reference only or version-blocked

- Infinigen — algorithm and procedural-architecture source;
- ProcFunc — function-oriented generation source pattern;
- BlenderProc — physics-aware placement/source or external-worker pattern;
- The Grove — high-quality tree/growth architecture, currently version-blocked for the BlenderSkill 5.1 runtime until compatible evidence exists.

Provider facts are stored in `99_sources/PROCEDURAL_GENERATION_SOURCES.md` and `executors/procedural_provider_catalog.py`; the active runtime probe always has priority.

## Botanical grammar

`VEGETATION_BOTANICAL_GRAMMAR` gives the agent plant semantics independent of backend:

```text
stem/trunk
branch hierarchy
internodes/nodes
branch angle + taper
phyllotaxis
crown envelope + density
apical dominance
tropism
age/season
root/contact datum
```

Supported structural form classes include:

```text
TREE
SHRUB
HERBACEOUS
GRASS
ROSETTE
REED
VINE
GROUND_COVER
ALIEN_BRANCHING
```

Lafar flora can deliberately violate terrestrial proportions, but deviations remain explicit grammar rather than arbitrary random geometry.

## Deterministic generation

Every procedural source asset preserves at least:

```text
provider_id
provider_version
seed
parameters_hash
source/nodegraph hash when applicable
geometry_signature
semantic part IDs
```

A fixed provider version + Blender version + semantic spec + seed must reproduce the same compact structural signature within declared tolerance. Otherwise generation remains `UNVERIFIED`.

Morphology seed and spatial scatter seed should normally be separate so layout changes do not silently regenerate plant morphology.

## Vegetation scatter

`VEGETATION_SCATTER` treats scatter as constrained deterministic placement rather than random duplication.

It can consume pre-sampled candidates carrying:
- biome weight;
- slope;
- exclusions;
- position;
- clustering/proximity metadata;
- stable candidate ID.

The pure-Python executor deterministically selects a valid subset from those candidates. Blender/Geometry Nodes remains responsible for surface sampling and actual instance placement.

## Planter composition

The planter/plant boundary is a separate physical owner.

Initial hard constraints:

```text
rootball inside usable soil footprint
rootball depth <= usable soil depth
stem does not intersect planter wall
root/contact datum meets soil surface
minimum required plant spacing survives
```

Canopy overlap may be legal or desirable. Root/stem/container conflicts cannot be hidden by soil or foliage.

## Vegetation runtime preparation

```text
VEGETATION_GENERATION_GATE PASS
!=
VEGETATION_RUNTIME_PREP PASS
```

Runtime preparation owns:
- triangle budgets by usage class/LOD;
- foliage reduction and leaf cards;
- optional whole-plant impostors;
- instancing strategy;
- material-slot/atlas strategy;
- collision policy;
- wind semantic attributes;
- package/export survival.

The v0.13 benchmark starts with MID source-plant targets of 30k / 14k / 5k / 1.2k triangles for LOD0–LOD3 and at most 3 material slots unless a project profile overrides them. These values are policy defaults, not engine invariants.

## Node graph compilation

`NODEGRAPH_TO_PYTHON` supports a compiler workflow:

```text
vetted Geometry Nodes graph
-> freeze graph/hash
-> compiler provider probe
-> generate Python
-> import-safe cleanup
-> reconstruct graph in clean scene
-> structural round-trip proof
-> store generated Python + provenance
```

The generated artifact is preferred over a permanent compiler dependency when practical.

## New v0.13 semantic skills

- `PROCEDURAL_GENERATOR_PROVIDER`;
- `NODEGRAPH_TO_PYTHON`;
- `VEGETATION_BOTANICAL_GRAMMAR`;
- `VEGETATION_GENERATE`;
- `VEGETATION_SURFACE_GROWTH`;
- `VEGETATION_SCATTER`;
- `PLANTER_VEGETATION_COMPOSITION`;
- `VEGETATION_RUNTIME_PREP`.

New decision executors:
- `procedural_provider.py`;
- `procedural_provider_catalog.py`;
- `nodegraph_codegen_gate.py`;
- `botanical_grammar.py`;
- `vegetation_generation_gate.py`;
- `vegetation_scatter.py`;
- `planter_composition.py`;
- `vegetation_runtime_prep.py`.

These remain `CONTRACT_READY` until the Lafar planter/vegetation Blender 5.1 benchmark proves end-to-end runtime maturity.

## v0.12 foundations retained

Reference-driven manufactured assets still use:

```text
Shape Graph
-> EXECUTION_AUTHORIZATION_GATE
-> one-node mutation
-> MUTATION_POSTCONDITION_GATE
-> ASSEMBLY_INTEGRITY_GATE
-> RECONSTRUCTION_NODE_GATE
-> GEOMETRIC_INTEGRITY_GATE
-> APPEARANCE_FIDELITY_GATE when required
-> RECON_FIDELITY_GATE
```

A procedural plant does not weaken these gates for its planter, support structure or other hard-surface hosts.

## Canonical benchmark

`07_examples/82_LAFAR_PLANTER_VEGETATION_V013_BENCHMARK.md`

Regression targets include:
- zero guessed third-party operator signatures;
- zero unseeded production vegetation;
- zero fixed-seed reproduction mismatches;
- zero planter-wall/root/stem physical violations;
- zero runtime claims directly from raw high-poly generator output;
- zero lost provider/seed/provenance metadata.

## Repository structure

- `00_governance` — state, routing, semantic skills, completion
- `01_analysis` — briefs, references, measurements
- `02_blender_api` — Blender 5.1 API/runtime rules
- `03_modeling` — hard-surface/topology/UV/Geometry Nodes authoring
- `04_game_ready` — LOD/collision/bake/export/runtime contracts
- `05_execution` — authorization, postconditions, integrity and fidelity gates
- `06_prompts` — planner/reviewer/repair prompts
- `07_examples` — benchmark and regression post-mortems
- `08_scripts` — reusable validation patterns
- `09_engine` — project/runtime profiles and engine proof
- `10_reconstruction` — evidence-driven 1:1 reconstruction
- `11_playbooks` — asset-class production playbooks
- `12_procedural_generation` — providers, vegetation grammar, scatter, composition and runtime preparation
- `executors` — reusable Python decision/execution components
- `99_sources` — technical and provider research sources

## Canonical source

Modular Markdown files listed in `MANIFEST.json` are canonical. `_FULL_LIBRARY.md` is generated from the manifest and must not be edited manually.
