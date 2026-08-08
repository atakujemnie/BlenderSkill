# Blender Image Datablock Cache Coherence

## Purpose

An external texture file changing on disk does **not** imply that an existing `bpy.data.images` datablock now contains the new pixels.

This is a silent failure class: filename, filepath, node binding and material graph can all look correct while Blender renders an older in-memory version.

## Core rule

```text
DISK ARTIFACT FRESHNESS != BLENDER IMAGE DATABLOCK FRESHNESS
```

When the pipeline declares the saved texture file authoritative, runtime material assembly must explicitly synchronize the Blender image datablock before QA.

## Authority states

Every image artifact should declare one state:

```text
GENERATED_IN_MEMORY_AUTHORITATIVE
DISK_FILE_AUTHORITATIVE
PACKED_BLEND_AUTHORITATIVE
UNRESOLVED
```

Do not call `reload()` blindly on an image that has unsaved authoritative in-memory edits.

## Disk-authoritative reload

For a baked texture that has already been saved externally:

```python
img = bpy.data.images.get(expected_name)
if img is None:
    img = bpy.data.images.load(path)
else:
    img.filepath = path
    img.reload()
```

Then verify:
- resolved absolute filepath points to the expected artifact;
- image dimensions are non-zero and expected;
- colorspace matches the channel contract;
- compact pixel/image statistics match the accepted bake artifact.

Prefer matching by canonical filepath/artifact ID rather than basename alone when duplicate filenames can exist.

## Runtime-material binding gate

Before a baked-runtime render:

```text
accepted disk bake
-> synchronize image datablock
-> verify material node binding
-> verify UV contract
-> render runtime material
```

Do not jump from `file exists` directly to runtime QA.

## Diagnostic order when disk maps look correct but runtime render is wrong

Use this order to avoid expensive false leads:

```text
1. disk artifact validator
2. in-memory image freshness / filepath
3. material node -> image binding
4. colorspace/channel wiring
5. UV contract on consuming mesh
6. shader/runtime interpretation
```

If disk validation passes but in-memory statistics differ, classify:

```text
STALE_IMAGE_DATABLOCK
```

Do not rebuild UVs or rebake channels until cache coherence is resolved.

## Freshness evidence

Useful compact evidence:
- canonical path;
- file modification time or content hash;
- Blender image filepath;
- dimensions;
- image/source type;
- small semantic statistics from `BAKE_VALIDATE`.

Avoid transporting full pixel arrays through the LLM.

## Save/reload transaction

A safe external bake transaction is:

```text
bake in memory
-> validate in-memory result
-> save external file
-> mark file authoritative
-> synchronize/reload runtime image datablock
-> validate runtime material
```

## Failure cases

Hard FAIL:
- expected disk artifact exists but Blender image points elsewhere;
- runtime material uses a stale datablock after a newer accepted bake;
- reload fails or dimensions become zero;
- colorspace differs from contract;
- multiple datablocks with ambiguous ownership cannot be resolved.

## Relation to other modules

Use with:
- `04_game_ready/51_BAKE_EXECUTION_AND_CHANNEL_SEMANTICS.md`;
- `08_scripts/93_BAKE_OUTPUT_VALIDATION_PATTERN.md`;
- `05_execution/65_INCREMENTAL_DIRTY_STAGE_CACHE.md`.

The dirty cache should distinguish texture-content dirtiness from Blender-datablock binding/freshness dirtiness. A stale datablock normally requires **reload + runtime QA**, not rebaking the texture.