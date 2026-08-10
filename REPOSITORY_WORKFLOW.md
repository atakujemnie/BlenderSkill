# Repository Workflow

Version: 0.18.0

## Source of truth

Repozytorium `atakujemnie/BlenderSkill` jest kanonicznym źródłem biblioteki. Modułowe pliki źródłowe, executory, testy i deklaracje w `MANIFEST.json` są źródłem prawdy; `_FULL_LIBRARY.md` oraz `_RUNTIME_INDEX.json` są deterministycznymi artefaktami generowanymi.

## Development policy

1. Feature development odbywa się na branchu i przez Pull Request. Nie implementuj wersji bezpośrednio na `main`.
2. Przed zmianą odczytaj aktualny stan odpowiednich plików z repozytorium; nie bazuj na starszej kopii lokalnej.
3. Normalne CI jest read-only i ma wyłącznie `contents: read`.
4. CI nigdy nie naprawia ani nie commituje wygenerowanych artefaktów. Jeżeli generator zmienia committed artifact, CI kończy się błędem.
5. `_FULL_LIBRARY.md` i `_RUNTIME_INDEX.json` muszą być wygenerowane i committed w tym samym PR co zmiany źródłowe.
6. `EXECUTOR_READY` wymaga istniejącego kontraktu, executora z poprawnym `EXECUTOR_ID` i `EXECUTOR_VERSION` oraz co najmniej jednego executable testu.
7. Kontrakt zależny od Blender runtime wymaga co najmniej jednego testu uruchomionego w prawdziwym, przypiętym Blenderze 5.1.x.
8. Release wymaga formalnego tagu `vX.Y.Z` i odpowiadającego GitHub Release.
9. `.github/workflows/release.yml` jest jedynym workflow z `contents: write`.
10. Historyczne `upgrade_v014_metadata.py`–`upgrade_v017_metadata.py` są utilities historycznymi i nie uczestniczą w normalnym CI ani release v0.18+.

## Manifest and generated artifacts

Zmiana listy modułów, executora, testu, maturity, benchmarku lub wersji musi być odzwierciedlona w `MANIFEST.json` schema v2. Generator pełnej biblioteki waliduje ścieżki, duplikaty, liczbę modułów, benchmarki, skill/executor/test references i deklaracje artefaktów.

`_FULL_LIBRARY.md` jest pełnym snapshotem treści modułów. `_RUNTIME_INDEX.json` jest małym indeksem routingu i nie zawiera pełnych treści modułów.

## Release gate

PR wersji nie jest gotowy, dopóki nie przejdą: ruff, pytest unit/integration, regresje historyczne, parity validation, manifest validation, deterministyczne generatory oraz wymagany Blender runtime suite. Release workflow dodatkowo sprawdza metadata, czystość artefaktów, branch `main` i brak istniejącego tagu.

## Versioning

- patch: korekty bez zmiany architektury;
- minor: nowa warstwa wiedzy, większy playbook lub pipeline;
- major: niekompatybilna zmiana kontraktów albo struktury biblioteki.
