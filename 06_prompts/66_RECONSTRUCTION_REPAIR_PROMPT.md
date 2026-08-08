# Reconstruction Repair Prompt

Masz naprawić wyłącznie wskazany reconstruction failure.

Przed zmianą:
- znajdź feature owner,
- constraints,
- dependencies,
- accepted checkpoint.

Wykonaj:
- minimalną zmianę parametryczną,
- nie ruszaj QA cameras,
- nie zmieniaj locked dimensions bez jawnego powodu.

Po zmianie:
- target validation,
- adjacent MUST regression,
- jeśli zmiana D0/D1: pełny multi-view gate.
