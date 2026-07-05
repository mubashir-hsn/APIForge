from fastapi import ( # type: ignore
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session # type: ignore

from app.db.database import get_db

from app.models.user import User
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember # type: ignore

from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse
)

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
)


# Create workspace
@router.post(
    "/",
    response_model=WorkspaceResponse
)
def create_workspace(
    workspace: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Create workspace
    new_workspace = Workspace(
        name=workspace.name,
        description=workspace.description
    )

    db.add(new_workspace)
    db.commit()
    db.refresh(new_workspace)

    # Add creator as owner
    workspace_member = WorkspaceMember(
        user_id=current_user.id,
        workspace_id=new_workspace.id,
        role="owner"
    )

    db.add(workspace_member)
    db.commit()

    return new_workspace


# Get all user workspaces
@router.get(
    "/",
    response_model=list[WorkspaceResponse]
)
def get_user_workspaces(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    memberships = db.query(
        WorkspaceMember
    ).filter(
        WorkspaceMember.user_id == current_user.id
    ).all()

    workspace_ids = [
        membership.workspace_id
        for membership in memberships
    ]

    workspaces = db.query(
        Workspace
    ).filter(
        Workspace.id.in_(workspace_ids)
    ).all()

    return workspaces

# Add Workspace Members
@router.post("/{workspace_id}/members/{user_id}")
def add_workspace_member(
    workspace_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Check workspace exists
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id
    ).first()

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    # Check current user is owner
    owner_membership = db.query(
        WorkspaceMember
    ).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id,
        WorkspaceMember.role == "owner"
    ).first()

    if not owner_membership:
        raise HTTPException(
            status_code=403,
            detail="Only owner can add members"
        )

    # Check user exists
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check already member
    existing_member = db.query(
        WorkspaceMember
    ).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == user_id
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User already member"
        )

    # Add member
    new_member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=user_id,
        role="viewer"
    )

    db.add(new_member)
    db.commit()

    return {
        "message": "Member added successfully"
    }