# Location Design System Contract

## v0.16 precedence

This v0.15 location-assembly contract remains the integration point, but the full persistent design-system authority now lives in:

- `00_governance/11_LOCATION_DESIGN_SYSTEM_EXTENSION.md`;
- `00_governance/12_LOCATION_DESIGN_SYSTEM_SKILL_REGISTRY_V016.md`;
- `14_design_system/400_LOCATION_DESIGN_SYSTEM_LAYER_INDEX.md` and modules `401`–`415`.

## Location-assembly requirement

One location owns one persistent design language. Individual assets consume it instead of inventing local styles.

For location assembly:

```text
LOCATION_DESIGN_SYSTEM_RESOLVE
-> DESIGN_SYSTEM_INHERITANCE_RESOLVE
-> resolved material/form/branding/component/light/weathering context
-> location asset population
```

The v0.14 persistent runtime material library remains linked from the source design system.

Final location art direction requires a READY resolved design system and conformance of required asset families. An incompatible one-off material/component/branding treatment is a design-system violation unless explicitly waived.

Canonical source-side root for the RPG profile defaults to:

```text
<repo>/Blender/DesignSystems/<location_id>/
```

Canonical resolver: `executors/design_system_resolver.py`.
Canonical final manifest validator: `executors/design_system_manifest.py`.
Canonical asset conformance validator: `executors/design_system_conformance.py`.
