from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, create_model
from src.schemas.model import Status


class Inputs(BaseModel):
    text: str


class summarizeResult(BaseModel):
    summary: str 
    status: Status


class categoryResults(BaseModel):
    category: str  # One of: "Technology", "Sports", "Health", "Politics", "Finance", "Business" 
    status: Status


class extract_keywordsResults(BaseModel):
    keywords: List[str] # Array of 5-10 relevant keywords or key phrases
    status: Status


class processResults(BaseModel):
    summary: str  # Concise 3-sentence summary of the article
    category: str  # Category label from the predefined set
    keywords: List[str] # Array of 5-10 relevant keywords or key phrases
    status: Status






