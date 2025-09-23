from __future__ import annotations
from typing import Dict, Any, Optional
from .scan_service import get_scanned_files


async def get_metadata(file_id: str) -> Dict[str, Any]:
    for f in get_scanned_files():
        if f.id == file_id:
            return {
                "id": f.id,
                "display_name": f.display_name,
                "relative_path": f.relative_path,
                "duration_seconds": f.duration_seconds,
                "file_size": f.file_size,
                "format": f.format,
            }
    return {"error": "not_found", "id": file_id}
