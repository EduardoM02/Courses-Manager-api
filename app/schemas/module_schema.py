from pydantic import BaseModel, ConfigDict, Field


class ModuleBase(BaseModel):
    title: str
    order_index: int = Field(ge=0)

class ModuleCreate(ModuleBase):
    pass

class ModuleUpdate(BaseModel):
    title: str | None = None
    order_index: int | None = Field(None, ge=0)

class ModuleResponse(ModuleBase):
    id: int
    course_id: int

    model_config = ConfigDict(from_attributes=True)