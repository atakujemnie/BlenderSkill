from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"

VERSION = "0.15.0"
BENCHMARK = "07_examples/84_LAFAR_RESTAURANT_V015_FULL_LOCATION_REGRESSION_BENCHMARK.md"
NEW_MODULES = [
    "00_governance/09_LOCATION_ASSEMBLY_EXTENSION.md",
    "00_governance/10_LOCATION_SKILL_REGISTRY_V015.md",
    "06_prompts/70_LOCATION_RECONSTRUCTION_PLANNER_PROMPT.md",
    BENCHMARK,
    "13_environment_assembly/300_LOCATION_RECONSTRUCTION_LAYER_INDEX.md",
    "13_environment_assembly/301_LOCATION_REFERENCE_INGESTION.md",
    "13_environment_assembly/302_LOCATION_SCENE_GRAPH.md",
    "13_environment_assembly/303_LOCATION_ASSET_MANIFEST.md",
    "13_environment_assembly/304_LOCATION_DESIGN_SYSTEM.md",
    "13_environment_assembly/305_MODULAR_ARCHITECTURE_ASSEMBLY.md",
    "13_environment_assembly/306_SPACE_ZONING_AND_PROGRAM.md",
    "13_environment_assembly/307_SPATIAL_RELATION_GRAPH.md",
    "13_environment_assembly/308_CIRCULATION_AND_CLEARANCE_CONTRACT.md",
    "13_environment_assembly/309_ASSET_PLACEMENT_AND_ANCHORS.md",
    "13_environment_assembly/310_HERO_ANCHOR_COMPOSITION.md",
    "13_environment_assembly/311_FURNITURE_CLUSTER_GRAMMAR.md",
    "13_environment_assembly/312_LOCATION_INTERPENETRATION_GATE.md",
    "13_environment_assembly/313_LOCATION_MATERIAL_AND_LIGHTING_LANGUAGE.md",
    "13_environment_assembly/314_LOCATION_BUILD_ORDER_AND_STAGE_BARRIERS.md",
    "13_environment_assembly/315_REFERENCE_COMPOSITION_FIDELITY.md",
    "13_environment_assembly/316_LOCATION_COMPLETENESS_GATE.md",
    "13_environment_assembly/317_GAME_READY_LOCATION_PARTITIONING_AND_INSTANCING.md",
    "13_environment_assembly/318_LOCATION_DEFINITION_OF_DONE.md",
]

README_SECTION = '''## v0.15 location reconstruction and environment assembly

v0.15 introduces the hierarchy above single-asset reconstruction. Complete authored interiors/exteriors are now planned and validated as spatial systems rather than as independent object builds.

```text
location references
-> Location Design System
-> Location Scene Graph + Asset Manifest
-> architecture
-> HERO anchors
-> fixed assets
-> furniture clusters
-> spatial relations + circulation/clearance
-> lighting/vegetation/props
-> reference composition fidelity
-> Location Completeness Gate
-> runtime partitioning/instancing
```

Hard final blockers include missing required HERO assets, final proxies, unintended interpenetration, blocked required circulation and failed reference composition. The canonical v0.15 regression is **Benchmark 84 — Lafar Restaurant Full Location Reconstruction**.

'''

CHANGELOG_SECTION = '''## 0.15.0

v0.15.0 is the **Location Reconstruction + Environment Assembly** release, driven by the failed v0.14 Lafar Restaurant full-location build.

Key changes:
- added `13_environment_assembly/` as the hierarchy above single-asset reconstruction;
- added persistent Location Scene Graph (`LOCATION -> ZONE -> SYSTEM -> ASSET -> INSTANCE`);
- added exhaustive Location Asset Manifest with explicit `MISSING/PROXY/BUILDING/ACCEPTED/INSTANCED` state and 100% required HERO closure;
- made Location Design System mandatory before asset proliferation, reusing the v0.14 persistent material-language library;
- added architecture-first assembly, zoning, placement anchors, HERO composition and furniture-cluster grammar;
- added semantic Spatial Relation Graph and explicit circulation/clearance validation;
- added non-compensating location interpenetration, reference-composition and completeness gates;
- added location completion levels and runtime partitioning/instancing boundary;
- upgraded `06_prompts/60_SYSTEM_PROMPT.md` to v0.15 and added the dedicated location planner prompt;
- added pure-Python decision validators and adversarial v0.15 regression tests;
- added Benchmark 84 — Lafar Restaurant Full Location Reconstruction.

Canonical benchmark: **84 — Lafar Restaurant v0.15 Full Location Reconstruction Regression**.

'''


def update_manifest() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data["version"] = VERSION
    data["environment_assembly_layer"] = "13_environment_assembly"
    data["benchmark"] = BENCHMARK
    benchmarks = list(data.get("benchmarks", []))
    if BENCHMARK not in benchmarks:
        benchmarks.append(BENCHMARK)
    data["benchmarks"] = benchmarks
    modules = list(data.get("modules", []))
    for module in NEW_MODULES:
        if module not in modules:
            modules.append(module)
    data["modules"] = modules
    data["module_count"] = len(modules)
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_readme() -> None:
    text = README.read_text(encoding="utf-8")
    text = text.replace(
        "**v0.14.0 — visual quality, library-first asset selection, persistent location material language and context efficiency.**",
        "**v0.15.0 — full-location reconstruction, environment assembly, spatial relations and completeness gates.**",
    )
    if "## v0.15 location reconstruction and environment assembly" not in text:
        marker = "## v0.14 quality/material additions"
        text = text.replace(marker, README_SECTION + marker)
    README.write_text(text, encoding="utf-8")


def update_changelog() -> None:
    text = CHANGELOG.read_text(encoding="utf-8")
    if "## 0.15.0" not in text:
        text = text.replace("# Changelog\n\n", "# Changelog\n\n" + CHANGELOG_SECTION)
    CHANGELOG.write_text(text, encoding="utf-8")


def main() -> None:
    update_manifest()
    update_readme()
    update_changelog()
    print("Promoted canonical metadata to v0.15.0")


if __name__ == "__main__":
    main()
