from executors.scene_component_snapshot import build
from executors.scene_snapshot_repository import list_revisions, load, publish


def _snapshot(scene_revision: int, depth: int) -> dict:
    return build(
        {
            "asset_id": "ASSET-005",
            "asset_revision": 1,
            "scene_revision": scene_revision,
            "objects": [
                {
                    "object_id": "bench.backrest.shell",
                    "component_id": "BACKREST",
                    "object_type": "MESH",
                    "dimensions_mm": [1580, depth, 390],
                }
            ],
        }
    )["snapshot"]


def test_scene_snapshots_are_revisioned_and_reloadable(tmp_path):
    first = _snapshot(1, 72)
    second = _snapshot(2, 76)
    assert publish(tmp_path, first)["status"] == "PASS"
    assert publish(tmp_path, second)["status"] == "PASS"

    current = load(tmp_path, "ASSET-005")
    old = load(tmp_path, "ASSET-005", scene_revision=1)
    assert current["snapshot"]["scene_revision"] == 2
    assert old["snapshot"]["objects"][0]["dimensions_mm"][1] == 72
    assert list_revisions(tmp_path, "ASSET-005")["scene_revisions"] == [1, 2]


def test_scene_snapshot_rejects_non_monotonic_revision_and_tampered_hash(tmp_path):
    first = _snapshot(1, 72)
    assert publish(tmp_path, first)["status"] == "PASS"
    assert publish(tmp_path, first)["blockers"][0]["reason"] == "SCENE_REVISION_NOT_MONOTONIC"

    tampered = dict(_snapshot(2, 76))
    tampered["snapshot_hash"] = "invalid"
    result = publish(tmp_path, tampered)
    assert result["status"] == "FAIL"
    assert result["blockers"][0]["reason"] == "SNAPSHOT_HASH_MISMATCH"
