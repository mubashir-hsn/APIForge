from fastapi import ( # type: ignore
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session # type: ignore

from app.db.database import get_db

from app.models.environment import Environment
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember
from app.models.user import User

from app.schemas.environment import (
    EnvironmentCreate,
    EnvironmentResponse
)

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/environments",
    tags=["Environments"]
)


@router.post(
    "/",
    response_model=EnvironmentResponse
)
def create_environment(
    environment: EnvironmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    workspace = db.query(Workspace).filter(
        Workspace.id == environment.workspace_id
    ).first()

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    membership = db.query(
        WorkspaceMember
    ).filter(
        WorkspaceMember.workspace_id == environment.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    new_environment = Environment(
        name=environment.name,
        variables=environment.variables,
        workspace_id=environment.workspace_id,
        created_by=current_user.id
    )

    db.add(new_environment)
    db.commit()
    db.refresh(new_environment)

    return new_environment


@router.get(
    "/workspace/{workspace_id}",
    response_model=list[EnvironmentResponse]
)
def get_workspace_environments(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    membership = db.query(
        WorkspaceMember
    ).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    environments = db.query(
        Environment
    ).filter(
        Environment.workspace_id == workspace_id
    ).all()

    return environments