# BlenderSkill

Canonical knowledge repository for the Blender AI Agent Library.

## Current release

**v0.13.0 — deterministic procedural vegetation, generator providers and planter composition.**

v0.13 adds a second authoring domain beside reference reconstruction: procedural organic/environment generation. The first benchmark target is a Lafar planter containing a reconstructed hard-surface container plus generated vegetation.

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
- NodeToPython — preferred node-graph-to-Python compiler when installed and probed; generated Python should normally remove the runtime compiler dependency.

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
