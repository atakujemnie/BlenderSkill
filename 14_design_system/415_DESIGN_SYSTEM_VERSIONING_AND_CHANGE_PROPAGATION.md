# Design System Versioning and Change Propagation

## Version ownership

`design_system_version` is independent from BlenderSkill version and individual asset version.

Increment it when canonical identity/resources change in a way that may affect dependent assets, for example:
- replacing a material family's source textures;
- changing a locked brand color;
- changing primary logo geometry;
- changing canonical component dimensions/interface;
- changing edge/seam family rules;
- changing weathering/lighting identity.

Adding a purely new unused optional resource can remain compatible when explicitly classified additive.

## Dependency record

Every consuming asset should record:

```text
design_system_path
design_system_version
resolved_layers
resource_ids
waivers
```

## Change impact

```text
design-system change
-> identify changed semantic IDs/paths
-> find dependent assets/locations
-> classify impact: NONE / REVALIDATE / REBAKE / REBUILD
-> invalidate only affected evidence/runtime stages
```

Examples:
- new logo bitmap for same geometry/color: revalidate branding/bake;
- changed trim profile dimensions: dependent geometry may require rebuild;
- changed roughness texture: retexture/rebake, geometry remains valid;
- changed weathering profile: appearance revalidation, not Shape Graph rebuild.

## No silent mutation

Do not overwrite a canonical resource file with materially different content while keeping the same version/evidence as if nothing changed. Hash conflicts are design-system changes.
