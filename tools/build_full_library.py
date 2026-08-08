from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"
OUTPUT = ROOT / "_FULL_LIBRARY.md"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    modules = manifest["modules"]

    declared_count = int(manifest.get("module_count", -1))
    actual_count = len(modules)
    if declared_count != actual_count:
        raise ValueError(
            f"MANIFEST module_count mismatch: declared={declared_count} actual={actual_count}"
        )

    duplicates = sorted({rel for rel in modules if modules.count(rel) > 1})
    if duplicates:
        raise ValueError(f"Duplicate manifest modules: {duplicates}")

    parts = [
        f"# Blender AI Agent Library v{manifest['version']} — Full compiled snapshot\n\n",
        "> GENERATED FILE. Do not edit directly. Canonical source: modular files listed in MANIFEST.json.\n",
    ]

    for rel in modules:
        path = ROOT / rel
        if not path.exists():
            raise FileNotFoundError(f"Missing manifest module: {rel}")
        parts.append(f"\n\n---\n\n## FILE: `{rel}`\n\n")
        parts.append(path.read_text(encoding="utf-8"))

    OUTPUT.write_text("".join(parts), encoding="utf-8")
    print(f"Generated {OUTPUT} from {actual_count} modules")


if __name__ == "__main__":
    main()
