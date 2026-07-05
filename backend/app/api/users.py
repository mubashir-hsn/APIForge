from fastapi import APIRouter, Depends # type: ignore
from sqlalchemy.orm import Session # type: ignore

from app.db.database import get_db

from app.models.user import User

from app.schemas.user import (
    UserResponse,
    UserUpdate
)

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Get current user profile
@router.get(
    "/",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


# Update profile
@router.put(
    "/",
    response_model=UserResponse
)
def update_profile(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Update only provided fields
    if user_data.name is not None:
        current_user.name = user_data.name

    if user_data.bio is not None:
        current_user.bio = user_data.bio

    if user_data.avatar is not None:
        current_user.avatar = user_data.avatar

    db.commit()
    db.refresh(current_user)

    return current_user