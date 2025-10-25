from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Hashtag(BaseModel):
    id: int
    name: str

class PostCreate(BaseModel):
    content: str
    image: Optional[str] =None
    location: Optional[str] = None

class Post(PostCreate):
    id: int
    author_id: int
    likes_count: int
    created_dt: datetime

    class Config:
        orm_mode = True