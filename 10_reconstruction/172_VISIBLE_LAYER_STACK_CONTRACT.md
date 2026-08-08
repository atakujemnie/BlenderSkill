# Visible Layer Stack Contract

## Cel

Wykrywać cechy, które istnieją geometrycznie, lecz są zakopane w host mesh, zwrócone normalną od kamery albo przesłonięte przez nieprzezroczystą warstwę.

To osobna klasa błędu od `object exists` i od poprawnego bounding boxu.

## Typowe przypadki

- display content za recess floor;
- glass za nieprzezroczystym hostem;
- decal/floater pod powierzchnią;
- emissive strip wewnątrz obudowy;
- panel relief o poprawnym rozmiarze, lecz po złej stronie host plane;
- quad skierowany normalną do wnętrza.

## Kontrakt

Dla każdej cechy wymagającej widoczności zapisz:

```yaml
visible_stack:
  view: FRONT
  axis: Y
  viewer_side: NEGATIVE
  opaque_occluder_plane: -0.065
  front_to_back:
    - glass
    - content
    - recess_floor
  layers:
    - name: glass
      interval: [-0.084, -0.080]
      normal_axis_component: -1.0
      required_visible: true
    - name: content
      interval: [-0.078, -0.078]
      normal_axis_component: -1.0
      required_visible: true
```

Dla viewer po stronie NEGATIVE mniejsza wartość osi jest bliżej obserwatora.

## Gate

MUST visible feature = PASS dopiero, gdy:
- leży po widocznej stronie opaque occluder/floor;
- normalna spełnia wymagany kierunek lub materiał jest jawnie two-sided zgodnie z kontraktem;
- wymagany front-to-back order jest zachowany;
- feature ROI potwierdza jego obecność, jeżeli ma authority wizualne.

## Anti-fix

Nie przesuwaj cechy losowo w stronę kamery. Najpierw ustal:
- host surface;
- recess depth;
- physical layer ownership;
- required clearance.

## Executor

`executors/layer_stack_validate.py` zapewnia tani numeric preflight. Finalna cecha może nadal wymagać ROI/ray/render proof.
