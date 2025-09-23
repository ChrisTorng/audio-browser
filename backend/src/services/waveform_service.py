from __future__ import annotations
from pathlib import Path
import os
from . import scan_service

PLACEHOLDER_PNG = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


def _find_audio(file_id: str):
    for f in scan_service.get_scanned_files():
        if f.id == file_id:
            return f
    return None


async def get_or_generate_waveform(file_id: str) -> str:
    """回傳與音檔相同資料夾同檔名之 .png 路徑（若不存在則生成 placeholder）。

    Returns relative path (相對於 ROOT_AUDIO_DIR) 以符合規格。
    """
    audio = _find_audio(file_id)
    if not audio:
        raise FileNotFoundError(file_id)
    root = Path(os.environ.get("ROOT_AUDIO_DIR", ".")).resolve()
    audio_abs = root / audio.relative_path
    # derive png path
    stem = audio_abs.stem
    target_abs = audio_abs.with_name(f"{stem}.png")
    if not target_abs.exists():
        target_abs.write_bytes(PLACEHOLDER_PNG)
    # produce relative path
    try:
        rel = target_abs.relative_to(root)
    except ValueError:
        rel = target_abs
    return str(rel)
