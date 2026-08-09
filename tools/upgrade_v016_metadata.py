from __future__ import annotations

import json
from pathlib import Path

from upgrade_v015_metadata import main as promote_v015

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
ROUTER = ROOT / "00_governance" / "04_KNOWLEDGE_ROUTER.md"
REGISTRY = ROOT / "00_governance" / "05_SEMANTIC_SKILL_REGISTRY.md"
SYSTEM_PROMPT = ROOT / "06_prompts" / "60_SYSTEM_PROMPT.md"

VERSION = "0.16.0"
BENCHMARK = "07_examples/85_LAFAR_LOCATION_DESIGN_SYSTEM_V016_REGRESSION_BENCHMARK.md"
NEW_MODULES = [
    "00_governance/11_LOCATION_DESIGN_SYSTEM_EXTENSION.md",
    "00_governance/12_LOCATION_DESIGN_SYSTEM_SKILL_REGISTRY_V016.md",
    "06_prompts/71_LOCATION_DESIGN_SYSTEM_BUILDER_PROMPT.md",
    BENCHMARK,
    "08_scripts/101_LOCATION_DESIGN_SYSTEM_VALIDATION_PATTERN.md",
    "14_design_system/400_LOCATION_DESIGN_SYSTEM_LAYER_INDEX.md",
    "14_design_system/401_DESIGN_SYSTEM_BUILD_AND_BOOTSTRAP.md",
    "14_design_system/402_DESIGN_SYSTEM_DIRECTORY_AND_PATH_CONTRACT.md",
    "14_design_system/403_DESIGN_SYSTEM_MANIFEST_CONTRACT.md",
    "14_design_system/404_DESIGN_SYSTEM_INHERITANCE_AND_OVERRIDES.md",
    "14_design_system/405_RESOURCE_PROVENANCE_PROMOTION_AND_DEDUPLICATION.md",
    "14_design_system/406_MATERIAL_AND_TEXTURE_LANGUAGE.md",
    "14_design_system/407_BRANDING_GRAPHICS_AND_SIGNAGE_LIBRARY.md",
    "14_design_system/408_REUSABLE_COMPONENT_PROFILE_AND_NODEGROUP_LIBRARY.md",
    "14_design_system/409_SHAPE_EDGE_SEAM_AND_DETAIL_LANGUAGE.md",
    "14_design_system/410_WEATHERING_AND_ENVIRONMENT_RESPONSE_LANGUAGE.md",
    "14_design_system/411_LIGHTING_AND_EMISSIVE_LANGUAGE.md",
    "14_design_system/412_BLENDER_ASSET_LIBRARY_PACKAGING.md",
    "14_design_system/413_ASSET_CONSUMPTION_AND_REUSE_PROTOCOL.md",
    "14_design_system/414_DESIGN_SYSTEM_CONFORMANCE_GATE.md",
    "14_design_system/415_DESIGN_SYSTEM_VERSIONING_AND_CHANGE_PROPAGATION.md",
]

README_SECTION = '''## v0.16 persistent Location Design Systems

v0.16 promotes the thin v0.15 Location Design System requirement into a persistent reusable authoring layer. Future assets resolve one canonical location/faction/family language before final appearance instead of recreating materials, logos, components and style rules per asset.

```text
<repo>/Blender/DesignSystems/<location_id>/
-> LOCATION_DESIGN_SYSTEM.md + design_system.json
-> source/provenance registry
-> materials + branding + components + decals + profiles + nodegroups
-> optional canonical Blender Asset Library .blend
-> inheritance: LOCATION -> ORGANIZATION -> FAMILY -> ASSET
-> asset consumption
-> DESIGN_SYSTEM_CONFORMANCE_GATE
```

The v0.14 runtime material library remains linked but separate under `Assets/GameAssets/Materials/Locations/<location_id>`. Canonical resources can be hash-deduplicated/promoted from accepted assets, and future asset prompts receive exact reusable paths rather than regenerating the same visual language.

Canonical regression: **Benchmark 85 — Lafar Location Design System v0.16**.

'''

CHANGELOG_SECTION = '''## 0.16.0

v0.16.0 is the **Persistent Location Design System + Reusable Visual Language** release.

Key changes:
- operationalized the thin v0.15 design-system gate as a persistent source-side layer under `14_design_system/`;
- added find-or-create `LOCATION_DESIGN_SYSTEM_RESOLVE` returning canonical MD/JSON/material/branding/component/Asset-Library paths;
- added machine-readable design-system manifest readiness validation;
- added deterministic Universe/Location/Organization/Family/Asset inheritance with locked-token protection and provenance;
- added hash-deduplicated promotion of reusable logos, textures, decals, profiles and source resources;
- separated source design-system root from the v0.14 runtime location material library;
- added canonical material, branding, component/nodegroup, form/edge/detail, weathering and lighting languages;
- added Blender Asset Library packaging contract for API-driven reuse through `.blend` libraries;
- added asset consumption protocol and non-compensating `DESIGN_SYSTEM_CONFORMANCE_GATE`;
- added design-system version/change propagation semantics;
- fixed the v0.15 CI import-path failure so the location-assembly regression runs from GitHub Actions;
- added Benchmark 85 and pure-Python v0.16 regression tests.

Canonical benchmark: **85 — Lafar Location Design System v0.16 Regression**.

'''

ROUTER_SECTION = '''## v0.16 persistent design-system routing override

For an asset or location assigned to a known location/faction/family, resolve reusable visual language before final appearance:

```text
location identity
-> LOCATION_DESIGN_SYSTEM_RESOLVE
-> bootstrap only if missing
-> DESIGN_SYSTEM_INHERITANCE_RESOLVE
-> compact resolved design context
-> asset/location authoring
-> DESIGN_SYSTEM_CONFORMANCE_GATE
```

Load `14_design_system/400_LOCATION_DESIGN_SYSTEM_LAYER_INDEX.md` and only the relevant domain modules. Do not reload raw logos/textures/reference packs when stable canonical IDs and paths already exist.

Asset-specific technical dimensions remain owned by authoritative asset references. Locked location/organization identity (canonical logo, brand color, material identity etc.) cannot be silently overridden by an asset-local approximation.

---

'''

REGISTRY_SECTION = '''## v0.16 persistent design-system registry precedence

The detailed v0.16 registry is `00_governance/12_LOCATION_DESIGN_SYSTEM_SKILL_REGISTRY_V016.md`.

Canonical new executable skills:

| Skill ID | Executor | Maturity |
|---|---|---|
| `LOCATION_DESIGN_SYSTEM_RESOLVE` | `executors/design_system_resolver.py` | EXECUTOR_READY |
| `LOCATION_DESIGN_SYSTEM_MANIFEST` | `executors/design_system_manifest.py` | EXECUTOR_READY |
| `DESIGN_SYSTEM_INHERITANCE_RESOLVE` | `executors/design_system_inheritance.py` | EXECUTOR_READY |
| `DESIGN_SYSTEM_RESOURCE_PROMOTE` | `executors/design_system_resource_registry.py` | EXECUTOR_READY |
| `DESIGN_SYSTEM_CONFORMANCE_GATE` | `executors/design_system_conformance.py` | EXECUTOR_READY |

For known-location L4/L5/final art-direction work, the resolved design system and conformance gate are upstream of runtime completion.

'''

SYSTEM_SECTION = '''## 0.16 design-system precedence

For any known-location/faction asset before final appearance:
- resolve `14_design_system/400_LOCATION_DESIGN_SYSTEM_LAYER_INDEX.md`;
- call `LOCATION_DESIGN_SYSTEM_RESOLVE`;
- reuse the existing canonical system when present;
- if missing and creation is authorized, bootstrap one canonical root and populate it from authoritative references/accepted assets;
- resolve Location -> Organization -> Family -> Asset inheritance;
- consume canonical material/branding/component/form/light/weathering IDs;
- run `DESIGN_SYSTEM_CONFORMANCE_GATE` before final appearance/runtime closure.

Never redraw a canonical logo or generate another generic equivalent of an existing approved material/component merely because the current asset folder does not contain it.

'''


def update_manifest() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data["version"] = VERSION
    data["design_system_layer"] = "14_design_system"
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
        "**v0.15.0 — full-location reconstruction, environment assembly, spatial relations and completeness gates.**",
        "**v0.16.0 — persistent location design systems, reusable visual language and canonical asset libraries.**",
    )
    if "## v0.16 persistent Location Design Systems" not in text:
        marker = "## v0.15 location reconstruction and environment assembly"
        text = text.replace(marker, README_SECTION + marker)
    README.write_text(text, encoding="utf-8")


def update_changelog() -> None:
    text = CHANGELOG.read_text(encoding="utf-8")
    if "## 0.16.0" not in text:
        text = text.replace("# Changelog\n\n", "# Changelog\n\n" + CHANGELOG_SECTION)
    CHANGELOG.write_text(text, encoding="utf-8")


def prepend_once(path: Path, header: str, section: str, marker: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker not in text:
        text = text.replace(header, header + section, 1)
        path.write_text(text, encoding="utf-8")


def update_router_registry_prompt() -> None:
    prepend_once(ROUTER, "# Knowledge Router\n\n", ROUTER_SECTION, "## v0.16 persistent design-system routing override")
    prepend_once(REGISTRY, "# Semantic Skill Registry\n\n", REGISTRY_SECTION, "## v0.16 persistent design-system registry precedence")
    text = SYSTEM_PROMPT.read_text(encoding="utf-8")
    text = text.replace("# System Prompt — Blender Asset and Location Agent v0.15", "# System Prompt — Blender Asset and Location Agent v0.16")
    if "## 0.16 design-system precedence" not in text:
        text = text.replace("## 0.15 precedence", SYSTEM_SECTION + "## 0.15 precedence", 1)
    SYSTEM_PROMPT.write_text(text, encoding="utf-8")


def main() -> None:
    # v0.15 was committed but its CI promotion failed before metadata/snapshot were pushed.
    # Reapply the idempotent v0.15 promotion first, then layer v0.16 on top.
    promote_v015()
    update_manifest()
    update_readme()
    update_changelog()
    update_router_registry_prompt()
    print("Promoted canonical metadata to v0.16.0")


if __name__ == "__main__":
    main()
