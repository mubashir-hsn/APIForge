from sqlalchemy import ( # type: ignore
    String,
    Integer,
    ForeignKey,
    JSON,
    Text
)

from sqlalchemy.orm import ( # type: ignore
    Mapped,
    mapped_column,
    relationship
)

from app.models.base import BaseModel


class ApiRequest(BaseModel):
    __tablename__ = "api_requests"

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    method: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    headers: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    query_params: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    body: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    collection_id: Mapped[int] = mapped_column(
        ForeignKey("collections.id")
    )

    collection = relationship(
        "Collection",
        back_populates="requests"
    )

    history = relationship(
       "RequestHistory",
       back_populates="api_request",
       cascade="all, delete"
    )

    environment_id: Mapped[int | None] = mapped_column(
      ForeignKey("environments.id"),
      nullable=True
    )

    environment = relationship(
       "Environment"
    )