#!/bin/bash
set -e

FRONTEND_DIR="frontend"
DIST_DIR="$FRONTEND_DIR/dist"

echo "=== Uruchamianie Smoke Testów Frontend (Integrity Check) ==="

if [ ! -d "$DIST_DIR" ]; then
    echo "Błąd: Katalog $DIST_DIR nie istnieje. Najpierw zbuduj projekt!"
    exit 1
fi

if [ ! -f "$DIST_DIR/index.html" ]; then
    echo "Błąd: Brak pliku index.html w buildzie!"
    exit 1
fi

JS_FILES=$(find "$DIST_DIR/assets" -name "*.js" | wc -l)
if [ "$JS_FILES" -eq 0 ]; then
    echo "Błąd: Nie znaleziono plików JavaScript w assets!"
    exit 1
fi

echo "Frontend Smoke Test Passed: Build wygląda poprawnie."
