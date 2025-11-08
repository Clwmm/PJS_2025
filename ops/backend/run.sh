#!/bin/bash
set -e

if [ ! -d "backend/.venv" ]; then
    echo "❌ Brak środowiska .venv! Uruchom najpierw build.sh"
    exit 1
fi

echo "=== Aktywacja środowiska ==="
source backend/.venv/bin/activate

echo "=== Uruchamianie aplikacji ==="
uvicorn backend.main:app --reload
