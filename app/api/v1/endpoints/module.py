from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from app.dependencies import get_current_user, get_module_service
from app.models import Course
from app.models.user import User
from app.schemas.module_schema import ModuleResponse, ModuleCreate, ModuleUpdate
from app.services.module_service import ModuleService

router = APIRouter()

@router.post( "/courses/{course_id}/modules", response_model=ModuleResponse, tags=["modules"])
def create_module(
    course_id: int,
    data: ModuleCreate,
    current_user: User = Depends(get_current_user),
    service: ModuleService = Depends(get_module_service)
):
    return service.create_module(
        course_id,
        data,
        current_user
    )

@router.get("/courses/{course_id}/modules", response_model=list[ModuleResponse], tags=["modules"])
def get_modules(
    course_id: int,
    service: ModuleService = Depends(get_module_service)
):
    return service.get_modules_by_course(course_id)

@router.patch("/modules/{module_id}", response_model=ModuleResponse, tags=["modules"])
def update_module(
    module_id: int,
    data: ModuleUpdate,
    current_user: User = Depends(get_current_user),
    service: ModuleService = Depends(get_module_service)
):
    return service.update_module(module_id, data, current_user)

@router.delete("/modules/{module_id}", tags=["modules"])
def delete_module(
    module_id: int,
    current_user: User = Depends(get_current_user),
    service: ModuleService = Depends(get_module_service)
):
    service.delete_module(module_id, current_user)
    return {"detail": "Module deleted successfully"}