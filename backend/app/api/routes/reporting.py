"""Route reporting & dashboard (M21)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_cabinet
from app.database import get_db
from app.models.user import User
from app.services import reporting as svc

router = APIRouter()


@router.get("/reporting/dashboard")
def dashboard(db: Session = Depends(get_db), _: User = Depends(require_cabinet)) -> dict:
    return svc.dashboard(db)
