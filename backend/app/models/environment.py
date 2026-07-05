from sqlalchemy import (
    String,
    ForeignKey,
    JSON
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.models.base import BaseModel


class Environment(BaseModel):
    __tablename__ = "environments"

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    variables: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id")
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    workspace = relationship(
        "Workspace",
        backref="environments"
    )