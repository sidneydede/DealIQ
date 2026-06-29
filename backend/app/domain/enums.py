"""Énumérations métier DealIQ (CDC v1.2)."""
from __future__ import annotations

from enum import Enum


class Role(str, Enum):
    """Rôles RBAC (CDC M1 / Annexe B)."""

    entrepreneur = "entrepreneur"
    investisseur = "investisseur"
    analyste = "analyste"
    senior = "senior"  # consultant senior
    conformite = "conformite"
    sponsor = "sponsor"  # DFI / banque finançant une cohorte (M23)
    admin = "admin"


class Zone(str, Enum):
    UEMOA = "UEMOA"
    CEMAC = "CEMAC"


class Country(str, Enum):
    """Pays cibles UEMOA (devise XOF) + CEMAC (devise XAF)."""

    # UEMOA
    BJ = "BJ"  # Bénin
    BF = "BF"  # Burkina Faso
    CI = "CI"  # Côte d'Ivoire
    GW = "GW"  # Guinée-Bissau
    ML = "ML"  # Mali
    NE = "NE"  # Niger
    SN = "SN"  # Sénégal
    TG = "TG"  # Togo
    # CEMAC
    CM = "CM"  # Cameroun
    CF = "CF"  # Centrafrique
    CG = "CG"  # Congo
    GA = "GA"  # Gabon
    GQ = "GQ"  # Guinée équatoriale
    TD = "TD"  # Tchad


class Currency(str, Enum):
    XOF = "XOF"  # FCFA BCEAO (UEMOA)
    XAF = "XAF"  # FCFA BEAC (CEMAC)
    EUR = "EUR"
    USD = "USD"


class Instrument(str, Enum):
    """Instruments de financement (mapping depuis le type de deal — M24)."""

    equity = "equity"
    dette = "dette"
    quasi_equity = "quasi_equity"
    subvention = "subvention"
    hybride = "hybride"
    variable = "variable"


class DealTypeCode(str, Enum):
    """Les 7 types de deal du référentiel (M24, CDC §6.24)."""

    ouverture_capital = "ouverture_capital"
    dette_bancaire = "dette_bancaire"
    dette_privee = "dette_privee"
    cession_parts = "cession_parts"
    ma = "ma"  # M&A / cession totale
    hybride = "hybride"
    partenariat = "partenariat"
    indecis = "indecis"  # « Je ne sais pas encore » → orientation cabinet


class CompanyStatus(str, Enum):
    """Statut du dossier entreprise (RG-M2-03)."""

    brouillon = "brouillon"
    qualifie = "qualifie"
    en_preparation = "en_preparation"
    investor_ready = "investor_ready"
    en_deal = "en_deal"
    clos = "clos"
    archive = "archive"


class CompanyStage(str, Enum):
    """Stade de maturité de l'entreprise."""

    idee = "idee"
    amorcage = "amorcage"
    early = "early"
    croissance = "croissance"
    mature = "mature"


class ReadinessCategory(str, Enum):
    """Sortie du Financing Readiness Score (M5) — jamais exposée brute à l'investisseur."""

    investor_ready = "investor_ready"
    a_preparer = "a_preparer"
    plutot_dette_banque = "plutot_dette_banque"
    trop_precoce = "trop_precoce"


class DocumentStatus(str, Enum):
    """Statut de vérification d'une pièce (RG-M4-02)."""

    recu = "recu"
    verifie = "verifie"
    rejete = "rejete"


class DataReliability(str, Enum):
    """Label de fiabilité obligatoire sur toute donnée (RG-IA-01, RG-M2-04)."""

    declare_non_audite = "declare_non_audite"
    verifie = "verifie"
    ia_a_verifier = "ia_a_verifier"
    inference = "inference"


class InvestorType(str, Enum):
    """Typologie financeur (RG-M9-01)."""

    equity_pe_vc = "equity_pe_vc"
    dette_mezzanine = "dette_mezzanine"
    dfi = "dfi"
    family_office = "family_office"
    corporate = "corporate"
    banque = "banque"


class InvestorQualifStatus(str, Enum):
    prospect = "prospect"
    qualifie = "qualifie"
    actif = "actif"
    inactif = "inactif"


class TeaserStatus(str, Enum):
    """Statut d'un teaser (M11). Publié = visible au catalogue investisseur."""

    brouillon = "brouillon"
    publie = "publie"
    retire = "retire"


class InteractionStatus(str, Enum):
    """Statut d'un intérêt investisseur / mise en relation (M12, amorce)."""

    interesse = "interesse"
    ecarte = "ecarte"
    nda_envoye = "nda_envoye"
    nda_signe = "nda_signe"


class QAStatus(str, Enum):
    """Statut d'une question (M14)."""

    ouverte = "ouverte"
    repondue = "repondue"
    cloturee = "cloturee"


class KycSubjectType(str, Enum):
    company = "company"
    investor = "investor"


class KycCheckType(str, Enum):
    """Type de contrôle (M15). RG-M15-01 : API achetée, ici en mode mock."""

    kyb = "kyb"  # identité légale, actionnariat, bénéficiaires effectifs
    aml_screening = "aml_screening"  # sanctions, PEP, adverse media
    manuelle = "manuelle"  # checklist KYC manuelle (M15-03)


class KycStatus(str, Enum):
    en_attente = "en_attente"
    valide = "valide"
    rejete = "rejete"
    hit = "hit"  # correspondance sanctions/PEP → bloque + alerte conformité


class DealStage(str, Enum):
    """Étapes du pipeline de deal execution (M16)."""

    interesse = "interesse"
    nda = "nda"
    data_room = "data_room"
    due_diligence = "due_diligence"
    term_sheet = "term_sheet"
    closing = "closing"
    abandonne = "abandonne"


class ProgramStatus(str, Enum):
    actif = "actif"
    clos = "clos"


class MissionStatus(str, Enum):
    en_cours = "en_cours"
    livre = "livre"


class DeliverableKind(str, Enum):
    """Livrables standardisés (RG-M8-03), déclinés par type de deal."""

    business_plan = "business_plan"
    modele_financier = "modele_financier"
    valorisation = "valorisation"
    teaser = "teaser"
    data_room_init = "data_room_init"


class DeliverableStatus(str, Enum):
    brouillon = "brouillon"
    soumis = "soumis"
    valide = "valide"


class RepresentedParty(str, Enum):
    """Partie dont le Cabinet est mandataire (RG-M17-01, gouvernance des conflits)."""

    entreprise = "entreprise"
    investisseur = "investisseur"
    les_deux = "les_deux"  # double mandat → conflit à divulguer


class MandateType(str, Enum):
    levee = "levee"  # levée de fonds / sourcing capital
    cession = "cession"
    sourcing = "sourcing"
    arrangement_dette = "arrangement_dette"
    conseil = "conseil"
    autre = "autre"


class MandateStatus(str, Enum):
    brouillon = "brouillon"
    actif = "actif"
    clos = "clos"


class FeeType(str, Enum):
    retainer = "retainer"
    success_fee = "success_fee"
    arrangement = "arrangement"


class FeeStatus(str, Enum):
    du = "du"
    facture = "facture"
    paye = "paye"


class DataRoomStatus(str, Enum):
    ouverte = "ouverte"
    fermee = "fermee"


class DataRoomLogAction(str, Enum):
    consultation = "consultation"
    telechargement = "telechargement"


class DealTypeChangeSource(str, Enum):
    """Origine d'un changement de type de deal (historisation M24)."""

    entrepreneur = "entrepreneur"  # sélection / changement par l'entrepreneur (onboarding)
    cabinet = "cabinet"  # requalification par un consultant (RG-M24-04)


class AuditAction(str, Enum):
    """Actions sensibles journalisées (M22)."""

    login = "login"
    login_failed = "login_failed"
    logout = "logout"
    token_refresh = "token_refresh"
    mfa_enabled = "mfa_enabled"
    mfa_disabled = "mfa_disabled"
    user_created = "user_created"
    role_changed = "role_changed"
    account_status_changed = "account_status_changed"
    investor_invited = "investor_invited"
    company_created = "company_created"
    company_status_changed = "company_status_changed"
    deal_type_changed = "deal_type_changed"
    document_uploaded = "document_uploaded"
    document_status_changed = "document_status_changed"
    score_computed = "score_computed"
    teaser_published = "teaser_published"
    interaction_created = "interaction_created"
    interaction_status_changed = "interaction_status_changed"
    kyc_check_created = "kyc_check_created"
    kyc_status_changed = "kyc_status_changed"
    kyc_hit_alert = "kyc_hit_alert"
    dataroom_access_granted = "dataroom_access_granted"
    dataroom_access_revoked = "dataroom_access_revoked"
    dataroom_document_viewed = "dataroom_document_viewed"
    deal_created = "deal_created"
    deal_stage_changed = "deal_stage_changed"
    mandate_created = "mandate_created"
    mandate_status_changed = "mandate_status_changed"
    fee_added = "fee_added"
    mission_reviewed = "mission_reviewed"
    mission_promoted = "mission_promoted"
    program_created = "program_created"
    program_member_added = "program_member_added"
    dd_computed = "dd_computed"
    export = "export"


class TaskStatus(str, Enum):
    """Statut d'une tâche / relance CRM (M20)."""

    a_faire = "a_faire"
    fait = "fait"


class NotificationType(str, Enum):
    """Catégories de notifications in-app (et e-mail mock)."""

    investor_interest = "investor_interest"
    qa_asked = "qa_asked"
    qa_answered = "qa_answered"
    dataroom_access_granted = "dataroom_access_granted"
    kyc_hit = "kyc_hit"
    account_invited = "account_invited"


# --- Tables de correspondance utiles ---

UEMOA_COUNTRIES = {
    Country.BJ, Country.BF, Country.CI, Country.GW,
    Country.ML, Country.NE, Country.SN, Country.TG,
}
CEMAC_COUNTRIES = {
    Country.CM, Country.CF, Country.CG, Country.GA, Country.GQ, Country.TD,
}


def currency_for_country(country: Country) -> Currency:
    """Devise par défaut selon la zone (FCFA BCEAO vs BEAC)."""
    return Currency.XOF if country in UEMOA_COUNTRIES else Currency.XAF


def zone_for_country(country: Country) -> Zone:
    return Zone.UEMOA if country in UEMOA_COUNTRIES else Zone.CEMAC
