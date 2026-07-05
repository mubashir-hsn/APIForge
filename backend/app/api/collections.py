from fastapi import ( # type: ignore
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session # type: ignore
from app.db.database import get_db

from app.models.collection import Collection
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember # type: ignore
from app.models.user import User

from app.schemas.collection import (
    CollectionCreate,
    CollectionResponse
)

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/collections",
    tags=["Collections"]
)


@router.post(
    "/",
    response_model=CollectionResponse
)
def create_collection(
    collection: CollectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Check workspace exists
    workspace = db.query(Workspace).filter(
        Workspace.id == collection.workspace_id
    ).first()

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    # Check user is member
    membership = db.query(
        WorkspaceMember
    ).filter(
        WorkspaceMember.workspace_id == collection.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You are not workspace member"
        )

    new_collection = Collection(
        name=collection.name,
        description=collection.description,
        workspace_id=collection.workspace_id,
        created_by=current_user.id
    )

    db.add(new_collection)
    db.commit()
    db.refresh(new_collection)

    return new_collection


@router.get(
    "/workspace/{workspace_id}",
    response_model=list[CollectionResponse]
)
def get_workspace_collections(
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

    collections = db.query(Collection).filter(
        Collection.workspace_id == workspace_id
    ).all()

    return collections