"""Lecture SYSCOHADA & retraitements (M18) — logique pure, traçable et testable.

Chaque retraitement renvoie sa valeur, la **règle** appliquée et les **comptes sources**
(RG-M18-02). La profondeur/les axes de la DD s'adaptent au type de deal (RG-M18-03).

Convention d'entrée : une balance = liste de lignes ``{"account": "601000", "label": "...",
"amount": <solde net, magnitude positive>}``. ``amount`` est la magnitude du solde du compte.
"""
from __future__ import annotations

from app.domain.enums import DealTypeCode

# Plan SYSCOHADA révisé — classes 1 à 8 (RG-M18-01, référentiel versionné).
SYSCOHADA_VERSION = "syscohada-revise-2017"
CLASS_LABELS = {
    "1": "Ressources durables (capitaux propres & dettes financières)",
    "2": "Immobilisations",
    "3": "Stocks",
    "4": "Tiers (créances & dettes)",
    "5": "Trésorerie",
    "6": "Charges",
    "7": "Produits",
    "8": "Autres charges et produits HAO",
}


def _sum(lines: list[dict], prefixes: tuple[str, ...]) -> float:
    return round(
        sum(
            float(ln.get("amount") or 0)
            for ln in lines
            if str(ln.get("account", "")).startswith(prefixes)
        ),
        2,
    )


def class_totals(lines: list[dict]) -> dict[str, float]:
    """Total par classe SYSCOHADA (1er chiffre du compte)."""
    totals = {c: 0.0 for c in CLASS_LABELS}
    for ln in lines:
        acc = str(ln.get("account", ""))
        if acc and acc[0] in totals:
            totals[acc[0]] = round(totals[acc[0]] + float(ln.get("amount") or 0), 2)
    return totals


def _item(value: float, rule: str, sources: tuple[str, ...]) -> dict:
    return {"value": round(value, 2), "rule": rule, "sources": list(sources)}


def retraitements(lines: list[dict]) -> dict[str, dict]:
    """Calcule les retraitements clés, chacun avec sa règle et ses comptes sources."""
    produits_exploitation = _sum(lines, ("70", "71", "72", "73", "74", "75"))
    charges_exploitation = _sum(lines, ("60", "61", "62", "63", "64", "65"))
    dotations = _sum(lines, ("681", "68"))

    dettes_financieres = _sum(lines, ("16", "17", "18"))
    tresorerie = _sum(lines, ("52", "53", "57"))
    stocks = _sum(lines, ("3",))
    creances_clients = _sum(lines, ("41",))
    dettes_fournisseurs = _sum(lines, ("40",))

    ebitda = round(produits_exploitation - charges_exploitation, 2)
    resultat_exploitation = round(ebitda - dotations, 2)
    dette_nette = round(dettes_financieres - tresorerie, 2)
    bfr = round(stocks + creances_clients - dettes_fournisseurs, 2)

    return {
        "chiffre_affaires": _item(_sum(lines, ("70",)), "Comptes 70 (ventes)", ("70",)),
        "ebitda": _item(
            ebitda,
            "Produits d'exploitation (70-75) − charges d'exploitation (60-65)",
            ("70-75", "60-65"),
        ),
        "resultat_exploitation": _item(
            resultat_exploitation, "EBITDA − dotations (68)", ("EBITDA", "68")
        ),
        "dette_nette": _item(
            dette_nette,
            "Dettes financières (16-18) − trésorerie (52,53,57)",
            ("16-18", "52", "53", "57"),
        ),
        "bfr": _item(
            bfr,
            "Stocks (3) + créances clients (41) − dettes fournisseurs (40)",
            ("3", "41", "40"),
        ),
    }


def dd_focus(deal_type: DealTypeCode | None) -> list[str]:
    """Axes de due diligence selon le type de deal (RG-M18-03)."""
    if deal_type in (DealTypeCode.dette_bancaire, DealTypeCode.dette_privee):
        return [
            "Capacité de remboursement (EBITDA / service de la dette)",
            "Niveau d'endettement (dette nette / EBITDA)",
            "Sûretés et garanties",
            "Couverture de trésorerie",
        ]
    if deal_type in (
        DealTypeCode.ouverture_capital,
        DealTypeCode.cession_parts,
        DealTypeCode.ma,
    ):
        return [
            "Valorisation (multiples d'EBITDA)",
            "Croissance et marge",
            "Qualité du BFR",
            "Vendor due diligence / synergies",
        ]
    return ["Rentabilité (EBITDA)", "Structure financière", "Qualité du BFR"]


def synthesis(retraite: dict, deal_type: DealTypeCode | None) -> str:
    """Synthèse investisseur courte à partir des retraitements."""
    ebitda = retraite["ebitda"]["value"]
    ca = retraite["chiffre_affaires"]["value"]
    dette_nette = retraite["dette_nette"]["value"]
    bfr = retraite["bfr"]["value"]
    marge = round(ebitda / ca * 100, 1) if ca else 0.0
    levier = round(dette_nette / ebitda, 2) if ebitda else None
    levier_txt = f"{levier}x" if levier is not None else "n/a"
    return (
        f"CA {ca:,.0f} ; EBITDA {ebitda:,.0f} (marge {marge}%) ; dette nette {dette_nette:,.0f} "
        f"(levier {levier_txt}) ; BFR {bfr:,.0f}. Retraitements SYSCOHADA "
        f"{SYSCOHADA_VERSION}, à valider sur pièces."
    )
