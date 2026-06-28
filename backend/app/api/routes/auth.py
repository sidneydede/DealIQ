"""Routes d'authentification (M1). Journalise les actions sensibles (M22)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import (
    REFRESH,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.database import get_db
from app.domain.enums import AuditAction, Role
from app.models.user import User
from app.schemas.auth import RefreshRequest, TokenPair, UserLogin, UserOut, UserRegister
from app.services import audit

router = APIRouter()


def _client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, request: Request, db: Session = Depends(get_db)) -> User:
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email déjà utilisé")
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=Role.entrepreneur,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    audit.record(
        db, AuditAction.user_created, actor=user, object_type="User", object_id=user.id,
        ip_address=_client_ip(request),
    )
    return user


@router.post("/login", response_model=TokenPair)
def login(payload: UserLogin, request: Request, db: Session = Depends(get_db)) -> TokenPair:
    user = db.query(User).filter(User.email == payload.email).first()
    if user is None or not verify_password(payload.password, user.hashed_password):
        audit.record(
            db, AuditAction.login_failed, actor_email=payload.email,
            ip_address=_client_ip(request),
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe incorrect"
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Compte désactivé")
    audit.record(
        db, AuditAction.login, actor=user, object_type="User", object_id=user.id,
        ip_address=_client_ip(request),
    )
    return TokenPair(
        access_token=create_access_token(user.id, user.role.value),
        refresh_token=create_refresh_token(user.id, user.role.value),
    )


@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest, request: Request, db: Session = Depends(get_db)) -> TokenPair:
    data = decode_token(payload.refresh_token)
    if data is None or data.get("type") != REFRESH:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token invalide"
        )
    user = db.get(User, data.get("sub"))
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur invalide")
    audit.record(
        db, AuditAction.token_refresh, actor=user, object_type="User", object_id=user.id,
        ip_address=_client_ip(request),
    )
    return TokenPair(
        access_token=create_access_token(user.id, user.role.value),
        refresh_token=create_refresh_token(user.id, user.role.value),
    )


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> User:
    return user
