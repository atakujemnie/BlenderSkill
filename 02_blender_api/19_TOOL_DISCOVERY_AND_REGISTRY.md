# Tool Discovery and Registry

Ten moduł dotyczy warstwy narzędzi AI/MCP/API stojącej przed `bpy`.

## Problem

Agent nie może zakładać, że:
- każde narzędzie wykonuje kod Python,
- każde narzędzie ma dostęp do UI,
- każde narzędzie zwraca render,
- każdy operator Blendera jest dostępny w tym samym kontekście,
- wywołanie jest tanie lub bez skutków ubocznych.

## Discovery przed pierwszą modyfikacją

Agent tworzy `Tool Registry`.

Dla każdego dostępnego narzędzia zapisuje:

| Field | Meaning |
|---|---|
| tool_name | dokładna nazwa |
| purpose | do czego służy |
| read/write | czy zmienia scenę |
| inputs | wymagane argumenty |
| output | co realnie zwraca |
| context | wymagania UI/scene/mode |
| side_effects | selection, mode, scene, file |
| idempotent | yes/no/conditional |
| cost | low/medium/high |
| preferred_for | najlepsze zastosowanie |
| avoid_for | zastosowania niewłaściwe |
| verification | jak sprawdzić wynik |

## Klasy narzędzi

### T1 — Read-only scene inspection
Preferowane do:
- inventory,
- object properties,
- mesh stats,
- materials,
- hierarchy.

### T2 — Python execution
Preferowane do:
- deterministycznych batchy,
- BMesh,
- tworzenia danych,
- audytu,
- parametrycznych zmian.

### T3 — UI/operator execution
Preferowane tylko, gdy:
- narzędzie jest rzeczywiście interaktywne,
- Python/Data API nie daje rozsądnej alternatywy.

### T4 — Render/screenshot
Preferowane do:
- visual QA,
- porównań,
- checkpointów.

### T5 — File/save/export
Preferowane do:
- checkpointów,
- finalnych artefaktów,
- testów eksportu.

## Routing rule

Wybieraj narzędzie o:
1. najwęższym zakresie wystarczającym do zadania,
2. najmniejszej liczbie skutków ubocznych,
3. najwyższej deterministyczności,
4. najniższym koszcie przy tej samej jakości.

## Zakaz tool guessing

Jeżeli agent nie zna dokładnego zachowania narzędzia:
- nie uruchamia go na głównym assetcie,
- odczytuje schema/help, jeśli dostępne,
- albo wykonuje minimalny test na obiekcie tymczasowym.

## Tool Registry persistence

Registry powinien być przechowywany dla danej sesji/wersji integracji.
Nie rediscoveruj tych samych możliwości przed każdym krokiem.
