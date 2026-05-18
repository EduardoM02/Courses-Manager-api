from app.core.exceptions import NotFoundError, ForbiddenError, ConflictError
from app.models.user import User
from app.models.lesson import Lesson
from app.repositories.module_repository import ModuleRepository
from app.repositories.lesson_repository import LessonRepository
from app.schemas.lesson_schema import LessonCreate, LessonUpdate

class LessonService:
    def __init__(self, lesson_repo: LessonRepository, module_repo: ModuleRepository):
        self.repo = lesson_repo
        self.module_repo = module_repo

    def get_lesson_by_id(self, lesson_id: int) -> Lesson:
        lesson = self.repo.get_by_id(lesson_id)

        if not lesson:
            raise NotFoundError('Lesson not found')

        return lesson

    def get_lessons_by_module(self, module_id: int) -> list[Lesson]:
        return self.repo.get_all_by_module(module_id)

    def get_by_module_and_order(self, module_id: int, order: int) -> Lesson | None:
        return self.repo.get_by_module_and_order(module_id, order)

    def create_lesson(self, module_id: int, data: LessonCreate, current_user: User) -> Lesson:
        module = self.module_repo.get_by_id(module_id)

        if not module:
            raise NotFoundError("Module not found")

        if module.course.owner_id != current_user.id:
            raise ForbiddenError("Not allowed")

        existing_lesson = self.get_by_module_and_order(
            module.id,
            data.order_index
        )

        if existing_lesson:
            raise ConflictError("Order already exists")

        lesson = Lesson(
            title=data.title,
            content=data.content,
            module_id=module.id,
            order_index=data.order_index
        )

        return self.repo.add(lesson)

    def update_lesson(self, lesson_id: int, data: LessonUpdate, current_user: User) -> Lesson:
        lesson = self.get_lesson_by_id(lesson_id)

        if lesson.module.course.owner_id != current_user.id:
            raise ForbiddenError("Not allowed")

        update_data = data.model_dump(exclude_unset=True)

        if "order_index" in update_data and update_data["order_index"] != lesson.order_index:
            existing_lesson = self.get_by_module_and_order(
                lesson.module_id,
                update_data["order_index"]
            )

            if existing_lesson:
                raise ConflictError("Order already exists")

        for key, value in update_data.items():
            setattr(lesson, key, value)

        return self.repo.update(lesson)

    def delete_lesson(self, lesson_id: int, current_user: User) -> None:
        lesson = self.get_lesson_by_id(lesson_id)

        if lesson.module.course.owner_id != current_user.id:
            raise ForbiddenError("Not allowed")

        self.repo.delete(lesson)