from sqlalchemy import ( # type: ignore
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship # type: ignore

from app.models.base import BaseModel


class WorkspaceMember(BaseModel):
    __tablename__ = "workspace_members"

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    workspace_id = Column(
        Integer,
        ForeignKey("workspaces.id")
    )

    role = Column(
        String,
        default="viewer"
    )

    workspace = relationship(
        "Workspace",
        back_populates="members"
    )