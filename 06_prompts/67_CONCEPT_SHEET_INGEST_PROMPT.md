# Concept Sheet Ingest Prompt

Przeanalizuj planszę referencyjną bez modelowania.

Najpierw sprawdź `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md`. Jeżeli istnieje ważny cache dla tego samego źródła, nie segmentuj i nie mierz ponownie zwalidowanych regionów.

Zidentyfikuj:
- wszystkie subviews,
- dimensions,
- material samples,
- real asset branding,
- annotations that are not part of asset,
- detail crops,
- inconsistencies.

Dla technical concept sheet stosuj kolejność autorytetu z `10_reconstruction/160_BLUEPRINT_AND_TECHNICAL_DRAWING_MODE.md`.

Wynik:
- segment manifest / Reference Registry,
- evidence ledger,
- view authority proposal,
- locked dimensions,
- cross-view aggregate consistency,
- unresolved ambiguity,
- cache update.

Nie interpretuj marketingowych podpisów jako geometrii.
Nie traktuj dimension lines, leaders, arrows ani separatorów layoutu jako silhouette.

Nie zwracaj pełnych pixel arrays, per-row profiles ani długich threshold traces. Przy niejednoznaczności wskaż minimalny ROI wymagający diagnostyki.

Po `ANALYZE: PASS` zakończ szeroką eksplorację planszy. Dalsza analiza musi dotyczyć konkretnego feature ID, metric ID, view conflict lub failing ROI.
