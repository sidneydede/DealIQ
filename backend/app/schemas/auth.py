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


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    full_name: str | None
    role: Role
    is_active: bool


class RoleUpdate(BaseModel):
    role: Role
