"""Questionnaire d'onboarding (M3) — questions de base + branches par type de deal (M24).

Le questionnaire est court (6-8 questions, RG/US-M3-01), à logique conditionnelle :
les questions spécifiques s'ajoutent selon le type de deal retenu.
"""
from __future__ import annotations

from typing import Any

from app.domain.enums import DealTypeCode

# Seuil de besoin minimal (gating RG-M3-03) — indicatif, paramétrable ultérieurement.
MIN_FINANCING_NEED_XOF = 10_000_000


def _q(qid: str, label: str, qtype: str, options: list[str] | None = None,
       required: bool = True) -> dict[str, Any]:
    return {
        "id": qid, "label": label, "type": qtype,
        "options": options or [], "required": required,
    }


# Questions communes (le type de deal est déjà choisi en amont — M24)
BASE_QUESTIONS: list[dict] = [
    _q("revenue_band", "Quel est votre chiffre d'affaires annuel ?", "single_choice",
       ["< 50 M FCFA", "50 – 200 M FCFA", "200 M – 1 Md FCFA", "> 1 Md FCFA"]),
    _q("stage", "À quel stade se trouve votre entreprise ?", "single_choice",
       ["Idée", "Amorçage", "Early", "Croissance", "Mature"]),
    _q("amount", "Quel montant recherchez-vous ? (FCFA)", "number"),
    _q("use_of_funds", "À quoi serviront principalement les fonds ?", "single_choice",
       ["Investissement", "Besoin en fonds de roulement", "Croissance / expansion",
        "Rachat / transmission", "Autre"]),
    _q("horizon", "Sous quel horizon souhaitez-vous boucler l'opération ?", "single_choice",
       ["< 6 mois", "6 – 12 mois", "> 12 mois"]),
]

# Branches spécifiques par type de deal (RG-M24-03)
DEAL_TYPE_QUESTIONS: dict[DealTypeCode, list[dict]] = {
    DealTypeCode.ouverture_capital: [
        _q("dilution", "Quelle dilution êtes-vous prêt à accepter ?", "single_choice",
           ["< 10 %", "10 – 25 %", "25 – 50 %", "Majoritaire"]),
        _q("cap_table_ready", "Disposez-vous d'une cap table à jour ?", "single_choice",
           ["Oui", "Non", "Partiellement"]),
    ],
    DealTypeCode.dette_bancaire: [
        _q("guarantees", "Pouvez-vous apporter des garanties ?", "single_choice",
           ["Oui", "Non", "Partielles"]),
        _q("bank_history", "Avez-vous un historique bancaire exploitable ?", "single_choice",
           ["Oui", "Non"]),
    ],
    DealTypeCode.dette_privee: [
        _q("collateral", "Disposez-vous de sûretés mobilisables ?", "single_choice",
           ["Oui", "Non", "Partielles"]),
    ],
    DealTypeCode.cession_parts: [
        _q("stake_for_sale", "Quel pourcentage de parts est concerné ?", "single_choice",
           ["< 25 %", "25 – 50 %", "> 50 %"]),
    ],
    DealTypeCode.ma: [
        _q("perimeter", "L'opération porte-t-elle sur la totalité de l'entreprise ?",
           "single_choice", ["Oui", "Non"]),
    ],
    DealTypeCode.hybride: [
        _q("structure_pref", "Quelle structure privilégiez-vous ?", "single_choice",
           ["Plutôt equity", "Plutôt dette", "Équilibré", "Sans préférence"]),
    ],
    DealTypeCode.partenariat: [
        _q("partner_type", "Quel type de partenaire recherchez-vous ?", "single_choice",
           ["Industriel", "Commercial", "Financier"]),
    ],
}


def questions_for(deal_type: DealTypeCode | None) -> list[dict]:
    """Liste ordonnée des questions pour un type de deal donné."""
    extra = DEAL_TYPE_QUESTIONS.get(deal_type, []) if deal_type else []
    return [*BASE_QUESTIONS, *extra]


def evaluate_gating(deal_type: DealTypeCode | None, answers: dict) -> dict:
    """Gating (RG-M3-03) : oriente vers pipeline, nurturing ou orientation cabinet.

    Renvoie {eligible, route, reasons}. Ne bloque jamais brutalement : un dossier hors
    cible est orienté, pas rejeté.
    """
    reasons: list[str] = []
    route = "pipeline"

    if deal_type in (None, DealTypeCode.indecis):
        route = "orientation_cabinet"
        reasons.append("Type d'opération à préciser avec un expert.")

    amount = answers.get("amount")
    try:
        amount_val = float(amount) if amount not in (None, "") else None
    except (TypeError, ValueError):
        amount_val = None
    if amount_val is not None and amount_val < MIN_FINANCING_NEED_XOF:
        route = "nurturing"
        reasons.append("Le besoin exprimé est sous le seuil d'accompagnement actuel.")

    eligible = route == "pipeline"
    return {"eligible": eligible, "route": route, "reasons": reasons}
