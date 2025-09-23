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


def _count_supported_files(root_path: Path) -> int:
    count = 0
    for _dirpath, _dirnames, filenames in os.walk(root_path):
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in SUPPORTED_FORMATS:
                count += 1
    return count


def _iter_supported_files(root_path: Path):
    for dirpath, _dirnames, filenames in os.walk(root_path):
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in SUPPORTED_FORMATS:
                yield Path(dirpath) / fn, ext


def _audio_file_from_path(root_path: Path, full_path: Path, ext: str) -> AudioFile:
    rel = str(full_path.relative_to(root_path))
    file_id = _hash_relative(rel)
    size = full_path.stat().st_size
    return AudioFile(
        id=file_id,
        display_name=full_path.name,
        relative_path=rel,
        duration_seconds=None,
        file_size=size,
        format=ext.lstrip('.'),
        waveform_png_path=None,
    )


async def start_scan(root: str):
    root_path = Path(root)
    if not root_path.exists():
        raise FileNotFoundError(root)
    if _scan_state["running"]:
        return  # already running
    _scan_state.update({"running": True, "progress": 0, "total": 0, "last_root": str(root_path)})

    total_files = _count_supported_files(root_path)
    _scan_state["total"] = total_files

    collected: List[AudioFile] = []
    processed = 0
    for full_path, ext in _iter_supported_files(root_path):
        audio = _audio_file_from_path(root_path, full_path, ext)
        collected.append(audio)
        processed += 1
        _scan_state["progress"] = processed
        if processed % 50 == 0:
            await asyncio.sleep(0)

    search_service.build_index(collected)
    global _files
    _files = collected
    _scan_state.update({"running": False, "progress": processed})


async def get_status():
    return _scan_state.copy()


def get_scanned_files() -> List[AudioFile]:
    return list(_files)
