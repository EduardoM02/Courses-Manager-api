from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Lesson(Base):
    __tablename__ = "lessons"

    __table_args__ = (
        UniqueConstraint("module_id", "order_index", name="uq_module_lesson_order"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    module: Mapped["Module"] = relationship(back_populates="lesson")
    lesson_progress: Mapped[list["LessonProgress"]] = relationship(back_populates="lesson")

    def __repr__(self) -> str:
        return f"<Lesson id={self.id} title={self.title} module_id={self.module_id}>"