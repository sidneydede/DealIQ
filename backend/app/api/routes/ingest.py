from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.domain.enrichment import (
    DECK_NO_TEXT_MESSAGE,
    LABEL_DECK,
    LABEL_PASTED_TEXT,
    NO_FIELDS_EXTRACTED_MESSAGE,
    TEXT_MIN_LENGTH,
    TEXT_TOO_SHORT_MESSAGE,
    RunStatus,
    SourceCode,
)
from app.models.deal import Deal
from app.models.enrichment import EnrichmentProposal, EnrichmentRun
from app.models.user import User
from app.schemas.enrichment import (
    EnrichResult,
    GuidedQuestion,
    ProposalOut,
    RunOut,
    TextExtractIn,
)
from app.services.enrichment.ingest import ingest_extracted
from app.services.guided import guided_questions
from app.services.pdf import extract_text_from_pdf
from app.services.text_extraction import extract_fields

router = APIRouter(tags=["ingest"])


def _deal_or_404(db: Session, deal_id: int) -> Deal:
    deal = db.get(Deal, deal_id)
    if deal is None:
        raise HTTPException(status_code=404, detail="Fiche introuvable.")
    return deal


def _result(db: Session, run: EnrichmentRun, fallback_message: str) -> EnrichResult:
    proposals = list(
        db.execute(
            select(EnrichmentProposal)
            .where(EnrichmentProposal.run_id == run.id)
            .order_by(EnrichmentProposal.id)
        )
        .scalars()
        .all()
    )
    message = fallback_message if run.status == RunStatus.NO_SOURCE else None
    return EnrichResult(
        run=RunOut.model_validate(run),
        proposals=[ProposalOut.model_validate(p) for p in proposals],
        message=message,
    )


@router.post("/deals/{deal_id}/extract-text", response_model=EnrichResult)
def extract_text(
    deal_id: int,
    payload: TextExtractIn,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> EnrichResult:
    deal = _deal_or_404(db, deal_id)
    if len(payload.text.strip()) < TEXT_MIN_LENGTH:
        raise HTTPException(status_code=400, detail=TEXT_TOO_SHORT_MESSAGE)
    extracted = extract_fields(payload.text)
    run = ingest_extracted(
        db, deal, source=SourceCode.PASTED_TEXT, label=LABEL_PASTED_TEXT, extracted=extracted
    )
    return _result(db, run, NO_FIELDS_EXTRACTED_MESSAGE)


@router.post("/deals/{deal_id}/deck", response_model=EnrichResult)
async def upload_deck(
    deal_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> EnrichResult:
    deal = _deal_or_404(db, deal_id)
    data = await file.read()
    try:
        text = extract_text_from_pdf(data)
    except Exception:
        raise HTTPException(status_code=400, detail="Fichier PDF invalide ou illisible.") from None

    extracted = extract_fields(text) if text else []
    run = ingest_extracted(
        db, deal, source=SourceCode.DECK_PDF, label=LABEL_DECK, extracted=extracted
    )
    fallback = DECK_NO_TEXT_MESSAGE if not text else NO_FIELDS_EXTRACTED_MESSAGE
    return _result(db, run, fallback)


@router.get("/deals/{deal_id}/guided-questions", response_model=list[GuidedQuestion])
def get_guided_questions(
    deal_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[dict]:
    deal = _deal_or_404(db, deal_id)
    return guided_questions(deal)
