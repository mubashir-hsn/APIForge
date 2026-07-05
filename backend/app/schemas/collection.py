from pydantic import BaseModel
from typing import Optional


class CollectionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    workspace_id: int


class CollectionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    workspace_id: int

    model_config = {
        "from_attributes": True
    }