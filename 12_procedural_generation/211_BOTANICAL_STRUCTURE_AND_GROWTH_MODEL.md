# Botanical Structure and Growth Model

## Purpose

Give the agent a plant-language layer independent of Sapling, Geometry Nodes, assets or any specific generator.

## Structural vocabulary

- stem/trunk and axis hierarchy;
- internodes and nodes;
- branching order;
- branch angle and taper;
- phyllotaxis / leaf attachment;
- crown envelope and density;
- apical dominance;
- tropism/gravity/light direction;
- pruning/termination;
- age class;
- season/leaf state;
- root/contact datum.

## Plant form classes

`TREE`, `SHRUB`, `HERBACEOUS`, `GRASS`, `ROSETTE`, `REED`, `VINE`, `GROUND_COVER`, `ALIEN_BRANCHING`.

The form class controls which structural fields are meaningful. Example: a rosette may have near-zero visible internode length; a tree normally may not.

## Coherence checks

- positive height/stem dimensions;
- bounded branching orders;
- phyllotaxis angle in `[0,360)`;
- normalized density/apical-dominance fields;
- nonzero seed for reproducibility;
- plausible crown/height ratio or explicit stylized/alien waiver;
- stable root/contact datum.

## What this does not do

This contract does not claim biological simulation. It provides enough structural semantics to prevent procedural vegetation from degenerating into arbitrary noise while still supporting stylized Lafar flora.

## Executor

`executors/botanical_grammar.py`.
