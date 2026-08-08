# Execution Protocol

## 0. Runtime capability preflight

Before the first production mutation in a session:
- load `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`;
- discover current connected tools;
- build/reuse Tool Registry;
- bind capabilities according to `02_blender_api/28_AGENT_TOOL_API_PROFILE.md`;
- require at least `scene_inspect=BOUND` and `python_execute=BOUND` for autonomous mesh mutation;
- record any missing capability as a blocker instead of guessing an unavailable tool.

Do not repeat capability discovery before every feature unless the binding becomes invalid.

## 1. Preflight

- odczytaj Scene Snapshot,
- sprawdź Blender version,
- sprawdź jednostki,
- sprawdź, czy asset już istnieje,
- sprawdź Feature Contract,
- sprawdź Build Plan,
- wybierz `SELECTED SKILL ID` dla operacji, jeśli istnieje zarejestrowany semantic skill,
- sprawdź wymagane capabilities wybranego skilla,
- sprawdź `executors/` zanim wygenerujesz lokalny helper dla zarejestrowanej operacji.

## 2. Create asset root

Utwórz lub znajdź:
- collection assetu,
- root object/empty, jeśli pipeline tego wymaga,
- naming namespace.

## 3. Build by phase

Każdy phase:
1. loguje start,
2. wykonuje spójny batch,
3. aktualizuje scenę,
4. wykonuje postcondition,
5. zapisuje status feature IDs,
6. uruchamia checkpoint.

Jeżeli faza wymaga większego skryptu, stosuj `05_execution/62_CODE_ARTIFACT_AND_PATCH_PROTOCOL.md`: kod jest artefaktem na dysku, a nie pełnym tekstem przenoszonym przez kontekst po każdym wywołaniu.

## 4. Postcondition examples

Po stworzeniu blockoutu:
- obiekt istnieje,
- dimensions są zgodne,
- scale jest oczekiwana,
- liczba części się zgadza.

Po boolean:
- modifier/rezultat istnieje,
- nie zniknęły faces z innej strefy,
- bounds nie zmieniły się poza tolerancją.

Po bevel:
- width zgodny,
- segment count zgodny,
- brak self-overlap.

Po semantic skill operation:
- skill-specific validation report exists,
- feature ownership remains valid,
- previously accepted MUST features have not regressed.

Po mesh validation:
- każdy mesh ma jawny `topology_intent`;
- `MESH_VALIDATE` nie raportuje ogólnego PASS, jeśli obiekt nie ma kontraktu topology intent;
- boundary/non-manifold są interpretowane zgodnie z kontraktem, nie ignorowane globalnie.

## 5. Checkpoint

Nie kontynuuj, jeśli checkpoint FAIL.

## 6. Save

Zapisuj:
- przed ryzykownym Apply,
- po zaakceptowanym dużym etapie,
- przed exportem,
- przed strategy switch, jeżeli nowa strategia może istotnie zmienić topologię.

Dla wygenerowanych skryptów zapisuj ścieżkę i ostatni pomyślny status zamiast powtarzać pełną treść kodu w logu.

## 7. No silent repair

Jeżeli wykonanie różni się od planu, zapisz to jako deviation.
Nie zmieniaj strategii po cichu.

Nie zmieniaj geometrii wyłącznie po to, aby detal był bardziej widoczny w jednym QA lighting setup. Najpierw rozstrzygnij, czy problem dotyczy geometrii, materiału, oświetlenia czy kamery.

## 8. Retry budget

Obowiązuje `05_execution/61_RETRY_BUDGET_AND_STRATEGY_SWITCH.md`.

Ta sama operacja z tą samą strategią i tymi samymi preconditions może zostać wykonana maksymalnie dwa razy łącznie:
- pierwsza próba,
- jedna poprawiona próba po diagnostyce.

Po drugiej porażce:
- zatrzymaj ten call pattern,
- wykonaj re-inspection,
- sklasyfikuj failure,
- przywróć checkpoint, jeśli scena została uszkodzona,
- zmień strategię lub zgłoś blocker.

Każdy retry musi wynikać z nowej informacji albo jawnej zmiany zwalidowanego precondition.
