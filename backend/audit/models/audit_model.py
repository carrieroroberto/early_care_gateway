from pydantic import BaseModel
from typing import Dict, Any

class LogEntry(BaseModel):
    event_type: str
    details: Dict[str, Any]