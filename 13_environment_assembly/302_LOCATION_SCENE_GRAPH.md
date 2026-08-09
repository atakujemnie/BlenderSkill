# Location Scene Graph

## Purpose

Represent the semantic hierarchy of a location separately from Blender Collections/Object parenting.

## Node kinds

```text
LOCATION
ZONE
SYSTEM
ASSET
INSTANCE
```

## Required node fields

```yaml
id: stable_id
kind: LOCATION|ZONE|SYSTEM|ASSET|INSTANCE
parent: stable_id|null
state: MISSING|PROXY|BUILDING|BUILT_UNVERIFIED|ACCEPTED|INSTANCED|BLOCKED|FAIL
importance: HERO|MID|BACKGROUND|TECHNICAL
references: []
dependencies: []
```

## Laws

- exactly one LOCATION root;
- no cycles;
- every non-root has a valid parent;
- INSTANCE points to a source ASSET;
- final INSTANCE source must be `ACCEPTED`;
- graph is persistent and revisioned.

Canonical executor: `executors/location_scene_graph.py`.
