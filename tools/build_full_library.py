from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"
OUTPUT = ROOT / "_FULL_LIBRARY.md"


def _require_file(rel: str, code: str) -> None:
    path = ROOT / rel
    if not path.is_file():
        raise FileNotFoundError(f"{code}: {rel}")


def validate_manifest(manifest: dict) -> None:
    if int(manifest.get("manifest_schema_version", 0)) != 2:
        raise ValueError("MANIFEST_SCHEMA_VERSION_MUST_BE_2")

    modules = list(manifest.get("modules") or [])
    declared_count = int(manifest.get("module_count", -1))
    if declared_count != len(modules):
        raise ValueError(f"MANIFEST module_count mismatch: declared={declared_count} actual={len(modules)}")

    duplicates = sorted({rel for rel in modules if modules.count(rel) > 1})
    if duplicates:
        raise ValueError(f"Duplicate manifest modules: {duplicates}")
    for rel in modules:
        _require_file(rel, "MISSING_MODULE")

    for rel in manifest.get("benchmarks", []) or []:
        _require_file(str(rel), "MISSING_BENCHMARK")
    canonical = str(manifest.get("benchmark") or "")
    if canonical:
        _require_file(canonical, "MISSING_CANONICAL_BENCHMARK")
        if canonical not in set(manifest.get("benchmarks", []) or []):
            raise ValueError("CANONICAL_BENCHMARK_NOT_DECLARED")

    skill_ids: set[str] = set()
    for skill in manifest.get("skills", []) or []:
        skill_id = str(skill.get("id") or "")
        if not skill_id:
            raise ValueError("SKILL_ID_REQUIRED")
        if skill_id in skill_ids:
            raise ValueError(f"DUPLICATE_SKILL_ID: {skill_id}")
        skill_ids.add(skill_id)
        contract = str(skill.get("contract") or "")
        if contract:
            _require_file(contract, "MISSING_SKILL_CONTRACT")
        executor = str(skill.get("executor") or "")
        if executor:
            _require_file(executor, "MISSING_SKILL_EXECUTOR")

    for entry in manifest.get("executors", []) or []:
        _require_file(str(entry.get("executor") or ""), "MISSING_EXECUTOR")
        contract = str(entry.get("contract") or "")
        if contract:
            _require_file(contract, "MISSING_EXECUTOR_CONTRACT")
        for test in entry.get("tests", []) or []:
            _require_file(str(test), "MISSING_EXECUTOR_TEST")

    for rel in manifest.get("tests", []) or []:
        _require_file(str(rel), "MISSING_TEST")

    artifacts = manifest.get("generated_artifacts", []) or []
    declared_outputs = {str(item.get("path") if isinstance(item, dict) else item) for item in artifacts}
    if "_FULL_LIBRARY.md" not in declared_outputs or "_RUNTIME_INDEX.json" not in declared_outputs:
        raise ValueError("GENERATED_ARTIFACT_DECLARATION_INCOMPLETE")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    modules = list(manifest["modules"])

    parts = [
        f"# Blender AI Agent Library v{manifest['version']} — Full compiled snapshot\n\n",
        "> GENERATED FILE. Do not edit directly. Canonical source: modular files listed in MANIFEST.json.\n",
    ]
    for rel in modules:
        path = ROOT / rel
        parts.append(f"\n\n---\n\n## FILE: `{rel}`\n\n")
        parts.append(path.read_text(encoding="utf-8"))

    OUTPUT.write_text("".join(parts), encoding="utf-8")
    print(f"Generated {OUTPUT} from {len(modules)} modules")


if __name__ == "__main__":
    main()
