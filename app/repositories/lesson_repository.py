from sqlalchemy.orm import Session
from app.models.lesson import Lesson

class LessonRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, lesson_id: int) -> Lesson:
        return self.session.query(Lesson).filter(Lesson.id == lesson_id).one_or_none()

    def get_all_by_module(self, module_id: int) -> list[Lesson]:
        return self.session.query(Lesson).filter(Lesson.module_id == module_id).order_by(Lesson.order_index).all()

    def get_by_module_and_order(self, module_id: int, order_index: int) -> Lesson:
        return self.session.query(Lesson).filter(Lesson.module_id == module_id, Lesson.order_index == order_index).one_or_none()

    def add(self, lesson: Lesson) -> Lesson:
        self.session.add(lesson)
        self.session.commit()
        self.session.refresh(lesson)
        return lesson

    def update(self, lesson: Lesson) -> Lesson:
        self.session.commit()
        self.session.refresh(lesson)
        return lesson

    def delete(self, lesson: Lesson) -> None:
        self.session.delete(lesson)
        self.session.commit()