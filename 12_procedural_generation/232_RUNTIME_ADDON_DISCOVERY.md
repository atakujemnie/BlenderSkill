# Blender Runtime Add-on Discovery

## Purpose

Discover what the active Blender process can actually see before provider selection.

## Evidence order

```text
Blender version
-> enabled add-on module IDs
-> discoverable add-on/extension modules
-> imported module metadata
-> registered Asset Libraries
-> known built-in backends
-> normalized provider inventory
```

Use Blender preferences as runtime evidence. Extension module names may differ from display names, so matching must use normalized module ID + display name + aliases rather than one hard-coded package string.

## Required states

- `DISCOVERED_ENABLED`
- `DISCOVERED_DISABLED`
- `NOT_DISCOVERED`
- `METADATA_PARTIAL`

Discovery is not an execution probe. A discovered provider still routes to its capability probe before production use.

## Mandatory mismatch behavior

If the user/project supplied an expected installed provider list and runtime discovery does not contain one of those providers:

```text
EXPECTED_PROVIDER_GATE = FAIL
```

Do not silently interpret that mismatch as `provider unavailable` and fall back. Report the mismatch because it usually means discovery logic, extension namespace handling, or the wrong Blender profile/process is being inspected.

## Asset Libraries

Registered Asset Libraries are inventoried separately from add-ons. An empty Asset Library list means only `READY_ASSET_SOURCE` is empty. It says nothing about Sapling, IvyGen, Sverchok, Geometry Nodes, external generators, or utilities.