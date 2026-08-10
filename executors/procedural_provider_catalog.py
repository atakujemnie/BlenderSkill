from __future__ import annotations

"""Backward-compatible facade over the canonical v0.18 provider registry.

Provider metadata must not be authored here. This module exists only so v0.17
callers importing procedural_provider_catalog continue to work during v0.18.
"""

from copy import deepcopy

from executors.provider_registry import get_provider, provider_definitions

CATALOG_AS_OF = "CANONICAL_REGISTRY_V018"


def _legacy_shape(provider_id: str, definition: dict) -> dict:
    item = deepcopy(definition)
    item["provider_id"] = provider_id
    item.setdefault("provider_version", "un-pinned")
    item.setdefault("license", item.get("license_policy"))
    item.setdefault("probe_required", item.get("probe_type") not in {None, "", "none"})
    return item


def get(provider_id: str) -> dict:
    definition = get_provider(provider_id)
    if definition is None:
        raise KeyError(provider_id)
    return _legacy_shape(provider_id, dict(definition))


def all_providers() -> dict[str, dict]:
    return {provider_id: _legacy_shape(provider_id, dict(definition)) for provider_id, definition in provider_definitions().items()}
