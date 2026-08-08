# QA Orthographic Camera Generator Pattern

## Cel

Tworzyć kamery z identycznym framingiem.

Pseudo-pattern:

```python
def ensure_ortho_camera(name, axis, target_bounds, margin=0.05):
    cam_obj = get_or_create_camera(name)
    cam_obj.data.type = "ORTHO"
    set_axis_rotation(cam_obj, axis)
    set_camera_position_outside_bounds(cam_obj, axis)
    cam_obj.data.ortho_scale = compute_required_scale(target_bounds, axis, margin)
    lock_camera_metadata(cam_obj)
    return cam_obj
```

## Important

`ortho_scale` zależy od widoku i aspect ratio.
Nie ustawiaj jednej wartości dla front i side bez obliczenia.

## Metadata

Zapisz custom properties:
- qa_view,
- reference_segment,
- calibrated,
- calibration_revision.
