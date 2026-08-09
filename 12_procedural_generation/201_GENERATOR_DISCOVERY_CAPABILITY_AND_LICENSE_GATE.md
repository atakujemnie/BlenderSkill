# Generator Discovery, Capability and License Gate

## Purpose

Bind documented provider claims to the actual Blender 5.1 runtime before production use.

## Probe sequence

```text
module/extension present?
-> exact version/readback
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
- `PROBE_REQUIRED` — documentation suggests compatibility but current runtime was not tested.
- `SOURCE_ONLY` — study/reference only; never called as a BlenderSkill runtime dependency.

## v0.13 provider policy

- NodeToPython: documented Blender 4.2–5.1 support; still probe the installed version.
- Sverchok: project README declares Blender 5.1; still probe requested nodes/API.
- Sapling, IvyGen, A.N.T. Landscape and Archimesh: discoverable Blender extensions; exact 5.1 call surface is probe-required.
- engon/botaniq: code compatibility is not an asset license; use only user-provided licensed packs and probe Blender 5.1.
- The Grove: current documentation lists Blender 4.2/4.3/4.4, therefore 5.1 is blocked until new evidence overrides this record.
- ProcFunc: current package pins `bpy==4.2.0`/Python 3.11; source pattern only for the 5.1 runtime.
- BlenderProc 2.8.0: based on Blender 4.2.1; source/external-worker pattern, not in-process 5.1 dependency.
- Infinigen: algorithm/reference source; do not import the full framework merely to obtain one generator.

## License gate

Record code license and, separately, generated/asset-pack license. Unknown license blocks vendoring/copying. Merely calling a locally installed provider may be allowed by project policy, but redistribution is a separate decision.

## Catalog

`executors/procedural_provider_catalog.py` stores dated discovery hints. They are not a substitute for runtime probe.
