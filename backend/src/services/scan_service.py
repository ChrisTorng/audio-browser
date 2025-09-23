from __future__ import annotations
from pathlib import Path
import os
from typing import Dict, Any

_scan_state: Dict[str, Any] = {"running": False, "progress": 0, "total": 0}
SUPPORTED_FORMATS = {".mp3", ".wav", ".flac", ".ogg", ".aac"}

async def start_scan(root: str):
    # TODO: implement async dir walk + populate structures
    root_path = Path(root)
    if not root_path.exists():
        raise FileNotFoundError(root)
    _scan_state.update({"running": True, "progress": 0, "total": 0})
    # Stub: instantly finish
    _scan_state.update({"running": False, "progress": 1, "total": 1})

async def get_status():
    return _scan_state.copy()
