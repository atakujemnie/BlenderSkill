from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "studio" / "server.py"
text = path.read_text(encoding="utf-8")


def rep(old, new, label):
    global text
    if old not in text:
        raise SystemExit(f"missing patch anchor: {label}")
    text = text.replace(old, new, 1)

rep(
    "    get_studio,\n    list_assets,\n",
    "    get_fidelity_review,\n    get_studio,\n    list_assets,\n",
    "get import",
)
rep(
    "    promote_production_tasks,\n    publish_scene,\n",
    "    promote_production_tasks,\n    publish_fidelity_review,\n    publish_scene,\n",
    "publish import",
)
rep('SERVER_VERSION = "0.21.0"', 'SERVER_VERSION = "0.22.0"', "version")
rep(
    '''            if len(parts) == 4 and parts[:2] == ["api", "assets"] and parts[3] == "studio":\n                query = parse_qs(parsed.query)\n                component = query.get("component", [None])[0]\n                self._result(get_studio(runtime_root, parts[2], component_id=component))\n                return\n''',
    '''            if len(parts) == 4 and parts[:2] == ["api", "assets"] and parts[3] == "studio":\n                query = parse_qs(parsed.query)\n                component = query.get("component", [None])[0]\n                self._result(get_studio(runtime_root, parts[2], component_id=component))\n                return\n            if len(parts) == 4 and parts[:2] == ["api", "assets"] and parts[3] == "fidelity-review":\n                self._result(get_fidelity_review(runtime_root, parts[2]))\n                return\n''',
    "get fidelity route",
)
rep(
    '''            if len(parts) == 4 and parts[3] == "scene":\n                report = body.get("scene", body)\n''',
    '''            if len(parts) == 4 and parts[3] == "fidelity-review":\n                review = body.get("review")\n                if not isinstance(review, Mapping):\n                    raise ValueError("FIDELITY_REVIEW_MAPPING_REQUIRED")\n                self._result(\n                    publish_fidelity_review(\n                        runtime_root,\n                        asset_id,\n                        review,\n                        expected_review_revision=self._required_int(body, "expected_review_revision"),\n                    )\n                )\n                return\n            if len(parts) == 4 and parts[3] == "scene":\n                report = body.get("scene", body)\n''',
    "post fidelity route",
)
path.write_text(text, encoding="utf-8")

# Existing operational HTTP regression should track the current server version.
test = ROOT / "tests" / "integration" / "test_v021_studio_http.py"
t = test.read_text(encoding="utf-8")
t = t.replace('assert health["version"] == "0.21.0"', 'assert health["version"] == "0.22.0"')
test.write_text(t, encoding="utf-8")
