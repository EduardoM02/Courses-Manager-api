from fastapi import APIRouter
from fastapi.params import Depends
from app.core.enums import RoleType
from app.dependencies import get_lesson_service, require_roles
from app.models import User
from app.schemas.lesson_schema import LessonCreate, LessonResponse, LessonUpdate
from app.services.lesson_service import LessonService

router = APIRouter()

@router.post("/modules/{module_id}/lessons", response_model=LessonResponse, tags=["lessons"])
def create_lesson(
        module_id: int,
        data: LessonCreate,
        current_user: User = Depends(require_roles(RoleType.ADMIN, RoleType.TEACHER)),
        service: LessonService = Depends(get_lesson_service)
):
    return service.create_lesson(module_id, data, current_user)

@router.get("/modules/{module_id}/lessons", response_model=list[LessonResponse], tags=["lessons"])
def get_lessons(
        module_id: int,
        service: LessonService = Depends(get_lesson_service)
):
    return service.get_lessons_by_module(module_id)

@router.get("lessons/{lesson_id}", response_model=LessonResponse, tags=["lessons"])
def get_lesson(
        lesson_id: int,
        service: LessonService = Depends(get_lesson_service)
):
    return service.get_lesson_by_id(lesson_id)

@router.patch("/lessons/{lesson_id}", response_model=LessonResponse, tags=["lessons"])
def update_lesson(
        lesson_id: int,
        data: LessonUpdate,
        current_user: User = Depends(require_roles(RoleType.ADMIN, RoleType.TEACHER)),
        service: LessonService = Depends(get_lesson_service)
):
    return service.update_lesson(lesson_id, data, current_user)

@router.delete("/lessons/{lesson_id}", tags=["lessons"])
def delete_lesson(
        lesson_id: int,
        current_user: User = Depends(require_roles(RoleType.ADMIN, RoleType.TEACHER)),
        service: LessonService = Depends(get_lesson_service)
):
    service.delete_lesson(lesson_id, current_user)
    return {"detail": "Lesson deleted successfully"}