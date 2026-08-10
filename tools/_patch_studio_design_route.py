from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "studio" / "server.py"
text = path.read_text(encoding="utf-8")
text = text.replace(
    'STUDIO_HTML = REPO_ROOT / "studio" / "asset_production_studio.html"\n',
    'STUDIO_HTML = REPO_ROOT / "studio" / "asset_production_studio.html"\nDESIGN_STUDIO_HTML = REPO_ROOT / "studio" / "design_system_studio.html"\n',
)
needle = '''            if path in {"/", "/studio", "/index.html"}:\n                self._serve_file(STUDIO_HTML)\n                return\n'''
replacement = needle + '''            if path in {"/design", "/design-system", "/design_system_studio.html"}:\n                self._serve_file(DESIGN_STUDIO_HTML)\n                return\n'''
if needle not in text:
    raise SystemExit("Studio route insertion point not found")
text = text.replace(needle, replacement, 1)
path.write_text(text, encoding="utf-8")
