"""Tests unitaires du barème completeness_score et du Mode Données Zéro."""

from app.models.deal import Deal, SocialProfile
from app.services.completeness import compute_completeness, is_data_zero_mode


def test_required_only_is_50():
    d = Deal(name="Acme", sector="Fintech", stage="mvp", country="CI")
    assert compute_completeness(d) == 50


def test_empty_is_zero():
    d = Deal(name="", sector="", stage="", country="")
    assert compute_completeness(d) == 0


def test_optional_fields_points():
    d = Deal(
        name="Acme",
        sector="Fintech",
        stage="mvp",
        country="CI",
        founders="Awa",       # +10
        description="pitch",  # +5
        deal_source="event",  # +5
        website_url="https://acme.ci",  # +5
        deck_status="oui",    # +5
    )
    assert compute_completeness(d) == 50 + 30


def test_social_points_breakdown():
    d = Deal(name="Acme", sector="Fintech", stage="mvp", country="CI")
    d.socials = [
        SocialProfile(network="x_twitter", value="@acme"),       # +6
        SocialProfile(network="linkedin_company", value="url"),  # +5
        SocialProfile(network="instagram", value="@a"),          # +2
    ]
    assert compute_completeness(d) == 50 + 13


def test_full_card_is_100():
    d = Deal(
        name="Acme",
        sector="Fintech",
        stage="scale",
        country="CI",
        founders="Awa",
        description="pitch",
        deal_source="event",
        website_url="https://acme.ci",
        deck_status="oui",
    )
    d.socials = [
        SocialProfile(network="x_twitter", value="@acme"),
        SocialProfile(network="linkedin_company", value="u1"),
        SocialProfile(network="linkedin_founder", value="u2"),
        SocialProfile(network="facebook", value="u3"),
        SocialProfile(network="instagram", value="u4"),
    ]
    assert compute_completeness(d) == 100


def test_blank_social_value_not_counted():
    d = Deal(name="Acme", sector="Fintech", stage="mvp", country="CI")
    d.socials = [SocialProfile(network="x_twitter", value="   ")]
    assert compute_completeness(d) == 50


def test_data_zero_mode_active():
    d = Deal(name="Acme", sector="Fintech", stage="idee", country="CI",
             website_url=None, deck_status="non")
    d.socials = []
    assert is_data_zero_mode(d) is True


def test_data_zero_exits_when_social_added():
    d = Deal(name="Acme", sector="Fintech", stage="idee", country="CI",
             website_url=None, deck_status="non")
    d.socials = [SocialProfile(network="x_twitter", value="@acme")]
    assert is_data_zero_mode(d) is False


def test_data_zero_requires_deck_non():
    d = Deal(name="Acme", sector="Fintech", stage="idee", country="CI",
             website_url=None, deck_status="en_attente")
    d.socials = []
    assert is_data_zero_mode(d) is False
