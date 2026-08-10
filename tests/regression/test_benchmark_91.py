from executors.asset_envelope_gate import validate as validate_envelope
from executors.component_execution_gate import authorize as authorize_recipe
from executors.component_validation_runner import validate_and_publish
from executors.production_studio_service import (
    authorize_component,
    create_asset,
    create_production_task,
    get_studio,
    prepare_task,
    promote_production_tasks,
    publish_scene,
    transition_production_task,
)
from executors.scene_snapshot_repository import load as load_scene_snapshot


def _asset(*, stage="BLOCKOUT", slab_width=994):
    return {
        "asset_id": "ACS-SM-SIDEWALK-3470-S-B91",
        "name": "Lafar Sidewalk Benchmark 91",
        "revision": 1,
        "stage": stage,
        "enforce_asset_envelope": False,
        "components": {
            "ROOT": {
                "parent": None,
                "state": "ACCEPTED",
                "shape_class": "ASSEMBLY",
                "origin": {"type": "CENTER_XY_BOTTOM_Z"},
                "dimensions": {
                    "width": {"value": 2000, "unit": "mm", "locked": True},
                    "depth": {"value": 2000, "unit": "mm", "locked": True},
                    "height": {"value": 160, "unit": "mm", "locked": True},
                },
                "anchors": {},
            },
            "SLAB_L": {
                "parent": "ROOT",
                "state": "CONSTRAINED",
                "shape_class": "ROUNDED_BOX",
                "origin": {"type": "CENTER_BOTTOM"},
                "placement_required": True,
                "transform": {"location_mm": [-500, 0, 120], "coordinate_space": "ASSET_LOCAL"},
                "depends_on": ["ROOT"],
                "dimensions": {
                    "width": {"value": slab_width, "unit": "mm", "locked": True},
                    "depth": {"value": 1000, "unit": "mm", "locked": True},
                    "height": {"value": 40, "unit": "mm", "locked": True},
                },
                "anchors": {},
                "validation": {
                    "required_validator_ids": ["SCENE_COMPONENT_VALIDATION", "REPRESENTATION_CONTRACT_GATE"],
                    "require_dimensions_match": True,
                    "placement_tolerance_mm": 0.5,
                    "dimension_tolerance_mm": 0.5,
                },
            },
            "SLAB_R": {
                "parent": "ROOT",
                "state": "CONSTRAINED",
                "shape_class": "ROUNDED_BOX",
                "origin": {"type": "CENTER_BOTTOM"},
                "placement_required": True,
                "transform": {"location_mm": [500, 0, 120], "coordinate_space": "ASSET_LOCAL"},
                "depends_on": ["ROOT"],
                "dimensions": {
                    "width": {"value": slab_width, "unit": "mm", "locked": True},
                    "depth": {"value": 1000, "unit": "mm", "locked": True},
                    "height": {"value": 40, "unit": "mm", "locked": True},
                },
                "anchors": {},
            },
            "TACTILE": {
                "parent": "ROOT",
                "state": "CONSTRAINED",
                "shape_class": "TACTILE_GRID_PANEL",
                "origin": {"type": "CENTER_BOTTOM"},
                "placement_required": True,
                "transform": {"location_mm": [0, -800, 150], "coordinate_space": "ASSET_LOCAL"},
                "depends_on": ["ROOT"],
                "dimensions": {
                    "width": {"value": 2000, "unit": "mm"},
                    "depth": {"value": 150, "unit": "mm"},
                    "height": {"value": 10, "unit": "mm"},
                },
                "anchors": {},
            },
            "GRATE": {
                "parent": "ROOT",
                "state": "CONSTRAINED",
                "shape_class": "SLOTTED_GRATE_PLATE",
                "origin": {"type": "CENTER_BOTTOM"},
                "placement_required": True,
                "transform": {"location_mm": [0, -930, 105], "coordinate_space": "ASSET_LOCAL"},
                "depends_on": ["ROOT"],
                "dimensions": {
                    "width": {"value": 1900, "unit": "mm"},
                    "depth": {"value": 100, "unit": "mm"},
                    "height": {"value": 8, "unit": "mm"},
                },
                "anchors": {},
            },
        },
        "seam_constraints": [
            {"a": "SLAB_L", "b": "SLAB_R", "axis": "X", "expected_gap_mm": 6, "tolerance_mm": 0.5}
        ],
        "bindings": {},
        "corrections": [],
        "history": [],
    }


def _slab_recipe():
    return {
        "component_id": "SLAB_L",
        "operations": [
            {
                "id": "body",
                "op": "ROUNDED_BOX",
                "output": "BODY",
                "dimensions": {"width": 994, "depth": 1000, "height": 40},
            }
        ],
        "final_outputs": ["BODY"],
    }


def test_benchmark_91_blocks_known_blind_test_failures_and_requires_trusted_acceptance(tmp_path):
    broken = _asset(slab_width=996)
    envelope = validate_envelope(broken)
    assert envelope["status"] == "FAIL"
    assert any(item["reason"] == "SEAM_GAP_MISMATCH" for item in envelope["blockers"])

    asset = _asset()
    assert validate_envelope(asset)["status"] == "PASS"
    created = create_asset(tmp_path, asset)
    assert created["status"] == "PASS", created

    prepared = prepare_task(tmp_path, asset["asset_id"], "SLAB_L", task_kind="BUILD")
    assert prepared["status"] == "PASS", prepared
    assert prepared["task_pack"]["component"]["transform"]["location_mm"] == [-500.0, 0.0, 120.0]
    assert prepared["metrics"]["estimated_input_tokens"] < 8000

    tactile_pack = prepare_task(tmp_path, asset["asset_id"], "TACTILE", task_kind="BUILD")["task_pack"]
    bad_tactile_recipe = {
        "component_id": "TACTILE",
        "operations": [
            {"id": "body", "op": "ROUNDED_BOX", "output": "BODY", "dimensions": {"width": 2000, "depth": 150, "height": 10}}
        ],
        "final_outputs": ["BODY"],
    }
    blocked_recipe = authorize_recipe(tactile_pack, bad_tactile_recipe)
    assert blocked_recipe["status"] == "BLOCKED"
    assert any(item["reason"] == "REPRESENTATION_REQUIRED_OPERATION_MISSING" for item in blocked_recipe["blockers"])

    unauthorized = create_production_task(
        tmp_path,
        asset["asset_id"],
        {"task_id": "T-SLAB-L", "component_id": "SLAB_L", "task_kind": "BUILD", "stage": "BLOCKOUT"},
        expected_queue_revision=1,
    )
    assert unauthorized["status"] == "BLOCKED"
    assert unauthorized["blockers"][0]["reason"] == "COMPONENT_BUILD_NOT_AUTHORIZED"

    authorized = authorize_component(
        tmp_path,
        asset["asset_id"],
        "SLAB_L",
        {"actor": "TEST", "reason": "BENCHMARK_91_AUTHORIZATION_REQUEST", "status": "FAIL", "validator_id": "UNTRUSTED_CALLER"},
        expected_asset_revision=1,
    )
    assert authorized["status"] == "PASS", authorized
    assert authorized["asset_revision"] == 2
    assert authorized["authorization"]["validator_id"] == "ASSET_EXECUTION_AUTHORIZATION_GATE"
    assert authorized["authorization"]["source"] == "SYSTEM"

    execution_pack_result = prepare_task(tmp_path, asset["asset_id"], "SLAB_L", task_kind="BUILD")
    assert execution_pack_result["status"] == "PASS", execution_pack_result
    execution_pack = execution_pack_result["task_pack"]
    assert execution_pack["asset_revision"] == 2

    task = create_production_task(
        tmp_path,
        asset["asset_id"],
        {"task_id": "T-SLAB-L", "component_id": "SLAB_L", "task_kind": "BUILD", "stage": "BLOCKOUT"},
        expected_queue_revision=1,
    )
    assert task["status"] == "PASS", task
    assert task["task"]["asset_revision"] == 2
    assert set(task["task"]["required_validation_ids"]) == {"SCENE_COMPONENT_VALIDATION", "REPRESENTATION_CONTRACT_GATE"}

    promoted = promote_production_tasks(tmp_path, asset["asset_id"], expected_queue_revision=2)
    assert promoted["promoted"] == ["T-SLAB-L"]
    running = transition_production_task(
        tmp_path,
        asset["asset_id"],
        "T-SLAB-L",
        "RUNNING",
        expected_queue_revision=3,
        actor="WORKER",
        reason="CLAIM",
        worker_id="worker-91",
    )
    assert running["status"] == "PASS"

    scene = publish_scene(
        tmp_path,
        asset["asset_id"],
        {
            "asset_revision": 2,
            "scene_revision": 1,
            "objects": [
                {
                    "object_id": "sidewalk.slab.left",
                    "component_id": "SLAB_L",
                    "object_type": "MESH",
                    "transform": {"location_mm": [-500, 0, 120]},
                    "dimensions_mm": [994, 1000, 40],
                }
            ],
        },
    )
    assert scene["status"] == "PASS", scene

    reviewed = transition_production_task(
        tmp_path,
        asset["asset_id"],
        "T-SLAB-L",
        "REVIEW",
        expected_queue_revision=4,
        actor="WORKER",
        reason="DONE",
        result={"validation_status": "PASS", "scene_revision": 1},
    )
    assert reviewed["status"] == "PASS"

    self_certified = transition_production_task(
        tmp_path,
        asset["asset_id"],
        "T-SLAB-L",
        "APPROVED",
        expected_queue_revision=5,
        actor="WORKER",
        reason="SELF_CERTIFIED",
    )
    assert self_certified["status"] == "FAIL"
    assert self_certified["blockers"][0]["reason"] == "TRUSTED_VALIDATION_RECEIPTS_REQUIRED"

    persisted_scene = load_scene_snapshot(tmp_path, asset["asset_id"])
    assert persisted_scene["status"] == "PASS", persisted_scene
    validation = validate_and_publish(tmp_path, execution_pack, _slab_recipe(), persisted_scene["snapshot"])
    assert validation["status"] == "PASS", validation
    assert {receipt["validator_id"] for receipt in validation["receipts"]} == {
        "SCENE_COMPONENT_VALIDATION",
        "REPRESENTATION_CONTRACT_GATE",
    }

    approved = transition_production_task(
        tmp_path,
        asset["asset_id"],
        "T-SLAB-L",
        "APPROVED",
        expected_queue_revision=5,
        actor="REVIEWER",
        reason="TRUSTED_GATES_PASS",
    )
    assert approved["status"] == "PASS", approved
    assert approved["component_state"] == "ACCEPTED"
    assert approved["asset_revision"] == 3

    studio = get_studio(tmp_path, asset["asset_id"], component_id="SLAB_L")
    assert studio["status"] == "PASS"
    component = next(item for item in studio["view_model"]["components"] if item["component_id"] == "SLAB_L")
    assert component["state"] == "ACCEPTED"


def test_benchmark_91_blocks_task_stage_bypass(tmp_path):
    asset = _asset(stage="RECONSTRUCTION_MANIFEST")
    asset["components"]["SLAB_L"]["state"] = "READY_TO_BUILD"
    assert create_asset(tmp_path, asset)["status"] == "PASS"
    result = create_production_task(
        tmp_path,
        asset["asset_id"],
        {"task_id": "T-BYPASS", "component_id": "SLAB_L", "task_kind": "BUILD", "stage": "STRUCTURAL_GEOMETRY"},
        expected_queue_revision=1,
    )
    assert result["status"] == "BLOCKED"
    assert result["blockers"][0]["reason"] == "TASK_STAGE_NOT_AUTHORIZED"
