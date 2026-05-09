from app.core.enums import RoleType
from app.core.exceptions import NotFoundError, ForbiddenError
from app.models import User
from app.models.enrollment import Enrollment
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository

class EnrollmentService:
    def __init__(self, repo: EnrollmentRepository, course_repo: CourseRepository):
        self.repo = repo
        self.course_repo = course_repo

    def get_by_user(self, user_id: int) -> list[Enrollment]:
        return self.repo.get_by_user_id(user_id)

    def get_by_course(self, course_id: int, current_user: User) -> list[Enrollment]:
        course = self.course_repo.get_by_id(course_id)

        if not course:
            raise NotFoundError("Course not found")

        if current_user.role == RoleType.ADMIN:
            return self.repo.get_by_course_id(course_id)

        if current_user.role == RoleType.TEACHER:
            if course.owner_id != current_user.id:
                raise ForbiddenError("Not allowed")

            return self.repo.get_by_course_id(course_id)

        raise ForbiddenError("Not allowed")

    def get_one(self, user_id: int, course_id: int) -> Enrollment:
        enrollment = self.repo.get_one(user_id, course_id)

        if not enrollment:
            raise NotFoundError("Enrollment not found")

        return enrollment

    def create_enrollment(self, current_user: User, course_id: int) -> Enrollment:
        course = self.course_repo.get_by_id(course_id)

        if not course:
            raise NotFoundError("Course not found")

        if not course.is_published:
            raise NotFoundError("Course is not published")

        if self.repo.exists(current_user.id, course_id):
            raise NotFoundError("Already enrolled")

        if current_user.role != RoleType.STUDENT:
            raise ForbiddenError("Only students can enroll")

        if course.owner_id == current_user.id:
            raise ForbiddenError("You cannot enroll in your own course")

        enrollment = Enrollment(
            user_id=current_user.id,
            course_id=course_id,
        )

        return self.repo.add(enrollment)

    def delete_enrollment(self, current_user: User, course_id: int) -> None:
        enrollment = self.get_one(current_user.id, course_id)
        self.repo.delete(enrollment)