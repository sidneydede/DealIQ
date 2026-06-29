"""Routes programmes sponsorisés (M23)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_cabinet
from app.database import get_db
from app.models.program import Program
from app.models.user import User
from app.schemas.program import (
    MemberAdd,
    ProgramCreate,
    ProgramMemberOut,
    ProgramOut,
    ProgramReport,
)
from app.services import programs as svc

router = APIRouter()


def _program(program_id: str, db: Session, user: User, *, access: bool = True) -> Program:
    program = db.get(Program, program_id)
    if program is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Programme introuvable")
    if access and not svc.can_access(user, program):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    return program


@router.post("/programs", response_model=ProgramOut, status_code=status.HTTP_201_CREATED)
def create_program(
    payload: ProgramCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> Program:
    return svc.create(db, payload, user)


@router.get("/programs", response_model=list[ProgramOut])
def list_programs(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list[Program]:
    return svc.list_for_user(db, user)


@router.get("/programs/{program_id}", response_model=ProgramOut)
def get_program(
    program_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> Program:
    return _program(program_id, db, user)


@router.post("/programs/{program_id}/members", response_model=ProgramMemberOut, status_code=201)
def add_member(
    program_id: str,
    payload: MemberAdd,
    db: Session = Depends(get_db),
    user: User = Depends(require_cabinet),
) -> dict:
    program = _program(program_id, db, user, access=False)
    svc.add_member(db, program, payload.company_id, user)
    return next(m for m in svc.members(db, program) if m["company_id"] == payload.company_id)


@router.get("/programs/{program_id}/members", response_model=list[ProgramMemberOut])
def list_members(
    program_id: str, db: Session = Depends(get_db), user: User = Depends(require_cabinet)
) -> list[dict]:
    return svc.members(db, _program(program_id, db, user, access=False))


@router.get("/programs/{program_id}/report", response_model=ProgramReport)
def program_report(
    program_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> dict:
    program = _program(program_id, db, user)  # cabinet ou sponsor propriétaire
    return svc.report(db, program)
