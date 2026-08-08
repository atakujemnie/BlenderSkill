# View Authority Matrix

## Cel

Ustalić, który widok rozstrzyga konkretną cechę.

## Przykładowa macierz

| Property | Primary authority | Secondary |
|---|---|---|
| total width | FRONT/TOP + numeric | REAR |
| total height | FRONT/SIDE + numeric | HERO |
| total depth | SIDE/TOP + numeric | HERO |
| backrest angle | SIDE | HERO |
| rear panel layout | REAR | HERO if visible |
| underside | BOTTOM | SIDE |
| material edge highlight | HERO/DETAIL | ORTHO |
| logo placement rear | REAR | DETAIL |

## Property-level authority

Nie istnieje jeden "najważniejszy widok" dla całego assetu.
Autorytet jest przypisany do właściwości.

## Conflict handling

Jeżeli dwa widoki o podobnym autorytecie są sprzeczne:
- oznacz konflikt,
- nie uśredniaj automatycznie,
- nie wybieraj bardziej atrakcyjnego renderu.
