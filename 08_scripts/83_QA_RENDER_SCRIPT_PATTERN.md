# QA Render Script Pattern

## Cel

Generować identyczne rendery kontrolne między iteracjami.

## Profile

Przykładowe profile:
- `SILHOUETTE`
- `NEUTRAL`
- `MATCAP_EQUIVALENT`
- `MATERIAL`
- `WIREFRAME_CAPTURE`

## Camera registry

Kamery:
- front,
- side,
- top,
- rear,
- 3/4.

Nie twórz przypadkowej kamery przy każdym run.

## File naming

```text
<asset_id>__<version>__<checkpoint>__<view>__<profile>.png
```

## Metadata

Obok renderu zachowaj JSON:
- camera transform,
- lens/ortho scale,
- resolution,
- engine,
- color management,
- asset bounds,
- feature set.

## Pseudocode

```python
def render_checkpoint(asset_id, checkpoint, cameras, profiles):
    for camera in cameras:
        set_camera(camera)
        for profile in profiles:
            apply_qa_profile(profile)
            path = build_output_path(...)
            render(path)
            write_metadata(path)
```

## Rule

QA render pipeline nie powinien permanentnie niszczyć materiałów assetu.
Użyj override/profile i po zakończeniu przywróć scenę.
