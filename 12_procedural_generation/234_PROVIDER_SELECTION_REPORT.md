# Provider Selection Report

## Purpose

Make provider selection auditable. The report is required before a fallback generator is accepted for procedural/environment content.

## Required report sections

```text
RUNTIME
READY ASSET SOURCES
PROCEDURAL GENERATORS
EXTERNAL GENERATORS
UTILITIES
BUILT-IN BACKENDS
REQUESTED DOMAIN
CANDIDATES / REJECTIONS
SELECTED BACKEND
FALLBACK REASON
```

## Mandatory candidate visibility

Every discovered provider relevant to the broad task family must be present, even if rejected.

For a vegetation request with installed Sapling, IvyGen and Sverchok, a legal report can say:

```text
Sapling Tree Gen 0.3.7   DISCOVERED  TREE             REJECTED: domain mismatch (GRASS)
IvyGen 0.1.5             DISCOVERED  VINE/GROWTH      REJECTED: domain mismatch (GRASS)
Sverchok 1.4.0           DISCOVERED  GENERIC_PROC     ELIGIBLE/PROBE_REQUIRED
Geometry Nodes 5.1       BUILTIN     GENERIC_PROC     ELIGIBLE
```

It cannot omit them and report only `no vegetation library`.

## Fallback proof

Custom/native generation is legal only after the report proves why stronger specialized or ready-asset sources were not selected.

If discovery mismatches user/project-declared installed providers, selection is `BLOCKED`, not fallback.