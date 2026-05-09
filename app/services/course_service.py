from app.core.enums import RoleType
from app.core.exceptions import NotFoundError, ForbiddenError
from app.models.user import User
from app.repositories.course_repository import CourseRepository
from app.schemas.course_schema import CourseCreate, CourseUpdate
from app.models.course import Course

class CourseService:
    def __init__(self, repo: CourseRepository):
        self.repo = repo

    def get_course_by_id(self, course_id: int) -> Course:
        course = self.repo.get_by_id(course_id)

        if not course:
            raise NotFoundError('Course not found')

        return course

    def get_course_by_owner(self, owner_id: int) -> list[Course]:
        return self.repo.get_by_owner(owner_id)

    def get_published(self) -> list[Course]:
        return self.repo.get_published()

    def get_all(self) -> list[Course]:
        return self.repo.get_all()

    def create_course(self, data: CourseCreate, current_user: User) -> Course:
        if current_user.role not in [RoleType.TEACHER, RoleType.ADMIN]:
            raise ForbiddenError("Not allowed")

        course = Course(
            title=data.title,
            description=data.description,
            owner_id=current_user.id,
            is_published=False
        )

        return self.repo.add(course)

    def update_course(self, course_id: int, data: CourseUpdate, current_user: User) -> Course:
        course = self.get_course_by_id(course_id)

        if course.owner_id != current_user.id:
            raise ForbiddenError('Not allowed')

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(course, key, value)

        return self.repo.update(course)

    def publish_course(self, course_id: int, current_user: User) -> Course:
        course = self.get_course_by_id(course_id)

        if course.owner_id != current_user.id:
            raise ForbiddenError("Not allowed")

        if not course.modules:
            raise NotFoundError("Course must have modules to be published")

        course.is_published = True

        return self.repo.update(course)

    def unpublish_course(self, course_id: int, current_user: User) -> Course:
        course = self.get_course_by_id(course_id)

        if course.owner_id != current_user.id:
            raise ForbiddenError("Not allowed")

        if not course.modules:
            raise NotFoundError("Course must have modules to be published")

        course.is_published = False

        return self.repo.update(course)

    def delete_course(self, course_id: int, current_user: User) -> None:
        course = self.get_course_by_id(course_id)

        if course.owner_id != current_user.id:
            raise ForbiddenError("Not allowed")

        self.repo.delete(course)

