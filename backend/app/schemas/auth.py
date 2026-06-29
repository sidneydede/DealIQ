"""Schémas Pydantic pour l'authentification (M1)."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.enums import Role


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = None
    # Auto-inscription = entrepreneur. Les autres rôles sont attribués par un admin.


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class LoginResponse(BaseModel):
    """Réponse de /auth/login : jetons, ou défi MFA si la 2FA est active."""

    mfa_required: bool = False
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "bearer"
    mfa_token: str | None = None  # présent uniquement si mfa_required


class MfaCode(BaseModel):
    code: str = Field(min_length=6, max_length=10)


class MfaVerify(BaseModel):
    mfa_token: str
    code: str = Field(min_length=6, max_length=10)


class MfaSetupOut(BaseModel):
    secret: str
    otpauth_uri: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    full_name: str | None
    role: Role
    is_active: bool
    mfa_enabled: bool = False


class RoleUpdate(BaseModel):
    role: Role


class UserCreate(BaseModel):
    """Création d'un compte par un admin (M1). Mot de passe optionnel : généré sinon."""

    email: EmailStr
    full_name: str | None = None
    role: Role = Role.entrepreneur
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserCreatedOut(UserOut):
    # Mot de passe temporaire renvoyé UNE SEULE FOIS quand il a été généré côté serveur.
    temporary_password: str | None = None


class ActiveUpdate(BaseModel):
    is_active: bool
