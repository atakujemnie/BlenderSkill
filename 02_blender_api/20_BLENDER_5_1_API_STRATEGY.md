# Blender 5.1 API Strategy

## Version lock

Ten corpus jest pisany dla Blender 5.1.x.
Przy zmianie wersji:
- sprawdź release notes Python API,
- sprawdź zmiany operatorów i Geometry Nodes,
- nie zakładaj kompatybilności skryptów bez testu.

## Preferowana kolejność narzędzi

1. bezpośrednie odczyty z `bpy.data` / obiektów RNA,
2. bezpośrednie modyfikowanie właściwości obiektów i data-blocków,
3. `bmesh` dla topologii,
4. modyfikatory,
5. `bpy.ops` tylko gdy dana operacja rzeczywiście jest operatorem lub alternatywa jest nieproporcjonalnie złożona,
6. emulowanie UI jako ostateczność.

## Dlaczego

Operatory:
- zależą od context,
- często zależą od mode,
- mogą zależeć od active object / selection,
- bywają trudniejsze do uruchomienia w automatyzacji bez UI.

Data API:
- odwołuje się do jawnych obiektów,
- lepiej nadaje się do idempotentnych skryptów,
- ogranicza ukryty stan.

BMesh:
- jest przeznaczony do niskopoziomowej edycji geometrii mesh,
- pozwala łańcuchować operacje bez symulowania Edit Mode.

## Agent rule

Przed użyciem `bpy.ops.*` odpowiedz wewnętrznie:
1. Czy istnieje prosty Data API?
2. Czy istnieje `bmesh.ops`?
3. Jaki context wymaga operator?
4. Jaki mode?
5. Jaki active object?
6. Jak sprawdzę `poll()`?
7. Czy operator zmienia selection/mode?
8. Jak wrócę do stabilnego stanu?

## API action wrapper

Każdy większy skrypt powinien:
- znaleźć obiekty po nazwie/tagu, a nie przypadkowym zaznaczeniu,
- zweryfikować typ obiektu,
- zweryfikować wersję,
- zapisać stan krytyczny,
- wykonać zmianę,
- uruchomić postcondition check.
