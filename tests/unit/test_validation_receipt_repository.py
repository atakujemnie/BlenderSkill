from executors.validation_receipt_repository import initialize, load, publish, query


def _receipt(receipt_id="R1", validator_id="SCENE_COMPONENT_VALIDATION"):
    return {
        "receipt_id": receipt_id,
        "validator_id": validator_id,
        "validator_version": "0.21.0",
        "asset_id": "ASSET-1",
        "asset_revision": 4,
        "component_id": "PART",
        "scene_revision": 2,
        "status": "PASS",
        "source": "SYSTEM",
    }


def test_receipts_are_persistent_immutable_and_revisioned(tmp_path):
    assert initialize(tmp_path, "ASSET-1")["status"] == "PASS"
    first = publish(tmp_path, "ASSET-1", _receipt(), expected_revision=1)
    assert first["status"] == "PASS", first
    assert first["revision"] == 2

    loaded = load(tmp_path, "ASSET-1")
    assert loaded["status"] == "PASS"
    assert loaded["revision"] == 2
    assert loaded["receipts"][0]["receipt_id"] == "R1"

    duplicate = publish(tmp_path, "ASSET-1", _receipt(), expected_revision=2)
    assert duplicate["status"] == "FAIL"
    assert duplicate["blockers"][0]["reason"] == "VALIDATION_RECEIPT_ID_IMMUTABLE"


def test_query_is_revision_component_scene_and_validator_scoped(tmp_path):
    initialize(tmp_path, "ASSET-1")
    publish(tmp_path, "ASSET-1", _receipt(), expected_revision=1)
    publish(tmp_path, "ASSET-1", _receipt("R2", "REPRESENTATION_CONTRACT_GATE"), expected_revision=2)

    result = query(
        tmp_path,
        "ASSET-1",
        component_id="PART",
        asset_revision=4,
        scene_revision=2,
        validator_ids=["REPRESENTATION_CONTRACT_GATE"],
    )
    assert result["status"] == "PASS"
    assert [item["receipt_id"] for item in result["receipts"]] == ["R2"]


def test_worker_source_cannot_publish_trusted_receipt(tmp_path):
    initialize(tmp_path, "ASSET-1")
    result = publish(tmp_path, "ASSET-1", {**_receipt(), "source": "WORKER"}, expected_revision=1)
    assert result["status"] == "FAIL"
    assert result["blockers"][0]["reason"] == "VALIDATION_RECEIPT_SOURCE_MUST_BE_SYSTEM"
