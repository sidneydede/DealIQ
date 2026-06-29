"""Pagination réutilisable : paramètres limit/offset + enveloppe de page générique."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")

DEFAULT_LIMIT = 25
MAX_LIMIT = 200


@dataclass
class Pagination:
    limit: int
    offset: int


def pagination(
    limit: int = Query(default=DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    offset: int = Query(default=0, ge=0),
) -> Pagination:
    """Dépendance FastAPI : `?limit=&offset=` bornés (1..200, défaut 25)."""
    return Pagination(limit=limit, offset=offset)


@dataclass
class SortParams:
    field: str | None
    desc: bool


def sorting(
    sort: str | None = Query(default=None),
    order: str = Query(default="asc"),
) -> SortParams:
    """Dépendance FastAPI : `?sort=<colonne>&order=asc|desc`."""
    return SortParams(field=sort, desc=order.lower() == "desc")


def apply_sql_sort(query, sort: SortParams, allowed: dict, *, default, default_desc: bool = True):
    """Trie une requête SQLAlchemy sur une colonne whitelistée, sinon ordre par défaut."""
    col = allowed.get(sort.field) if sort.field else None
    if col is not None:
        return query.order_by(col.desc() if sort.desc else col.asc())
    return query.order_by(default.desc() if default_desc else default.asc())


class Page(BaseModel, Generic[T]):
    """Enveloppe standard d'une liste paginée."""

    items: list[T]
    total: int
    limit: int
    offset: int

    @classmethod
    def build(cls, items: list[T], total: int, page: Pagination) -> Page[T]:
        return cls(items=items, total=total, limit=page.limit, offset=page.offset)
