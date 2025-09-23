from pydantic import BaseModel, Field
from typing import Optional, Literal

class AudioFile(BaseModel):
    id: str  # path hash
    relative_path: str
    file_name: str
    format: Literal["wav", "mp3", "flac", "ogg", "aac", "unsupported"]
    duration: Optional[float] = None
    size: Optional[int] = None
    waveform_png_path: Optional[str] = None
    star_rating: Optional[int] = Field(default=None, ge=0, le=5)
    description: Optional[str] = Field(default=None, max_length=1024)
    created_at: Optional[str] = None
    last_modified_at: Optional[str] = None
    scan_status: Literal["active", "skipped", "unsupported"] = "active"
