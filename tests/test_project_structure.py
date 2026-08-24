from pathlib import Path

from ui.demo_adapters import CATALOG

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"


def test_catalog_matches_project_directories():
    catalog = {item["slug"] for item in CATALOG}
    directories = {path.name for path in PROJECTS.iterdir() if path.is_dir()}
    assert directories == catalog


def test_every_product_has_engine_and_readme():
    missing = []
    for item in CATALOG:
        folder = PROJECTS / item["slug"]
        for filename in ("main.py", "README.md"):
            if not (folder / filename).is_file():
                missing.append(f"{item['slug']}/{filename}")
    assert missing == []
