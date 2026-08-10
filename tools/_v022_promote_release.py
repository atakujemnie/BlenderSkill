from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.22.0"
BENCHMARK = "07_examples/92_LAFAR_SERVICE_TERMINAL_VISUAL_FIDELITY_V022_REGRESSION_BENCHMARK.md"
CONTRACT = "15_asset_production/504_VISUAL_FIDELITY_AND_FEATURE_COMPLETION.md"


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def update_pyproject() -> None:
    path = ROOT / "pyproject.toml"
    text = path.read_text(encoding="utf-8")
    text, count = re.subn(r'(?m)^version\s*=\s*"[^"]+"', f'version = "{VERSION}"', text, count=1)
    if count != 1:
        raise SystemExit("PYPROJECT_VERSION_NOT_FOUND")
    path.write_text(text, encoding="utf-8")


def update_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    marker = "## v0.18 Runtime Verification & Contract Convergence"
    if marker not in text:
        raise SystemExit("README_MARKER_NOT_FOUND")
    _old, tail = text.split(marker, 1)
    head = '''> Current production runtime: v0.22.0 — visual fidelity, feature completion and measured geometry proof.

# BlenderSkill

Canonical knowledge repository for the Blender AI Agent Library.

## Current release

**v0.22.0 — Visual Fidelity & Feature Completion.**

v0.22 is driven by the Lafar Public Service Terminal blind test. v0.21 proved placement, envelope, materials and trusted task receipts, but a human could still rate the final reconstruction roughly 3/10 because reference-critical details were omitted or simplified. v0.22 makes visible MUST features explicit production data, requires measured scene proof for deterministic geometry, adds independent multi-view visual review and prevents `STRUCTURAL_GEOMETRY` from being reported as final quality.

Canonical regression: **Benchmark 92 — Lafar Public Service Terminal Visual Fidelity v0.22**.

## v0.22 Visual Fidelity & Feature Completion

```text
reference evidence
-> Feature Contract (MUST / SHOULD / OPTIONAL)
-> component-scoped task pack + QA views
-> representation + deterministic detail primitives
-> measured Blender feature proof
-> structural/details/material/game-ready acceptance levels
-> registered multi-view QA renders
-> independent per-MUST visual review
-> current revision-bound fidelity review
-> final APPROVED
```

Hard rules include: a Boolean must prove material effect, repeated details must prove count/pitch when contracted, newly discovered reference-critical details block final approval until mapped, a global similarity score cannot override a failed MUST feature, and final approval cannot reuse a stale visual review.

'''
    path.write_text(head + marker + tail, encoding="utf-8")


def update_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    if text.startswith("## 0.22.0"):
        return
    entry = '''## 0.22.0 — Visual Fidelity & Feature Completion

- Added machine-enforced `feature_contract` records with `MUST` / `SHOULD` / `OPTIONAL` priorities, reference ownership, representation requirements, counts and measurable scene proof.
- Added `FEATURE_CONTRACT_GATE`; missing reference-critical features, wrong repeat counts, missing proof types or out-of-tolerance feature measurements now fail closed.
- Added first-class deterministic `CYLINDER`, `RING` and `CAPSULE_PRISM` primitives for sensor lenses/rings, fasteners and rounded ventilation slots instead of generic-box approximations.
- Strengthened `BOOLEAN_CUT` / `BOOLEAN_UNION`: the real Blender executor measures evaluated volume before/after and fails when no material effect is observed.
- Scene snapshots now carry compact evaluated-mesh metrics plus `feature_ids` and deterministic `feature_proofs`.
- Added component acceptance levels (`BLOCKOUT` through `FIDELITY`/`FINAL`) and `ASSET_STAGE_COMPLETION_GATE`; structural success can no longer be declared final success.
- Added revisioned `FIDELITY_REVIEW_REPOSITORY` and `VISUAL_FIDELITY_REVIEW_GATE` for independent multi-view review bound to exact asset, scene and reference revisions.
- A global visual score is secondary: every visual MUST feature is reviewed separately, and newly discovered unmapped reference details block final approval.
- Added HTTP endpoints for publishing/reading current fidelity reviews and wired final `APPROVED` stage to current fidelity evidence.
- Preserved component-scoped token budgets while carrying Feature Contract, visual feature map, QA views, edge profiles and materialized reference attachments.
- Added real Blender 5.1 tests for semantic detail primitives and measured feature/Boolean proof.
- Added canonical Benchmark 92 — Lafar Public Service Terminal Visual Fidelity — based directly on the blind terminal reconstruction failure classes.

'''
    path.write_text(entry + text, encoding="utf-8")


def update_system_prompt() -> None:
    path = ROOT / "06_prompts/60_SYSTEM_PROMPT.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("# System Prompt — Blender Asset and Location Agent v0.21.1", "# System Prompt — Blender Asset and Location Agent v0.22.0", 1)
    marker = "## Location design system"
    if marker not in text:
        raise SystemExit("SYSTEM_PROMPT_MARKER_NOT_FOUND")
    block = '''## v0.22 visual fidelity and feature completion

Dla production reference reconstruction po `REFERENCE_ANALYSIS` utwórz jawny Feature Contract zanim wejdziesz w poważną geometrię. Dla assetów wymagających zgodności z referencją ustaw `enforce_feature_contracts: true` i przypisz każdy widoczny, reference-critical feature do komponentu.

Feature Contract rozróżnia:

- `MUST` — brak lub błędna reprezentacja blokuje akceptację;
- `SHOULD` — błąd jest jawny, ale może nie blokować;
- `OPTIONAL` — nigdy nie kompensuje brakującego MUST.

Nie zakładaj, że tekstowy brief wymienia wszystkie detale. Jeżeli śruba, ring sensora, podcięcie, bezel, kanał LED, szczelina lub inny element jest jednoznacznie widoczny w authoritative reference, musi zostać zmapowany albo jawnie sklasyfikowany jako nieistotny zgodnie z polityką źródła.

Pipeline v0.22:

```text
reference evidence + registered views
→ Shape Graph
→ Feature Contract + Visual Feature Map + edge/profile requirements
→ component-scoped task pack
→ representation contract
→ deterministic Blender mutation
→ measured feature proof (nie tylko obecność operacji)
→ trusted component receipts
→ stage-specific acceptance level
→ registered multi-view QA renders
→ independent visual reviewer
→ per-MUST fidelity verdict
→ current asset+scene+reference-bound fidelity review
→ final APPROVED
```

Twarde reguły v0.22:

- `BOOLEAN_CUT` / `BOOLEAN_UNION` musi wykazać rzeczywisty efekt geometryczny w ewaluowanej siatce; sam modifier nie jest dowodem;
- contracted repeat/detail musi udowodnić wymaganą liczbę/pitch/miarę, jeśli takie parametry są authoritative;
- sensor/camera wymagający ring/housing/lens nie może zostać uznany za poprawny jako pojedyncza płaska kropka/cylinder;
- jeden globalny bevel nie zastępuje reference-specific edge language; zachowuj wymagane edge profiles;
- `STRUCTURAL_GEOMETRY` oznacza wyłącznie structural acceptance; nie wolno raportować final completion bez przejścia wymaganych późniejszych poziomów;
- independent visual reviewer musi pracować na renderach QA i reference evidence dla dokładnego asset/scene/reference revision;
- wynik global similarity jest pomocniczy i nigdy nie nadpisuje FAIL/MISSING dla MUST feature;
- jeśli reviewer odkryje reference-critical detal nieobecny w Feature Contract (`discovered_unmapped_features`), final approval jest zablokowany do czasu aktualizacji kontraktu i modelu;
- po każdej mutacji unieważnij stale fidelity evidence przez revision binding zamiast ponownie używać poprzedniego PASS;
- reviewer nie może być builderem tej samej iteracji.

'''
    if "## v0.22 visual fidelity and feature completion" not in text:
        text = text.replace(marker, block + marker, 1)
    if "Runtime release: v0.22.0." not in text:
        text += "\n\nRuntime release: v0.22.0. Reference-driven production MUST use Feature Contracts for reference-critical details, measured feature proof and current independent multi-view fidelity review before final APPROVED.\n"
    path.write_text(text, encoding="utf-8")


def update_reviewer_prompt() -> None:
    write(
        "06_prompts/62_REVIEWER_PROMPT.md",
        '''# Reviewer Prompt — Independent Visual Fidelity Reviewer v0.22

Jesteś **niezależnym** reviewerem assetu 3D. Nie jesteś builderem tej iteracji i nie poprawiasz modelu.

Dane wejściowe:
- exact `asset_revision`, `scene_revision`, `reference_revision`;
- Feature Contract z priorytetami MUST / SHOULD / OPTIONAL;
- Visual Feature Map i edge/profile requirements;
- authoritative reference evidence / ROI;
- zarejestrowane rendery QA (FRONT/REAR/SIDE/TOP/PERSPECTIVE/DETAIL według kontraktu);
- Scene Snapshot i measured feature proofs;
- mesh/material/runtime stats.

## Zasada główna

Nie oceniaj wyłącznie bounding boxa, liczby obiektów ani globalnego podobieństwa. Jeżeli człowiek widzi reference-critical różnicę, reviewer ma ją nazwać i przypisać do Feature ID albo do `discovered_unmapped_features`.

## Per-feature review

Dla każdego visual `MUST` zwróć:
- `feature_id`;
- `status`: `PASS` / `FAIL` / `BLOCKED` / `NOT_VISIBLE`;
- `view_ids`, na których oceniono feature;
- evidence: konkretna różnica między reference i renderem;
- failure class: silhouette / proportion / geometry / negative_space / placement / orientation / edge_profile / material_region / shading / runtime;
- minimalną korektę;
- etap, do którego należy wrócić.

`SHOULD` i `OPTIONAL` raportuj osobno, ale nie używaj ich do kompensowania FAIL dla MUST.

## Obowiązkowe kontrole

Sprawdź co najmniej:
- silhouette i major/secondary boundaries;
- negative spaces, recesses, trims, lips, bezels, channels i junctions;
- liczbę, spacing i orientację powtarzalnych feature'ów;
- edge language / bevel / chamfer / undercut względem referencji;
- material-region boundaries i emissive placement;
- czy mały detal nie został zastąpiony semantycznie słabszą bryłą (np. kamera → płaska kropka);
- czy model nie pominął elementów widocznych w authoritative reference tylko dlatego, że brief tekstowy ich nie nazwał;
- czy optymalizacja/LOD nie usunęły cechy;
- czy agent nie dodał niezatwierdzonych elementów;
- czy pivot/transform/export/runtime są poprawne, gdy dany etap tego wymaga.

Jeżeli widzisz reference-critical feature, którego nie ma w Feature Contract, dodaj go do `discovered_unmapped_features` z komponentem i view ID. Taki przypadek blokuje final fidelity PASS do czasu aktualizacji kontraktu.

Globalny similarity score może być podany jako sygnał pomocniczy, ale **nie może** nadpisać brakującego lub błędnego MUST feature.

Nie używaj oceny „wygląda dobrze”. Każdy PASS i FAIL musi wskazywać kryterium i evidence.
''',
    )


def update_release_workflow() -> None:
    path = ROOT / ".github/workflows/release.yml"
    text = path.read_text(encoding="utf-8")
    text = text.replace("0.21.0", VERSION)
    text = text.replace("Fidelity Enforcement & Deterministic Assembly", "Visual Fidelity & Feature Completion")
    text = text.replace("Require main and v0.22.0", "Require main and v0.22.0")
    path.write_text(text, encoding="utf-8")


def find_by_id(records, item_id):
    for item in records:
        if isinstance(item, dict) and item.get("id") == item_id:
            return item
    return None


def upsert(records, value):
    existing = find_by_id(records, value["id"])
    if existing is None:
        records.append(value)
    else:
        existing.update(value)


def update_manifest() -> None:
    path = ROOT / "MANIFEST.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = VERSION
    data["benchmark"] = BENCHMARK
    data["runtime_verification_version"] = VERSION
    if BENCHMARK not in data["benchmarks"]:
        data["benchmarks"].append(BENCHMARK)
    for module in (BENCHMARK, CONTRACT):
        if module not in data["modules"]:
            data["modules"].append(module)
    data["module_count"] = len(data["modules"])

    skills = data.setdefault("skills", [])
    executors = data.setdefault("executors", [])

    updates = {
        "COMPONENT_TASK_PACK": ("Scope Feature Contract, QA views and edge/profile requirements into compact component tasks.", "executors/component_task_pack.py", ["tests/unit/test_component_task_pack.py", "tests/unit/test_feature_contract_gate.py"]),
        "ASSET_PRODUCTION_ORCHESTRATOR": ("Compile persistent asset/design/reference state into scoped v0.22 production tasks.", "executors/asset_production_orchestrator.py", ["tests/unit/test_asset_production_orchestrator.py"]),
        "HARD_SURFACE_RECIPE": ("Validate deterministic hard-surface recipes including sensor/detail primitives.", "executors/hard_surface_recipe.py", ["tests/unit/test_hard_surface_recipe.py", "tests/blender/test_v022_feature_primitives_and_proof.py"]),
        "BLENDER_HARD_SURFACE_BUILDER": ("Execute deterministic Blender geometry and emit measured feature/Boolean proof.", "executors/blender_hard_surface_builder.py", ["tests/blender/test_hard_surface_builder.py", "tests/blender/test_v021_component_execution.py", "tests/blender/test_v0211_primitive_winding_and_boolean.py", "tests/blender/test_v022_feature_primitives_and_proof.py"]),
        "SCENE_COMPONENT_SNAPSHOT": ("Persist compact scene evidence including evaluated metrics and feature proof.", "executors/scene_component_snapshot.py", ["tests/unit/test_scene_component_snapshot.py", "tests/blender/test_v022_feature_primitives_and_proof.py"]),
        "BLENDER_SCENE_SNAPSHOT_ADAPTER": ("Measure Blender 5.1 scene state and feature proof without mutating the scene.", "executors/blender_scene_snapshot_adapter.py", ["tests/blender/test_scene_snapshot_adapter.py", "tests/blender/test_v022_feature_primitives_and_proof.py"]),
        "REPRESENTATION_CONTRACT_GATE": ("Reject semantically weaker recipes for reference-critical representations.", "executors/representation_contract_gate.py", ["tests/unit/test_representation_contract_gate.py", "tests/regression/test_benchmark_92.py"]),
        "COMPONENT_EXECUTION_GATE": ("Block incomplete feature recipes before deterministic Blender mutation.", "executors/component_execution_gate.py", ["tests/unit/test_component_execution_gate.py", "tests/blender/test_v022_feature_primitives_and_proof.py"]),
        "ASSET_EXECUTION_AUTHORIZATION_GATE": ("Authorize persisted component work across structural and later production stages.", "executors/asset_execution_authorization_gate.py", ["tests/unit/test_asset_execution_authorization_gate.py", "tests/regression/test_benchmark_92.py"]),
        "COMPONENT_VALIDATION_RUNNER": ("Publish trusted representation, scene and feature-completion receipts.", "executors/component_validation_runner.py", ["tests/unit/test_component_validation_runner.py", "tests/unit/test_feature_contract_gate.py", "tests/regression/test_benchmark_92.py"]),
        "PRODUCTION_STUDIO_SERVICE": ("Operational production service with feature validation, acceptance levels and fidelity review persistence.", "executors/production_studio_service.py", ["tests/integration/test_v021_studio_http.py", "tests/integration/test_v022_fidelity_review_http.py", "tests/regression/test_benchmark_92.py"]),
    }
    for item_id, (purpose, executor_path, tests) in updates.items():
        skill = find_by_id(skills, item_id)
        if skill is not None:
            skill["purpose"] = purpose
            skill["contract"] = CONTRACT
            skill["benchmark"] = BENCHMARK
            skill["routing_keywords"] = sorted(set(skill.get("routing_keywords", []) + ["v0.22", "feature", "fidelity"]))
            skill["tests"] = tests
        executor = find_by_id(executors, item_id)
        if executor is not None:
            executor["contract"] = CONTRACT
            executor["tests"] = tests

    new_entries = [
        {
            "id": "FEATURE_CONTRACT_GATE",
            "purpose": "Require every reference-critical MUST feature to have recipe intent and measured scene proof.",
            "executor": "executors/feature_contract_gate.py",
            "dependencies": ["COMPONENT_TASK_PACK", "SCENE_COMPONENT_SNAPSHOT"],
            "tests": ["tests/unit/test_feature_contract_gate.py", "tests/regression/test_benchmark_92.py"],
            "routing_keywords": ["feature", "must", "completion", "fidelity"],
        },
        {
            "id": "VISUAL_FIDELITY_REVIEW_GATE",
            "purpose": "Validate independent per-MUST multi-view fidelity review bound to current revisions.",
            "executor": "executors/visual_fidelity_review_gate.py",
            "dependencies": ["FEATURE_CONTRACT_GATE"],
            "tests": ["tests/unit/test_visual_fidelity_review_gate.py", "tests/regression/test_benchmark_92.py"],
            "routing_keywords": ["visual", "review", "multiview", "fidelity"],
        },
        {
            "id": "FIDELITY_REVIEW_REPOSITORY",
            "purpose": "Persist revision-bound independent visual fidelity reviews.",
            "executor": "executors/fidelity_review_repository.py",
            "dependencies": ["VISUAL_FIDELITY_REVIEW_GATE"],
            "tests": ["tests/integration/test_v022_fidelity_review_http.py"],
            "routing_keywords": ["fidelity", "review", "revision", "persistence"],
        },
        {
            "id": "ASSET_STAGE_COMPLETION_GATE",
            "purpose": "Prevent structural acceptance from being reported as later-stage or final completion.",
            "executor": "executors/asset_stage_completion_gate.py",
            "dependencies": ["FEATURE_CONTRACT_GATE", "FIDELITY_REVIEW_REPOSITORY"],
            "tests": ["tests/unit/test_asset_stage_completion_gate.py", "tests/regression/test_benchmark_92.py"],
            "routing_keywords": ["stage", "completion", "approval", "fidelity"],
        },
    ]
    for entry in new_entries:
        skill = {
            "id": entry["id"],
            "purpose": entry["purpose"],
            "contract": CONTRACT,
            "executor": entry["executor"],
            "maturity": "EXECUTOR_READY",
            "dependencies": entry["dependencies"],
            "benchmark": BENCHMARK,
            "routing_keywords": entry["routing_keywords"],
            "tests": entry["tests"],
        }
        executor = {
            "id": entry["id"],
            "contract": CONTRACT,
            "executor": entry["executor"],
            "maturity": "EXECUTOR_READY",
            "tests": entry["tests"],
        }
        upsert(skills, skill)
        upsert(executors, executor)

    tests = data.setdefault("tests", [])
    new_tests = [
        "tests/unit/test_feature_contract_gate.py",
        "tests/unit/test_visual_fidelity_review_gate.py",
        "tests/unit/test_asset_stage_completion_gate.py",
        "tests/integration/test_v022_fidelity_review_http.py",
        "tests/regression/test_benchmark_92.py",
        "tests/blender/test_v022_feature_primitives_and_proof.py",
    ]
    for test in new_tests:
        if test not in tests:
            tests.append(test)

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_release_validator() -> None:
    path = ROOT / "tools/validate_release_metadata.py"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'TARGET_VERSION = "[^"]+"', f'TARGET_VERSION = "{VERSION}"', text, count=1)
    text = re.sub(r'TARGET_BENCHMARK = "[^"]+"', f'TARGET_BENCHMARK = "{BENCHMARK}"', text, count=1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    update_pyproject()
    update_readme()
    update_changelog()
    update_system_prompt()
    update_reviewer_prompt()
    update_release_workflow()
    update_manifest()
    update_release_validator()
    print("v0.22.0 release metadata promoted")


if __name__ == "__main__":
    main()
