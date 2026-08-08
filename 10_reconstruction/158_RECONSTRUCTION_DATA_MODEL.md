# Reconstruction Data Model

## Recommended entities

### Reference
source file.

### Segment
crop/view/material sample.

### Evidence
claim from segment.

### Constraint
numeric/geometric rule.

### Feature
visible or functional characteristic.

### Owner
scene object/data/modifier/material.

### Landmark
point/line/region used by QA.

### Checkpoint
accepted scene state.

### Deviation
authorized change from reference.

### ValidationResult
measurement/status.

## IDs

Prefer stable IDs:
- REF001
- SEG_FRONT
- E023
- C014
- F031
- LM009
- CP_D1

## Why

Stable IDs allow:
- machine-readable reports,
- targeted repair,
- regression tracking,
- future automation.
