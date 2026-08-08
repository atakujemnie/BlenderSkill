from __future__ import annotations

"""Pure-Python runtime path validation helpers.

The contract favors explicit profile/build authority and rejects ambiguous
lookalike roots. It does not scan the filesystem and pick the first match.
"""

from pathlib import Path
from typing import Iterable


def canonical(path) -> Path:
    return Path(path).expanduser().resolve()


def is_within(path, root) -> bool:
    p = canonical(path)
    r = canonical(root)
    try:
        p.relative_to(r)
        return True
    except ValueError:
        return False


def validate_runtime_context(
    *,
    project_root,
    engine_asset_directory,
    game_asset_root,
    forbidden_roots: Iterable[str] = (),
    require_exists: bool = True,
) -> dict:
    project = canonical(project_root)
    engine_assets = canonical(engine_asset_directory)
    game_assets = canonical(game_asset_root)
    forbidden = [canonical(x) for x in forbidden_roots]

    reasons: list[str] = []
    if require_exists:
        if not project.is_dir():
            reasons.append("PROJECT_ROOT_MISSING")
        if not engine_assets.is_dir():
            reasons.append("ENGINE_ASSET_DIRECTORY_MISSING")
        if not game_assets.is_dir():
            reasons.append("GAME_ASSET_ROOT_MISSING")

    if not is_within(engine_assets, project):
        reasons.append("ENGINE_ASSET_DIRECTORY_OUTSIDE_PROJECT")
    if not is_within(game_assets, engine_assets):
        reasons.append("GAME_ASSET_ROOT_OUTSIDE_ENGINE_ASSET_DIRECTORY")
    if any(game_assets == x for x in forbidden):
        reasons.append("FORBIDDEN_LOOKALIKE_ROOT_SELECTED")

    return {
        "status": "FAIL" if reasons else "PASS",
        "project_root": str(project),
        "engine_asset_directory": str(engine_assets),
        "game_asset_root": str(game_assets),
        "forbidden_roots": [str(x) for x in forbidden],
        "reasons": reasons,
    }


def resolve_profile_relative(project_root, relative_path: str) -> str:
    root = canonical(project_root)
    p = canonical(root / relative_path)
    if not is_within(p, root):
        raise ValueError(f"PROFILE_PATH_ESCAPES_PROJECT: {relative_path}")
    return str(p)


def validate_output_path(path, *, runtime_root, forbidden_roots: Iterable[str] = ()) -> dict:
    p = canonical(path)
    root = canonical(runtime_root)
    forbidden = [canonical(x) for x in forbidden_roots]
    reasons = []
    if not is_within(p, root):
        reasons.append("OUTPUT_OUTSIDE_RUNTIME_ROOT")
    if any(is_within(p, x) for x in forbidden):
        reasons.append("OUTPUT_INSIDE_FORBIDDEN_LOOKALIKE_ROOT")
    return {
        "status": "FAIL" if reasons else "PASS",
        "path": str(p),
        "runtime_root": str(root),
        "reasons": reasons,
    }
