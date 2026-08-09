# Planting Reference Composition Fidelity

## Purpose

When concept/reference art exists, planter vegetation must be validated as a massing/composition problem, not only as valid object placement.

## Reference representation

Derive compact reference descriptors from canonical views:
- vegetation occupancy mask;
- height profile across the planter;
- focal-mass centroid;
- number/width of major masses;
- low/mid/tall occupancy bands;
- exposed-soil ratio;
- negative-space regions;
- optional semantic masks for focal, tall, mid and ground-cover layers.

Prefer compact grids such as 32x16 or 64x32 rather than raw pixel dumps.

## Candidate representation

Render neutral vegetation-only QA views with the same framing/registration. Compute the same descriptors locally.

## Gate

A strict reference-driven planter cannot claim visual completion from physical placement alone. The composition gate checks declared tolerances for:
- occupancy overlap/IoU;
- height-profile error;
- focal centroid error;
- exposed-soil difference;
- mass-count/continuity mismatch;
- required semantic-layer coverage.

High global overlap cannot compensate for a missing focal mass or missing required height layer.

## Efficiency

Compute masks and reductions locally. Return only aggregate scores and failing ROIs/bands.
