# Weathering and Environment-Response Language

## Purpose

Environment response is a location-level visual rule. Without it, each asset receives unrelated dirt/wetness/wear and the scene loses material continuity.

## Profile record

```yaml
weathering:
  profiles:
    WEATHER_LAFAR_MAINTAINED_WET_A:
      maintenance: HIGH
      humidity: HIGH
      rainfall: HIGH
      ground_grime: MEDIUM
      water_streaks: MEDIUM
      mineral_residue: LOW
      edge_wear: LOW
      usage_polish: LOW_TO_MEDIUM
      rust: VERY_LOW
```

## Semantic masks

Prefer physically meaningful masks:
- distance from ground;
- upward-facing surfaces;
- recess/concavity;
- contact zones;
- water-flow paths;
- frequently touched surfaces;
- sheltered vs exposed zones.

Do not replace all weathering with uniform global grunge.

## Maintenance state

Location/corporation identity may specify that infrastructure is maintained. Weathering then means subtle accumulated use, wetness and local dirt—not abandoned/apocalyptic damage.

## Asset variation

Assets can carry per-instance wear seeds/intensity, but the underlying profile remains canonical.

## Runtime

Source weathering language may drive material masks and bake parameters. Runtime textures should preserve the same semantic hierarchy at the available resolution.
