from pydantic import BaseModel, ConfigDict, Field

class LessonBase(BaseModel):
    title: str
    content: str | None = None
    order_index: int = Field(ge=0)

class LessonCreate(LessonBase):
    pass

class LessonUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    order_index: int | None = Field(None, ge=0)

class LessonResponse(LessonBase):
    id: int
    module_id: int

    model_config = ConfigDict(from_attributes=True)
