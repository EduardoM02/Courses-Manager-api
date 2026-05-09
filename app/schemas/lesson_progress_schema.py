from datetime import datetime
from pydantic import BaseModel, ConfigDict

class LessonProgressResponse(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    completed: bool
    completed_at: datetime | None = None


    model_config = ConfigDict(from_attributes=True)
