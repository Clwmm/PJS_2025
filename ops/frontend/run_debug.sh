#!/bin/bash
set -e

# Default port = 4173, or user can pass first argument: ./run.sh 5000
PORT="${1:-4173}"

FRONTEND_DIR="frontend"
DIST_DIR="$FRONTEND_DIR/dist"

if [ ! -d "$DIST_DIR" ]; then
    echo "❌ dist/ directory not found! Run build.sh first."
    exit 1
fi

echo "=== Running frontend using Vite preview (port: $PORT) ==="
cd "$FRONTEND_DIR"

npm run preview -- --port "$PORT"