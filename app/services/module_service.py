from app.core.exceptions import NotFoundError, ForbiddenError, ConflictError
from app.models.user import User
from app.models.module import Module
from app.repositories.course_repository import CourseRepository
from app.repositories.module_repository import ModuleRepository
from app.schemas.module_schema import ModuleCreate, ModuleUpdate

class ModuleService:
    def __init__(self, module_repo: ModuleRepository, course_repo: CourseRepository):
        self.repo = module_repo
        self.course_repo = course_repo

    def get_module_by_id(self, module_id: int) -> Module:
        module = self.repo.get_by_id(module_id)

        if not module:
            raise NotFoundError('Module not found')

        return module

    def get_modules_by_course(self, course_id: int) -> list[Module]:
        return self.repo.get_all_by_course(course_id)

    def get_by_course_and_order(self, course_id: int, order: int) -> Module | None:
        return self.repo.get_by_course_and_order(course_id, order)

    def create_module(self, course_id: int, data: ModuleCreate, current_user: User) -> Module:
        course = self.course_repo.get_by_id(course_id)

        if not course:
            raise NotFoundError("Course not found")

        if course.owner_id != current_user.id:
            raise ForbiddenError("Not allowed")

        existing_module = self.get_by_course_and_order(
            course.id,
            data.order_index
        )

        if existing_module:
            raise ConflictError("Order already exists")

        module = Module(
            title=data.title,
            course_id=course.id,
            order_index=data.order_index
        )

        return self.repo.add(module)

    def update_module(self, module_id: int, data: ModuleUpdate, current_user: User) -> Module:
        module = self.get_module_by_id(module_id)

        if module.course.owner_id != current_user.id:
            raise ForbiddenError("Not allowed")

        update_data = data.model_dump(exclude_unset=True)

        if "order_index" in update_data and update_data["order_index"] != module.order_index:
            existing_module = self.get_by_course_and_order(
                module.course_id,
                update_data["order_index"]
            )

            if existing_module:
                raise ConflictError("Order already exists")

        for key, value in update_data.items():
            setattr(module, key, value)

        return self.repo.update(module)

    def delete_module(self, module_id: int, current_user: User) -> None:
        module = self.get_module_by_id(module_id)

        if module.course.owner_id != current_user.id:
            raise ForbiddenError("Not allowed")

        self.repo.delete(module)