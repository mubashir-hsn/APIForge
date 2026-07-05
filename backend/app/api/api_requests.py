from fastapi import ( # type: ignore
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session # type: ignore
from app.db.database import get_db

from app.models.api_request import ApiRequest
from app.models.collection import Collection
from app.models.workspace_member import WorkspaceMember
from app.models.user import User
from app.models.request_history import RequestHistory

from app.schemas.api_request import (
    ApiRequestCreate,
    ApiRequestResponse
)
from app.schemas.request_history import (
    RequestExecutionResponse
)
from app.services.request_executor import (
    execute_request
)

from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/requests",
    tags=["API Requests"]
)


@router.post(
    "/",
    response_model=ApiRequestResponse
)
def create_api_request(
    request_data: ApiRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    collection = db.query(Collection).filter(
        Collection.id == request_data.collection_id
    ).first()

    if not collection:
        raise HTTPException(
            status_code=404,
            detail="Collection not found"
        )

    membership = db.query(
        WorkspaceMember
    ).filter(
        WorkspaceMember.workspace_id == collection.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    new_request = ApiRequest(
        name=request_data.name,
        method=request_data.method,
        url=request_data.url,
        headers=request_data.headers,
        query_params=request_data.query_params,
        body=request_data.body,
        description=request_data.description,
        collection_id=request_data.collection_id,
        environment_id=request_data.environment_id
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


@router.get(
    "/collection/{collection_id}",
    response_model=list[ApiRequestResponse]
)
def get_collection_requests(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    collection = db.query(Collection).filter(
        Collection.id == collection_id
    ).first()

    if not collection:
        raise HTTPException(
            status_code=404,
            detail="Collection not found"
        )

    membership = db.query(
        WorkspaceMember
    ).filter(
        WorkspaceMember.workspace_id == collection.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    requests = db.query(ApiRequest).filter(
        ApiRequest.collection_id == collection_id
    ).all()

    return requests

@router.post(
    "/{request_id}/execute",
    response_model=RequestExecutionResponse
)
async def execute_saved_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Find request
    api_request = db.query(ApiRequest).filter(
        ApiRequest.id == request_id
    ).first()

    if not api_request:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    # Find collection
    collection = db.query(Collection).filter(
        Collection.id == api_request.collection_id
    ).first()

    # Check workspace access
    membership = db.query(
        WorkspaceMember
    ).filter(
        WorkspaceMember.workspace_id == collection.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    # Execute request
    result = await execute_request(api_request)

    # Save history
    history = RequestHistory(
        api_request_id=api_request.id,
        status_code=result["status_code"],
        response_time=result["response_time"],
        response_headers=result["response_headers"],
        response_body=result["response_body"],
        error_message=result["error_message"]
    )

    db.add(history)
    db.commit()

    return history

@router.get(
    "/{request_id}/history",
    response_model=list[RequestExecutionResponse]
)
def get_request_history(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    api_request = db.query(ApiRequest).filter(
        ApiRequest.id == request_id
    ).first()

    if not api_request:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    collection = db.query(Collection).filter(
        Collection.id == api_request.collection_id
    ).first()

    membership = db.query(
        WorkspaceMember
    ).filter(
        WorkspaceMember.workspace_id == collection.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    history = db.query(
        RequestHistory
    ).filter(
        RequestHistory.api_request_id == request_id
    ).order_by(
        RequestHistory.created_at.desc()
    ).all()

    return history

@router.delete(
    "/{request_id}"
)
def delete_api_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    api_request = db.query(ApiRequest).filter(ApiRequest.id == request_id).first()
    if not api_request:
        raise HTTPException(status_code=404, detail="Request not found")
        
    collection = db.query(Collection).filter(Collection.id == api_request.collection_id).first()
    membership = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == collection.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
        
    db.delete(api_request)
    db.commit()
    
    return {"message": "Request deleted successfully"}