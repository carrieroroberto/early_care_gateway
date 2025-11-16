from pydantic import BaseModel
from typing import Dict, Any

class LogEntryDTO(BaseModel):
    event_type: str
    details: Dict[str, Any]