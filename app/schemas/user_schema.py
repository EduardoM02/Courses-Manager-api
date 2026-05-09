from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.core.enums import RoleType


class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None

class UserChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)

class UserRoleUpdate(BaseModel):
    role: RoleType

class UserResponse(UserBase):
    id: int
    role: RoleType
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)