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

source "$VENV_ACTIVATE"
export PYTHONPATH="$PYTHONPATH:$(pwd)/backend"

echo "=== 🔥 Uruchamianie Smoke Testów API... ==="
# -v: verbose, -s: pokazuje output (printy)
pytest backend/tests/test_smoke.py -v
