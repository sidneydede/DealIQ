"""Synchronise le schéma d'une base SQLite de dev avec les modèles SQLAlchemy.

En dev/tests on utilise SQLite + ``create_all`` (Postgres/Alembic n'est pas joignable
localement). ``create_all`` crée les tables manquantes mais n'ajoute JAMAIS les colonnes
ajoutées à une table existante. Quand un modèle gagne une colonne (ex. ``users.mfa_secret``),
la base de dev existante devient obsolète et chaque requête qui lit cette table tombe en
erreur ``no such column``.

Ce script, idempotent, comble l'écart sans détruire les données :
  1. ``create_all`` -> crée les tables manquantes ;
  2. ``ALTER TABLE ADD COLUMN`` -> ajoute les colonnes manquantes des tables existantes.

Usage : ``./.venv/Scripts/python.exe scripts/sync_sqlite_dev.py [chemin_db]`` (défaut dev.db)
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

from sqlalchemy import create_engine

import app.models  # noqa: F401 — importe tous les modèles pour peupler metadata
from app.models.base import Base


def _sqlite_type(col) -> str:
    """Type SQLite tolérant pour une colonne SQLAlchemy."""
    name = col.type.__class__.__name__.upper()
    if "BOOL" in name:
        return "BOOLEAN"
    if "DATETIME" in name or "DATE" in name:
        return "DATETIME"
    if "INT" in name:
        return "INTEGER"
    return "TEXT"


def sync(db_path: str = "dev.db") -> None:
    if not Path(db_path).exists():
        print(f"Base introuvable: {db_path} — rien à synchroniser (create_all la créera).")
        return

    # 1) Tables manquantes via create_all (ne touche pas aux tables existantes).
    #    Moteur SQLite dédié au fichier ciblé, indépendant de la config (Postgres).
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    engine.dispose()

    # 2) Colonnes manquantes via ALTER TABLE.
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    existing = {r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    added = 0
    for tname, table in Base.metadata.tables.items():
        if tname not in existing:
            continue
        cols_db = {r[1] for r in cur.execute(f"PRAGMA table_info('{tname}')")}
        for col in table.columns:
            if col.name in cols_db:
                continue
            sqltype = _sqlite_type(col)
            clause = f'ALTER TABLE "{tname}" ADD COLUMN "{col.name}" {sqltype}'
            if not col.nullable:
                default = "0" if sqltype in ("BOOLEAN", "INTEGER") else "''"
                clause += f" NOT NULL DEFAULT {default}"
            cur.execute(clause)
            added += 1
            print(f"+ {tname}.{col.name} ({sqltype})")
    con.commit()
    con.close()
    print(f"OK — {added} colonne(s) ajoutée(s). Tables manquantes créées via create_all.")


if __name__ == "__main__":
    sync(sys.argv[1] if len(sys.argv) > 1 else "dev.db")
