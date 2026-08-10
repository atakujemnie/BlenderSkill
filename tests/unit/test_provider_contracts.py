from executors.provider_contracts import ProbeState, SourceKind, normalize_provider_record, validate_provider_record


def test_probe_required_is_canonical_state():
    assert ProbeState.PROBE_REQUIRED.value == "PROBE_REQUIRED"


def test_unknown_source_kind_is_preserved_for_unclassified_provider():
    record = normalize_provider_record({"provider_id": "mystery", "source_kind": "UNKNOWN", "discovered": True})
    assert record["source_kind"] == SourceKind.UNKNOWN.value
    assert record["probe_state"] == ProbeState.PROBE_REQUIRED.value
    assert validate_provider_record(record) == []
