from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceUpdate
from app.schemas.workspace_member import WorkspaceMemberWithUserResponse
from app.services.workspace_service import create_workspace, delete_workspace, get_user_workspaces, get_workspace_by_id, update_workspace
from app.services.workspace_member_service import get_workspace_members
from app.auth.permissions import require_workspace_access, require_workspace_role

router = APIRouter(prefix="/api/v1/workspaces", tags=["workspaces"])


@router.post("/", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
def create(data: WorkspaceCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> Any:
    workspace = create_workspace(db, current_user, data)
    return workspace


@router.get("/", response_model=List[WorkspaceResponse])
def list_workspaces(db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> Any:
    workspaces = get_user_workspaces(db, current_user.id)
    return workspaces


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(workspace_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> Any:
    workspace = get_workspace_by_id(db, workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    require_workspace_access(workspace_id, db=db, current_user=current_user)
    return workspace


@router.patch("/{workspace_id}", response_model=WorkspaceResponse)
def patch_workspace(workspace_id: UUID, data: WorkspaceUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> Any:
    workspace = get_workspace_by_id(db, workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    # only owner or admin can update
    require_workspace_role(workspace_id, ["owner", "admin"], db=db, current_user=current_user)
    updated = update_workspace(db, workspace, data)
    return updated


@router.delete("/{workspace_id}")
def remove_workspace(workspace_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> Any:
    workspace = get_workspace_by_id(db, workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    # only owner can delete
    require_workspace_role(workspace_id, ["owner"], db=db, current_user=current_user)
    delete_workspace(db, workspace)
    return {"message": "Workspace deleted successfully"}


@router.get("/{workspace_id}/members", response_model=List[WorkspaceMemberWithUserResponse])
def list_members(workspace_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> Any:
    workspace = get_workspace_by_id(db, workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    require_workspace_access(workspace_id, db=db, current_user=current_user)
    members = get_workspace_members(db, workspace_id)
    # map members to include user info
    results: List[WorkspaceMemberWithUserResponse] = []
    for m in members:
        results.append(
            WorkspaceMemberWithUserResponse(
                id=m.id,
                workspace_id=m.workspace_id,
                user_id=m.user_id,
                role=m.role,
                joined_at=m.joined_at,
                user_email=getattr(m.user, "email", None),
                user_full_name=getattr(m.user, "full_name", None),
            )
        )
    return results
