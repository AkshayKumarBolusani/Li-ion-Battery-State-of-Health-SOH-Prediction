#!/bin/bash
# Compile IEEE Paper to PDF
# Requires: pdflatex (from TeX Live or MiKTeX)

echo "Compiling IEEE Paper..."

# Run pdflatex twice for references
pdflatex ieee_paper.tex
pdflatex ieee_paper.tex

# Clean auxiliary files
rm -f *.aux *.log *.out *.bbl *.blg

echo ""
echo "Done! Output: ieee_paper.pdf"
