import json
from pathlib import Path

from executors.asset_state_runtime import add_correction, advance_stage, resolve_correction, validate_asset


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "lafar_street_bench_vnext.json"


def _asset():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_bench_fixture_is_valid_asset_state():
    verdict = validate_asset(_asset())
    assert verdict["status"] == "PASS"
    assert verdict["component_count"] == 5
    assert verdict["root_component_id"] == "BENCH"


def test_human_correction_becomes_persistent_state_and_dirties_accepted_component():
    asset = _asset()
    asset["components"]["BACKREST"]["state"] = "ACCEPTED"
    result = add_correction(
        asset,
        {
            "id": "COR-018",
            "component_id": "BACKREST",
            "stage": "STRUCTURAL_GEOMETRY",
            "kind": "PARAMETER_OVERRIDE",
            "parameter": "angle",
            "value": 12,
            "unit": "deg",
            "priority": "HARD",
        },
    )
    assert result["status"] == "PASS"
    assert result["asset"]["revision"] == 2
    assert result["asset"]["components"]["BACKREST"]["state"] == "DIRTY"
    assert result["asset"]["corrections"][0]["status"] == "OPEN"
    assert asset["corrections"] == []


def test_open_hard_correction_blocks_stage_advance_until_resolved():
    added = add_correction(
        _asset(),
        {"id": "COR-019", "component_id": "SEAT", "priority": "HARD", "kind": "COMMENT"},
    )
    blocked = advance_stage(added["asset"], "BLOCKOUT")
    assert blocked["status"] == "BLOCKED"
    assert blocked["blockers"][0]["reason"] == "OPEN_HARD_CORRECTIONS"

    resolved = resolve_correction(added["asset"], "COR-019", resolution={"artifact_id": "render:r2"})
    assert resolved["status"] == "PASS"
    assert resolved["asset"]["corrections"][0]["resolved_in_revision"] == 3

    advanced = advance_stage(resolved["asset"], "BLOCKOUT")
    assert advanced["status"] == "PASS"
    assert advanced["asset"]["stage"] == "BLOCKOUT"
