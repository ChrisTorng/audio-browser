from __future__ import annotations
from typing import Any, Dict, List, Optional
from pathlib import PurePosixPath
from .scan_service import get_scanned_files


def _ensure_child(node: Dict[str, Any], name: str) -> Dict[str, Any]:
    for ch in node["children"]:
        if ch["name"] == name:
            return ch
    new_child = {"name": name, "type": "folder", "children": []}
    node["children"].append(new_child)
    return new_child


async def get_tree(path: Optional[str] = None) -> Dict[str, Any]:
    files = get_scanned_files()
    root: Dict[str, Any] = {"name": "", "type": "folder", "children": []}
    base_parts = []
    if path:
        base_parts = PurePosixPath(path).parts

    for f in files:
        rel_parts = PurePosixPath(f.relative_path).parts
        if path:
            if tuple(rel_parts[: len(base_parts)]) != base_parts:
                continue
            rel_parts = rel_parts[len(base_parts) :]
        if not rel_parts:
            continue
        cursor = root
        for segment in rel_parts[:-1]:
            cursor = _ensure_child(cursor, segment)
        # file leaf
        cursor["children"].append({
            "name": rel_parts[-1],
            "type": "file",
            "id": f.id,
            "format": f.format,
        })
    return root
