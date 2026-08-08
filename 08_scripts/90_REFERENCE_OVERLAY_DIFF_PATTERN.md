# Reference Overlay Diff Pattern

## External/image-tool pattern

Input:
- reference crop,
- QA render,
- calibration metadata.

Output:
- alpha overlay,
- silhouette mask,
- diff heatmap,
- metrics JSON.

## Geometry-safe approach

Dla geometry QA używaj flat object mask.
To ogranicza wpływ:
- lighting,
- material,
- tone mapping.

## ROI

Dla feature-specific diff:
crop/weight według Visual Feature Map.

## Rule

Image diff nie modyfikuje sceny.
Jego wyniki są dowodem dla Inspector/Repairer.
