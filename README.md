# DealIQ

Plateforme privée de **qualification, préparation et mise en relation** PME ↔ investisseurs
qualifiés (UEMOA / CEMAC). Boutique de conseil *tech-enabled* — pas une marketplace, pas
d'appel public à l'épargne.

> Cahier des charges de référence : [`Cahier_des_Charges_DealIQ_v1.2.md`](./Cahier_des_Charges_DealIQ_v1.2.md)

## Périmètre MVP (couche 1)

Funnel entrepreneur + cockpit cabinet minimal + reporting sponsor simple :
M1 (comptes/rôles), M2 (référentiel entreprises), M3 (onboarding/questionnaire),
M4 (documents/checklist), M5 (readiness interne), M6 (mini-rapport),
M7 (offres sur devis), M20 (CRM), M21 (reporting), M22 (admin/audit),
**M24 (type de deal — pivot du parcours)**.

## Stack

- **Backend** : Python / FastAPI · SQLAlchemy 2.0 · PostgreSQL · Alembic · JWT/RBAC
- **Frontend** : React (Vite) + TypeScript · i18n (FR par défaut) · PWA
- **Infra** : Docker Compose (Postgres, Redis), worker async (ultérieur)
- **IA** : LLM en *accélérateur* uniquement (mode mock par défaut, aucune clé requise)

## Démarrage rapide

```bash
cp .env.example .env
docker compose up --build        # API sur http://localhost:8000, docs /docs
```

### Backend en local (sans Docker)

```bash
cd backend
python -m venv .venv && . .venv/Scripts/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
python -m app.seed.seed
uvicorn app.main:app --reload
pytest
```

### Frontend

```bash
cd frontend
npm install
npm run dev          # http://localhost:5173
```

### Migrations de base de données (Alembic — autogénérées)

Le schéma est géré par des migrations Alembic **autogénérées** (les enums sont stockés
en VARCHAR + CHECK via `native_enum=False`, ce qui évite les types ENUM Postgres partagés
et fiabilise l'autogen). La metadata porte une **convention de nommage** des contraintes.

```bash
cd backend
alembic upgrade head                              # applique les migrations
# Après toute modification d'un modèle SQLAlchemy :
alembic revision --autogenerate -m "ma migration" # génère le diff
# (relire/ajuster le fichier généré, puis)
alembic upgrade head
```

> Règle : ne jamais éditer une migration déjà appliquée en prod ; toujours en créer une nouvelle.

## Organisation des lots

| Lot | Contenu |
|-----|---------|
| **0** | Fondations : repo, modèle de données, M1+M22 (auth/RBAC/audit) |
| 1 | M24 (type de deal) + M2 (référentiel entreprises) |
| 2 | M3 (onboarding) + M4 (documents/checklist) — funnel entrepreneur |
| 3 | M5 (readiness) + M6 (mini-rapport) + M7 (offres/devis) |
| 4 | Cockpit cabinet + M20 (CRM) / M21 (reporting) |
| 5 | Design system + recette (critères §13) |

**Note conformité** : vocabulaire imposé (§11) — jamais « financement garanti »,
« marketplace », « rendement ». Tout livrable IA porte un label de fiabilité et requiert
une validation humaine champ par champ.
