"""Agrège les modèles pour que Base.metadata les connaisse (Alembic, create_all)."""
from app.models.audit import AuditLog
from app.models.base import Base
from app.models.company import Company, Contact, FinancingNeed
from app.models.company_history import CompanyHistory
from app.models.dataroom import (
    DataRoom,
    DataRoomAccess,
    DataRoomDocument,
    DataRoomLog,
)
from app.models.dd import DdAnalysis, SyscohadaImport
from app.models.deal import Deal, DealMilestone, DealStageHistory
from app.models.dealtype_history import DealTypeHistory
from app.models.document import Document
from app.models.esg import EsgProfile
from app.models.investor import InvestmentCriteria, Investor
from app.models.kyc import KycCheck
from app.models.mandate import Fee, Mandate
from app.models.mission import Deliverable, Mission, MissionReview, MissionTask
from app.models.notification import Notification
from app.models.onboarding import OnboardingSession
from app.models.program import Program, ProgramMember
from app.models.qa import QAItem
from app.models.quote import QuoteRequest
from app.models.reference import DealType
from app.models.score import Score
from app.models.scoring_config import ScoringConfig
from app.models.task import CrmTask
from app.models.teaser import Interaction, Teaser
from app.models.user import User

__all__ = [
    "Base",
    "User",
    "Company",
    "Contact",
    "FinancingNeed",
    "CompanyHistory",
    "DealType",
    "DealTypeHistory",
    "Investor",
    "InvestmentCriteria",
    "Teaser",
    "Interaction",
    "QAItem",
    "KycCheck",
    "DataRoom",
    "DataRoomDocument",
    "DataRoomAccess",
    "DataRoomLog",
    "Deal",
    "DealStageHistory",
    "DealMilestone",
    "Mandate",
    "Fee",
    "Mission",
    "MissionTask",
    "Deliverable",
    "MissionReview",
    "EsgProfile",
    "Program",
    "ProgramMember",
    "SyscohadaImport",
    "DdAnalysis",
    "Score",
    "ScoringConfig",
    "CrmTask",
    "Document",
    "OnboardingSession",
    "QuoteRequest",
    "Notification",
    "AuditLog",
]
