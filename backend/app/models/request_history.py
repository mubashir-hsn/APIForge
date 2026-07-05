from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    JSON,
    Float,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.models.base import BaseModel


class RequestHistory(BaseModel):
    __tablename__ = "request_histories"

    api_request_id: Mapped[int] = mapped_column(
        ForeignKey("api_requests.id")
    )

    status_code: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    response_time: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    response_headers: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    response_body: Mapped[dict | str | None] = mapped_column(
        JSON,
        nullable=True
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    api_request = relationship(
        "ApiRequest",
        back_populates="history"
    )