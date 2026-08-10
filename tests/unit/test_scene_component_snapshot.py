from executors.scene_component_snapshot import assert_mutation_scope, build, diff


def _scene() -> dict:
    return {
        "asset_id": "ASSET-005",
        "asset_revision": 17,
        "scene_revision": 3,
        "objects": [
            {
                "object_id": "bench.backrest.shell",
                "component_id": "BACKREST",
                "object_type": "MESH",
                "dimensions_mm": [1580, 72, 390],
                "mesh_metrics": {"vertices": 128, "triangles": 240},
                "material_ids": ["ASTERA_GRAPHITE_01"],
                "selected": True,
            },
            {
                "object_id": "bench.seat.shell",
                "component_id": "SEAT",
                "object_type": "MESH",
                "dimensions_mm": [1580, 480, 75],
                "mesh_metrics": {"vertices": 96, "triangles": 180},
                "material_ids": ["ASTERA_GRAPHITE_01"],
            },
        ],
    }


def test_component_snapshot_is_compact_and_stable():
    first = build(_scene(), component_ids=["BACKREST"])
    second = build(_scene(), component_ids=["BACKREST"])
    assert first["status"] == "PASS"
    assert first["snapshot"]["snapshot_hash"] == second["snapshot"]["snapshot_hash"]
    assert first["metrics"]["object_count"] == 1
    assert "selected" not in first["snapshot"]["objects"][0]


def test_snapshot_diff_and_scope_gate():
    before = build(_scene())["snapshot"]
    changed_scene = _scene()
    changed_scene["scene_revision"] = 4
    changed_scene["objects"][0]["dimensions_mm"] = [1580, 76, 390]
    after = build(changed_scene)["snapshot"]

    delta = diff(before, after)
    assert delta["status"] == "PASS"
    assert delta["diff"]["changed_object_count"] == 1
    assert delta["diff"]["changed"][0]["object_id"] == "bench.backrest.shell"

    allowed = assert_mutation_scope(before, after, allowed_to_modify=["BACKREST"])
    assert allowed["status"] == "PASS"

    forbidden = assert_mutation_scope(before, after, allowed_to_modify=["SEAT"])
    assert forbidden["status"] == "FAIL"
    assert forbidden["blockers"][0]["reason"] == "MUTATION_SCOPE_VIOLATION"
