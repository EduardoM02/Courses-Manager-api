from sqlalchemy.orm import Session
from app.models.course import Course

class CourseRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, course_id: int) -> Course | None:
        return self.session.query(Course).filter(Course.id == course_id).one_or_none()

    def get_by_owner(self, owner_id: int) -> list[Course]:
        return self.session.query(Course).filter(Course.owner_id == owner_id).all()

    def get_published(self) -> list[Course]:
        return self.session.query(Course).filter(Course.is_published.is_(True)).all()

    def get_all(self) -> list[Course]:
        return self.session.query(Course).all()

    def add(self, course: Course) -> Course:
        self.session.add(course)
        self.session.commit()
        self.session.refresh(course)
        return course

    def update(self, course: Course) -> Course:
        self.session.commit()
        self.session.refresh(course)
        return course

    def delete(self, course: Course) -> None:
        self.session.delete(course)
        self.session.commit()