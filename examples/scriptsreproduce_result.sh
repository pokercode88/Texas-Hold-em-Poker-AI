#!/bin/bash
# One-click reproduction script for Texas Hold'em AI
# This script will train a minimal model and evaluate its performance

set -e  # Exit on error

echo "=========================================="
echo "Texas Hold'em AI - Result Reproduction"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📌 Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
if (( $(echo "$python_version < 3.8" | bc -l) )); then
    echo -e "${RED}Error: Python 3.8+ required. Found: $python_version${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $python_version found${NC}"

# Create virtual environment
echo ""
echo "📌 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo ""
echo "📌 Installing dependencies..."
pip install --upgrade pip -q
pip install numpy scipy pytest -q
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create necessary directories
echo ""
echo "📌 Creating directories..."
mkdir -p models results logs figures
echo -e "${GREEN}✓ Directories created${NC}"

# Train a minimal model
echo ""
echo "📌 Training minimal CFR model (100 iterations)..."
echo "   This will take about 30 seconds..."
python3 scripts/minimal_train.py --iterations 100 --output models/minimal_model.bin
echo -e "${GREEN}✓ Model trained and saved to models/minimal_model.bin${NC}"

# Evaluate the model
echo ""
echo "📌 Evaluating model against random opponent..."
echo "   Running 500 games..."
python3 scripts/minimal_evaluate.py --model models/minimal_model.bin --num-games 500 --output results/reproduction_results.json

# Display results
echo ""
echo "=========================================="
echo -e "${GREEN}✅ Reproduction Complete!${NC}"
echo "=========================================="
echo ""
echo "Results saved to: results/reproduction_results.json"
echo ""
echo "To run the model interactively:"
echo "  source venv/bin/activate"
echo "  python3 examples/play_vs_ai.py"
echo ""
echo "To view results:"
echo "  cat results/reproduction_results.json"
echo ""