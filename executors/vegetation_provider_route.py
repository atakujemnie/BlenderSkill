from __future__ import annotations

"""Executable vegetation-provider route backed by the canonical provider orchestrator."""

from typing import Any, Mapping

from executors.provider_orchestrator import evaluate as evaluate_provider_pipeline

EXECUTOR_ID = "VEGETATION_PROVIDER_ROUTE"
EXECUTOR_VERSION = "0.18.0"

VEGETATION_DOMAINS = {"TREE", "WOODY_PLANT", "GRASS", "GROUNDCOVER", "VINE", "SURFACE_GROWTH", "VEGETATION"}


def evaluate(inventory: Mapping[str, Any], *, requested_domains: list[str], **kwargs: Any) -> dict[str, Any]:
    normalized = [str(domain).upper() for domain in requested_domains]
    invalid = sorted(set(normalized) - VEGETATION_DOMAINS)
    if invalid:
        return {
            "status": "BLOCKED",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "NON_VEGETATION_DOMAIN", "domains": invalid}],
        }
    result = evaluate_provider_pipeline(inventory, requested_domains=normalized, **kwargs)
    result["validator_id"] = EXECUTOR_ID
    return result
