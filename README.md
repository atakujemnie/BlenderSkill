# Blender AI Agent Library v0.3.0

Biblioteka wiedzy i procedur dla agenta AI sterującego Blenderem przez Python API / narzędzia automatyzacyjne.

## Canonical source vs single-file snapshot

**Źródłem kanonicznym jest katalog modułów MD.**

`_FULL_LIBRARY.md` jest plikiem generowanym automatycznie z modułów:
- służy do przeglądu całości,
- może służyć do jednorazowego importu,
- nie powinien być edytowany ręcznie.

Każda zmiana biblioteki:
1. modyfikuje właściwy moduł,
2. aktualizuje `MANIFEST.json`,
3. regeneruje `_FULL_LIBRARY.md`.

## Warstwa 2 — production techniques

Wersja 0.2 dodaje:
- camera/reference matching,
- Visual Feature Map,
- high-poly / low-poly,
- baking,
- trim sheets,
- decals,
- curves,
- Geometry Nodes,
- procedural materials,
- texture packing i mip safety,
- warianty assetów,
- automated visual diff,
- fidelity protocol,
- authoring-to-runtime handoff,
- Engine Profile i Engine Adapter.

## Warstwa 3 — Reconstruction Layer

Wersja 0.3 dodaje pełny system rekonstrukcji 1:1:
- model dowodów i provenance,
- segmentację concept sheet,
- klasyfikację projekcji,
- View Authority Matrix,
- rozwiązywanie konfliktów między widokami,
- uncertainty/confidence ledger,
- dimension graph,
- hard/derived/soft locks,
- landmark system,
- kalibrację rzutów,
- perspective camera solving,
- silhouette i negative-space constraints,
- inference przekrojów, krzywizn, promieni i grubości,
- hidden/occluded geometry policy,
- material/lighting disentanglement,
- branding/decal exactness,
- object decomposition,
- parametric master model,
- precision hard-surface construction,
- rear/bottom/underside workflow,
- multi-view QA,
- overlay, silhouette diff, landmark validation i ROI validation,
- reconstruction-specific regression gates,
- ambiguity escalation,
- change control,
- Definition of Done,
- osobne playbooki klas assetów,
- benchmark Lafar Street Bench.

Reconstruction Layer jest rozwinięciem standardowego pipeline, nie jego zamiennikiem.

## Cel

Agent ma produkować assety:
- zgodne z briefem i referencją,
- planowane przed wykonaniem,
- możliwie deterministycznie budowane,
- łatwe do poprawiania,
- poprawne technicznie w Blenderze,
- gotowe do użycia w silniku gry,
- kontrolowane wizualnie i technicznie po każdej istotnej fazie,
- bez marnowania wywołań API i tokenów na chaotyczne próby.

Biblioteka jest celowo podzielona na małe pliki. Agent powinien ładować tylko moduły potrzebne w danym etapie.

## Wersja docelowa

- Blender: 5.1.x
- Python: zgodny z Pythonem dostarczanym z Blenderem 5.1
- format runtime baseline: glTF 2.0 / GLB
- profil główny: assety do gry, hard-surface, props, architektura modułowa
- zasady są silnikowo neutralne; wymagania konkretnego silnika mają nadpisywać wartości domyślne

## Hierarchia wiedzy

1. jawne wymagania użytkownika,
2. zatwierdzone referencje i concept art,
3. kontrakt projektu / assetu,
4. stan sceny Blendera,
5. niniejsza biblioteka,
6. oficjalna dokumentacja Blender 5.1 i specyfikacja formatu eksportowego,
7. heurystyki agenta.

Niższy poziom nie może nadpisywać wyższego.

## Główna zasada

**Nie modeluj, dopóki nie wiadomo, co dokładnie ma zostać zachowane.**

Każdy asset przechodzi przez:

`ANALYZE -> CONTRACT -> PLAN -> BUILD -> INSPECT -> REPAIR -> VALIDATE -> EXPORT`

Przejście do następnego etapu jest dozwolone dopiero po spełnieniu kryteriów poprzedniego.

## Struktura

- `00_governance` — reguły nadrzędne i state machine.
- `01_analysis` — analiza briefu, referencji i cech.
- `02_blender_api` — sposób używania `bpy`, `bmesh`, operatorów i kontekstu.
- `03_modeling` — praktyka modelowania 3D.
- `04_game_ready` — ograniczenia runtime.
- `05_execution` — wykonanie, checkpointy, QA i naprawy.
- `06_prompts` — gotowe role i szablony promptów.
- `07_examples` — przykłady planowania assetów.
- `08_scripts` — bezpieczne fragmenty kodu audytowego.
- `10_reconstruction` — pełna warstwa rekonstrukcji 1:1.
- `11_playbooks` — playbooki klas assetów i technik.
- `99_sources` — źródła techniczne.

## Minimalny zestaw plików ładowanych przez agenta

Dla większości zadań:
1. `00_governance/00_AGENT_CHARTER.md`
2. `00_governance/02_STATE_MACHINE.md`
3. `01_analysis/12_FEATURE_CONTRACT.md`
4. `02_blender_api/20_BLENDER_5_1_API_STRATEGY.md`
5. `02_blender_api/25_TOOL_CALL_AND_TOKEN_EFFICIENCY.md`
6. `03_modeling/30_MODELING_DECISION_TREE.md`
7. `04_game_ready/40_GAME_ASSET_CONTRACT.md`
8. `05_execution/51_EXECUTION_PROTOCOL.md`
9. `05_execution/52_CHECKPOINT_AND_VISUAL_QA.md`
10. odpowiedni przykład z `07_examples`.

## Nieprawidłowy workflow

`reference -> bpy.ops -> dużo zmian -> render końcowy -> "prawie"`

## Prawidłowy workflow

`reference -> feature contract -> metryki -> plan brył -> checkpoint sylwetki -> detale pierwszego rzędu -> checkpoint -> materiały -> checkpoint -> optymalizacja -> walidacja`

## Definicja sukcesu

Asset jest skończony dopiero, gdy:
- wszystkie cechy `MUST` z Feature Contract są obecne,
- proporcje mieszczą się w tolerancji,
- widoki kontrolne nie pokazują utraty istotnych detali,
- geometria nie ma błędów technicznych blokujących runtime,
- materiały i UV spełniają kontrakt projektu,
- transformacje, pivot, nazewnictwo i eksport są poprawne,
- plik źródłowy pozostaje edytowalny.
