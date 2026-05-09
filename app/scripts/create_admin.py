from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from app.core.enums import RoleType

def create_admin():
    db = SessionLocal()
    try:
        user = User(
            email="admin@test.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role=RoleType.ADMIN,
            is_active=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()