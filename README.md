# DealIQ

SaaS de **sourcing manuel** + **enrichissement assisté par IA** de deals VC, pour analyste junior en Côte d'Ivoire / UEMOA.

Périmètre strict à 2 modules : (1) Sourcing 100 % manuel, (2) Enrichissement assisté (Agent A).
Hors scope : scoring, pipeline, DD, IC, matching auto, veille/scraping proactif.

## Stack
- **Backend** : FastAPI + SQLAlchemy 2 + PostgreSQL, Alembic, auth JWT
- **Workers** (Phase 2) : Celery/RQ + Redis pour Agent A
- **Frontend** : React + Vite
- **LLM** : Claude API (Anthropic)

> Aucune clé d'API externe n'est requise pour l'instant : les sources d'enrichissement
> (X, LinkedIn, site, FB/IG, Crunchbase, LLM) seront branchées via des adaptateurs
> avec un **mode `mock`** (Phase 2).

## Démarrage rapide (Docker)
```bash
cp .env.example .env          # adapter SECRET_KEY, mots de passe...
docker compose up --build
# API   : http://localhost:8000
# Docs  : http://localhost:8000/docs
```
Le conteneur applique les migrations, exécute le seed CI/UEMOA puis lance l'API.

## Démarrage local (sans Docker)
```bash
cd backend
python -m venv .venv && source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Lancer Postgres (ex. via docker compose up db) puis :
export DATABASE_URL=postgresql+psycopg2://dealiq:dealiq@localhost:5432/dealiq
alembic upgrade head
python -m app.seed.seed
uvicorn app.main:app --reload
```

## Tests & lint
```bash
cd backend
pytest          # tests sur SQLite en mémoire (aucune dépendance externe)
ruff check .
```

## Auth
- Login : `POST /api/auth/login` (form `username`=email, `password`)
- Profil : `GET /api/auth/me` (Bearer token)
- Utilisateur initial créé au seed : `FIRST_USER_EMAIL` / `FIRST_USER_PASSWORD` (cf. `.env`).

## Structure
```
backend/
  app/
    api/routes/   health, auth (+ deals, enrichment en Phase 1/2)
    core/         sécurité (JWT, bcrypt)
    models/       user, reference (+ 5 entités métier en Phase 1)
    schemas/      Pydantic
    seed/         données de référence CI/UEMOA
  alembic/        migrations
  tests/
frontend/         React + Vite (scaffold)
```

## Roadmap
- **Phase 0** ✅ Fondations : monorepo, docker, FastAPI, auth, Alembic, seed CI/UEMOA
- **Phase 1** Module 1 — Sourcing manuel (5 entités, completeness_score, Mode Données Zéro)
- **Phase 2** Agent A — enrichissement multi-sources (adaptateurs mock)
- **Phase 3** Features IA (import texte, deck PDF, enrichissement guidé, notes)
- **Phase 4** Finitions MVP
