"""Provider KYC/KYB/AML — logique d'adaptateur (M15, RG-M15-01).

En MVP/V1 sans clé API, un **mode mock déterministe** simule les réponses des fournisseurs
(Smile ID / Youverify pour le KYB, World-Check / Moody's Grid pour sanctions/PEP). L'interface
est conçue pour brancher la vraie API plus tard sans changer les appelants.
"""
from __future__ import annotations

from app.domain.enums import KycCheckType, KycStatus

# Marqueurs déclencheurs en mode mock (insensibles à la casse).
_SANCTION_MARK = "sanction"
_PEP_MARK = "pep"
_FRAUD_MARK = "fraud"


def run_mock(name: str, check_type: KycCheckType) -> tuple[KycStatus, dict]:
    """Renvoie (statut, résultat structuré) pour un sujet donné.

    Conventions de test : un nom contenant « sanction »/« pep » déclenche un hit AML ;
    un nom contenant « fraud » fait échouer le KYB. Sinon, conforme.
    """
    low = (name or "").lower()
    provider = "mock"

    if check_type == KycCheckType.aml_screening:
        sanctions = _SANCTION_MARK in low
        pep = _PEP_MARK in low
        if sanctions or pep:
            return KycStatus.hit, {
                "provider": provider,
                "sanctions": sanctions,
                "pep": pep,
                "adverse_media": False,
            }
        return KycStatus.valide, {
            "provider": provider, "sanctions": False, "pep": False, "adverse_media": False,
        }

    if check_type == KycCheckType.kyb:
        if _FRAUD_MARK in low:
            return KycStatus.rejete, {"provider": provider, "legal_identity": "non vérifiable"}
        return KycStatus.valide, {
            "provider": provider,
            "legal_identity": "vérifiée",
            "beneficial_owners": "identifiés",
        }

    # Contrôle manuel : créé en attente, validé/rejeté à la main par la conformité.
    return KycStatus.en_attente, {"provider": "manuel"}
