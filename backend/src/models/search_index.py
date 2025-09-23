from pydantic import BaseModel
from typing import List

class SearchIndexEntry(BaseModel):
    term: str
    audio_file_ids: List[str]
    updated_at: str
