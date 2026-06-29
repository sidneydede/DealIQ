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


class Page(BaseModel, Generic[T]):
    """Enveloppe standard d'une liste paginée."""

    items: list[T]
    total: int
    limit: int
    offset: int

    @classmethod
    def build(cls, items: list[T], total: int, page: Pagination) -> Page[T]:
        return cls(items=items, total=total, limit=page.limit, offset=page.offset)
