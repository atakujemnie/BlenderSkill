# Reconstruction Regression Gates

## Baseline

Po każdym zaakceptowanym etapie przechowaj:
- geometry manifest,
- renders,
- feature statuses,
- dimension report.

## Change classes

### LOCAL DETAIL
Test:
- target ROI,
- neighboring MUST.

### SHAPE
Test:
- all ortho silhouettes,
- dimensions,
- all D0/D1 MUST.

### TOPOLOGY
Test:
- shape + shading + UV if existing.

### MATERIAL
Test:
- material ROIs + no geometry change.

### EXPORT
Test:
- full runtime regression.

## Fail

Regresja MUST blokuje dalszy etap nawet jeśli naprawiany feature został poprawiony.
