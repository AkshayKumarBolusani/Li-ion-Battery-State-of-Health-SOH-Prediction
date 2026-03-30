#!/bin/bash
# ============================================================
# Create Project ZIP (without .venv)
# ============================================================
# This script creates a complete zip of the project
# excluding virtual environment and cache files
#
# Usage: ./create_zip.sh
# ============================================================

set -e

cd "$(dirname "$0")"

echo "=============================================="
echo "Creating Project ZIP"
echo "=============================================="

# Output filename
OUTPUT="li-ion-battery-project.zip"

# Remove old zip if exists
rm -f "$OUTPUT"

echo ""
echo "Zipping project (this may take a few minutes)..."
echo "Excluding: .venv, __pycache__, .ipynb_checkpoints, .git"
echo ""

# Create zip excluding unnecessary files
zip -r "$OUTPUT" . \
    -x ".venv/*" \
    -x ".venv/**" \
    -x "*__pycache__*" \
    -x "*.pyc" \
    -x "*.pyo" \
    -x "*/.ipynb_checkpoints/*" \
    -x ".git/*" \
    -x ".git/**" \
    -x "*.tar" \
    -x ".DS_Store" \
    -x "li-ion-battery-project.zip"

echo ""
echo "=============================================="
echo "ZIP CREATED SUCCESSFULLY!"
echo "=============================================="
echo ""
echo "File: $OUTPUT"
echo "Size: $(du -h "$OUTPUT" | cut -f1)"
echo ""
echo "Contents include:"
echo "  - All source code (src/)"
echo "  - All notebooks (notebooks/)"
echo "  - Trained models (models/)"
echo "  - NASA datasets"
echo "  - Mendeley datasets"
echo "  - API and frontend"
echo "  - Docker files"
echo "  - Documentation"
echo ""
echo "To share:"
echo "  1. Send the zip file to others"
echo "  2. They unzip and run:"
echo "     cd 'li-ion battery'"
echo "     python -m venv .venv"
echo "     source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows"
echo "     pip install -r requirements.txt"
echo "     python main_pipeline.py"
echo ""
