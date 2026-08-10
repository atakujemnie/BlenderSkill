import json
from pathlib import Path

from executors.design_system_repository import initialize as initialize_design_resource
from executors.production_studio_service import (
    add_asset_correction,
    advance_asset_stage,
    create_asset,
    create_production_task,
    get_studio,
    list_assets,
    prepare_task,
    promote_production_tasks,
    publish_scene,
    resolve_asset_correction,
    upsert_reference_evidence,
)


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "lafar_street_bench_vnext.json"


def _install_design_resources(root):
    definitions = {
        "ASTERA_GRAPHITE_01": "MATERIAL",
        "ASTERA_TRIM_PROFILE_01": "TRIM_PROFILE",
        "ASTERA_EDGE_PROFILE_02": "EDGE_PROFILE",
        "ASTERA_LED_UNDERGLOW_01": "LED_PROFILE",
        "ASTERA_LED_INFO_BLUE_01": "LED_PROFILE",
        "ASTERA_UTILITY_PANEL_01": "DETAIL_MODULE",
    }
    for resource_id, kind in definitions.items():
        result = initialize_design_resource(
            root,
            {
                "design_system_id": "ASTERA_CIVIC",
                "resource_id": resource_id,
                "kind": kind,
                "version": "1.0.0",
                "revision": 1,
                "locked": True,
                "payload": {"canonical": True},
            },
        )
        assert result["status"] == "PASS", result


def test_studio_service_manages_asset_evidence_tasks_corrections_and_scene(tmp_path):
    asset = json.loads(FIXTURE.read_text(encoding="utf-8"))
    created = create_asset(tmp_path, asset)
    assert created["status"] == "PASS"
    assert created["queue_revision"] == 1
    assert created["reference_revision"] == 1
    _install_design_resources(tmp_path)

    assets = list_assets(tmp_path)
    assert assets["asset_count"] == 1
    assert assets["assets"][0]["asset_id"] == "ASSET-005"

    evidence = upsert_reference_evidence(
        tmp_path,
        "ASSET-005",
        {
            "evidence_id": "EV-BACKREST-SIDE",
            "reference_id": "lafar-bench-sheet",
            "component_id": "BACKREST",
            "view": "SIDE",
            "authority": "PRIMARY",
            "feature_ids": ["BACKREST_PROFILE"],
            "roi": [690, 590, 840, 870],
            "artifact_id": "roi:backrest:side",
            "registration_id": "reg:bench:side",
        },
        expected_reference_revision=1,
    )
    assert evidence["status"] == "PASS"
    assert evidence["revision"] == 2

    prepared = prepare_task(
        tmp_path,
        "ASSET-005",
        "BACKREST",
        task_kind="REPAIR",
        feature_ids=["BACKREST_PROFILE"],
    )
    assert prepared["status"] == "PASS", prepared
    assert prepared["task_pack"]["allowed_to_modify"] == ["BACKREST"]
    assert prepared["task_pack"]["reference_evidence"][0]["evidence_id"] == "EV-BACKREST-SIDE"
    assert prepared["metrics"]["estimated_input_tokens"] < 4000

    task = create_production_task(
        tmp_path,
        "ASSET-005",
        {
            "task_id": "T-BACKREST",
            "component_id": "BACKREST",
            "task_kind": "REPAIR",
            "priority": 20,
        },
        expected_queue_revision=1,
    )
    assert task["status"] == "PASS"
    assert task["queue_revision"] == 2

    promoted = promote_production_tasks(tmp_path, "ASSET-005", expected_queue_revision=2)
    assert promoted["status"] == "PASS"
    assert promoted["promoted"] == ["T-BACKREST"]
    assert promoted["queue_revision"] == 3

    studio = get_studio(tmp_path, "ASSET-005", component_id="BACKREST")
    assert studio["status"] == "PASS"
    view = studio["view_model"]
    assert view["selected_component_id"] == "BACKREST"
    assert view["runtime_revisions"] == {"asset": 1, "task_queue": 3, "reference_evidence": 2, "scene": 0}
    assert view["inspector"]["reference_evidence"][0]["evidence_id"] == "EV-BACKREST-SIDE"
    assert view["inspector"]["resolved_parameters"]["width"]["value"] == 1580.0

    correction = add_asset_correction(
        tmp_path,
        "ASSET-005",
        {
            "id": "COR-001",
            "component_id": "BACKREST",
            "kind": "PARAMETER_OVERRIDE",
            "parameter": "angle",
            "value": 13,
            "unit": "deg",
            "priority": "HARD",
        },
        expected_asset_revision=1,
    )
    assert correction["status"] == "PASS"
    assert correction["asset_revision"] == 2

    blocked = advance_asset_stage(
        tmp_path,
        "ASSET-005",
        "BLOCKOUT",
        expected_asset_revision=2,
    )
    assert blocked["status"] == "BLOCKED"
    assert blocked["blockers"][0]["reason"] == "OPEN_HARD_CORRECTIONS"

    resolved = resolve_asset_correction(
        tmp_path,
        "ASSET-005",
        "COR-001",
        expected_asset_revision=2,
        resolution={"accepted": True},
    )
    assert resolved["status"] == "PASS"
    assert resolved["asset_revision"] == 3

    advanced = advance_asset_stage(
        tmp_path,
        "ASSET-005",
        "BLOCKOUT",
        expected_asset_revision=3,
    )
    assert advanced["status"] == "PASS"
    assert advanced["asset_revision"] == 4

    scene = publish_scene(
        tmp_path,
        "ASSET-005",
        {
            "asset_revision": 4,
            "scene_revision": 1,
            "objects": [
                {
                    "object_id": "bench.backrest.shell",
                    "component_id": "BACKREST",
                    "object_type": "MESH",
                    "dimensions_mm": [1580, 72, 390],
                    "material_ids": ["ASTERA_GRAPHITE_01"],
                }
            ],
        },
    )
    assert scene["status"] == "PASS"
    assert scene["scene_revision"] == 1

    refreshed = get_studio(tmp_path, "ASSET-005", component_id="BACKREST")
    assert refreshed["view_model"]["runtime_revisions"]["asset"] == 4
    assert refreshed["view_model"]["runtime_revisions"]["scene"] == 1
    assert refreshed["view_model"]["inspector"]["scene_objects"][0]["object_id"] == "bench.backrest.shell"


def test_studio_service_rejects_stale_asset_revision(tmp_path):
    asset = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert create_asset(tmp_path, asset)["status"] == "PASS"
    result = add_asset_correction(
        tmp_path,
        "ASSET-005",
        {"id": "COR-STALE", "component_id": "BACKREST", "priority": "HARD"},
        expected_asset_revision=99,
    )
    assert result["status"] == "CONFLICT"
    assert result["blockers"][0] == {"reason": "ASSET_REVISION_CONFLICT", "expected": 99, "actual": 1}
