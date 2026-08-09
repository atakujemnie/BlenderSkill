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
    location_material_library_root: <repo>/Assets/GameAssets/Materials/Locations
    location_material_library_pattern: <repo>/Assets/GameAssets/Materials/Locations/<location_id>

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
- resolve/create the location material library under `<repo>/Assets/GameAssets/Materials/Locations/<location_id>` and return that path to the user;
- reuse compatible location material families before generating new texture sets;
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
