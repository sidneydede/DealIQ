"""Dépendances FastAPI : session DB, utilisateur courant, contrôle RBAC (M1, moindre privilège)."""
from __future__ import annotations

from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import ACCESS, decode_token
from app.database import get_db
from app.domain.enums import Role
from app.models.user import User

bearer = HTTPBearer(auto_error=False)

_CREDENTIALS_EXC = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Identifiants invalides ou expirés",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    if creds is None:
        raise _CREDENTIALS_EXC
    payload = decode_token(creds.credentials)
    if payload is None or payload.get("type") != ACCESS:
        raise _CREDENTIALS_EXC
    user = db.get(User, payload.get("sub"))
    if user is None or not user.is_active:
        raise _CREDENTIALS_EXC
    return user


def require_roles(*roles: Role) -> Callable[[User], User]:
    """Dépendance paramétrée : n'autorise que les rôles listés."""

    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès refusé : rôle insuffisant",
            )
        return user

    return checker


# Raccourcis usuels
CABINET_ROLES = (Role.analyste, Role.senior, Role.admin)
require_admin = require_roles(Role.admin)
require_cabinet = require_roles(*CABINET_ROLES)
