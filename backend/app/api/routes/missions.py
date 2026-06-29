"""Routes espace mission / préparation (M8)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, load_company, require_cabinet
from app.database import get_db
from app.models.company import Company
from app.models.mission import Deliverable, Mission, MissionTask
from app.models.user import User
from app.schemas.company import CompanyOut
from app.schemas.mission import (
    DeliverableCreate,
    DeliverableOut,
    DeliverableUpdate,
    MissionDetailOut,
    MissionReviewOut,
    MissionTaskOut,
    TaskToggle,
)
from app.services import missions as svc

router = APIRouter()


def _mission(mission_id: str, db: Session) -> Mission:
    mission = db.get(Mission, mission_id)
    if mission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission introuvable")
    return mission


@router.post("/companies/{company_id}/mission", response_model=MissionDetailOut)
def create_mission(
    company_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> dict:
    company = load_company(company_id, db, user)
    mission = svc.get_or_create(db, company, user)
    return svc.detail(db, mission, company)


@router.get("/companies/{company_id}/mission", response_model=MissionDetailOut)
def get_mission(
    company_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> dict:
    company = load_company(company_id, db, user)  # propriétaire ou cabinet
    mission = db.query(Mission).filter(Mission.company_id == company.id).first()
    if mission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mission non démarrée"
        )
    return svc.detail(db, mission, company)


@router.patch("/mission-tasks/{task_id}", response_model=MissionTaskOut)
def toggle_task(
    task_id: str,
    payload: TaskToggle,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> MissionTask:
    task = db.get(MissionTask, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche introuvable")
    return svc.toggle_task(db, task, payload.done)


@router.post("/missions/{mission_id}/deliverables", response_model=DeliverableOut, status_code=201)
def add_deliverable(
    mission_id: str,
    payload: DeliverableCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> Deliverable:
    mission = _mission(mission_id, db)
    return svc.add_deliverable(db, mission, payload.kind, payload.note)


@router.patch("/deliverables/{deliverable_id}", response_model=DeliverableOut)
def update_deliverable(
    deliverable_id: str,
    payload: DeliverableUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_cabinet),
) -> Deliverable:
    deliverable = db.get(Deliverable, deliverable_id)
    if deliverable is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livrable introuvable")
    return svc.update_deliverable(db, deliverable, payload)


@router.post("/missions/{mission_id}/review", response_model=MissionReviewOut)
def review_mission(
    mission_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> dict:
    mission = _mission(mission_id, db)
    try:
        return svc.add_review(db, mission, user)
    except svc.GateError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e


@router.post("/missions/{mission_id}/promote", response_model=CompanyOut)
def promote_mission(
    mission_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> Company:
    mission = _mission(mission_id, db)
    company = db.get(Company, mission.company_id)
    try:
        return svc.promote(db, mission, company, user)
    except svc.GateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
