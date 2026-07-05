from fastapi import FastAPI # type: ignore

from app.db.database import Base, engine

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.users import router as user_router # type: ignore
from app.api.workspaces import router as workspace_router # type: ignore
from app.api.collections import router as collection_router
from app.api.api_requests import router as api_request_router
from app.api.environments import (
    router as environment_router
)

import app.models # type: ignore
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Collaboration Platform",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(workspace_router)
app.include_router(collection_router)
app.include_router(api_request_router)
app.include_router(environment_router)


@app.get("/")
def home():
    return {
        "message": "API Platform Backend Running Successfully"
    }