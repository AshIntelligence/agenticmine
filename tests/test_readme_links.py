from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def _local_targets(readme: Path):
    text = readme.read_text(encoding="utf-8")
    for raw in LINK_RE.findall(text):
        target = raw.strip().split()[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if target:
            yield target


def test_local_readme_links_resolve():
    broken = []
    for readme in ROOT.rglob("README.md"):
        for target in _local_targets(readme):
            resolved = (readme.parent / target).resolve()
            if not resolved.exists():
                broken.append(f"{readme.relative_to(ROOT)} -> {target}")
    assert not broken, "Broken local README links:\n" + "\n".join(sorted(broken))
