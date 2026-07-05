from pydantic import BaseModel
from typing import Optional


class EnvironmentCreate(BaseModel):
    name: str
    variables: dict
    workspace_id: int


class EnvironmentResponse(BaseModel):
    id: int
    name: str
    variables: dict
    workspace_id: int

    model_config = {
        "from_attributes": True
    }