# Repository Workflow

## Source of truth

Repozytorium `atakujemnie/BlenderSkill` jest kanonicznym źródłem biblioteki.

Od tej wersji kolejne skille, playbooki, reguły API, benchmarki i poprawki są wykonywane w repozytorium, a nie w lokalnej kopii rozmowy.

## Change policy

Każda zmiana powinna:
1. modyfikować możliwie najmniejszy zestaw kanonicznych modułów,
2. zachować zgodność z `00_governance/04_KNOWLEDGE_ROUTER.md`,
3. aktualizować `MANIFEST.json`, jeśli zmienia się lista modułów lub wersja,
4. aktualizować `CHANGELOG.md` przy zmianie wersji lub istotnej zmianie zachowania,
5. regenerować `_FULL_LIBRARY.md`, gdy potrzebny jest skompilowany snapshot,
6. nie traktować `_FULL_LIBRARY.md` jako źródła do ręcznej edycji.

## Versioning

- patch: korekty, doprecyzowania, drobne nowe reguły bez zmiany architektury,
- minor: nowa warstwa wiedzy, większy playbook lub nowy pipeline,
- major: niekompatybilna zmiana kontraktów agenta lub struktury biblioteki.

## Working rule

Przed zmianą należy najpierw odczytać aktualny stan odpowiednich plików z repozytorium. Nie wolno opierać aktualizacji na starszej lokalnej kopii, jeśli repozytorium zawiera nowszą wersję.
