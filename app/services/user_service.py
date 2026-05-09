from app.core.exceptions import NotFoundError, ForbiddenError
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate, UserChangePassword
from app.models.user import User
from app.core.security import get_password_hash, verify_password
from app.core.enums import RoleType


class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user_by_id(self, user_id: int) -> User:
        return self.repo.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> User:
        return self.repo.get_by_username(username)

    def create_user(self, data: UserCreate) -> User:
        if self.repo.exists_by_email(data.email):
            raise NotFoundError("Email already registered")

        if self.repo.exists_by_username(data.username):
            raise NotFoundError("Username already registered")

        hashed_password = get_password_hash(data.password)

        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hashed_password,
            role=RoleType.STUDENT,
            is_active=True
        )

        return self.repo.add(user)

    def update_user(self, user_id: int, data: UserUpdate, current_user: User) -> User:
        user = self.get_user_by_id(user_id)

        if current_user.id != user_id and current_user.role != RoleType.ADMIN:
            raise ForbiddenError("Not allowed")

        update_data = data.model_dump(exclude_unset=True)
        allowed_fields = {"email", "username"}

        for key, value in update_data.items():
            if key in allowed_fields:
                setattr(user, key, value)

        return self.repo.update(user)

    def update_user_role(self, user_id: int, role: RoleType, current_user: User) -> User:
        if current_user.role != RoleType.ADMIN:
            raise ForbiddenError("Only admins can change roles")

        user = self.get_user_by_id(user_id)
        user.role = role

        return self.repo.update(user)

    def change_password(self, current_user: User, data: UserChangePassword) -> None:
        if not verify_password(data.current_password, current_user.hashed_password):
            raise NotFoundError("Incorrect password")

        current_user.hashed_password = get_password_hash(data.new_password)

        self.repo.update(current_user)

    def delete_user(self, user_id: int, current_user: User) -> None:
        user = self.get_user_by_id(user_id)

        if current_user.id != user_id and current_user.role != RoleType.ADMIN:
            raise ForbiddenError("Not allowed")

        self.repo.delete(user)