# Axisymmetric Profile Asset Primitive

## Skill ID

`AXISYMMETRIC_PROFILE`

## Purpose

Build rotationally symmetric hard-surface parts from an explicit 2D radius/height profile revolved around a known axis.

Typical assets/features:
- bollards;
- posts;
- cylindrical housings;
- caps and collars;
- light rings;
- bases;
- round knobs and service rings.

Use this skill when the design is defined primarily by stacked radial profile changes rather than arbitrary surface sculpting.

## Why this is a semantic primitive

A profile revolution guarantees by construction:
- shared center axis;
- exact radii;
- deterministic height transitions;
- repeatable circumferential segmentation;
- predictable triangle cost;
- straightforward cylindrical UVs.

Do not rebuild the same `lathe()`/revolve helper inside every asset script.

## Input contract

```yaml
axisymmetric_profile:
  feature_id: F001
  object_name: BOL_MainBody
  axis: Z
  unit: mm
  segments: 32
  profile:
    - [70.0, 66.0]
    - [70.0, 954.0]
  closed_profile: false
  cap_bottom: false
  cap_top: false
  smoothing: AUTO_BY_PROFILE
  uv_mode: CYLINDRICAL_ARC_LENGTH
```

A profile point is `[radius, axis_position]`.

Optional:
- explicit corner fillet radii;
- per-segment material bands;
- start angle;
- seam angle;
- cap policy;
- normal/sharp-edge policy.

## Preconditions

- axis and origin are known;
- radial dimensions are LOCKED/HIGH confidence or explicitly provisional;
- no required feature breaks rotational symmetry inside this primitive;
- segment count satisfies silhouette and triangle budget.

Asymmetric features such as service panels, logos or local emitters are separate feature owners added after the master rotational geometry is accepted.

## Segment selection

Choose circumference segments from:
- projected silhouette size;
- target LOD;
- radius;
- expected viewing distance;
- triangle budget.

Do not increase segmentation because a local asymmetric detail needs more topology. Keep local detail separate when possible.

For a small game-ready civic prop, 24–32 segments is often sufficient, but the actual contract/QA result wins.

## Fillet/bevel policy

Prefer fillets encoded directly in the radial profile when:
- the radius is dimension-critical;
- modifier order would make bevel width unstable;
- the part is fully rotationally symmetric.

Use a normal Bevel modifier when editability or downstream variation is more important and the modifier can be validated reliably.

Do not create unnecessary profile rings. Every extra radial profile point multiplies around the circumference and can dominate triangle count.

## UV policy

For the revolved side wall:
- U = normalized angle around axis;
- V = normalized or physical arc length along the profile.

This produces deterministic orientation and avoids selection-dependent UV operators.

Caps require a separate planar/radial mapping policy.

## Topology contract

Each generated object must explicitly declare one of:

```text
CLOSED_SOLID
OPEN_ASSEMBLY_PART
SURFACE_DETAIL
```

`CLOSED_SOLID` requires zero boundary/non-manifold edges.

`OPEN_ASSEMBLY_PART` is allowed only when the open boundary is intentionally sealed/occluded by another owned assembly feature and the Game Asset Contract allows it.

Never report a general `mesh PASS` while boundary edges exist and topology intent is unspecified.

## Postconditions

Validate:
- axis center deviation;
- min/max radius;
- min/max Z/axis position;
- total dimensions;
- circumferential continuity;
- duplicate vertices;
- zero-area faces;
- boundary edges against topology intent;
- UV existence;
- triangle count.

## Asymmetric feature handoff

After the rotational master passes:

```text
service panel -> dedicated curved-surface/local-detail strategy
radial bolt pattern -> radial repetition strategy
logo/serial -> decal
local base emitter -> local feature owner
```

Do not distort the rotational master simply to accommodate these details.

## Candidate executor

Canonical candidate implementation:

`executors/axisymmetric_profile.py`

Until that implementation is benchmarked in the active Blender runtime, registry maturity remains `CONTRACT_READY`.
