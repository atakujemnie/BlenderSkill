import json
from pathlib import Path

from executors.design_system_repository import initialize as initialize_design_resource
from executors.production_studio_service import (
    create_asset,
    create_production_task,
    get_studio,
    prepare_task,
    promote_production_tasks,
    publish_scene,
    upsert_reference_evidence,
)
from executors.reference_evidence_repository import load as load_reference_evidence
from executors.scene_snapshot_repository import load as load_scene_snapshot


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


def test_benchmark_90_operational_studio_runtime(tmp_path):
    asset = json.loads(FIXTURE.read_text(encoding="utf-8"))
    created = create_asset(tmp_path, asset)
    assert created["status"] == "PASS", created
    assert created["queue_revision"] == 1
    assert created["reference_revision"] == 1
    _install_design_resources(tmp_path)

    backrest_evidence = {
        "evidence_id": "EV-BACKREST-SIDE",
        "reference_id": "lafar-bench-sheet",
        "component_id": "BACKREST",
        "view": "SIDE",
        "authority": "PRIMARY",
        "feature_ids": ["BACKREST_PROFILE"],
        "roi": [690, 590, 840, 870],
        "artifact_id": "roi:backrest:side",
        "registration_id": "reg:bench:side",
    }
    seat_evidence = {
        "evidence_id": "EV-SEAT-TOP",
        "reference_id": "lafar-bench-sheet",
        "component_id": "SEAT",
        "view": "TOP",
        "authority": "PRIMARY",
        "feature_ids": ["SEAT_OUTLINE"],
        "roi": [100, 100, 500, 300],
        "artifact_id": "roi:seat:top",
    }
    first = upsert_reference_evidence(
        tmp_path,
        "ASSET-005",
        backrest_evidence,
        expected_reference_revision=1,
    )
    assert first["status"] == "PASS", first
    assert first["revision"] == 2
    second = upsert_reference_evidence(
        tmp_path,
        "ASSET-005",
        seat_evidence,
        expected_reference_revision=2,
    )
    assert second["status"] == "PASS", second
    assert second["revision"] == 3

    stale_evidence = upsert_reference_evidence(
        tmp_path,
        "ASSET-005",
        {**seat_evidence, "artifact_id": "stale-write"},
        expected_reference_revision=2,
    )
    assert stale_evidence["status"] == "CONFLICT"
    assert stale_evidence["blockers"][0]["reason"] == "REFERENCE_EVIDENCE_REVISION_CONFLICT"

    prepared = prepare_task(
        tmp_path,
        "ASSET-005",
        "BACKREST",
        task_kind="REPAIR",
        feature_ids=["BACKREST_PROFILE"],
    )
    assert prepared["status"] == "PASS", prepared
    assert prepared["task_pack"]["allowed_to_modify"] == ["BACKREST"]
    assert "SEAT" in prepared["task_pack"]["read_only"]
    assert prepared["metrics"]["estimated_input_tokens"] < 4000
    evidence_ids = [item["evidence_id"] for item in prepared["task_pack"]["reference_evidence"]]
    assert evidence_ids == ["EV-BACKREST-SIDE"]

    task = create_production_task(
        tmp_path,
        "ASSET-005",
        {
            "task_id": "T-BACKREST-90",
            "component_id": "BACKREST",
            "task_kind": "REPAIR",
            "priority": 20,
        },
        expected_queue_revision=1,
    )
    assert task["status"] == "PASS", task
    promoted = promote_production_tasks(tmp_path, "ASSET-005", expected_queue_revision=2)
    assert promoted["status"] == "PASS", promoted
    assert promoted["promoted"] == ["T-BACKREST-90"]

    scene = publish_scene(
        tmp_path,
        "ASSET-005",
        {
            "asset_revision": asset["revision"],
            "scene_revision": 1,
            "objects": [
                {
                    "object_id": "bench.backrest.shell",
                    "component_id": "BACKREST",
                    "object_type": "MESH",
                    "dimensions_mm": [1580, 72, 390],
                    "material_ids": ["ASTERA_GRAPHITE_01"],
                    "binding_ids": ["ASTERA_GRAPHITE_01"],
                }
            ],
        },
    )
    assert scene["status"] == "PASS", scene
    assert scene["scene_revision"] == 1

    reloaded_evidence = load_reference_evidence(tmp_path, "ASSET-005")
    reloaded_scene = load_scene_snapshot(tmp_path, "ASSET-005")
    assert reloaded_evidence["status"] == "PASS"
    assert reloaded_evidence["registry"]["revision"] == 3
    assert {item["evidence_id"] for item in reloaded_evidence["registry"]["evidence"]} == {
        "EV-BACKREST-SIDE",
        "EV-SEAT-TOP",
    }
    assert reloaded_scene["status"] == "PASS"
    assert reloaded_scene["snapshot"]["scene_revision"] == 1

    studio = get_studio(tmp_path, "ASSET-005", component_id="BACKREST")
    assert studio["status"] == "PASS", studio
    view = studio["view_model"]
    assert view["selected_component_id"] == "BACKREST"
    assert view["runtime_revisions"] == {
        "asset": asset["revision"],
        "task_queue": 3,
        "reference_evidence": 3,
        "scene": 1,
    }
    assert [item["evidence_id"] for item in view["inspector"]["reference_evidence"]] == ["EV-BACKREST-SIDE"]
    assert view["inspector"]["scene_objects"][0]["component_id"] == "BACKREST"
