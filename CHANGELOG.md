# Changelog

## 0.3.1

Integrated two reviewed production skills without creating redundant parallel modules:
- expanded `03_modeling/40_TRIM_SHEETS.md` into a full semantic trim-sheet UV texturing skill;
- integrated the reference-image proportion/silhouette workflow into `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md` as the high-level reconstruction controller;
- added explicit trim-sheet routing and controller-first reference routing to the Knowledge Router.

Important integration corrections:
- texel density is now unit-explicit (`px_per_m`) instead of a bare numeric value;
- intentional trim-sheet UV reuse is distinguished from accidental overlap;
- trim-sheet reuse is not treated as an automatic draw-call reduction;
- persistent surface identity should not rely only on transient polygon indices;
- reconstruction confidence vocabulary is aligned with the existing `LOCKED/HIGH/MEDIUM/LOW/UNKNOWN` ledger;
- image-space quality thresholds are defined as overridable heuristics, not universal hard limits.

## 0.3.0

Added full Reconstruction Layer:
- 70 reconstruction modules/playbooks/scripts/prompts/benchmark elements,
- evidence/provenance model,
- concept-sheet segmentation,
- authority/conflict system,
- dimension graph and locks,
- landmark and calibration system,
- geometry inference rules,
- exact feature/material/branding handling,
- parametric reconstruction workflow,
- multi-view QA and regression gates,
- specialized modes for blueprint/photo/stylized references,
- Lafar Street Bench reconstruction benchmark.

## 0.2.0

Added production layer:
- camera/reference matching,
- Visual Feature Map,
- high/low-poly workflow,
- baking pipeline,
- trim sheets,
- decals/floating details,
- curve authoring,
- Geometry Nodes authoring,
- procedural material authoring,
- texture packing/mip safety,
- asset variants/randomization,
- automated visual diff,
- reference fidelity levels,
- authoring-to-runtime handoff,
- engine profile schema,
- engine adapter protocol,
- deterministic QA render pattern,
- visual diff script pattern.

Architecture decision:
- modular MD files are canonical,
- `_FULL_LIBRARY.md` is generated from them.
