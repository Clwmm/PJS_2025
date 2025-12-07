#!/bin/bash
set -e

FRONTEND_DIR="frontend"

echo "=== Installing frontend dependencies ==="
cd "$FRONTEND_DIR"
npm install

echo "=== Building frontend for production ==="
npm run build

echo "=== Frontend build completed. Output is in frontend/dist ==="
