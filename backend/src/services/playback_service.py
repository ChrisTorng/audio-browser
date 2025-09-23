from __future__ import annotations
from typing import Dict, Any

async def get_metadata(file_id: str) -> Dict[str, Any]:
    return {"id": file_id, "duration": 0.0, "format": "mp3"}
