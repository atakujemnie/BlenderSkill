# API Decision Matrix

## Cel

Wybrać najbezpieczniejszą warstwę wykonania.

| Potrzeba | Preferuj | Unikaj jako pierwszy wybór |
|---|---|---|
| odczyt obiektu | RNA / `bpy.data` | UI |
| tworzenie data-block | `bpy.data` | operator add + selection |
| proceduralna topologia | `bmesh` | setki Edit Mode ops |
| zmiana transform | object properties | translate operator |
| modifier params | modifier properties | UI |
| import/export | właściwy operator/export API | ręczne UI |
| render kontrolny | render API/tool | screenshot przypadkowego viewportu |
| masowa zmiana | jeden batch Python | wiele małych tool calls |
| pojedynczy interaktywny tool | operator z kontrolowanym context | emulacja kliknięć bez inspekcji |

## Decision questions

Przed operacją:
1. Czy jest read-only?
2. Czy trzeba zmieniać topologię?
3. Czy istnieje Data API?
4. Czy operator jest context-sensitive?
5. Czy rezultat wymaga renderu do oceny?
6. Czy operację można wykonać jako jeden parametryczny batch?
7. Jaki jest rollback?

## Priority

`read-only inspect -> direct data -> BMesh -> modifier -> controlled operator -> UI emulation`

To jest reguła biblioteki, nie twierdzenie, że wyższa warstwa jest zawsze technicznie możliwa.
