#!/bin/bash
set -e

if [[ "$OSTYPE" == "msys" ]]; then
    VENV_ACTIVATE="backend/.venv/Scripts/activate"
else
    VENV_ACTIVATE="backend/.venv/bin/activate"
fi

echo "=== Tworzenie środowiska wirtualnego (.venv) ==="
python -m venv backend/.venv

echo "=== Aktywacja środowiska ==="
source "$VENV_ACTIVATE"

echo "=== Instalacja zależności z requirements.txt ==="
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "=== Środowisko gotowe ==="