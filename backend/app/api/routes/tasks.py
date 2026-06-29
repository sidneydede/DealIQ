"""Routes tâches & relances CRM (M20, US-M20-02) — outil cabinet."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_cabinet
from app.database import get_db
from app.domain.enums import TaskStatus
from app.models.task import CrmTask
from app.models.user import User
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services import tasks as svc

router = APIRouter()


@router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> dict:
    return svc.to_dict(db, svc.create(db, payload, user))


@router.get("/tasks", response_model=list[TaskOut])
def list_tasks(
    status_filter: TaskStatus | None = None,
    overdue: bool = False,
    company_id: str | None = None,
    mine: bool = False,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> list[dict]:
    rows = svc.list_tasks(
        db, status=status_filter, only_overdue=overdue, company_id=company_id,
        assignee_id=user.id if mine else None,
    )
    return [svc.to_dict(db, t) for t in rows]


def _load(task_id: str, db: Session) -> CrmTask:
    task = db.get(CrmTask, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche introuvable")
    return task


@router.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(
    task_id: str,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> dict:
    return svc.to_dict(db, svc.update(db, _load(task_id, db), payload))


@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: str, db: Session = Depends(get_db), _: User = Depends(require_cabinet)
) -> dict:
    svc.delete(db, _load(task_id, db))
    return {"deleted": True}
