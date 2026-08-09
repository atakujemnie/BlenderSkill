from __future__ import annotations

"""Small dependency-free semantic version constraint evaluator for Blender runtime."""

import re
from typing import Iterable


def _parts(version: str) -> tuple[int, ...] | None:
    match = re.match(r"^\s*(\d+(?:\.\d+)*)", str(version or ""))
    if not match:
        return None
    return tuple(int(x) for x in match.group(1).split("."))


def _cmp(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    width = max(len(a), len(b))
    aa = a + (0,) * (width - len(a))
    bb = b + (0,) * (width - len(b))
    return (aa > bb) - (aa < bb)


def satisfies(version: str, constraint: str) -> bool:
    actual = _parts(version)
    if actual is None:
        return False
    clauses: Iterable[str] = [x.strip() for x in str(constraint or "").split(",") if x.strip()]
    for clause in clauses:
        match = re.match(r"^(==|!=|>=|<=|>|<)?\s*(\d+(?:\.\d+)*)$", clause)
        if not match:
            raise ValueError(f"INVALID_VERSION_CONSTRAINT:{clause}")
        op = match.group(1) or "=="
        target = _parts(match.group(2))
        assert target is not None
        value = _cmp(actual, target)
        if op == "==" and value != 0: return False
        if op == "!=" and value == 0: return False
        if op == ">=" and value < 0: return False
        if op == "<=" and value > 0: return False
        if op == ">" and value <= 0: return False
        if op == "<" and value >= 0: return False
    return True
