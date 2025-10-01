from __future__ import annotations
from typing import List, Dict, Optional
from ..lib.tokenizer import tokenize
from ..models.audio_file import AudioFile

# In-memory simple index structure: token -> set[file_id]
_INDEX: Dict[str, set] = {}
_FILES: Dict[str, AudioFile] = {}


def _add_file_to_index(audio: AudioFile):
    _FILES[audio.id] = audio
    terms = set(tokenize(audio.display_name)) | set(tokenize(audio.relative_path))
    for t in terms:
        _INDEX.setdefault(t, set()).add(audio.id)


def get_indexed_count() -> int:
    return len(_FILES)


def clear_index():
    _INDEX.clear()
    _FILES.clear()


def build_index(files: List[AudioFile]):
    clear_index()
    for f in files:
        _add_file_to_index(f)


def search(query: str = "", min_stars: Optional[int] = None, annotations: Optional[dict] = None) -> List[AudioFile]:
    # annotations: file_id -> {star_rating, description}
    if not query.strip():
        candidate_ids = set(_FILES.keys())
    else:
        terms = [t for t in tokenize(query) if t]
        if not terms:
            candidate_ids = set(_FILES.keys())
        else:
            sets = [ _INDEX.get(t, set()) for t in terms ]
            if not sets:
                return []
            candidate_ids = set.intersection(*sets) if sets else set()

    results: List[AudioFile] = []
    for fid in candidate_ids:
        audio = _FILES[fid]
        if min_stars is not None and annotations:
            ann = annotations.get(fid)
            if not ann or ann.get("star_rating") is None or ann.get("star_rating") < min_stars:
                continue
        results.append(audio)

    # simple deterministic order: relative_path then display_name
    results.sort(key=lambda a: (a.relative_path, a.display_name))
    return results
