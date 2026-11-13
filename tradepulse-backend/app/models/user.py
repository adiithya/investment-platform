
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Integer,
    String,
    func,
)

from app.database.base import Base
from app.constants.roles import UserRole


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            f"role IN ('{UserRole.ADMIN.value}', '{UserRole.USER.value}')",
            name="check_user_role",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    role = Column(
        String(20),
        nullable=False,
        default=UserRole.USER.value,
        server_default=UserRole.USER.value,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )