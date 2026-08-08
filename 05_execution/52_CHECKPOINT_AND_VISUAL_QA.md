# Checkpoint and Visual QA

## QA scene isolation preflight

Before rendering a checkpoint:
- identify the asset collection/root;
- identify the QA rig collection;
- temporarily exclude unrelated renderable objects/lights that are not part of the intended QA setup;
- preserve and restore their previous `hide_render`/collection visibility state;
- do not delete user objects to obtain a clean QA render.

Viewport visibility is not proof of render visibility. An object can be hidden in viewport and still appear in render.

## Minimalny zestaw widoków

Dla statycznego prop:
- front ortho,
- side ortho,
- top ortho,
- 3/4 perspective.

Jeżeli geometria ma znaczenie z innych stron:
- rear,
- bottom.

For a reference-driven asset, add feature-specific close-up ROI views only when the wide views cannot validate a MUST feature.

## Tryby kontroli

### Silhouette
Jednolity ciemny materiał / maska.
Cel: ocenić tylko obrys.

### Neutral shaded
Szary PBR.
Cel: forma i highlight.

### Matcap
Cel: wykrywanie falowania i shading artefacts.

### Wireframe
Cel: topologia i gęstość.

### Material preview
Cel: materiały, UV i texture direction.

## Geometry/material separation

Do not use a MATERIAL/HERO render as the first proof of geometric correctness.

Order:

```text
SILHOUETTE / ORTHO NUMERIC
-> NEUTRAL / MATCAP FORM
-> MATERIAL
-> HERO
```

If a detail is difficult to see in one material/lighting render:
1. test it in neutral geometry QA;
2. inspect reference evidence and dimensions;
3. determine whether the cause is geometry, lighting, material or camera;
4. modify geometry only if geometric evidence supports the change.

Do not increase panel relief, bevel width, groove depth or feature size merely to make it visible under a particular QA lighting setup.

## Visible feature proof

For a feature whose contract says it must be visible, object existence is insufficient.

Accept one or more of:
- expected pixels detected in the feature ROI;
- silhouette/neutral render shows the feature;
- ray/occlusion test proves it is outside the host surface and visible from required view;
- geometric host/detail offset is validated along the correct normal.

This applies especially to floating panels, local emissive accents and decals/floaters.

## Checkpoint C1 — Blockout
Oceniaj:
- bounds,
- proporcje,
- osie,
- negative spaces,
- primary silhouette.

Nie oceniaj tekstur.

## Checkpoint C2 — Primary details
Oceniaj wszystkie `MUST`.

## Checkpoint C3 — Shading
Oceniaj:
- bevel,
- normals,
- smooth transitions,
- boolean artifacts.

## Checkpoint C4 — Runtime
Oceniaj:
- LOD,
- collision,
- pivot,
- material count,
- texture use,
- topology contract through `MESH_VALIDATE`.

## Difference score

Dla każdej cechy:
- PASS,
- MINOR,
- FAIL.

`MUST + FAIL` = asset nie może przejść dalej.

A checkpoint summary should contain compact metrics and failing feature IDs, not raw pixel/profile dumps.
