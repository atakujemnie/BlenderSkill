# v0.16 Location Design System Skill Registry

This registry has precedence over the thin v0.15 `LOCATION_DESIGN_SYSTEM_GATE` semantics when v0.16 is active.

| Skill ID | Purpose | Canonical implementation | Maturity |
|---|---|---|---|
| `LOCATION_DESIGN_SYSTEM_BUILD` | create/populate a persistent design system from location/organization references and accepted assets | `14_design_system/401`; prompt 71 | CONTRACT_READY |
| `LOCATION_DESIGN_SYSTEM_RESOLVE` | find existing system or bootstrap its canonical path/layout and return paths | `14_design_system/402`; `executors/design_system_resolver.py` | EXECUTOR_READY |
| `LOCATION_DESIGN_SYSTEM_MANIFEST` | validate the machine-readable design-system contract | `14_design_system/403`; `executors/design_system_manifest.py` | EXECUTOR_READY |
| `DESIGN_SYSTEM_INHERITANCE_RESOLVE` | resolve Universe→Location→Organization→Family→Asset overrides with locked-token protection | `14_design_system/404`; `executors/design_system_inheritance.py` | EXECUTOR_READY |
| `DESIGN_SYSTEM_RESOURCE_PROMOTE` | hash-dedupe and promote reusable textures/logos/decals/components into canonical ownership | `14_design_system/405`; `executors/design_system_resource_registry.py` | EXECUTOR_READY |
| `DESIGN_SYSTEM_MATERIAL_LANGUAGE` | own material families, texture sets and surface-response rules | `14_design_system/406` | CONTRACT_READY |
| `DESIGN_SYSTEM_BRANDING_LIBRARY` | own logo/symbol/wordmark/signage/decal sources and usage rules | `14_design_system/407` | CONTRACT_READY |
| `DESIGN_SYSTEM_COMPONENT_LIBRARY` | own reusable geometry, trim profiles, panels, node groups and Blender assets | `14_design_system/408` | CONTRACT_READY |
| `DESIGN_SYSTEM_FORM_LANGUAGE` | own shape/edge/gap/seam/detail grammar and forbidden forms | `14_design_system/409` | CONTRACT_READY |
| `DESIGN_SYSTEM_ENVIRONMENT_RESPONSE` | own weathering, dirt, wetness and maintenance language | `14_design_system/410` | CONTRACT_READY |
| `DESIGN_SYSTEM_LIGHTING_LANGUAGE` | own emissive/lighting families and semantic roles | `14_design_system/411` | CONTRACT_READY |
| `DESIGN_SYSTEM_ASSET_LIBRARY_BUILD` | package approved resources into a Blender Asset Library `.blend` | `14_design_system/412` | CONTRACT_READY |
| `DESIGN_SYSTEM_CONSUME` | bind one asset task to the resolved location/family resources before surface authoring | `14_design_system/413` | CONTRACT_READY |
| `DESIGN_SYSTEM_CONFORMANCE_GATE` | reject unregistered materials/components/branding/lighting or incompatible form language | `14_design_system/414`; `executors/design_system_conformance.py` | EXECUTOR_READY |
| `DESIGN_SYSTEM_CHANGE_CONTROL` | version tokens/resources and propagate invalidation to dependent assets | `14_design_system/415` | CONTRACT_READY |

## Routing law

```text
known location
-> LOCATION_DESIGN_SYSTEM_RESOLVE
-> DESIGN_SYSTEM_INHERITANCE_RESOLVE
-> consume canonical resources
-> asset construction/reconstruction
-> DESIGN_SYSTEM_CONFORMANCE_GATE
```

If the system is missing, `LOCATION_DESIGN_SYSTEM_BUILD` bootstraps and populates it before final appearance. Blockout geometry may proceed while the system is `BOOTSTRAPPED`; final appearance may not claim closure until the relevant design-system domains are `READY`.
