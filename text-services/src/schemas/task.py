from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, create_model
from src.schemas.model import Status


# Input/Output models
class TextRequest(BaseModel):
    text: str


class TaskResponse(BaseModel):
    task_id: str
    status: str = "Pending"

class TaskResult(BaseModel):
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
