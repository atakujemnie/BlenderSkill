# Reference Decomposition

## Cel

Nie opisuj referencji słowami typu "futurystyczny panel".
Rozbij ją na informacje możliwe do odwzorowania geometrycznie.

## Warstwa A — silhouette
Zidentyfikuj:
- bounding box,
- główne załamania,
- skosy,
- wcięcia,
- wypukłości,
- otwarte przestrzenie.

## Warstwa B — proportions
Zapisz relacje:
- width : height : depth,
- wysokość detalu względem całego obiektu,
- szerokość ramek,
- grubość paneli,
- promienie i bevel widths.

Jeżeli brak skali absolutnej, relacje są ważniejsze niż zgadywane metry.

## Warstwa C — primary features
Elementy, bez których asset przestaje być tym samym projektem.

Przykłady:
- charakterystyczny łuk,
- konkretny rowek biegnący po dwóch bokach,
- asymetryczny moduł,
- otwór o określonym profilu,
- osobna metalowa osłona.

## Warstwa D — secondary features
Detale zwiększające wiarygodność, ale niewpływające mocno na identyfikację.

## Warstwa E — materials
Dla każdego obszaru:
- metal / dielectric,
- roughness family,
- transparency,
- emissive,
- normal detail,
- texture continuity.

## Warstwa F — construction logic
Zadaj sobie:
- z ilu produkcyjnych części powstałby przedmiot,
- które elementy są nakładkami,
- które są frezowane,
- gdzie istnieją szczeliny montażowe,
- czy detal powinien być geometrią, normal mapą czy teksturą.

## Widoki referencyjne

Jeżeli dostępne są różne widoki:
- nie zakładaj automatycznie zgodności,
- utwórz tabelę sprzeczności,
- wybierz referencję kanoniczną dla każdej strefy.
