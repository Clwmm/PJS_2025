#!/bin/bash
set -e

FRONTEND_DIR="frontend"
DIST_DIR="$FRONTEND_DIR/dist"

echo "=== Installing serve globally (if not installed) ==="
npm install -g serve

if [ ! -d "$DIST_DIR" ]; then
    echo "ERROR: dist/ directory not found. Run build.sh first."
    exit 1
fi

echo "=== Running frontend on production server ==="
cd "$DIST_DIR"

# Serve static files on port 4173
serve . -l 4173
