from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET_VERSION = "0.19.0"
TARGET_BENCHMARK = "07_examples/89_LAFAR_PRODUCTION_STUDIO_V019_REGRESSION_BENCHMARK.md"


def main() -> None:
    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    system_prompt = (ROOT / "06_prompts/60_SYSTEM_PROMPT.md").read_text(encoding="utf-8")
    runtime_index = json.loads((ROOT / "_RUNTIME_INDEX.json").read_text(encoding="utf-8"))

    errors: list[str] = []
    if manifest.get("version") != TARGET_VERSION:
        errors.append("MANIFEST_VERSION_MISMATCH")
    if int(manifest.get("manifest_schema_version", 0)) != 2:
        errors.append("MANIFEST_SCHEMA_NOT_V2")
    if manifest.get("benchmark") != TARGET_BENCHMARK:
        errors.append("CANONICAL_BENCHMARK_MISMATCH")
    if not re.search(r"\bv?0\.19\.0\b", readme):
        errors.append("README_VERSION_MISSING")
    if not re.search(r"(?:^|\n)#+\s*(?:\[)?0\.19\.0", changelog):
        errors.append("CHANGELOG_VERSION_MISSING")
    if "0.19.0" not in system_prompt:
        errors.append("SYSTEM_PROMPT_VERSION_MISSING")
    if runtime_index.get("library_version") != TARGET_VERSION:
        errors.append("RUNTIME_INDEX_VERSION_MISMATCH")
    if runtime_index.get("canonical_benchmark") != TARGET_BENCHMARK:
        errors.append("RUNTIME_INDEX_BENCHMARK_MISMATCH")

    if errors:
        raise SystemExit(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
    print(json.dumps({"status": "PASS", "version": TARGET_VERSION}))


if __name__ == "__main__":
    main()
