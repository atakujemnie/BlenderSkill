# Reconstruction Checkpoint Manifest Pattern

## Manifest contains

```text
asset_id
stage
timestamp/version
hard_dimensions
object_bounds
feature_status
modifier_stacks
materials
qa_camera_revision
reference_revision
render_paths
```

## Use

Porównuj checkpointy:
- D0 accepted,
- D1 accepted,
- D2 accepted,
- surface accepted,
- runtime.

## Rule

Nie przechowuj tylko pliku `.blend`.
Bez manifestu agent nie wie, co było zaakceptowane.
