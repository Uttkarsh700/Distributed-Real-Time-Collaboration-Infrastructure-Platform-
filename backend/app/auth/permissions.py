from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.services.workspace_member_service import user_has_workspace_access, user_has_workspace_role


def require_workspace_access(workspace_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not user_has_workspace_access(db, workspace_id, current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this workspace")
    return True


def require_workspace_role(workspace_id: UUID, allowed_roles: List[str], db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not user_has_workspace_role(db, workspace_id, current_user.id, allowed_roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient workspace role")
    return True
