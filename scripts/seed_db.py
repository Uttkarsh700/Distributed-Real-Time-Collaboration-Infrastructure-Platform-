from __future__ import annotations

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.audit_log import AuditLog
from app.models.project import Project
from app.models.project_file import ProjectFile
from app.models.user import User
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember


def main() -> None:
    print("Starting CloudCollab demo seed...")
    db = SessionLocal()

    try:
        user = db.execute(select(User).where(User.email == "owner@cloudcollab.dev")).scalar_one_or_none()
        if user is None:
            print("Creating demo user...")
            user = User(
                email="owner@cloudcollab.dev",
                full_name="Demo Owner",
                hashed_password="demo-hashed-password",
            )
            db.add(user)
            db.flush()
        else:
            print("Demo user already exists. Reusing existing record.")

        workspace = db.execute(select(Workspace).where(Workspace.slug == "demo-cloud-workspace")).scalar_one_or_none()
        if workspace is None:
            print("Creating demo workspace...")
            workspace = Workspace(name="Demo Cloud Workspace", slug="demo-cloud-workspace", owner_id=user.id)
            db.add(workspace)
            db.flush()
        else:
            print("Demo workspace already exists. Reusing existing record.")

        membership = db.execute(
            select(WorkspaceMember).where(
                WorkspaceMember.workspace_id == workspace.id,
                WorkspaceMember.user_id == user.id,
            )
        ).scalar_one_or_none()
        if membership is None:
            print("Creating demo workspace membership...")
            db.add(WorkspaceMember(workspace_id=workspace.id, user_id=user.id, role="owner"))

        project = db.execute(select(Project).where(Project.workspace_id == workspace.id, Project.slug == "demo-fastapi-service")).scalar_one_or_none()
        if project is None:
            print("Creating demo project...")
            project = Project(
                workspace_id=workspace.id,
                name="Demo FastAPI Service",
                slug="demo-fastapi-service",
                description="Demo service for CloudCollab seed data.",
                environment="development",
                status="active",
                created_by_id=user.id,
            )
            db.add(project)
            db.flush()
        else:
            print("Demo project already exists. Reusing existing record.")

        file_specs = [
            ("docker-compose.yml", "docker-compose.yml", "yaml"),
            ("README.md", "README.md", "markdown"),
            (".env.example", ".env.example", "env"),
        ]
        for file_path, file_name, language in file_specs:
            existing_file = db.execute(
                select(ProjectFile).where(ProjectFile.project_id == project.id, ProjectFile.file_path == file_path)
            ).scalar_one_or_none()
            if existing_file is None:
                print(f"Creating demo project file: {file_path}")
                db.add(
                    ProjectFile(
                        project_id=project.id,
                        file_path=file_path,
                        file_name=file_name,
                        language=language,
                        content=f"Seeded file placeholder for {file_name}",
                        last_edited_by_id=user.id,
                    )
                )

        audit_log = db.execute(
            select(AuditLog).where(
                AuditLog.project_id == project.id,
                AuditLog.action == "project.created",
            )
        ).scalar_one_or_none()
        if audit_log is None:
            print("Creating demo audit log...")
            db.add(
                AuditLog(
                    workspace_id=workspace.id,
                    project_id=project.id,
                    user_id=user.id,
                    action="project.created",
                    entity_type="project",
                    entity_id=project.id,
                    metadata_json={"seed": True},
                )
            )

        db.commit()
        print("Seed completed successfully.")
    except Exception as exc:
        db.rollback()
        print(f"Seed failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()