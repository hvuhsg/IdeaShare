from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, constr, Field


class NewIdea(BaseModel):
    name: constr(max_length=100)
    tldr: constr(max_length=400)


class Idea(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: constr(max_length=100)
    tldr: constr(max_length=400)

    upvote: int = 0
    downvote: int = 0
    score: int = 0

    created_at: datetime = datetime.now()
