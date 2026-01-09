#!/bin/bash
set -e

if [[ "$OSTYPE" == "msys" ]]; then
    VENV_ACTIVATE="backend/.venv/Scripts/activate"
else
    VENV_ACTIVATE="backend/.venv/bin/activate"
fi

if [ ! -d "backend/.venv" ]; then
    echo "Brak środowiska .venv! Uruchom najpierw build.sh"
    exit 1
fi

echo "=== Aktywacja środowiska ==="
source "$VENV_ACTIVATE"

echo "=== Ustawienie PYTHONPATH ==="
export PYTHONPATH="$PYTHONPATH:$(pwd)/backend"

echo "=== Uruchamianie testów z pomiarem pokrycia (Code Coverage) ==="
# --cov=backend: Mierzy pokrycie kodu w folderze 'backend'
# --cov-report=term-missing: Wyświetla raport w terminalu i pokazuje numery linii, których brakuje
# --cov-fail-under=80: Zwraca błąd (exit code 1), jeśli pokrycie jest mniejsze niż 80%
# backend/tests: Ścieżka do Twoich testów
pytest --cov=backend --cov-report=term-missing --cov-fail-under=80 backend/tests/