from __future__ import annotations

import json
from pathlib import Path

CONTENT_SUFFIXES = {".pdf", ".html", ".json", ".txt", ".zip", ".csv", ".xlsx"}


def load_sidecar(content_path: Path) -> dict:
    sidecar = content_path.with_suffix(content_path.suffix + ".meta.json")
    if not sidecar.is_file():
        raise FileNotFoundError(f"missing sidecar: {sidecar}")
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"sidecar is not a JSON object: {sidecar}")
    return data


def iter_content_files(root: Path) -> list[Path]:
    if not root.is_dir():
        raise FileNotFoundError(f"content root not found: {root}")
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name.endswith(".meta.json"):
            continue
        if path.suffix.lower() not in CONTENT_SUFFIXES:
            continue
        files.append(path)
    return files
