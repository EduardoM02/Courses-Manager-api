from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from app.core.enums import RoleType
from app.core.security import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.services.auth_service import AuthService
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from app.services.user_service import UserService
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_repository(db = Depends(get_db)):
    return UserRepository(db)

def get_user_service(repo: UserRepository = Depends(get_user_repository)):
    return UserService(repo)

def get_auth_service(user_service: UserService = Depends(get_user_service)):
    return AuthService(user_service)

def get_course_repository(db = Depends(get_db)):
    return CourseRepository(db)

def get_course_service(repo: CourseRepository = Depends(get_course_repository)):
    return CourseService(repo)

def get_enrollment_repository(db = Depends(get_db)):
    return EnrollmentRepository(db)

def get_enrollment_service(repo: EnrollmentRepository = Depends(get_enrollment_repository), course_repo: CourseRepository = Depends(get_course_repository)):
    return EnrollmentService(repo, course_repo)

def require_roles(*roles: RoleType):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker

def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = user_service.get_user_by_username(username)

    if user is None:
        raise credentials_exception

    return user