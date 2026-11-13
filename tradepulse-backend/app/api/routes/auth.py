from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import (
    register_user,
    DuplicateEmailError
)

from app.schemas.user import UserLogin, TokenResponse
from app.services.auth_service import (
    authenticate_user,
    InvalidCredentialsError
)
from app.core.security import create_access_token

from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        new_user = register_user(
            db=db,
            user_data=user_data
        )

        return new_user

    except DuplicateEmailError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        user = authenticate_user(
            db=db,
            email=str(login_data.email),
            password=login_data.password
        )

        access_token = create_access_token(
            user_id=user.id,
            role=user.role
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user