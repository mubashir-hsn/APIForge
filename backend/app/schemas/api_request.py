from pydantic import BaseModel
from typing import Optional


class ApiRequestCreate(BaseModel):
    name: str
    method: str
    url: str

    headers: Optional[dict] = None

    query_params: Optional[dict] = None

    body: Optional[dict] = None

    description: Optional[str] = None

    collection_id: int
    environment_id: Optional[int] = None


class ApiRequestResponse(BaseModel):
    id: int
    name: str
    method: str
    url: str

    headers: Optional[dict]

    query_params: Optional[dict]

    body: Optional[dict]

    description: Optional[str]

    collection_id: int
    environment_id: Optional[int]
    model_config = {
        "from_attributes": True
    }