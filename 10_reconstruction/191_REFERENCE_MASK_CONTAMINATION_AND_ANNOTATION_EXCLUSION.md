# Reference Mask Contamination and Annotation Exclusion

## Purpose

Technical sheets contain product pixels and annotation pixels in the same raster.

The v0.11 lamp showed that dimension lines and leaders materially changed contour deviation. A registered overlay can therefore fail or pass for the wrong reason if it treats annotations as product silhouette.

## Mask classes

Where relevant distinguish:

```text
PRODUCT_MASK
DIMENSION_LINE_MASK
LEADER_MASK
TEXT_MASK
ARROWHEAD_MASK
DECORATIVE_GRAPHIC_MASK
```

Only PRODUCT_MASK participates in outer-silhouette metrics unless a specific annotation is itself the measured source.

## Canonical cleanup sequence

1. use the registered view ROI;
2. apply explicit exclusion rectangles for known labels/leaders where available;
3. select the product connected component by seed or largest-component policy;
4. preserve bright/chromatic product materials with the reference contrast model;
5. calculate silhouette metrics on the cleaned product mask;
6. report mask policy and exclusions as evidence provenance.

## Connected-component policy

`largest component` is appropriate only when the product is one connected silhouette in that view. For separated feet, floating parts or intentional gaps, use a seeded/declared component set instead.

Never silently erase small components merely because they are small; they may be real trim or detached structure.

## Executor integration

`executors/reference_overlay_validate.py` supports mask exclusions and connected-component filtering. Registration remains global; mask cleanup must not locally warp or translate the candidate to improve score.
