# pyrefly: ignore [missing-import]
from sqlalchemy import String
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.models.base import BaseModel


class Workspace(BaseModel):
    __tablename__ = "workspaces"

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    members = relationship(
        "WorkspaceMember",
        back_populates="workspace",
        cascade="all, delete"
    )

    collections = relationship(
        "Collection",
        back_populates="workspace",
        cascade="all, delete"
    )