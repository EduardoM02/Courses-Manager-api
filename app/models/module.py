from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Module(Base):
    __tablename__ = "modules"

    __table_args__ = (
        UniqueConstraint("course_id", "order_index", name="uq_course_module_order"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    course: Mapped["Course"] = relationship(back_populates="modules")
    lesson: Mapped[list["Lesson"]] = relationship(back_populates="module")

    def __repr__(self) -> str:
        return f"<Module id={self.id} title={self.title} course_id={self.course_id}>"