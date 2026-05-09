from __future__ import annotations
from datetime import datetime
from app.core.enums import RoleType
from sqlalchemy import Enum, DateTime, func, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleType] = mapped_column(Enum(RoleType, name="role_type", native_enum=True, values_callable=lambda enum: [e.value for e in enum]), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    courses: Mapped[list["Course"]] = relationship(back_populates="owner")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="user")
    lesson_progress: Mapped[list["LessonProgress"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f'User(id={self.id}, email={self.email}, username={self.username}, role={self.role})'