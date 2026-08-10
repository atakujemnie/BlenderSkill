import json
from pathlib import Path

from executors.asset_repository import initialize, list_revisions, load, save
from executors.asset_state_runtime import add_correction


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "lafar_street_bench_vnext.json"


def _asset():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_repository_persists_current_state_and_immutable_revisions(tmp_path):
    initial = initialize(tmp_path, _asset())
    assert initial["status"] == "PASS"
    assert list_revisions(tmp_path, "ASSET-005")["revisions"] == [1]

    changed = add_correction(
        initial["asset"],
        {"id": "COR-021", "component_id": "BACKREST", "priority": "HARD", "kind": "COMMENT"},
    )["asset"]
    persisted = save(tmp_path, changed, expected_revision=1)
    assert persisted["status"] == "PASS"
    assert persisted["revision"] == 2
    assert list_revisions(tmp_path, "ASSET-005")["revisions"] == [1, 2]

    old = load(tmp_path, "ASSET-005", revision=1)
    current = load(tmp_path, "ASSET-005")
    assert old["asset"]["corrections"] == []
    assert current["asset"]["corrections"][0]["id"] == "COR-021"


def test_optimistic_revision_conflict_prevents_agent_overwrite(tmp_path):
    initial = initialize(tmp_path, _asset())
    changed = add_correction(
        initial["asset"],
        {"id": "COR-022", "component_id": "SEAT", "priority": "HARD", "kind": "COMMENT"},
    )["asset"]
    result = save(tmp_path, changed, expected_revision=99)
    assert result["status"] == "CONFLICT"
    assert result["blockers"][0]["reason"] == "ASSET_REVISION_CONFLICT"
