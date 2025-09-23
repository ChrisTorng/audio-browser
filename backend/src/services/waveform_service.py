from __future__ import annotations
from pathlib import Path
import os

WAVEFORM_DIR = Path(os.environ.get("WAVEFORM_DIR", "waveforms"))
WAVEFORM_DIR.mkdir(parents=True, exist_ok=True)


async def get_or_generate_waveform(file_id: str) -> str:
    """Return a filesystem path to waveform PNG, generating a 1x1 placeholder if missing."""
    target = WAVEFORM_DIR / f"{file_id}.png"
    if not target.exists():
        placeholder = (
            b"\x89PNG\r\n\x1a\n"
            b"\x00\x00\x00\rIHDR"
            b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
            b"\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x05\x00\x01\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        target.write_bytes(placeholder)
    return str(target)
