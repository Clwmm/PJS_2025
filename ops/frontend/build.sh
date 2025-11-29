#!/bin/bash
set -e

echo "=== Instalacja zależności (npm install) ==="
cd frontend
npm install

echo "=== Budowanie projektu (npm run build) ==="
npm run build

echo "=== Build gotowy ==="
