# Civic Street Lamp Reconstruction Playbook

## Scope

Industrial smart street lamps with:
- plinth/service base;
- vertical mast;
- elbow/structural head transition;
- luminaire shell;
- sensor housing;
- diffuser/LED array;
- integrated trim and emissive strips.

## Recommended Shape Graph

```text
G0 LAMP_ENVELOPE
G1 FOOT / PLINTH / SHOULDER / POLE / ARM / ELBOW
G2 SENSOR_HOUSING / LED_ENGINE / MAJOR_TRIM
G3 SERVICE_HATCHES / SEAMS / ACCENT_CHANNELS / SENSOR_LENSES
G4 EDGE_FAMILIES
G5 MATERIAL / BRANDING / MICRODETAIL
```

## Head rule

Never treat the head as `rounded box + light` when detail references show separate shell cuts, sensor cap, trim ring, diffuser bezel or layered terminations.

Create appearance owners for:
- head top break lines;
- sensor-shell boundary;
- sensor ring/trim sequence;
- underside diffuser bezel;
- accent-strip path and termination;
- elbow/head junction.

## Conflict rule

Street-lamp concept sheets often exaggerate the head in FRONT/SIDE views for readability. Resolve:
- global dimensions from explicit dimensions / calibrated views;
- local shell cuts from detail views;
- junction intent from detail + hero;
- never let one view globally override the others.

## RDL0

Render only base/pole/head envelope in neutral grey. Verify height, base footprint and head projection.

## RDL1

Build and accept sequentially:
1. foot;
2. plinth;
3. shoulder;
4. pole;
5. arm/head mass;
6. elbow junction.

Do not build sensor, LED array or emissive strips before all required G1 nodes pass.

## Detail closure

Before RDL5 acceptance inventory all visible head/base cuts, hatches, fasteners, vents, branding and emissive terminations. Missing MUST head cuts are not cosmetic TODOs.
