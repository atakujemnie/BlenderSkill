# Import-Safe Blender Python Module Pattern

## Purpose

Reusable Blender build/bake/export code must be safe to load for functions without accidentally executing destructive top-level work.

The v0.5 bollard bake exposed two expensive failure classes:
- loading an export script for helper functions also executed the export;
- reusing a collection helper cleared objects that were still needed by the caller.

v0.6 treats module side effects and collection ownership as explicit contracts.

---

# 1. No production side effects on import

Reusable modules may define:
- constants;
- pure helpers;
- builders;
- validators;
- `run()` / `main()` entrypoints.

They must not automatically:
- rebuild the production asset;
- clear collections;
- export files;
- save the blend;
- delete objects;
- run a full bake;

merely because another script imports/executes them for a helper.

Preferred:

```python
def main():
    ...

if __name__ == "__main__":
    result = main()
```

When code is loaded through `exec`/`runpy`, choose the synthetic `__name__` intentionally.

---

# 2. Separate responsibilities

Prefer modules such as:

```text
build_asset.py     -> geometry/material authoring functions
bake_asset.py      -> texture closure
export_asset.py    -> LOD/package/export
qa_asset.py        -> QA cameras/render/validation
```

Shared helpers belong in reusable executors or a side-effect-free helper module.

Do not make `bake_asset.py` import `export_asset.py` if doing so automatically exports.

---

# 3. Collection ownership

A helper that clears a collection must own that collection exclusively.

Do not call:

```text
work_collection()
```

from a nested export helper if `work_collection()` clears the collection that currently contains the LODs being exported.

Use explicit ownership:

```text
ASSET_AUTHORING_COLLECTION
BAKE_SCRATCH_COLLECTION
EXPORT_SCRATCH_COLLECTION
QA_SCRATCH_COLLECTION
```

Scratch helpers may clear only their own scratch namespace.

---

# 4. Destructive helper naming

A function that clears/replaces state must say so in its contract/name/documentation.

Bad:

```python
work_collection()
```

when the function silently clears objects.

Better:

```python
reset_scratch_collection(name)
get_or_create_collection(name)
```

with distinct behavior.

---

# 5. Caller-owned objects

A callee must not delete, unlink or rename caller-owned production objects unless the call contract explicitly transfers ownership.

For temporary mirrored export copies:
- clone source data;
- operate in export scratch collection;
- export clones;
- remove clones;
- restore/leave source unchanged.

Do not mutate the source hierarchy merely to satisfy one export call when a copy can carry the transformation.

---

# 6. Idempotent entrypoints

`main()` / `run()` should:
- identify previous artifacts by stable names/tags;
- update/replace only owned artifacts;
- leave unrelated scene content unchanged;
- return a compact report.

Repeated invocation should not accumulate `.001` copies unless those copies are deliberately versioned artifacts.

---

# 7. Stable part identity

Imported/rebuilt objects may receive Blender suffixes. Never let `.001` change semantic behavior.

Use semantic part IDs/custom properties for:
- UV assignment;
- Feature Contract ownership;
- LOD mapping;
- material routing;
- validation.

Names remain useful for human readability/export conventions but are not sufficient as internal identity.

---

# 8. Validation

Before treating a helper module as reusable:
- load it without calling `main()`;
- assert no production files were written;
- assert production object count did not unexpectedly change;
- assert no source collection was cleared;
- call one helper in a scratch scene/collection;
- run twice and verify idempotent behavior where required.

---

# Compact module contract

```yaml
module:
  path: export_asset.py
  import_safe: true
  top_level_scene_mutation: false
  owned_collections:
    - EXPORT_SCRATCH
  entrypoint: main
  idempotent: true
  status: PASS
```
