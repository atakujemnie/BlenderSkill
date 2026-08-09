# Installed Provider Inventory

## Purpose

Inventory the active Blender environment before selecting a procedural provider.

The inventory is runtime evidence, not a documentation guess.

## Required source buckets

```text
READY_ASSET_SOURCE
PROCEDURAL_GENERATOR
EXTERNAL_GENERATOR
UTILITY
BUILTIN_BACKEND
```

A registered Blender Asset Library is a `READY_ASSET_SOURCE` candidate. Sapling/IvyGen/Sverchok are not asset libraries; they remain visible as procedural generators.

## Required provider fields

```yaml
provider_id: sapling_tree_gen
display_name: Sapling Tree Gen
module_name: ...
version: 0.3.7
source_kind: PROCEDURAL_GENERATOR
enabled: true
discovered: true
runtime_probe_status: PROBE_REQUIRED
domains: [TREE, WOODY_PLANT]
```

## Required inventory summary

```yaml
ready_asset_sources_count: 0
procedural_generators_count: 4
external_generators_count: 1
utilities_count: 3
builtin_backends_count: 1
```

The summary must never compress these counts into a generic statement such as `no libraries/providers`.

## Runtime sources

The Blender-side collector should inspect at least:
- enabled add-on module IDs in Blender Preferences;
- discoverable add-on/extension modules and their metadata where available;
- registered Asset Library names and paths;
- built-in Blender procedural backends relevant to the task.

Missing metadata is `UNKNOWN`, not proof of absence.