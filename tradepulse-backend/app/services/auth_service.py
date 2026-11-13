from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.constants.roles import UserRole
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password


class DuplicateEmailError(Exception):
    pass


def register_user(
    db: Session,
    user_data: UserCreate
) -> User:

    email = str(user_data.email).lower()

    # Check whether email already exists
    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise DuplicateEmailError(
            "Email is already registered"
        )

    # Hash the password
    hashed_password = hash_password(
        user_data.password
    )

    # Create SQLAlchemy ORM object
    new_user = User(
        full_name=user_data.full_name.strip(),
        email=email,
        password_hash=hashed_password,
        role=UserRole.USER.value
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise DuplicateEmailError(
            "Email is already registered"
        )

    return new_user

class InvalidCredentialsError(Exception):
    pass


def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> User:

    normalized_email = email.lower()

    user = db.scalar(
        select(User).where(
            User.email == normalized_email
        )
    )

    if user is None:
        raise InvalidCredentialsError()

    password_valid = verify_password(
        password,
        user.password_hash
    )

    if not password_valid:
        raise InvalidCredentialsError()

    return user