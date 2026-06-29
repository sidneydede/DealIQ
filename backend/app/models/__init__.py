"""Agrège les modèles pour que Base.metadata les connaisse (Alembic, create_all)."""
from app.models.audit import AuditLog
from app.models.base import Base
from app.models.company import Company, Contact, FinancingNeed
from app.models.dealtype_history import DealTypeHistory
from app.models.document import Document
from app.models.investor import InvestmentCriteria, Investor
from app.models.onboarding import OnboardingSession
from app.models.quote import QuoteRequest
from app.models.reference import DealType
from app.models.score import Score
from app.models.teaser import Interaction, Teaser
from app.models.user import User

__all__ = [
    "Base",
    "User",
    "Company",
    "Contact",
    "FinancingNeed",
    "DealType",
    "DealTypeHistory",
    "Investor",
    "InvestmentCriteria",
    "Teaser",
    "Interaction",
    "Score",
    "Document",
    "OnboardingSession",
    "QuoteRequest",
    "AuditLog",
]
