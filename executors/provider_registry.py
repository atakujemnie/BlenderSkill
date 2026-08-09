from __future__ import annotations

"""Load and query the canonical provider registry."""

from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping
import json
import re

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "data" / "provider_registry.json"


def _norm(value: Any) -> str:
    text = str(value or "").lower().replace("_", " ").replace("-", " ").replace(".", " ")
    return " ".join(re.findall(r"[a-z0-9]+", text))


@lru_cache(maxsize=1)
def load_registry() -> dict[str, Any]:
    payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    providers = payload.get("providers") or {}
    if not isinstance(providers, dict):
        raise ValueError("PROVIDER_REGISTRY_INVALID")
    return payload


def provider_definitions() -> Mapping[str, Mapping[str, Any]]:
    return load_registry()["providers"]


def match_provider(module_name: str, display_name: str) -> tuple[str | None, Mapping[str, Any] | None]:
    module_norm = _norm(module_name)
    display_norm = _norm(display_name)
    combined = _norm(f"{module_name} {display_name}")
    haystacks = {module_norm, display_norm, combined}

    best: tuple[int, str, Mapping[str, Any]] | None = None
    for provider_id, definition in provider_definitions().items():
        candidates = list(definition.get("aliases") or []) + list(definition.get("module_patterns") or [])
        score = 0
        for candidate in candidates:
            needle = _norm(candidate)
            if not needle:
                continue
            if needle in haystacks:
                score = max(score, 100 + len(needle))
            elif any(needle in hay for hay in haystacks):
                score = max(score, len(needle))
        if score and (best is None or score > best[0]):
            best = (score, provider_id, definition)
    return (best[1], best[2]) if best else (None, None)


def get_provider(provider_id: str) -> Mapping[str, Any] | None:
    return provider_definitions().get(provider_id)
