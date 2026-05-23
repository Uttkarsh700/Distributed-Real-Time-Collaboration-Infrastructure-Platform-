from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    action: str,
    entity_type: str,
    user_id: Optional[UUID] = None,
    workspace_id: Optional[UUID] = None,
    project_id: Optional[UUID] = None,
    entity_id: Optional[UUID] = None,
    metadata: Optional[dict] = None,
):
    log = AuditLog(
        workspace_id=workspace_id,
        project_id=project_id,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata_json=metadata,
    )
    db.add(log)
    db.flush()
    return log
