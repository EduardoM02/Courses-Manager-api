from typing import Annotated
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from app.dependencies import get_current_user, get_enrollment_service
from app.models import User
from app.schemas.enrollment_schema import EnrollmentResponse
from app.services.enrollment_service import EnrollmentService

router = APIRouter()

@router.post("/courses/{course_id}/enroll", response_model=EnrollmentResponse, tags=["enrollment"])
def create_enrollment(
    course_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: EnrollmentService = Depends(get_enrollment_service),
):
    return service.create_enrollment(current_user, course_id)


@router.get("/me/enrollments", response_model=list[EnrollmentResponse], tags=["enrollment"])
def get_my_enrollments(
    current_user: Annotated[User, Depends(get_current_user)],
    service: EnrollmentService = Depends(get_enrollment_service),
):
    return service.get_by_user(current_user.id)


@router.get("/courses/{course_id}/enrollment", response_model=EnrollmentResponse, tags=["enrollment"])
def get_my_enrollment_in_course(
    course_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: EnrollmentService = Depends(get_enrollment_service),
):
    return service.get_one(current_user.id, course_id)


@router.get("/courses/{course_id}/enrollments", response_model=list[EnrollmentResponse], tags=["enrollment"])
def get_course_enrollments(
    course_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: EnrollmentService = Depends(get_enrollment_service),
):
    return service.get_by_course(course_id, current_user)


@router.delete("/courses/{course_id}/enroll", tags=["enrollment"])
def delete_enrollment(
    course_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: EnrollmentService = Depends(get_enrollment_service),
):
    service.delete_enrollment(current_user, course_id)
    return {"detail": "Enrollment deleted successfully"}
