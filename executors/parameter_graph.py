from __future__ import annotations

"""Resolve relational component dimensions without arbitrary Python eval."""

import ast
from typing import Any, Mapping

EXECUTOR_ID = "PARAMETER_GRAPH"
EXECUTOR_VERSION = "0.1.0"

_ALLOWED_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
}
_ALLOWED_UNARY = {ast.UAdd: lambda a: a, ast.USub: lambda a: -a}


class ParameterError(ValueError):
    pass


def _reference(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parts: list[str] = []
        current: ast.AST = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
            return ".".join(reversed(parts))
    return None


def _dependencies(expr: str) -> set[str]:
    tree = ast.parse(expr, mode="eval")
    deps: set[str] = set()
    for node in ast.walk(tree):
        ref = _reference(node)
        if ref and "." in ref:
            deps.add(ref)
        if isinstance(node, (ast.Call, ast.Subscript, ast.Lambda, ast.Dict, ast.List, ast.Tuple, ast.Compare, ast.BoolOp)):
            raise ParameterError("EXPRESSION_NODE_FORBIDDEN")
    return deps


def _eval(node: ast.AST, values: Mapping[str, float]) -> float:
    if isinstance(node, ast.Expression):
        return _eval(node.body, values)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    ref = _reference(node)
    if ref is not None:
        if ref not in values:
            raise ParameterError(f"REFERENCE_UNRESOLVED:{ref}")
        return float(values[ref])
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        left = _eval(node.left, values)
        right = _eval(node.right, values)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ParameterError("DIVISION_BY_ZERO")
        return float(_ALLOWED_BINOPS[type(node.op)](left, right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY:
        return float(_ALLOWED_UNARY[type(node.op)](_eval(node.operand, values)))
    raise ParameterError(f"EXPRESSION_NODE_FORBIDDEN:{type(node).__name__}")


def _flatten(spec: Mapping[str, Any]) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    params: dict[str, dict[str, Any]] = {}
    blockers: list[dict[str, Any]] = []
    components = spec.get("components", {})
    if not isinstance(components, Mapping):
        return {}, [{"reason": "COMPONENTS_MAPPING_REQUIRED"}]
    for component_id, raw_component in components.items():
        if not isinstance(raw_component, Mapping):
            blockers.append({"reason": "COMPONENT_INVALID", "component_id": str(component_id)})
            continue
        dimensions = raw_component.get("dimensions", {})
        if not isinstance(dimensions, Mapping):
            blockers.append({"reason": "DIMENSIONS_MAPPING_REQUIRED", "component_id": str(component_id)})
            continue
        for parameter_id, raw in dimensions.items():
            key = f"{component_id}.{parameter_id}"
            if isinstance(raw, (int, float)):
                params[key] = {"value": float(raw), "unit": None, "locked": False}
            elif isinstance(raw, Mapping):
                item = dict(raw)
                has_value = item.get("value") is not None
                has_expr = bool(str(item.get("expr") or "").strip())
                if has_value == has_expr:
                    blockers.append({"reason": "PARAMETER_REQUIRES_EXACTLY_ONE_VALUE_OR_EXPR", "parameter": key})
                    continue
                params[key] = item
            else:
                blockers.append({"reason": "PARAMETER_INVALID", "parameter": key})
    return params, blockers


def resolve(spec: Mapping[str, Any]) -> dict[str, Any]:
    params, blockers = _flatten(spec)
    if blockers:
        return {"status": "FAIL", "validator_id": EXECUTOR_ID, "blockers": blockers}

    values: dict[str, float] = {}
    metadata: dict[str, dict[str, Any]] = {}
    unresolved = set(params)
    dependencies: dict[str, set[str]] = {}

    for key, item in params.items():
        if item.get("value") is not None:
            try:
                values[key] = float(item["value"])
            except (TypeError, ValueError):
                blockers.append({"reason": "PARAMETER_VALUE_INVALID", "parameter": key})
            metadata[key] = {"unit": item.get("unit"), "locked": bool(item.get("locked", False)), "source": "LITERAL"}
            unresolved.discard(key)
        else:
            expr = str(item.get("expr") or "")
            try:
                dependencies[key] = _dependencies(expr)
            except (SyntaxError, ParameterError) as exc:
                blockers.append({"reason": str(exc), "parameter": key})
            metadata[key] = {
                "unit": item.get("unit"),
                "locked": bool(item.get("locked", False)),
                "source": "EXPRESSION",
                "expr": expr,
            }

    if blockers:
        return {"status": "FAIL", "validator_id": EXECUTOR_ID, "blockers": blockers}

    missing = sorted({dep for deps in dependencies.values() for dep in deps if dep not in params})
    if missing:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "PARAMETER_REFERENCE_MISSING", "references": missing}],
        }

    while unresolved:
        progressed = False
        for key in sorted(unresolved):
            deps = dependencies.get(key, set())
            if not deps.issubset(values):
                continue
            expr = str(params[key]["expr"])
            try:
                values[key] = _eval(ast.parse(expr, mode="eval"), values)
            except (SyntaxError, ParameterError) as exc:
                return {
                    "status": "FAIL",
                    "validator_id": EXECUTOR_ID,
                    "blockers": [{"reason": str(exc), "parameter": key}],
                }
            unresolved.remove(key)
            progressed = True
        if not progressed:
            return {
                "status": "FAIL",
                "validator_id": EXECUTOR_ID,
                "blockers": [{"reason": "PARAMETER_DEPENDENCY_CYCLE", "parameters": sorted(unresolved)}],
            }

    nested: dict[str, dict[str, Any]] = {}
    for key in sorted(values):
        component_id, parameter_id = key.split(".", 1)
        nested.setdefault(component_id, {})[parameter_id] = {
            "value": values[key],
            **metadata[key],
        }

    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "parameter_count": len(values),
        "resolved": nested,
        "flat_values": {key: values[key] for key in sorted(values)},
        "blockers": [],
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "resolve"]
