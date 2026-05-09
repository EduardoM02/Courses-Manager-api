from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.schemas.user_schema import UserCreate
from app.services.auth_service import AuthService
from app.dependencies import get_auth_service

router = APIRouter()

@router.post("/auth/login", tags=["auth"])
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service)
):

    try:
        return auth_service.login_user(
            form_data.username,
            form_data.password
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.post("/auth/register", tags=["auth"])
def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return auth_service.register_user(user_data)
    except Exception as e:
        raise