# Vegetation LOD, Leaf Cards and Impostors

## Principle

Do not use the same reduction method for trunk, branches and foliage.

## Woody plants

- preserve trunk silhouette longest;
- simplify branch hierarchy by screen importance;
- merge/remove twigs before primary branches;
- transition dense leaf geometry to clustered cards;
- background may use whole-plant impostor/billboard if engine policy supports it.

## Small plants

- source leaf/grass meshes remain instanced through authoring;
- reduce clump variation count before realizing millions of primitives;
- share card atlas where possible.

## LOD invariants

Across LODs preserve:
- ground/root contact point;
- major crown envelope;
- species/variant identity;
- wind attribute semantics;
- material family/atlas contract;
- pivot/orientation.

## Validation

Check triangle/material budgets, silhouette drift from representative views and runtime package attributes. LOD success never repairs a failed botanical/composition gate.
