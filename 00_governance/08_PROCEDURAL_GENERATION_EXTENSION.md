# v0.13 Procedural Generation Extension

## Purpose

v0.13 extends BlenderSkill from reference-driven hard-surface production into deterministic procedural vegetation and environment authoring without weakening the v0.12 reconstruction/integrity gates.

This file is the canonical v0.13 registry/routing amendment. It has precedence for procedural-generation tasks while the existing Shape Graph, mutation, assembly, fidelity and runtime rules remain authoritative for hard-surface owners.

## Fundamental split

A planter with vegetation is not one undifferentiated asset:

```text
PLANTER_CONTAINER
-> existing reconstruction / hard-surface pipeline

VEGETATION_ASSEMBLY
-> procedural provider + botanical grammar + deterministic generation

COMPOSITION
-> soil/root/stem/canopy fit and placement relations

RUNTIME
-> vegetation-specific LOD/cards/attributes + existing game-ready pipeline
```

A correct planter does not prove correct vegetation. A beautiful plant does not prove that it fits the soil volume or is game-ready.

## v0.13 semantic skills

| Skill ID | Purpose | Canonical knowledge | Executor | Maturity |
|---|---|---|---|---|
| `PROCEDURAL_GENERATOR_PROVIDER` | provider compatibility, capability and execution gate | `12_procedural_generation/200`–`201` | `procedural_provider.py` | CONTRACT_READY |
| `NODEGRAPH_TO_PYTHON` | compile a vetted node graph into reproducible Python authoring code | `202` | `nodegraph_codegen_gate.py` | CONTRACT_READY |
| `VEGETATION_BOTANICAL_GRAMMAR` | structural plant specification independent of backend | `211` | `botanical_grammar.py` | CONTRACT_READY |
| `VEGETATION_GENERATE` | deterministic generation acceptance | `210`, `212`, `213` | `vegetation_generation_gate.py` | CONTRACT_READY |
| `VEGETATION_SURFACE_GROWTH` | vines/roots/creepers on host surfaces | `214` | provider-specific adapter | KNOWLEDGE_ONLY |
| `VEGETATION_SCATTER` | deterministic ecological placement over sampled candidates | `215` | `vegetation_scatter.py` | CONTRACT_READY |
| `PLANTER_VEGETATION_COMPOSITION` | rootball/soil/wall/stem fit between vegetation and container | `216` | `planter_composition.py` | CONTRACT_READY |
| `VEGETATION_RUNTIME_PREP` | bridge rich generated plants into runtime budgets | `217`–`219` | `vegetation_runtime_prep.py` | CONTRACT_READY |

## Canonical state flow

```text
PROCEDURAL_REQUEST
-> PROVIDER_DISCOVERY
-> PROVIDER_CAPABILITY_PROBE
-> SPEC_CONSTRAINED
-> GENERATION_READY
-> GENERATED_UNVERIFIED
-> botanical / placement / composition proof
-> VEGETATION_GENERATION_GATE
-> AUTHORING_ACCEPTED
-> VEGETATION_RUNTIME_PREP
-> existing UV/bake/package/export/runtime gates
```

No provider probe means no production call to a third-party generator.

## Provider law

Third-party generators are adapters, not the semantic API. Agent-facing requests use stable specs such as `PlantSpec`, `ScatterSpec` and `RuntimeVegetationSpec`. Backend names never become the asset contract.

Every provider records:
- provider/version;
- Blender min/max known compatibility;
- execution type;
- background/UI requirements;
- deterministic seed support;
- input/output schema;
- license and asset-license boundary;
- probe artifact;
- cleanup/postcondition contract.

`AVAILABLE` is a runtime fact, not a documentation assumption.

## Preferred v0.13 providers

1. Built-in Blender 5.1 Geometry Nodes — primary runtime-safe procedural backend.
2. NodeToPython — preferred node-graph compiler when installed and probed; generated code should not require it at runtime.
3. Python-authored Geometry Nodes (`geonodes`) — optional provider after capability/license probe.
4. Sapling / IvyGen — optional domain providers after Blender 5.1 operator probe.
5. Sverchok — optional parametric provider after local probe.
6. engon/botaniq — optional licensed asset/scatter provider; asset-pack license remains external.
7. Infinigen / ProcFunc / BlenderProc — source/reference patterns unless current runtime compatibility is independently proven.
8. The Grove — version-blocked for Blender 5.1 under the currently documented Blender 4.2–4.4 support window.

## Reproducibility law

A procedural asset must preserve:

```text
provider_id
provider_version
seed
parameters_hash
source/nodegraph hash when applicable
generation geometry signature
semantic part IDs
```

Fixed seed + fixed parameters must reproduce the same structural signature within the declared tolerance. Otherwise the asset is `UNVERIFIED`.

## Game-ready law

High-quality generated geometry may be an authoring artifact only.

```text
VEGETATION_GENERATE PASS
!=
VEGETATION_RUNTIME_PREP PASS
```

Runtime prep owns LOD budgets, leaf cards/impostors, instancing, material-slot budget, collision policy, wind attributes and export survival.

## Benchmark

Canonical v0.13 benchmark: `07_examples/82_LAFAR_PLANTER_VEGETATION_V013_BENCHMARK.md`.
