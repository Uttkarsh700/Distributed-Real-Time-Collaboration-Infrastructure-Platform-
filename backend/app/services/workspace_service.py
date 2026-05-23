from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember
from app.models.user import User
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate
from app.utils.slug import create_slug
from app.services.audit_service import create_audit_log


def _ensure_unique_slug(db: Session, base_slug: str) -> str:
    slug = base_slug
    exists = db.execute(select(Workspace).where(Workspace.slug == slug)).scalar_one_or_none()
    if not exists:
        return slug
    # append short suffix
    slug = f"{base_slug}-{uuid4().hex[:6]}"
    return slug


def create_workspace(db: Session, user: User, data: WorkspaceCreate) -> Workspace:
    base_slug = create_slug(data.name)
    slug = _ensure_unique_slug(db, base_slug)
    workspace = Workspace(name=data.name, slug=slug, description=data.description, owner_id=user.id)
    db.add(workspace)
    db.flush()

    member = WorkspaceMember(workspace_id=workspace.id, user_id=user.id, role="owner")
    db.add(member)
    db.commit()
    db.refresh(workspace)

    try:
        create_audit_log(db, action="workspace.created", entity_type="workspace", user_id=user.id, workspace_id=workspace.id, entity_id=workspace.id)
    except Exception:
        pass

    return workspace


def get_workspace_by_id(db: Session, workspace_id: UUID) -> Optional[Workspace]:
    stmt = select(Workspace).where(Workspace.id == workspace_id)
    return db.execute(stmt).scalar_one_or_none()


def get_user_workspaces(db: Session, user_id: UUID) -> List[Workspace]:
    stmt = select(Workspace).join(WorkspaceMember).where(WorkspaceMember.user_id == user_id)
    return db.execute(stmt).scalars().all()


def update_workspace(db: Session, workspace: Workspace, data: WorkspaceUpdate) -> Workspace:
    changed = False
    if data.name and data.name != workspace.name:
        base_slug = create_slug(data.name)
        workspace.slug = _ensure_unique_slug(db, base_slug)
        workspace.name = data.name
        changed = True
    if data.description is not None and data.description != workspace.description:
        workspace.description = data.description
        changed = True
    if changed:
        db.add(workspace)
        db.commit()
        db.refresh(workspace)
        try:
            create_audit_log(db, action="workspace.updated", entity_type="workspace", workspace_id=workspace.id, entity_id=workspace.id)
        except Exception:
            pass
    return workspace


def delete_workspace(db: Session, workspace: Workspace) -> None:
    try:
        create_audit_log(db, action="workspace.deleted", entity_type="workspace", workspace_id=workspace.id, entity_id=workspace.id)
    except Exception:
        pass
    db.delete(workspace)
    db.commit()
