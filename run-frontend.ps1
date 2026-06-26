# Lance le frontend DealIQ (Vite). Le backend doit tourner en parallèle (run-backend.ps1).
# Usage :  powershell -ExecutionPolicy Bypass -File .\run-frontend.ps1
$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\frontend"

if (-not (Test-Path "node_modules")) {
    Write-Host "Installation des dépendances front..." -ForegroundColor Cyan
    npm install
}

Write-Host "Front sur http://localhost:5173" -ForegroundColor Green
npm run dev
