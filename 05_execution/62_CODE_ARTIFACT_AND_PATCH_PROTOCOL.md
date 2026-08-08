# Code Artifact and Patch Protocol

## Purpose

Generated Blender Python is an executable artifact, not conversational prose.

The language model must not repeatedly place complete build scripts, complete QA scripts or large patches into its own reasoning context when the file already exists on disk.

## Core rule

```text
plan in context
-> write/update artifact on disk
-> execute artifact
-> return compact result
-> inspect only the failing symbol/range
```

## File-first policy

If generated code is more than roughly 120 lines or contains reusable helpers, write it to a file and treat the path as persistent state.

After creation, return only:
- path;
- changed symbols/functions;
- approximate line count;
- execution status;
- compact diagnostics.

Do not echo the complete source unless the user explicitly asks to see it.

## Patch policy

For an existing script:

1. identify the failing function or constant;
2. read only the required range;
3. apply the smallest coherent patch;
4. report the changed symbols and reason;
5. execute tests/validation.

Do not re-read or re-print the entire file after every edit.

## Tool output contract

Preferred result:

```yaml
code_artifact:
  path: build_asset.py
  action: PATCHED
  changed_symbols:
    - build_base_accent
    - ACCENT_DEPTH
  lines_touched: 18
  syntax: PASS
  execution: PASS
  validation:
    visible_pixels: 214
    mesh_issues: 0
```

Not acceptable by default:
- full 600-line source after creation;
- full source after a 5-line patch;
- complete unified diff containing unrelated context;
- repeated unchanged function bodies;
- long stderr/stdout when a compact error classification is sufficient.

## Read budget

Read source in this order:

```text
symbol index / grep
-> targeted line range
-> local dependency function
-> whole file only when architecture cannot be inferred otherwise
```

## Generated helper reuse

Before writing a helper such as:
- lathe/profile revolution;
- fillet generation;
- radial repetition;
- mesh validation;
- QA scene isolation;
- reference measurement;

check the Semantic Skill Registry and `executors/` directory.

If a compatible reusable executor exists, import/use it instead of generating another local implementation.

## Artifact persistence

Persist:
- build script path;
- QA script path;
- last successful execution hash/mtime when available;
- produced asset collection/object IDs;
- validation summary.

A later phase should reference the artifact, not reconstruct its source from conversation history.

## Failure diagnostics

On failure, return:
- error class;
- file/function/line when available;
- relevant state;
- smallest required source range.

Raw stack traces may be retained on disk. The LLM should normally receive only the decisive portion.

## Token objective

Code generation should consume tokens for design decisions, not for transporting unchanged source code between tools and the model.
