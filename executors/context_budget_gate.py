from __future__ import annotations

"""Decision gate for token/context and per-asset code-sprawl budgets."""

from typing import Any, Mapping

EXECUTOR_ID = "CONTEXT_BUDGET_GATE"
EXECUTOR_VERSION = "0.14.0"


def evaluate(report: Mapping[str, Any], policy: Mapping[str, Any] | None = None) -> dict[str, Any]:
    p = dict(policy or {})
    blockers = []
    warnings = []

    token_limit = int(p.get("max_context_tokens", 30000))
    tokens = int(report.get("context_tokens", 0) or 0)
    if tokens and tokens > token_limit:
        blockers.append({"reason": "CONTEXT_TOKEN_BUDGET_EXCEEDED", "actual": tokens, "maximum": token_limit})

    line_limit = int(p.get("max_asset_specific_generated_lines", 400))
    lines = int(report.get("asset_specific_generated_lines", 0) or 0)
    if lines > line_limit:
        blockers.append({"reason": "ASSET_SPECIFIC_CODE_BUDGET_EXCEEDED", "actual": lines, "maximum": line_limit})

    if bool(report.get("full_source_echo_after_persist", False)):
        blockers.append({"reason": "FULL_SOURCE_ECHO_AFTER_PERSIST"})
    if bool(report.get("reread_unchanged_source_without_need", False)):
        blockers.append({"reason": "UNCHANGED_SOURCE_REREAD"})
    if int(report.get("reusable_executor_misses", 0) or 0) > int(p.get("max_reusable_executor_misses", 0)):
        blockers.append({"reason": "REUSABLE_EXECUTOR_NOT_USED", "count": int(report.get("reusable_executor_misses", 0) or 0)})

    if tokens and tokens > int(p.get("stretch_context_tokens", 20000)) and tokens <= token_limit:
        warnings.append({"reason": "ABOVE_STRETCH_CONTEXT_TARGET", "actual": tokens})

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "blockers": blockers,
        "warnings": warnings,
        "metrics": {
            "context_tokens": tokens,
            "asset_specific_generated_lines": lines,
            "reusable_executor_misses": int(report.get("reusable_executor_misses", 0) or 0),
        },
    }
