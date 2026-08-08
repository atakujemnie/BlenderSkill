# QA Render Script Pattern

## Cel

Generować identyczne rendery kontrolne między iteracjami bez zanieczyszczenia kadru obiektami spoza testowanego assetu.

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
Dla reconstruction reference camera ma być zapisana w registry/cache i ponownie używana.

## Scene isolation

Przed renderem:
- zidentyfikuj asset root/collection;
- zidentyfikuj QA rig;
- zapisz aktualne `hide_render`/collection visibility dla pozostałych obiektów;
- tymczasowo wyłącz unrelated renderable geometry/lights;
- po renderze przywróć stan w `finally`/transaction cleanup.

`hide_viewport=True` nie oznacza `hide_render=True`.
Nie usuwaj obcych obiektów tylko po to, aby uzyskać czysty render.

## Render-engine capability

Nie zakładaj nazwy enum render engine z pamięci.
Jeżeli skrypt ma działać między wersjami/kompilacjami, odczytaj dostępne enum values i wybierz wspierany profil.

Ta detekcja ma odbyć się raz na sesję/rig, nie przed każdym obrazem.

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
- QA lighting profile,
- asset bounds,
- feature set,
- scene isolation state/version.

## Pseudocode

```python
def render_checkpoint(asset_id, checkpoint, cameras, profiles):
    saved = isolate_scene_for_qa(asset_id)
    try:
        for camera in cameras:
            set_camera(camera)
            for profile in profiles:
                apply_qa_profile(profile)
                path = build_output_path(...)
                render(path)
                write_metadata(path)
    finally:
        restore_scene(saved)
```

## Compact output

The render tool should return paths and compact status, not the full render metadata or repeated source code:

```yaml
qa_render:
  status: PASS
  outputs:
    front: /tmp/...front.png
    hero: /tmp/...hero.png
  engine: BLENDER_EEVEE
  isolated_objects: 1
```

## Rule

QA render pipeline nie powinien permanentnie niszczyć materiałów, visibility ani innych ustawień sceny.
Użyj override/profile i po zakończeniu przywróć scenę.
