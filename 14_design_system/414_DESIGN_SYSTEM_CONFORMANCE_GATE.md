# Design System Conformance Gate

## Purpose

Prove that an asset belongs to the resolved location/organization/family language. This gate is separate from reference fidelity: an asset can match its concept while still fragmenting the wider location system.

## Required evidence

Depending on the asset:
- material family IDs;
- component source IDs;
- branding resource IDs;
- lighting/emissive family IDs;
- weathering profile ID;
- shape/edge family IDs;
- declared one-off additions and waivers.

## Hard failures

```text
unregistered one-off material without waiver
unregistered shared component without waiver
redrawn/unregistered branding when canonical branding applies
foreign lighting/accent family
foreign locked shape/edge identity
reuse ratio below an explicit family target
```

## Non-compensating

A correct logo cannot compensate for wrong materials. High geometric fidelity cannot compensate for a foreign brand color or unregistered material family.

## Reuse ratio

Diagnostic metric:

```text
canonical referenced resources / all design-system resource references
```

It is not a universal quality score. Use a minimum only when the asset family is expected to reuse standardized resources.

## Waivers

Waivers are explicit semantic keys, for example:

```text
material:MAT_SPECIAL_MEDICAL_GLASS
component:CMP_UNIQUE_HERO_SCANNER
```

A waiver documents a legitimate exception; it does not automatically promote the resource into the shared system.

Canonical executor: `executors/design_system_conformance.py`.
