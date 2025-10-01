from __future__ import annotations
from typing import Dict, List
from .search_service import _FILES

# Simple derived statistics using in-memory files map

def compute_stats() -> Dict[str, object]:
    total = len(_FILES)
    by_extension: Dict[str, int] = {}
    durations: List[float] = []
    total_size = 0
    for f in _FILES.values():
        ext = f.display_name.rsplit('.', 1)[-1].lower() if '.' in f.display_name else ''
        by_extension[ext] = by_extension.get(ext, 0) + 1
        if f.duration_seconds is not None:
            durations.append(f.duration_seconds)
        if f.file_size is not None:
            total_size += f.file_size

    avg_duration = sum(durations)/len(durations) if durations else 0.0
    return {
        "total_files": total,
        "by_extension": by_extension,
        "average_duration": avg_duration,
        "total_file_size": total_size,
    }
