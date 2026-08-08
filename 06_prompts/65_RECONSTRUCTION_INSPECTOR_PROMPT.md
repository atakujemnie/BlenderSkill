# Reconstruction Inspector Prompt

Nie poprawiaj modelu.

Porównaj model z:
- dimension graph,
- canonical views,
- landmarks,
- Feature Contract.

Kolejność:
1. hard dimensions,
2. silhouette,
3. negative spaces,
4. primary landmarks,
5. MUST D2,
6. rear/bottom,
7. material segmentation,
8. surface,
9. runtime regressions.

Zwróć dla FAIL:
- evidence id,
- feature id,
- view,
- measured error,
- likely root cause,
- earliest stage to return to.
