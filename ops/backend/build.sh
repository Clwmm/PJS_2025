#!/bin/bash
set -e

echo "=== Tworzenie środowiska wirtualnego (.venv) ==="
python -m venv backend/.venv

echo "=== Aktywacja środowiska ==="
source backend/.venv/bin/activate

echo "=== Instalacja zależności z requirements.txt ==="
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "=== Środowisko gotowe ==="
