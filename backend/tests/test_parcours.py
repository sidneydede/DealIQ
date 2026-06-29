"""Recette (Lot 5) — parcours entrepreneur de bout en bout, par type de deal.

Exerce toute la chaîne (auth réelle incluse) : inscription → connexion → entreprise →
type de deal → questionnaire/consentement → checklist adaptée → readiness → rapport → devis,
en vérifiant l'adaptation au type de deal (critères d'acceptation §13).
"""
import pytest

PDF = ("piece.pdf", b"%PDF-1.4 contenu", "application/pdf")

# (type de deal, pièce requise attendue, fragment d'instrument attendu)
CASES = [
    ("ouverture_capital", "cap_table", "equity"),
    ("dette_bancaire", "releves_bancaires", "dette"),
    ("dette_privee", "suretes", "dette"),
    ("ma", "information_memorandum", "equity"),
]


def _register_login(client, email):
    client.post("/api/v1/auth/register", json={"email": email, "password": "Password123!"})
    tokens = client.post(
        "/api/v1/auth/login", json={"email": email, "password": "Password123!"}
    ).json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.mark.parametrize("deal_type,required_doc,instrument", CASES)
def test_full_parcours_by_deal_type(client, deal_type, required_doc, instrument):
    h = _register_login(client, f"{deal_type}@dealiq.com")

    # 1. Entreprise
    cid = client.post(
        "/api/v1/companies",
        json={"name": f"Co {deal_type}", "country": "CI", "sector": "Agro"},
        headers=h,
    ).json()["company"]["id"]

    # 2. Type de deal
    r = client.post(
        f"/api/v1/companies/{cid}/deal-type",
        json={"deal_type_primary": deal_type, "amount": 80000000, "use_of_funds": "Croissance"},
        headers=h,
    )
    assert r.status_code == 200

    # 3. Checklist adaptée au type de deal
    checklist = client.get(f"/api/v1/companies/{cid}/documents/checklist", headers=h).json()
    by_type = {i["doc_type"]: i for i in checklist}
    assert required_doc in by_type and by_type[required_doc]["required"] is True
    assert by_type[required_doc]["received"] is False

    # 4. Upload d'une pièce requise -> reçue
    up = client.post(
        f"/api/v1/companies/{cid}/documents",
        data={"doc_type": required_doc},
        files={"file": PDF},
        headers=h,
    )
    assert up.status_code == 201
    checklist = client.get(f"/api/v1/companies/{cid}/documents/checklist", headers=h).json()
    assert {i["doc_type"]: i for i in checklist}[required_doc]["received"] is True

    # 5. Questionnaire + consentement + soumission (gating)
    client.put(
        f"/api/v1/companies/{cid}/questionnaire",
        json={"answers": {"amount": 80000000, "stage": "Croissance"}, "current_step": 6},
        headers=h,
    )
    client.post(
        f"/api/v1/companies/{cid}/questionnaire/consent",
        json={"consent_text": "J'accepte le traitement."},
        headers=h,
    )
    gating = client.post(f"/api/v1/companies/{cid}/questionnaire/submit", headers=h).json()
    assert gating["route"] in {"pipeline", "nurturing", "orientation_cabinet"}

    # 6. Readiness — vue entrepreneur (catégorie, jamais de score chiffré)
    score = client.post(f"/api/v1/companies/{cid}/score", headers=h).json()
    assert score["category"] is not None and "total" not in score

    # 7. Mini-rapport — instrument cohérent avec le type de deal
    report = client.get(f"/api/v1/companies/{cid}/report", headers=h).json()
    assert instrument in report["recommended_instrument"].lower()
    assert isinstance(report["blockers"], list)
    assert any("garantie de financement" in d for d in report["disclaimers"])

    # 8. Conversion — demande de devis
    quote = client.post(
        f"/api/v1/companies/{cid}/quote-request",
        json={"offer_key": "preparation"},
        headers=h,
    )
    assert quote.status_code == 201
