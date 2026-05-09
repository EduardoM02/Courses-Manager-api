from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment

class EnrollmentRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_user_id(self, user_id: int) -> list[Enrollment]:
        return self.session.query(Enrollment).filter_by(user_id=user_id).all()

    def get_by_course_id(self, course_id: int) -> list[Enrollment]:
        return self.session.query(Enrollment).filter_by(course_id=course_id).all()

    def get_one(self, user_id: int, course_id: int) -> Enrollment | None:
        return self.session.query(Enrollment).filter_by(user_id=user_id, course_id=course_id).one_or_none()

    def exists(self, user_id: int, course_id: int) -> bool:
        return self.session.query(Enrollment).filter_by(user_id=user_id, course_id=course_id).first() is not None

    def add(self, enrollment: Enrollment) -> Enrollment:
        self.session.add(enrollment)
        self.session.commit()
        self.session.refresh(enrollment)
        return enrollment

    def delete(self, enrollment: Enrollment) -> None:
        self.session.delete(enrollment)
        self.session.commit()