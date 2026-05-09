from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CourseBase(BaseModel):
    title: str
    description: str | None = None

class CourseCreate(BaseModel):
    title: str
    description: str | None = None

class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_published: bool | None = None

class CourseResponse(CourseBase):
    id: int
    owner_id: int
    is_published: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

