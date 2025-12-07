#!/bin/bash
set -e

if [[ "$OSTYPE" == "msys" ]]; then
    VENV_ACTIVATE="backend/.venv/Scripts/activate"
else
    VENV_ACTIVATE="backend/.venv/bin/activate"
fi

if [ ! -d "backend/.venv" ]; then
    echo "❌ Brak środowiska .venv! Uruchom najpierw build.sh"
    exit 1
fi

echo "=== Aktywacja środowiska ==="
source "$VENV_ACTIVATE"

echo "=== Uruchamianie aplikacji ==="
uvicorn backend.main:app --reload