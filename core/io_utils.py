from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_text_file(path: str | Path) -> str:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".json", ".csv"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as e:
            raise RuntimeError("Install pypdf to read PDFs: pip install pypdf") from e
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    if suffix == ".docx":
        try:
            from docx import Document
        except ImportError as e:
            raise RuntimeError("Install python-docx to read DOCX files: pip install python-docx") from e
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError(f"Unsupported file type: {suffix}")


def write_json(path: str | Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
