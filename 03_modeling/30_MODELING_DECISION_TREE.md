# Modeling Strategy Decision Tree

## 1. Czy asset jest głównie hard-surface?

Tak:
- box modeling,
- curves,
- booleans,
- bevel,
- solidify,
- mirror/array,
- controlled normals.

Nie:
przejdź do odpowiedniego profilu organic/deformation.

## 2. Czy kształt jest powtarzalny?

Tak:
- Array,
- instancing,
- linked data,
- Geometry Nodes, jeśli korzyść przewyższa złożoność.

## 3. Czy kształt jest symetryczny?

Tak:
- Mirror na wczesnym etapie.
Nie:
- nie wymuszaj symetrii.

## 4. Czy detal przecina bryłę?

Rozważ:
- boolean,
- inset + extrude,
- oddzielny insert mesh.

Wybór zależy od:
- wymogu edytowalności,
- shadingu,
- częstotliwości powtarzania,
- eksportu.

## 5. Czy detal jest tylko powierzchniowy?

Rozważ:
- normal map,
- decal,
- trim sheet,
- shader detail.

## 6. Czy detal wpływa na silhouette?

Jeżeli tak, geometria ma pierwszeństwo.

## 7. Czy część może być osobnym obiektem?

Preferuj osobny obiekt, jeśli:
- ma inny materiał,
- ma być animowana,
- może występować w wariantach,
- ułatwia boolean,
- ma własny pivot,
- może być instancją.

## 8. Czy Subdivision Surface jest naprawdę potrzebny?

Użyj, gdy:
- powierzchnia ma być ciągle zakrzywiona,
- kontrolna siatka daje korzyść.

Nie używaj jako automatycznego sposobu "wygładzania" wszystkiego.
