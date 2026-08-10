from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"


def _constants(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    values: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                values[node.targets[0].id] = node.value.value
    return values


def validate(manifest: dict) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    executors = manifest.get("executors", []) or []
    declared_paths = {str(item.get("executor") or "") for item in executors if item.get("executor")}

    for item in executors:
        if str(item.get("maturity") or "") != "EXECUTOR_READY":
            continue
        skill_id = str(item.get("id") or "")
        contract = ROOT / str(item.get("contract") or "")
        executor_rel = str(item.get("executor") or "")
        executor = ROOT / executor_rel
        tests = [ROOT / str(path) for path in item.get("tests", []) or []]

        if not contract.is_file():
            errors.append({"code": "MISSING_CONTRACT", "id": skill_id})
        if not executor.is_file():
            errors.append({"code": "MISSING_EXECUTOR", "id": skill_id})
            continue
        if not tests or not any(path.is_file() for path in tests):
            errors.append({"code": "MISSING_EXECUTOR_TEST", "id": skill_id})

        constants = _constants(executor)
        if constants.get("EXECUTOR_ID") != skill_id:
            errors.append({"code": "EXECUTOR_ID_MISMATCH", "id": skill_id})
        if not constants.get("EXECUTOR_VERSION"):
            errors.append({"code": "EXECUTOR_VERSION_MISSING", "id": skill_id})

    for executor in sorted((ROOT / "executors").glob("*.py")):
        constants = _constants(executor)
        if constants.get("EXECUTOR_ID") and executor.relative_to(ROOT).as_posix() not in declared_paths:
            errors.append({"code": "ORPHAN_EXECUTOR", "id": constants["EXECUTOR_ID"]})

    return errors


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = validate(manifest)
    if errors:
        raise SystemExit(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
    print(json.dumps({"status": "PASS", "executor_ready": sum(1 for x in manifest.get("executors", []) if x.get("maturity") == "EXECUTOR_READY")}))


if __name__ == "__main__":
    main()
