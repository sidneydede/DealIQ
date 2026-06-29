"""Service tâches & relances CRM (M20, US-M20-02)."""
from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.domain.enums import TaskStatus
from app.models.company import Company
from app.models.task import CrmTask
from app.models.user import User


def _is_overdue(task: CrmTask) -> bool:
    if task.status != TaskStatus.a_faire or task.due_date is None:
        return False
    due = task.due_date if task.due_date.tzinfo else task.due_date.replace(tzinfo=UTC)
    return due < datetime.now(UTC)


def to_dict(db: Session, task: CrmTask) -> dict:
    company = db.get(Company, task.company_id) if task.company_id else None
    assignee = db.get(User, task.assignee_id) if task.assignee_id else None
    return {
        "id": task.id,
        "title": task.title,
        "note": task.note,
        "due_date": task.due_date,
        "status": task.status,
        "company_id": task.company_id,
        "company_name": company.name if company else None,
        "assignee_id": task.assignee_id,
        "assignee_email": assignee.email if assignee else None,
        "overdue": _is_overdue(task),
        "created_at": task.created_at,
    }


def create(db: Session, data, actor: User) -> CrmTask:
    task = CrmTask(
        title=data.title,
        note=data.note,
        due_date=data.due_date,
        company_id=data.company_id,
        assignee_id=data.assignee_id,
        created_by=actor.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(
    db: Session,
    *,
    status: TaskStatus | None = None,
    only_overdue: bool = False,
    assignee_id: str | None = None,
    company_id: str | None = None,
) -> list[CrmTask]:
    q = db.query(CrmTask).order_by(CrmTask.due_date.is_(None), CrmTask.due_date.asc())
    if status:
        q = q.filter(CrmTask.status == status)
    if assignee_id:
        q = q.filter(CrmTask.assignee_id == assignee_id)
    if company_id:
        q = q.filter(CrmTask.company_id == company_id)
    rows = q.all()
    if only_overdue:
        rows = [t for t in rows if _is_overdue(t)]
    return rows


def update(db: Session, task: CrmTask, data) -> CrmTask:
    payload = data.model_dump(exclude_unset=True)
    if "status" in payload:
        new_status = payload["status"]
        task.done_at = datetime.now(UTC) if new_status == TaskStatus.fait else None
    for field, value in payload.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete(db: Session, task: CrmTask) -> None:
    db.delete(task)
    db.commit()
