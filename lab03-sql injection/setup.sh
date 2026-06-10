#!/usr/bin/env bash
# setup.sh — Secure Coding Lab 3 (Injection) environment preparation
#
# Creates a Python virtual environment, installs Flask, and seeds the database.
# Run once before the session.
set -e

HERE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$HERE"

echo "=== Lab 3 (Injection) setup ==="

# --- 1. Python check ---
if ! command -v python3 >/dev/null 2>&1; then
    echo "[!] python3 not found. Install: sudo apt install python3 python3-venv python3-pip"
    exit 1
fi
echo "[ok] $(python3 --version)"

# --- 2. Virtual environment ---
if [ ! -d ".venv" ]; then
    echo "[*] Creating virtual environment .venv ..."
    python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
echo "[ok] venv active"

# --- 3. Flask ---
pip install --quiet --upgrade pip
pip install --quiet flask
echo "[ok] Flask installed"

# --- 4. Seed database ---
python app/init_db.py
echo ""
echo "=== Setup complete ==="
echo "To run the app:"
echo "    source .venv/bin/activate"
echo "    python app/app.py"
echo "Then open http://127.0.0.1:5000"
echo ""
echo "To reset the database to a clean state at any time:"
echo "    python app/init_db.py"
