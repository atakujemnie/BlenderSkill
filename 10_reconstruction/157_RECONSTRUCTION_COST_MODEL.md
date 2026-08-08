# Reconstruction Cost Model

## Koszt agentowy

Śledź:
- tool calls,
- failed calls,
- renders,
- full-scene rebuilds,
- tokens loaded,
- repair iterations.

## Koszt artystyczny

Najdroższe regresje:
1. zmiana D0 po D3,
2. zmiana topologii po UV/bake,
3. zmiana material segmentation po atlasie,
4. zmiana hierarchy po animation/export.

## Strategy

Najwięcej analizy wykonaj przed kosztownymi freeze points.

## Efficiency metric

`accepted_features / tool_calls`

oraz:
`MUST regressions / repair`

## Rule

Oszczędność tokenów nie może polegać na pomijaniu checkpointów.
Ma wynikać z:
- lepszego routingu wiedzy,
- batch operations,
- parametryzacji,
- lokalnych napraw.
