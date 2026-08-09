from __future__ import annotations

"""Runtime budget planner/validator for procedural vegetation."""

from typing import Any, Mapping

EXECUTOR_ID = "VEGETATION_RUNTIME_PREP"; EXECUTOR_VERSION = "0.1.0"
USAGE_DEFAULTS = {"HERO": {"lod0": 60000, "lod1": 30000, "lod2": 12000, "lod3": 2500}, "MID": {"lod0": 30000, "lod1": 14000, "lod2": 5000, "lod3": 1200}, "BACKGROUND": {"lod0": 12000, "lod1": 5000, "lod2": 1800, "lod3": 500}}


def plan(spec: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []; usage = str(spec.get("usage_class", "MID")).upper()
    if usage not in USAGE_DEFAULTS: blockers.append({"reason": "INVALID_USAGE_CLASS", "value": usage}); usage = "MID"
    if not isinstance(spec.get("seed"), int): blockers.append({"reason": "INTEGER_SEED_REQUIRED"})
    if not spec.get("generator_provenance_id"): blockers.append({"reason": "GENERATOR_PROVENANCE_REQUIRED"})
    generated_tris = int(spec.get("generated_triangle_count", 0) or 0)
    if generated_tris <= 0: blockers.append({"reason": "GENERATED_TRIANGLE_COUNT_REQUIRED"})
    custom = spec.get("triangle_budgets"); budgets = {k: int(v) for k, v in dict(custom or USAGE_DEFAULTS[usage]).items()}
    for key in ("lod0", "lod1", "lod2", "lod3"):
        if key not in budgets or budgets[key] <= 0: blockers.append({"reason": "LOD_BUDGET_REQUIRED", "lod": key})
    if all(k in budgets for k in ("lod0", "lod1", "lod2", "lod3")) and not (budgets["lod0"] >= budgets["lod1"] >= budgets["lod2"] >= budgets["lod3"]): blockers.append({"reason": "LOD_BUDGETS_NOT_MONOTONIC", "budgets": budgets})
    semantic_parts = set(str(x) for x in spec.get("semantic_parts", []) or []); form = str(spec.get("form_class", "")).upper()
    if form in {"TREE", "SHRUB", "ALIEN_BRANCHING"} and not {"stem", "leaves"}.issubset(semantic_parts): blockers.append({"reason": "WOODY_SEMANTIC_PARTS_REQUIRED", "required": ["stem", "leaves"]})
    if form in {"HERBACEOUS", "GRASS", "ROSETTE", "REED"} and "leaves" not in semantic_parts: blockers.append({"reason": "FOLIAGE_PART_REQUIRED"})
    lod_targets = {key.upper(): min(generated_tris, value) for key, value in budgets.items()}; use_leaf_cards = bool(spec.get("leaf_count", 0) and generated_tris > budgets.get("lod1", generated_tris)); use_impostor = generated_tris > budgets.get("lod2", generated_tris) * 4 or usage == "BACKGROUND"
    material_slots = int(spec.get("material_slots", 1) or 1)
    if material_slots > int(spec.get("max_material_slots", 3) or 3): blockers.append({"reason": "MATERIAL_SLOT_BUDGET_EXCEEDED", "actual": material_slots})
    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID, "usage_class": usage, "generated_triangle_count": generated_tris, "lod_targets": lod_targets, "leaf_cards_recommended": use_leaf_cards, "impostor_recommended": use_impostor, "preserve_instancing": True, "required_runtime_attributes": ["wind_weight", "wind_phase", "semantic_part_id"], "blockers": blockers}
