# shared_context.py
from typing import Any, Dict, List
from pydantic import BaseModel

class ContextModel(BaseModel):
    schemaVersion: str
    userId: str
    conversationHistory: List[Dict[str, Any]]
