#!/usr/bin/env bash
# setup.sh
# Fitzwilliam Institute — Environment Setup
#
# Run this once to set up a clean Python virtual environment.
# Usage: bash shared/setup/setup.sh

set -e

echo "──────────────────────────────────────────"
echo "  Fitzwilliam Institute — Environment Setup"
echo "──────────────────────────────────────────"

# Check Python version
python3 --version || { echo "❌  Python 3 not found. Install from https://python.org"; exit 1; }

# Create virtual environment
echo ""
echo "Creating virtual environment (.venv)..."
python3 -m venv .venv

# Activate
echo "Activating..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r shared/setup/requirements.txt --quiet

echo ""
echo "✅  Done! Your environment is ready."
echo ""
echo "To activate in future sessions, run:"
echo "  source .venv/bin/activate   (Mac/Linux)"
echo "  .venv\\Scripts\\activate      (Windows)"
