# Node Graph to Python Codegen

## Purpose

Turn a vetted Geometry Nodes/Shader/Compositor graph into deterministic, reviewable Python authoring code without making the compiler a runtime dependency.

Preferred v0.13 compiler when available: NodeToPython. Python-first Geometry Nodes libraries may be used as an alternative authoring route after provider probe.

## Canonical flow

```text
approved node graph
-> freeze source tree ID + hash
-> provider capability probe
-> compile/export Python
-> import-safe cleanup
-> regenerate node tree in clean scene
-> structural round-trip comparison
-> NODEGRAPH_TO_PYTHON gate
-> store generated Python + provenance
```

## Required provenance

```yaml
source_node_tree_id: GN_LAFAR_GROUND_COVER
source_node_tree_hash: ...
compiler_provider_id: nodetopython
compiler_provider_version: ...
blender_version: 5.1.x
generated_script_hash: ...
compiler_probe_status: PASS
roundtrip_probe_status: PASS
requires_runtime_compiler_dependency: false
provenance_id: codegen:...
```

## Anti-lock-in rule

The asset contract is the semantic inputs/outputs and generated graph behavior, not the compiler add-on. Prefer committed generated code that can reconstruct the graph with Blender Python alone.

## Recompile trigger

Recompile when source node tree hash changes, Blender/node API changes, or a round-trip probe fails. Do not hand-edit generated code and then pretend it still corresponds to the old source hash.

## Executor

`executors/nodegraph_codegen_gate.py`.
