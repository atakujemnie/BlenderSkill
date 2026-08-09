# Tree, Shrub and Plant Generation

## Routing

Preferred backend order is capability-driven, not brand-driven:

```text
semantic PlantSpec
-> provider registry
-> compatible deterministic backend
-> generate disposable candidate
-> botanical + geometry proof
-> accepted authoring plant
```

## Tree/shrub requirements

- explicit trunk/stem datum;
- branch hierarchy and taper;
- crown envelope;
- leaf/needle semantic separation when runtime cards are expected;
- no zero-area branch tubes or disconnected floating foliage unless design says so;
- seed/reproducibility record.

## Sapling route

Sapling is an optional tree backend. Adapter translates `PlantSpec` into discovered operator parameters. Never hardcode remembered operator signatures; inspect the installed extension and run a minimal probe.

## Geometry Nodes route

For shrubs and alien flora, Geometry Nodes is often preferred because it allows explicit semantic inputs and better control over instancing, leaf clusters and runtime attributes.

## Asset-library route

A third-party plant asset may be used as a source member in a variation family, but record its asset identity/license separately from procedural placement. Asset selection is not botanical generation.
