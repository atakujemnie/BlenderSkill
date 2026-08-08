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