"""Enrichissement manuel guidé : une question contextuelle par champ vide."""

from app.domain.enums import SocialNetwork
from app.models.deal import Deal

# Question courte par champ (cf. exemples du CDC)
_QUESTIONS = {
    "description": "Quel problème cette startup résout-elle ?",
    "founders": "Qui sont les fondateurs et quel est leur parcours ?",
    "sector": "Dans quel secteur / verticale opère-t-elle ?",
    "website_url": "A-t-elle un site web ? Si oui, quelle URL ?",
    "deal_source": "Comment as-tu connu ce deal (événement, WhatsApp, reco) ?",
    "deck_status": "As-tu reçu un deck ?",
}

_SOCIAL_QUESTION = (
    "As-tu le @Twitter du fondateur ou de la startup ? "
    "C'est souvent la seule donnée publique disponible en CI."
)


def _filled(value: str | None) -> bool:
    return value is not None and str(value).strip() != ""


def guided_questions(deal: Deal) -> list[dict]:
    """Liste de {field, question} pour chaque champ encore vide."""
    questions = [
        {"field": field, "question": text}
        for field, text in _QUESTIONS.items()
        if not _filled(getattr(deal, field))
    ]
    has_twitter = any(
        s.network == SocialNetwork.X_TWITTER.value and _filled(s.value)
        for s in deal.socials
    )
    if not has_twitter:
        questions.append({"field": "x_twitter", "question": _SOCIAL_QUESTION})
    return questions
