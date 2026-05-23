from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workspace_member import WorkspaceMember


def get_workspace_member(db: Session, workspace_id: UUID, user_id: UUID) -> Optional[WorkspaceMember]:
    stmt = select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id, WorkspaceMember.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def get_workspace_members(db: Session, workspace_id: UUID) -> List[WorkspaceMember]:
    stmt = select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id)
    return db.execute(stmt).scalars().all()


def user_has_workspace_access(db: Session, workspace_id: UUID, user_id: UUID) -> bool:
    return get_workspace_member(db, workspace_id, user_id) is not None


def user_has_workspace_role(db: Session, workspace_id: UUID, user_id: UUID, allowed_roles: List[str]) -> bool:
    member = get_workspace_member(db, workspace_id, user_id)
    if not member:
        return False
    return member.role in allowed_roles
