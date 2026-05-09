from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.schemas.user_schema import UserResponse, UserUpdate, UserChangePassword, UserRoleUpdate
from app.dependencies import get_current_user, get_user_service
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter()


@router.get("/users/me", response_model=UserResponse, tags=["users"])
def read_user_me(
        current_user: Annotated[User, Depends(get_current_user)],
        service: UserService = Depends(get_user_service)
):
    return service.get_user_by_id(current_user.id)


@router.patch("/users/me", response_model=UserResponse, tags=["users"])
def update_user(
        user_data: UserUpdate,
        current_user: Annotated[User, Depends(get_current_user)],
        service: UserService = Depends(get_user_service)
):
    return service.update_user(current_user.id, user_data, current_user)



@router.put("/users/me/password", tags=["users"])
def update_user_password(
    data: UserChangePassword,
    current_user: Annotated[User, Depends(get_current_user)],
    service: UserService = Depends(get_user_service)
):
    service.change_password(current_user, data)
    return {"detail": "Password updated successfully"}


@router.patch("/users/{user_id}/role", response_model=UserResponse, tags=["users"])
def update_user_role(
    user_id: int,
    data: UserRoleUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: UserService = Depends(get_user_service)
):
    return service.update_user_role(user_id, data.role, current_user)

@router.delete("/users/{user_id}", tags=["users"])
def delete_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: UserService = Depends(get_user_service)
):
    service.delete_user(user_id, current_user)
    return {"detail": "User deleted"}
