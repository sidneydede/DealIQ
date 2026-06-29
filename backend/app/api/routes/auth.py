"""Routes d'authentification (M1). Journalise les actions sensibles (M22)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import (
    MFA,
    REFRESH,
    create_access_token,
    create_mfa_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.database import get_db
from app.domain import mfa
from app.domain.enums import AuditAction, Role
from app.models.user import User
from app.schemas.auth import (
    LoginResponse,
    MfaCode,
    MfaSetupOut,
    MfaVerify,
    RefreshRequest,
    TokenPair,
    UserLogin,
    UserOut,
    UserRegister,
)
from app.services import audit

router = APIRouter()


def _client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


def _token_pair(user: User) -> LoginResponse:
    return LoginResponse(
        access_token=create_access_token(user.id, user.role.value),
        refresh_token=create_refresh_token(user.id, user.role.value),
    )


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


@router.post("/login", response_model=LoginResponse)
def login(payload: UserLogin, request: Request, db: Session = Depends(get_db)) -> LoginResponse:
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
    if user.mfa_enabled:
        # Mot de passe OK mais 2FA requise : on renvoie un défi, pas de jetons.
        return LoginResponse(
            mfa_required=True, mfa_token=create_mfa_token(user.id, user.role.value)
        )
    audit.record(
        db, AuditAction.login, actor=user, object_type="User", object_id=user.id,
        ip_address=_client_ip(request),
    )
    return _token_pair(user)


@router.post("/mfa/verify", response_model=LoginResponse)
def mfa_verify(
    payload: MfaVerify, request: Request, db: Session = Depends(get_db)
) -> LoginResponse:
    data = decode_token(payload.mfa_token)
    if data is None or data.get("type") != MFA:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Défi MFA invalide ou expiré"
        )
    user = db.get(User, data.get("sub"))
    if user is None or not user.is_active or not user.mfa_enabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Défi MFA invalide")
    if not mfa.verify(user.mfa_secret, payload.code):
        audit.record(
            db, AuditAction.login_failed, actor_email=user.email,
            meta={"reason": "mfa"}, ip_address=_client_ip(request),
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Code d'authentification incorrect"
        )
    audit.record(
        db, AuditAction.login, actor=user, object_type="User", object_id=user.id,
        meta={"mfa": True}, ip_address=_client_ip(request),
    )
    return _token_pair(user)


@router.post("/mfa/setup", response_model=MfaSetupOut)
def mfa_setup(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> MfaSetupOut:
    if user.mfa_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="2FA déjà active")
    secret = mfa.generate_secret()
    user.mfa_secret = secret  # en attente d'activation
    db.commit()
    return MfaSetupOut(secret=secret, otpauth_uri=mfa.provisioning_uri(secret, user.email))


@router.post("/mfa/enable", response_model=UserOut)
def mfa_enable(
    payload: MfaCode,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> User:
    if user.mfa_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="2FA déjà active")
    if not user.mfa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Lancez d'abord la configuration"
        )
    if not mfa.verify(user.mfa_secret, payload.code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Code incorrect")
    user.mfa_enabled = True
    db.commit()
    db.refresh(user)
    audit.record(
        db, AuditAction.mfa_enabled, actor=user, object_type="User", object_id=user.id,
        ip_address=_client_ip(request),
    )
    return user


@router.post("/mfa/disable", response_model=UserOut)
def mfa_disable(
    payload: MfaCode,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> User:
    if not user.mfa_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="2FA non active")
    if not mfa.verify(user.mfa_secret, payload.code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Code incorrect")
    user.mfa_enabled = False
    user.mfa_secret = None
    db.commit()
    db.refresh(user)
    audit.record(
        db, AuditAction.mfa_disabled, actor=user, object_type="User", object_id=user.id,
        ip_address=_client_ip(request),
    )
    return user


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
