# Checkpoint and Visual QA

## Minimalny zestaw widoków

Dla statycznego prop:
- front ortho,
- side ortho,
- top ortho,
- 3/4 perspective.

Jeżeli geometria ma znaczenie z innych stron:
- rear,
- bottom.

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
- texture use.

## Difference score

Dla każdej cechy:
- PASS,
- MINOR,
- FAIL.

`MUST + FAIL` = asset nie może przejść dalej.
