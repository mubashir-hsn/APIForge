# pyrefly: ignore [missing-import]
from sqlalchemy import (
    String,
    Integer,
    ForeignKey
)

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.models.base import BaseModel


class Collection(BaseModel):
    __tablename__ = "collections"

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id")
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    workspace = relationship(
        "Workspace",
        back_populates="collections"
    )

    requests = relationship(
        "ApiRequest",
        back_populates="collection",
        cascade="all, delete"
    )