# Procedural Reproducibility and Provenance

## Rule

Procedural variation is allowed; uncontrolled variation is not.

Every generated asset stores at least:

```yaml
generator: builtin_geometry_nodes
generator_version: 5.1.x
seed: 347013
parameters_hash: ...
geometry_signature: ...
semantic_parts: [stem, branches, leaves]
generated_triangle_count: 180000
source_graph_hash: optional
provider_probe_id: ...
```

## Reproduction probe

For a frozen provider version, Blender version, semantic spec and seed:

```text
generate A
-> compact structural signature A
reset disposable generation scope
generate B
-> compact structural signature B
A == B within declared tolerance
```

The signature should not depend on object names or transient datablock IDs. Use topology counts, semantic part counts, bounds, stable sampled landmarks and parameter hashes.

## Variation families

A family uses one semantic base spec and many explicit seeds. Store family ID + member seed. Do not duplicate a random output and lose its generating parameters.

## Manual edits

Manual sculpt/repair after generation changes ownership:
- either promote to a frozen authored asset and record the generator only as provenance;
- or encode the edit back into the procedural spec/generator.

Do not keep editing a random output while claiming it remains reproducible.
