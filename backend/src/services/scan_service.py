from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
import os
import asyncio
import hashlib
from ..models.audio_file import AudioFile
from . import search_service

_scan_state: Dict[str, Any] = {"running": False, "progress": 0, "total": 0, "last_root": None}
_files: List[AudioFile] = []
SUPPORTED_FORMATS = {".mp3", ".wav", ".flac", ".ogg", ".aac"}


def _hash_relative(rel_path: str) -> str:
    return hashlib.sha1(rel_path.encode("utf-8")).hexdigest()


async def start_scan(root: str):
    root_path = Path(root)
    if not root_path.exists():
        raise FileNotFoundError(root)
    if _scan_state["running"]:
        return  # already running
    _scan_state.update({"running": True, "progress": 0, "total": 0, "last_root": str(root_path)})

    collected: List[AudioFile] = []
    total_files = 0
    for dirpath, _dirnames, filenames in os.walk(root_path):
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in SUPPORTED_FORMATS:
                continue
            total_files += 1
    _scan_state["total"] = total_files

    processed = 0
    for dirpath, _dirnames, filenames in os.walk(root_path):
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in SUPPORTED_FORMATS:
                continue
            full_path = Path(dirpath) / fn
            rel = str(full_path.relative_to(root_path))
            file_id = _hash_relative(rel)
            size = full_path.stat().st_size
            audio = AudioFile(
                id=file_id,
                display_name=fn,
                relative_path=rel,
                duration_seconds=None,  # duration extraction deferred
                file_size=size,
                format=ext.lstrip('.'),
                waveform_png_path=None,
            )
            collected.append(audio)
            processed += 1
            if total_files:
                _scan_state["progress"] = processed
            # Yield control occasionally
            if processed % 50 == 0:
                await asyncio.sleep(0)

    # Build search index from collected
    search_service.build_index(collected)
    global _files
    _files = collected
    _scan_state["running"] = False
    _scan_state["progress"] = processed


async def get_status():
    return _scan_state.copy()


def get_scanned_files() -> List[AudioFile]:
    return list(_files)
