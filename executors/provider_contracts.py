from __future__ import annotations

"""Canonical provider protocol shared by discovery, probes, quality and selection."""

from enum import Enum
from typing import Any, Mapping

EXECUTOR_VERSION = "0.18.0"


class SourceKind(str, Enum):
    READY_ASSET_SOURCE = "READY_ASSET_SOURCE"
    PROCEDURAL_GENERATOR = "PROCEDURAL_GENERATOR"
    EXTERNAL_GENERATOR = "EXTERNAL_GENERATOR"
    UTILITY = "UTILITY"
    BUILTIN_BACKEND = "BUILTIN_BACKEND"
    UNKNOWN = "UNKNOWN"


class DiscoveryState(str, Enum):
    DISCOVERED = "DISCOVERED"
    NOT_DISCOVERED = "NOT_DISCOVERED"
    DISCOVERY_MISMATCH = "DISCOVERY_MISMATCH"


class ProbeState(str, Enum):
    PROBE_REQUIRED = "PROBE_REQUIRED"
    PASS = "PASS"
    FAIL = "FAIL"
    DISABLED = "DISABLED"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class DomainState(str, Enum):
    MATCH = "MATCH"
    GENERIC_MATCH = "GENERIC_MATCH"
    MISMATCH = "MISMATCH"
    UNKNOWN = "UNKNOWN"


class QualityState(str, Enum):
    UNRATED = "UNRATED"
    PASS = "PASS"
    REJECTED = "REJECTED"


class SelectionState(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    ELIGIBLE_GENERIC = "ELIGIBLE_GENERIC"
    REJECTED = "REJECTED"
    SELECTED = "SELECTED"
    BLOCKED = "BLOCKED"


SOURCE_KINDS = {item.value for item in SourceKind}
PROBE_STATES = {item.value for item in ProbeState}
DISCOVERY_STATES = {item.value for item in DiscoveryState}
DOMAIN_STATES = {item.value for item in DomainState}
QUALITY_STATES = {item.value for item in QualityState}
SELECTION_STATES = {item.value for item in SelectionState}


def _enum_value(value: Any, enum_type: type[Enum], default: Enum) -> str:
    text = str(value or default.value)
    allowed = {item.value for item in enum_type}
    return text if text in allowed else str(default.value)


def normalize_provider_record(record: Mapping[str, Any]) -> dict[str, Any]:
    out = dict(record)
    out["provider_id"] = str(out.get("provider_id") or "").strip()
    out["source_kind"] = _enum_value(out.get("source_kind"), SourceKind, SourceKind.UNKNOWN)
    out["discovery_state"] = _enum_value(
        out.get("discovery_state") or ("DISCOVERED" if out.get("discovered", True) else "NOT_DISCOVERED"),
        DiscoveryState,
        DiscoveryState.NOT_DISCOVERED,
    )
    out["probe_state"] = _enum_value(
        out.get("probe_state") or out.get("runtime_probe_status"),
        ProbeState,
        ProbeState.PROBE_REQUIRED,
    )
    out["runtime_probe_status"] = out["probe_state"]
    out["domains"] = sorted({str(x).strip().upper() for x in out.get("domains", []) or [] if str(x).strip()})
    out["enabled"] = bool(out.get("enabled", False))
    out["discovered"] = out["discovery_state"] == DiscoveryState.DISCOVERED.value
    return out


def validate_provider_record(record: Mapping[str, Any]) -> list[dict[str, Any]]:
    item = normalize_provider_record(record)
    errors: list[dict[str, Any]] = []
    if not item["provider_id"]:
        errors.append({"reason": "PROVIDER_ID_REQUIRED"})
    if item["source_kind"] not in SOURCE_KINDS:
        errors.append({"reason": "INVALID_SOURCE_KIND", "value": item["source_kind"]})
    if item["probe_state"] not in PROBE_STATES:
        errors.append({"reason": "INVALID_PROBE_STATE", "value": item["probe_state"]})
    if item["discovery_state"] not in DISCOVERY_STATES:
        errors.append({"reason": "INVALID_DISCOVERY_STATE", "value": item["discovery_state"]})
    return errors
