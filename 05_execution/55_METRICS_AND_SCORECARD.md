# Asset Quality Scorecard

Scorecard nie zastępuje bramek MUST.

## Categories

### A. Reference fidelity — 0–30
- silhouette 10
- proportions 8
- primary features 8
- material regions 4

### B. Modeling quality — 0–20
- topology appropriate 5
- shading 5
- modifier strategy 5
- editability 5

### C. Game readiness — 0–25
- geometry budget 5
- materials/textures 5
- pivot/transforms/naming 5
- LOD/collision 5
- export 5

### D. API/process quality — 0–15
- deterministic operations 5
- idempotency 4
- checkpoint discipline 3
- efficient tool usage 3

### E. Documentation — 0–10
- feature mapping 4
- build parameters 2
- manifest 2
- known limitations 2

## Thresholds

- 90–100: production-ready
- 80–89: acceptable with minor fixes
- 70–79: requires repair
- <70: return to planning/modeling

## Hard fail

Niezależnie od score:
- dowolny `MUST = FAIL`,
- błędny pivot dla funkcjonalnego assetu,
- brakujący wymagany materiał/animation,
- uszkodzony export,
- poważny shading/runtime defect.
