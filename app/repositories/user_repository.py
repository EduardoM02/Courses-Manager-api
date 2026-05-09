from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.query(User).filter(User.id == user_id).one_or_none()

    def get_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter(User.email == email).one_or_none()

    def get_by_username(self, username: str) -> User | None:
        return self.session.query(User).filter(User.username == username).one_or_none()

    def exists_by_email(self, email: str) -> bool:
        return self.session.query(User).filter(User.email == email).first() is not None

    def exists_by_username(self, username: str) -> bool:
        return self.session.query(User).filter(User.username == username).first() is not None

    def add(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user: User) -> User:
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()