from fastapi import Depends, HTTPException # type: ignore
from fastapi.security import ( # type: ignore
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlalchemy.orm import Session # type: ignore

from jose import jwt, JWTError # type: ignore

from app.core.security import (
    SECRET_KEY,
    ALGORITHM
)

from app.db.database import get_db

from app.models.user import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )