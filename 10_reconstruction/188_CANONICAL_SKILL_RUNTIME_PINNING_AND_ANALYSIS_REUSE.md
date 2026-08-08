# Canonical Skill Runtime Pinning and Analysis Reuse

## Purpose

A project must not unknowingly execute a stale embedded copy of BlenderSkill while analysis reads a different checkout.

The Street Lamp run referenced both `BlenderSkill_main` and a project-local `blenderskill/` copy. They were synchronized during that run, but the architecture permits silent divergence.

## Runtime pin

Every benchmark/project execution records:

```yaml
skill_runtime:
  version: 0.11.0
  commit: <canonical commit>
  source_path: <single active executor root>
  active_duplicate_roots: []
```

Mismatch with the task's expected release is a hard preflight FAIL.

## One active executor root

Multiple copies may exist on disk for history or development, but only one executor root may be active in `sys.path`/tool routing for a run.

## Analysis helper reuse

The Lamp run also produced many one-off `card_scanN.py` helpers. Before creating a local scanner, search the Semantic Skill Registry and `executors/` for:
- reference measurement;
- view/crop registration;
- silhouette mask;
- landmark projection;
- conflict arbitration;
- appearance owner validation.

Local analysis code is allowed for asset-specific extraction, but reusable primitives must migrate into canonical executors after a benchmark proves their generality.

## Canonical executor

`executors/runtime_source_pin.py` validates runtime version/commit/source-root integrity.
