# RPG Project Asset Pipeline Profile

## Scope

Verified project profile extracted from the Lafar/Astera civic-asset pipeline benchmark.

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

  evidence:
    - Lafar Civic Bollard final runtime integration benchmark
    - engine loader resolved assets from RPG_ENGINE_ASSET_DIRECTORY/Assets
    - ModelTests successfully loaded the Astera bollard after export moved to Assets/GameAssets
    - wrong sibling root <repo>/GameAssets produced runtime load failure
```

## Required use

When this profile matches the active project:
- do not rediscover the runtime root with `ls/find` before every asset;
- do not write to `<repo>/GameAssets`;
- inject the resolved runtime root into bake/decal/export stages;
- package the LOD family into one glTF module using `_LOD0.._LODn` node naming;
- use the existing `ModelTests` infrastructure for engine-loader regression where appropriate;
- capture `ModelTests.exe` exit status directly;
- do not claim Level D from Blender glTF import alone.

## Handedness caution

`MIRROR_X` is a project/runtime packaging fact observed in the current pipeline. Reverify if the engine importer or coordinate conversion changes. Prefer readable asymmetric details as proof.

## Profile freshness

This is a project-specific optimization layer, not a universal Blender rule.

Invalidate/reverify affected fields after changes to:
- CMake asset-directory definitions;
- engine loader root configuration;
- glTF importer handedness;
- LOD grouping parser;
- catalog layout;
- test/build directory layout.