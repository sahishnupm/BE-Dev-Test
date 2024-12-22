from beanie import Document
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Joke(Document):
    joke_text: str
    source_id: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None

    class Settings:
        name = "jokes"

class JokeCreate(BaseModel):
    joke_text: str
    source_id: Optional[str] = None

class JokeUpdate(BaseModel):
    joke_text: Optional[str] = None 