#!/bin/bash
# ============================================================
# Build and Export Docker Image for Battery SOH Predictor
# ============================================================
# Run this script to build and export the Docker image
# 
# Usage: ./build_docker.sh
# ============================================================

set -e  # Exit on error

echo "=============================================="
echo "Building Battery SOH Predictor Docker Image"
echo "=============================================="

# Navigate to project directory
cd "$(dirname "$0")"

# Build the image
echo ""
echo "Step 1: Building Docker image..."
docker build -t battery-soh-predictor:latest .

echo ""
echo "Step 2: Image built successfully!"
docker images | grep battery-soh-predictor

# Export to file
echo ""
echo "Step 3: Exporting image to file..."
docker save -o battery-soh-predictor.tar battery-soh-predictor:latest

echo ""
echo "=============================================="
echo "BUILD COMPLETE!"
echo "=============================================="
echo ""
echo "Image file: battery-soh-predictor.tar"
echo "File size: $(du -h battery-soh-predictor.tar | cut -f1)"
echo ""
echo "To share with others:"
echo "  1. Send them the .tar file"
echo "  2. They run: docker load -i battery-soh-predictor.tar"
echo "  3. They run: docker run -d -p 8000:8000 --name battery-api battery-soh-predictor"
echo "  4. Open: http://localhost:8000"
echo ""
echo "To run locally now:"
echo "  docker run -d -p 8000:8000 --name battery-api battery-soh-predictor:latest"
echo ""
