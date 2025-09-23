import re
from typing import List

_SPLIT_RE = re.compile(r"[\s/_.\\-]+")

def tokenize(text: str) -> List[str]:
    text = text.lower().strip()
    if not text:
        return []
    parts = [p for p in _SPLIT_RE.split(text) if p]
    # 去重但保留順序
    seen = set()
    ordered = []
    for p in parts:
        if p not in seen:
            seen.add(p)
            ordered.append(p)
    return ordered
