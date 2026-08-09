from __future__ import annotations

import json
from pathlib import Path

from upgrade_v016_metadata import main as promote_v016

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
ROUTER = ROOT / "00_governance" / "04_KNOWLEDGE_ROUTER.md"
REGISTRY = ROOT / "00_governance" / "05_SEMANTIC_SKILL_REGISTRY.md"
SYSTEM_PROMPT = ROOT / "06_prompts" / "60_SYSTEM_PROMPT.md"

VERSION = "0.17.0"
BENCHMARK = "07_examples/86_LAFAR_PROVIDER_DISCOVERY_V017_REGRESSION_BENCHMARK.md"
NEW_MODULES = [
    "00_governance/13_PROVIDER_DISCOVERY_EXTENSION_V017.md",
    "00_governance/14_PROVIDER_DISCOVERY_SKILL_REGISTRY_V017.md",
    "06_prompts/72_PROVIDER_DISCOVERY_AND_SELECTION_PROMPT.md",
    BENCHMARK,
    "12_procedural_generation/230_INSTALLED_PROVIDER_INVENTORY.md",
    "12_procedural_generation/231_PROVIDER_CLASSIFICATION_TAXONOMY.md",
    "12_procedural_generation/232_RUNTIME_ADDON_DISCOVERY.md",
    "12_procedural_generation/233_PROVIDER_CAPABILITY_PROBE_MATRIX.md",
    "12_procedural_generation/234_PROVIDER_SELECTION_REPORT.md",
    "12_procedural_generation/235_DISCOVERY_MISMATCH_AND_EXPECTED_PROVIDER_GATE.md",
    "12_procedural_generation/236_VEGETATION_PROVIDER_ROUTING.md",
]

README_SECTION = '''## v0.17 runtime provider discovery and selection transparency

v0.17 fixes the provider-discovery failure exposed by the Lafar planter workflow. BlenderSkill no longer treats an empty ready-made vegetation Asset Library as proof that no procedural providers are installed.

```text
active Blender runtime
-> installed/enabled add-on + Asset Library discovery
-> normalized source buckets
-> expected-provider mismatch gate when user/project supplied known installations
-> provider-specific execution probe
-> requested-domain + quality suitability
-> mandatory provider selection report
-> selected backend or explicit BLOCKED
```

The inventory distinguishes `READY_ASSET_SOURCE`, `PROCEDURAL_GENERATOR`, `EXTERNAL_GENERATOR`, `UTILITY` and `BUILTIN_BACKEND`. Relevant discovered providers remain visible even when rejected. A custom fallback is illegal when an expected installed provider disappeared from discovery.

Canonical regression: **Benchmark 86 — Lafar Provider Discovery v0.17**.

'''

CHANGELOG_SECTION = '''## 0.17.0

v0.17.0 is the **Runtime Provider Discovery + Capability Inventory + Selection Transparency** release.

Key changes:
- added Blender-side discovery of enabled/discoverable add-ons/extensions plus registered Asset Libraries;
- separated ready Asset Libraries from procedural generators, external generators, utilities and built-in backends;
- added normalized identity/classification for Sapling, IvyGen, A.N.T. Landscape, Sverchok, MPFB, Meshy, Geo Nodes Guide and MCP;
- added `EXPECTED_PROVIDER_GATE`: user/project-declared installed providers cannot silently disappear from discovery;
- added explicit discovery/probe/domain/quality/selection state separation;
- added mandatory `PROVIDER_SELECTION_REPORT` showing relevant rejected providers and reasons;
- added vegetation routing that keeps Sapling/IvyGen/Sverchok visible even when no ready vegetation library exists;
- changed NodeToPython policy to optional reference/development tool rather than BlenderSkill 5.1 runtime dependency;
- added Benchmark 86 and adversarial provider-discovery regression tests.

Canonical benchmark: **86 — Lafar Provider Discovery v0.17 Regression**.

'''

ROUTER_SECTION = '''## v0.17 installed-provider discovery precedence

Before procedural/environment provider selection:

```text
BLENDER_RUNTIME_ADDON_DISCOVERY
-> INSTALLED_PROVIDER_DISCOVERY
-> EXPECTED_PROVIDER_GATE when expected installations are known
-> provider capability probes
-> PROVIDER_SELECTION_REPORT
-> provider quality/route selection
```

Do not route `Asset Library empty` to `no provider`. Keep ready assets, generators, external services, utilities and built-ins as separate evidence buckets.

If an expected installed provider is missing from normalized discovery, stop on `DISCOVERY_MISMATCH`; do not silently fall back to a custom generator.

---

'''

REGISTRY_SECTION = '''## v0.17 provider-discovery registry precedence

The detailed v0.17 registry is `00_governance/14_PROVIDER_DISCOVERY_SKILL_REGISTRY_V017.md`.

| Skill ID | Executor | Maturity |
|---|---|---|
| `INSTALLED_PROVIDER_DISCOVERY` | `executors/blender_addon_inventory.py` + `executors/installed_provider_inventory.py` | EXECUTOR_READY |
| `EXPECTED_PROVIDER_GATE` | `executors/expected_provider_gate.py` | EXECUTOR_READY |
| `PROVIDER_SELECTION_REPORT` | `executors/provider_selection_report.py` | EXECUTOR_READY |
| `PROVIDER_CAPABILITY_PROBE_MATRIX` | provider-specific adapters + `12_procedural_generation/233` | CONTRACT_READY |
| `VEGETATION_PROVIDER_ROUTE` | `12_procedural_generation/236` | CONTRACT_READY |

For procedural/environment content, these precede v0.14 provider-quality selection and any custom fallback.

'''

SYSTEM_SECTION = '''## 0.17 provider-discovery precedence

For procedural/environment work where installed providers may help:
- inspect the active Blender runtime; do not infer installed add-ons from an empty Asset Library directory;
- separate ready asset sources, procedural generators, external generators, utilities and built-in backends;
- if the user/project names installed providers, treat that list as expected evidence and run `EXPECTED_PROVIDER_GATE`;
- missing expected providers are `DISCOVERY_MISMATCH`, not permission to fall back;
- discovered-but-untested providers are `PROBE_REQUIRED`, not `UNAVAILABLE`;
- produce `PROVIDER_SELECTION_REPORT` before custom/native fallback, including relevant rejected providers and reasons.

`READY_ASSET_SOURCE: NONE` must never be summarized as `NO_PROVIDERS` when generators/backends are present.

'''


def update_manifest() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data["version"] = VERSION
    data["provider_discovery_version"] = VERSION
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
        "**v0.16.0 — persistent location design systems, reusable visual language and canonical asset libraries.**",
        "**v0.17.0 — runtime provider discovery, capability inventory and selection transparency.**",
    )
    text = text.replace(
        "- NodeToPython — preferred node-graph-to-Python compiler when installed and probed; generated Python should normally remove the runtime compiler dependency.",
        "- NodeToPython — optional reference/development tool only; it is not a required BlenderSkill 5.1 runtime dependency.",
    )
    if "## v0.17 runtime provider discovery and selection transparency" not in text:
        marker = "## v0.16 persistent Location Design Systems"
        text = text.replace(marker, README_SECTION + marker)
    README.write_text(text, encoding="utf-8")


def update_changelog() -> None:
    text = CHANGELOG.read_text(encoding="utf-8")
    if "## 0.17.0" not in text:
        text = text.replace("# Changelog\n\n", "# Changelog\n\n" + CHANGELOG_SECTION)
    CHANGELOG.write_text(text, encoding="utf-8")


def prepend_once(path: Path, header: str, section: str, marker: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker not in text:
        text = text.replace(header, header + section, 1)
        path.write_text(text, encoding="utf-8")


def update_router_registry_prompt() -> None:
    prepend_once(ROUTER, "# Knowledge Router\n\n", ROUTER_SECTION, "## v0.17 installed-provider discovery precedence")
    prepend_once(REGISTRY, "# Semantic Skill Registry\n\n", REGISTRY_SECTION, "## v0.17 provider-discovery registry precedence")
    text = SYSTEM_PROMPT.read_text(encoding="utf-8")
    text = text.replace("# System Prompt — Blender Asset and Location Agent v0.16", "# System Prompt — Blender Asset and Location Agent v0.17")
    if "## 0.17 provider-discovery precedence" not in text:
        insert_before = "## 0.16 design-system precedence"
        text = text.replace(insert_before, SYSTEM_SECTION + insert_before, 1)
    SYSTEM_PROMPT.write_text(text, encoding="utf-8")


def main() -> None:
    promote_v016()
    update_manifest()
    update_readme()
    update_changelog()
    update_router_registry_prompt()
    print("Promoted canonical metadata to v0.17.0")


if __name__ == "__main__":
    main()
