# Generator Discovery, Capability and License Gate

## Purpose

Bind provider identity and documented claims to the actual Blender 5.1 runtime before production use.

v0.17 separates ready Asset Libraries from procedural generators. An empty Asset Library inventory must never be interpreted as an empty provider inventory.

## Mandatory pre-probe discovery

```text
BLENDER_RUNTIME_ADDON_DISCOVERY
-> INSTALLED_PROVIDER_DISCOVERY
-> EXPECTED_PROVIDER_GATE when user/project supplied expected providers
-> provider-specific capability probes
-> PROVIDER_SELECTION_REPORT
```

## Probe sequence

```text
module/extension discovered?
-> enabled state + exact version/readback where available
-> expected operator/API symbol present?
-> operator poll/context requirements
-> minimal disposable generation
-> deterministic seed smoke test where applicable
-> output type/semantic parts
-> cleanup succeeds
-> compact probe artifact
```

## Statuses

- `PASS` — compatible and capability-complete for the requested route.
- `BLOCKED` — known incompatible version, missing capability, failed probe, license policy failure.
- `PROBE_REQUIRED` — discovered/documented but current execution capability was not tested.
- `SOURCE_ONLY` — study/reference only; never called as a BlenderSkill runtime dependency.
- `DISCOVERY_MISMATCH` — user/project says a provider is installed but normalized runtime discovery omitted it; fix discovery before fallback.

## Provider policy

- Blender Geometry Nodes: built-in procedural backend; still validate requested nodes/API where version-sensitive.
- Sapling Tree Gen: tree/woody-plant generator; discover and probe explicitly.
- IvyGen: vine/surface-growth generator; discover and probe explicitly.
- A.N.T. Landscape: terrain generator, not a vegetation asset library.
- Sverchok: parametric/generic procedural generator; discover and probe requested API.
- MPFB: character generator; report it but do not route it as vegetation.
- Meshy official plugin: external 3D generator/service adapter; report separately from local asset libraries.
- Geo Nodes Guide and MCP: utilities/integration tools; keep visible in inventory without pretending they are content libraries.
- engon/botaniq: ready asset/scatter source only when actually installed/licensed and discovered; code and asset licenses are separate.
- NodeToPython: optional reference/development tool, not a required BlenderSkill 5.1 runtime dependency.
- The Grove, ProcFunc, BlenderProc and Infinigen retain their version/license/source-only restrictions from the provider catalog.

## License gate

Record code license and, separately, generated/asset-pack/service-output license. Unknown redistribution rights block vendoring/copying. Merely calling a locally installed provider and redistributing its assets are separate decisions.

## Catalog

`executors/procedural_provider_catalog.py` stores dated identity/capability hints. They are not a substitute for runtime discovery or execution probe.