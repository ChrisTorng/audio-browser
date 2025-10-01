from pydantic import BaseModel
from typing import List, Optional

class UserPreference(BaseModel):
    id: str = "local"
    last_expanded_paths: Optional[List[str]] = None
    last_selected_audio_id: Optional[str] = None
    display_density: str = "compact"  # compact / comfortable
