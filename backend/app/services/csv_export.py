"""Export CSV réutilisable (module standard `csv`, aucune dépendance).

BOM UTF-8 en tête pour qu'Excel ouvre correctement les accents.
"""
from __future__ import annotations

import csv
import io
from enum import Enum

# Une colonne = (clé dans le dict, en-tête lisible).
Column = tuple[str, str]


def _cell(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, Enum):
        return str(value.value)
    if isinstance(value, bool):
        return "oui" if value else "non"
    return str(value)


def to_csv(rows: list[dict], columns: list[Column]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, delimiter=";", lineterminator="\r\n")
    writer.writerow([header for _, header in columns])
    for row in rows:
        writer.writerow([_cell(row.get(key)) for key, _ in columns])
    # ﻿ = BOM UTF-8 (compatibilité Excel) ; séparateur ';' = locale FR.
    return "﻿" + buf.getvalue()
