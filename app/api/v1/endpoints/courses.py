from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from app.dependencies import get_current_user, get_course_service
from app.models.user import User
from app.schemas.course_schema import CourseResponse, CourseCreate, CourseUpdate
from app.services.course_service import CourseService

router = APIRouter()

@router.post("/courses", response_model=CourseResponse, tags=["courses"])
def create_course(
        data: CourseCreate,
        current_user: Annotated[User, Depends(get_current_user)],
        service: CourseService = Depends(get_course_service)
):
    return service.create_course(data, current_user)


@router.get("/courses/published", response_model=list[CourseResponse], tags=["courses"])
def get_published_courses(
        service: CourseService = Depends(get_course_service)
):
    return service.get_published()


@router.patch("/courses/{course_id}", response_model=CourseResponse, tags=["courses"])
def update_course(
        course_id: int,
        course_data: CourseUpdate,
        current_user: Annotated[User, Depends(get_current_user)],
        service: CourseService = Depends(get_course_service)
):
    return service.update_course(course_id, course_data, current_user)


@router.post("/courses/{course_id}/publish", response_model=CourseResponse, tags=["courses"])
def publish_course(
        course_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        service: CourseService = Depends(get_course_service)
):
    return service.publish_course(course_id, current_user)


@router.post("/courses/{course_id}/unpublish", response_model=CourseResponse, tags=["courses"])
def unpublish_course(
        course_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        service: CourseService = Depends(get_course_service)
):
    return service.unpublish_course(course_id, current_user)


@router.delete("/courses/{course_id}", tags=["courses"])
def delete_course(
        course_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        service: CourseService = Depends(get_course_service)
):
    return service.delete_course(course_id, current_user)
