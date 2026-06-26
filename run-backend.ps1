# Lance le backend DealIQ en local sur SQLite (aucune base externe requise).
# Usage :  powershell -ExecutionPolicy Bypass -File .\run-backend.ps1
$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\backend"

# Base SQLite locale (fichier dealiq.sqlite3) + secret de dev
$env:DATABASE_URL = "sqlite:///./dealiq.sqlite3"
$env:SECRET_KEY = "dev-secret-change-me"
$env:ENRICHMENT_MODE = "mock"

# Crée le venv si absent (utilise le vrai Python Windows, pas celui d'Inkscape)
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Création du venv..." -ForegroundColor Cyan
    py -3.13 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
}

Write-Host "Migrations + seed..." -ForegroundColor Cyan
.\.venv\Scripts\alembic.exe upgrade head
.\.venv\Scripts\python.exe -m app.seed.seed

Write-Host "API sur http://localhost:8000  (doc: http://localhost:8000/docs)" -ForegroundColor Green
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
