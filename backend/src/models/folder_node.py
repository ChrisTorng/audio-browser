from pydantic import BaseModel
from typing import List, Union, Optional
from .audio_file import AudioFile

class FolderNode(BaseModel):
    id: str
    name: str
    path: str  # relative to root
    children_loaded: bool = False
    expanded: bool = False
    children: Optional[List[Union['FolderNode', AudioFile]]] = None  # lazy loaded

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {}
