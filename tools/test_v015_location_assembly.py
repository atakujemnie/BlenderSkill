from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from executors.clearance_gate import evaluate_clearances
from executors.location_asset_manifest import evaluate_asset_manifest
from executors.location_completeness_gate import evaluate_location_completeness
from executors.location_design_system_gate import evaluate_location_design_system
from executors.location_reference_fidelity_gate import evaluate_location_reference_fidelity
from executors.location_scene_graph import validate_location_scene_graph
from executors.location_stage_barrier import evaluate_stage_barrier
from executors.spatial_relation_gate import evaluate_spatial_relations


def assert_status(result, expected):
    assert result["status"] == expected, result


def main() -> None:
    graph = [
        {"id": "LOC", "kind": "LOCATION", "state": "ACCEPTED"},
        {"id": "BAR_ZONE", "kind": "ZONE", "parent": "LOC", "state": "ACCEPTED"},
        {"id": "BAR", "kind": "ASSET", "parent": "BAR_ZONE", "state": "ACCEPTED"},
        {"id": "BAR_01", "kind": "INSTANCE", "parent": "BAR_ZONE", "state": "INSTANCED"},
    ]
    assert_status(validate_location_scene_graph(graph), "PASS")
    assert_status(validate_location_scene_graph(graph + [{"id": "LOC2", "kind": "LOCATION"}]), "FAIL")

    final_manifest = [
        {"asset_id": "BAR_MAIN", "required": True, "tier": "HERO", "state": "ACCEPTED"},
        {"asset_id": "CHAIR", "required": True, "tier": "MID", "state": "INSTANCED"},
    ]
    assert_status(evaluate_asset_manifest(final_manifest, final=True), "PASS")
    broken_manifest = [dict(final_manifest[0], state="PROXY"), final_manifest[1]]
    assert_status(evaluate_asset_manifest(broken_manifest, final=True), "FAIL")

    design = {
        "location_id": "lafar_restaurant_01",
        "unit_scale": 0.001,
        "architectural_grid_mm": 1200,
        "material_families": {"stone": {}},
        "edge_families": {"micro_bevel_mm": [1, 2]},
        "lighting_families": {"warm": {"k": 2700}},
        "branding": {"logo": "lafar"},
    }
    assert_status(evaluate_location_design_system(design), "PASS")
    assert_status(evaluate_location_design_system({}), "FAIL")

    assert_status(evaluate_spatial_relations([{"relation_id": "R1", "relation": "BEHIND", "a": "BACKBAR", "b": "BAR", "satisfied": True}]), "PASS")
    assert_status(evaluate_spatial_relations([{"relation_id": "R1", "relation": "BEHIND", "a": "BACKBAR", "b": "BAR", "satisfied": False}]), "FAIL")

    assert_status(evaluate_clearances([{"clearance_id": "AISLE", "required_mm": 900, "measured_mm": 1000}]), "PASS")
    assert_status(evaluate_clearances([{"clearance_id": "AISLE", "required_mm": 900, "measured_mm": 700}]), "FAIL")
    assert_status(evaluate_clearances([{"clearance_id": "CHAIR_WALL", "required_mm": 0, "measured_mm": 0, "penetration_mm": 200, "max_penetration_mm": 0}]), "FAIL")

    stages = {"REFERENCE": "PASS", "DESIGN_SYSTEM": "PASS", "ARCHITECTURE": "PASS"}
    assert_status(evaluate_stage_barrier(stages, "HERO_ANCHORS"), "PASS")
    assert_status(evaluate_stage_barrier({"REFERENCE": "PASS", "DESIGN_SYSTEM": "FAIL"}, "ARCHITECTURE"), "FAIL")

    metrics = {"layout_anchor_error_mm": 50, "orientation_error_deg": 2, "hero_scale_error_pct": 1, "composition_score": 0.91}
    assert_status(evaluate_location_reference_fidelity(metrics, [{"owner_id": "BAR", "status": "PASS"}]), "PASS")
    assert_status(evaluate_location_reference_fidelity(dict(metrics, composition_score=0.4), [{"owner_id": "BAR", "status": "PASS"}]), "FAIL")

    good = {gate: "PASS" for gate in ("scene_graph", "design_system", "asset_manifest", "architecture", "spatial_relations", "clearance", "reference_fidelity")}
    assert_status(evaluate_location_completeness(good), "PASS")
    assert_status(evaluate_location_completeness(dict(good, proxy_count=1)), "FAIL")
    assert_status(evaluate_location_completeness(dict(good, missing_hero_count=1)), "FAIL")
    assert_status(evaluate_location_completeness(dict(good, unintended_penetration_count=1)), "FAIL")
    assert_status(evaluate_location_completeness(dict(good, blocked_required_path_count=1)), "FAIL")

    print("v0.15 location assembly tests: PASS")


if __name__ == "__main__":
    main()
