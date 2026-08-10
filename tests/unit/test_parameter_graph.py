import json
from pathlib import Path

from executors.parameter_graph import resolve


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "lafar_street_bench_vnext.json"


def test_bench_relational_dimensions_resolve_without_llm_arithmetic():
    asset = json.loads(FIXTURE.read_text(encoding="utf-8"))
    result = resolve({"components": asset["components"]})
    assert result["status"] == "PASS"
    assert result["flat_values"]["LEFT_SUPPORT.depth"] == 535.0
    assert result["flat_values"]["RIGHT_SUPPORT.width"] == 210.0
    assert result["flat_values"]["SEAT.width"] == 1580.0
    assert result["flat_values"]["BACKREST.width"] == 1580.0
    assert result["flat_values"]["BACKREST.info_strip_width"] == 1500.0


def test_missing_reference_fails_explicitly():
    result = resolve(
        {
            "components": {
                "A": {"dimensions": {"width": {"expr": "B.width + 1"}}},
            }
        }
    )
    assert result["status"] == "FAIL"
    assert result["blockers"][0]["reason"] == "PARAMETER_REFERENCE_MISSING"


def test_cycle_fails_explicitly():
    result = resolve(
        {
            "components": {
                "A": {"dimensions": {"width": {"expr": "B.width + 1"}}},
                "B": {"dimensions": {"width": {"expr": "A.width + 1"}}},
            }
        }
    )
    assert result["status"] == "FAIL"
    assert result["blockers"][0]["reason"] == "PARAMETER_DEPENDENCY_CYCLE"
