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