from __future__ import annotations

"""Idempotently promote canonical repository metadata/routing to v0.14.0."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NEW_MODULES = [
    "03_modeling/46_LOCATION_MATERIAL_LANGUAGE_AND_LIBRARY_FIRST_AUTHORING.md",
    "05_execution/79_VISUAL_QUALITY_AND_CONTEXT_BUDGET_GATE.md",
    "07_examples/83_LAFAR_PLANTER_V014_VISUAL_QUALITY_AND_EFFICIENCY_REGRESSION_BENCHMARK.md",
    "12_procedural_generation/220_LOCATION_MATERIAL_LANGUAGE_LIBRARY.md",
    "12_procedural_generation/221_PROVIDER_CLASSIFICATION_AND_QUALITY_TIERS.md",
    "12_procedural_generation/222_PLANTING_COMPOSITION_GRAMMAR.md",
    "12_procedural_generation/223_VEGETATION_SOURCE_QUALITY_AND_LIBRARY_FIRST_POLICY.md",
    "12_procedural_generation/224_PLANTING_REFERENCE_COMPOSITION_FIDELITY.md",
]
BENCHMARK = "07_examples/83_LAFAR_PLANTER_V014_VISUAL_QUALITY_AND_EFFICIENCY_REGRESSION_BENCHMARK.md"


def write_if_changed(path: Path, text: str) -> None:
    old = path.read_text(encoding="utf-8")
    if old != text:
        path.write_text(text, encoding="utf-8")


def upgrade_manifest() -> None:
    path = ROOT / "MANIFEST.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = "0.14.0"
    data["benchmark"] = BENCHMARK
    if BENCHMARK not in data["benchmarks"]:
        data["benchmarks"].append(BENCHMARK)
    for module in NEW_MODULES:
        if module not in data["modules"]:
            data["modules"].append(module)
    data["module_count"] = len(data["modules"])
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def upgrade_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "**v0.13.0 — deterministic procedural vegetation, generator providers and planter composition.**",
        "**v0.14.0 — visual quality, library-first asset selection, persistent location material language and context efficiency.**",
    )
    marker = "## v0.14 quality/material additions"
    if marker not in text:
        anchor = "v0.13 adds a second authoring domain beside reference reconstruction: procedural organic/environment generation. The first benchmark target is a Lafar planter containing a reconstructed hard-surface container plus generated vegetation.\n"
        addition = """

## v0.14 quality/material additions

v0.14 keeps the v0.13 deterministic vegetation contracts but adds a production-quality barrier before runtime finishing:

```text
location material library find-or-create
-> installed asset/provider discovery
-> runtime probe
-> quality-tier selection
-> physical composition
-> planting massing/composition quality
-> reference composition fidelity when applicable
-> shared material-language reuse/adaptation
-> early visual-quality barrier
-> runtime finishing
-> context-budget gate
```

For the RPG profile, location material language defaults to:
`<repo>/Assets/GameAssets/Materials/Locations/<location_id>/`.
Every material task must return the resolved path. Existing compatible families are reused before any new texture generation; new approved families are written back to the same location library.

Provider compatibility and provider quality are separate. A runtime-safe C-tier procedural generator cannot displace an installed A-tier source for a HERO asset merely because it is available first.

The v0.14 Lafar regression target reduces the previous approximately 80k-token three-planter run to <=30k tokens (stretch <=20k) by moving reusable probing, selection, material-library and composition logic into canonical executors.
"""
        text = text.replace(anchor, anchor + addition)
    write_if_changed(path, text)


def upgrade_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    if "## 0.14.0" not in text:
        entry = """## 0.14.0

v0.14.0 is the **visual-quality + library-first + persistent location-material-language + context-efficiency** release, driven by human review of the v0.13 Lafar planter benchmark.

Key changes:
- runtime provider compatibility is separated from visual quality tier and usage suitability;
- final vegetation is library-first: project/licensed quality sources outrank generic procedural fallback when compatible;
- planting composition now owns masses, height layers, rhythm, negative space, periodicity and clone visibility in addition to physical root/stem/container fit;
- reference-driven planting gains compact occupancy/height/mass composition fidelity;
- every location resolves or bootstraps one persistent material-language library and returns its exact path for subsequent prompts;
- material authoring reuses/adapts location families before generating new textures and adds semantic wetness/dirt/contact/wear breakup;
- early visual-quality barrier blocks expensive runtime finishing for visually unresolved assets;
- context-budget gate targets <=30k tokens for the three-planter regression (stretch <=20k) and promotes repeated helpers into canonical executors;
- fixed `PROCEDURAL_GENERATOR_PROVIDER` to emit its canonical `validator_id` directly;
- added benchmark 83 and v0.14 regression tests.

Canonical benchmark: **83 — Lafar Planter v0.14 Visual Quality and Efficiency Regression**.

"""
        text = text.replace("# Changelog\n\n", "# Changelog\n\n" + entry, 1)
    write_if_changed(path, text)


def upgrade_router() -> None:
    path = ROOT / "00_governance" / "04_KNOWLEDGE_ROUTER.md"
    text = path.read_text(encoding="utf-8")
    if "## v0.14 visual-quality routing override" not in text:
        block = """## v0.14 visual-quality routing override

This section has precedence for final environment/vegetation/material authoring while preserving v0.12 physical-integrity rules.

```text
project/location preflight
-> LOCATION_MATERIAL_LIBRARY find-or-create and persist returned path
-> discover installed providers/asset libraries
-> PROCEDURAL_GENERATOR_PROVIDER runtime probe where executable
-> PROVIDER_QUALITY_SELECT for HERO/MID/BACKGROUND usage
-> source/variation generation
-> PLANTER_VEGETATION_COMPOSITION physical gate when applicable
-> PLANTING_COMPOSITION_QUALITY
-> reference composition fidelity when reference-driven
-> location material-language reuse/adaptation
-> early visual-quality barrier
-> only then LOD/bake/export/runtime
-> CONTEXT_BUDGET_GATE
```

Hard rules:
- do not regenerate a private material language when the location library exists;
- if the location library is absent, create its canonical skeleton/manifest and report the exact path;
- runtime compatibility never implies hero-quality suitability;
- physical placement PASS never implies planting-composition PASS;
- visually unresolved final assets do not proceed to expensive runtime finishing;
- reusable provider/material/composition infrastructure belongs in `executors/`, not repeated project-local scripts.

---

"""
        text = text.replace("# Knowledge Router\n\n", "# Knowledge Router\n\n" + block, 1)
    write_if_changed(path, text)


def upgrade_registry() -> None:
    path = ROOT / "00_governance" / "05_SEMANTIC_SKILL_REGISTRY.md"
    text = path.read_text(encoding="utf-8")
    if "## v0.14 registry additions" not in text:
        anchor = "Do not claim higher maturity without evidence.\n"
        block = """

## v0.14 registry additions

| Skill ID | Purpose | Canonical implementation | Maturity |
|---|---|---|---|
| `LOCATION_MATERIAL_LIBRARY` | resolve/create persistent material language per location and return its path | `12_procedural_generation/220`; `executors/location_material_library.py` | EXECUTOR_READY |
| `PROVIDER_QUALITY_SELECT` | choose visually suitable provider independently of runtime compatibility | `12_procedural_generation/221`; `executors/provider_quality.py` | EXECUTOR_READY |
| `PLANTING_COMPOSITION_QUALITY` | validate masses/layers/coverage/periodicity/clone repetition | `12_procedural_generation/222`; `executors/planting_composition_quality.py` | EXECUTOR_READY |
| `VEGETATION_SOURCE_QUALITY` | enforce library-first quality by usage class | `12_procedural_generation/223` | CONTRACT_READY |
| `PLANTING_REFERENCE_FIDELITY` | compact reference-vs-candidate planting massing proof | `12_procedural_generation/224` | CONTRACT_READY |
| `LOCATION_MATERIAL_AUTHORING` | reuse/adapt shared location material families before creating new ones | `03_modeling/46` | CONTRACT_READY |
| `CONTEXT_BUDGET_GATE` | block excessive context/code churn and reusable-executor misses | `05_execution/79`; `executors/context_budget_gate.py` | EXECUTOR_READY |

v0.13 procedural skills remain canonical and are now explicitly downstream of provider-quality selection when final visual quality matters.
"""
        text = text.replace(anchor, anchor + block, 1)
    write_if_changed(path, text)


def upgrade_profile() -> None:
    path = ROOT / "09_engine" / "profiles" / "RPG_PROJECT_ASSET_PIPELINE_PROFILE.md"
    text = path.read_text(encoding="utf-8")
    needle = "    first_planet_road_modules: <repo>/Assets/GameAssets/City/first_planet/road_kit/modules\n"
    addition = "    location_material_library_root: <repo>/Assets/GameAssets/Materials/Locations\n    location_material_library_pattern: <repo>/Assets/GameAssets/Materials/Locations/<location_id>\n"
    if "location_material_library_root:" not in text:
        text = text.replace(needle, needle + addition, 1)
    if "resolve/create the location material library" not in text:
        marker = "When this profile matches the active project:\n"
        text = text.replace(marker, marker + "- resolve/create the location material library under `<repo>/Assets/GameAssets/Materials/Locations/<location_id>` and return that path to the user;\n- reuse compatible location material families before generating new texture sets;\n", 1)
    write_if_changed(path, text)


if __name__ == "__main__":
    upgrade_manifest()
    upgrade_readme()
    upgrade_changelog()
    upgrade_router()
    upgrade_registry()
    upgrade_profile()
    print("v0.14 canonical metadata upgrade: PASS")
