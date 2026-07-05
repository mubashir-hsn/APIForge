from pydantic import BaseModel
from typing import Optional


class RequestExecutionResponse(BaseModel):
    status_code: Optional[int]

    response_time: Optional[float]

    response_headers: Optional[dict]

    response_body: Optional[dict | str]

    error_message: Optional[str]

    model_config = {
        "from_attributes": True
    }