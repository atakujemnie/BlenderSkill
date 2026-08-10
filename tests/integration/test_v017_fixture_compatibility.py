import json
from pathlib import Path

from executors.installed_provider_inventory import build_inventory

ROOT = Path(__file__).resolve().parents[2]


def test_v017_inventory_fixture_normalizes_without_semantic_regression():
    raw = json.loads((ROOT / "tests/fixtures/provider_inventory_v017.json").read_text(encoding="utf-8"))
    inventory = build_inventory(raw)
    by_id = {item["provider_id"]: item for item in inventory["providers"]}
    assert by_id["sapling_tree_gen"]["source_kind"] == "PROCEDURAL_GENERATOR"
    assert by_id["sapling_tree_gen"]["probe_state"] == "PROBE_REQUIRED"
    unknown = next(item for key, item in by_id.items() if key.startswith("addon:unknown_fixture"))
    assert unknown["source_kind"] == "UNKNOWN"
    assert unknown["classification_known"] is False
