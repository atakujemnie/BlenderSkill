# Topology, Normals and Shading

## Topologia game assetu

Nie optymalizuj pod estetykę wireframe.
Optymalizuj pod:
- silhouette,
- shading,
- deformację,
- bake,
- runtime.

## N-gons

N-gon nie jest automatycznie błędem.
Jest ryzykowny, gdy:
- triangulacja jest nieprzewidywalna,
- powierzchnia jest nieplanarna,
- będzie deformowany,
- powoduje shading artefacts.

## Long thin triangles

Unikaj, jeżeli:
- powodują artefakty,
- niepotrzebnie komplikują UV,
- powstają po agresywnych booleanach.

## Normals

Sprawdź:
- orientację face normals,
- spójność smooth/flat,
- custom normals, jeśli używane,
- zachowanie po eksporcie.

## Weighted / edited normals

Stosuj jako świadome narzędzie shadingu.
Nie używaj do maskowania złej geometrii, która nadal daje błędną sylwetkę lub bake.

## Bevel + normals

Mały bevel:
- poprawia highlight,
- daje wizualną skalę,
- często jest ważniejszy niż dodatkowy detal powierzchniowy.

## Kontrolla

Render kontrolny:
- szary neutralny materiał,
- światło pod małym kątem,
- matcap,
- wireframe overlay.

Beauty lighting może ukryć błędy.
