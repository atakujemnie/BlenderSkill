from __future__ import annotations

"""Registered executable identity for the provider capability probe matrix."""

from typing import Any, Mapping

from executors.provider_probe_runner import run_inventory_probes, run_probe

EXECUTOR_ID = "PROVIDER_CAPABILITY_PROBE_MATRIX"
EXECUTOR_VERSION = "0.18.0"


def evaluate_provider(provider: Mapping[str, Any]) -> dict[str, Any]:
    return run_probe(provider)


def evaluate_inventory(inventory: Mapping[str, Any], provider_ids: list[str] | None = None) -> dict[str, Any]:
    return run_inventory_probes(inventory, provider_ids=provider_ids)
