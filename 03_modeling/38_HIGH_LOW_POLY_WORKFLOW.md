# High-Poly / Low-Poly Workflow

## Kiedy stosować

High -> Low + bake jest uzasadnione, gdy:
- detal powierzchniowy jest zbyt kosztowny jako runtime geometry,
- wymagane są miękkie przejścia lub złożone mikrofazy,
- asset będzie oglądany wystarczająco blisko,
- detal normal mapy daje realną korzyść.

Nie stosuj automatycznie do każdego prop.

## High-poly

Cel:
- wygląd,
- powierzchnia,
- edge highlights,
- szczegóły do bake.

High-poly nie musi:
- mieć runtime topology,
- mieć minimalnego polycount,
- posiadać finalnego UV low-poly.

Musi:
- odpowiadać finalnej sylwetce tam, gdzie bake jej nie zastąpi.

## Low-poly

Cel:
- zachować silhouette,
- zachować funkcjonalną geometrię,
- posiadać stabilne shading/UV,
- mieścić się w runtime contract.

## Matching

High i low powinny:
- dzielić ten sam world scale,
- nakładać się przestrzennie,
- mieć kontrolowane odległości powierzchni.

## Hard edges and UV

Rozdzielenie smoothingu i seamów powinno być planowane razem z tangent-space normal bake.

Nie zmieniaj topologii i triangulacji po finalnym bake bez ponownej walidacji.

## Bake-critical freeze

Po zatwierdzeniu low-poly do bake:
- zachowaj kopię,
- zamroź UV,
- zamroź krytyczne normals/smoothing,
- zapisz triangulation policy.

## Naming

Przykład:
- `HP_Lafar_Bench_Frame`
- `LP_Lafar_Bench_Frame`
- `CAGE_Lafar_Bench_Frame`

## Exit criteria

- silhouette low-poly zaakceptowana,
- bake nie musi kompensować złej bryły,
- projection errors mieszczą się w przyjętej jakości,
- tangent-space normal działa poprawnie w docelowym runtime.
