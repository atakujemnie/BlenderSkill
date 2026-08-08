# RDL Diagnostic Geometry and Neutral Shading

## Purpose

Coarse-to-fine reconstruction must become visually falsifiable before materials and detail can mask geometry errors.

## RDL0 is geometry

RDL0 must create a disposable diagnostic representation of:
- total envelope;
- ground/contact datum;
- primary extents;
- major negative space;
- principal axes.

For a street lamp this can be only:

```text
base envelope
pole envelope
head projection envelope
```

No service hatches, LEDs, branding or production materials.

## Diagnostic shading rule

RDL0–RDL3 source-fit QA uses a neutral diagnostic material by default:
- fixed neutral albedo;
- high enough roughness to read planes;
- no micro-normal;
- no anisotropy;
- no bloom;
- no stylized lighting;
- emission shown only when the geometry of the emitter itself is the owner under test.

Production graphite/aluminium/titanium shaders belong to RDL5 lookdev validation.

## Why

The Lamp v0.10 builder created full material nodes before solving primary geometry. That was not the main reason for its remaining errors, but it weakens the diagnostic separation between form and finish.

## Required RDL0 checkpoint

```text
build diagnostic envelope
-> FRONT/SIDE/TOP as applicable
-> numeric envelope check
-> registered comparison
-> RDL0 node gate
-> ACCEPTED
```

Only then authorize G1/RDL1 forms.

## Material replacement

Diagnostic materials are QA infrastructure, not final materials. Replacing them later must not modify accepted geometry.
