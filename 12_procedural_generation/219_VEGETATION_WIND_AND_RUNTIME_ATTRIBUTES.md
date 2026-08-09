# Vegetation Wind and Runtime Attributes

## Goal

Separate authored vegetation structure from engine-specific wind simulation while preserving enough semantic data for runtime animation.

## Canonical attributes

At authoring/runtime handoff use stable semantics such as:
- `wind_weight` — normalized flexibility/influence;
- `wind_phase` — variation phase;
- `semantic_part_id` — trunk/branch/leaf/etc.;
- optional branch hierarchy/depth;
- optional stiffness or anchor distance.

Exact attribute names may be mapped by engine profile, but semantics remain stable.

## Weight policy

Typical gradient:

```text
root/trunk base -> near 0
upper trunk/primary branch -> low
small branches -> medium
leaves/tips -> high
```

Alien flora may invert or stylize this, but must declare the rule.

## Runtime boundary

Authoring proof requires attributes to exist and be coherent. Actual shader deformation, gust fields or physics are Level C/D runtime concerns and require engine-side proof.
