from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    __table_args__ = (
        UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson_progress"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    lesson_id: Mapped[int] = mapped_column(ForeignKey('lessons.id'), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="lesson_progress")
    lesson: Mapped["Lesson"] = relationship(back_populates="lesson_progress")

    def __repr__(self) -> str:
        return f"<LessonProgress id={self.id}, user_id={self.user_id}, lesson_id={self.lesson_id}, completed={self.completed}>"