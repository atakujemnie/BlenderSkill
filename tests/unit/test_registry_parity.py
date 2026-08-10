import json
from pathlib import Path

from tools.validate_registry_parity import validate

ROOT = Path(__file__).resolve().parents[2]


def test_executor_ready_registry_has_contract_executor_test_parity():
    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    assert validate(manifest) == []
