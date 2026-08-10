from executors.reference_evidence_repository import initialize, list_revisions, load, remove, upsert


def _evidence(evidence_id: str, component_id: str = "BACKREST") -> dict:
    return {
        "evidence_id": evidence_id,
        "reference_id": "lafar-bench-sheet",
        "component_id": component_id,
        "view": "SIDE",
        "authority": "PRIMARY",
        "feature_ids": ["PROFILE"],
        "roi": [10, 20, 110, 220],
        "artifact_id": f"roi:{evidence_id}",
    }


def test_reference_evidence_repository_revision_history(tmp_path):
    created = initialize(tmp_path, "ASSET-005", {"evidence": [_evidence("EV-1")]})
    assert created["status"] == "PASS"
    assert created["registry"]["revision"] == 1

    changed = upsert(tmp_path, "ASSET-005", _evidence("EV-2", "SEAT"), expected_revision=1)
    assert changed["status"] == "PASS"
    assert changed["revision"] == 2

    current = load(tmp_path, "ASSET-005")
    old = load(tmp_path, "ASSET-005", revision=1)
    assert len(current["registry"]["evidence"]) == 2
    assert len(old["registry"]["evidence"]) == 1

    deleted = remove(tmp_path, "ASSET-005", "EV-1", expected_revision=2)
    assert deleted["status"] == "PASS"
    assert deleted["revision"] == 3
    assert list_revisions(tmp_path, "ASSET-005")["revisions"] == [1, 2, 3]


def test_reference_evidence_repository_rejects_stale_writer(tmp_path):
    assert initialize(tmp_path, "ASSET-005", {"evidence": []})["status"] == "PASS"
    result = upsert(tmp_path, "ASSET-005", _evidence("EV-1"), expected_revision=0)
    assert result["status"] == "CONFLICT"
    assert result["blockers"][0]["reason"] == "REFERENCE_EVIDENCE_REVISION_CONFLICT"
