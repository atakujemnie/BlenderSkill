# Blender 5.1 Runtime Compatibility Matrix

## Purpose

The library targets Blender 5.1.x, but agents must still **discover actual runtime capabilities** instead of assuming an enum/property/operator name from memory.

This module records compatibility lessons observed in real agent execution and converts them into guarded patterns.

Each item is tagged:
- `OBSERVED_RUNTIME` — encountered during a Blender 5.1 project run;
- `GENERAL_GUARD` — safe automation rule independent of a specific build;
- `FUTURE_DEPRECATION` — current API worked but runtime emitted a deprecation warning.

---

## Render engine enum

### Observed
`OBSERVED_RUNTIME`

A run that assumed:

```python
scene.render.engine = "BLENDER_EEVEE_NEXT"
```

failed because that enum was not exposed by the connected Blender 5.1 build.

### Rule

Never hardcode one expected EEVEE identifier without discovery.

```python
engines = scene.render.bl_rna.properties["engine"].enum_items.keys()
for wanted in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
    if wanted in engines:
        scene.render.engine = wanted
        break
```

The actual selected engine must be included in QA metadata.

---

## Auto Smooth assumptions

### Observed
`OBSERVED_RUNTIME`

Legacy scripts that expect a `use_auto_smooth` mesh flag are not a safe compatibility strategy for the target runtime.

### Rule

Do not use the existence of `use_auto_smooth` as a required precondition.

Prefer explicit shading intent:
- polygon smooth state;
- sharp-edge marking where required;
- normal/shading workflow appropriate to the target mesh;
- runtime feature discovery when an API property is version-sensitive.

If a script depends on a version-sensitive property, wrap it in `hasattr()` and provide a fallback.

---

## Material node activation

### Observed
`FUTURE_DEPRECATION`

The target runtime accepted `Material.use_nodes`, but emitted a warning that the property is expected to be removed in Blender 6.0.

### Rule

Do not scatter direct `mat.use_nodes = True` assumptions throughout generated asset scripts.

Centralize material-node initialization in a compatibility helper.

Preferred behavior:
1. inspect whether a usable node tree already exists;
2. use the target-version mechanism only when required;
3. keep future-version compatibility isolated to one helper;
4. record deprecation warnings but do not treat a future warning as a current execution failure.

---

## Unsaved `.blend` path

### Observed
`OBSERVED_RUNTIME`

In a fresh unsaved Blender session:

```python
bpy.data.filepath == ""
```

A generated decal script derived the project root from that empty value and wrote output to an unintended `C:\GameAssets` location.

### Rule

Never use `bpy.data.filepath` as the sole project-root anchor.

Path precedence:

```text
active Project Asset Pipeline Profile
> explicit task/project root
> script __file__ anchor
> saved blend path
> cwd only as last controlled fallback
```

Before writing files outside the temporary QA directory, validate that the resolved root contains an expected project marker.

---

## Viewport visibility vs render visibility

### Observed
`OBSERVED_RUNTIME`

A default Cube was hidden in the viewport but still rendered and completely obscured a QA render.

### Rule

`hide_viewport` and `hide_render` are separate states.

QA isolation must:
- preserve original render visibility;
- hide non-QA/non-asset scene objects only for the render transaction;
- restore every saved state in `finally`;
- never delete unrelated user objects to clean a QA frame.

Use the reusable QA isolation helper when available.

---

## Importing/executing builder scripts

### Observed
`OBSERVED_RUNTIME`

A LOD/export script executed the build script only to access helper functions, but the build file contained an unconditional top-level:

```python
BUILD_REPORT = build()
```

This cleared the asset collection and deleted freshly created decal plates.

### Rule

Reusable build modules must not mutate the production scene on import.

Use:

```python
if __name__ == "__main__":
    BUILD_REPORT = build()
```

or expose an explicit callable entry point.

Import/namespace loading must be side-effect free unless the semantic executor contract explicitly says otherwise.

---

## Function default capture

### Observed
`OBSERVED_RUNTIME`

A parametric LOD generator changed a global segment count, but a function defined as:

```python
def lathe(..., segs=SEG):
```

had already captured the old value at definition time.

### Rule

Runtime-configurable defaults must not be captured from mutable global configuration.

Use:

```python
def lathe(..., segs=None):
    if segs is None:
        segs = CURRENT_CONFIG.segments
```

or pass the value explicitly.

---

# Capability preflight

Before generated code uses a version-sensitive API, inspect and persist:

```yaml
blender_compat:
  version: [5, 1, x]
  render_engines: []
  material_node_api: DISCOVERED
  shading_api: DISCOVERED
  export_gltf_available: true
  blend_saved: false
  project_root_source: PROJECT_PROFILE
```

Do this once per session unless the runtime changes.

---

# Rule for future versions

This is not a promise that Blender 5.2/6.x behaves identically.

When the runtime version differs from the library target:
- mark compatibility `UNVERIFIED`;
- discover relevant RNA/enums;
- test on a temporary object/scene;
- record the new compatibility fact before production mutation.
