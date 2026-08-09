# Asset Placement and Anchors

## Purpose

Make important transforms reference-derived and testable.

An anchor may own:
- position;
- orientation/facing;
- scale;
- wall/ceiling/floor attachment;
- reference camera projection;
- zone membership.

HERO/fixed assets use explicit anchors. Loose decorative scatter is downstream.

Example:

```yaml
anchor_id: A_BAR_MAIN
asset_id: BAR_MAIN
zone: BAR_ZONE
position_mm: [6200, 4100, 0]
yaw_deg: 90
authority: LOCATION_HERO_01
importance: HERO
```
