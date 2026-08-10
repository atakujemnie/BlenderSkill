from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"
OUTPUT = ROOT / "_RUNTIME_INDEX.json"
MAX_BYTES = 150 * 1024


def build_index(manifest: dict) -> dict:
    skills = []
    for item in manifest.get("skills", []) or []:
        skills.append(
            {
                "skill_id": item.get("id"),
                "purpose": item.get("purpose", ""),
                "contract": item.get("contract"),
                "executor": item.get("executor"),
                "maturity": item.get("maturity", "CONTRACT_READY"),
                "dependencies": sorted(item.get("dependencies", []) or []),
                "relevant_benchmark": item.get("benchmark"),
                "routing_keywords": sorted(item.get("routing_keywords", []) or []),
            }
        )
    skills.sort(key=lambda item: str(item.get("skill_id") or ""))
    return {
        "runtime_index_schema_version": 1,
        "library_version": manifest.get("version"),
        "canonical_benchmark": manifest.get("benchmark"),
        "skills": skills,
    }


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload = json.dumps(build_index(manifest), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    size = len(payload.encode("utf-8"))
    if size >= MAX_BYTES:
        raise ValueError(f"Runtime index too large: {size} bytes >= {MAX_BYTES}")
    OUTPUT.write_text(payload, encoding="utf-8")
    print(f"Generated {OUTPUT} ({size} bytes)")


if __name__ == "__main__":
    main()
