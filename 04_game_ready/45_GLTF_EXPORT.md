# glTF / GLB Export Baseline

## Dlaczego glTF jako baseline

glTF 2.0 jest formatem runtime-oriented przeznaczonym do efektywnego przenoszenia:
- scen,
- hierarchy,
- meshes,
- materials,
- cameras,
- animations.

Biblioteka traktuje go jako domyślny kontrakt wymiany, jeśli silnik nie wymaga innego formatu.

## Coordinate system

Przed exportem zawsze sprawdź konwersję osi między Blenderem i runtime.

Specyfikacja glTF:
- right-handed,
- +Y up,
- +Z forward,
- jednostka długości: metr.

Nie zakładaj, że ustawienia eksportera i silnika są identyczne.

## Authoring vs runtime

glTF nie jest formatem authoringowym.
Nie zastępuje `.blend`.

## Export checklist

- prawidłowe root nodes,
- oczekiwane meshes,
- materiały,
- UV,
- normals/tangents,
- textures,
- animations,
- transforms,
- skinning,
- no accidental cameras/lights, jeśli niepotrzebne.

## Post-export validation

Nie kończ pracy na komunikacie "export successful".

Sprawdź wynik:
- importerem docelowego silnika,
- lub niezależnym glTF validator/viewer,
- porównaj bounds,
- material appearance,
- animation,
- hierarchy.

## Embedded vs external

GLB upraszcza pojedynczy plik.
Zewnętrzne zasoby mogą ułatwiać reuse/cache.
Wybór należy do pipeline projektu.
