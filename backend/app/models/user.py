from sqlalchemy import Column, String, Boolean # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    bio = Column(
        String,
        nullable=True
    )

    avatar = Column(
        String,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    workspace_memberships = relationship(
        "WorkspaceMember",
        backref="user"
    )