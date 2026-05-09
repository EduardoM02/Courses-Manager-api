from app.core.exceptions import NotFoundError
from app.models.user import User
from app.core.security import verify_password, create_access_token, get_password_hash
from app.schemas.user_schema import UserCreate
from app.services.user_service import UserService

DUMMY_HASH = get_password_hash("dummy_password")


class AuthService:

    def __init__(self, service: UserService):
        self.service = service

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.service.get_user_by_username(username)

        if not user:
            verify_password(password, DUMMY_HASH)
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def login_user(self, username: str, password: str):
        user = self.authenticate_user(username, password)

        if not user:
            raise NotFoundError("Invalid credentials")

        access_token = create_access_token(
            data={"sub": user.username}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    def register_user(self, data: UserCreate):
        user = self.service.create_user(data)

        access_token = create_access_token(
            data={"sub": user.username}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }